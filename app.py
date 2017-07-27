# App for parsing HTML data from specific external website, showing favourite
# shows sorted by soonest release date
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

"""
@app.route('/')
def index():
    return "index page"
"""
@app.route('/')
def index():
    base_url = r"http://www.edna.cz"
    short_name = "/gotham/"
    show_name = "Gotham"
    url_link = base_url + short_name


    source_code = requests.get(url_link, verify=False)
    html_text = source_code.text
    b_soup = BeautifulSoup(html_text,"html.parser")

    #print (tbody)
    tbody = b_soup.table.parent

    for h2 in tbody.findAll("h2"):
        h2.string = show_name

    for a in tbody.findAll("a"):
        #print(a)
        a_href = a.get('href')

        if short_name in a_href:
            a['href'] = r"http://www.edna.cz" + a_href


    for img in tbody.findAll("img"):
        data_src = img.get('data-src')
        src = img.get('src')

        img['data-src'] = r"http://www.edna.cz" + data_src
        img['src'] = r"http://www.edna.cz" + src

    #Remove script at the bottom
    [x.extract() for x in tbody.findAll('td', {"colspan" : 8})]

    html_output = tbody.prettify()

    return html_output.encode('utf-8')


"""
if __name__ == '__main__':
    app.run(debug=True)
"""
