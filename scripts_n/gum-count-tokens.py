import os
import re

def count_lines_starting_with_number(directory, output_file):
    results = []
    
    # Regular expression patterns
    pattern = re.compile(r'^\d+\s')  # Match lines starting with one or more digits followed by a space
    range_pattern = re.compile(r'^\d+-\d+\s')  # Match lines starting with two numbers separated by a dash

    for filename in os.listdir(directory):
        if filename.endswith(".conllu"):
            filepath = os.path.join(directory, filename)
            token_count = 0
            range_count = 0
            
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    if pattern.match(line) and not range_pattern.match(line):  # Count lines with only a single number
                        token_count += 1
                    elif range_pattern.match(line):  # Count lines with a number range
                        range_count += 1
            
            results.append(f"{filename}\t{token_count}\t{range_count}")
    
    # Write results to output file
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write("Filename\tSingle Number Tokens\tRange Tokens\n")
        out_file.write("\n".join(results) + "\n")
    
    print(f"Results saved to {output_file}")

# Directory path and output file
directory = "sample/gum"
output_file = "token_counts_with_ranges.tsv"  # Output file name

# Run the function
count_lines_starting_with_number(directory, output_file)
