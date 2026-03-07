#!/usr/bin/env python3

import subprocess
import sys
import shutil
import os
import time
import threading

APP_NAME = "ATIF Downloader v7"

# Terminal Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def banner():
    os.system("clear")
    print(CYAN + "=" * 50)
    print(APP_NAME.center(50))
    print("=" * 50 + RESET)


def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print(RED + "\nyt-dlp installed nahi hai!" + RESET)
        sys.exit(1)


def get_download_folder():
    home = os.path.expanduser("~")

    if os.path.exists(os.path.join(home, "Desktop")):
        folder = os.path.join(home, "Desktop", "ATIF_Downloader")
    else:
        folder = os.path.join(home, "Downloads", "ATIF_Downloader")

    os.makedirs(folder, exist_ok=True)
    return folder


def show_formats(link):
    print(YELLOW + "\nFetching available qualities...\n" + RESET)
    subprocess.run(["yt-dlp", "-F", link])


# Stylish loading animation
def loading_animation(stop_event):
    symbols = ["|", "/", "-", "\\"]
    i = 0

    while not stop_event.is_set():
        sys.stdout.write(
            CYAN + f"\rPreparing Download {symbols[i % len(symbols)]}" + RESET
        )
        sys.stdout.flush()
        i += 1
        time.sleep(0.2)


def download_video(link, format_code, folder):

    stop_event = threading.Event()
    t = threading.Thread(target=loading_animation, args=(stop_event,))
    t.start()

    time.sleep(3)   # animation duration
    stop_event.set()
    t.join()

    print(GREEN + "\n\n🚀 Download Started...\n" + RESET)

    command = [
        "yt-dlp",
        "-f", format_code,
        "-o", f"{folder}/%(title)s.%(ext)s",
        "--merge-output-format", "mp4",
        link
    ]

    subprocess.run(command)

    print(GREEN + f"\n✅ Download Completed!\nSaved in: {folder}" + RESET)


def main():

    check_yt_dlp()

    while True:

        banner()

        link = input("\nPaste Video Link: ").strip()

        if not link:
            print(RED + "Invalid link!" + RESET)
            continue

        show_formats(link)

        format_code = input(
            CYAN + "\nEnter format code: " + RESET
        ).strip()

        folder = get_download_folder()

        download_video(link, format_code, folder)

        again = input(
            CYAN + "\nDownload another video? (y/n): " + RESET
        ).lower()

        if again != "y":
            print(GREEN + "\nThanks for using ATIF Downloader ❤️" + RESET)
            break


if __name__ == "__main__":
    main()
