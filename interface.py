import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import main

def creerFenetre():
    
    # Constantes correspondant au texte des labels et à leur clé dans dicLabels.
    EXPLORATEUR = "Fichier sélectionné : "
    SIGNATURE = "Signature : "
    DESCRIPTION = "Description : "
    EXTENSIONS = "Extensions : "
    
    INTROUVABLE = "(introuvable)"
    
    # Définition de la marge (padding) extérieure à 10 pixels.
    PAD = 10
    
    dicLabels = {}
    
    def selectionnerFichier():
        nomFichier = tk.filedialog.askopenfilename()
        signature = main.obtenirSignature(nomFichier)

        def configurerLabel(nom, texteAAjouter):
            """ Met la propriété text du label de dicLabels[nom] à la valeur nom+texteAAjouter. """
            dicLabels[nom].configure(text = nom+texteAAjouter)
        
        configurerLabel(EXPLORATEUR, nomFichier)
        
        # Si la signature n'a pas été trouvée (le DataFrame est vide)
        if signature.empty:
            configurerLabel(SIGNATURE, INTROUVABLE)
            configurerLabel(DESCRIPTION, INTROUVABLE)
            configurerLabel(EXTENSIONS, INTROUVABLE)
        else:
            configurerLabel(SIGNATURE, signature.Signature.iloc[0])
            configurerLabel(DESCRIPTION, signature.Description.iloc[0])
            configurerLabel(EXTENSIONS, signature.Extensions.iloc[0])
        
    
    root = tk.Tk()
    root.title("Détecteur de signature de fichier") # titre de la fenêtre
    root.minsize(237, 180) # taille minimum en pixels
    root.config(bg="white") # couleur de fond : blanc
    
    boutonParcourir = ttk.Button(text = "Parcourir", command = selectionnerFichier, padding=(3,3,3,3))
    boutonParcourir.pack(padx = PAD, pady = PAD, side=tk.LEFT, anchor = tk.NW)
    
    
    def updateWraplength(event):
        """ Sous-fonction qui définit la propriété wraplength d'un contrôle à la largeur de celui-ci.
            Cela garantit un comportement cohérent de retour à la ligne automatique. """
        event.widget.configure(wraplength=event.width-6)
    
    def ajouterLabel(texte):
        """ Fonction locale qui permet d'éviter la répétition du code de création de labels. """
        label = ttk.Label(root, text=texte, borderwidth=2, relief="groove", padding=(3,3,3,3)) # Création du label
        label.bind("<Configure>", updateWraplength) # Bind de l'évènement de changement de taille
        dicLabels[texte] = label # Ajout au dictionnaire des labels
        label.pack(padx = PAD, pady = PAD, fill=tk.BOTH, expand=1) # Pack du label
    
    ajouterLabel(EXPLORATEUR)
    ajouterLabel(SIGNATURE)
    ajouterLabel(DESCRIPTION)
    ajouterLabel(EXTENSIONS)
    
    root.mainloop()
