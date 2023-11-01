from tools.bucket import download_from_bucket
import pickle
import re
import math
import os


download_from_bucket('brainbit_bucket', 'bwdata_test1.pkl', 'blobs1')
download_from_bucket('brainbit_bucket', 'bwdata_test2.pkl', 'blobs2')

# Unpickle data downloaded from bucket
with open('blobs1', 'rb') as file:
    data1 = pickle.load(file)
    #print(data1)

# Unpickle data downloaded from bucket
with open('blobs2', 'rb') as file:
    data2 = pickle.load(file)
    #print(data2)

matches1 = re.findall(r'O1=([\d\.-]+),\s*O2=([\d\.-]+),\s*T3=([\d\.-]+),\s*T4=([\d\.-]+)', data1)
matches2 = re.findall(r'O1=([\d\.-]+),\s*O2=([\d\.-]+),\s*T3=([\d\.-]+),\s*T4=([\d\.-]+)', data2)

data1_o1 = []
data1_o2 = []
data1_t3 = []
data1_t4 = []

data2_o1 = []
data2_o2 = []
data2_t3 = []
data2_t4 = []

for match in matches1:
    o1, o2, t3, t4 = match
    data1_o1.append(float(o1))
    data1_o2.append(float(o2))
    data1_t3.append(float(t3))
    data1_t4.append(float(t4))

for match in matches2:
    o1, o2, t3, t4 = match
    data2_o1.append(float(o1))
    data2_o2.append(float(o2))
    data2_t3.append(float(t3))
    data2_t4.append(float(t4))

distances = []

for o1_1, o2_1, t3_1, t4_1, o1_2, o2_2, t3_2, t4_2 in zip(data1_o1, data1_o2, data1_t3, data1_t4, data2_o1, data2_o2, data2_t3, data2_t4):
    distance = math.sqrt((o1_1 - o1_2)**2 + (o2_1 - o2_2)**2 + (t3_1 - t3_2)**2 + (t4_1 - t4_2)**2)
    distances.append(distance)

for idx, distance in enumerate(distances, 1):
    print(f"Set {idx}: {distance}")

average_distance = sum(distances) / len(distances)

print(f"Average distance: {average_distance}")

min_distance = min(distances)
max_distance = max(distances)

match_percentages = [100 * (1 - (distance - min_distance) / (max_distance - min_distance)) for distance in distances]

for idx, match_percentage in enumerate(match_percentages, 1):
    print(f"Set {idx}: {match_percentage}% match")

# Calculate average match percentage
average_match_percentage = sum(match_percentages) / len(match_percentages)

# Print the average match percentage
print(f"Average Match Percentage: {average_match_percentage}%")


os.remove('blobs1')
os.remove('blobs2')