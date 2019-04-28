import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)




def main():
    # Example
    data = {}
    data['key'] = 'value2'

    writeToJSONFile('./','file-name',data)
    # './' represents the current directory so the directory save-file.py is in

main()
