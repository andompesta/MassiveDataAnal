
f = open('data/news/ok_Obama.json','r')

nt = f.read().replace('"_id": "4fd298818eb7c8105d875b24"','"_id": {"$oid": "4fd298818eb7c8105d875b24"}')

f.close()

f = open('data/news/ok_Obama.json','w')
f.write(nt)
f.close()
