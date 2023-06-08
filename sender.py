# code de l'emetteur

import sys
import os
from PIL import Image #pour transformer nos images en niveau 
import numpy


SIZE_IMAGE = 504 #travailler avec des multiples de 18 pour eviter des debordements de memoire (a regler plustard)
SIZE_BLOCK = 18
SUB_SIZE_BLOCK = 6
MAX_HASH_CODE = 128 #mettre a 256 pour travailler sur 8 bits

class Hash:
    def __init__(self, x, y, mask):
        self.x = x
        self.y = y
        self.mask = mask


#Table de hash
hashTable = [] 

#Initialisation de la table de hash 
def init():
    for id in range(MAX_HASH_CODE):
        hashTable.append(Hash(-1, -1, 0))


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


#Mise a jour de la table de hachage
#cette table contient les coordonnes, et mask et le code Ascii
def miseAjourTableHachage(x, y, code):
    codeBinaire = "0" + code[1:] #cette ligne permet de travailler uniquement avec 7 bits
    codeAscii = int(codeBinaire, 2) #conversion chaine binaire en entier
    hashTable[codeAscii].x = x
    hashTable[codeAscii].y = y
    hashTable[codeAscii].mask = 1
    print("Le block (" + str(x) + "," + str(y) + ") a pour chaine binaire ==> " + codeBinaire + " equivalent en ASCII a ==> " + str(codeAscii) + " correspond au caractere ==> " + chr(codeAscii))
    

#Generation de la table de hachage a partir d'une image
def generationTableHachage(image):
    #Transformation de l'image en niveau de gris
    img = Image.open(image)
    imageGray = img.convert('L')

    #redimenstionner l'image
    newDim = (SIZE_IMAGE, SIZE_IMAGE)
    imageGray = imageGray.resize(newDim)

    #Recuperation des dimensions et contenu de l'image
    largeur, hauteur = imageGray.size                  
    lign = []
    imageData = []
    for valeur in list(imageGray.getdata()):
        lign.append(valeur)
        if len(lign) == largeur:
            imageData.append(lign)
            lign = []
    #fin recuperation dimension  et contenu

    #initialisation de la table de hachage
    init()

    #boucle principale
    _maxPrecedent = 0
    chaineBinaire = ""
    i = 0
    while i < SIZE_IMAGE:
        j = 0
        while j < SIZE_IMAGE:
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
            #mettre a jour la table de hash
            miseAjourTableHachage(i, j, chaineBinaire)
            print("\nFin de calcul pour le block de coordonnes (", i, "," , j, ")\n")
            j += SIZE_BLOCK
        i += SIZE_BLOCK
    #fin de la boucle principale


def afficherTableHachage():
    print("\n               ################ Table de hachage ################")
    for id in range(MAX_HASH_CODE):
        x = hashTable[id].x
        y = hashTable[id].y
        mask = hashTable[id].mask
        if mask == 1 :
            print("     codeAscii = ", id, ",  coordonnees du block (", str(x), ",", str(y), "),  et le mask = ", str(mask))
    print("                 ##################################################\n")

    
def incorporationSecret(secret):
    send = True #verifie si tout les caracteres sont incorpores
    cle = ""
    for car in secret:
        code = ord(car) #code ascii du caractere
        if hashTable[code].mask == 0:
            send = False
        cle += str(hashTable[code].x) + "," + str(hashTable[code].y) + "\n"

    if send:
        fichier = open("cleSecretePartage", "w")
        fichier.write(cle)
        fichier.close()
        print("\n\n\n       SUCCES. Secret dissimuler dans l'image\n\n")
    else:
        print("\n\n         ECHEC. Veuillez choisir une autre image pour ce secret\n")

 
#-------------- PROGRAMME PRINCIPALE -------------------------------------
if __name__ == "__main__" :
    #verifie que le script a recu exactement deux arguments et que le second est une image
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[2]):
        print("\n\nMauvaise usage du script\nLe script attend deux arguments\nArgument1: Le secret\nArgument2: le chemin vers le repertoire contenant l'image\n\n")
        print("Pour lancer le script entrer la commande: |\n")
        print("                                          |-> python3 ", sys.argv[0], " \"votre secret\" chemin_vers_image\n\n")
        exit(1)


    generationTableHachage(sys.argv[2])
    afficherTableHachage()
    incorporationSecret(str(sys.argv[1]))
