import os
import sys

def list_directory_structure(startpath):
    """
    Lists the directory structure starting from the given path.

    Args:
        startpath (str): The root directory path to start listing from.
    """
    # Check if the provided path is a valid directory
    if not os.path.isdir(startpath):
        print(f"Error: The path '{startpath}' is not a valid directory or does not exist.")
        return

    print(f"Structure for: {startpath}")

    # os.walk generates the directory tree structure
    # It yields a 3-tuple (dirpath, dirnames, filenames) for each directory
    for root, dirs, files in os.walk(startpath):
        # Calculate the level of indentation based on path depth
        # We subtract the length of the starting path and count separators
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level) # 4 spaces per level

        # Print the current directory name
        # os.path.basename gets the last part of the path (the directory name)
        # Don't print the root directory name again if it's the very first iteration
        if level > 0 or root == startpath: # Ensure root is printed if it's the start
             # For the very first root, don't add extra indent/prefix
             if root == startpath:
                 print(f'{os.path.basename(root)}/')
             else:
                 print(f'{indent}|-- {os.path.basename(root)}/')

        # Print files in the current directory
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}|-- {f}')

# --- Main part of the script ---
if __name__ == "__main__":
    # Define the target directory path
    # Using a raw string (r"...") is good practice for Windows paths
    # to avoid issues with backslashes being interpreted as escape characters.
    target_directory = r"C:\Users\bhupan\Documents\Utillities"

    # Call the function to list the structure
    list_directory_structure(target_directory)
