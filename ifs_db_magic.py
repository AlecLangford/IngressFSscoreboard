

from peewee import *
import requests


db = SqliteDatabase(':memory:', threadlocals=True)




class player_begin(Model):

    PlayerName = CharField(unique=True)
    Faction = CharField(unique=False)
    StartLevel = IntegerField()
    StartAP = IntegerField()
    StartKms = IntegerField()
    StartHacks = IntegerField()

    class Meta:
        database = db

class player_end(Model):

    PlayerName = CharField(unique=True)
    EndLevel = IntegerField()
    EndAP = IntegerField()
    EndKms = IntegerField()
    EndHacks = IntegerField()

    class Meta:
        database = db
class player(Model):
    PlayerName = CharField(unique=True)
    Faction = CharField(unique=False)
    DiffLevel = IntegerField()
    DiffAP = IntegerField()
    DiffKms = IntegerField()
    DiffHacks = IntegerField()
    class Meta:
        database = db

db.create_tables([player_begin,player_end,player])


def get_key(x):
    x=x[39:].split("/")
    return x[0]

def add_csv2db(csv):
    csv = csv.split("\n")[1:]
    for item in csv:
        item= csv.split(",")[1:]
        player_begin(*item)






template_url = "https://docs.google.com/spreadsheets/d/%s/export?format=csv"

urls=["https://docs.google.com/spreadsheets/d/1b6hcUfZv4JO1qNxPMsWm0eiVuuaF0JIndlijvzCYDhM/pubhtml",
      "https://docs.google.com/spreadsheets/d/1n6m-QXZeZ15JczhNsc5c8hO-44DOOgB1cEU96BlvgMY/pubhtml",
]

def get_data(url):
    response = requests.get(url)
    return response.text.split("\n")[1:]


tables=[]

for item in urls:
    i=template_url%get_key(item)
    tables.append(get_data(i))

url1,url2=tables



golden=''

for item in url1:

    item=item.split(",")
    item[3]=int(item[3])
    item[4]=int(item[4])
    item[5]=int(item[5])
    item[6]=int(item[6])

    try:
        c=player_begin.create(PlayerName=item[1].lower(),Faction=item[2],StartLevel=item[3],StartAP=item[4],StartKms=item[5],StartHacks=item[6])
        golden+=item[1].lower()+"\n"
    except IntegrityError:
        pass
##############################################

import re, collections

def words(text): return re.findall('[a-z=+0-9]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model



NWORDS = train(words(golden))

alphabet = 'abcdefghijklmnopqrstuvwxyz0987654321-_'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)





#####################


#print url1



for item in url2:
    item=item.split(",")
    item[2]=int(item[2])
    item[3]=int(item[3])
    item[4]=int(item[4])
    item[5]=int(item[5])
    try:
        c=player_end.create(PlayerName=correct(item[1].lower()),EndLevel=item[2],EndAP=item[3],EndKms=item[4],EndHacks=item[5])
    except IntegrityError:
        pass

'''
fields={"joined":['PlayerName','Faction','StartAP','EndAP','StartLevel','EndLevel','StartHacks','EndHacks','StartKms','EndKms'],
        "final":["PlayerName","Faction", "DiffLevel" ,"DiffAP" ,"DiffKms","DiffHacks"] }
'''

for item in player_begin.raw('select * from player_begin LEFT JOIN player_end ON player_begin.PlayerName=player_end.PlayerName'):
    try:
        r=[item.PlayerName, item.Faction, item.EndLevel-item.StartLevel, item.EndAP-item.StartAP, item.EndKms-item.StartKms, item.EndHacks-item.StartHacks]
        q=player.create(PlayerName=r[0],Faction=r[1],DiffLevel=r[2],DiffAP=r[3],DiffKms=r[4],DiffHacks=r[5])
    except TypeError:
        pass
    #q.save()
    #print r

print "---"
f=player._meta.get_field_names()[1:]
#qry = player.select().where(player.Faction=="Enlightened").order_by(player.DiffLevel, player.DiffAP)

qry = player.select().order_by(player.DiffLevel, player.DiffAP)
results=open("scoreboard.csv","w")
for item in qry[::-1]:
    x=[str(getattr(item,i)) for i in f]
    results.write(",".join(x)+"\n")
results.close()
 

qry1 = player.select().where(player.Faction=="Enlightened")
print
r=open("enlightened","w")
r.write(str(sum([item.DiffAP for item in qry1])/qry1.count()))
r.close()
qry1 = player.select().where(player.Faction=="Resistance")
r=open("resistance","w")
try:
    r.write(str(sum([item.DiffAP for item in qry1])/qry1.count()))
except ZeroDivisionError:
    r.write(str(0))

r.close()

