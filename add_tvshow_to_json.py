"""
    Script which is used to add a new tvshow to the favourite list of tvshows:
    tvshows.json
"""

import json
import os
import shutil
import datetime

# New tv shows to be added
new_tvshows = [
    {
        'name' : 'The Book of Boba Fett',
        'shortcut' : 'the-book-of-boba-fett',
        'new':'true'
    }
]

# Current time, used for backup files
now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M')

# Location to json files (original and backup)
tvshows_loc = os.path.join('data', 'tvshows.json')
tvshows_loc_backup = os.path.join('data', f'{now}_backup_tvshows.json')

# Make a backup of the original json file first
shutil.copyfile(tvshows_loc, tvshows_loc_backup)

# Read the json file
with open(tvshows_loc, 'r') as json_file:
    json_data = json.load(json_file)

# List variable for storing names of all tv shows
tvshow_name_list = []

# Go through the json file and grab the names of the tvshows
# then append them to the list
for tvshow_name in json_data['tvShows']:
    tvshow_name_list.append(tvshow_name['name'])

# Check if the new tv show is in the list of tv shows
# If not, append the new tv show to the json object
for new_tvshow in new_tvshows:
    print(new_tvshow)
    if new_tvshow['name'] not in tvshow_name_list:
        json_data['tvShows'].append(new_tvshow)

# Save the json object to a file
with open(tvshows_loc, 'w') as json_file:
    json.dump(json_data, json_file, indent=4, sort_keys=True, ensure_ascii=False)

# Print out new json data with recently added tv show
new_data = json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False)
print(new_data)
