import pandas as pd

def preprocess_data(data_path, output_path, label):
    import pandas as pd

    # Load FASTA file and remove empty rows & headers
    fasta_file = data_path
    sequences = []

    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith(">"):  # Ignore headers and empty lines
                sequences.append(line)

    # Create CSV file
    df = pd.DataFrame({"sequence": sequences, "label": label})
    df.to_csv(output_path, index=False)

    print(f"✅ CSV file saved as %s" % output_path)


if __name__ == '__main__':
    preprocess_data("uniprotkb_AND_reviewed_true_AND_model_o_2025_01_26.fasta", "none-AMP.csv", 0)