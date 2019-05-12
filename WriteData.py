import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)




def writeData(data):
    # Example


    writeToJSONFile('./','output',data)
    # './' represents the current directory so the directory save-file.py is in

def printData(data):
    print(data)
