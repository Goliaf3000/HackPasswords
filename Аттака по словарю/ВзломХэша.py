import hashlib
import pickle
import math

#symb = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
symb = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
string = "75bc0cad575f5484dce6eced07dcedf9"
def func_reduce(hassh):
	password = ""
	for j in str(hassh):
		while len(password)<6:
			password += symb[(hassh**int(j))%len(symb)]
			hassh //= int(j)*len(symb)
	return password

rainbow_table = {}
for h in range(1,2000,50):
	start = func_reduce(int(hashlib.md5(str(h).encode('ascii')).hexdigest(),16))
	pwd = start

	for i in range(0,1000):
		new_hash=hashlib.md5(str(pwd).encode('ascii')).hexdigest()
		pwd=func_reduce(int(new_hash,16))
		rainbow_table[start] = pwd.encode('ascii')
		print(rainbow_table)
	with open("password.txt", "wb") as file:
		pickle.dump(rainbow_table, file)

def func_password_crack(h):	
	hassh=h
	with open("password.txt", "rb") as file:
		a = pickle.load(file)
	h = func_reduce(int(h, 16))
	while h.encode('ascii') not in a.values() and len(h) != 0:
		h = hashlib.md5(h.encode("ascii")).hexdigest()
		h = func_reduce(int(h, 16))
	for k, v in a.items():
		proverka = b""
		if v.decode("utf-8") == h and v != proverka:
				proverka = v
				key = k				
				print(func_generate_pass(key, hassh, proverka, k))
				exit()	

def func_generate_pass(key, hassh, proverka, k):
	new_hash=''
	delet = k
	while new_hash!=hassh:
		new_hash = hashlib.md5(key.encode('ascii')).hexdigest()
		if new_hash == hassh:				
			break
		elif key == proverka.decode("utf-8") and new_hash != hassh:
			with open("password.txt", "rb") as file:
				a = pickle.load(file)
				if delet in a:
					del a[delet]
					print("удалить", delet)
				with open("password.txt", "wb") as file:
					pass
				with open("password.txt", "wb") as file:
					pickle.dump(a, file)
				func_password_crack(hassh)
		else:
			key = func_reduce(int(new_hash, 16))
	return key
func_password_crack(string)

