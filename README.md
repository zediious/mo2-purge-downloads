# Mod Organizer 2 - Purge Downloads

Purge uninstalled mod download archives from Mod Organizer 2's download folder.

This exists as a Mod Organizer 2 plugin.

1) Download the [latest release](https://github.com/zediious/mo2-purge-downloads/releases).

2) Extract `PurgeUninstalledDownloads.py` to the `plugins` directory in your Mod Organizer 2 instance. Restart Mod Organizer if it is not already closed.

3) Use the "Purge Uninstalled Downloads" option under the puzzle piece icon at the top panel in Mod Organizer.
   
<div align=center>
  <image src=https://i.imgur.com/59gPDaz.png></image>
</div>

5) Any archive and respective `.meta` file associated with a *deleted* mod will be removed, and a dialog box will appear showing a list of all removed archives.

The standalone script is to be placed directly in your `downloads` directory and ran by command line. It will print a log of removed archives.
