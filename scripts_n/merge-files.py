import os
import glob

# Specify the folder containing the CoNLL-U files
folder_path = 'sample/gum/multigenre'

# Define the output file path for the merged file
merged_file = os.path.join(folder_path, 'en_gum_multigenre-merged.conllu')

# Get a list of all .conllu files in the folder
conllu_files = glob.glob(os.path.join(folder_path, '*.conllu'))

# Initialize a list to store the content from each file
merged_content = []

# Read and append each file's content
for file_path in conllu_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        merged_content.extend(file.readlines())
        # Separate each file's content with a newline for clarity
        merged_content.append('\n')

# Write the merged content to the output file
with open(merged_file, 'w', encoding='utf-8') as output_file:
    output_file.writelines(merged_content)

print(f"Merged file saved to {merged_file}")