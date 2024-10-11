import hashlib
import pickle
import math
import sys

sys.setrecursionlimit(100000)

def func_reduce(hassh):
	password = ""
	for j in str(hassh):
		while len(password)<5:
			password += symb[(hassh**int(j))%len(symb)]
			hassh //= int(j)*len(symb)
	return password

def func_table():
	rainbow_table = {}
	for h in range(10000,1000000,1000):
		start = func_reduce(int(hashlib.md5(str(h).encode('ascii')).hexdigest(),16))
		pwd = start
		for i in range(0,100):
			new_hash=hashlib.md5(str(pwd).encode('ascii')).hexdigest()
			pwd=func_reduce(int(new_hash,16))
			rainbow_table[start] = pwd.encode('ascii')
	with open("password.txt", "wb") as file:
		pickle.dump(rainbow_table, file)
	return rainbow_table


def func_password_crack(h,table):	
	hassh=h
	h = func_reduce(int(h, 16))
	while h.encode('ascii') not in table.values() and len(h) != 0:
		h = hashlib.md5(h.encode("ascii")).hexdigest()
		h = func_reduce(int(h, 16))
	for k, v in table.items():
		if v.decode("utf-8") == h:
			key = k				
			print(func_generate_pass(key, hassh, v, table))
			exit()

def func_generate_pass(key, hassh, v, table):
	new_hash=''
	delet = key
	while new_hash!=hassh:
		new_hash = hashlib.md5(key.encode('ascii')).hexdigest()
		if new_hash == hassh:				
			break
		elif key == v.decode("utf-8"):
				if delet in table:
					del table[delet]
					func_password_crack(hassh,table)
		else:
			key = func_reduce(int(new_hash, 16))
			
	return f"Ваш пароль {key}"
symb = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
string = input("Input hash - ")
answer = input("You want new rainbow_table? - ")
if answer == 'yes' or answer == 'Yes':
	table = func_table()
	print(func_password_crack(string,table))
else: 
	with open('password.txt','rb') as file:
		#file.seek(0)
		table = pickle.load(file)
		func_password_crack(string,table)

