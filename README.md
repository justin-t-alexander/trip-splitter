# trip-splitter
Trip Splitter is a full stack web application that simplifies traveling for large groups. Whether you’re on a road trip, group vacation, or splitting bills with friends, this app makes cost-sharing easy and transparent.



#Features

Add trip expenses with categories
Split costs among multiple users equally or by percent
Calculate who owes what
View a summary of shared expenses
Save and retrieve trip data via pdf



#Ensure you have the following installed

Node.js & npm
Python 3
pip



#Setup

git clone https://github.com/justin-t-alexander/trip-splitter.git
cd trip-splitter

cd backend
python3 -m venv venv  
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  
python app.py  # Runs the Flask server

cd frontend
npm install
npm start  # Runs the React app on localhost:3000



#Usage
Open http://localhost:3000 in your browser.
Add a new trip and enter shared expenses.
View the calculated cost split among participants.
Save or export the data.

