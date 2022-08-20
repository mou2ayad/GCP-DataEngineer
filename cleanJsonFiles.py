import json

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def cleanJSONFile(jsonFilePath,cleanFilePath,dirtyFilePath):
    with open(jsonFilePath) as inputFile, open(cleanFilePath, 'w') as cf, open(dirtyFilePath, 'w') as df:
        for line in inputFile:
            if validateJSON(line):
                cf.write(line)
            else:
                df.write(line)
    return True

def cleanJsonFiles(directory,files):
    for file in files:
        cleanFilePath = directory + '/' + file.split('.')[0] + '_clean.json'
        dirtyFilePath = directory + '/' + file.split('.')[0] + '_dirty.json'
        cleanJSONFile(directory + '/' + file,cleanFilePath,dirtyFilePath)
    return True

files = ['yc_app_events_2022_05_31.json','yc_app_events_2022_06_02.json','yc_app_events_2022_06_01.json']

directory='/Users/mouayadkhashfeh/Downloads'

cleanJsonFiles(directory,files)


