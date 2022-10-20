import json,requests,atexit,argparse,os
from time import sleep
from termcolor import colored as cl
args = argparse.ArgumentParser()
args.add_argument('-g','--isgroup',help="Specify if user is a group, 1:True 0:False",type=int,required=True)
args.add_argument('-cn','--creatorname',help="Creator's name",type=str,required=True)
args.add_argument('-q','--queue',help='Amount of processes that will be queued',type=int,default=10)
args.add_argument('-d','--delay',help='delay for each end of the process',type=int,default=5)
args = args.parse_args()

url = 'https://catalog.roblox.com/v1/search/items/details?'
assets = []

acceptable = ['tail','fin','critter','ear','ears','synth','wing','head','fluff']
unacceptable = ['pigtail','elf','earrings','beard','heart','elf','hood','ponytail','spear','coat','woman','faceless','shadow','glitch','phone','smug','anime','evil','headset','gas mask','gear']
exceptions = ['hallowogen']

isgroup = args.isgroup
CreatorName = args.creatorname
limit = 30
time = args.queue
delay = args.delay
num = 0

file = os.getcwd()+'\\'+CreatorName+".json"
print(file)
file = open(file,"w+")

@atexit.register 
def error(): 
    exit = Convert(assets)
    exit = json.dumps(exit)
    file.write(exit)
    file.close()
    print('completed                              ')


finalurl = url+'CreatorType'+str(isgroup)+'&CreatorName='+CreatorName.replace(' ','%20')+'&limit'+str(limit)
print(finalurl)
content = requests.get(finalurl).json()
content = content


def chkname(name=''):
    name = str.lower(name)
    isOK = False
    for i in range(len(acceptable)):
        if acceptable[i] in name:
            isOK = True
            break
    for i in range(len(unacceptable)):
        if unacceptable[i] in name:
            isOK = False
            print(unacceptable[i],cl(name,color="red", attrs=["bold"]),'                                                                                                               ')
            break
    for i in range(len(exceptions)):
        if exceptions[i] in name:
            print(exceptions[i],name)
            isOK = True
            break
    if isOK != False:
        print(cl(name,color="green", attrs=["bold"]),'                                                                                                               ')
    return isOK

def itemiterate(info,list,currentnum):
    try:
        for i in range(len(info['data'])):
            a = chkname(info['data'][i]['name'])
            if a == True:
                list.append(str(info['data'][i]['name']))
                list.append(str(info['data'][i]['id']))
                currentnum += 1
    except:
        print('error')
        return
    return currentnum

def nextpage(info,user):
    try:
        cursor = info['nextPageCursor']
        info = requests.get(url+'Cursor='+cursor+'&CreatorName='+user).json()
        return info
    except:
        return info

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

while time >= 0:
    num = itemiterate(content,assets,currentnum=num)
    if not content['nextPageCursor']:
        content['nextPageCursor'] = 'CURSOR MISSING'
    print('processes in queue: '+str(time),' || nextpage cursor: '+content['nextPageCursor'],' || assets collected: '+str(num), end='\r')
    content = nextpage(content,CreatorName)
    sleep(delay)
    time -= 1