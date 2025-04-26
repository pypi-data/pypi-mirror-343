# Dax
# Developed by AnniePrograms
# Alpha

from random import choice

daxmodulepass = []

def createpass(charset, len):
	for _ in range(len):
		daxmodulepass.append(choice(charset))
	return ''.join(daxmodulepass)
	daxmodulepass.clear()
