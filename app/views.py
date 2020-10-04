#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import app, db
from sqlalchemy import exc
from haversine import haversine

from flask import Flask, request, jsonify
from app.utils import make_error

from app.models import Driver
db.create_all()


class BadRequest(Exception):

    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


@app.after_request
def set_header(response):
    '''Set Response Header to return the content type as application/json
    '''

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/v1/driver/register/', methods=['POST'])
def register_driver():
    '''Register Driver Method

    :param name(required): the name of the driver.
    :type name: string
    :param email(required): the email of the driver
    :type email: string
    :param phone_number(required): the phone number of the driver (10)
    :type phone_number: number
    :param license_number(required): the license number of the driver
    :type license_number: string
    :param car_number(required): the car number used by the driver
    :type car_number: string

    :returns: driver details
    :rtype: dictionary
    '''

    data = request.get_json()
    if request.method == 'POST':
        try:
            name = data['name']
            email = data['email']
            phone_number = data['phone_number']
            if len(str(phone_number)) != 10:
                raise BadRequest('Phone Number should be 10')
            license_number = data['license_number']
            car_number = data['car_number']
            driver = Driver(name, email, phone_number, license_number,
                            car_number)
            db.session.add(driver)
            db.session.commit()
            res = Driver.query.get(driver.id)
            result = res.serialize()
            return (jsonify(result), 201)
        except (BadRequest, KeyError, exc.IntegrityError) as e:
            return make_error('failure', 400, str(e))


@app.route('/api/v1/driver/<id>/sendLocation/', methods=['POST'])
def sendLocation(id):
    '''Update the Driver Location

    :param id(required): the id of the driver taken from the route.
    :type name: string

    :param latitude(required): the latitude of the driver
    :type latitude: float
    :param longitude(required): the longitude of the driver
    :type longitude: float
 
    :returns: message
    :rtype: dictionary
    '''

    data = request.get_json()
    if request.method == 'POST':
        try:
            latitude = data['latitude']
            longitude = data['longitude']
            Driver.query.filter_by(id=int(id)).update(dict(latitude=latitude,
                    longitude=longitude))
            db.session.commit()
            return (jsonify({'status': 'success'}), 202)
        except (BadRequest, KeyError, exc.IntegrityError) as e:
            return make_error('failure', 400, str(e))


@app.route('/api/v1/passenger/available_cabs/', methods=['POST'])
def available_cabs():
    '''Get the Available cabs under 4 km
    :param latitude(required): the latitude of the driver
    :type latitude: float
    :param longitude(required): the longitude of the driver
    :type longitude: float
 
    :returns: list of cabs
    :rtype: dictionary
    '''

    data = request.get_json()
    available_cabs_data = []
    if request.method == 'POST':
        try:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
            drivers = Driver.query.all()
            for driver in drivers:
                if driver.latitude and driver.longitude:
                    distance = haversine((latitude, longitude),
                            (driver.latitude, driver.longitude), unit='km')
                    if distance <= 4:
                        available_cabs_data.append(driver.serialize())

            if len(available_cabs_data) > 0:
                return (jsonify({'available_cabs': list(available_cabs_data)}),
                        200)
            else:
                return (jsonify({'message': 'No cabs available!'}), 200)
        except (BadRequest, KeyError, exc.IntegrityError) as e:
            return make_error('failure', 400, str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
