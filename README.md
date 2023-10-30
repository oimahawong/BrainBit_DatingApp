# BrainBit Dating App

## How to install and run the Flask server
### Setup
1. Clone this github repository:
```
git clone https://github.com/oimahawong/BrainBit_DatingApp.git
```
or
```
git clone git@github.com:oimahawong/BrainBit_DatingApp.git`
```
2. [Download and install python](https://www.python.org/downloads/)
3. Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html):
```
python -m venv /path/to/venv
source /path/to/venv/bin/activate
```
4. Install required python dependencies:
```
pip install -r requirements.txt
```
5. Initialize the database. Database can be reset by deleting `users.sqlite3` and re-running the below command:
```
python db_con.py
```

### Running the server
1. Configure based on whether or not you're running on Windows with the BrainBit SDK installed. Comment out lines 10, 36, and 37 in app.py if running in an environment without the BrainBit SDK, uncomment them if BrainBit functionality is needed:
```
from tools.eeg import get_head_band_sensor_object
```
and
```
if 'hb' not in g:
    g.hb = get_head_band_sensor_object()
```
3. Start the server:
```
python app.py
```
3. Access the server by visiting `http://localhost` in a web browser.

##### Available webpages
- `/`: The splash page. Redirects to other pages as needed.
- `/video`: Holds the video users will watch while their brains are scanned. WIP.
- `/signup`: Holds the user signup form. Data input here will be saved to the database file.
