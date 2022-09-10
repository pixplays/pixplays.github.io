import json

def urlize(name):
    return name.lower().replace(' - ', ' ').replace("'",'').replace(' ', '-')

TEMPLATE = open('template.html').read()

def extractFromJSON(name,desc):
   return (TEMPLATE
      .replace('#TITLE#', name)
      .replace('#IMG#', '')
      .replace('#URL#', 'https://torchlight-doc.xd.com')
      .replace('#DESC#', desc)
      )

with open('tooltips.json', 'r') as ref:
   tooltips = json.load(ref)
   for t in tooltips:
      with open('out/tooltips/'+urlize(t)+'.html', 'w') as f:
         desc = tooltips[t]['desc'].replace('\\n', '\n')
         f.write(extractFromJSON(t, desc))

