import os

def Console(globalData):
    
    if(os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')
    for key, value in globalData.items():
        globals()[key] = value    
    if 'system.hsf' in os.listdir('.cache/'):
        print(f"[ LOAD ] Noticed previously stored session. Loading now...")
        try:
            loadSession(globalData,'./.cache/system.hsf')
        except Exception as e:
            print(f"[ WARN ] Corrupted session file. Unable to load variables. Session will be saved and restored upon exit of terminal.")
    #try:
    while True:
        userInput = input(f"{config['websocket']['web_socket_endpoint_value']}")
        if userInput.lower() not in blacklistDefinitions['command_list'] and userInput != '':
            match userInput.split()[0].lower():
                
                case "debug":
                    try:
                        envResponse = exec(f"{userInput[6:len(userInput)]}")
                        print(f"[ DEBG ] {envResponse}")
                    except Exception as e:
                        print(f"[ EXCP ] {e}")
                case "help":
                    try:
                        helpFile(userInput[5:len(userInput)])
                    except Exception as e:
                        print(f"[ FAIL ] Unable to open help file: {e}")
                case "load":
                    if "session" in userInput.lower():
                        try:
                            if len(userInput.split()) > 2:
                                loadSession(globalData, userInput.split()[2])
                            else:
                                loadSession(globalData, './.cache/system.hsf')
                        except Exception as e:
                            print(f"[ FAIL ] Unable to reload session: {e}")
                            pass
                case "save":
                    if "config" in userInput.lower():
                        with open('config.ini', 'w', encoding='utf-8') as configState:
                            config.write(configState)
                    elif "session" in userInput.lower():
                        if len(userInput.split()) > 2:
                            saveSession(globals(),userInput.split()[2])
                        else:
                            saveSession(globals(),'./.cache/system.hsf')
                    else:
                        helpFile('save')
                case "exit":
                    try:
                        if len(userInput.split()) > 1:
                            saveSession(globals(),'./.cache/system.hsf')
                            exit(int(userInput.split()[1]))
                        else:
                            exit()
                    except Exception as e:
                        print(f"[ FAIL ] An error occured: {e}")
                case _:
                    try:
                        print("not implemented")
                    except Exception as e:
                        print(f"[ FAIL ] An error occured: {e}")
        else:
            if(userInput != ''):
                print(f"[ EXCP ] Firewall rules disabled this command.")
            
    #except Exception as e:
    #    print(f"[ NOTE ] An error occured while running the main instance.")
    #    print(f"[ DATA ] {e}")
    #    print(f"[ KILL ] A catastrophic error occured while attempting to run interface. Ending instance.")

def saveSession(globalList, filename):
    print('[ SAVE ] Saving session... Do not exit or power off.')
    with open(f"{filename}", 'w') as sessionState:
        blankState = {}
        for key, value in globalList.items():
            if not inspect.isfunction(key) and not isinstance(key, type):
                blankState[str(key)] = str(value)
            else:
                print(f"[ SKIP ] Skipping unsavable instance: {key}")
        print(f"[ SAVE ] Exporting...")
        sessionInfo = json.dumps(blankState)
        sessionState.write(sessionInfo)
    print(f"[ SAVE ] Successfully saved to: {filename}")

def loadSession(globalData, filename):
    try:
        sessionFile = open(filename).read()
        environmentArray = json.loads(sessionFile)
        for key, value in environmentArray.items():
            if '__' not in key and isinstance(value, str) == True:
                    globals()[key] = value
            else:
                print(f"[ NOTE ] Skipping possible library or encoding dispute: {key}")
        print("[ LOAD ] Reimporting required libraries...")
        for key, value in globalData.items():
            globals()[key] = value
        try:
            sessionFile.close()
        except:
            pass
    except Exception as e:
        print(f"[ FAIL ] Unable to reload session token: {e}")
        pass

def saveConfig(config, filename='config.ini'):
    with open('config.ini', 'w', encoding='utf-8') as configState:
        config.write(configState)