#!/usr/bin/python

import xml.etree.ElementTree as et
import random
from datetime import datetime

BALLOON_TIME = 3000

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
        self.result['messages'] = self.__parse_messages__(root.find('messages')) # Messages
        return self.result

    def __parse_name__(self, name_element):
        if name_element != None:
            return name_element.text
        else:
            self.error = True
            return None

    def __parse_messages__(self, messages_element):
        if messages_element == None:
            self.error = True
            return None
        result = []
        for msg in messages_element: # Parse every message
            result.append(message(msg, {'name': self.result['name']}))
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
            nowtime = datetime.now()
            if self.time['year'] != None:
                if not nowtime.year in self.time['year']:
                    return False
            if self.time['month'] != None:
                if not nowtime.month in self.time['month']:
                    return False
            if self.time['day'] != None:
                if not nowtime.day in self.time['day']:
                    return False
            if self.time['hour'] != None:
                if not nowtime.hour in self.time['hour']:
                    return False
            if self.time['minute'] != None:
                if not nowtime.minute in self.time['minute']:
                    return False
            if self.time['second'] != None:
                if not nowtime.second in self.time['second']:
                    return False
            if self.time['weekday'] != None:
                if not nowtime.weekday() in self.time['weekday']:
                    return False
            return True

    def __cond_default__(self, condition_element):
        self.type = None

    def __cond_startup__(self, condition_element):
        self.type = 'startup'

    def __cond_end__(self, condition_element):
        self.type = 'end'

    def __cond_time__(self, condition_element):
        self.type = 'time'
        self.time = {}
        self.time['year'] = self.__parse_comma__(condition_element.get('year'))
        self.time['month'] = self.__parse_comma__(condition_element.get('month'))
        self.time['day'] = self.__parse_comma__(condition_element.get('day'))
        self.time['hour'] = self.__parse_comma__(condition_element.get('hour'))
        self.time['minute'] = self.__parse_comma__(condition_element.get('minute'))
        self.time['second'] = self.__parse_comma__(condition_element.get('second'))
        self.time['weekday'] = self.__parse_comma__(
            condition_element.get('weekday').lower()\
            .replace('sun','0').replace('mon','1').replace('tue','2')\
            .replace('wed','3').replace('thu','4').replace('fri','5')\
            .replace('sat','6') if condition_element.get('weekday') != None else None
        )

    def __parse_comma__(self, desc):
        if desc is None:
            return None
        result = []
        items = desc.split(',')
        for item in items:
            item = item.strip()
            if '-' in item: # from-to
                try:
                    num_from, num_to = item.split('-')
                    for i in range(int(num_from.strip()), int(num_to.strip()) + 1):
                        if not i in result:
                            result.append(i)
                except ValueError:
                    continue
            else: # one value
                try:
                    i = int(item)
                    if not i in result:
                        result.append(i)
                except ValueError:
                    continue
        return result

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
