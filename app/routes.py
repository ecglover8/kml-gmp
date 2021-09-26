# bring in app
from app import app

# import packages
import urllib.request
from flask import render_template, request
from lxml import etree
from pathlib import Path
from pykml import parser
from pykml.parser import Schema

#load in GMP schema
scheme = Schema("GMP_Schema.xsd")

# route requests for / and /index to index.html
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html", err_message="")

# route requests for /fileprocess    
@app.route("/fileprocess", methods=["GET", "POST"])
def valid1():
    if request.method == "POST":
        # make sure a file was actually chosen
        if request.files["kml"].filename != "":            
            # save uploaded file
            kmlfile = request.files["kml"]
            kmlfile.seek(0)
            kml = kmlfile.read()
            # validate KML file
            try:
                doc = parser.parse(kml, scheme)
                return render_template("valid.html", response="The KML file you just uploaded is correctly formed!")
            except etree.XMLSyntaxError as err:
                return render_template("invalid.html", response=str(err.error_log))
        return render_template("index.html", err_message="Please upload a file to continue.") 
    
# route requests for /urlprocess    
@app.route("/urlprocess", methods=["GET", "POST"])
def valid2():
    if request.method == "POST":
        # make sure a URL was inputted
        if request.form["url"] != "":
            # extract KML from link
            url = request.form["url"]
            kml_file = urllib.request.urlopen(url)
            # validate online KML
            try:
                doc = parser.parse(kml_file, scheme).getroot()
                return render_template("valid.html", response="The KML file you just linked to is correctly formed!")
            except etree.XMLSyntaxError as err:
                return render_template("invalid.html", response=str(err.error_log))
        return render_template("index.html", err_message="Please enter a URL to continue.")
    
# route requests for /textprocess    
@app.route("/textprocess", methods=["GET", "POST"])
def valid3():
    if request.method == "POST":
        # make sure text was inputted
        if request.form["txt"] != "":
            # extract KML from link
            txt = request.form["txt"]
            # validate KML from textarea
            try:
                doc = parser.fromstring(txt, scheme)  
                return render_template("valid.html", response="The KML sample you just entered is correctly formed!")
            except etree.XMLSyntaxError as err:
                return render_template("invalid.html", response=str(err.error_log))
            except ValueError:
                return render_template("index.html", err_message="Unicode strings with encoding declaration are not supported.")
        return render_template("index.html", err_message="Please copy-paste in your KML to continue.")