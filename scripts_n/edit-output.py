import pandas as pd
import os

# Define the folder path where the file is located
folder_path = 'sample/jan25/output_2'  # Replace with your folder path

# Check if the folder exists and process the file
if os.path.exists(folder_path):
    print(f"Looking for files in folder: {folder_path}")
    
    for filename in os.listdir(folder_path):
        # Only process .tsv files
        if filename.endswith('.tsv'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            
            # Load the file
            df = pd.read_csv(file_path, sep='\t')

            # Identify columns to combine (those starting with 'Node A-form', 'Node B-form', etc.)
            node_columns = [col for col in df.columns if col.startswith("Node") and col.endswith("-form")]

            # Combine the node columns into a new column 'String' (space-separated) and drop the originals
            df['String'] = df[node_columns].apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
            df = df.drop(columns=node_columns)

            # Rename "Absolute frequency" to "Frequency"
            if 'Absolute frequency' in df.columns:
                df = df.rename(columns={'Absolute frequency': 'Frequency'})

            # Drop "Relative frequency" if it exists
            if 'Relative frequency' in df.columns:
                df = df.drop(columns=['Relative frequency'])

            # Define previously kept columns
            previous_columns = ['Tree', 'String', 'Frequency', 'Grew-match URL', 'Number of nodes']
            
            # Define additional columns to keep
            additional_columns = ['MI', 'MI3', 'Dice', 'logDice', 't-score', 'simple-LL']
            
            # Merge both lists and filter existing columns
            all_columns = previous_columns + additional_columns
            existing_columns = [col for col in all_columns if col in df.columns]
            
            # Reorder DataFrame to keep selected columns
            df = df[existing_columns]
            
            # Create output file path with "modified" prefix
            output_filename = f"modified_{filename}"
            output_path = os.path.join(folder_path, output_filename)
            
            # Save the modified DataFrame to a new file
            df.to_csv(output_path, sep='\t', index=False)
            print(f"Modified file saved to: {output_path}")

    print("Processing completed.")
else:
    print(f"The folder path '{folder_path}' does not exist. Please verify the path.")
