import subprocess
import os
import shutil

class Validator:
    def __init__(self, build_dir="build_sandbox"):
        self.build_dir = build_dir

    def validate(self, mutated_file_path, original_file_path):
        # Create a sandbox directory
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

        # Copy the whole project to sandbox, but replace the file with mutation
        # Actually, it might be easier to just try to compile the project in the current state but with the mutated file,
        # and if it fails, revert.
        
        # But "sandbox compilation" suggests we shouldn't mess with the main project yet.
        # Let's try a simple approach: copy the source to a temp location, swap the file, and try to build.
        
        sandbox_src = os.path.join(self.build_dir, "src")
        shutil.copytree("src", sandbox_src)
        shutil.copytree("include", os.path.join(self.build_dir, "include"))
        shutil.copy("CMakeLists.txt", self.build_dir)
        
        # Replace the file in sandbox
        rel_path = os.path.relpath(original_file_path, ".")
        target_path = os.path.join(self.build_dir, rel_path)
        
        with open(mutated_file_path, 'r') as f:
            mutated_code = f.read()
        
        with open(target_path, 'w') as f:
            f.write(mutated_code)
            
        # Try to build in sandbox
        try:
            build_path = os.path.join(self.build_dir, "build")
            os.makedirs(build_path)
            
            import sys
            import subprocess
            pybind11_dir = subprocess.check_output([sys.executable, "-m", "pybind11", "--cmakedir"]).decode().strip()

            subprocess.run(["cmake", "..", f"-Dpybind11_DIR={pybind11_dir}"], cwd=build_path, check=True, capture_output=True)
            subprocess.run(["make"], cwd=build_path, check=True, capture_output=True)

        # Smoke test: try to run tests if they exist
            # For now, let's just say if it compiles, it passes basic validation
            print(f"Validation passed for {mutated_file_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Validation failed: {e.stderr.decode()}")
            return False
        finally:
            # Cleanup sandbox
            # shutil.rmtree(self.build_dir)
            pass
