import json
class Produit:
    def __init__(self, Id, nom, prix, quantite, seuil_alerte=10, categorie="Divers") :
        self.id=Id
        self.nom=nom
        self.prix=prix
        self.quantite=quantite
        self.seuil_alerte=seuil_alerte
        self.categorie=categorie
    def to_dict(self):
        dict = {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "quantite": self.quantite,
            "seuil_alerte": self.seuil_alerte,
            "categorie": self.categorie
        }
        return dict
class GestionnaireInventaire:
    def __init__(self, fichierss="inventaire.json"):
        self.fichierss = fichierss
        self.produits = []
        self.charger_load()

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
                    Produit.categorie=prod["categorie"]
                    self.produits.append(Produit(Produit.id, Produit.nom, Produit.prix, Produit.quantite, Produit.seuil_alerte, Produit.categorie))
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
        
    def ajouter_produit(self, nom, prix, quantite, seuil_alerte=10, categorie="Divers"):
        # self.donnees=self.charger_load()
        # self.Id = len(self.donnees)+1
        # self.Nom=input("Nom du produit à ajouter: ")
        # self.Categorie=input("Catégorie: ")
        # self.Prix=float(input("Prix: "))
        # self.Quantite=int(input("Quantité: "))
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
                    self.produits.append(Produit(Id, nom, prix, quantite, seuil_alerte, categorie))
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
                    if p.nom== nom:
                        x=1
                        if nouveau_prix is not None:
                            p.prix=nouveau_prix
                        if nouvelle_quantite is not None:
                            p.quantite=nouvelle_quantite
                        if nouveau_seuil is not None:
                            p.seuil_alerte=nouveau_seuil
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
                self.produits.pop(i-1)
                i=0
        self.sauvegarde() 

    def rechercher_produit(self, nom):
        liste=[]
        x=None
        for p in self.produits:
            if p.nom.lower()==nom.lower():
                print("Produit trouvé: ")
                print(p.to_dict())
                x=0
            elif p.nom.lower()!=nom.lower():
                liste.append(p.nom)
        if x is None:
            if nom.lower() not in liste:
                print(f"Produit {nom} introuvable.")

    def modifier_Quantite(self, nom, nouvelle_quantite):
        try:
            nouvelle_quantite=int(nouvelle_quantite)
            if nouvelle_quantite<0:
                print("Entrez une valeur positive")
            else:
                p=self.rechercher_produit(nom)
                if p is not None:
                    p.quantite=nouvelle_quantite
                    self.sauvegarder()
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
                print(f"\n {p.nom} | {p.categorie} | {p.quantite} unités | {p.prix} francs cfa | seuil={p.seuil_alerte}")

    def rechercher_par_categorie(self, categorie):
        resultats=[]
        for p in self.produits:
            if p.categorie.lower()==categorie.lower():
                resultats.append(p.to_dict())
        return resultats
    
    def rapport_valeur(self):
        print(f"\n valeur totale du stock : {self.valeur_totale_stock} francs cfa")
        

inventaire=GestionnaireInventaire()
while True:
    print("\n=== SYSTEME DE GESTION D'INVENTAIRE ===")
    print("1.Ajouter un produit")
    print("2.Modifier un produit")
    print("3.Supprimer un produit")
    print("4.Rechercher un produit")
    print("5.Rechercher des produits par categorie")
    print("6.Modifier la quantite d'un produit")
    print("7.Vérifier les alertes ")
    print("8.Afficher l'inventaire complet")
    print("9.Générer un rapport de valeur du stock")
    print("10.Quitter")
    print("=============================================")
    choix=input("Veuillez choisir une option(1-10): ")
    if choix=="1":
        print("\n---Ajouter un produit---")
        nom=input("Nom du produit à ajouter: ")
        prix=input("Prix du produit: ")
        quantite=input("Quantité du produit: ")
        seuil_alerte=input("Seuil d'alerte(défaut:10): ")
        categorie=input("Entrer la catégorie du produit: ")
        inventaire.ajouter_produit(nom, prix, quantite, seuil_alerte, categorie)
    elif choix=="2":
        print("\n--Modifier un produit--")
        nom=input("Nom du produit à modifier: ")
        nouveau_nom=input("Nouveau nom (laisser vide pour ne pas changer): ")
        nouveau_prix=input("nouveau prix (laisser vide pour ne pas changer): ")
        nouvelle_quantite=input("Nouvelle quantité (laisser vide pour ne pas changer): ")
        nouveau_seuil=input("Nouveau seuil d'alerte(laisser vide pour ne pas changer): ")
        inventaire.modifier_produit(nom, nouveau_prix, nouvelle_quantite, nouveau_seuil)
    elif choix=="3":
        print("\n--Supprimer un produit---")
        nom=input("Nom du produit à supprimer: ")
        inventaire.supprimer_produit(nom)
    elif choix=="4":
        print("\n--Rechercher un produit--")
        nom=input("Nom du produit à rechercher: ")
        inventaire.rechercher_produit(nom)
    elif choix=="5":
        print("\n---Recherche par catégorie---")
        categorie=input("La catégorie des produits que vous souhaitez afficher: ")
        liste_categorie=inventaire.rechercher_par_categorie(categorie)
        print(f"Produits de categorie '{categorie}' : {liste_categorie}")
    elif choix=="6":
        print("\n---Modifier la quantite d'un produit---")
        nom=input("Nom du produit: ")
        nouvelle_quantite=input("Nouvelle quantité: ")
        inventaire.modifier_Quantite(nom,categorie)
    elif choix=="7":
        print("\n---vérifier les alertes de stock ---")
        inventaire.alerte_stock()
    elif choix=="8":
        print("\n---Affichage complet de l'inventaire---")
        inventaire.afficher_inventaire()
    elif choix=="9":
        print("\n---Génération d'un rapport de valeur de stock---")
    elif choix=="10":
        print("Merci!")
        break
    else:
        print("Choix invalide, veuillez choisir entre 1 et 9")












# inventaire.ajouter_produit(1, "pomme", 200, 20, seuil_alerte=10, categorie="Fruits")
# inventaire.ajouter_produit(1, "ananas", 500, 12, seuil_alerte=10, categorie="Fruits")
# inventaire.ajouter_produit(1, "robe", 2500, 10, seuil_alerte=10, categorie="Vetements")
# # inventaire.modifier_produit("pomme", nouvelle_quantite=30)
# inventaire.modifier_produit("pomme", nouveau_prix=400, nouvelle_quantite=40, nouveau_seuil=20)
# inventaire.supprimer_produit("ananas")
# inventaire.supprimer_produit("pomme")
