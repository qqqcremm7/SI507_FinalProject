## SI507 Final Project

# Structure:
1. The project gets data from wikipedia and a specific csv and saved raw results in cache files
2. Use function 'createbdall' to call all related functions needed for building the database
3. Use serial functions begin with 'db_' to process data for later presentation
4. Use Flask names 'app' to give visual output to user

# Requirement
1. beautifulsoup4==4.8.1   Flask==1.1.1
2. Need to import secret.py which provides API keys.
3. Need to unzip the templates.zip

# User guide (after running the py file):
1. If you want to get official website of specific university and get a link redirecting you to the site, input in explorer, for example: “127.0.0.1:5000/website/University of Michigan”, and several options are provided.
2. If you want to find cafes near specific university, for example, input “127.0.0.1:5000/nearbycafe/University of Michigan” in explorer, then several options are provided.
3. If you want to get the map of the university and its nearby venues, for example, input in explorer: “127.0.0.1:5000/map/University of Michigan”, then several options provided.
4. If you want to get list of regions and their numbers of universities in QS Rankings ordered by average score of local universities, input in explorer: '127.0.0.1:5000/score', then only 1 option provided.
5. If you want to get list of America universities ordered by its rank in 2019 or 2018, input in explorer, for example, '127.0.0.1:5000/universityrankings/2019 rank', and 2 options provided.
