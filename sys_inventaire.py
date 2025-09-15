import csv
import json
import os

# Classe Product
class Product:
    CSV_FILE = "gestion_inventaire.csv"
    FIELDNAMES = ["ID", "name", "description", "category_id", "supplier_id",
                "price", "cost", "quantity", "min_quantity", "SKU", "created_at", "updated_at"]

    def __init__(self, id, name, description, category_id, supplier_id, price, cost, quantity, min_quantity, SKU, created_at, updated_at):
        self.id = id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.price = price
        self.cost = cost
        self.quantity = int(quantity)
        self.min_quantity = int(min_quantity)
        self.SKU = SKU
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _charger_produits():
        if not os.path.exists(Product.CSV_FILE):
            return []
        with open(Product.CSV_FILE, "r", newline="") as file:
            lecteur = csv.DictReader(file)
            return list(lecteur)

    def ajouter_produit(self):
        """Ajoute un produit en vérifiant que la catégorie existe"""
        if not Category.categorie_existe(self.category_id):
            print(f" La catégorie '{self.category_id}' n'existe pas. Ajoutez-la d'abord.")
            return

        produits = self._charger_produits()
        for p in produits:
            if p["ID"] == self.id:
                print(f" Un produit avec l'ID '{self.id}' existe déjà.")
                return
            if p["SKU"] == self.SKU:
                print(f" Un produit avec le SKU '{self.SKU}' existe déjà.")
                return

        fichier_existe = os.path.exists(self.CSV_FILE)
        with open(self.CSV_FILE, 'a', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            if not fichier_existe:
                writer.writeheader()
            writer.writerow({
                "ID": self.id, "name": self.name, "description": self.description,
                "category_id": self.category_id, "supplier_id": self.supplier_id,
                "price": self.price, "cost": self.cost, "quantity": self.quantity,
                "min_quantity": self.min_quantity, "SKU": self.SKU,
                "created_at": self.created_at, "updated_at": self.updated_at
            })
        print("Produit ajouté avec succès !")

    @staticmethod
    def lister_produits():
        produits = Product._charger_produits()
        if not produits:
            print(" Aucun produit enregistré.")
            return
        print("\n Liste des produits :")
        for i, ligne in enumerate(produits, start=1):
            print(f"{i}: {ligne}")

    @staticmethod
    def rechercher_produit(a_rechercher):
        produits = Product._charger_produits()
        for ligne in produits:
            if (
                a_rechercher.strip().lower() == ligne["ID"].strip().lower()
                or a_rechercher.strip().lower() == ligne["name"].strip().lower()
                or a_rechercher.strip().lower() == ligne["SKU"].strip().lower()
            ):
                print(f"Produit trouvé : {ligne}")
                return
        print(" Aucun produit trouvé.")

    @staticmethod
    def modifier_produit(name, **modifications):
        produits = Product._charger_produits()
        modifie = False
        for ligne in produits:
            if ligne["name"].strip().lower() == name.strip().lower():
                for champ, valeur in modifications.items():
                    if champ in ligne:
                        ligne[champ] = str(valeur)
                modifie = True
        if modifie:
            with open(Product.CSV_FILE, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=Product.FIELDNAMES)
                writer.writeheader()
                writer.writerows(produits)
            print(f"Produit '{name}' modifié avec succès.")
        else:
            print(f"Produit '{name}' introuvable.")

    @staticmethod
    def supprimer_produit(nom_produit):
        produits = Product._charger_produits()
        nouvelle_liste = [p for p in produits if p["name"].strip().lower() != nom_produit.strip().lower()]
        if len(produits) == len(nouvelle_liste):
            print(f" Produit '{nom_produit}' introuvable.")
            return
        with open(Product.CSV_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=Product.FIELDNAMES)
            writer.writeheader()
            writer.writerows(nouvelle_liste)
        print(f"Produit '{nom_produit}' supprimé avec succès.")

    @staticmethod
    def produits_par_categorie(category_name):
        produits = Product._charger_produits()
        if not produits:
            print(" Aucun produit enregistré.")
            return
        trouve = False
        print(f"\n Produits de la catégorie '{category_name}' :")
        for ligne in produits:
            if ligne["category_id"].strip().lower() == category_name.strip().lower():
                print(ligne)
                trouve = True
        if not trouve:
            print(" Aucun produit trouvé dans cette catégorie.")

    @staticmethod
    def produits_stock_faible():
        produits = Product._charger_produits()
        if not produits:
            print(" Aucun produit enregistré.")
            return
        print("\n Produits en rupture ou stock faible :")
        trouve = False
        for ligne in produits:
            try:
                if int(ligne["quantity"]) <= int(ligne["min_quantity"]):
                    print(ligne)
                    trouve = True
            except ValueError:
                pass
        if not trouve:
            print(" Aucun produit en rupture ou stock faible.")


# Classe Category
class Category:
    JSON_FILE = "les_categories.json"

    def __init__(self, id, name, description, created_at):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    @staticmethod
    def _charger_categories():
        if not os.path.exists(Category.JSON_FILE):
            return []
        try:
            with open(Category.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def categorie_existe(category_id):
        categories = Category._charger_categories()
        return any(cat["ID"].lower() == category_id.lower() or cat["name"].lower() == category_id.lower() for cat in categories)

    def ajouter_categorie(self):
        categories = Category._charger_categories()
        for c in categories:
            if c["ID"].lower() == self.id.lower() or c["name"].lower() == self.name.lower():
                print(" Cette catégorie existe déjà.")
                return
        categories.append({
            "ID": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        })
        with open(self.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(categories, file, indent=4, ensure_ascii=False)
        print(" Catégorie ajoutée avec succès.")

    @staticmethod
    def lecture_categories():
        categories = Category._charger_categories()
        if not categories:
            print(" Aucune catégorie enregistrée.")
            return
        print("\n Liste des catégories :")
        for cat in categories:
            print(cat)

    @staticmethod
    def supprimer_categorie(nom_categorie):
        categories = Category._charger_categories()
        nouvelle_liste = [c for c in categories if c["name"].lower() != nom_categorie.lower()]
        if len(categories) == len(nouvelle_liste):
            print(f" La catégorie '{nom_categorie}' n'existe pas.")
            return
        with open(Category.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(nouvelle_liste, file, indent=4, ensure_ascii=False)
        print(f"️ Catégorie '{nom_categorie}' supprimée avec succès.")
# Classe Fournisseur
class Fournisseur:
    JSON_FILE = "les_fournisseurs.json"

    def __init__(self, id, name, phone, email, address, created_at):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at

    @staticmethod
    def _charger_fournisseurs():
        if not os.path.exists(Fournisseur.JSON_FILE):
            return []
        try:
            with open(Fournisseur.JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def fournisseur_existe(fournisseur_id):
        fournisseurs = Fournisseur._charger_fournisseurs()
        return any(f["ID"].lower() == fournisseur_id.lower() or f["name"].lower() == fournisseur_id.lower()
                for f in fournisseurs)

    def ajouter_fournisseur(self):
        fournisseurs = Fournisseur._charger_fournisseurs()
        for f in fournisseurs:
            if f["ID"].lower() == self.id.lower() or f["name"].lower() == self.name.lower():
                print(" Ce fournisseur existe déjà.")
                return
        fournisseurs.append({
            "ID": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at
        })
        with open(self.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(fournisseurs, file, indent=4, ensure_ascii=False)
        print(" Fournisseur ajouté avec succès.")

    @staticmethod
    def lecture_fournisseurs():
        fournisseurs = Fournisseur._charger_fournisseurs()
        if not fournisseurs:
            print(" Aucun fournisseur enregistré.")
            return
        print("\n Liste des fournisseurs :")
        for f in fournisseurs:
            print(f)

    @staticmethod
    def modifier_fournisseur(nom, **modifications):
        fournisseurs = Fournisseur._charger_fournisseurs()
        modifie = False
        for f in fournisseurs:
            if f["name"].strip().lower() == nom.strip().lower():
                for champ, valeur in modifications.items():
                    if champ in f:
                        f[champ] = str(valeur)
                modifie = True
        if modifie:
            with open(Fournisseur.JSON_FILE, "w", encoding="utf-8") as file:
                json.dump(fournisseurs, file, indent=4, ensure_ascii=False)
            print(f" Fournisseur '{nom}' modifié avec succès.")
        else:
            print(f" Fournisseur '{nom}' introuvable.")

    @staticmethod
    def supprimer_fournisseur(nom_fournisseur):
        fournisseurs = Fournisseur._charger_fournisseurs()
        nouvelle_liste = [f for f in fournisseurs if f["name"].lower() != nom_fournisseur.lower()]
        if len(fournisseurs) == len(nouvelle_liste):
            print(f" Le fournisseur '{nom_fournisseur}' n'existe pas.")
            return
        with open(Fournisseur.JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(nouvelle_liste, file, indent=4, ensure_ascii=False)
        print(f" Fournisseur '{nom_fournisseur}' supprimé avec succès.")
    @staticmethod
    def produits_par_fournisseur(fournisseur_name):
        produits = Product._charger_produits()
        if not produits:
            print(" Aucun produit enregistré.")
            return
        trouve = False
        print(f"\n Produits du fournisseur '{fournisseur_name}' :")
        for ligne in produits:
            if ligne["supplier_id"].strip().lower() == fournisseur_name.strip().lower():
                print(ligne)
                trouve = True
        if not trouve:
            print(" Aucun produit trouvé pour ce fournisseur.")
class StockManager:
    HISTORIQUE_FILE = "historique_mouvements.json"

    @staticmethod
    def _charger_historique():
        if not os.path.exists(StockManager.HISTORIQUE_FILE):
            return []
        try:
            with open(StockManager.HISTORIQUE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def _sauver_historique(historique):
        with open(StockManager.HISTORIQUE_FILE, "w", encoding="utf-8") as file:
            json.dump(historique, file, indent=4, ensure_ascii=False)

    @staticmethod
    def mise_a_jour_stock(nom_produit, quantite, type_mouvement):
        produits = Product._charger_produits()
        modifie = False
        for p in produits:
            if p["name"].strip().lower() == nom_produit.strip().lower():
                ancienne_qte = int(p["quantity"])
                if type_mouvement == "ajout":
                    p["quantity"] = str(ancienne_qte + int(quantite))
                elif type_mouvement == "retrait":
                    p["quantity"] = str(max(0, ancienne_qte - int(quantite)))
                modifie = True

                # Enregistrer dans l’historique
                historique = StockManager._charger_historique()
                historique.append({
                    "produit": nom_produit,
                    "mouvement": type_mouvement,
                    "quantite": quantite,
                    "ancienne_qte": ancienne_qte,
                    "nouvelle_qte": p["quantity"]
                })
                StockManager._sauver_historique(historique)

        if modifie:
            with open(Product.CSV_FILE, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=Product.FIELDNAMES)
                writer.writeheader()
                writer.writerows(produits)
            print(" Stock mis à jour avec succès.")
        else:
            print(f" Produit '{nom_produit}' introuvable.")

    @staticmethod
    def consulter_historique():
        historique = StockManager._charger_historique()
        if not historique:
            print(" Aucun mouvement enregistré.")
            return
        print("\n Historique des mouvements :")
        for h in historique:
            print(h)

    @staticmethod
    def valorisation_totale():
        produits = Product._charger_produits()
        total = 0
        for p in produits:
            try:
                total += int(p["quantity"]) * float(p["cost"])
            except ValueError:
                continue
        print(f" Valeur totale du stock : {total}")




# Menus
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gestion des produits")
        print("2. Gestion des catégories")
        print("3. Gestion des fournisseurs")
        print("4. Outils de stock")
        print("0. Quitter")

        choix = input(" Votre choix : ")

        if choix == "1":
            menu_produits()
        elif choix == "2":
            menu_categories()
        elif choix=="3":
            menu_fournisseurs()
        elif choix=="4":
            menu_stocks()
        elif choix == "0":
            print(" Au revoir !")
            break
        else:
            print(" Choix invalide.")


def menu_produits():
    while True:
        print("\n--- Gestion des Produits ---")
        print("1. Ajouter un produit")
        print("2. Lister les produits")
        print("3. Rechercher un produit")
        print("4. Modifier un produit")
        print("5. Supprimer un produit")
        print("6. Afficher les produits par catégorie")
        print("7. Afficher les produits en stock faible")
        print("0. Retour")

        choix = input(" Votre choix : ")

        if choix == "1":
            id = input("ID produit : ")
            name = input("Nom produit : ")
            description = input("Description : ")
            category_id = input("Catégorie (ID ou nom) : ")
            supplier_id = input("Fournisseur : ")
            price = input("Prix : ")
            cost = input("Coût : ")
            quantity = input("Quantité : ")
            min_quantity = input("Quantité minimale : ")
            SKU = input("SKU : ")
            created_at = input("Date de création : ")
            updated_at = input("Date de mise à jour : ")

            produit = Product(id, name, description, category_id, supplier_id, price, cost, quantity, min_quantity, SKU, created_at, updated_at)
            produit.ajouter_produit()

        elif choix == "2":
            Product.lister_produits()

        elif choix == "3":
            recherche = input("Nom, ID ou SKU du produit : ")
            Product.rechercher_produit(recherche)

        elif choix == "4":
            nom = input("Nom du produit à modifier : ")
            champ = input("Champ à modifier : ")
            valeur = input("Nouvelle valeur : ")
            Product.modifier_produit(nom, **{champ: valeur})

        elif choix == "5":
            nom = input("Nom du produit à supprimer : ")
            Product.supprimer_produit(nom)

        elif choix == "6":
            cat = input("Nom ou ID de la catégorie : ")
            Product.produits_par_categorie(cat)

        elif choix == "7":
            Product.produits_stock_faible()

        elif choix == "0":
            break
        else:
            print(" Choix invalide.")


def menu_categories():
    while True:
        print("\n--- Gestion des Catégories ---")
        print("1. Ajouter une catégorie")
        print("2. Lister les catégories")
        print("3. Supprimer une catégorie")
        print("0. Retour")

        choix = input(" Votre choix : ")

        if choix == "1":
            id = input("ID catégorie : ")
            name = input("Nom catégorie : ")
            description = input("Description : ")
            created_at = input("Date de création : ")
            categorie = Category(id, name, description, created_at)
            categorie.ajouter_categorie()

        elif choix == "2":
            Category.lecture_categories()

        elif choix == "3":
            nom = input("Nom de la catégorie à supprimer : ")
            Category.supprimer_categorie(nom)

        elif choix == "0":
            break
        else:
            print(" Choix invalide.")
def menu_fournisseurs():
    while True:
        print("\n--- Gestion des Fournisseurs ---")
        print("1. Ajouter un fournisseur")
        print("2. Lister les fournisseurs")
        print("3. Modifier un fournisseur")
        print("4. Supprimer un fournisseur")
        print("5. Voir les produits d'un fournisseur")
        print("0. Retour")

        choix = input(" Votre choix : ")

        if choix == "1":
            id = input("ID fournisseur : ")
            name = input("Nom fournisseur : ")
            phone = input("Téléphone : ")
            email = input("Email : ")
            address = input("Adresse : ")
            created_at = input("Date de création : ")
            fournisseur = Fournisseur(id, name, phone, email, address, created_at)
            fournisseur.ajouter_fournisseur()

        elif choix == "2":
            Fournisseur.lecture_fournisseurs()

        elif choix == "3":
            nom = input("Nom du fournisseur à modifier : ")
            champ = input("Champ à modifier (name, phone, email, address) : ")
            valeur = input("Nouvelle valeur : ")
            Fournisseur.modifier_fournisseur(nom, **{champ: valeur})

        elif choix == "4":
            nom = input("Nom du fournisseur à supprimer : ")
            Fournisseur.supprimer_fournisseur(nom)

        elif choix == "5":
            fournisseur = input("Nom ou ID du fournisseur : ")
            Product.produits_par_fournisseur(fournisseur)

        elif choix == "0":
            break
        else:
            print(" Choix invalide.")
def menu_stocks():
    while True:
        print("\n--- Outils de gestion des stocks ---")
        print("1. Mettre à jour le stock d'un produit")
        print("2. Afficher les alertes de stock faible")
        print("3. Consulter l'historique des mouvements")
        print("4. Valorisation du stock")
        print("0. Retour")

        choix = input(" Votre choix : ")

        if choix == "1":
            nom = input("Nom du produit : ")
            type_mvt = input("Type de mouvement (ajout/retrait) : ")
            qte = input("Quantité : ")
            StockManager.mise_a_jour_stock(nom, qte, type_mvt)

        elif choix == "2":
            Product.produits_stock_faible()

        elif choix == "3":
            StockManager.consulter_historique()

        elif choix == "4":
            StockManager.valorisation_totale()

        elif choix == "0":
            break
        else:
            print(" Choix invalide.")




# Lancement
if __name__ == "__main__":
    menu()
