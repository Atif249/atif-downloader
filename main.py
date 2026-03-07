#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys
import time
import threading

APP_NAME = "ATIF Downloader v10"

# Colors
GREEN="\033[92m"
RED="\033[91m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"


def banner():
    os.system("clear")
    print(CYAN+"="*50)
    print(APP_NAME.center(50))
    print("="*50+RESET)


def check_yt_dlp():
    if not shutil.which("yt-dlp"):
        print(RED+"yt-dlp install nahi hai"+RESET)
        print("Install karo:")
        print("Termux: pkg install yt-dlp")
        print("Linux: sudo apt install yt-dlp")
        sys.exit()


def validate_link(link):

    if "youtube.com" in link or "youtu.be" in link:
        return True
    return False


def get_folder():

    home=os.path.expanduser("~")

    if os.path.exists(home+"/Desktop"):
        folder=home+"/Desktop/ATIF_Downloader"
    else:
        folder=home+"/Downloads/ATIF_Downloader"

    os.makedirs(folder,exist_ok=True)

    return folder


def get_qualities(link):

    result=subprocess.run(
        ["yt-dlp","-F",link],
        capture_output=True,
        text=True
    )

    lines=result.stdout.splitlines()

    q={}
    count=1

    for line in lines:

        if "360p" in line and "360p" not in str(q.values()):
            q[str(count)]=("360p",line.split()[0])
            count+=1

        elif "720p" in line and "720p" not in str(q.values()):
            q[str(count)]=("720p",line.split()[0])
            count+=1

        elif "1080p" in line and "1080p" not in str(q.values()):
            q[str(count)]=("1080p",line.split()[0])
            count+=1

    return q


def show_menu(q):

    print(YELLOW+"\nAvailable Qualities:\n"+RESET)

    for k,v in q.items():
        print(f"{k}. {v[0]}")


def loading_animation(stop):

    symbols=["|","/","-","\\"]
    i=0

    while not stop.is_set():

        sys.stdout.write(
            CYAN+f"\rPreparing Download {symbols[i%4]}"+RESET
        )

        sys.stdout.flush()
        i+=1
        time.sleep(0.2)


def download(link,format_code,folder):

    stop=threading.Event()

    t=threading.Thread(target=loading_animation,args=(stop,))
    t.start()

    time.sleep(3)

    stop.set()
    t.join()

    print(GREEN+"\n\n🚀 Download Started...\n"+RESET)

    cmd=[
        "yt-dlp",
        "-f",format_code,
        "-o",f"{folder}/%(title)s.%(ext)s",
        "--merge-output-format","mp4",
        link
    ]

    subprocess.run(cmd)

    print(GREEN+"\n✅ Download Completed"+RESET)
    print("Saved in:",folder)


def main():

    check_yt_dlp()

    while True:

        banner()

        link=input("Paste YouTube Video Link: ").strip()

        if not validate_link(link):

            print(RED+"\n⚠ Warning: Ye YouTube link nahi hai!"+RESET)
            print(YELLOW+"Please sahi YouTube video link add karo\n"+RESET)

            input("Press Enter...")
            continue

        qualities=get_qualities(link)

        if not qualities:

            print(RED+"No supported quality found"+RESET)
            input("Press Enter...")
            continue

        show_menu(qualities)

        choice=input("\nSelect quality: ")

        if choice not in qualities:

            print(RED+"Invalid option"+RESET)
            input("Press Enter...")
            continue

        format_code=qualities[choice][1]

        folder=get_folder()

        download(link,format_code,folder)

        again=input("\nDownload another video? (y/n): ")

        if again.lower()!="y":
            print(GREEN+"\nThanks for using ATIF Downloader ❤️"+RESET)
            break


if __name__=="__main__":
    main()
