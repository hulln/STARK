import os

def count_conllu_tokens(directory):
    file_token_counts = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.conllu'):
                filepath = os.path.join(root, filename)
                file_tokens = 0
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        stripped_line = line.strip()
                        # Skip empty lines and comments
                        if not stripped_line or stripped_line.startswith('#'):
                            continue
                        # Check if the line starts with a numeric character
                        if stripped_line[0].isdigit():
                            file_tokens += 1
                file_token_counts[filepath] = file_tokens

    return file_token_counts

# Directory containing CONLLU files
directory = 'sample/gum'
file_counts = count_conllu_tokens(directory)

# Print token counts for each file
print("Token counts per file (lines starting with a number):")
for filepath, count in sorted(file_counts.items()):
    print(f"- {os.path.basename(filepath):<30}: {count} tokens")