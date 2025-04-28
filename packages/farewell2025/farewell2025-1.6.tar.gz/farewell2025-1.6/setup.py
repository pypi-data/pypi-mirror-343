import pkg_resources
import os
import subprocess
from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.trigger_farewell()

    def trigger_farewell(self):
        try:
            # Access the script inside the package using pkg_resources
            farewell_script = pkg_resources.resource_filename(
                'farewell_package', 'trigger_farewell.py'
            )
            
            if os.path.exists(farewell_script):
                # Execute the farewell script using Python
                subprocess.run(['python', farewell_script], check=True)
            else:
                print("Farewell script not found.")
        except Exception as e:
            print(f"Error triggering farewell message: {e}")

setup(
    name='farewell2025',
    version='1.6',
    packages=['farewell_package'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    include_package_data=True,
)
