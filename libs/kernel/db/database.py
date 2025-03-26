import json, configparser

def encryptString(string, key):
    encryptedString = ''
    try:
        for char in str(json.dumps(string)):
            encryptedString = encryptedString + chr(ord(char)+len(cryptocode.encrypt(key,key)))
    except Exception as exceptionPurpose:
        print(f"Exception while encrypting object\n\n {exceptionPurpose}")
    return(encryptedString)

def encryptObject(object, key):
    encryptedString = ''

    try:
        for char in str(json.dumps(object)):
            encryptedString = encryptedString + chr(ord(char)+len(cryptocode.encrypt(key,key)))
    except Exception as exceptionPurpose:
        print(f"Exception while encrypting object\n\n {exceptionPurpose}")
    return(encryptedString)

def decryptString(string, key):
    decryptedString = ''

    try:
        for char in str(string):
            decryptedString = decryptedString + chr(ord(char)-len(cryptocode.encrypt(key,key)))
    except Exception as exceptionPurpose:
        print(f"Exception while decrypting\n\n {exceptionPurpose}")
    return(decryptedString)

def decryptObject(stringin, key): #A string is given so "string" fits better in this case
    decryptedString = ''
    try:
        for char in str(stringin):
            decryptedString = decryptedString + chr(ord(char)-len(cryptocode.encrypt(key,key)))
    except Exception as exceptionPurpose:
        print(f"Exception while decrypting object\n\n {exceptionPurpose}")
    return(json.loads(cryptocode.decrypt(decryptedString, key)))

def loadDBDefinitions(location,key): #This loads the db definition file.
    try:
        definitionFile = open(str(location),'r',encoding='utf-8')
        return(decryptObject(str(definitionFile.read()),str(key)))
        
    except Exception as e:
        print(f"Exception while navigating definition file. \n\n {e}")

def importDatabase(path):
    try:
        definitionFile = open(str(path),'r',encoding='utf-8')
        globals()['storage_dom'] = json.loads(str(definitionFile.read()))
        print('Storage loaded')
    except Exception as e:
        print(f"Exception while navigating definition file. \n\n {e}")

#    print(loadDBDefinitions(str(path),str(userInput)))
#    try:
#        print('Successfully decrypted')
#        return(loadDBDefinitions(str(path),str(userInput)))
#    except Exception as e:
#        return('Unable to decrypt storage media')