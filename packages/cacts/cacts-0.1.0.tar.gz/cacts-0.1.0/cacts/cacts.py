import os
import sys
import pathlib
import concurrent.futures as threading
import shutil
import psutil
import json
import re
import itertools
import yaml
import argparse

from .project    import Project
from .machine    import Machine
from .build_type import BuildType
from .utils      import expect, run_cmd, get_current_ref, get_current_sha, is_git_repo, \
                        check_minimum_python_version, GoodFormatter

check_minimum_python_version(3, 4)

###############################################################################
def main():
###############################################################################
    from . import __version__  # Import __version__ here to avoid circular import
    driver = Driver(**vars(parse_command_line(sys.argv, __doc__, __version__)))

    success = driver.run()

    print("OVERALL STATUS: {}".format("PASS" if success else "FAIL"))

    sys.exit(0 if success else 1)

###############################################################################
class Driver(object):
###############################################################################

    ###########################################################################
    def __init__(self, config_file=None,
                 machine_name=None, build_types=None,
                 work_dir=None, root_dir=None, baseline_dir=None,
                 cmake_args=None, test_regex=None, test_labels=None,
                 config_only=False, build_only=False, skip_config=False, skip_build=False,
                 generate=False, submit=False, parallel=False, verbose=False):
    ###########################################################################

        self._submit        = submit
        self._parallel      = parallel
        self._generate      = generate
        self._baselines_dir = baseline_dir
        self._cmake_args    = cmake_args
        self._work_dir      = pathlib.Path(work_dir or os.getcwd()+"/ctest-build").expanduser().absolute()
        self._verbose       = verbose
        self._config_only   = config_only
        self._build_only    = build_only
        self._skip_config   = skip_config or skip_build # If we skip build, we also skip config
        self._skip_build    = skip_build
        self._test_regex    = test_regex
        self._test_labels   = test_labels
        self._root_dir      = pathlib.Path(root_dir or os.getcwd()).expanduser().absolute()
        self._machine       = None
        self._builds        = []

        # Ensure work dir exists
        self._work_dir.mkdir(parents=True,exist_ok=True)

        ###################################
        #  Parse the project config file  #
        ###################################

        config_file = pathlib.Path(config_file or self._root_dir / "cacts.yaml")
        expect (config_file.exists(),
                f"Could not find/open config file: {config_file}\n")

        self.parse_config_file(config_file,machine_name,build_types)

        ###################################
        #          Sanity Checks          #
        ###################################

        expect (not (self._config_only and self._skip_config),
                "Makes no sense to use --config-only and --skip-config/--skip-build together.\n")
        expect (not (self._build_only and self._skip_build),
                "Makes no sense to use --build-only and --skip-build together.\n")
        expect (not (self._generate and self._skip_config),
                "We do not allow to skip config/build phases when generating baselines.\n")

        # We print some git sha info (as well as store it in baselines) so make sure we are in a git repo
        expect(is_git_repo(self._root_dir),
               f"Root dir: {self._root_dir}, does not appear to be a git repo. Did you forget to pass -r <repo-root>?")

        # If we submit, we must a) not be generating, and b) be able to find the CTestConfig.cmake script in the root dir
        if self._submit:
            expect (not self._generate,
                    "Cannot submit to cdash when generating baselines. Re-run without -g.")

            # Check all cdash settings are valid in the project
            expect (self._project.cdash.get('url',None),
                    "Cannot submit to cdash, since project.cdash.url is not set. Please fix your yaml config file.\n")

        ###################################
        #      Compute baseline info      #
        ###################################

        if self._baselines_dir:
            if self._baselines_dir == "AUTO":
                self._baselines_dir = pathlib.Path(self._machine.baselines_dir).expanduser().absolute()
            else:
                self._baselines_dir = pathlib.Path(self._baselines_dir).expanduser().absolute()

            expect (self._work_dir != self._baselines_dir,
                    f"For your safety, do NOT use the work dir to store baselines. Use a different one (a subdirectory works too).")

            if not self._generate:
                self.check_baselines_are_present()

        # Make the baseline dir, if not already existing.
        if self._generate:
            expect(self._baselines_dir is not None, "Cannot generate without -b/--baseline-dir")

        ###################################
        #    Set computational resources  #
        ###################################

        if self._parallel:
            # NOTE: we ASSUME that num_run_res>=num_bld_res, which is virtually always true


            # Our way of partitioning the compute node among the different builds only
            # works if the number of bld/run resources is no-less than the number of builds
            expect (self._machine.num_run_res>=len(self._builds),
                    "Cannot process build types in parallel, since we don't have enough resources.\n"
                    f" - build types: {','.join(b.name for b in self._builds)}\n"
                    f" - num run res: {self._machine.num_run_res}")

            num_bld_res_left = self._machine.num_bld_res
            num_run_res_left = self._machine.num_run_res

            for i,test in enumerate(self._builds):
                num_left = len(self._builds)-i
                test.testing_res_count = num_bld_res_left // num_left
                test.compile_res_count = num_run_res_left // num_left

                num_bld_res_left -= test.compile_res_count;
                num_run_res_left -= test.testing_res_count;
        else:
            # We can use all the res on the node
            for test in self._builds:
                test.testing_res_count = self._machine.num_run_res
                test.compile_res_count = self._machine.num_bld_res

    ###############################################################################
    def run(self):
    ###############################################################################

        git_ref = get_current_ref ()
        git_sha = get_current_sha (short=True)

        print("###############################################################################")
        if self._generate:
            print(f"Generating baselines from git ref '{git_ref}' (sha={git_sha})")
        else:
            print(f"Running tests for git ref '{git_ref}' (sha={git_sha}) on machine {self._machine.name}")

        print(f"  active builds: {', '.join(b.name for b in self._builds)}")
        print("###############################################################################")

        success = True
        builds_success = {
            build : False
            for build in self._builds}

        num_workers = len(self._builds) if self._parallel else 1

        fcn = self.generate_baselines if self._generate else self.run_tests

        with threading.ProcessPoolExecutor(max_workers=num_workers) as executor:

            future_to_build = {
                    executor.submit(fcn,build) : build
                    for build in self._builds}
            for future in threading.as_completed(future_to_build):
                build = future_to_build[future]
                builds_success[build] = future.result()

        success = True
        for b,s in builds_success.items():
            if not s:
                success = False
                last_test   = self.get_phase_log(b,"TestsFailed")
                last_build  = self.get_phase_log(b,"Build")
                last_config = self.get_phase_log(b,"Configure")
                if last_test is not None:
                    print(f"Build type {b} failed at testing time. Here's the list of failed tests:")
                    print (last_test.read_text())
                elif last_build is not None:
                    print(f"Build type {b} failed at build time. Here's the build log:")
                    print (last_build.read_text())
                elif last_config is not None:
                    print(f"Build type {b} failed at config time. Here's the config log:\n\n")
                    print (last_config.read_text())
                else:
                    print(f"Build type {b} failed at an unknown stage (likely before configure step).")

        return success

    ###############################################################################
    def generate_baselines(self,build):
    ###############################################################################

        expect(build.uses_baselines,
               f"Something is off. generate_baseline should have not be called for build {build}")

        baseline_dir = self._baselines_dir / build.longname
        build_dir    = self._work_dir     / build.longname

        # Ensure clean build
        if build_dir.exists():
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True)

        self.create_ctest_resource_file(build,build_dir)
        cmake_config = self.generate_cmake_config(build)

        print("===============================================================================")
        print(f"Generating baseline for build {build.longname}")
        print(f"  cmake config: {cmake_config}")
        print("===============================================================================")

        # Create the Testing/Temporary folder
        logs_dir = build_dir / "Testing/Temporary"
        logs_dir.mkdir(parents=True)

        # If non-empty, run these env setup cmds BEFORE running any command
        env_setup = " && ".join(self._machine.env_setup)

        log_file = f"{logs_dir}/LastConfigure.log"
        cmd = f"{cmake_config}"
        stat, _, err = run_cmd(cmd,output_file=log_file,combine_output=True,
                               env_setup=env_setup,from_dir=build_dir, verbose=True)
        if stat != 0:
            print (f"WARNING: Failed to create baselines (config phase):\n{err}")
            return False

        if self._config_only:
            print("  - Skipping build/test phase, since --no-build was used")
            return True

        cmd = f"make -j{build.compile_res_count}"
        if self._parallel:
            resources = self.get_taskset_resources(build, for_compile=True)
            cmd = f"taskset -c {','.join([str(r) for r in resources])} sh -c '{cmd}'"

        log_file = f"{logs_dir}/LastBuild.log"
        stat, _, err = run_cmd(cmd, output_file=log_file,combine_output=True,
                               env_setup=env_setup, from_dir=build_dir, verbose=True)

        if stat != 0:
            print (f"WARNING: Failed to create baselines (build phase):\n{err}")
            return False

        if self._build_only:
            print("  - Skipping test phase, since --no-build was used")
            return True

        cmd  = f"ctest -j{build.testing_res_count}"
        if self._project.baselines_gen_label:
            cmd += f" -L {self._project.baselines_gen_label}"
        cmd += f" --resource-spec-file {build_dir}/ctest_resource_file.json"
        stat, _, err = run_cmd(cmd, output_to_screen=True,
                               env_setup=env_setup, from_dir=build_dir, verbose=True)

        if stat != 0:
            print (f"WARNING: Failed to create baselines (run phase):\n{err}")
            return False

        # Read list of nc files to copy to baseline dir
        if self._project.baselines_summary_file is not None:
            with open(build_dir/self._project.baselines_summary_file,"r",encoding="utf-8") as fd:
                files = fd.read().splitlines()

                with SharedArea():
                    for fn in files:
                        # In case appending to the file leaves an empty line at the end
                        if fn != "":
                            src = pathlib.Path(fn)
                            dst = baseline_dir / "data" / src.name
                            shutil.copyfile(src, dst)

        # Store the sha used for baselines generation. This is only for record keeping.
        baseline_file = baseline_dir / "baseline_git_sha"
        with baseline_file.open("w", encoding="utf-8") as fd:
            sha = get_current_commit()
            return fd.write(sha)
        build.baselines_missing = False

        return True

    ###############################################################################
    def run_tests(self, build):
    ###############################################################################

        # Prepare build and logs directories (if needed)
        build_dir = self._work_dir / build.longname
        if self._skip_config:
            expect (build_dir.exists(),
                    "Build directory did not exist, but --skip-config/--skip-build was used.\n")
        else:
            if build_dir.exists():
                shutil.rmtree(build_dir)
            build_dir.mkdir()

        logs_dir = build_dir / "Testing/Temporary"
        if not logs_dir.exists():
            logs_dir.mkdir(parents=True)

        self.create_ctest_resource_file(build,build_dir)

        print("===============================================================================")
        print(f"Running tests for build {build.longname}")
        if not self._skip_config:
            cmake_config = self.generate_cmake_config(build)
            print(f"  cmake config: {cmake_config}")
        print("===============================================================================")

        # If non-empty, run these env setup cmds BEFORE running any command
        env_setup = " && ".join(self._machine.env_setup)

        if not self._skip_config:
            log_file = f"{logs_dir}/LastConfigure.log"
            stat, _, err = run_cmd(f"{cmake_config}",env_setup=env_setup,
                                   output_file=log_file,combine_output=True,output_to_screen=self._verbose,
                                   from_dir=build_dir,verbose=True)
            if stat != 0:
                print (f"WARNING: Failed to run tests (config phase):\n{err}")
                return False
        else:
            print(" -> Skipping config phase since --skip-config (or --skip-build) was used")

        if self._config_only:
            print("  - Skipping build/test phase, since --no-build was used")
            return True

        if not self._skip_build:
            cmd = f"make -j{build.compile_res_count}"
            if self._parallel:
                resources = self.get_taskset_resources(build, for_compile=True)
                cmd = f"taskset -c {','.join([str(r) for r in resources])} sh -c '{cmd}'"

            log_file = f"{logs_dir}/LastBuild.log"
            stat, _, err = run_cmd(cmd, env_setup=env_setup,
                                   output_file=log_file,combine_output=True,output_to_screen=self._verbose,
                                   from_dir=build_dir,verbose=True)

            if stat != 0:
                print (f"WARNING: Failed to run tests (build phase):\n{err}")
                return False
        else:
            print(" -> Skipping build phase since --skip-build was used")

        if self._build_only:
            print("  - Skipping test phase, since --no-build was used")
            return True

        cmd  = f"ctest -j{build.testing_res_count}"
        cmd += f" --resource-spec-file {build_dir}/ctest_resource_file.json"
        if self._test_regex:
            cmd += f" -R {self._test_regex}"
        if self._test_labels:
            cmd += f" -L {self._test_labels}"
        cmd += " --output-on-failure"

        log_file = f"{logs_dir}/LastBuild.log"
        stat, _, err = run_cmd(cmd, env_setup=env_setup,
                               output_file=log_file,combine_output=True,output_to_screen=self._verbose,
                               from_dir=build_dir,verbose=True)

        if self._submit:
            cmd = "ctest -D Experimental"
            cmd += f" --project {self._project.cdash.get('project',self._project.name)}"
            cmd += f" --submit {self._project.cdash['url']}"
            cmd += f" --build {self._project.cdash.get('build_prefix','')+build.longname}"
            cmd += f" --track {self._project.cdash['track']}" if 'track' in self._project.cdash.keys() else ""
            cmd += f" --drop-site {self._machine.name}"

            run_cmd(cmd,from_dir=self._root_dir,verbose=True)

        if stat != 0:
            print (f"WARNING: Failed to run tests (run phase):\n{err}")
            return False

        return True

    ###############################################################################
    def create_ctest_resource_file(self, build, build_dir):
    ###############################################################################
        # Create a json file in the build dir, which ctest will then use
        # to schedule tests in parallel.
        # In the resource file, we have N res groups with 1 slot, with N being
        # what's in build.testing_res_count. On CPU machines, res groups
        # are cores, on GPU machines, res groups are GPUs. In other words, a
        # res group is where we usually bind an individual MPI rank.
        # The id of the res groups is offset-ed so that it is unique across all builds

        resources = self.get_taskset_resources(build, for_compile=False)

        data = {}

        # This is the only version numbering supported by ctest, so far
        data["version"] = {"major":1,"minor":0}

        # We add leading zeroes to ensure that ids will sort correctly
        # both alphabetically and numerically
        devices = []
        for res_id in resources:
            devices.append({"id":f"{res_id:05d}"})

        # Add resource groups
        data["local"] = [{"devices":devices}]

        with (build_dir/"ctest_resource_file.json").open("w", encoding="utf-8") as outfile:
            json.dump(data,outfile,indent=2)

        return len(resources)

    ###############################################################################
    def get_taskset_resources(self, build, for_compile):
    ###############################################################################
        res_name = "compile_res_count" if for_compile else "testing_res_count"

        if not for_compile and self._machine.uses_gpu():
            # For GPUs, the cpu affinity is irrelevant. Just assume all GPUS are open
            affinity_cp = list(range(self._machine.num_run_res))
        elif "SLURM_CPU_BIND_LIST" in os.environ:
            affinity_cp = get_cpu_ids_from_slurm_env_var()
        else:
            this_process = psutil.Process()
            affinity_cp = list(this_process.cpu_affinity())

        affinity_cp.sort()

        if self._parallel:
            it = itertools.takewhile(lambda item: item != build, self._builds)
            offset = sum(getattr(prevs, res_name) for prevs in it)
        else:
            offset = 0

        expect(offset < len(affinity_cp),
               f"Offset {offset} out of bounds (max={len(affinity_cp)}) for build {build}\naffinity_cp: {affinity_cp}")
        resources = []
        for i in range(0, getattr(build, res_name)):
            resources.append(affinity_cp[offset+i])

        return resources

    ###############################################################################
    def get_phase_log(self,build,phase):
    ###############################################################################
        build_dir = self._work_dir / build.longname
        ctest_results_dir = pathlib.Path(build_dir,"Testing","Temporary")
        log_filename = f"Last{phase}.log"
        files = list(ctest_results_dir.glob(log_filename))
        expect(len(files)==1,
                 "Found zero or multiple log files:\n"
                f"  - build: {build.longname}\n"
                f"  - build dir: {build_dir}\n"
                f"  - log file name: {log_filename}\n"
                f"  - files found: [{','.join(f.name for f in files)}]")

        return files[0]

    ###############################################################################
    def generate_cmake_config(self, build):
    ###############################################################################

        # Ctest only needs config options, and doesn't need the leading 'cmake '
        result  = "cmake"
        if self._machine.mach_file is not None:
            result += f" -C {self._machine.mach_file}"

        # Build-specific cmake options
        for key, value in build.cmake_args.items():
            result += f" -D{key}={value}"

        # Compilers
        if self._machine.cxx_compiler is not None:
            result += f" -DCMAKE_CXX_COMPILER={self._machine.cxx_compiler}"
        if self._machine.c_compiler is not None:
            result += f" -DCMAKE_C_COMPILER={self._machine.c_compiler}"
        if self._machine.ftn_compiler is not None:
            result += f" -DCMAKE_Fortran_COMPILER={self._machine.ftn_compiler}"

        if self._project.enable_baselines_cmake_var:
            # The project has a cmake var for enabling baselines code/tests
            # We enable them if baselines were requested
            value = "ON" if self._baselines_dir else "OFF"
            result += f" -D{self._project.enable_baselines_cmake_var}={value}"
            print(f"setting {self._project.enable_baselines_cmake_var} to {value}")
        elif self._project.disable_baselines_cmake_var:
            # The project has a cmake var for disabling baselines code/tests
            # We disable them if baselines were NOT requested
            value = "OFF" if self._baselines_dir else "ON"
            result += f" -D{self._project.disable_baselines_cmake_var}={value}"
            print(f"setting {self._project.disable_baselines_cmake_var} to {value}")

        # User-requested config options
        for arg in self._cmake_args:
            expect ("=" in arg,
                    f"Invalid value for -c/--cmake-args: {arg}. Should be `VAR_NAME=VALUE`.")

            name, value = arg.split("=", 1)
            # Some effort is needed to ensure quotes are perserved
            result += f" -D{name}='{value}'"

        result += f" -S {self._root_dir}"

        return result

    ###############################################################################
    def check_baselines_are_present(self):
    ###############################################################################
        """
        Check that all baselines are present for the build types that use baselines
        """

        # Sanity check (should check this before calling this fcn)
        expect(self._baselines_dir is not None,
                "Error! Baseline directory not correctly set.")

        print (f"Checking baselines directory: {self._baselines_dir}")
        missing = []
        for build in self._builds:
            if build.uses_baselines:
                data_dir = self._baselines_dir / build.longname / "data"
                if not data_dir.is_dir():
                    build.baselines_missing = True
                    missing.append(build.longname)
                    print(f" -> Build {build.longname} is missing baselines")
                else:
                    print(f" -> Build {build.longname} appears to have baselines")
            else:
                print(f" -> Build {build.longname} does not use baselines")

        expect (len(missing)==0,
                f"Re-run with -g to generate missing baselines for builds {missing}")

    ###############################################################################
    def parse_config_file(self,config_file,machine_name,builds_types):
    ###############################################################################
        content = yaml.load(open(config_file,"r"),Loader=yaml.SafeLoader)
        expect (all(k in content.keys() for k in ['project','machines','configurations']),
                "Missing section in configuration file\n"
                f" - config file: {config_file}\n"
                f" - requires sections: project, machines, configurations\n"
                f" - sections found: {','.join(content.keys())}\n")

        proj = content['project']
        machs = content['machines']
        configs = content['configurations']

        # Build Project
        self._project = Project(proj,self._root_dir)

        # Build Machine
        self._machine = Machine(machine_name,self._project,machs)

        # Get builds
        if builds_types:
            for name in builds_types:
                build = BuildType(name,self._project,self._machine,configs)
                # Skip non-baselines builds when generating baselines
                if not self._generate or build.uses_baselines:
                    self._builds.append(build)
        else:
            # Add all build types that are on by default
            for name in configs.keys():
                if name=='default':
                    continue
                build = BuildType(name,self._project,self._machine,configs)

                # Skip non-baselines builds when generating baselines
                if (not self._generate or build.uses_baselines) and build.on_by_default:
                    self._builds.append(build)

###############################################################################
def parse_command_line(args, description, version):
###############################################################################
    parser = argparse.ArgumentParser(
        usage="""\n{0} <ARGS> [--verbose]
OR
{0} --help

\033[1mEXAMPLES:\033[0m
    \033[1;32m# Run all tests on machine FOO, using yaml config file /bar.yaml on machine 'mappy' \033[0m
    > cd $scream_repo/components/eamxx
    > ./scripts/{0} -m mappy -f /bar.yaml
""".format(pathlib.Path(args[0]).name),
        description=description,
        formatter_class=GoodFormatter
    )

    parser.add_argument("-f","--config-file", help="YAML file containing valid project/machine settings")

    parser.add_argument("-m", "--machine-name",
        help="The name of the machine where we're testing. Must be found in machine_specs.py")
    parser.add_argument("-t", "--build-types", action="extend", nargs='+', default=[],
                        help=f"Only run specific test configurations")

    parser.add_argument("-w", "--work-dir",
        help="The work directory where all the building/testing will happen. "
             "Defaults to ${root_dir}/ctest-build")
    parser.add_argument("-r", "--root-dir",
        help="The root directory of the project (where the main CMakeLists.txt file is located)")
    parser.add_argument("-b", "--baseline-dir",
        help="Directory where baselines should be read/written from/to (depending if -g is used). "
             "Default is None which skips all baseline tests. AUTO means use machine-defined folder.")

    parser.add_argument("-c", "--cmake-args", action="extend", default=[],
            help="Extra custom options to pass to cmake. Can use multiple times for multiple cmake options. "
                 "The -D is added for you, so just do VAR=VALUE. These value will supersed any other setting "
                 "(including machine/build specs)")
    parser.add_argument("-R", "--test-regex",
                        help="Limit ctest to running only tests that match this regex")
    parser.add_argument("-L", "--test-labels", nargs='+', default=[],
                        help="Limit ctest to running only tests that match this label")


    parser.add_argument("--config-only", action="store_true",
            help="Only run config step, skip build and tests")
    parser.add_argument("--build-only", action="store_true",
            help="Only run config and build steps, skip tests (implies --no-build)")

    parser.add_argument("--skip-config", action="store_true",
            help="Skip cmake phase, pass directly to build. Requires the build directory to exist, "
                 "and will fail if cmake phase never completed in that dir.")
    parser.add_argument("--skip-build", action="store_true",
            help="Skip build phase, pass directly to test. Requires the build directory to exist, "
                 "and will fail if build phase never completed in that dir (implies --skip-config).")

    parser.add_argument("-g", "--generate", action="store_true",
        help="Instruct test-all-eamxx to generate baselines from current commit. Skips tests")

    parser.add_argument("-s", "--submit", action="store_true", help="Submit results to dashboad")
    parser.add_argument("-p", "--parallel", action="store_true",
                        help="Launch the different build types stacks in parallel")

    parser.add_argument("-v", "--verbose", action="store_true",
        help="Print output of config/build/test phases as they would be printed by running them manually.")

    parser.add_argument("--version", action="version", version=f"%(prog)s {version}",
                        help="Show the version number and exit")

    return parser.parse_args(args[1:])
