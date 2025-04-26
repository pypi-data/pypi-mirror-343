import re
import pandas as pd
import time
import os
import json
import chardet

def detect_encoding(file_path):
    """
    Detects the encoding of a file using chardet.
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)  # Read a portion of the file to detect encoding
        result = chardet.detect(raw_data)
        print(f"Detected encoding: {result['encoding']}")  # Print the detected encoding
        return result['encoding']

def sosi_block_iterator(file_path):
    """
    A generator function that reads a SOSI file line by line, identifies blocks,
    and processes coordinates (NØ and NØH) while keeping all values as strings.
    """
    # Detect the file encoding
    encoding = detect_encoding(file_path)
    
    current_block = []
    coordinate_type = None
    coordinates = []
    with open(file_path, 'r', encoding=encoding) as file:
        for line in file:
            # Skip full-line comments
            if line.lstrip().startswith('!'):
                continue
            # Remove inline comments (everything after "!")
            if '!' in line:
                line = line.split('!', 1)[0] + "\n"
            stripped_line = line.strip()
            if not stripped_line:
                continue

            # New block found (line starts with a dot and uppercase letters)
            if re.match(r'^\.([A-Z]+)', stripped_line):
                if current_block:
                    if coordinate_type and coordinates:
                        current_block.append(f'{coordinate_type} {coordinates}')
                    yield current_block
                current_block = [stripped_line]
                coordinate_type = None
                coordinates = []
            # Check for coordinate types (e.g. ..NØ or ..NØH)
            elif stripped_line.startswith('..NØ') or stripped_line.startswith('..NØH'):
                if coordinate_type and coordinates:
                    current_block.append(f'{coordinate_type} {coordinates}')
                coordinate_type = stripped_line
                coordinates = []
            # Collect coordinate data as strings
            elif coordinate_type:
                coordinates.append(stripped_line.split())
            # Regular line (non-coordinate)
            else:
                if coordinate_type and coordinates:
                    current_block.append(f'{coordinate_type} {coordinates}')
                    coordinate_type = None
                    coordinates = []
                current_block.append(stripped_line)
        # Yield the last block
        if current_block:
            if coordinate_type and coordinates:
                current_block.append(f'{coordinate_type} {coordinates}')
            yield current_block

def add_to_dict(stack, data, main_dict):
    """
    Adds data to the dictionary based on the provided stack.
    """
    d = main_dict
    for key in stack[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    d[stack[-1]] = data

def stack_append(stack, to_append, dotcounter, stack_dict):
    """
    Manages the stack for dictionary creation, handling duplicate keys with suffixes.
    """
    if dotcounter not in stack_dict:
        stack_dict[dotcounter] = {}
    if to_append in stack_dict[dotcounter]:
        stack_dict[dotcounter][to_append] += 1
        suffix = stack_dict[dotcounter][to_append]
        stack.append(f'{to_append}_xx{suffix}')
    else:
        stack_dict[dotcounter][to_append] = 1
        stack.append(to_append)
    return stack

def has_one_value(name_string):
    """
    Checks if a string contains exactly one word (no spaces).
    """
    return len(name_string.split()) == 1

def process_sosi_file_to_dict(file_path):
    """
    Processes a SOSI file and converts it into a nested Python dictionary.
    """
    main_dict = {}
    for data in sosi_block_iterator(file_path):
        # Use the first line (minus the dot) as the starting key for the block
        stack = [data[0].strip('.')]
        dot_counter = len(data[0]) - len(data[0].lstrip('.'))
        stack_dict = {}  # Reset stack_dict for each block
        for line in data[1:]:
            cleaned_line = line.strip('.')
            if not has_one_value(cleaned_line):
                key, value = cleaned_line.split(' ', 1)
            prev_dot_counter = dot_counter
            dot_counter = len(line) - len(line.lstrip('.'))
            if dot_counter == prev_dot_counter:
                if has_one_value(line):
                    stack = stack[:-1]
                    stack = stack_append(stack, cleaned_line, dot_counter, stack_dict)
                else:
                    stack = stack[:-1]
                    stack = stack_append(stack, key, dot_counter, stack_dict)
                    add_to_dict(stack, value, main_dict)
            elif dot_counter > prev_dot_counter:
                if has_one_value(line):
                    stack = stack_append(stack, cleaned_line, dot_counter, stack_dict)
                else:
                    stack = stack_append(stack, key, dot_counter, stack_dict)
                    add_to_dict(stack, value, main_dict)
            else:
                if has_one_value(line):
                    stack = stack[:dot_counter-1]
                    stack = stack_append(stack, cleaned_line, dot_counter, stack_dict)
                else:
                    stack = stack[:dot_counter-1]
                    stack = stack_append(stack, key, dot_counter, stack_dict)
                    add_to_dict(stack, value, main_dict)
    return main_dict

def clean_column_name(name):
    """
    Cleans column names to be valid for Excel:
    - Removes brackets, asterisks, and other special characters
    - Replaces them with underscores or removes them
    """
    # Replace problematic characters with underscores
    clean_name = re.sub(r'[\[\]*/\\:?*]', '_', str(name))
    
    # Remove leading/trailing underscores and spaces
    clean_name = clean_name.strip('_').strip()
    
    # Ensure it's not empty
    if not clean_name:
        return "Column"
        
    return clean_name

def flatten_dict(obj, prefix='', result=None):
    """
    Flattens a nested dictionary, joining keys with underscores.
    Ensures all keys are valid Excel column names.
    """
    if result is None:
        result = {}
    
    for key, value in obj.items():
        # Skip HODE and SLUTT
        if key.startswith("HODE") or key.startswith("SLUTT"):
            continue
        
        # Clean the key for Excel compatibility
        clean_key = clean_column_name(key)
            
        # Handle nested dictionaries
        if isinstance(value, dict):
            new_prefix = f"{prefix}_{clean_key}" if prefix else clean_key
            flatten_dict(value, new_prefix, result)
        else:
            new_key = f"{prefix}_{clean_key}" if prefix else clean_key
            
            # Convert lists or arrays to string representation if needed
            if isinstance(value, (list, tuple)) or (isinstance(value, str) and (value.startswith('[') and value.endswith(']'))):
                value = str(value)
                
            result[new_key] = value
            
    return result

def sosi_to_json(sosi_file_path, json_file_path=None):
    """Converts a SOSI file to a JSON file while handling duplicate keys and omitting in-line comments.

    Parameters:
        sosi_file_path (str): The path to the input SOSI file.
        json_file_path (str, optional): The path to save the output JSON file.
                                        If None, it will use the same name as the input file with .json extension.

    Processing Details:
        - Duplicate keys: If duplicate keys are encountered during the SOSI file processing,
          a numeric suffix (xx(number)) is appended to ensure uniqueness.
        - Comments: Any text in the SOSI file following an exclamation mark (!) is considered a comment and is ignored.
        - Encoding: The file encoding is automatically detected.

    Output:
        Writes the processed contents as a formatted JSON file with UTF-8 encoding.
    """
    start_time = time.time()

    # Automatically generate JSON file name if not provided
    if json_file_path is None:
        base_name = os.path.splitext(sosi_file_path)[0]  # Remove extension
        json_file_path = f"{base_name}.json"  # Add .json extension

    # Process the SOSI file to build a dictionary
    main_dict = process_sosi_file_to_dict(sosi_file_path)
    main_dict['SLUTT'] = {}

    # Save the final dictionary as JSON
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(main_dict, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully converted SOSI to JSON: {json_file_path}")
    except Exception as e:
        print(f"❌ Error writing to JSON file: {e}")

    end_time = time.time()
    print(f"Processing time: {end_time - start_time:.2f} seconds")

def sosi_to_excel(sosi_file_path, excel_file_path=None):
    """
    Enhanced version of sosi_to_excel that:
    1. Creates a separate sheet for each OBJTYPE
    2. Only includes columns that have data
    3. Flattens hierarchical column names with underscores
    4. Ensures column names are valid for Excel (no brackets, special chars, etc.)
    
    Args:
        sosi_file_path (str): The path to the input SOSI file.
        excel_file_path (str, optional): The path to save the output Excel file.
                                         If None, it will use the same name as the input file with .xlsx extension.
    """
    start_time = time.time()

    # Automatically generate Excel file name if not provided
    if excel_file_path is None:
        base_name = os.path.splitext(sosi_file_path)[0]  # Remove extension
        excel_file_path = f"{base_name}.xlsx"  # Add .xlsx extension

    # Process the SOSI file to build a dictionary
    main_dict = process_sosi_file_to_dict(sosi_file_path)
    main_dict['SLUTT'] = {}

    # Group objects by OBJTYPE
    objtype_groups = {}
    
    for obj_key, obj_value in main_dict.items():
        # Skip header and footer entries
        if obj_key.startswith("HODE") or obj_key.startswith("SLUTT"):
            continue
            
        # Add the object ID to the dictionary for reference
        obj_with_id = {**obj_value, "ID": obj_key}
        
        # Get OBJTYPE or use "Unknown" if not present
        objtype = obj_value.get("OBJTYPE", "Unknown")
        
        if objtype not in objtype_groups:
            objtype_groups[objtype] = []
            
        # Flatten the object and add to the appropriate group
        flattened_obj = flatten_dict(obj_with_id)
        objtype_groups[objtype].append(flattened_obj)
    
    # Create the Excel writer
    try:
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            for objtype, objects in objtype_groups.items():
                # Skip if no objects of this type
                if not objects:
                    continue
                    
                # Convert list of dictionaries to DataFrame
                df = pd.DataFrame(objects)
                
                # Clean column names for Excel compatibility
                df.columns = [clean_column_name(col) for col in df.columns]
                
                # Remove columns that are completely empty
                df = df.dropna(axis=1, how='all')
                
                # Remove columns with all empty strings
                df = df.loc[:, ~(df == '').all()]
                
                # Write to Excel with the OBJTYPE as sheet name
                # Clean sheet name (remove invalid characters for Excel sheet names)
                sheet_name = clean_column_name(objtype)
                if len(sheet_name) > 31:  # Excel has a 31 character limit for sheet names
                    sheet_name = sheet_name[:31]
                
                # Add a number suffix if sheet name is too short or empty
                if not sheet_name:
                    sheet_name = f"Sheet_{len(objtype_groups)}"
                    
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Auto-adjust column widths
                try:
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(df.columns):
                        # Set column width based on content (max of column name or max content length)
                        max_len = max(df[col].astype(str).map(len).max(), len(str(col)))
                        # Add a little extra space and convert to Excel's character width
                        adjusted_width = min(max(max_len + 2, 10), 50)  # Min width of 10, max of 50
                        
                        # Convert column index to Excel column letter
                        col_letter = ''
                        temp = idx + 1
                        while temp > 0:
                            remainder = (temp - 1) % 26
                            col_letter = chr(65 + remainder) + col_letter
                            temp = (temp - 1) // 26
                            
                        worksheet.column_dimensions[col_letter].width = adjusted_width
                except Exception as e:
                    print(f"Warning: Could not adjust column widths for sheet {sheet_name}: {e}")

        print(f"✅ Successfully converted SOSI to Excel with separate sheets: {excel_file_path}")
    except Exception as e:
        print(f"❌ Error writing to Excel file: {e}")

    end_time = time.time()
    print(f"Processing time: {end_time - start_time:.2f} seconds")

def test():
    return "Test function executed successfully!"

