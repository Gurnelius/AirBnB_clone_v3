#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    '''Lists all Amenity objects'''
    list_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Gets an Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    amenity.remove(amenity[0])
    for obj in amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''Creates an Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates an Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
                   if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity[0]), 200
