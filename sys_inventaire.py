import csv 

with open("gestion_inventaire.csv","w",newline="") as file:
    fieldnames=["1","2","3","4","5","6","7","8","9","10","11","12"]
    writer=csv.DictWriter(file,fieldnames)

    writer.writeheader
    writer.writerow({"1":"ID","2":"name","3":"description","4":"category_id","5":"supplier_id","6":"price","7":"cost","8":"quantity","9":"min_quantity","10":"SKU","11":"created_at","12":"updated_at"})
    writer.writerow({"1":"4ee603","2":"Eau Cristal","3":"Eau minérale 1L","4":"Alimentation","5":"Cristal company","6":500,"7":300,"8":250,"9":50,"10":"44OS08","11":12-4-2025,"12":19-11-2025})
    writer.writerow({"1":"77ydh9","2":"Lait Milk","3":"Lait entier en poudre de 900g","4":"Alimentation","5":"Milk company","6":5000,"7":7000,"8":100,"9":25,"10":"00io8","11":4-9-2007,"12":19-5-2020})


class Product:
    def __init__(self,id,name,description,category_id,supplier_id,price,cost,quantity,min_quantity,SKU,created_at,updated_at):
        self.id=id
        self.name=name
        self.description=description
        self.category_id=category_id
        self.supplier_id=supplier_id
        self.price=price
        self.cost=cost
        self.quantity=quantity
        self.min_quantity=min_quantity
        self.SKU=SKU
        self.created_at=created_at
        self.updated_at=updated_at
# Ajouter un produit :formulaire console avec validation
    def ajouter_produit(self):
        with open("gestion_inventaire.csv",'a',newline="") as file:
            fieldnames=["1","2","3","4","5","6","7","8","9","10","11","12"]
            writer=csv.DictWriter(file,fieldnames)
            writer.writerow({"1":self.id,"2":self.name,"3":self.description,"4":self.category_id,"5":self.supplier_id,"6":self.price,"7":self.cost,"8":self.quantity,"9":self.min_quantity,"10":self.SKU,"11":self.created_at,"12":self.updated_at})
        print("Produit ajouté avec succes!")
#Affichage tabulaire avec pagination
    def lister_produits(self):
        with open("gestion_inventaire.csv","r",newline="") as file :
            contenu=csv.reader(file)
            for ligne in contenu:
                print(ligne)
#Recherche du produit par nom,SKU ou catégorie
    def search_product(self,**kwargs):
        with open("gestion_inventaire.csv","r",newline="") as file:
            lecteur=csv.DictReader(file)
            for ligne in lecteur: 
                for cle,valeur in ligne.items():
                    for c,v in kwargs.items():
                        if c==cle and valeur==v:
                            print(ligne)
                    
#Modifier les informations d'un produit
    def modifier_produit(self,nom_produit,**kwargs):
        with open ("gestion_inventaire.csv","rb","wb",newline="") as file:
            lecteur=csv.DictReader(file)
            for ligne in lecteur: 
                for cle,valeur in ligne.items():
                    if self.name==nom_produit:
                        for c,v in kwargs.items():
                            if c==cle:
                                valeur=v
            fieldnames=["1","2","3","4","5","6","7","8","9","10","11","12"]
            writer=csv.DictWriter(file,fieldnames)
            writer.writerows(lecteur)
            print(f"Les informations du  produit {nom_produit} ont été supprimé avec succès.")


#Suppression du produit avec confirmation 
    def supprimer_produit(self,nom_produit):
        with open ("gestion_inventaire.csv","wb","rb") as file :
            lecture=csv.DictReader(file)
            for ligne in lecture:
                if self.name==nom_produit:
                    del ligne
            fieldnames=["1","2","3","4","5","6","7","8","9","10","11","12"]
            writer=csv.DictWriter(file,fieldnames)

            writer.writeheader
            writer.writerow(lecture)
        print(f"Le produit {nom_produit} a été supprimé avec succès")
            
sucre=Product(id="234sry9",name="Flan alsa",description="Flan pâtissier aux oeufs",category_id="Alimentation",supplier_id="Alsa France",price=7000,cost=4000,quantity=300,min_quantity=50,SKU="L24281",created_at=12-3-2023,updated_at=11-9-2026 )
sucre.ajouter_produit()
sucre.lister_produits()
sucre.search_product(name="Lait Milk")
sucre.supprimer_produit(nom_produit="Eau Cristal")

class Category:
    def __init__(self,id,name,description,created_at):
        self.id=id
        self.name=name
        self.description=description
        self.created_at=created_at

    
    def create(self):
        with open("category.csv","w",newline="") as file:
            fieldnames=["1","2","3","4"]
            writer=csv.DictWriter(file)
            writer.writeheader
            writer.writerow({"ID","name","Description","created_at"})
            writer.writerow({"1":self.id,"2":self.name,"3":self.description,"4":self.created_at})

    def read(self):
        with open("category.csv","w",newline="") as file:
            lecteur=csv.reader(file)
            for ligne in lecteur:
                print(ligne)

    def delete(self,name_category):
        with open("category.csv","r",newline="") as file:
            lecteur=csv.DictReader(file)
            for ligne in lecteur:
                if ligne["name"]==name_category:
                    del ligne 
                    print(f"La suppression de la categorie {ligne["name"] }est faite avec succès.")
                else: 
                    print(f"Il n'existe pas une categorie du nom {ligne["name"]}.")
    def 