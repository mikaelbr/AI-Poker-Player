
dic = {}


dic['Marius Bar'] = "Hei"
dic['Marius'] = "Deg"
dic['Marius'] = "Foo"
dic['Marius'] = "Bar"
dic['Marius'] = "Bat"


for k,v in dic.items():
	print("%s: %s" % (k, v))