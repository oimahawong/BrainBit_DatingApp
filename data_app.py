from tools.bucket import download_all_from_bucket, upload_to_bucket
from google.cloud import storage
import pickle
import re
import math
import os

from db_con import get_db_instance

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


client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-a4aa72be527e.json') # Creates GCS instance
bucket = client.bucket('brainbit_bucket') # Access cloud bucket

average_distances = {} # Dictionary that holds results of comparisons
all_distances = [] # Store all calculated distances

# Compare each blob against every other blob
for i, blob_path_1 in enumerate(blob_paths):
    data_1 = process_blob(blob_path_1)
    blob_name_1 = os.path.basename(blob_path_1)
    average_distances[blob_name_1] = {}

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

        all_distances.extend(distances)

        # Calculate average distance and store it in results dictionary
        avg_distance = sum(distances) / len(distances)
        average_distances[blob_name_1][blob_name_2] = avg_distance
        print(f"Average distance between {blob_name_1} and {blob_name_2}: {avg_distance: 0.4f}")

min_distance = min(all_distances)
max_distance = max(all_distances)
match_percentages = {}

#SQL database cursor
db, cur = get_db_instance()

for blob1, comparisons in average_distances.items():
    match_percentages[blob1] = {}

    for blob2, avg_distance in comparisons.items():
        match_percentage = 100 * (1 - (avg_distance - min_distance) / (max_distance - min_distance))
        match_percentages[blob1][blob2] = match_percentage
        print(f"Match percentage between {blob1} and {blob2}: {match_percentage: 0.2f}%")
        
        # Add match percentage to SQL database
        userid_1 = blob1[:-11] if len(blob1) > 11 else blob1
        userid_2 = blob2[:-11] if len(blob2) > 11 else blob2
        cur.execute(f"update matches set {userid_2}={match_percentage} where id={userid_1}")
        db.commit()

# Directory to store pickled result comparisons
matches_directory = 'blobs_tmp/users_match_data'

# Create directory if it doesn't exist
if not os.path.exists(matches_directory):
    os.makedirs(matches_directory)

# Save and upload average_distances and match_percentages to the bucket
for blob_name in average_distances.keys():
    # Constructing file names for each dictionary
    avg_dist_pkl_name = f"average_distances_for_{blob_name}"
    match_perc_pkl_name = f"match_percentages_for_{blob_name}"

    # Full path for storing files
    avg_dist_pkl_path = os.path.join(matches_directory, avg_dist_pkl_name)
    match_perc_pkl_path = os.path.join(matches_directory, match_perc_pkl_name)

    # Pickle and save the average distances
    with open(avg_dist_pkl_path, 'wb') as pickle_file:
        pickle.dump(average_distances[blob_name], pickle_file)
    upload_to_bucket('brainbit_bucket', avg_dist_pkl_path, f"users_match_data/{avg_dist_pkl_name}")

    # Pickle and save the match percentages
    with open(match_perc_pkl_path, 'wb') as pickle_file:
        pickle.dump(match_percentages[blob_name], pickle_file)
    upload_to_bucket('brainbit_bucket', match_perc_pkl_path, f"users_match_data/{match_perc_pkl_name}")
