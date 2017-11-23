#This Python file uses the following encoding: utf-8

import requests
import random
import config

def createURL(url, key, checkWord): #create URL with search words
    checkWord = checkWord.strip()

    checkWord = checkWord.replace(' ', '+').replace('\n', '')

    return url + key + '=' + checkWord

def getWebContent(targetURL): #get the content of the serp
    headers = {
        'User-Agent': random.choice(config.config['ualist'])
    }

    resault = requests.get(targetURL, headers = headers)

    return resault.content

def spliceDictionary(dictionary, spliceword, spliceKeyValueWord = '='): #splice dictionary
    temporary_list = []

    for key in dictionary:
        temporary_list.append(key + spliceKeyValueWord + dictionary.get(key))

    return spliceword.join(temporary_list)

def dd(*vartuple):
    for var in vartuple:
        print var

    return exit()