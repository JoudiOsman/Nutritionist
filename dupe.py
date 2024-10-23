def remove_duplicates(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    # Remove duplicate lines while preserving order
    unique_lines = list(dict.fromkeys(lines))
    
    # Write the unique lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(unique_lines)

# swap 'backUpList' with relevant name
remove_duplicates('backUplist.txt')
