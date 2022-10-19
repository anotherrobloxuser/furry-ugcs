import json,requests,atexit,argparse,os
from time import sleep

args = argparse.ArgumentParser()
args.add_argument('-cn','--creatorname',help="Creator's name",type=str,required=True)
args.add_argument('-q','--queue',help='Amount of processes that will be queued',type=int,default=10)
args.add_argument('-d','--delay',help='delay for each end of the process',type=int,default=5)
args = args.parse_args()

url = 'https://catalog.roblox.com/v1/search/items/details?'
assets = []

acceptable = ['tail','fin','critter','ear','ears']
unacceptable = ['pigtail','elf','earrings','beard','heart','elf','hood','ponytail']

CreatorName = args.creatorname
limit = 30
time = args.queue
delay = args.delay

file = os.getcwd()+'\\'+CreatorName+".json"
print(file)
file = open(file,"w+")

@atexit.register 
def error(): 
    exit = Convert(assets)
    exit = json.dumps(exit)
    file.write(exit)
    file.close()

finalurl = url+'CreatorName='+CreatorName+'&limit'+str(limit)
print(finalurl)
content = requests.get(finalurl)

content = json.loads(content.content)


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
            break
    return isOK

def itemiterate(info,list):
    for i in range(len(info['data'])):
        a = chkname(info['data'][i]['name'])
        if a == True:
            list.append(str(info['data'][i]['name']))
            list.append(str(info['data'][i]['id']))

def nextpage(info,user):
    cursor = info['nextPageCursor']
    try:
        info = requests.get(url+'Cursor='+cursor+'&CreatorName='+user)
    except:
        nextpage(info,user)
    if info.status_code == 200:
        return info
    else:
        nextpage(info,user)

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

while time >= 0:
    itemiterate(content,assets)
    content = json.loads(nextpage(content,CreatorName).content)
    sleep(delay)
    time -= 1
    print('processes in queue: '+str(time), end='\r')
    

