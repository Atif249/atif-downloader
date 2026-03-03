
#!/usr/bin/env python3

import subprocess
import sys
import shutil
import os

APP_NAME = "ATIF Downloader v5"

# Terminal Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def banner():
    os.system("clear")
    print(CYAN + "=" * 50)
    print(f"{APP_NAME.center(50)}")
    print("=" * 50 + RESET)


def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print(RED + "\n[ERROR] yt-dlp installed nahi hai!" + RESET)
        print("Install karo:")
        print("Termux: pkg install yt-dlp")
        print("Kali/Linux: sudo apt install yt-dlp")
        sys.exit(1)


def show_quality_menu():
    print(YELLOW + "\nSelect Video Quality:" + RESET)
    print("1. 360p")
    print("2. 720p")
    print("3. 1080p")
    print("4. Best Available")


def get_format(choice):
    formats = {
        "1": "18",
        "2": "22",
        "3": "137+140",
        "4": "bestvideo+bestaudio"
    }
    return formats.get(choice)


def download_video(link, format_code):
    try:
        command = [
            "yt-dlp",
            "-f", format_code,
            "--merge-output-format", "mp4",
            "--newline",
            link
        ]

        print(GREEN + "\n⏳ Download Starting...\n" + RESET)
        subprocess.run(command, check=True)

        print(GREEN + "\n✅ Download Completed Successfully!" + RESET)

    except subprocess.CalledProcessError:
        print(RED + "\n❌ Download Failed!" + RESET)

    except KeyboardInterrupt:
        print(YELLOW + "\n\n⚠ Download Cancelled by User!" + RESET)


def main():
    check_yt_dlp()

    while True:
        banner()

        link = input("\nPaste Video Link Here: ").strip()

        if not link:
            print(RED + "❌ Invalid Link!" + RESET)
            input("\nPress Enter to continue...")
            continue

        show_quality_menu()
        choice = input("\nEnter option (1-4): ").strip()

        format_code = get_format(choice)

        if not format_code:
            print(RED + "❌ Invalid Selection!" + RESET)
            input("\nPress Enter to continue...")
            continue

        download_video(link, format_code)

        again = input(
            CYAN + "\nDo you want to download another video? (y/n): " + RESET
        ).lower()

        if again != "y":
            print(GREEN + "\nThanks for using ATIF Downloader ❤️" + RESET)
            break


if _name_ == "_main_":
    main()
