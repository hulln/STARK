import os

def analyze_conllu_files(directory):
    file_analyses = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.conllu'):
                filepath = os.path.join(root, filename)
                tokens = 0
                empty_lines = 0
                comment_lines = 0
                total_lines = 0

                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        total_lines += 1
                        stripped_line = line.strip()

                        if not stripped_line:
                            empty_lines += 1
                        elif stripped_line.startswith('#'):
                            comment_lines += 1
                        elif stripped_line[0].isdigit():
                            tokens += 1

                # Calculate discrepancy (if any)
                sum_counts = tokens + empty_lines + comment_lines
                discrepancy = total_lines - sum_counts
                status = "✅" if discrepancy == 0 else f"❌ (Discrepancy: {discrepancy} lines)"

                file_analyses[filepath] = {
                    'tokens': tokens,
                    'empty': empty_lines,
                    'comments': comment_lines,
                    'total': total_lines,
                    'status': status
                }

    return file_analyses

# Directory containing CONLLU files
directory = 'sample/gum'
file_analyses = analyze_conllu_files(directory)

# Print results
print("Analysis per file:")
for filepath, data in sorted(file_analyses.items()):
    filename = os.path.basename(filepath)
    print(f"- {filename}:")
    print(f"  Tokens: {data['tokens']}")
    print(f"  Empty lines: {data['empty']}")
    print(f"  Comment lines: {data['comments']}")
    print(f"  Total lines: {data['total']}")
    print(f"  Validation: {data['status']}\n")