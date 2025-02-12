from os import listdir, remove

from PyQt6.QtGui import QIcon
from PyQt6 import QtWidgets
import mobase


def traverse_and_purge(downloadsPath: str):
    """
    Remove all archives and respective meta files from mods that have been
    deleted from the mod list entirely, returning a list of deleted archives.
    """
    removed_archives = []
    for file in listdir(downloadsPath):
        if file.endswith(".meta"):
            is_uninstalled = False
            path = file
            with open(f"{downloadsPath}\\{file}") as meta_file:
                for line in meta_file:
                    if "uninstalled" in line:
                        uninstalled_data = line.strip().split("=")
                        if uninstalled_data[1] == str("true"):
                            is_uninstalled = True
                            try:
                                mod_archive = path.replace(".meta", "").replace("downloads\\", "")
                                remove(f"{downloadsPath}\\{mod_archive}")
                                removed_archives.append(mod_archive)
                            except FileNotFoundError:
                                continue

            meta_file.close()
            if is_uninstalled:
                remove(f"{downloadsPath}\\{file}")

    return removed_archives


class PurgeDownloads(mobase.IPluginTool):
    organizer: mobase.IOrganizer

    def __init__(self):
        super().__init__()

    def init(self, newOrganizer: mobase.IOrganizer):
        self.organizer = newOrganizer
        return True

    def name(self) -> str:
        return "Purge Uninstalled Downloads"

    def author(self) -> str:
        return "Zediious"

    def description(self) -> str:
        return ("Delete archives and .meta files for mods that have "
                "been deleted from the mod list.")

    def version(self) -> mobase.VersionInfo:
        return mobase.VersionInfo(1, 0, mobase.ReleaseType.FINAL)

    def isActive(self) -> bool:
        return self.organizer.pluginSetting(self.name(), "enabled")

    def settings(self):
        return [mobase.PluginSetting("Enabled", "Enable this plugin", True)]

    def displayName(self) -> str:
        return "Purge Uninstalled Downloads"

    def tooltip(self) -> str:
        return ("Delete all archives and .meta files for mods that you "
                "have completely deleted from the mod list.")

    def icon(self):
        return QIcon('null')

    def display(self):
        """
        Function called when tool is used in GUI
        """
        removed_archives = traverse_and_purge(self.organizer.downloadsPath())
        removed_archives_string = ""
        for archive in removed_archives:
            removed_archives_string += f"{archive}\n"

        QtWidgets.QMessageBox.information(
            self._parentWidget(), 'Deleted Archives', removed_archives_string)


def createPlugin() -> mobase.IPlugin:
    return PurgeDownloads()
