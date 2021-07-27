import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "includes":
        [
            "PySide6",
            "PySide2",
            "requests",
            "json",
            "ctypes",
            "webbrowser"
        ],
        "excludes": [
            "tkinter",
            "unittest",
            "numpy",
            "libcrypto",
            "lib2to3",
            "pygments",
            
        ],
        'optimize': 2
    }
}

executables = [
    Executable("ask_bowl.py", base=base,
               target_name="ask_bowl", icon="icon.ico")
]

setup(
    name="ask_bowl",
    version="1",
    description="This is a program that is meant to help high schools students practice science bowl questions for NSB",
    options=options,
    executables=executables,
)
