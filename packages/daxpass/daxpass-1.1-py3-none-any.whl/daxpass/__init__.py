# daxpass
# (c) Annie 2025 under MIT license
# V1.0

from random import choice

daxmodulepass = []

def createpass(charset, len):
	for _ in range(len):
		daxmodulepass.append(choice(charset))
	return ''.join(daxmodulepass)
	daxmodulepass.clear()
