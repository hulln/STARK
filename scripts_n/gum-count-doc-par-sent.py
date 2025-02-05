import os

def count_docs_pars_sents(directory, output_file):
    results = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".conllu"):
            filepath = os.path.join(directory, filename)
            doc_count = 0
            par_count = 0
            sent_count = 0
            
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("# newdoc id"):
                        doc_count += 1
                    elif line.startswith("# newpar"):
                        par_count += 1
                    elif line.startswith("# sent_id"):
                        sent_count += 1
            
            results.append(f"{filename}\t{doc_count}\t{par_count}\t{sent_count}")  # Included sent_count
    
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write("Filename\tDocuments\tParagraphs\tSentences\n")
        out_file.write("\n".join(results) + "\n")  # Added newline for proper formatting
    
    print(f"Results saved to {output_file}")

directory = "sample/gum/"  # Directory path
output_file = "doc_par_sent_counts.tsv"  # Updated output file name

count_docs_pars_sents(directory, output_file)
