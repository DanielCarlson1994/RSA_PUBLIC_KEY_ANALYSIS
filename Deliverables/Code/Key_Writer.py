import csv
import base64
from Crypto.PublicKey import RSA
import operator
import numpy as np
import math
from fractions import gcd
import matplotlib.pyplot as plt

Key_Array = []
Decoded_Keys = []
e_values = 65537
n_values = []
i = 0
key = ""
temp_key = ""
SkipLine = False

with open("shodan_data.csv") as csvfile:
	reader = csv.reader(csvfile)
	firstline = True
	for row in reader:
		if firstline:
			firstline = False
			continue
		current_row = row[2]
		Key_Array.append(current_row)
		i += 1


f = open ('TheKeys.txt', 'r')
for line in f:
	if SkipLine == True:
		Decoded_Keys.append(key.replace(" ", ""))	
		key = ""
		SkipLine = False
	key += line
	if len(line) < 76:
		SkipLine = True


Decoded_Keys[6214] = Decoded_Keys[6213] #Errored keys, replaced with previous key so not to error, but not added
Decoded_Keys[6998] = Decoded_Keys[6997]
Decoded_Keys[6999] = Decoded_Keys[6997]
Decoded_Keys[11937] = Decoded_Keys[11936]
Decoded_Keys[12802] = Decoded_Keys[12801]
Decoded_Keys[12803] = Decoded_Keys[12801]
for j in range(0, 13426):
	temp_key = "ssh-rsa " + Decoded_Keys[j]
	final_key = RSA.importKey(temp_key)
	if(final_key.n in n_values):
		continue
	else:
		n_values.append(int(final_key.n))

X = open("Nvalues.txt", "w")
for i in n_values:
	X.write(str(i) + "\n")
	
#BATCH GCD
#Various Unique primes used

def prod(a):
	return reduce(operator.mul, a, 1)

def product(X):
	if len(X) == 0:
		return 1
	while len(X) > 1:
		X = [prod(X[i*2:(i+1)*2]) for i in range ((len(X)+1)/2)]
	return X[0]

def producttree(X):
	result = [X]
	while len(X) > 1:
		X = [prod(X[i*2:(i+1)*2]) for i in range ((len(X)+1)/2)]
		result.append(X)
	return result

def remaindertree(n,T):
	result = [n]
	for t in reversed(T):
		result = [result[int(math.floor(i/2))] % t[i] for i in range(0,len(t))]
	return result

def remainders(n,X):
	return remaindertree(n,producttree(X))

def batchgcd(X):
	R = remainders(product(X),[n**2 for n in X])
	return [gcd(r/n,n) for r,n in zip(R,X)]

#batchgcdresults = batchgcd(n_values)
#for i in batchgcdresults:
#	if(i != 1):
#		print i

#Fermat's Factorization

def isqrt(n):
	x = n
	y = (x + n // x) // 2
	while y < x:
		x = y
		y = (x + n // x) // 2
	return x

def FermatsFactorization(N):
	a = isqrt(N)
	b2 = ((a*a) - N)
	b = isqrt(N)
	while b*b != b2:
		a = a+ 1
		b2 = a*a - N
		b = isqrt(b2)
	p = a + b
	q = a - b
	print p
	print q
	return p,q

#Lehman's Factorization
#Can use, somehwat faster but will still take just as long to get results

def iQbrt(n):
	x = n
	y = (x + n // x) // 3
	while y < x:
		x = y
		y = (x + n // x) // 3
	return x

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True

def Lehman(N):
	n13 = iQbrt(N)
	n23 = iQbrt(N*N)
	k = 1
	while k <= n13:
		a = isqrt(4*k*N-1) + 1
		alimit = isqrt(4*k*N+n23)
		while a <= alimit:
			if is_square(a*a-4*k*N):
				return gcd((a+isqrt(a*a-4*k*N))/2,N)
			a += 1
		k += 1
