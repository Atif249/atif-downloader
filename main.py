#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys
import time
import threading

APP_NAME = "ATIF DOWNLOADER v13 ULTRA PRO MAX"

# Colors
GREEN="\033[92m"
RED="\033[91m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"


# 🔥 Typewriter Effect
def typewriter(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


# 🚀 Ultimate Banner
def banner():
    os.system("clear")

    intro = [
        "⚡ Initializing ATIF System...",
        "📦 Loading Modules...",
        "🔓 Bypassing Limits...",
        "🚀 Launching Downloader..."
    ]

    for line in intro:
        print(GREEN + line + RESET)
        time.sleep(0.3)

    os.system("clear")

    print(CYAN)
    print("╔" + "═"*60 + "╗")
    print("║" + " "*60 + "║")
    print("║        🚀 ATIF DOWNLOADER v13 ULTRA PRO 🚀     ║")
    print("║" + " "*60 + "║")
    print("║            👑 CREATED BY: ATIF 👑              ║")
    print("║" + " "*60 + "║")
    print("║     ⚡ ULTRA FAST | NO LIMIT | STABLE ⚡       ║")
    print("║" + " "*60 + "║")
    print("║        🎬 YOUTUBE DOWNLOADER ENGINE 🎬        ║")
    print("║" + " "*60 + "║")
    print("╚" + "═"*60 + "╝")
    print(RESET)

    typewriter("⚡ Welcome to ATIF Downloader System ⚡", 0.04)
    print()


# ✅ Check dependencies
def check_dependencies():
    if not shutil.which("yt-dlp"):
        print(RED+"yt-dlp install nahi hai"+RESET)
        print("Install karo: sudo apt install yt-dlp")
        sys.exit()

    if not shutil.which("ffmpeg"):
        print(RED+"ffmpeg install nahi hai"+RESET)
        print("Install karo: sudo apt install ffmpeg")
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


# 🔍 Fetch qualities (FAST + SAFE)
def get_qualities(link):
    print(CYAN+"\n🔍 Fetching qualities..."+RESET)

    try:
        result = subprocess.run(
            ["yt-dlp", "-F", link],
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.TimeoutExpired:
        print(RED+"⏳ Timeout! Internet slow ya video issue."+RESET)
        return {}

    if result.returncode != 0:
        print(RED+"❌ Video load nahi ho rahi."+RESET)
        return {}

    lines = result.stdout.splitlines()

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


# ⏳ Loading animation
def loading_animation(stop):
    symbols=["|","/","-","\\"]
    i=0
    while not stop.is_set():
        sys.stdout.write(CYAN+f"\rProcessing {symbols[i%4]}"+RESET)
        sys.stdout.flush()
        i+=1
        time.sleep(0.15)


# 🚀 Download
def download(link,format_code,folder):
    stop=threading.Event()
    t=threading.Thread(target=loading_animation,args=(stop,))
    t.start()

    time.sleep(1)
    stop.set()
    t.join()

    print(GREEN+"\n🚀 Download Started...\n"+RESET)

    cmd=[
        "yt-dlp",
        "-f", f"{format_code}+bestaudio",
        "-o", f"{folder}/%(title)s.%(ext)s",
        "--merge-output-format","mp4",
        "--no-playlist",
        "--concurrent-fragments","4",
        "--no-warnings",
        "--progress"
    ]

    subprocess.run(cmd)

    print(GREEN+"\n✅ Download Completed"+RESET)
    print("📁 Saved in:",folder)


# 🧠 Main App
def main():
    check_dependencies()

    while True:
        banner()

        link=input("📌 Paste YouTube Video Link: ").strip()

        if not validate_link(link):
            print(RED+"\n⚠ Invalid YouTube Link!"+RESET)
            input("Press Enter...")
            continue

        qualities=get_qualities(link)

        if not qualities:
            print(RED+"No quality found"+RESET)
            input("Press Enter...")
            continue

        show_menu(qualities)

        choice=input("\n🎯 Select quality: ")

        if choice not in qualities:
            print(RED+"Invalid option"+RESET)
            input("Press Enter...")
            continue

        format_code=qualities[choice][1]
        folder=get_folder()

        download(link,format_code,folder)

        again=input("\n🔁 Download another video? (y/n): ")

        if again.lower()!="y":
            print(GREEN+"\n❤️ Thanks for using ATIF Downloader"+RESET)
            break


if __name__=="__main__":
    main()
