import os
from collections import defaultdict

spoken_genre_counts = defaultdict(int)
written_genre_counts = defaultdict(int)
spoken_speaker_counts = defaultdict(int)
written_speaker_counts = defaultdict(int)

spoken_output_path = 'sample/gum/output_spoken.conllu'
written_output_path = 'sample/gum/output_written.conllu'

def process_file(file_path, genre_counts, speaker_counts):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        current_speaker_count = 0
        current_genre = ""
        current_doc = []

        for line in file:
            # Check for genre line
            if line.startswith('# meta::genre ='):
                current_genre = line.split('=')[1].strip()

            # Check for speaker count line
            if line.startswith('# meta::speakerCount'):
                try:
                    count = int(line.split('=')[1].strip())
                    current_speaker_count = count
                except (IndexError, ValueError):
                    pass  # Treat invalid counts as 0

            # If a new document starts, process the previous document
            if line.startswith('# newdoc'):
                if current_doc:  # Process the current document if it's not empty
                    # Only count documents that have a valid genre or speaker count
                    if current_genre and current_speaker_count >= 0:
                        genre_counts[current_genre] += 1
                        speaker_counts[current_speaker_count] += 1

                current_doc = [line]  # Reset for the next document

            else:
                current_doc.append(line)

        # Process the last document after the loop
        if current_doc:
            if current_genre and current_speaker_count >= 0:
                genre_counts[current_genre] += 1
                speaker_counts[current_speaker_count] += 1

# Process the spoken and written files to gather statistics
process_file(spoken_output_path, spoken_genre_counts, spoken_speaker_counts)
process_file(written_output_path, written_genre_counts, written_speaker_counts)

# Print the statistics for the spoken file
print("Spoken File Statistics:")
print("\nGenres in Spoken File:")
for genre, count in sorted(spoken_genre_counts.items()):
    print(f"{genre}: {count} documents")

print("\nSpeaker Counts in Spoken File:")
for speaker_count, count in sorted(spoken_speaker_counts.items()):
    print(f"{speaker_count} speakers: {count} documents")

# Print the statistics for the written file
print("\nWritten File Statistics:")
print("\nGenres in Written File:")
for genre, count in sorted(written_genre_counts.items()):
    print(f"{genre}: {count} documents")

print("\nSpeaker Counts in Written File:")
for speaker_count, count in sorted(written_speaker_counts.items()):
    print(f"{speaker_count} speakers: {count} documents")
