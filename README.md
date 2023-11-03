# BrainBit Dating App

## How to install and run the Flask server
### Setup
1. Clone this github repository:
2. [Download and install python](https://www.python.org/downloads/)
3. Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html)
4. Install required python dependencies:
```
pip install -r requirements.txt
```
5. Initialize the database. Database can be reset by deleting `users.sqlite3` and re-running the below command:
```
python db_con.py
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
- `/video`: Holds the video users will watch while their brains are scanned.
