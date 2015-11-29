#!/usr/bin/python

import xml.etree.ElementTree as et

class configFile:
    def __init__(self, filename):
        self.f = filename
        self.error = False
        
    def parse(self):
        self.error = False
        result = {}
        root = et.parse(self.f).getroot()
        result['name'] = self.__parse_name__(root.find('name'))
        result['messages'] = self.__parse_messages__(root.find('messages'))
        return result
        
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
        for msg in messages_element:
            result.append(self.__parse_message__(msg))
        return result
        
    def __parse_message__(self, message_element):
        if message_element == None:
            self.error = True
            return None
        result = {}
        result['conditions'] = self.__parse_conditions__(message_element.find('conditions'))
        result['contents'] = self.__parse_contents__(message_element.find('contents'))
        return result
        
    def __parse_conditions__(self, conditions_element):
        if conditions_element == None:
            self.error = True
            return None
        result = []
        for cond in conditions_element:
            result.append(condition(cond))
        return result
        
    def __parse_contents__(self, contents_element):
        if contents_element == None:
            self.error = True
            return None
        result = []
        for cont in contents_element:
            result.append(cont.text)
        return result
            
class condition:
    def __init__(self, condition_element):
        condition_switcher = {
            'startup': self.__cond_startup__
        }
    
        if(condition_element == None):
            return
        condition_switcher.get(condition_element.get('type'), self.__cond_default__)(condition_element)
        
    def __cond_default__(self, condition_element):
        return None
        
    def __cond_startup__(self, condition_element):
        self.type = 'startup'