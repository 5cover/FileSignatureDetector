import pandas
import interface

""" Nom du fichier CSV de base de données de signatures. """
NOM_CSV = "signatures.csv"

def lireHexadecimal(nomFichier: str, nbOctets: int):
    assert nbOctets >= 0, "Le nombre d'octets à lire doit être positif"
    """ Lit en héxadécimal dans un fichier un certain nombre d'octets.
    Source : https://stackoverflow.com/a/34687617 """
    with open(nomFichier, 'rb') as f:
        return f.read(nbOctets).hex()

def obtenirLongueurPlusLongueSignature():
    """ Retourne la longueur de la plus longue signature enregistrée dans la base de données. """
    return len(max(pandas.read_csv(NOM_CSV).loc[:, "Signature"], key=len))

def rechercherSignature(possibleSignature: str):
    """ Alogorithme glouton qui retourne la ligne de la base de donnée correspondant à la signature spécifiée,
    ou un DataFrame vide si aucune signature ne correspond.
    La variable de retour, un DataFrame Pandas, peut s'utiliser comme un dictionnaire."""
    
    # Au départ, toutes les signatures pourraient convenir
    candidats = pandas.read_csv(NOM_CSV)
    
    # On boucle sur chaque chiffre de la potentielle signature
    for i in range(len(possibleSignature)):
        
        candidatsOntChiffre = []
        for candidat in candidats.Signature:
            # Le candidat est valide si il est moins long que la signature 
                                        # OU
            # si son ième chiffre correspond au ième chiffre de la signature
            candidatsOntChiffre.append(i >= len(candidat) or candidat[i] == possibleSignature[i]) 
            
        # Indexation. On garde les candidats aux index de candidatsOntChiffre qui ont pour valeur True.
        candidats = candidats.loc[candidatsOntChiffre]
    
    # On retourne la ligne du DataFrame candidats contenant plus longue signature qui pourrait convenir
    return candidats.loc[candidats.Signature == max(candidats.Signature, key=len, default=None)]


def obtenirSignature(nomFichier):
    return rechercherSignature(lireHexadecimal(nomFichier, obtenirLongueurPlusLongueSignature()//2))


def test():
    """ Test de la fonction de lecture hexadécimale et de l'algorithme de recherche de signature """
    print("Test en cours...")
    hexdata = lireHexadecimal("fichier_test", obtenirLongueurPlusLongueSignature()//2)
    print(hexdata)
    assert hexdata == "4d5a900003000000", "La fonction lireHexadecimal a retourne de mauvaises donnees."
    assert rechercherSignature(hexdata).Signature.iloc[0] == "4d5a", "La fonction trouverSignature n'a pas trouve la signature."
    print("Test reussi.")

""" Cette condition permet d'exécuter le script seulement si il est ouvert en tant que fichier et non pas importé. """
if __name__ == "__main__":
        #test()    
        interface.creerFenetre()

