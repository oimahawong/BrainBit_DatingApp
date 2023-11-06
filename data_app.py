from tools.bucket import download_all_from_bucket, upload_to_bucket
from google.cloud import storage
import pickle
import re
import math
import os

# Process blobs and extract O1, O2, T3, T4 data
def process_blob(blob_path):
    # Unpickle data
    with open(blob_path, 'rb') as file:
        data = pickle.load(file)
    # Use regex to find data (int, float, and negatives) after O1, O2, T3, T4
    matches = re.findall(r'O1=([\d\.-]+),\s*O2=([\d\.-]+),\s*T3=([\d\.-]+),\s*T4=([\d\.-]+)', data)
    # Convert matches to tuples of floats and return
    return [tuple(map(float, match)) for match in matches]


destination_folder = "blobs_tmp"

# Downloads all blobs from cloud in 'bw_scans/' folder
blob_paths = download_all_from_bucket('brainbit_bucket', destination_folder, prefix="bw_scans/") # Holds list of local file paths to blobs


client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-65e54374e3c7.json') # Creates GCS instance
bucket = client.bucket('brainbit_bucket') # Access cloud bucket

all_results = {} # Dictionary that holds results of comparisons

# Compare each blob against every other blob
for i, blob_path_1 in enumerate(blob_paths):
    data_1 = process_blob(blob_path_1)
    blob_name_1 = os.path.basename(blob_path_1)
    all_results[blob_name_1] = {}

    for j, blob_path_2 in enumerate(blob_paths):
        # Skips current file
        if i == j:
            continue

        data_2 = process_blob(blob_path_2)
        blob_name_2 = os.path.basename(blob_path_2)

        # Calculate distances between corresponding data points in two data sets
        distances = []
        for ref_set, cur_set in zip(data_1, data_2):
            distance = math.sqrt(sum([(i - j) ** 2 for i, j in zip(ref_set, cur_set)]))
            distances.append(distance)

        # Calculate average distance and store it in results dictionary
        average_distance = sum(distances) / len(distances)
        all_results[blob_name_1][blob_name_2] = average_distance
        print(f"Average distance between {blob_name_1} and {blob_name_2}: {average_distance}")

# Directory to store pickled result comparisons
matches_directory = 'blobs_tmp/users_match_data'

# Create directory if it doesn't exist
if not os.path.exists(matches_directory):
    os.makedirs(matches_directory)

# Save result comparisons and upload to bucket
for blob_name, results in all_results.items():
    matches_pkl_name = f"matches_for_{blob_name}" # Name of file of comparison results
    matches_pkl_path = os.path.join(matches_directory, matches_pkl_name) # Sets full path to store file
    # Pickle the results
    with open(matches_pkl_path, 'wb') as pickle_file:
        pickle.dump(results, pickle_file)
    upload_to_bucket('brainbit_bucket', matches_pkl_path, f"users_match_data/{matches_pkl_name}") # Upload to bucket

