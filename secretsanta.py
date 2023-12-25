import tkinter as tk
from tkinter import messagebox
import random

class SecretSantaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secret Santa Generator")
        self.master.geometry("400x300")

        self.label = tk.Label(master, text="Liste des prénoms (séparés par des virgules) :")
        self.label.pack(pady=10)

        self.prenoms_entry = tk.Entry(master)
        self.prenoms_entry.pack(pady=10)

        # Charger les prénoms depuis le fichier au démarrage
        self.charger_prenoms()

        self.tirage_button = tk.Button(master, text="Effectuer le tirage au sort", command=self.effectuer_tirage)
        self.tirage_button.pack(pady=10)

    def effectuer_tirage(self):
        prenoms_text = self.prenoms_entry.get()
        prenoms = [prenom.strip() for prenom in prenoms_text.split(',')]

        if len(prenoms) < 2:
            messagebox.showwarning("Erreur", "Veuillez entrer au moins deux prénoms pour effectuer le tirage.")
            return

        tirages = self.tirage_secret_santa(prenoms)

        result_window = tk.Toplevel(self.master)
        result_window.title("Résultats du tirage au sort")

        result_label = tk.Label(result_window, text="Résultats du tirage Secret Santa :")
        result_label.pack(pady=10)

        for participant, destinataire in tirages.items():
            result_text = f"{participant} offre un cadeau à {destinataire}"
            result_item = tk.Label(result_window, text=result_text)
            result_item.pack()

        # Enregistrement des prénoms après le tirage pour éviter les doublons
        self.enregistrer_prenoms(prenoms)

    def tirage_secret_santa(self, prenoms):
        participants = prenoms.copy()
        destinataires = prenoms.copy()
        tirages = {}

        random.shuffle(participants)
        random.shuffle(destinataires)

        for participant in participants:
            destinataire = random.choice(destinataires)
            while destinataire == participant or destinataire in tirages.values():
                destinataire = random.choice(destinataires)

            tirages[participant] = destinataire
            destinataires.remove(destinataire)

        return tirages

    def charger_prenoms(self):
        try:
            with open("database.txt", "r") as file:
                prenoms = [prenom.strip() for prenom in file.read().split(',')]
                self.prenoms_entry.insert(0, ', '.join(prenoms))
        except FileNotFoundError:
            print("Le fichier 'database.txt' n'existe pas.")

    def enregistrer_prenoms(self, prenoms):
        with open("database.txt", "w") as file:
            file.write(','.join(prenoms))

if __name__ == "__main__":
    root = tk.Tk()
    app = SecretSantaApp(root)
    root.mainloop()
