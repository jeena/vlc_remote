#!/usr/bin/env python3

"""
Library for contacting VLC through HTTP
"""

import logging
import xmltodict
import requests
import json

_LOGGER = logging.getLogger(__name__)

class ConnectionError(Exception):
    """Something is wrong with the connection to VLC."""
    pass

class VLCHttp(object):
    def __init__(self, host, password="", port=8080):
        self._host = host
        self._password = password
        self._port = port

    def run_command(self, command="", attrs=""):
        url = "http://{}:{}/requests/status.xml?command={}{}".format(self._host, self._port, command, attrs)
        data=None
        try:
            req = requests.get(url, auth=("", self._password), timeout=1)
            if req.status_code != 200:
                raise ConnectionError("Query failed, response code: %s Full message: %s".format(req.status, req))

            data = xmltodict.parse(req.text, process_namespaces=True).get("root")

        except Exception as error:
            _LOGGER.debug("Failed communicating with VLC Server: %s".format(error))

        try:
            return data
        except AttributeError:
            _LOGGER.error("Received invalid response: %s".format(data))

    def status(self):
        return self.run_command()

    def get_length(self):
        try:
            return int(self.status()['length'])
        except:
            pass

    def get_time(self):
        try:
            return int(self.status()['time'])
        except:
            pass
    
    def info(self):
        try:
            category = self.status()['information']['category']
            if type(category) is list:
                data = category[0]['info']
                if type(data) is list:
                    title = None
                    artist = None
                    for item in data:
                        if item['@name'] == 'title':
                            title = item['#text']
                        elif item['@name'] == 'artist':
                            artist = item['#text']
                            return [{"title": title, "artist": artist}]
                        elif data['@name'] == 'filename':
                            return [{"title": data['#text']}]
                        else:
                            return
        except Exception:
            return

    def seek(self, time):
        self.run_command("seek&val={}".format(time))
        
    def set_volume(self, new_volume):
        self.run_command("volume&val={}".format(new_volume))

    def play(self):
        self.run_command("pl_play")

    def pause(self):
        self.run_command("pl_pause")

    def stop(self):
        self.run_command("pl_stop")

    def add(self, url):
        self.run_command("in_play&input={}".format(url))

    def prev(self):
        self.run_command("pl_previous")

    def next(self):
        self.run_command("pl_next")

    def clear(self):
        self.run_command("pl_empty")

    def random(self):
        self.run_command("pl_random")

