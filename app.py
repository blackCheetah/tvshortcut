# App for parsing data from specific external website
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Markup
from bs4 import BeautifulSoup
import requests
#from datetime import datetime

app = Flask(__name__)

# Global variables
BASE_URL = r"http://www.edna.cz/"

# Names of the tv shows and their link, to be manually updated with new shows
tv_shows = {
"Arrow" : "/arrow/",
"Agents of S.H.I.E.L.D." : "/agents-of-shield/",
"Better Call Saul" : "/better-call-saul/",
"Daredevil" : "/daredevil/",
"Fear the Walking Dead" : "/fear-the-walking-dead/",
"Game of Thrones" : "/game-of-thrones/",
"Gotham" : "/gotham/",
"Iron Fist": "/iron-fist/",
"Jessica Jones" : "/jessica-jones/",
"Legends of Tomorrow" : "/legends-of-tomorrow",
"Luke Cage" : "/luke-cage",
"Marco Polo" : "/marco-polo/",
"Mr. Robot" : "/mr-robot",
"Supergirl" : "/supergirl/",
"Vikings" : "/vikings/",
"The Flash" : "/the-flash/",
"The Walking Dead" : "/walking-dead/"
}

# Function to parse all of the needed data from external website
def get_data(url_link, url_name, show_name):

    # Get the html markup from the website and convert it to text
    source_code = requests.get(url_link+url_name, timeout=5, verify=False)
    html_text = source_code.text

    # Bsoup declaration
    b_soup = BeautifulSoup(html_text,"lxml")

    # Find parent of table element
    tbody = b_soup.table.parent

    # Rename content of h2 element with shows' name
    for h2 in tbody.findAll("h2"):
        h2.string = show_name

    # Make all "a href" links usable
    for a in tbody.findAll("a"):
        #print(a)
        a_href = a.get('href')

        if url_name in a_href:
            a['href'] = r"http://www.edna.cz" + a_href

    # Make url in data-src the same as for src
    for img in tbody.findAll("img"):
        data_src = img.get('data-src')
        #src = img.get('src')

        img['data-src'] = r"http://www.edna.cz" + data_src
        img['src'] = r"http://www.edna.cz" + data_src

    # Remove unnecessary script at the bottom
    [x.extract() for x in tbody.findAll('td', {"colspan" : 8})]

    # Html output with parsed data
    html_output = Markup(tbody.prettify() + "<br/>")

    return html_output

# Def "get_data(url_link, url_name, show_name)" to be callable in "index.html"
app.jinja_env.globals.update(get_data=get_data)

# Default routing to homepage
@app.route('/')
def index():
    # Rendering content of "index.html"
    return render_template("index.html", tv_shows=tv_shows, base_url=BASE_URL)

# Running app locally
if __name__ == '__main__':
    app.run(debug=True)
