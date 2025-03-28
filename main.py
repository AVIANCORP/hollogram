#NOTE: SHOULD BE GOOD
import os, configparser, json, sys, uuid
from importlib import import_module
import cryptocode
##import config file for getting general properties
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf8")
postload = []
moduleList = ['os','configparser','json','sys','uuid']
def libraryImport(folderLocation):
    generalBlob = {}
    postLoadList = []
    for moduleListing in os.listdir(folderLocation):
        print(f"[ LOAD ] Module: {moduleListing}")
        for fileListing in os.listdir(f"{folderLocation}/{moduleListing}"):
            if 'config.ini' in fileListing:
                moduleConfigurationFile = configparser.ConfigParser()
                moduleConfigurationFile.read(f"{folderLocation}/{moduleListing}/config.ini", encoding="utf8")
                if(moduleConfigurationFile['module']['module_type'] not in config['firewall']['blacklist_type']):
                    if('module_file' in moduleConfigurationFile['module']): #This is used to import libraries inside the module file
                        try:
                            #This will import resources required for the module to function correctly in a list based format in-case multiple libraries are required.
                            for moduleFile in json.loads(str(moduleConfigurationFile['module']['module_file'])):
                                globals()[moduleFile.replace('.py','')] = import_module(f"{folderLocation.replace('./','').replace('.','').replace('/','.')}.{moduleListing}.{moduleFile.replace('.py','')}","*") 
                                print(f"[  OK  ] Loaded {str(moduleListing)} resource: {str(moduleFile).replace('.py','')}")
                        except Exception as e:
                            #This allows the service to still run if non-important scripts are not loaded and exit if something bad happened.
                            #module_required will need to be set to True if you need the software to close if an error occurs while importing a file.
                            if 'module_required' in moduleConfigurationFile['module'] and moduleConfigurationFile['module']['module_required'] == 'True':
                                print(f"[ KILL ] Catastrophic exception occured: {e}\n[ EXIT ] Killing instance.")
                                sys.exit()
                            else:
                                print(f"[ WARN ] Exception occured: {e}")
                    if('python_modules' in moduleConfigurationFile['module']): #This imports python libraries
                        for module in json.loads(moduleConfigurationFile['module']['python_modules']):
                            try:
                                globals()[module] = import_module(module)
                                globals()['moduleList'].append(module)
                            except Exception as e:
                                #This allows the service to still run if non-important scripts are not loaded and exit if something bad happened.
                                #module_required will need to be set to True if you need the software to close if an error occurs while importing a file.
                                if 'module_required' in moduleConfigurationFile['module'] and moduleConfigurationFile['module']['module_required'] == 'True':
                                    print(f"[ KILL ] Catastrophic exception occured: {e}\n[ EXIT ] Killing instance.")
                                    sys.exit(1)
                                else:
                                    print(f"[ WARN ] Exception occured: {e}")
                    #If a module has a greeting assigned to it, upon it being loaded it will respond with a custom response instead of a generic load response.
                    if('module_greeting' in moduleConfigurationFile['module']):
                        print(f"[  OK  ] {str(moduleConfigurationFile.get('module','module_greeting'))}")
                    if('post_init' in moduleConfigurationFile['module']):
                        inputRequirement = {}
                        if('@' in moduleConfigurationFile['module']['post_init']):
                            #This cleans up the variable so that it can be used as a custom value once the bootstrapper is loaded
                            #If a function has a custom value required that the bootstrapper or program is unable to generate off the bat,
                            #this can be used to compensate for that issue with user input being generated.
                            #NOTE: Will probably need clean up and optimization because I don't believe this is good way to accomplish this.
                            #NOTE TO OTHER DEVS: There is a visual representation of what is going on since I know this will confuse me later
                            #and I am sure it will confuse you as well.
                            #["function(", "@user_input,", "@user_input_2)"] - will remove first element since it is the function and the '@'.
                            for variableName in moduleConfigurationFile['module']['post_init'].split('@')[1:]:
                                #["user_input","user_input_2"] - removes right bracket and commas
                                randString = str(uuid.uuid4()).split('-')[1]
                                if('random' in variableName):
                                    inputRequirement[randString] = [True,'general']
                                else:
                                    #input required: False, string type: general
                                    inputRequirement[variableName.split()[0].replace(',','').replace(')','')] = [False,'general']
                                    #input required: True, string type: general
                        
                        moduleID = str(f"{moduleListing}:{moduleConfigurationFile['module']['post_init'].split('(')[0]}")
                        if '@random' not in moduleConfigurationFile['module']['post_init']:
                            offboardData = [moduleConfigurationFile['module']['post_init'].replace('@','')]
                            globals()['postload'].append({moduleID:{"offboard_function":offboardData, "onboard_function":inputRequirement}})
                        else:
                            variableList = ''.join(inputRequirement)                                    
                            offboardData = [moduleConfigurationFile['module']['post_init'].replace('@random','').replace('(',str('('+variableList))]
                            globals()['postload'].append({moduleID:{"offboard_function":offboardData, "onboard_function":inputRequirement}})
                    if('handover_control' in moduleConfigurationFile['module']):
                        if(modules, api, encryption, blacklistDefinitions):
                            lightKernel = f"{folderLocation.replace('./','').replace('.','').replace('/','.')}/{moduleListing}/{moduleConfigurationFile['module']['handover_control']}"
                            with open(str(lightKernel), 'r') as file:
                                modules = globals()["modules"]
                                api = globals()["api"]
                                encryption = globals()["encryption"]
                                blacklistDefinitions = globals()["blacklistDefinitions"]
                                moduleConfigurationFile = globals()["moduleConfigurationFile"]
                                exec(str(file.read()), {'modules': modules,
                                                        'api': api,
                                                        'encryption': encryption,
                                                        'blacklistDefinitions': blacklistDefinitions,
                                                        'moduleConfigurationFile': moduleConfigurationFile})
                else:
                    print(f"[ XXXX ] {moduleListing} is blacklisted.\n"+
                          f"[ !!!! ] Enable the \"{moduleConfigurationFile['module']['module_type']}\" type to allow use.")              
                    
modules = libraryImport(config.get('config','modules_path'))
api = libraryImport(config.get('config','api_path'))
encryption = libraryImport(config.get('config','encryption_path'))
blacklistDefinitions = {"ip_list":json.loads(config.get('firewall','blacklist_ips')),
                        "command_list":json.loads(config.get('firewall','blacklist_requests')),
                        "username_list":json.loads(config.get('firewall','blacklist_usernames')),
                        "libraries_array":json.loads(config.get('firewall','blacklist_libraries'))}

hollogram = libraryImport(config.get('config','system_path'))
try:
    for functionData in postload:
        #functionBootstrap = postload[functionData]
        for moduleFunction, functionData in functionData.items():
            for inputStrapper in functionData['onboard_function']:
                if(functionData['onboard_function'][inputStrapper][0] == True):
                    globals()[inputStrapper] = input(f"{moduleFunction} requires input to continue: ")
                else:
                    globals()[inputStrapper] = input(f"{moduleFunction} requests \"{inputStrapper}\" to be entered: ")

            execResponse = exec(functionData['offboard_function'][0])
except Exception as e:
    print(f"[ WARN ] Exception noted while running: \"{moduleFunction}\"")
    print(f"[ DATA ] {e}")