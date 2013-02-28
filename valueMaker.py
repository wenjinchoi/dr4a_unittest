# -*- coding: UTF-8 -*-

import random, string

def randomPrintableStr(randomlength=8):
	a = list(string.printable)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randomLettersStr(randomlength=8):
	a = list(string.letters
					+ string.digits
					+ string.whitespace)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randStr():
	n = random.randint(1, 50)
	return randomPrintableStr(n)

def randStr2():
	n = random.randint(1, 50)
	return randomLettersStr(n)

def randUnicode():
	return unichr(random.randint(0x4E00, 0x9FA5)).encode('utf-8', 'ignore')

def randUTF8(randomlength = 10):
	strs = []
	for x in xrange(randomlength):
		strs.append(randUnicode())
	return ''.join(strs)

if __name__ == '__main__':
	# print random_str(50)
	print randUTF8(70)
