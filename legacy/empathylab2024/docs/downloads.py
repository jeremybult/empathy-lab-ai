import subprocess
import sys

class download:
    @staticmethod
    def package(package_name):
        command = [sys.executable, "-m", "pip", "install", package_name]

        try:
            subprocess.check_call(command)
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}: {e}")

download.package("flask")
