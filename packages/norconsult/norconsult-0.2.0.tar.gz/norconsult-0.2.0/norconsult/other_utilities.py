
import os

def rename_autocad_publish(folder_path, overwrite=False):
    """
    Renames AutoCAD published PDF files by keeping only the last part after the last hyphen.
    Useful when using the publish command in AutoCAD and wanting just the layout name in the filename.

    Args:
        folder_path (str): Path to the folder containing the PDF files.
        overwrite (bool): If True, allows overwriting existing files. Defaults to False.

    Example:
        If the folder contains:
        - "drawing1-2024-01-01.pdf" -> Renamed to "01.pdf"
        - "projectX-final-v2.pdf" -> Renamed to "v2.pdf"
    """
    # Validate if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder does not exist - {folder_path}")
        return

    # Iterate through all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") and "-" in filename:
            parts = filename.split("-")
            new_name = parts[-1].strip()  # Keep only the last part

            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)

            # Check if new file already exists
            if os.path.exists(new_path):
                if not overwrite:
                    print(f"Skipping: {new_name} (File already exists)")
                    continue
                else:
                    print(f"Overwriting: {new_name}")

            # Rename file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

    print("✅ Rename process completed.")
