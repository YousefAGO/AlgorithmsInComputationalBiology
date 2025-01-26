import torch
import esm

# Load ESM-2 model (smallest version for quick testing)
model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
batch_converter = alphabet.get_batch_converter()

# Example peptide sequences
sequences = [("peptide1", "MKKVLLLVGA"), ("peptide2", "GFTYRDEKM")]
batch_labels, batch_strs, batch_tokens = batch_converter(sequences)

# Extract embeddings
with torch.no_grad():
    results = model(batch_tokens, repr_layers=[6])
    embeddings = results["representations"][6].mean(1).numpy()  # Mean pooling


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load AMP dataset (CSV with columns: 'sequence', 'label')
import pandas as pd
df = pd.read_csv("amp_dataset.csv")


if __name__ == '__main__':
    # Convert sequences to embeddings
    peptides = [(str(i), seq) for i, seq in enumerate(df["sequence"])]
    batch_labels, batch_strs, batch_tokens = batch_converter(peptides)
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[6])
        features = results["representations"][6].mean(1).numpy()

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(features, df["label"], test_size=0.2, random_state=42)

    # Train Classifier
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

