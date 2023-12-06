# BrainBit Dating App

## Installing and running the Flask server
### Setup
1. Clone this github repository:
2. [Download and install python](https://www.python.org/downloads/)
3. Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html)
4. Install required python dependencies:
```
pip install -r requirements.txt
```
5. Initialize the database. Running the below command without arguments initializes an empty database. Adding the `full` argument additionally populates the database with 4 dummy users for testing purposes:
```
python db_con.py [full]
```

### Running the server
1. Start the server. If your environment does not support the BrainBit SDK (neurosdk), it will not be loaded and a warning will print to the python console:
```
python app.py
```
2. Access the server by visiting `http://localhost` in a web browser.

##### Available webpages
- `/`: The splash page. Redirects to other pages as needed.
- `/signup`: Holds the user signup form. Data input here will be saved to the database file.
- `/video`: Holds the video users watch while their brains are scanned.
- `/results`: Displays the closest match for returning users.

## Calculating Matches
Run the below command. This retrieves any stored brainscan data and calculates the match distance and percentage for each user pair in the database. Match percentages are saved back to the database:
```
python data_app.py
```

## Database Structure
The database consists of 3 tables as described below.
##### users (Users)
| id (User ID) | name (Username) | email (User email) | img (Reference to profile image) |
| --- | --- | --- | --- |
##### images (Profile images)
| id (Image ID) | path (Path to image from /static) |
| --- | --- |
##### matches (User pair match data)
| id (User ID to cross-reference) | match_1 (Match percentages for user ID 1) | ... | match_# (Match percentages for user ID #) |
| --- | --- | --- | --- |

The columns of the matches table are dynamically expanded as users are added to the database.
