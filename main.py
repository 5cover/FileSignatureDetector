import pandas
import interface

""" Nom du fichier CSV de base de données de signatures. """
NOM_CSV = "signatures.csv"

def lireHexadecimal(nomFichier: str, nbCaracteres: int):
    """ Lit en héxadécimal dans un fichier un certain nombre de caractères.
    Source : https://stackoverflow.com/a/34687617 """
    with open(nomFichier, 'rb') as f:
        hexdata = f.read().hex()
    return hexdata[0:nbCaracteres]

def obtenirLongueurPlusLongueSignature():
    """ Retourne la longueur de la plus longue signature enregistrée dans la base de données. """
    return len(max(pandas.read_csv(NOM_CSV).loc[:, "Signature"], key=len))

def rechercherSignature(possibleSignature: str):
    """ Retourne la ligne de la base de donnée correspondant à la signature spécifiée,
    ou None si aucune signature de correspond.
    La variable de retour, un DataFrame Pandas, peut s'utiliser comme un dictionnaire."""
    
    # Au départ, toutes les signatures pourraient convenir
    candidats = pandas.read_csv(NOM_CSV)
    
    # On boucle sur chaque chiffre de la potentielle signature
    for i in range(len(possibleSignature)):
        
        candidatsOntChiffre = []
        for candidat in candidats.Signature:
            # On conserve le candidat si on l'a dépassé ou si il contient le bon chiffre
            # L'opérateur séquentiel "or" permet de ne pas tenter d'accéder à un chiffre de candidat trop élevé.
            candidatsOntChiffre.append(i >= len(candidat) or candidat[i] == possibleSignature[i]) 
            
        # Indexation. On garde les candidats aux index de candidatsOntChiffre qui ont pour valeur True.
        candidats = candidats.loc[candidatsOntChiffre, :]
    
    # On retourne la ligne du DataFrame candidats contenant plus longue signature qui pourrait convenir
    return candidats.loc[candidats.Signature == max(candidats.Signature, key=len, default=None)]


def obtenirSignature(nomFichier):
    return rechercherSignature(lireHexadecimal(nomFichier, obtenirLongueurPlusLongueSignature()))


def test():
    """ Test de la fonction de lecture hexadécimale et de l'algorithme de recherche de signature """
    print("Test en cours...")
    hexdata = lireHexadecimal("fichier_test", obtenirLongueurPlusLongueSignature())
    assert hexdata == "4d5a900003000000", "La fonction lireHexadecimal a retourne de mauvaises donnees."
    assert rechercherSignature(hexdata).Signature.iloc[0] == "4d5a", "La fonction trouverSignature n'a pas trouve la signature."
    print("Test reussi.")

if __name__ == "__main__":
        interface.creerFenetre()

