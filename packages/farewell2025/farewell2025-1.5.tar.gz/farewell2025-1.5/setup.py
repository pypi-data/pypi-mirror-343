from setuptools import setup
from setuptools.command.install import install
import os
import subprocess

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.trigger_farewell()

    def trigger_farewell(self):
        # Path to the trigger_farewell.py script in the installed package
        farewell_script = os.path.join(os.path.dirname(__file__), 'farewell_package', 'trigger_farewell.py')

        if os.path.exists(farewell_script):
            try:
                # Execute the farewell script using Python
                subprocess.run(['python', farewell_script], check=True)
            except Exception as e:
                print(f"Error triggering farewell message: {e}")
        else:
            print("Farewell script not found.")

setup(
    name='farewell2025',
    version='1.5',
    packages=['farewell_package'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    include_package_data=True,
)
