from tools.bucket import download_from_bucket, download_all_from_bucket
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
blob_paths = download_all_from_bucket('brainbit_bucket', destination_folder)

client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-65e54374e3c7.json')

bucket = client.bucket('brainbit_bucket')

blobs = list(bucket.list_blobs())

reference_blob_path = os.path.join(destination_folder, 'bwdata_test1.pkl')
reference_data = process_blob(reference_blob_path)

all_distances = []
for blob_path in blob_paths:
    if blob_path == reference_blob_path:
        continue
    current_data = process_blob(blob_path)
    distances = []

    for ref_set, cur_set in zip(reference_data, current_data):
        distance = math.sqrt(sum([(i-j)**2 for i, j in zip(ref_set, cur_set)]))
        distances.append(distance)

    all_distances.extend(distances)
    average_distance = sum(distances) / len(distances)
    print(f"Average distance for {blob_path}: {average_distance}")

min_distance = min(all_distances)
max_distance = max(all_distances)

for blob_path in blob_paths:
    if blob_path == reference_blob_path:
        continue

    current_data = process_blob(blob_path)
    distances = [math.sqrt(sum([(i - j) ** 2 for i, j in zip(ref_set, cur_set)])) for ref_set, cur_set in
                 zip(reference_data, current_data)]
    match_percentages = [100 * (1 - (distance - min_distance) / (max_distance - min_distance)) for distance in distances]
    #for idx, match_percentage in enumerate(match_percentages, 1):
    #    print(f"Set {idx} for blob {blob_path}: {match_percentage}% match")

    average_match_percentage = sum(match_percentages) / len(match_percentages)
    print(f"Average Match Percentage for {blob_path}: {average_match_percentage}% match")

    os.remove(blob_path)
os.remove(reference_blob_path)

