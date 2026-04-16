import subprocess
import os
import sys
import importlib

class Rebuilder:
    def __init__(self, build_dir="build"):
        self.build_dir = build_dir

    def rebuild(self):
        """
        Hot-swap manager that triggers the CMake build process.
        """
        print("Starting system-wide rebuild...")
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
        
        try:
            # Get pybind11 cmake dir
            pybind11_dir = subprocess.check_output([sys.executable, "-m", "pybind11", "--cmakedir"]).decode().strip()
            
            # Configure
            subprocess.run(
                ["cmake", "..", f"-Dpybind11_DIR={pybind11_dir}", f"-DCMAKE_INSTALL_PREFIX={os.getcwd()}"], 
                cwd=self.build_dir, 
                check=True,
                capture_output=True
            )
            
            # Build and install
            subprocess.run(["make", "install"], cwd=self.build_dir, check=True, capture_output=True)
            
            print("Rebuild and installation successful.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Rebuild failed with exit code {e.returncode}")
            print(f"Error: {e.stderr.decode() if e.stderr else e}")
            return False
        except Exception as e:
            print(f"Rebuild failed with unexpected error: {e}")
            return False

    def reload_module(self, module_name):
        """
        Reloads the C++ module if validation passes.
        Note: Reloading C extensions in Python can be tricky and may not always 
        reflect changes without a process restart, but we use importlib.reload 
        for the hot-swap mechanism.
        """
        try:
            if module_name in sys.modules:
                print(f"Hot-swapping: Reloading {module_name}...")
                # Remove from sys.modules to force a fresh import might be better for C extensions
                # but importlib.reload is the standard way.
                # del sys.modules[module_name]
                # return importlib.import_module(module_name)
                return importlib.reload(sys.modules[module_name])
            else:
                print(f"Initial load: Importing {module_name}...")
                return importlib.import_module(module_name)
        except Exception as e:
            print(f"Failed to reload module {module_name}: {e}")
            return None
