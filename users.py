#25         cols = ['ID', 'f', 'm', 'l', 'netid', 'email', 'fullname', 'nick',
# 26                 'init', 'phone', 'tags', 'orcid']


import names
import random

NUMS = list('1234567890')
CHARS = list('qwertyuiopasdfghjklzxcvbnm')
ALNUM = CHARS + NUMS

def gen(length, alph=None):
	if not alph:
		alph = CHARS
	c = []
	for i in range(length):
		c.append(random.choice(alph))
	return ''.join(c)

for i in range(10):
	name_components = [
		names.get_first_name(gender='female'),
		gen(1),
		names.get_last_name(),
	]
	cols = [
		str(i),
	] + name_components + [
		gen(5, alph=ALNUM).lower(),
		gen(5, alph=ALNUM).lower() + "@gmail.com",
		' '.join(name_components),
		'',
		name_components[0] + name_components[1],
		gen(10, alph=NUMS),
		'',
		''
	]


	print('\t'.join(cols))
