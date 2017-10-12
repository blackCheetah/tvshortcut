# App for parsing HTML data from specific external website, showing favourite
# shows sorted by soonest release date
# -*- coding: utf-8 -*-
# !/usr/bin/env


# Importing required modules
import os
from datetime import datetime
import json
from flask import Flask, render_template, Markup, url_for
from bs4 import BeautifulSoup
import requests

# Declaration of Flask app
app = Flask(__name__)

# Global variables
# url link to external website
BASE_URL = r"https://www.edna.cz/"

# dictionary to store days till release of upcoming episode and it's corresponding html code 
# {days_till_release : html_data}
HTML_OUTPUT_DICT = {}

# Definitions
# Return current date and time
def current_time():
    i = datetime.now()
    now = ("%d.%d.%d | %d:%02d" % (i.day, i.month, i.year, i.hour, i.minute))

    return now


# Format date and current_time
def replace_date_format(date_string):
    date = datetime.strptime(date_string, '%d.%m. | %H:%M')

    return date

# Calculate days till release of a new episode
def days_till_release(date):
    current_date = datetime.now()

    date_new = datetime(current_date.year, date.month, date.day) - datetime(year=current_date.year, month=current_date.month, day=current_date.day)
    date_string = str(date_new).split(' ')[0]

    if date_string == '0:00:00':
        date_string = "0"

    return int(date_string)


def create_a_file(location, file_name, data_list):
    try:
        with open(os.path.join(location, file_name), "w", encoding='utf-8', errors='ignore') as output_file:
            results = ''.join(data_list)
            output_file.write(results)

    except FileNotFoundError as fNot:
        print("Jezuz christ!!! File not found!! \n{0}".format(fNot))


def file_modified_date(location, file_name):
    full_path = os.path.join(location,file_name)
    
    if os.path.exists(full_path):
        today = datetime.today()

        # today:  2017-08-04 20:08:00.963539
        modified_date = datetime.fromtimestamp(os.path.getmtime(full_path))

        # modified_date:  2017-08-04 19:58:00.498725
        duration = today - modified_date

        hours = duration.seconds // 3600
        minutes = duration.seconds // 60

        return (hours, minutes)

    else:
        return (-1, -1)



# Function to parse needed HTML data from specific external website
def get_data(url_link, show_name):

    # Get the html markup from the website and convert it to text
    source_code = requests.get(url_link, timeout=5, verify=False)
    html_text = source_code.text

    # Bsoup declaration
    b_soup = BeautifulSoup(html_text, "lxml")

    # Find parent of table element
    tbody = b_soup.table.parent

    # Remove domain name from url
    url_name = url_link.replace("https://www.edna.cz/", '')

    # Rename content of h2 element with tv show names
    for h2 in tbody.findAll("h2"):
        h2.string = show_name

    # Make all "a href" links usable/clickable
    for a in tbody.findAll(href=True):
        a_href = a.get('href')
        if not a['href'].startswith('https://www.'):
            a['href'] = r"https://www.edna.cz" + a_href

    # Make url in data-src the same as for src
    for img_index, img in enumerate(tbody.findAll("img")):
        data_src = img.get('data-src')
        img['data-src'] = r"https://www.edna.cz" + data_src
        img['src'] = r"https://www.edna.cz" + data_src

    if img_index < 3:
        tbody['class'] = tbody.get('class', []) + ['margin-extra']

    # Find date and time of upcoming episode and make it bald
    for td in tbody.findAll("td"):
        tag = b_soup.new_tag('b')
        newest_episode_date = td.string
        (td.string, tag.string) = ("", td.string)
        td.string.insert_before(tag)
        break

    # Generate days till release of each tv show episode
    formatted_date = replace_date_format(newest_episode_date)
    release_date = days_till_release(formatted_date)

    # Elements which have td.colspan="5" are active tv shows
    for _ in tbody.findAll("td", colspan=lambda x: x and x.startswith('5')):
        tbody['class'] = tbody.get('class', []) + ['active']
        break
    else:
        if release_date > 0:
            release_date *= -1

    # Get snippet id for each episode
    """for td_snippet in tbody.findAll("td", id=lambda x: x and x.startswith('snippet--episodes-')):
        # print("td_snippet: ", td_snippet.get('id'))
        snippet_id = int(td_snippet.get('id').replace("snippet--episodes-", ''))
    """
    # Remove unnecessary script at the bottom of the page, saving loading time
    for x in tbody.findAll('colgroup'):
        x.extract()
    for x in tbody.findAll('td', {"colspan": 8}):
        x.extract()

    # Html output with parsed prettified data
    html_output = Markup(tbody.prettify() + "<br/>")

    # append html code (value) to dictionary HTML_OUTPUT_DICT based on release_date (key)
    HTML_OUTPUT_DICT.setdefault(int(release_date), []).append(html_output)


def load_json(location, file_name):
    full_path = os.path.join(location, file_name)
    with open(full_path, "r", encoding='utf-8', errors='ignore') as output_file:
        json_load_file = json.load(output_file)

    return json_load_file

# Run through tv shows dictionary with show names and url names, parse needed data in function get_data
LOADED_JSON = load_json("data", "tvshows.json")
NUM_OF_TVSHOWS = len(LOADED_JSON['tvShows'])

def run_tv_shows():

    for i in range(0, NUM_OF_TVSHOWS):
        tv_show_shortcut = LOADED_JSON['tvShows'][i]['shortcut']
        tv_show_name = LOADED_JSON['tvShows'][i]['name']
    
        get_data(BASE_URL + tv_show_shortcut, tv_show_name)


# Sort html output by days till release of new episode for each tv show
def get_data_sorted():

    filename="data.html"
    file_modified = file_modified_date("templates", filename)

    print("# get_data_sorted > {} file has been modified {}h {}m ago "
        .format(filename, file_modified[0], file_modified[1])
    )
    
    if 12 > file_modified[0] >= 0:
        return ''

    # Function to run through tv shows and parse needed html data
    run_tv_shows()

    # sorted list of strings with html codes for each episode
    tv_sorted_list = []

    # sorted dictionary from lowest positive number to lowest negative number
    sort_equation = lambda x: (x[0] < 0, abs(x[0]))
    sorted_html_output_dict = sorted(HTML_OUTPUT_DICT.items(), key=sort_equation, reverse=False)

    # append value (html codes) to list "tv_sorted_list" by key in sorted_dict
    for _, value in sorted_html_output_dict:
        value = ''.join(value)
        tv_sorted_list.append(value)

    create_a_file("templates/", "data.html", tv_sorted_list)

    return ''


# Functions to be callable in "index.html" template
app.jinja_env.globals.update(get_data_sorted=get_data_sorted)
app.jinja_env.globals.update(num_of_tvshows=NUM_OF_TVSHOWS)
app.jinja_env.globals.update(current_time=current_time)

# Add timestamp for static css, to generate a new cached css on every load
@app.context_processor
def override_url_for():
    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)
    return dict(url_for=dated_url_for)


# Default routing to homepage
@app.route('/')
def index():
    # Rendering content of "index.html"
    return render_template("index.html")


# Running app locally with cpu threads for faster results
if __name__ == '__main__':
    app.run(threaded=True, debug=True)
