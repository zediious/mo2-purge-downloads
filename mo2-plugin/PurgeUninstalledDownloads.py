from os import listdir, remove

from PyQt6.QtGui import QIcon
from PyQt6 import QtWidgets, QtCore
import mobase


def purge_downloads(plugin, listOnly=False):
    """
    Find all deletable archives and delete them, instead only listing
    the deletable archives if user chooses. Display a messagebox with
    the found archives regardless.
    """
    def _traverse_and_purge(downloadsPath: str, listOnly: bool = False):
        """
        Traverse downloads directory, checking any .meta files for
        "uninstalled=true". If found, delete that .meta file's respective
        archive, then delete the .meta file. Return a list of deleted files.

        If listOnly is passed to purge_downloads as True, this function will
        only return the list, without deleting any files.
        """
        removed_archives = []
        for file in listdir(downloadsPath):
            if file.endswith(".meta"):
                is_uninstalled = False
                with open(f"{downloadsPath}\\{file}") as meta_file:
                    for line in meta_file:
                        if "uninstalled" in line:
                            uninstalled_data = line.strip().split("=")
                            if uninstalled_data[1] == str("true"):
                                is_uninstalled = True
                                try:
                                    mod_archive = file.replace(".meta", "")
                                    if not listOnly:
                                        remove(f"{downloadsPath}\\{mod_archive}")
                                    removed_archives.append(mod_archive)
                                except FileNotFoundError:
                                    continue

                meta_file.close()
                if is_uninstalled and not listOnly:
                    remove(f"{downloadsPath}\\{file}")

        return removed_archives

    # Main function begin
    if not listOnly:
        removed_archives = _traverse_and_purge(plugin.organizer.downloadsPath())
        messagebox_title = "Deleted Archives"
    else:
        removed_archives = _traverse_and_purge(plugin.organizer.downloadsPath(), True)
        messagebox_title = "Delatable Archives"

    # Construct string of removable/removed archives
    removed_archives_string = ""
    for archive in removed_archives:
        removed_archives_string += f"{archive}\n"

    if removed_archives_string == "":
        removed_archives_string = "No archives to remove."

    # Write log file if user checked box
    if plugin.logging:
        with open(f"{plugin.organizer.overwritePath()}\\mo2-purge-downloads.log", "w") as log_file:
            for archive in removed_archives:
                log_file.write(f"- {archive}\n")

    # Display messagebox with list of archives
    QtWidgets.QMessageBox.information(
        plugin._parentWidget(), messagebox_title, removed_archives_string)


def construct_choice_dialog(plugin):
    """
    Construct and return a dialog box to choose from tool options.
    """
    # Create a dialog and resize to 200x200
    dialog = QtWidgets.QDialog(plugin._parentWidget())
    dialog.resize(230, 200)
    dialog.setWindowTitle("Purge Uninstalled Downloads")

    # Create buttons for tool options
    buttonList = QtWidgets.QPushButton()
    buttonList.setText("List Purgable Archives")
    buttonList.clicked.connect(
            lambda: purge_downloads(
                        plugin,
                        listOnly=True
                    ))

    buttonPurge = QtWidgets.QPushButton()
    buttonPurge.setText("Purge Archives")
    buttonPurge.clicked.connect(
        lambda: purge_downloads(
                    plugin
                ))

    # Checkbox for logging option
    checkbox = QtWidgets.QCheckBox()
    checkbox.setText("Output a log file to Overwrite.")
    checkbox.clicked.connect(
        lambda: plugin.setLogging(True)
    )

    # Add label for direction
    label = QtWidgets.QLabel()
    label.setText("Choose an option above.\n\nArchives are only selected "
                  "if the mod download has been marked 'Uninstalled'.")
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Create a new layout, add widgets, insert to dialog
    layout = QtWidgets.QBoxLayout(
        QtWidgets.QBoxLayout.Direction.TopToBottom)
    layout.addWidget(buttonList)
    layout.addWidget(buttonPurge)
    layout.addWidget(checkbox)
    layout.addWidget(label)
    dialog.setLayout(layout)

    return dialog


class PurgeDownloads(mobase.IPluginTool):
    organizer: mobase.IOrganizer
    logging: bool = False

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
        return mobase.VersionInfo(1, 2, mobase.ReleaseType.FINAL)

    def isActive(self) -> bool:
        return self.organizer.pluginSetting(self.name(), "enabled")

    def settings(self):
        return [mobase.PluginSetting("Enabled", "Enable this plugin", True)]

    def displayName(self) -> str:
        return "Purge Uninstalled Downloads"

    def tooltip(self) -> str:
        return ("Delete all archives and .meta files for mods that you "
                "have completely deleted from the mod list. Alternatively, "
                "opt to only list the deletable archives without deleting them.")

    def icon(self):
        return QIcon.fromTheme(QIcon.ThemeIcon.DialogWarning)

    def setLogging(self, enabled: bool):
        self.logging = enabled

    def display(self):
        """
        Function called when tool is used in GUI.
        Display dialog box to choose from tool options.
        """
        # Show the choice dialog
        construct_choice_dialog(self).exec()


def createPlugin() -> mobase.IPlugin:
    return PurgeDownloads()
