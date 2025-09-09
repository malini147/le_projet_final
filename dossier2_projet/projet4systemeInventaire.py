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
        
    def ajouter_produit(self, Id, nom, prix, quantite, seuil_alerte=10, categorie="Divers"):
        # self.donnees=self.charger_load()
        # self.Id = len(self.donnees)+1
        # self.Nom=input("Nom du produit à ajouter: ")
        # self.Categorie=input("Catégorie: ")
        # self.Prix=float(input("Prix: "))
        # self.Quantite=int(input("Quantité: "))
        # self.donnees.append({
        #     "nom": self.Nom,
        #     "prix": self.Prix,
        #     "quantite": self.Quantite,
        #     "categorie": self.Categorie
        # })
        self.produits.append(Produit(Id, nom, prix, quantite, seuil_alerte, categorie))
        self.sauvegarde()
        print(f"Produit '{nom}' ajouté avec succès.")

    def modifier_produit(self, nom, nouveau_prix=None, nouvelle_quantite=None, nouveau_seuil=None):
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

            
        

inventaire=GestionnaireInventaire()
inventaire.ajouter_produit(1, "pomme", 200, 20, seuil_alerte=10, categorie="Fruits")
# inventaire.ajouter_produit(1, "ananas", 500, 20, seuil_alerte=10, categorie="Fruits")
# # inventaire.modifier_produit("pomme", nouvelle_quantite=30)
# inventaire.modifier_produit("pomme", nouveau_prix=400, nouvelle_quantite=40, nouveau_seuil=20)
inventaire.supprimer_produit("ananas")