import os
import time
import sys
import threading
import pkg_resources  # To access package data in the installed package

def show_farewell():
    # Clear the screen
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

    # Thank you message
    print("\nThank you for being part of my journey 🙏 - Rohit Ghadi".center(80))
    time.sleep(2)

    # Open image and play music together
    threading.Thread(target=open_image).start()
    threading.Thread(target=play_music).start()

def open_image():
    try:
        # Use pkg_resources to load the image file from the package
        img_path = pkg_resources.resource_filename('farewell_package', 'farewell.png')
        if os.path.exists(img_path):
            if os.name == 'nt':
                os.startfile(img_path)
            elif sys.platform == 'darwin':
                os.system(f'open "{img_path}"')
            else:
                os.system(f'xdg-open "{img_path}"')
        else:
            print("Farewell image not found.")
    except Exception as e:
        print(f"Error opening image: {e}")

def play_music():
    try:
        # Use pkg_resources to load the music file from the package
        music_path = pkg_resources.resource_filename('farewell_package', 'farewell.mp3')
        if os.path.exists(music_path):
            if os.name == 'nt':
                os.system(f'start /min wmplayer "{music_path}"')
            elif sys.platform == 'darwin':
                os.system(f'afplay "{music_path}"')
            else:
                os.system(f'xdg-open "{music_path}"')
        else:
            print("Farewell music not found.")
    except Exception as e:
        print(f"Error playing music: {e}")

if __name__ == "__main__":
    show_farewell()
