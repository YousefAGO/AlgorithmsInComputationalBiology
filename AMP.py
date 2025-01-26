import pandas as pd

def preprocess_data(data_path, output_path, label):
    import pandas as pd

    # Define input and output file names
    fasta_file = data_path  # Change this if needed
    csv_file = output_path

    # Initialize variables
    sequences = []
    lengths = []
    length = 0
    current_sequence = ""

    # Read and process the FASTA file
    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):  # If it's a new header, save the previous sequence
                if current_sequence:
                    sequences.append(current_sequence)  # Save the completed sequence
                    lengths.append(length)  # Save the length of the sequence
                current_sequence = ""  # Reset for the new sequence
                length = 0  # Reset for the new sequence
            else:
                current_sequence += line  # Concatenate sequence lines
                length += len(line)  # Update the length of the sequence

    # Append the last sequence if it exists
    if current_sequence:
        sequences.append(current_sequence)
        lengths.append(length)

    # Create a DataFrame with Label = 0 (Non-AMPs)
    df = pd.DataFrame({"sequence": sequences, "label": label, "length": lengths})

    # Save to CSV
    df.to_csv(csv_file, index=False)

    print(f"✅ Conversion complete! Saved as: {csv_file}")


if __name__ == '__main__':
    preprocess_data("uniprotkb_AND_reviewed_true_AND_model_o_2025_01_26.fasta", "none-AMP.csv", 0)