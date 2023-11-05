from tools.bucket import download_from_bucket, download_all_from_bucket, upload_to_bucket
from google.cloud import storage
import pickle
import re
import math
import os

file_name = "bwdata_test1.pkl"
def process_blob(blob_path):
    with open(blob_path, 'rb') as file:
        data = pickle.load(file)
    matches = re.findall(r'O1=([\d\.-]+),\s*O2=([\d\.-]+),\s*T3=([\d\.-]+),\s*T4=([\d\.-]+)', data)
    return [tuple(map(float, match)) for match in matches]

destination_folder = "blobs_tmp"
blob_paths = download_all_from_bucket('brainbit_bucket', destination_folder, prefix="bw_scans/")

client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-65e54374e3c7.json')
bucket = client.bucket('brainbit_bucket')

reference_blob_path = os.path.join(destination_folder, 'bw_scans', file_name)

if not os.path.isfile(reference_blob_path):
    download_from_bucket('brainbit_bucket', reference_blob_path, reference_blob_path)

reference_data = process_blob(reference_blob_path)
reference_base_name = os.path.splitext(os.path.basename(reference_blob_path))[0]
matches_pkl_name = f"matches_for_{reference_base_name}.pkl"
results = {}

for blob_path in blob_paths:
    if blob_path == reference_blob_path:
        continue
    current_data = process_blob(blob_path)
    distances = []
    blob_name = os.path.basename(blob_path)
    for ref_set, cur_set in zip(reference_data, current_data):
        distance = math.sqrt(sum([(i-j)**2 for i, j in zip(ref_set, cur_set)]))
        distances.append(distance)

    average_distance = sum(distances) / len(distances)
    results[blob_name] = average_distance
    print(f"Average distance for {blob_name}: {average_distance}")

matches_directory = 'blobs_tmp/users_match_data'

if not os.path.exists(matches_directory):
    os.makedirs(matches_directory)

matches_pkl_path = os.path.join(matches_directory, matches_pkl_name)
with open(matches_pkl_path, 'wb') as pickle_file:
    pickle.dump(results, pickle_file)

upload_to_bucket('brainbit_bucket', matches_pkl_path, f"users_match_data/{matches_pkl_name}")

