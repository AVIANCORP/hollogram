import configparser, json, requests
from libs.alerts import *
def friendConsole(token):
    latch = True
    while latch == True:
        
        command = input(f"{Fore.LIGHTCYAN_EX }fc:> {Style.RESET_ALL}")
        match command:
            case "help":
                from libs.help import friendshipLibrary
                for generalInstructions in friendshipLibrary:
                    spacer = 15 - len(generalInstructions)
                    info(f"{generalInstructions}: {' '*spacer}  {friendshipLibrary[generalInstructions]['content']}")
            case "exit":
                latch = False
            case "clear":
                if(os.name == 'nt'):
                    os.system('cls')
                else:
                    os.system('clear')
            case "info":
                cache = configparser.ConfigParser()
                cache.read('cache.ini', encoding="utf8")
                print("Username:" + ' ' * 16 + '- ' + "ID\n"+'-'*35)
                for userID in json.loads(cache.get('relationships','registry')):
                    colorSet = callColor(cache.get('relationships',f"{userID}.color"))
                    title = cache.get('relationships',f"{userID}.name") + ' ' * (25 - len(cache.get('relationships',f"{userID}.name"))) + '- ' + userID
                    print(f"{colorSet}{title}{Style.RESET_ALL}")
            case _:

                if('check' in command):
                    returnData = requests.get(f"http://localhost:8000/token/{token}")
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                        if(len(json.loads(returnData.text)['DAT']) == 1):
                            info(f"There was 1 result found.")
                        else:
                            info(f"There were {len(json.loads(returnData.text)['DAT'])} results found.")
                    for TokenId in json.loads(returnData.text)['DAT']:
                        info(TokenId)

                if('request' in command and len(command.split(' ')) == 2):
                    returnData = requests.post(f"http://localhost:8000/token/update/id/{command.split(' ')[1]}",params={'user_id':token})
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                       info(f"Request sent: {json.loads(returnData.text)['TOK']}")
                    else:
                        fail('Request issue. Try again later.')

                if('accept' in command and len(command.split(' ')) == 2):
                    returnData = requests.put(f"http://localhost:8000/token/{token}/{command.split(' ')[1]}/accept")
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                       info('Accepted follow.')
                    else:
                       fail('Request issue. Try again later.')
                
                if('decline' in command and len(command.split(' ')) == 2):
                    returnData = requests.put(f"http://localhost:8000/token/{token}/{command.split(' ')[1]}/declined")
                    if(returnData.status_code == 200 and json.loads(returnData.text)['RES'] == 'OK'):
                       info('Denied follow.')
                    else:
                       fail('Request issue. Try again later.')
def timelineDisplay(token):
    returnData = requests.get(f"http://127.0.0.1:8000/timeline/{token.split('-')[4]}")
    for postID in json.loads(returnData.text)['DAT']:
        try:
            returnData = requests.get(f"http://127.0.0.1:8000/post/{postID}")
            if(json.loads(returnData.text)['DAT'] != '--redacted framework data--'):
                termWidth, termHeight = os.get_terminal_size()
                print('-'*termWidth)
                if(returnData.status_code == 200 and json.loads(returnData.text)['DAT'] != None):
                    returnJSON = json.loads(returnData.text)
                    try:
                        info(f"Post Content: {json.loads(returnJSON['DAT'])['content']}")
                    except:
                        info(f"Post Content: {returnJSON['DAT']}")
                    try:
                        if("'mime'" in json.loads(returnJSON['DAT'])['data']):
                            info(f"Post Data: {json.loads(json.loads(returnJSON['DAT'])['data'])['mime']}")
                        elif(json.loads(returnJSON['DAT'])['data'] == None):
                            info(f"No Data")
                        else:
                            info(f"Post Data: {json.loads(returnJSON['DAT'])['data']}")
                        
                    except:
                        i = 1
                else:
                    if(returnData.status_code == 200):
                        serverResponse = json.loads(returnData.text)['DAT']
                        match serverResponse:

                            case "ERR":
                                fail('There was a server side error.')
                            
                            case _:
                                fail(f"Nothing found")

        except Exception as e:
            fail(e)
        