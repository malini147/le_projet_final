import time
def timer(func):
    #Un décorateur qui mésure le temps d'excécution d'une fonction
    def wrapper(*args,**kwargs):
        start_time=time.time()#Enregistre le temps de debut
        result=func(*args,**kwargs)#Appelle la fonction originale
        end_time=time.time()#Enregistre le temps de fin 
        print(f"La fonction {func.__name__} a pris {end_time-start_time:.4f} pour s'excécuter")
        return result
    return wrapper

@timer #Le décorateur est appliqué ici 
def ma_fn_lente():
    #Une fonction qui prend un peu de temps 
    print("Je suis une fn lente")
    time.sleep(2) #Simule une tâche qui prend du temps 
    print("...Et j'ai terminé!")

#Appel de la fonction décorée
ma_fn_lente()  

def require_admin(func):
    def wrapper(user,*args,**kwargs):
        if user!="admin":
            print("Accès réfusé")
            return None 
        return func(user,*args,*kwargs)
    return wrapper

@ require_admin
def supp_donnees(user):
    print(f"Donnees supprimer par {user}")

supp_donnees("Invité")
supp_donnees("admin")

def memoize(fun):
    cache={}
    def wrapper(*args):
        if args in cache :
            print("Resultat en cache")
            return cache[args]
        result=fun(*args)
        cache[args]=result
        return result
    return wrapper

@memoize
def fact(n):
    if n==0:
        return 1
    return n*fact(n-1)

print(fact(5))
print(fact(5))

import uuid
def attribuer_id(fun):
    def wrapper(*args,**kwargs):
        result=fun(*args,**kwargs)
        id=uuid.uuid4()
        print(id)
        return result
    return wrapper

@attribuer_id
def la_fn():
    print("Mon identifiant est: ")

for i in range(5):
    print(i+1)
    la_fn()

import csv

with open("names.csv","w",newline="") as file:
    fieldnames=["first_name","last_name"]
    writer=csv.DictWriter(file,fieldnames=["first_name","last_name"])

    writer.writeheader
    writer.writerow({"first_name":"nom","last_name":"prenom"})
    writer.writerow({"first_name":"Zahra","last_name":"Malini"})
    writer.writerow({"first_name":"Arwa","last_name":"Amine"})

with open("names.csv",'r',newline="") as fichier:
    lecteur=csv.DictReader(fichier)
    for ligne in lecteur:
        print(ligne)