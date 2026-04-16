import subprocess
import os
import sys
import importlib

class Rebuilder:
    def __init__(self, build_dir="build"):
        self.build_dir = build_dir

    def rebuild(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
        
        try:
            # Get pybind11 cmake dir
            import subprocess
            pybind11_dir = subprocess.check_output([sys.executable, "-m", "pybind11", "--cmakedir"]).decode().strip()
            
            subprocess.run(["cmake", "..", f"-Dpybind11_DIR={pybind11_dir}", f"-DCMAKE_INSTALL_PREFIX={os.getcwd()}"], cwd=self.build_dir, check=True)
            subprocess.run(["make", "install"], cwd=self.build_dir, check=True)
            print("Rebuild successful.")
            return True
        except Exception as e:
            print(f"Rebuild failed: {e}")
            return False

    def reload_module(self, module_name):
        if module_name in sys.modules:
            print(f"Reloading {module_name}...")
            return importlib.reload(sys.modules[module_name])
        else:
            print(f"Importing {module_name}...")
            return importlib.import_module(module_name)
