from .features import PEFeatureExtractor
import os
from multiprocessing import Pool
from tqdm import tqdm
import pickle
import json
import pandas as pd
import numpy as np


def extract_features(malware_filename):
    with open(malware_filename, "rb") as f:
        f_bytes = f.read()
    return extractor.raw_features(f_bytes)


def convert_bytes(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    raise TypeError(f"Type {type(obj)} not serializable")


extractor = PEFeatureExtractor()

base_dir = os.getenv("MALWARE_DIR_PATH")  # "/home/luca/WD/NortonDataset670/MALWARE"
malware_families_dirs = os.listdir(base_dir)

malware_filenames = []
for malware_family_dir in malware_families_dirs:
    malware_family_abs_dir = os.path.join(base_dir, malware_family_dir)
    for malware_filename in os.listdir(malware_family_abs_dir):
        malware_filenames.append(os.path.join(malware_family_abs_dir, malware_filename))

print("Number of malware match: ", len(malware_filenames) == 67000)

# Extract features
n_proc = int(os.getenv("N_PROCESSES"))
with Pool(n_proc) as p:
    malware_ember_features = list(
        tqdm(
            p.imap_unordered(extract_features, malware_filenames),
            total=len(malware_filenames),
        )
    )

# with open("malware_ember_features.pkl", "wb") as f:
#     pickle.dump(malware_ember_features, f)

features = []
for malware_features in tqdm(malware_ember_features, desc="Merging features"):
    features.append(extractor.process_raw_features(malware_features))


# Extract SHA256 to use them as DataFrame index
shas_256 = [malware_features["sha256"] for malware_features in malware_ember_features]

# Create the dataframe with column names of the full dataset (train + test)
df = pd.DataFrame(features, index=shas_256, columns=extractor.column_names())
print(df.head())

# Save the dataframe to a CSV file
malware_dataset_filename = os.path.join(
    os.getenv("FINAL_DATASET_DIR"), "malware_ember_features.csv"
)
df.to_csv(malware_dataset_filename, index=True, index_label="sha256")
print("DONE!")
