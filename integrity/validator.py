import subprocess
import os
import shutil
import sys

class Validator:
    def __init__(self, build_dir="build_sandbox"):
        self.build_dir = build_dir

    def validate(self, mutated_file_path, original_file_path):
        """
        Runs a sandbox compilation and smoke tests for any generated mutation.
        """
        print(f"Validating mutation {mutated_file_path} for {original_file_path}...")
        
        # Create a sandbox directory
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

        try:
            # Copy necessary files to sandbox
            shutil.copytree("src", os.path.join(self.build_dir, "src"))
            shutil.copytree("include", os.path.join(self.build_dir, "include"))
            shutil.copy("CMakeLists.txt", self.build_dir)
            
            # Replace the file in sandbox with the mutated version
            rel_path = os.path.relpath(original_file_path, ".")
            target_path = os.path.join(self.build_dir, rel_path)
            
            # Ensure the directory exists in sandbox
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            shutil.copy(mutated_file_path, target_path)
                
            # Try to build in sandbox
            build_path = os.path.join(self.build_dir, "build")
            os.makedirs(build_path)
            
            pybind11_dir = subprocess.check_output([sys.executable, "-m", "pybind11", "--cmakedir"]).decode().strip()

            # Run CMake
            cmake_res = subprocess.run(
                ["cmake", "..", f"-Dpybind11_DIR={pybind11_dir}"], 
                cwd=build_path, 
                capture_output=True, 
                text=True
            )
            if cmake_res.returncode != 0:
                print(f"CMake failed:\n{cmake_res.stderr}")
                return False

            # Run Make
            make_res = subprocess.run(
                ["make"], 
                cwd=build_path, 
                capture_output=True, 
                text=True
            )
            if make_res.returncode != 0:
                print(f"Make failed:\n{make_res.stderr}")
                return False

            # Smoke test: try to run the compiled module
            print("Compilation successful. Running smoke tests...")
            
            # Find the built .so file
            so_file = None
            for f in os.listdir(build_path):
                if f.endswith(".so"):
                    so_file = f
                    break
            
            if not so_file:
                # Try in subdirectories if any
                for root, dirs, files in os.walk(build_path):
                    for f in files:
                        if f.endswith(".so"):
                            so_file = os.path.join(root, f)
                            break
                    if so_file: break

            if not so_file:
                print("Could not find built .so file for smoke test.")
                return False
            
            # Run a python script that imports the module and calls a function
            # We add build_path to PYTHONPATH
            env = os.environ.copy()
            env["PYTHONPATH"] = build_path + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")
            
            smoke_test_script = """
import sys
try:
    import wraith_core
    engine = wraith_core.WraithEngine("SmokeTest")
    res = engine.process_data("test_payload")
    print(f"Smoke test success: {res}")
    if "test_payload" not in res:
        print("Smoke test failed: unexpected output")
        sys.exit(1)
except Exception as e:
    print(f"Smoke test failed with exception: {e}")
    sys.exit(1)
"""
            smoke_res = subprocess.run(
                [sys.executable, "-c", smoke_test_script], 
                env=env,
                capture_output=True, 
                text=True
            )
            
            if smoke_res.returncode != 0:
                print(f"Smoke test failed:\n{smoke_res.stderr}\n{smoke_res.stdout}")
                return False
            
            print(f"Smoke test passed: {smoke_res.stdout.strip()}")
            return True

        except Exception as e:
            print(f"Validation failed with unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Cleanup sandbox could be done here if desired
            pass
