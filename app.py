# App for parsing HTML data from specific external website, showing favourite
# shows sorted by soonest release date
# -*- coding: utf-8 -*-


# Importing required modules
from flask import Flask, render_template, Markup, url_for
from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import time

# import heapq
# import collections
# import jinja2
# import operator
# import re
# from queue import Queue
# from threading import Thread

# Declaration of Flask app
app = Flask(__name__)


# Global variables
# url link to external website
BASE_URL = r"http://www.edna.cz/"
# dictionary to store days till release of upcoming episode and it's corresponding html code
html_output_dict = {}


# Names of the tv shows and their link; to be manually updated with new tv shows
tv_shows = {
    "Arrow":
    "arrow",

    "Agents of S.H.I.E.L.D.":
    "agents-of-shield",

    "Better Call Saul":
    "better-call-saul",

    "Daredevil":
    "daredevil",

    "Fear the Walking Dead":
    "fear-the-walking-dead",

    "Game of Thrones":
    "game-of-thrones",

    "Gotham":
    "gotham/",

    "Iron Fist":
    "iron-fist",

    "Jessica Jones":
    "jessica-jones",

    "Legends of Tomorrow":
    "legends-of-tomorrow",

    "Luke Cage":
    "luke-cage",

    "Marco Polo":
    "marco-polo",

    "Mr. Robot":
    "mr-robot",

    "Supergirl":
    "supergirl",

    "Vikings":
    "vikings",

    "The Flash":
    "the-flash",

    "The Walking Dead":
    "walking-dead",

    "Prison break":
    "prison-break",

    "American Gods (NOVINKA) ":
    "american-gods",

    "Narcos (NOVINKA) ":
    "narcos",

    "House of Cards (NOVINKA)":
    "house-of-cards",

    "Peaky Blinders (NOVINKA)":
    "peaky-blinders",

    "West World (NOVINKA)":
    "westworld",

    "Homeland (NOVINKA)":
    "homeland",

    "The 100 (NOVINKA)":
    "the-hundred",

    "SouthPark":
    "south-park",

    "Defenders":
    "defenders"
}


# Return current date and time
def current_time():
    i = datetime.now()
    now = ("%d.%d.%d | %d:%02d" % (i.day, i.month, i.year, i.hour, i.minute))

    return now


# Format date and time and calculate days till release of a new episode
def replace_date_format(date_obj):
    date = datetime.strptime(date_obj, '%d.%m. | %H:%M')
    current_date = datetime.now()

    date_new = datetime(current_date.year, date.month, date.day) - datetime(year=current_date.year, month=current_date.month, day=current_date.day)
    date_string = str(date_new).split(' ', 1)[0]

    if date_string == "0:00:00":
        date_string = "0"

    return date_string


def create_a_file(location, file_name, data_list):
    try:
        with open(os.path.join(location, file_name), "w", encoding='utf-8', errors='ignore') as output_file:
            results = ''.join(data_list)
            output_file.write(results)

    except FileNotFoundError as fNot:
    #except IOError as e:
        print("Jezuz christ!!! File not found!! \n{0}".format(fNot))


def file_modified_date(location, file_name):
    if (os.path.exists(location + "/" + file_name)):
        today = datetime.today()
        # today:  2017-08-04 20:08:00.963539
        modified_date = datetime.fromtimestamp(os.path.getmtime(location + "/" + file_name))
        # modified_date:  2017-08-04 19:58:00.498725
        duration = today - modified_date
        minutes = duration.total_seconds() // 60
        hours = duration.total_seconds() // 3600

        #print("today: ", today)
        #print("modified_date: ", modified_date)
        #print("duration.days: ", duration)
        #print("duration.total_seconds(): ", duration.total_seconds())
        #print("hours: ", hours)
        #print("minutes: ", minutes)

        return hours

    else:
        #print("test")
        return -1



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
    url_name = url_link.replace("http://www.edna.cz/", '')

    # Rename content of h2 element with tv show names
    for h2 in tbody.findAll("h2"):
        h2.string = show_name
        # print(h2)

    # Make all "a href" links usable/clickable
    for a in tbody.findAll("a"):
        a_href = a.get('href')
        # print("a_href:", a_href)
        if url_name in a_href:
            a['href'] = r"http://www.edna.cz" + a_href

    # Make url in data-src the same as for src
    img_counter = 0
    for img in tbody.findAll("img"):
        data_src = img.get('data-src')
        # src = img.get('src')
        img['data-src'] = r"http://www.edna.cz" + data_src
        img['src'] = r"http://www.edna.cz" + data_src
        img_counter += 1
    # print("img_counter: ", img_counter)

    if img_counter < 3:
        #tbody['class'] = tbody['class'] + 'margin-extra'
        tbody['class'] = tbody.get('class', []) + ['margin-extra']

    # Find date and time of upcoming episode and make it bald
    for td in tbody.findAll("td"):
        tag = b_soup.new_tag('b')
        temp_string = td.string
        td.string = ""
        tag.string = temp_string
        td.string.insert_before(tag)
        break

    # Generate days till release of each tv show episode

    days_till_release = int(replace_date_format(temp_string))

    """if int(days_till_release) < -7:
        tbody['class'] = 'episodes-bg disabled'
    """

    for col in tbody.findAll("td", colspan=lambda x: x and x.startswith('5')):
        # print("td_snippet: ", td_snippet.get('id'))
        # print("col: ", col)
        tbody['class'] = tbody.get('class', []) + ['active']
        break
    else:
        if days_till_release > 0:
            days_till_release *= -1

    # Get snippet id for each episode
    """for td_snippet in tbody.findAll("td", id=lambda x: x and x.startswith('snippet--episodes-')):
        # print("td_snippet: ", td_snippet.get('id'))
        snippet_id = int(td_snippet.get('id').replace("snippet--episodes-", ''))
    """
    # Remove unnecessary script at the bottom of the page, saving loading time
    [x.extract() for x in tbody.findAll('colgroup')]
    [x.extract() for x in tbody.findAll('td', {"colspan": 8})]

    # Html output with parsed prettified data
    html_output = Markup(tbody.prettify() + "<br/>")

    # append html codes (values) to dictionary html_output_rendered based on days_till_release (keys)
    html_output_dict[int(days_till_release)] = html_output

    # return html_output


# Run through tv shows dictionary with show names and url names, parse needed data in function get_data
def run_tv_shows():
    for show_name, url_name in tv_shows.items():
        get_data(BASE_URL + url_name, show_name)


# Sort html output by days till release of new episode for each tv show
def get_data_sorted():

    file_modified = file_modified_date("templates", "data.html")

    print("file modified: ", file_modified)
    if file_modified >= 0 and file_modified < 12:
        return ''

    # Function to run through tv shows and parse needed html data
    run_tv_shows()

    # sorted list of strings with html codes for each episode
    tv_sorted_list = []

    # sorted dictionary from lowest positive number to lowest negative number
    sorted_html_output_dict = sorted(html_output_dict.items(), key=lambda x: (x[0] < 0, abs(x[0])), reverse=False)
    # sorted_dict = collections.OrderedDict(sorted(html_output_rendered.items(), key=lambda x: (x[0] < 0, x), reverse=False))
    # key=lambda x: (x[0] < 0, x)
    # operator.itemgetter(0)

    # append value (html codes) to list "tv_sorted_list" by key in sorted_dict
    # counter = 0
    for key, value in sorted_html_output_dict:
        # counter += 1
        # print("value: ", value)
        tv_sorted_list.append(value)
        # test = ("%02d.Key: %02d" % (counter, key))
        # print(test)

    create_a_file("templates/", "data.html", tv_sorted_list)

    return ''

    # join html codes in tv_sorted_list together and return it all
    #results = ''.join(tv_sorted_list)
    #return results


# Functions to be callable in "index.html" template
app.jinja_env.globals.update(get_data_sorted=get_data_sorted)
app.jinja_env.globals.update(current_time=current_time)
app.jinja_env.globals.update(tv_shows=tv_shows)
# app.jinja_env.globals.update(sorted=sorted)
# app.jinja_env.globals.update(get_data=get_data)
# app.add_template_filter(filter_supress_none)


# Add timestamp for static css, to generate a new cached css on every load
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# Default routing to homepage
@app.route('/')
def index():
    # Rendering content of "index.html"
    return render_template("index.html")


# Running app locally with cpu threads for faster results
if __name__ == '__main__':
    app.run(threaded=True, debug=True)
