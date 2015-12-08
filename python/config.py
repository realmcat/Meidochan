#!/usr/bin/python

import xml.etree.ElementTree as et
import random
from datetime import datetime

BALLOON_TIME = 3000
DEFAULT_DATETIME = '%Y/%m/%d %H:%M:%S'

class configFile:
    def __init__(self, filename):
        self.f = filename
        self.error = False
        self.result = None

    # Parse a config file
    def parse(self):
        self.error = False
        self.result = {}
        # Get root node
        root = et.parse(self.f).getroot()
        self.result['name'] = self.__parse_name__(root.find('name')) # Name
        self.result['datetime'] = self.__parse_datetime__(root.find('datetime')) # Format of datetime
        self.result['messages'] = self.__parse_messages__(root.find('messages')) # Messages
        return self.result

    def __parse_name__(self, name_element):
        if name_element != None:
            return name_element.text
        else:
            self.error = True
            return None

    def __parse_datetime__(self, datetime_element):
        if datetime_element != None:
            return datetime_element.text
        else:
            # Use default
            return DEFAULT_DATETIME

    def __parse_messages__(self, messages_element):
        if messages_element == None:
            self.error = True
            return None
        result = []
        for msg in messages_element: # Parse every message
            result.append(message(msg, {'name': self.result['name'], 'datetime': self.result['datetime']}))
        return result

    def findMessageByCondition(self, conditions = {}): # Find a message with a specific group of conditions
        if self.result == None:
            self.parse()
        result = []
        for msg in self.result['messages']:
            if msg.checkConditions(conditions):
                result.append(msg)
        return result

class condition:
    def __init__(self, condition_element, global_attr):
        self.global_attr = global_attr
        # Available conditions
        condition_switcher = {
            'startup': self.__cond_startup__,
            'end': self.__cond_end__,
            'time': self.__cond_time__,
        }

        if(condition_element == None):
            return
        condition_switcher.get(condition_element.get('type'), self.__cond_default__)(condition_element)

    # Check if the specific condition list meets the criteria
    def checkCondition(self, conditions):
        if self.type == None:
            return False

        if self.type == 'startup':
            if 'startup' in conditions:
                if conditions['startup']:
                    return True
            return False
        elif self.type == 'end':
            if 'end' in conditions:
                if conditions['end']:
                    return True
            return False
        elif self.type == 'time':
            if self.time == None:
                return False
            if datetime.now().replace(microsecond = 0) == self.time: # We don't need ms when comparing time
                return True
            else:
                return False

    def __cond_default__(self, condition_element):
        self.type = None

    def __cond_startup__(self, condition_element):
        self.type = 'startup'

    def __cond_end__(self, condition_element):
        self.type = 'end'

    def __cond_time__(self, condition_element):
        self.type = 'time'
        try:
            self.time = datetime.strptime(condition_element.get('time'), self.global_attr['datetime'])
        except ValueError:
            self.time = None

class message:
    def __init__(self, message_element, global_attributes):
        if message_element == None:
            self.error = True
            return None
        self.global_attr = global_attributes
        self.result = {}
        self.result['conditions'] = self.__parse_conditions__(message_element.find('conditions'))
        self.result['contents'] = self.__parse_contents__(message_element.find('contents'))

    def __parse_conditions__(self, conditions_element):
        if conditions_element == None:
            self.error = True
            return None
        result = []
        for cond in conditions_element:
            result.append(condition(cond, self.global_attr))
        return result

    def __parse_contents__(self, contents_element):
        if contents_element == None:
            self.error = True
            return None
        result = []
        for cont in contents_element:
            result.append(cont.text)
        return result

    # Choose a random message
    def chooseMessage(self):
        if self.result == None:
            self.parse()
        return random.choice(self.result['contents']).replace('{NAME}', self.global_attr['name'])

    # Check conditions (AND logic)
    def checkConditions(self, conditions):
        result = True
        for cond in self.result['conditions']:
            if not cond.checkCondition(conditions):
                result = False
        return result
