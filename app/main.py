from flask import Flask
from flask import request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home_view():
	return "<h1>get stickbugged</h1>"

google_API_key = os.environ.get('GOOGLE_API_KEY')

def parse_args(value):
	coords = value.split('&', 1)
	lat = -1
	lng = -1
	for c in coords:
		if c.split('=')[0] == "long":
			lng = float(c.split('=')[1])
		elif c.split('=')[0] == "lat":
			lat = float(c.split('=')[1])
	if lat == -1 or lng == -1:
		return None
	return (lat, lng)

def get_geocode_coords(coordinates):
	reverse_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={coordinates[0]},{coordinates[1]}&key={google_API_key}"

	response = requests.get(reverse_url)

	print(reverse_url)
	if response.json()["status"] == "OK":
		result_address = response.json()["results"][0]["formatted_address"]

		print(result_address)

		result_address = result_address.replace(' ', '+')
		geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={result_address}&key={google_API_key}"

		response = requests.get(geocode_url)

		result_location = response.json()["results"][0]["geometry"]["location"]

		print(result_location)
		return result_location
	return None

def hash_coords(coordinates):
	if coordinates is None:
		return -1
	lat = lo = coordinates["lat"] + 90
	lng = hi = coordinates["lng"] + 180
	while lat < 0xffff and lng < 0xffff:
		lo = lat
		hi = lng
		lat *= 10
		lng *= 10
	lo = int(lo)
	hi = int(hi) << 16
	return lo + hi

@app.route("/seed")
def hash():
	args = request.args
	seed = "git seed"
	if args:
		coords = (args["lat"], args["long"])
		seed = -1
		if coords:
			new_coords = get_geocode_coords(coords)
			seed = hash_coords(new_coords)
		print(seed)
	return f"<h1>{seed}</h1>"

