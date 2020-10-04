#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify


def make_error(status, status_code, message):
    '''Function to create the error response in proper format
    '''

    response = jsonify({'status': status, 'reason': message})
    response.status_code = status_code
    return response
