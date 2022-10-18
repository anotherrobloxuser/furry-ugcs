import json,requests,atexit
from time import sleep

url = 'https://catalog.roblox.com/v1/search/items/details?'
assets = []
file = open("accessory.json","w+")

category = 1
CreatorName = 'WhoToTrus'
limit = 30
subcategory = 1
time = 120
delay = 5

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
    if 'tail' in name:
        return True
    elif 'fin' in name:
        return True
    elif 'critter' in name:
        return True
    elif 'ear' in name:
        return True
    elif 'ears' in name:
        return True
    else:
        return False

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

while True:
    itemiterate(content,assets)
    content = json.loads(nextpage(content,CreatorName).content)
    sleep(delay)
    time -= 1
    print('processes left: '+str(time), end='\r')
    


#if 'tail' in str.lower(content['data'][i]['name']) or'fin' in str.lower(content['data'][i]['name']) or'critter' in str.lower(content['data'][i]['name']) or'ears' in str.lower(content['data'][i]['name']) or'ear' in str.lower(content['data'][i]['name']):
#        print(str.lower(content['data'][i]['name']))