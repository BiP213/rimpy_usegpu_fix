import os
import subprocess
import mods_list
import mods_list_formater


# Your RimWorld mods folder path.
RIMWORLD_MODS_DIR = "A:/Games/RimWorld/Mods/"


def rimpy_directory_verifier():
    curr_dir_name = os.path.basename(os.getcwd())
    if curr_dir_name != "compressors":
        print(
            "\nPlace the scripts in your RimPy_Windows/compressors folder before running it!"
        )
        input("\nPress Enter to exit...")
        exit(0)


def is_file_empty(mods_py_path):
    return os.stat(mods_py_path).st_size == 0


def mods_list_verifier():
    COMPLETION_MESSAGE = "Done!"
    mods_txt_path = "mods_list.txt"
    mods_py_path = "mods_list.py"

    if os.path.exists(mods_txt_path):
        mods_txt_mod_time = os.path.getmtime(mods_txt_path)

        if os.path.exists(mods_py_path):
            mods_py_mod_time = os.path.getmtime(mods_py_path)

            if is_file_empty(mods_py_path) or (mods_txt_mod_time > mods_py_mod_time):
                print(f"\n{mods_txt_path} file identified!")
                print(f"Updating {mods_py_path} file...")
                mods_list_formater.process_file(mods_txt_path, mods_py_path)
                print(COMPLETION_MESSAGE)
                exit(0)
        update_mods_list = input("Update mods list? [y/n]: ")
        if update_mods_list.lower() == "y":
            print(f"\nUpdating {mods_txt_path} file...\n")

            mods_folder_list = next(os.walk(RIMWORLD_MODS_DIR))[1]

            with open(mods_txt_path, "w") as file:
                for mod_folder in mods_folder_list:
                    file.write(f"{mod_folder}\n")
                    print(f"{mod_folder}")

            print(f"\n{mods_txt_path} file updated!")
            print(f"\nUpdating {mods_py_path} file...")
            mods_list_formater.process_file(mods_txt_path, mods_py_path)
            print(COMPLETION_MESSAGE)
            print("\nRun it again.")
            exit(0)

    else:
        print(f"\n{mods_txt_path} file not found. Creating...")

        mods_folder_list = next(os.walk(RIMWORLD_MODS_DIR))[1]

        with open(mods_txt_path, "w") as file:
            for mod_folder in mods_folder_list:
                file.write(f"{mod_folder}\n")
                print(f"{mod_folder}")

        print(f"\n{mods_txt_path} file created!")
        print(f"\nUpdating {mods_py_path} file...")
        mods_list_formater.process_file(mods_txt_path, mods_py_path)
        print(COMPLETION_MESSAGE)
        print("\nRun it again.")
        exit(0)


def calculate_conversion_ratio(local_rimworld_mods_dir, mod_folder_name):
    png_count = 0
    dds_count = 0

    if os.path.exists(local_rimworld_mods_dir):
        for root, dirs, files in os.walk(local_rimworld_mods_dir):
            for file in files:
                if file.endswith(".png"):
                    png_count += 1
                    # Construct the expected.dds filename based on the.png filename
                    dds_filename = file.replace(".png", ".dds")
                    full_dds_path = os.path.join(root, dds_filename)
                    if os.path.exists(full_dds_path):
                        dds_count += 1

        if png_count > 0:
            conversion_ratio = dds_count / png_count * 100

            if conversion_ratio == 100:
                print(
                    f"\nIn '{mod_folder_name}', {conversion_ratio:.2f}% of .png files have been already converted to .dds."
                )
                print("All .png files will be deleted.")
                can_proceed = input("Proceed? [y/n]: ")
                if can_proceed.lower() == "y":
                    delete_pngs(local_rimworld_mods_dir, mod_folder_name)
                else:
                    print("Skipping...")
            else:
                print(
                    f"\nIn '{mod_folder_name}', {conversion_ratio:.2f}% of .png files have been already converted to .dds."
                )

                print("\nConvert all .png files not converted yet? [y/n]: ")
                can_proceed = input("Proceed? [y/n]: ")

                if can_proceed.lower() == "y":
                    convert_png_to_dds(local_rimworld_mods_dir, mod_folder_name)
                else:
                    print("Skipping...")
        else:
            print(f"\nNo .png files found in '{mod_folder_name}'.")
    else:
        print(f"\nThe directory '{local_rimworld_mods_dir}' does not exist.")


def delete_pngs(local_rimworld_mods_dir, mod_folder_name):
    print("\nDeleting .png files...")
    if os.path.exists(local_rimworld_mods_dir):
        for root, dirs, files in os.walk(local_rimworld_mods_dir):
            for file in files:
                if file.endswith(".png"):
                    # Construct the expected .dds filename based on the .png filename
                    dds_filename = file.replace(".png", ".dds")
                    full_dds_path = os.path.join(root, dds_filename)
                    full_png_path = os.path.join(root, file)

                    if os.path.exists(full_dds_path):
                        # Check if the .dds file is newer than the .png file
                        if os.path.getmtime(full_dds_path) > os.path.getmtime(
                            full_png_path
                        ):
                            os.remove(full_png_path)
                            print(f"Deleting {full_png_path}...")
                        else:
                            print(
                                f"\n{full_png_path} was not deleted because the corresponding .dds file is not newer."
                            )
                            can_proceed = input("\nConvert .png files? [y/n]: ")

                            if can_proceed.lower() == "y":
                                convert_png_to_dds(local_rimworld_mods_dir, mod_folder_name)
                            else:
                                print("Skipping...")

                    else:
                        print(
                            f"\nNo corresponding .dds file found for {full_png_path}."
                        )
                        print("\nSkipping...")
    else:
        print(f"\nThe directory '{local_rimworld_mods_dir}' does not exist.")


def convert_png_to_dds(local_rimworld_mods_dir, mod_folder_name):
    if os.path.exists(local_rimworld_mods_dir):
        print(f"\nConverting {mod_folder_name} .png files to .dds...")
        subprocess.run(
            [
                "texconv.exe",
                "-r:keep",
                "-f",
                "BC7_UNORM",
                "-y",
                "-vflip",
                "-fixbc4x4",
                "-m",
                "1",
                "-gpu",
                "0",
                "-o",
                f"{local_rimworld_mods_dir}",
                f"{local_rimworld_mods_dir}/*.png",
            ]
        )
        print(f"{mod_folder_name} conversion completed.")

    else:
        print(f"The directory {local_rimworld_mods_dir} does not exist.")


if __name__ == "__main__":
    rimpy_directory_verifier()
    mods_list_verifier()

    for mod_folder_name in mods_list.mods:
        local_rimworld_mods_dir = RIMWORLD_MODS_DIR + mod_folder_name
        calculate_conversion_ratio(local_rimworld_mods_dir, mod_folder_name)

    print("\nMade with <3 by @bip213")
    input("Press Enter to exit...")
