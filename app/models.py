#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import db


class Driver(db.Model):

    ''' Model for the Driver
    '''

    __tablename__ = 'driver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone_number = db.Column(db.Numeric(10), unique=True)
    license_number = db.Column(db.String(255), unique=True)
    car_number = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(
        self,
        name,
        email,
        phone_number,
        license_number,
        car_number,
        latitude=None,
        longitude=None,
        ):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.license_number = license_number
        self.car_number = car_number
        self.longitude = longitude
        self.latitude = latitude

    def serialize(self):
        '''Serialize the Object to JSON response
        '''

        response = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': int(self.phone_number),
            'license_number': self.license_number,
            'car_number': self.car_number,
            }
        if self.latitude:
            response['latitude'] = float(self.latitude)
        if self.longitude:
            response['long'] = float(self.longitude)
        return response
