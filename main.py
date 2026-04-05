#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys
import time

APP_NAME = "ATIF DOWNLOADER v14 STABLE"

GREEN="\033[92m"
RED="\033[91m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"


def banner():
    os.system("clear")

    print(CYAN)
    print("╔════════════════════════════════════════════╗")
    print("║      🚀 ATIF DOWNLOADER v14 STABLE 🚀      ║")
    print("║          👑 CREATED BY ATIF 👑            ║")
    print("║   ⚡ AUTO BEST QUALITY | NO STUCK ⚡      ║")
    print("╚════════════════════════════════════════════╝")
    print(RESET)


def check_dependencies():
    if not shutil.which("yt-dlp"):
        print(RED+"Install yt-dlp: sudo apt install yt-dlp"+RESET)
        sys.exit()

    if not shutil.which("ffmpeg"):
        print(RED+"Install ffmpeg: sudo apt install ffmpeg"+RESET)
        sys.exit()


def validate_link(link):
    return "youtube.com" in link or "youtu.be" in link


def get_folder():
    home=os.path.expanduser("~")

    if os.path.exists(home+"/Desktop"):
        folder=home+"/Desktop/ATIF_Downloader"
    else:
        folder=home+"/Downloads/ATIF_Downloader"

    os.makedirs(folder,exist_ok=True)
    return folder


def download(link, folder):

    print(GREEN+"\n🚀 Starting Smart Download...\n"+RESET)

    cmd = [
        "yt-dlp",

        # 🔥 BEST + FAST + STABLE
        "-f", "bv*+ba/b",

        "-o", f"{folder}/%(title)s.%(ext)s",

        "--merge-output-format", "mp4",

        # 🔥 SPEED + STABILITY OPTIONS
        "--no-playlist",
        "--concurrent-fragments", "5",
        "--retries", "10",
        "--fragment-retries", "10",
        "--retry-sleep", "2",

        "--buffer-size", "16K",
        "--http-chunk-size", "1M",

        "--no-warnings",
        "--progress"
    ]

    subprocess.run(cmd)

    print(GREEN+"\n✅ Download Completed"+RESET)
    print("📁 Saved in:", folder)


def main():
    check_dependencies()

    while True:
        banner()

        link = input("📌 Paste YouTube Link: ").strip()

        if not validate_link(link):
            print(RED+"Invalid link"+RESET)
            input("Press Enter...")
            continue

        folder = get_folder()

        download(link, folder)

        again = input("\n🔁 Download another? (y/n): ")

        if again.lower() != "y":
            print(GREEN+"\n❤️ Thanks for using ATIF Downloader"+RESET)
            break


if __name__ == "__main__":
    main()
