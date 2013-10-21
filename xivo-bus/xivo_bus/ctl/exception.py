# -*- coding: UTF-8 -*-


class BusCtlClientError(Exception):

    def __init__(self, error):
        Exception.__init__(self, error)
        self.error = error


class BusCtlServerError(Exception):

    error = 'server error'
