from collections import defaultdict

current_doc = []
current_speaker_count = 0
current_genre = ""
speaker_counts = defaultdict(int)
genre_counts = defaultdict(int)

spoken_genres = {"court", "interview", "conversation", "dialogue", "interview", "speech", "podcast", "vlog"}  # Adjust as needed

input_path = 'sample/gum/en_gum-ud-merged.conllu'  # Update with your actual input filename
spoken_output_path = 'sample/gum/output_spoken.conllu'
written_output_path = 'sample/gum/output_written.conllu'

both_conditions_count = 0  # Variable to count documents meeting both conditions
genres_with_speaker_count_greater_than_0 = defaultdict(int)  # Track genres where speaker count > 0

with open(input_path, 'r') as infile, \
     open(spoken_output_path, 'w') as spoken_outfile, \
     open(written_output_path, 'w') as written_outfile:
    
    for line in infile:
        if line.startswith('# newdoc'):
            # Process the previous document
            if current_doc:
                # Check the conditions for the document
                if (current_speaker_count < 1 or current_genre == "") and current_genre in spoken_genres:
                    both_conditions_count += 1  # Increment the count for both conditions
                    print(f"Document meets both conditions: Speaker Count: {current_speaker_count}, Genre: {current_genre}")
                
                # Track genres with speaker count > 0
                if current_speaker_count > 0:
                    genres_with_speaker_count_greater_than_0[current_genre] += 1
                
                # Determine where to write the document
                if current_speaker_count > 0 or current_genre in spoken_genres:
                    # If the genre is 'letter' or 'fiction', write to the written file instead
                    if current_genre in ["letter", "fiction"]:
                        written_outfile.write(''.join(current_doc))
                    else:
                        spoken_outfile.write(''.join(current_doc))
                else:
                    written_outfile.write(''.join(current_doc))
                
                # Reset for the next document
                current_doc = []
                current_speaker_count = 0
                current_genre = ""
            # Start new document
            current_doc.append(line)
        else:
            current_doc.append(line)
            # Check for speaker count line
            if line.startswith('# meta::speakerCount'):
                try:
                    count = int(line.split('=')[1].strip())
                    current_speaker_count = count
                    speaker_counts[count] += 1
                except (IndexError, ValueError):
                    pass  # Treat invalid counts as 0
            # Check for genre line
            if line.startswith('# meta::genre ='):
                try:
                    current_genre = line.split('=')[1].strip()
                    genre_counts[current_genre] += 1
                except IndexError:
                    pass  # Ignore invalid genres
    
    # Process the last document
    if current_doc:
        # Check the conditions for the last document
        if (current_speaker_count < 1 or current_genre == "") and current_genre in spoken_genres:
            both_conditions_count += 1  # Increment the count for both conditions
            print(f"Document meets both conditions: Speaker Count: {current_speaker_count}, Genre: {current_genre}")
        
        # Track genres with speaker count > 0
        if current_speaker_count > 0:
            genres_with_speaker_count_greater_than_0[current_genre] += 1
        
        # Determine where to write the document
        if current_speaker_count > 0 or current_genre in spoken_genres:
            # If the genre is 'letter' or 'fiction', write to the written file instead
            if current_genre in ["letter", "fiction"]:
                written_outfile.write(''.join(current_doc))
            else:
                spoken_outfile.write(''.join(current_doc))
        else:
            written_outfile.write(''.join(current_doc))

# Print speaker count occurrences
print("Speaker counts and their occurrences:")
for count, occurrences in sorted(speaker_counts.items()):
    print(f"{count}: {occurrences}")

# Print genre occurrences
print("\nGenres and their occurrences:")
for genre, occurrences in sorted(genre_counts.items()):
    print(f"{genre}: {occurrences}")

# Print the number of documents that meet both conditions
print(f"\nNumber of documents meeting both conditions: {both_conditions_count}")

# Print the genres where speaker count > 0
print("\nGenres with more than 0 speakers:")
for genre, doc_count in sorted(genres_with_speaker_count_greater_than_0.items()):
    print(f"{genre}: {doc_count}")
