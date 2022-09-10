#python3
import json
import os
import re
import urllib.request

def urlize(name):
    return name.lower().replace(' - ', ' ').replace("'",'').replace(' ', '-')

def toWiki(id):
   return 'https://torchlight-doc.xd.com/inventory/detail?id='+id+'&lang=en_WW'

def removeTags(s):
   return re.sub('<[^>]+>', '', s).replace('"', '')

def findMatches(s):
   matches = re.search('<e id=(\d+)>([^<]+)</e>',s)
   if matches:
      tooltips[matches.group(2)] = matches.group(1)
   return matches

TEMPLATE = open('template.html').read()

tooltips = {}

def convertJSON(json_file):
   for n in json_file:
      if not 'DetailAffix' in n.keys():
       return
      #wiki encoding error
      n['Name'] = n['Name'].replace('**','').capitalize()
      fname = urlize(n['Name'])
      print(fname)
      # collect tooltips
      [findMatches(effect['desc']) for effect in n['DetailAffix']]
      if 'BaseAffix' in n.keys():
         base = ['Base: '+removeTags(effect['desc']) for effect in n['BaseAffix']]
      else:
         base = [] 
      desc = '\n'.join( base+ [removeTags(effect['desc']) for effect in n['DetailAffix']])
      
      t = (TEMPLATE
         .replace('#TITLE#',n['Name']+' - lvl'+str(n['NeedLevel'])+' '+n['WeaponType'])
         .replace('#IMG#', n['Icon'])
         .replace('#URL#', toWiki(n['Id']))
         .replace('#DESC#', desc)
         )

      directory = 'out/'+n['WeaponType']   
      if not os.path.exists(directory):
          os.makedirs(directory)

      with open(directory+'/'+fname+'.html', 'w') as f:
         f.write(t)

# should only be 1-handed items, but actually returns the full list?
ITEMS_URL = "https://wiki.torchlight.xd.com/wiki_equip_list?Language=en_WW&ContentList=1_0_0"


with urllib.request.urlopen(ITEMS_URL) as url:
    ITEMS = json.load(url)

convertJSON(ITEMS)

extracted_tooltips = {}
for t in tooltips.keys():
   print(t)
   print(tooltips[t])
   extracted_tooltips[t.capitalize()] = {
      'id': tooltips[t],
      'desc': json.load(urllib.request.urlopen('https://wiki.torchlight.xd.com/wiki_equip_tips?Language=en_WW&Id='+tooltips[t]))
   }
print(extracted_tooltips)


with open('tooltips.json', 'w') as f:
   f.write(json.dumps(extracted_tooltips))
