# Mod Organizer 2 - Purge Downloads

Purge uninstalled mod download archives and their respective `.meta` files from Mod Organizer 2's download folder.

## Instructions to run

1) Download Python https://www.python.org/downloads/

2) Download the [LATEST RELEASE](https://github.com/zediious/mo2-purge-downloads/releases) and place the `.py` file inside your Mod Organizer 2 `downloads` directory.

3) Open your terminal of choice, and move to your `download` directory. Run `python purge.py` once you are in the `download` directory.

This will remove all archives for mods you have deleted from your mods list, as well as their `.meta` files. A log will be printed to the terminal of all archives removed, and that log will be saved in the `downloads` directory.
