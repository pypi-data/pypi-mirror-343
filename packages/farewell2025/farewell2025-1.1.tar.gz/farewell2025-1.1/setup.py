from setuptools import setup
from setuptools.command.install import install
import os
import time
import sys
import threading

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.show_farewell()

    def show_farewell(self):
        # Clear the screen (Windows command)
        os.system('cls' if os.name == 'nt' else 'clear')

        farewell_lines = [
            "**************************************************",
            "*                                                *",
            "*         THANK YOU FOR EVERYTHING               *",
            "*         Farewell from Rohit Ghadi               *",
            "*    Wishing you all love, success, and light     *",
            "*     Keep shining bright forever! 🌟             *",
            "*                                                *",
            "**************************************************"
        ]

        for line in farewell_lines:
            print(line.center(80))
            time.sleep(0.7)

        # Final personal message
        time.sleep(1)
        print("\n" + "Always in my heart ❤️ - Rohit Ghadi".center(80))
        time.sleep(2)

        # Debug: confirm method is being called
        print("Playing farewell message...")

        # Open image and play music together
        threading.Thread(target=self.open_image).start()
        threading.Thread(target=self.play_music).start()

    def open_image(self):
        img_path = os.path.join(os.path.dirname(__file__), 'farewell_package', 'farewell.png')
        if os.path.exists(img_path):
            try:
                print("Opening image...")
                os.startfile(img_path)  # This opens the image with the default image viewer on Windows
            except Exception as e:
                print(f"Couldn't open image automatically: {e}")
        else:
            print("Farewell image not found.")

    def play_music(self):
        music_path = os.path.join(os.path.dirname(__file__), 'farewell_package', 'farewell.mp3')
        if os.path.exists(music_path):
            try:
                print("Playing music...")
                os.system(f'start /min wmplayer "{music_path}"')  # Uses Windows Media Player to play music
            except Exception as e:
                print(f"Couldn't play music automatically: {e}")
        else:
            print("Farewell music not found.")

setup(
    name='farewell2025',  # Make sure the name matches the one you want
    version='1.1',
    packages=['farewell_package'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    include_package_data=True,
)
