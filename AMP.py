import pandas as pd

def preprocess_data():
    import pandas as pd

    # Load FASTA file and remove empty rows & headers
    fasta_file = "humanAMPs_APD2024.fasta.txt"
    sequences = []

    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith(">"):  # Ignore headers and empty lines
                sequences.append(line)

    # Create CSV file
    df = pd.DataFrame({"sequence": sequences, "label": 1})
    df.to_csv("human_AMPs_dataset.csv", index=False)

    print("✅ CSV file saved as 'human_AMPs_dataset.csv'")


if __name__ == '__main__':
    preprocess_data()