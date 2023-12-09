from tools.bucket import download_all_from_bucket, upload_to_bucket
from google.cloud import storage
import pickle
import re
import math
import os
from email.message import EmailMessage
import ssl
import smtplib
from email.utils import make_msgid
from pathlib import Path


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
        cur.execute(f"update matches set match_{userid_2}={match_percentage} where id={userid_1}")
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

def attach_image(email_message, image_path):
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
        img_filename = Path(image_path).name
        email_message.add_attachment(img_data, maintype='image', subtype=Path(image_path).suffix.lstrip('.'), filename=img_filename)

db, cur = get_db_instance()

email_sender = 'soulfinders.match@gmail.com'
email_password = input('Password: ')

# Iterate through users 1-4
for userid in range(1, 5):
    cur.execute("select name, email, img from users where id=?", (userid,))
    thisuser = cur.fetchone()

    if not thisuser:
        print(f"No data found for user ID {userid}")
        continue

    cur.execute("select path from images where id=?", (thisuser[2],))
    thisimg = f"static/images/{cur.fetchone()[0]}"

    # Fetch ordered list of matches by match %
    cur.execute(f"select id, match_{userid} from matches order by match_{userid} desc")
    match = cur.fetchall()

    if not match:
        print(f"No match data found for user ID {userid}")
        continue
    
    # Iterate over top 3 matches
    thatuser = []
    thatimg = []
    for i in range(3):
      cur.execute("select name, email, img from users where id=?", (match[i][0],))
      thatuser.append(cur.fetchone())
      if not thatuser[i]:
        break
      cur.execute("select path from images where id=?", (thatuser[i][2],))
      thatimg.append(f"static/images/{cur.fetchone()[0]}")

    email_receiver = thisuser[1]
    subject = 'Your Best Match'

    html_body = f"""
    <html>
        <body>
            <h1>Hello, {thisuser[0]}!</h1>
            <p>You have new matches!</p>
            <h2>{thatuser[0][0]}</h2>
            <p>Match percentage: {match[0][1]}%</p>
            <h2>{thatuser[1][0]}</h2>
            <p>Match percentage: {match[1][1]}%</p>
            <h2>{thatuser[2][0]}</h2>
            <p>Match percentage: {match[2][1]}%</p>
            <p>See attached images for profile pictures.</p>
        </body>
    </html>
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content("This is an automated message.")
    em.add_alternative(html_body, subtype='html')

    for i in range(3):
      attach_image(em, thatimg[i])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    print(f"Email sent to user ID {userid}")
