from functools import cache
import requests
from geopy.geocoders import Nominatim
import folium
from flask import Flask, render_template, request

def address_to_coordinates(address):
    if address != "":
        try:
            location = Nominatim(user_agent='tutorial').geocode(address, timeout=180)
            coordinate = (location.latitude, location.longitude)
            return coordinate
        except AttributeError:
            pass
    else:
        return 0

def create_new_list(user_list):
    new_list = []
    for user in user_list:
        coordinate = address_to_coordinates(user[-1])
        if coordinate is not None and coordinate != 0:
            new_list.append((user[0],coordinate))
        if len(new_list) == 30:
            return new_list
    return new_list


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("twittertemplate.html")

@app.route("/create_map", methods = ["POST"])
def create_map():
    username = request.form.get("username")
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIgRZQEAAAAAfqkKxMTK%2Bkj5g5I4tDMLQQfKFws%3DEuumTSAiA7eWUr3h78W4n8EWlTCHBfyeBYfpRL1oauyPChiZsh"
    headers = {'Authorization': f'Bearer {bearer_token}'}
    params = {'screen_name': username, 'count': 200}
    response = requests.get('https://api.twitter.com/1.1/friends/list.json',
                        headers=headers,
                        params=params)

    if list(response.json().keys()) == ['errors']:
        return render_template("failure.html")
    user_list = [[user["name"], user["location"]] for user in response.json()["users"]]
    coordinates = create_new_list(user_list)
    my_map = folium.Map(zoom_start=5)
    for user in coordinates:
        folium.Marker(location = tuple(user[-1]), popup = user[0], tooltip='click').add_to(my_map)
    return my_map._repr_html_()

if __name__ == "__main__":
    app.run(debug = False)