#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Gets a list of all Place objects in city'''
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city == []:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Gets a Place object'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places if obj.id == place_id]
    if place == []:
        abort(404)
    return jsonify(place[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places
                 if obj.id == place_id]
    if place == []:
        abort(404)
    place.remove(place[0])
    for obj in places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities
                if obj.id == city_id]
    if city == []:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    '''Updates a Place object'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places if obj.id == place_id]
    if place == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        place[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        place[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        place[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        place[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        place[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        place[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        place[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        place[0]['longitude'] = request.json['longitude']
    for obj in places:
        if obj.id == place_id:
            if 'name' in request.get_json():
                obj.name = request.json['name']
            if 'description' in request.get_json():
                obj.description = request.json['description']
            if 'number_rooms' in request.get_json():
                obj.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                obj.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                obj.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                obj.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                obj.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                obj.longitude = request.json['longitude']
    storage.save()
    return jsonify(place[0]), 200
