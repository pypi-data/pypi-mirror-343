from ahk.autostart import create
from pathlib import Path
import subprocess
import argparse
import os
from ahk.regenerate import regenerate as init

CURRENT = Path(__file__).resolve().parent
scripts = CURRENT.parent.joinpath("ahk_scripts")


def clean():
    if scripts.exists():
        files = scripts.glob("*.ahk")
        for file in files:
            file.unlink()


def create_autoruns():
    files = list(scripts.glob("*.ahk"))
    for f in files:
        create(f)


def exec1():
    files = list(scripts.glob("*.ahk"))
    for f in files:
        os.startfile(f)


def open_reg():
    regjump = CURRENT.parent.joinpath("ahk_resources").joinpath("regjump.exe")
    subprocess.Popen(
        rf"{regjump} HKCU:\Software\Microsoft\Windows\CurrentVersion\Run /accepteula"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--open", action="store_true", default=False, help="open startup location"
    )

    args = parser.parse_args()
    if args.open:
        open_reg()

    clean()
    init()
    create_autoruns()
    exec1()
