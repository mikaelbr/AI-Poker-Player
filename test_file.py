
def isset(vard, v):
	try:
	    vard[v]
	    return True
	except KeyError:
	    return False

a = {}

print(isset(a, "a"))