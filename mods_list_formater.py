def format_mod_text(mod_text):
    mod_name = mod_text.strip()
    
    formatted_mod = f'    ("{mod_name}"),'
    
    return formatted_mod

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    formatted_lines = [format_mod_text(line.strip()) for line in lines]
    
    with open(output_file_path, 'w') as file:
        file.write('mods = [\n')
        file.write('\n'.join(formatted_lines))
        file.write('\n]\n')

if __name__ == "__main__":
    input_file_path = 'mods_list.txt'
    output_file_path = 'mods_list.py'
    process_file(input_file_path, output_file_path)