from os import chdir, listdir, remove

DEVELOPMENT = False

# Value that can be changed in development. Python file should be placed in downloads folder.
PATH = "downloads"

with open('mo2-purge-downloads.log', 'w') as log_file:

    log_file.write("List of archives and their respective meta files that were deleted\n")

    if DEVELOPMENT:
        chdir('downloads')

    for file in listdir():

        if file.endswith(".meta"):

            is_uninstalled = False

            path = f"{PATH}\{file}"

            with open(file) as meta_file:

                for line in meta_file:

                    if line.__contains__('uninstalled'):

                        uninstalled_data = line.strip().split('=')

                        print(uninstalled_data)

                        if uninstalled_data[1] == str('true'):

                            is_uninstalled = True
                            
                            try:

                                mod_archive = path.replace('.meta', '').replace("downloads\\", '')
                                remove(mod_archive)

                                log_file.write(f"- {mod_archive}\n")

                            except FileNotFoundError:

                                print("A mod download archive was not found, and it's .meta file indicates it was uninstalled. This means the archive was removed manually at some point.")
                                continue

            meta_file.close()
            if is_uninstalled == True:

                remove(path.replace("downloads\\", ''))

with open('mo2-purge-downloads.log', 'r') as log_file:

    print(" ")
    for line in log_file:

        print(line.strip())
