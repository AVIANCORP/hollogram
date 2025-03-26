def helpFile(command,contextData):
    callContext = ['-h','--help','/?','/help']
    for call in callContext:
        if(call in command):
            print('help called')