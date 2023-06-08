#code du recepteur

import sys
import os
from PIL import Image #pour transformer nos images en niveau 
import numpy


SIZE_IMAGE = 504 #travailler avec des multiples de 18 pour eviter des debordements de memoire (a regler plustard)
SIZE_BLOCK = 18
SUB_SIZE_BLOCK = 6

#contruction d'une matrice de taille SUB_SIZE_BLOCK * SUB_SIZE_BLOCK
#calcul puis retourne le max des valeurs propres
def maxValeursPropres(debutI, finI, debutJ, finJ, data):
    matrice = numpy.zeros((SUB_SIZE_BLOCK, SUB_SIZE_BLOCK))
    x = 0
    i = debutI
    while i < finI:
        j = debutJ
        y = 0
        while j < finJ:
            matrice[x][y] = data[i][j]
            j += 1
            y += 1
        i += 1
        x += 1
    valeursPropres = numpy.linalg.eigvals(matrice)

    return max(valeursPropres).real #retourner uniquement la partie reel


#Reconstitution du secret
def constructionSecret(cle, image):
    #Transformation de l'image en niveau de gris
    img = Image.open(image)
    imageGray = img.convert('L')


    #redimenstionner l'image
    newDim = (SIZE_IMAGE, SIZE_IMAGE)
    imageGray = imageGray.resize(newDim)

    #Recuperation des dimensions et contenu de l'image
    largeur, hauteur = imageGray.size                  
    print("largeur image == " + str(largeur) + " et longeur == " + str(hauteur))
    lign = []
    imageData = []
    for valeur in list(imageGray.getdata()):
        lign.append(valeur)
        if len(lign) == largeur:
            imageData.append(lign)
            lign = []
    #fin recuperation dimension et contenu

    #boucle principale
    secret = ""
    _maxPrecedent = 0
    chaineBinaire = ""
    fichier = open(cle, "r")
    for ligne in fichier:
        coordonnees = ligne.split(",")
        i = int(coordonnees[0])
        j = int(coordonnees[1])
        blockI = i
        print("\nDebut de calcul pour le block de coordonnes (", i, "," , j, ")\n")
        while blockI < (i + SIZE_BLOCK):
            blockJ = j
            while blockJ < (j + SIZE_BLOCK):
                #retroune le max des valeurs propres
                maxSuivant = maxValeursPropres(blockI, blockI + SUB_SIZE_BLOCK, blockJ, blockJ + SUB_SIZE_BLOCK, imageData)
                #construire la chaine binaire selon l'arrangement 2
                if blockJ == j and blockI == i:
                    chaineBinaire = ""
                else:
                    if maxPrecedent >= maxSuivant:
                        chaineBinaire += "1"
                    else:
                        chaineBinaire += "0"
                maxPrecedent = maxSuivant
                blockJ += SUB_SIZE_BLOCK
            blockI += SUB_SIZE_BLOCK


        codeBinaire = "0" + chaineBinaire[1:] #cette ligne permet de travailler uniquement avec 7 bits
        codeAscii = int(codeBinaire, 2) #conversion chaine binaire en entier
        print( "code binaire ==> " + codeBinaire + " equivalent en ASCII a ==> " + str(codeAscii) + " correspond au caractere ==> " + chr(codeAscii))
        print("\nFin du calcul pour le block de coordonnes (", i, "," , j, ")\n")
        secret += str(chr(codeAscii))
    #fin de la boucle principale
     
    print("\n\n\n       SUCCES. Le secret est \"" + secret + "\"\n\n")
    
#-------------- PROGRAMME PRINCIPALE -------------------------------------
if __name__ == "__main__" :
    #verifie que le script a recu exactement deux arguments et que le second est une image
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print("\n\nMauvaise usage du script\nLe script attend deux arguments\nArgument1: La cle secret partagee\nArgument2: le chemin vers le repertoire contenant l'image stegano\n\n")
        print("Pour lancer le script entrer la commande: |\n")
        print("                                          |-> python3 ", sys.argv[0], " \"cle secrete partagee\" chemin_vers_image\n\n")
        exit(1)

    constructionSecret(str(sys.argv[1]), str(sys.argv[2]))
