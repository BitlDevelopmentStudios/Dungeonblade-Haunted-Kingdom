import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

target = Executable(
    script="../../Dungeonblade_HauntedKingdom.py",
    base=None,
    icon="icon.ico")

setup(
    name = "Dungeonblade: Haunted Kingdom",
    version = "1.0",
    description = "A simple text adventure game.",
    author = "Bitl",
    options = {"build_exe": build_exe_options},
    executables = [target])
