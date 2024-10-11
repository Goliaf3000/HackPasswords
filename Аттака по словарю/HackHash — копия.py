import hashlib
import pickle
import math


delet = 'abb'
with open("password.txt", "rb") as file:
	a = pickle.load(file)
	if delet in a:
		del a[delet]
		print("удалить", delet)
		with open("password.txt", "wb") as file:
			pass
		with open("password.txt", "wb") as file:
			pickle.dump(a, file)
			print("Slovar ",a)
	else: print("delet")