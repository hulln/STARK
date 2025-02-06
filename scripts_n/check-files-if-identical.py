import sys

def compare_conllu_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        if lines1 == lines2:
            print("The files are identical.")
            return True
        else:
            print("The files are different.")
            for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
                if line1 != line2:
                    print(f"Difference at line {i}:")
                    print(f"File 1: {line1.strip()}")
                    print(f"File 2: {line2.strip()}")
            return False

# Example usage
file1 = 'sample/gum/output_written.conllu'
file2 = 'sample/gum/output_written_2.conllu'
compare_conllu_files(file1, file2)
