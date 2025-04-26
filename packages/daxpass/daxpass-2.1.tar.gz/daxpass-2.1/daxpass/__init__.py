from random import choice

daxmodule = []
daxmodule2 = []

def createpass(charset, len):
	for _ in range(len):
		daxmodule.append(choice(charset))
	return ''.join(daxmodule)
	daxmodule.clear()

def en(str, charset):
	for char in str:
		for _ in range(charset.index(char) + 1):
			daxmodule2.append('-')
		daxmodule.append(''.join(daxmodule2))
		daxmodule2.clear()
	return ' '.join(daxmodule)
	daxmodule.clear()

def de(str, charset):
	daxmodule3 = str.split(' ')
	for encline in daxmodule3:
		daxmodule.append(charset[len(encline) - 1])
	daxmodule3.clear()
	return ''.join(daxmodule)
	daxmodule.clear()
