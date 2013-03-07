# -*- coding: UTF-8 -*-

import random, string

def randomPrintableStr(randomlength=8):
	a = list(string.printable)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randStr():
	n = random.randint(1, 50)
	return randomPrintableStr(n)


def randomLettersStr(randomlength=8):
	a = list(string.letters+string.digits+string.whitespace)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randStr2():
	n = random.randint(1, 36)
	return randomLettersStr(n)


def randomLettersDigitsBlank(randomlength = 8):
	a = list((string.letters+string.digits+5*" ")*5)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randStr3():
	n = random.randint(1, 50)
	return randomLettersDigitsBlank(n)

def randomDigits(randomlength = 8):
	a = list(string.digits*5)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randDig():
	n = random.randint(1, 30)
	return randomDigits(n)

def randUnicode():
	return unichr(random.randint(0x4E00, 0x9FA5)).encode('utf-8', 'ignore')

def randUTF8(randomlength = 10):
	strs = []
	for x in xrange(randomlength):
		strs.append(randUnicode())
	return ''.join(strs)

if __name__ == '__main__':
	# print random_str(50)
	print randStr3()
	a = ()
	a.append(1)
	print a
