import random
random.seed(485)
import pandas as pd

MAX_SEQ_NUM = 10000
NUMBER_OF_SEQ = 154

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
    count = 0
    # Read and process the FASTA file
    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()
            count += 1
            if line.startswith(">"):  # If it's a new header, save the previous sequence
                if current_sequence:
                    sequences.append(current_sequence)  # Save the completed sequence
                    lengths.append(length)  # Save the length of the sequence
                current_sequence = ""  # Reset for the new sequence
                length = 0  # Reset for the new sequence
            else:
                current_sequence += line  # Concatenate sequence lines
                length += len(line)  # Update the length of the sequence
            if count == MAX_SEQ_NUM/2:
                break
    # Append the last sequence if it exists
    if current_sequence:
        sequences.append(current_sequence)
        lengths.append(length)

    print(f"✅ Conversion complete! Saved as: {csv_file}")
    # Function to extract random peptide fragments
    def extract_random_peptides(protein_seq, num_peptides=3, min_len=5, max_len=200):
        peptides = []
        seq_len = len(protein_seq)

        # Skip sequences shorter than the minimum length
        if seq_len < min_len:
            return []

        for _ in range(num_peptides):
            peptide_len = random.randint(min_len, min(max_len, seq_len))  # Ensure peptide fits in the sequence
            start_pos = random.randint(0, seq_len - peptide_len)  # Choose a random start position
            peptides.append(protein_seq[start_pos:start_pos + peptide_len])

        return peptides

    # Extract random peptides from each protein sequence
    random_peptides = []
    i = 0
    for protein_seq in sequences:
        l = lengths[i]
        seq = extract_random_peptides(protein_seq, num_peptides=int(random.uniform(0.7, 0.9)*(l)) + 1)
        random_peptides.extend(seq)  # Extract 3 peptides per protein
        if len(random_peptides) >= MAX_SEQ_NUM:
            break
    lengths = []
    for peptide in random_peptides:
        lengths.append(len(peptide))

    # sample NUMBER_OF_SEQ indexes from the list of random peptides
    index_list = range(len(random_peptides))
    sampled_indexes = random.sample(index_list, NUMBER_OF_SEQ)
    random_peptides = [random_peptides[i] for i in sampled_indexes]
    lengths = [lengths[i] for i in sampled_indexes]

    # Create a DataFrame with Label = 0 (Non-AMPs)
    df = pd.DataFrame({"sequence": random_peptides[:NUMBER_OF_SEQ], "label": [label]*NUMBER_OF_SEQ})

    # Save to CSV
    df.to_csv(csv_file, index=False)


def draw_len_hist():
    import matplotlib.pyplot as plt

    # Load the dataset
    df = pd.read_csv("none-AMP2.csv")

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df["length"], bins=50, color="skyblue", edgecolor="black")
    plt.title("Distribution of Sequence Lengths")
    plt.xlabel("Sequence Length")
    plt.ylabel("Count")
    plt.grid(axis="y", alpha=0.75)
    plt.show()

if __name__ == '__main__':
    preprocess_data("uniprotkb_AND_reviewed_true_AND_model_o_2025_01_26.fasta", "none-AMP4.csv", 0)
