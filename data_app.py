from tools.bucket import download_all_from_bucket, upload_to_bucket
from google.cloud import storage
import pickle
import re
import math
import os

def process_blob(blob_path):
    with open(blob_path, 'rb') as file:
        data = pickle.load(file)
    matches = re.findall(r'O1=([\d\.-]+),\s*O2=([\d\.-]+),\s*T3=([\d\.-]+),\s*T4=([\d\.-]+)', data)
    return [tuple(map(float, match)) for match in matches]

destination_folder = "blobs_tmp"
blob_paths = download_all_from_bucket('brainbit_bucket', destination_folder, prefix="bw_scans/")

client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-65e54374e3c7.json')
bucket = client.bucket('brainbit_bucket')

all_results = {}

for i, blob_path_1 in enumerate(blob_paths):
    data_1 = process_blob(blob_path_1)
    blob_name_1 = os.path.basename(blob_path_1)
    all_results[blob_name_1] = {}

    for j, blob_path_2 in enumerate(blob_paths):
        if i == j:
            continue

        data_2 = process_blob(blob_path_2)
        blob_name_2 = os.path.basename(blob_path_2)

        distances = []
        for ref_set, cur_set in zip(data_1, data_2):
            distance = math.sqrt(sum([(i - j) ** 2 for i, j in zip(ref_set, cur_set)]))
            distances.append(distance)

        average_distance = sum(distances) / len(distances)
        all_results[blob_name_1][blob_name_2] = average_distance
        print(f"Average distance between {blob_name_1} and {blob_name_2}: {average_distance}")

matches_directory = 'blobs_tmp/users_match_data'

if not os.path.exists(matches_directory):
    os.makedirs(matches_directory)

for blob_name, results in all_results.items():
    matches_pkl_name = f"matches_for_{blob_name}"
    matches_pkl_path = os.path.join(matches_directory, matches_pkl_name)
    with open(matches_pkl_path, 'wb') as pickle_file:
        pickle.dump(results, pickle_file)
    upload_to_bucket('brainbit_bucket', matches_pkl_path, f"users_match_data/{matches_pkl_name}")

