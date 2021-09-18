#!/usr/bin/env python
"""
Software developed by Eduardo Felipe Da Silva Braga - 17/09/2021
            GNU GENERAL PUBLIC LICENSE
                Version 2, June 1991

Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""

import sys
import os
import re
import csv
import unicodedata

def strNormalize(str):
    nkfd_form = unicodedata.normalize('NFKD', str)
    return u"".join([ch for ch in nkfd_form if not unicodedata.combining(ch)])

def determineFilename(filename):
    n = 1
    while os.path.isfile("CH-{num}.csv".format(num=n)):
        n+=1
    return "CH-{num}.csv".format(num=n)


def regex(text, names):
    regex = r"^[\d ]+\| ([\w ]+)\| [@a-zA-Z0-9 ]+\|"

    matches = re.finditer(regex, text, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if(strNormalize(match.group(groupNum).strip()) not in names):
                names[strNormalize(match.group(groupNum).strip())] = 0
            names[strNormalize(match.group(groupNum).strip())] += 1
    return names

def pathRetifier(path):
    regex = r"/$"
    if(re.search(regex, path) == None):
        return path+'/'
    return path

def dictRetifier(dictionary):
    list = []
    auxDictionary = {}
    for key, value in dictionary.items():
            list.append([key,value])
    return list


def main():
    filename = 'CH.csv'
    header = ['Nome Completo', 'Presence']
    data = {}
    
    try:
        argValidator = os.path.isfile(sys.argv[1]) or os.path.isdir(sys.argv[1])
    except:
        print("Ops! you need to specify a filename or directory")
        sys.exit()

    if((not os.path.isdir(sys.argv[1])) and (not os.path.isfile(sys.argv[1]))):
        print("Ops! the file or directory doesn't exist")
        sys.exit()

    elif(os.path.isfile(sys.argv[1])):
        with open(os.path.join(os.getcwd(), sys.argv[1]), 'r') as file:
            data = regex(file.read(), data)

    elif(os.path.isdir(sys.argv[1])):
        for files in os.listdir(sys.argv[1]):
            with open(os.path.join(os.getcwd(), sys.argv[1], files), 'r') as file:
                data.update(regex(file.read(),data))

    if(os.path.isfile('./'+filename)):
        filename = determineFilename(filename)

    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in data.items():
            if(key == ''):
                continue
            writer.writerow([key,value])

if __name__ == '__main__':
  main()