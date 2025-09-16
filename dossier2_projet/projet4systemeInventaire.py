import json
import datetime
import uuid

class Categorie:
    def __init__(self, nom, description=""):
        self.id= str(uuid.uuid4())
        self.nom=nom
        self.description=description
    
    def to_dict(self):
        dict={
            "id": self.id,
            "nom": self.nom,
            "description": self.description
        }
        return dict 
    
class Fournisseur:
    def __init__(self, name, contact_person="", email="", phone="", address=""):
        self.id=str(uuid.uuid4())
        self.name=name
        self.contact_person=contact_person
        self.email=email
        self.phone=phone
        self.address=address
        self.created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        dict={
            "id": self.id,
            "name": self.name,
            "contact_fournisseur": self.contact_person,
            "email": self.email,
            "téléphone": self.phone,
            "address": self.address,
            "created_at": self.created_at
        }
        return dict

class Produit:
    def __init__(self, Id, nom, prix, quantite, seuil_alerte, categorie_id, supplier_id) :
        self.id=Id
        self.nom=nom
        self.prix=prix
        self.quantite=quantite
        self.seuil_alerte=seuil_alerte
        self.categorie_id=categorie_id
        self.supplier_id=supplier_id
    def to_dict(self):
        dict = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "quantite": self.quantite,
            "seuil_alerte": self.seuil_alerte,
            "categorie_id": self.categorie_id,
            "Supplier_id": self.supplier_id
        }
        return dict
    
class GestionnaireInventaire:
    def __init__(self, fichierss="inventaire.json"):
        self.fichierss = fichierss
        self.produits = []
        self.charger_load()
        self.categories=[]
        self.fournisseurs=[]

    def charger_load(self):
        try:
            with open(self.fichierss,"r") as fichier:
                donnees=json.load(fichier)
                for prod in donnees:
                    Produit.id=prod["id"]
                    Produit.nom=prod["nom"]
                    Produit.prix=prod["prix"]
                    Produit.quantite=prod["quantite"]
                    Produit.seuil_alerte=prod["seuil_alerte"]
                    Produit.categorie_id=prod["categorie_id"]
                    Produit.supplier_id=prod["Supplier_id"]
                    self.produits.append(Produit(Produit.id, Produit.nom, Produit.prix, Produit.quantite, Produit.seuil_alerte, Produit.categorie_id, Produit.supplier_id))
                #return 
        except FileNotFoundError :
            print("Le fichier n'existe pas")
            #return []
            self.produits=[]
        except json.JSONDecodeError:
            print("Fichier JSON invalide")
            #return []
            self.produits=[]
    
    def sauvegarde(self):
        with open(self.fichierss, "w") as fichier:
            # liste_dict=[]
            # for p in self.produits:
            #     liste_dict.append(p.to_dict)
            # json.dump(liste_dict, fichier, indent=4)
            json.dump([p.to_dict() for p in self.produits], fichier,indent=4)

    def charger_categories(self, fichier_cat="categories.json"):
        try:
            with open(fichier_cat,"r") as fichier:
                donnees=json.load(fichier)
                for c in donnees:
                    Categorie.id=c["id"]
                    Categorie.nom=c["nom"]
                    Categorie.description=["description"]
                    self.categories.append(Categorie(Categorie.nom, Categorie.description))
        except FileNotFoundError :
            print("Le fichier n'existe pas")
            #return []
            self.categoriess=[]
        except json.JSONDecodeError:
            print("Fichier JSON invalide")
            #return []
            self.categories=[]

    def sauvegarder_categories(self, fichier_cat="categories.json"):
        with open(fichier_cat, "w") as f:
            json.dump([c.to_dict() for c in self.categories], f, indent=4)

    def charger_fournisseur(self, fichier_fou="fournisseurs.json"):
        try:
            with open(fichier_fou, "r") as f:
                donnees=json.load(f)
                for fou in donnees:
                    Fournisseur.id=fou["id"]
                    Fournisseur.name=fou["name"]
                    Fournisseur.contact_person=fou["contact_person"]
                    Fournisseur.email=fou["email"]
                    Fournisseur.phone=fou["téléphone"]
                    Fournisseur.address=fou["address"]
                    Fournisseur.created_at=fou["created_at"]
                    self.fournisseurs.append(Fournisseur(Fournisseur.name, Fournisseur.contact_person, Fournisseur.email, Fournisseur.phone, Fournisseur.address))
        except FileNotFoundError :
            print("Le fichier n'existe pas")
            self.categoriess=[]
        except json.JSONDecodeError:
            print("Fichier JSON invalide")
            self.categories=[]

    def sauvegarder_fournisseur(self, fichier_fou="fournisseurs.json"):
        with open(fichier_fou) as f:
            json.dump([fou.to_dict()  for fou in self.fournisseurs], f, indent=4)
        

        
    def ajouter_categorie(self, nom, description):
        cat=Categorie(nom.lower(), description)
        self.categories.append(cat)
        self.sauvegarder_categories()
        print(f"Catégorie '{nom}' ajoutée avec succès.")
        return cat.id

    def afficher_categories(self):
        if not self.categories:
            print("Aucune catégorie enregistrée.")
        else:
            print("\n=== Liste des catégories ===")
            for c in self.categories:
                print(f"[{c.id}]  {c.nom}")

    def trouver_categorie(self, nom):
        for c in self.categories:
            if c.nom.lower()==nom.lower():
                return c.id
            else:
                return False
    
    def supprimer_categorie(self, categorie_nom):
        for i,c in enumerate (self.categories):
            if c.nom.lower()==categorie_nom.lower():
                confirmation = input(f"Etes vous sur de vouloir supprimer la categorie {c.nom} ? (oui/non) : ").lower()
                if confirmation=="oui":
                    del self.categories[i]
                    print(f"Produit {c.nom} supprimé")
                    self.sauvegarder_categories()
                else:
                    print("Supression annulé.")
            else:
                print("Catégorie inexistante")

    def ajouter_fournisseur(self, name, contact="", email="", phone="", address=""):
        fou=Fournisseur(name, contact, email, phone, address)
        self.fournisseurs.append(fou)
        self.sauvegarder_categories()
        print(f"Fournisseur '{name}' enregistré avec succès")
        return fou.id
    
    def afficher_fournisseur(self):
        if not self.fournisseurs:
            print("Aucun fourniseur enregistré.")
        else:
            print("===LISTE DES FOURNISSEURS===")
            for fou in self.fournisseurs:
                print(f"[{fou.id}]  {fou.name} enregistré le {fou.created_at} ")

    def trouver_fournisseur(self, name):
        for fou in self.fournisseurs:
            if fou.name.lower()==name.lower():
                return fou.id
            else:
                return False
            
    def supprimer_fournisseur(self, fournisseur_name):
        for i,fou in enumerate (self.fournisseurs):
            if fou.name.lower()==fournisseur_name.lower():
                confirmation = input(f"Etes vous sur de vouloir supprimer le fournisseur {fou.name} ? (oui/non) : ").lower()
                if confirmation=="oui":
                    del self.categories[i]
                    print(f"Produit {fou.name} supprimé")
                    self.sauvegarder_fournisseur()
                else:
                    print("Supression annulé.")
            else:
                print("Fournisseur inexistant")

    def ajouter_produit(self, nom, prix, quantite, seuil_alerte, categorie_id, supplier_id):
        # self.donnees=self.charger_load()
        # self.Id = len(self.donnees)+1
        # self.Nom=input("Nom du produit à ajouter: ")
        # self.Categorie=input("Catégorie: ")
        # self.Prix=float(input("Prix: "))
        # self.Quantite=int(input("Quantité: "))
        x=1
        for p in self.produits:
            if p.nom==nom:
                print(f"Le produit '{nom}' existe déja.")
                x=0
        if x!=0:
            try:
                Id=len(self.produits)+1
                prix=float(prix)
                quantite=int(quantite)
                seuil_alerte=int(seuil_alerte)
                if prix<0 or quantite<0 or seuil_alerte<0:
                    print("les valeurs ne peuvent pas etre négatives.")
                else:
                    self.produits.append(Produit(Id, nom, prix, quantite, seuil_alerte, categorie_id, supplier_id))
                    self.sauvegarde()
                    print(f"Produit '{nom}' ajouté avec succès.")
            except ValueError:
                print("Erreur:le prix doit etre un nombre, la quantité et le seuil d'alerte des entiers")


    def modifier_produit(self, nom, nouveau_prix=None, nouvelle_quantite=None, nouveau_seuil=None):
        try:
            nouveau_prix=float(nouveau_prix)
            nouvelle_quantite=int(nouvelle_quantite)
            nouveau_seuil=int(nouveau_seuil)
            if nouveau_prix<0 or nouvelle_quantite<0 or nouveau_seuil<0:
                print("les valeurs ne peuvent pas etre négatives.")
            else:
                for p in self.produits:
                    if p.nom.lower()== nom.lower():
                        x=1
                        if nouveau_prix:
                            p.prix=nouveau_prix
                            #self.sauvegarde()
                        if nouvelle_quantite:
                            p.quantite=nouvelle_quantite
                            #self.sauvegarde()
                        if nouveau_seuil:
                            p.seuil_alerte=nouveau_seuil
                            #self.sauvegarde()
                self.sauvegarde()
                if x==1:
                    print(f"Produit '{nom}' modifié avec succès.")
                else:
                    print(f"Produit '{nom}' non trouvé")
        except ValueError:
            print("Erreur:le prix doit etre un nombre, la quantité et le seuil d'alerte des entiers")

    def supprimer_produit(self,nom):

        i=0
        for p in self.produits:
            i=i+1
            # if p.nom==nom:
            #     self.produits.pop(i-1)
            if self.produits[i-1].nom==nom:
                confirmation = input(f"Etes vous sur de vouloir supprimer le fournisseur {fou.name} ? (oui/non) : ").lower()
                if confirmation=="oui":
                    self.produits.pop(i-1)
                    self.sauvegarde() 
                    print("Produit '{nom} supprimé avec succès.")
                else:
                    print("Supression annulé.")
        # if 

    def rechercher_produit(self, nom):
        liste=[]
        x=None
        for p in self.produits:
            if p.nom.lower()==nom.lower():
                print("Produit trouvé: ")
                print(p.to_dict())
                x=0
                return p
            elif p.nom.lower()!=nom.lower():
                liste.append(p.nom)
        if x is None:
            if nom.lower() not in liste:
                print(f"Produit {nom} introuvable.")
                return None

    def modifier_Quantite(self, nom, nouvelle_quantite):
        try:
            nouvelle_quantite=int(nouvelle_quantite)
            if nouvelle_quantite<0:
                print("Entrez une valeur positive")
            else:
                p=self.rechercher_produit(nom)
                if p is not None:
                    p.quantite=nouvelle_quantite
                    self.sauvegarde()
                    print(f"Quantité de '{nom}' mise à jour: {nouvelle_quantite}")
                else:
                    print("Produit introuvable.")
        except ValueError:
            print("la quantité doit etre une valeur entière")

    def alerte_stock(self):
        alertes=[]
        for p in self.produits:
            if p.quantite<=p.seuil_alerte:
                alertes.append(p)
        if alertes:
            print("\n Produits en stock bas : ")
            for p in alertes:
                print(f" - {p.nom} ({p.quantite} restants, seuil : {p.seuil_alerte})")
        else:
            print("\n Aucun produit en stock critique.")

    def valeur_totale_stock(self):
        stock_total=0
        for p in self.produits:
            stock_total=p.prix*p.quantite
        return stock_total
    
    def afficher_inventaire(self):
        if not self.produits:
            print("Inventaire vide.")
        else:
            print("\n Inventaire complet : ")
            for p in self.produits:
                print(f"\n {p.nom} | {p.categorie_id} | {p.quantite} unités | {p.prix} francs cfa | seuil={p.seuil_alerte}")

    def rechercher_par_categorie(self, cat_nom):
        resultats=[]
        cat_id=self.trouver_categorie(cat_nom)
        for p in self.produits:
            if p.categorie_id.lower()==cat_id.lower():
                resultats.append(p.to_dict())
        if resultats:
            return resultats
        # else:
        #     return False
    
    def rapport_valeur(self):
        print(f"\n valeur totale du stock : {self.valeur_totale_stock()} francs cfa")
        

inventaire=GestionnaireInventaire()
inventaire.charger_categories()
inventaire.charger_fournisseur()
while True:
    print("\n=== SYSTEME DE GESTION D'INVENTAIRE ===")
    print("1. Gestion des produits")
    print("2. Gestion des catégories")
    print("3. Gestion des fournisseurs et stock")
    print("4. Quitter")
    # print("1.Ajouter un produit")
    # print("2.Modifier un produit")
    # print("3.Supprimer un produit")
    # print("4.Rechercher un produit")
    # print("5.Rechercher des produits par categorie")
    # print("6.Modifier la quantite d'un produit")
    # print("7.Vérifier les alertes ")
    # print("8.Afficher l'inventaire complet")
    # print("9.Générer un rapport de valeur du stock")
    # print("10.Ajouter categorie")
    # print("11.Afficher toutes les categories")
    # print("12.Rechercher une categorie")
    # print("13.Quitter")
    # print("=============================================")
    choix=input("Veuillez choisir une option(1-4): ")
    if choix=="1":
        while True:
            print("--- GESTION DES PRODUITS ---")
            print("1.Ajouter un produit")
            print("2.Modifier un produit")
            print("3.Supprimer un produit")
            print("4.Rechercher un produit")
            print("5.Afficher l'inventaire complet")
            print("6.Retour")
            sous_choix=input("Choisissez une option: ")
            if sous_choix=="1":
                print("\n---Ajouter un produit---")
                nom=input("Nom du produit à ajouter: ")
                prix=input("Prix du produit: ")
                quantite=input("Quantité du produit: ")
                seuil_alerte=input("Seuil d'alerte(défaut:10): ")
                print("\n Choisir une catégorie existante ou taper 'nouvelle': ") 
                inventaire.afficher_categories()
                choix_cat=input("Nom de la categorie: ")
                if choix_cat.lower()=="nouvelle":
                    nom_cat=input("Nom de la nouvelle catégorie: ")
                    desc_cat=input("Description: ")
                    categorie_id=inventaire.ajouter_categorie(nom_cat.lower(), desc_cat)
                    #inventaire.ajouter_produit(nom, prix, quantite, seuil_alerte, categorie)
                else:
                    categorie_id=inventaire.trouver_categorie(choix_cat.lower())
                    if not categorie_id:
                        print("Categorie introuvable")
                print("Choisir un fournisseur existant ou taper 'nouveau': ")
                choix_fou=input("Nom du fournisseur: ")
                if choix_fou.lower()=="nouveau":
                    name=input("Nom du nouveau fournisseur: ")
                    contact=input("Contact du fournisseur: ")
                    email=input("Email du fournisseur: ")
                    phone=input("Numéro téléphonne du fournisseur: ")
                    address=input("L'addresse du fournisseur")
                    supplier_id=inventaire.ajouter_fournisseur(name, contact, email, phone, address)
                else:
                    supplier_id=inventaire.trouver_fournisseur(choix_fou.lower())
                    if not supplier_id:
                        print("Fournisseur introuvable")
                inventaire.ajouter_produit(nom, prix, quantite, seuil_alerte, categorie_id, supplier_id)
            elif sous_choix=="2":
                print("\n--Modifier un produit--")
                nom=input("Nom du produit à modifier: ")
                nouveau_nom=input("Nouveau nom (laisser vide pour ne pas changer): ")
                nouveau_prix=input("nouveau prix (laisser vide pour ne pas changer): ")
                nouvelle_quantite=input("Nouvelle quantité (laisser vide pour ne pas changer): ")
                nouveau_seuil=input("Nouveau seuil d'alerte(laisser vi de pour ne pas changer): ")
                inventaire.modifier_produit(nom, nouveau_prix, nouvelle_quantite, nouveau_seuil)
            elif sous_choix=="3":
                print("\n--Supprimer un produit---")
                nom=input("Nom du produit à supprimer: ")
                inventaire.supprimer_produit(nom)
            elif sous_choix=="4":
                print("\n--Rechercher un produit--")
                nom=input("Nom du produit à rechercher: ")
                inventaire.rechercher_produit(nom)
            elif sous_choix=="5":
                print("\n---Affichage complet de l'inventaire---")
                inventaire.afficher_inventaire()
            elif sous_choix=="6":
                
                break
    elif choix=="2":
        while True:
            print("\n--- GESTION DES CATEGORIES ---")
            print("1.Ajouter categorie")
            print("2.Afficher toutes les categories")
            print("3.Supprimer une categorie")
            print("4.Afficher produits par categorie")
            print("5. Retour")
            sous_choix=input("Choisissez une option: ")
            if sous_choix=="1":
                print("\n---Ajouter une categorie---")
                nom=input("Nom de la categorie: ")
                description=input("Description: ")
                inventaire.ajouter_categorie(nom.lower(), description)
            elif sous_choix=="2":
                print("\n---Afficher toutes les categories---")
                inventaire.afficher_categories()
            elif sous_choix=="3":
                print("\n---Supprimer une catégorie---")
                nom_cat=input("Nom de la categorie à supprimer: ")
                inventaire.supprimer_categorie(nom_cat)
            elif sous_choix=="4":
                print("---Afficher produit par categorie---")
                categorie_nom=input("Nom de la catégorie: ")
                resultat=inventaire.rechercher_par_categorie(categorie_nom)
                # if resultat:
                print(f"Liste des produits de la categorie {categorie_nom}: {resultat}")
                # elif not resultat:
                #     print("Catégorie introuvable")
            elif sous_choix=="5":
                print("\n Retour au menu principal")
                break
    elif choix=="3":
        while True:
            print("\n--- GESTION DES FOURNISSEURS ---")
            print("1.Ajouter un fournisseur")
            print("2.Afficher tous les fournisseurs")
            print("3.Supprimer un fournisseur")
            print("4. Retour")
            sous_choix=input("Choisissez une option: ")
            if sous_choix=="1":
                print("\n---Ajouter un fournisseur---")
                name=input("Nom du fournisseur: ")
                contact=input("Contact du fournisseur: ")
                email=input("Email du fournisseur: ")
                phone=input("Numéro téléphonne du fournisseur: ")
                address=input("L'addresse du fournisseur")
                inventaire.ajouter_fournisseur(name, contact, email, phone, address)
            elif sous_choix=="2":
                print("\n---Afficher tous les fournisseurs---")
                inventaire.afficher_fournisseur()
            elif sous_choix=="3":
                print("\n---Supprimer fournisseur---")
                name=input("Nom du fournisseur à supprimer: ")
                inventaire.supprimer_categorie(name) 
            elif sous_choix=="4":
                print("Retour.")
                break       
    elif choix=="4":
        print("Merci!")
        break

    # if choix=="10":
    #     print("\n---Ajouter une categorie---")
    #     nom=input("Nom de la categorie: ")
    #     description=input("Description: ")
    #     inventaire.ajouter_categorie(nom.lower(), description)
    # elif choix=="1":
    #     print("\n---Ajouter un produit---")
    #     nom=input("Nom du produit à ajouter: ")
    #     prix=input("Prix du produit: ")
    #     quantite=input("Quantité du produit: ")
    #     seuil_alerte=input("Seuil d'alerte(défaut:10): ")
    #     print("\n Choisir une catégorie existante ou taper 'nouvelle': ") 
    #     inventaire.afficher_categories()
    #     choix_cat=input("Nom de la categorie: ")
    #     if choix_cat.lower()=="nouvelle":
    #         nom_cat=input("Nom de la nouvelle catégorie: ")
    #         desc_cat=input("Description: ")
    #         categorie_id=inventaire.ajouter_categorie(nom_cat.lower(), desc_cat)
    #         #inventaire.ajouter_produit(nom, prix, quantite, seuil_alerte, categorie)
    #     else:
    #         categorie_id=inventaire.trouver_categorie(choix_cat.lower())
    #         if not categorie_id:
    #             print("Categorie introuvable")
    #     inventaire.ajouter_produit(nom, prix, quantite, seuil_alerte, categorie_id)
        
            
   # elif choix=="2":
    #     print("\n--Modifier un produit--")
    #     nom=input("Nom du produit à modifier: ")
    #     nouveau_nom=input("Nouveau nom (laisser vide pour ne pas changer): ")
    #     nouveau_prix=input("nouveau prix (laisser vide pour ne pas changer): ")
    #     nouvelle_quantite=input("Nouvelle quantité (laisser vide pour ne pas changer): ")
    #     nouveau_seuil=input("Nouveau seuil d'alerte(laisser vi de pour ne pas changer): ")
    #     inventaire.modifier_produit(nom, nouveau_prix, nouvelle_quantite, nouveau_seuil)
    # elif choix=="3":
    #     print("\n--Supprimer un produit---")
    #     nom=input("Nom du produit à supprimer: ")
    #     inventaire.supprimer_produit(nom)
    # elif choix=="4":
    #     print("\n--Rechercher un produit--")
    #     nom=input("Nom du produit à rechercher: ")
    #     inventaire.rechercher_produit(nom)
    # elif choix=="5":
    #     print("\n---Recherche par catégorie---")
    #     categorie=input("La catégorie des produits que vous souhaitez afficher: ")
    #     liste_categorie=inventaire.rechercher_par_categorie(categorie)
    #     print(f"Produits de categorie '{categorie}' : {liste_categorie}")
    # elif choix=="6":
    #     print("\n---Modifier la quantite d'un produit---")
    #     nom=input("Nom du produit: ")
    #     nouvelle_quantite=input("Nouvelle quantité: ")
    #     inventaire.modifier_Quantite(nom,nouvelle_quantite)
    # elif choix=="7":
    #     print("\n---vérifier les alertes de stock ---")
    #     inventaire.alerte_stock()
    # elif choix=="8":
    #     print("\n---Affichage complet de l'inventaire---")
    #     inventaire.afficher_inventaire()
    # elif choix=="9":
    #     print("\n---Génération d'un rapport de valeur de stock---")
    #     inventaire.rapport_valeur()
    # elif choix=="13":
    #     print("Merci!")
    #     break
    # else:
    #     print("Choix invalide, veuillez choisir entre 1 et 9")












# inventaire.ajouter_produit(1, "pomme", 200, 20, seuil_alerte=10, categorie="Fruits")
# inventaire.ajouter_produit(1, "ananas", 500, 12, seuil_alerte=10, categorie="Fruits")
# inventaire.ajouter_produit(1, "robe", 2500, 10, seuil_alerte=10, categorie="Vetements")
# # inventaire.modifier_produit("pomme", nouvelle_quantite=30)
# inventaire.modifier_produit("pomme", nouveau_prix=400, nouvelle_quantite=40, nouveau_seuil=20)
# inventaire.supprimer_produit("ananas")
# inventaire.supprimer_produit("pomme")
