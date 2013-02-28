# -*- coding: UTF-8 -*-

import random, string

def randomPrintableStr(randomlength=8):
	random.seed()
	a = list(string.printable)
	random.shuffle(a)
	return ''.join(a[:randomlength])

def randomLettersStr(randomlength=8):
	random.seed()
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

if __name__ == '__main__':
	print random_str(50)
