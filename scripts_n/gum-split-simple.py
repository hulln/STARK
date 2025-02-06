from collections import defaultdict

current_doc = []
current_genre = ""
genre_counts = defaultdict(int)

spoken_genres = {"court", "interview", "conversation", "speech", "podcast", "vlog"}

input_path = 'sample/gum/en_gum-ud-merged.conllu'
spoken_output_path = 'sample/gum/output_spoken_2.conllu'
written_output_path = 'sample/gum/output_written_2.conllu'

with open(input_path, 'r') as infile, \
     open(spoken_output_path, 'w') as spoken_outfile, \
     open(written_output_path, 'w') as written_outfile:
    
    for line in infile:
        if line.startswith('# newdoc'):
            # Process the previous document
            if current_doc:
                # Write to the appropriate file based on genre
                if current_genre in spoken_genres:
                    spoken_outfile.write(''.join(current_doc))
                else:
                    written_outfile.write(''.join(current_doc))
                
                # Reset for the next document
                current_doc = []
                current_genre = ""
            # Start new document
            current_doc.append(line)
        else:
            current_doc.append(line)
            # Check for genre line
            if line.startswith('# meta::genre ='):
                try:
                    current_genre = line.split('=')[1].strip()
                    genre_counts[current_genre] += 1
                except IndexError:
                    pass  # Ignore invalid genres
    
    # Process the last document
    if current_doc:
        if current_genre in spoken_genres:
            spoken_outfile.write(''.join(current_doc))
        else:
            written_outfile.write(''.join(current_doc))

# Print genre occurrences
print("\nGenres and their occurrences:")
for genre, occurrences in sorted(genre_counts.items()):
    print(f"{genre}: {occurrences}")