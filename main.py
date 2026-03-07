#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys

APP_NAME = "ATIF Downloader v8"

GREEN="\033[92m"
RED="\033[91m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"


def banner():
    os.system("clear")
    print(CYAN + "="*50)
    print(APP_NAME.center(50))
    print("="*50 + RESET)


def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print(RED+"yt-dlp install nahi hai"+RESET)
        sys.exit()


def get_folder():

    home=os.path.expanduser("~")

    if os.path.exists(home+"/Desktop"):
        path=home+"/Desktop/ATIF_Downloader"
    else:
        path=home+"/Downloads/ATIF_Downloader"

    os.makedirs(path,exist_ok=True)

    return path


def get_available_qualities(link):

    result=subprocess.run(
        ["yt-dlp","-F",link],
        capture_output=True,
        text=True
    )

    lines=result.stdout.splitlines()

    qualities={}

    for line in lines:

        if "360p" in line and "360p" not in qualities:
            qualities["1"]=("360p",line.split()[0])

        elif "720p" in line and "720p" not in qualities:
            qualities["2"]=("720p",line.split()[0])

        elif "1080p" in line and "1080p" not in qualities:
            qualities["3"]=("1080p",line.split()[0])

    return qualities


def show_menu(q):

    print(YELLOW+"\nAvailable Qualities:\n"+RESET)

    for key,val in q.items():
        print(f"{key}. {val[0]}")


def download(link,format_code,folder):

    print(GREEN+"\nDownloading...\n"+RESET)

    cmd=[
        "yt-dlp",
        "-f",format_code,
        "-o",f"{folder}/%(title)s.%(ext)s",
        "--merge-output-format","mp4",
        link
    ]

    subprocess.run(cmd)

    print(GREEN+"\nDownload Completed\n"+RESET)
    print("Saved in:",folder)


def main():

    check_yt_dlp()

    while True:

        banner()

        link=input("Paste Video Link: ").strip()

        qualities=get_available_qualities(link)

        if not qualities:
            print(RED+"No supported quality found"+RESET)
            input("Enter press...")
            continue

        show_menu(qualities)

        choice=input("\nSelect quality: ")

        if choice not in qualities:
            print(RED+"Invalid option"+RESET)
            input("Enter press...")
            continue

        format_code=qualities[choice][1]

        folder=get_folder()

        download(link,format_code,folder)

        again=input("\nDownload another video? (y/n): ")

        if again.lower()!="y":
            break


if __name__=="__main__":
    main()
