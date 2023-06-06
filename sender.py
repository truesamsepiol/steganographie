# code de l'emetteur

import sys
import os
from PIL import Image #pour transformer nos images en niveau 
import numpy


SIZE_IMAGE = 512 
SIZE_BLOCK = 18
SUB_SIZE_BLOCK = 6
MAX_HASH_CODE = 256

class Hash:
    def __init__(self, x, y, mask):
        self.x = x
        self.y = y
        self.mask = mask


#Table de hash
hashTable = [] 

#secret
secret = ""

#-0 Initialisation de la table de hash
def init():
    for id in range(MAX_HASH_CODE):
        hashTable.append(Hash(0, 0, 0))

#1- Generation de la table de hachage a partir d'une image
def generationTableHachage(image):

    #Transformation de l'image en niveau de gris
    img = Image.open(image)
    imageGray = img.convert('L')

    #redimenstionner l'image
    newDim = (SIZE_IMAGE, SIZE_IMAGE)
    imageGray = imageGray.resize(newDim)

    #initialisation de la table de hachage
    init()

    #boucle principale
    i = 0
    while i < SIZE_IMAGE:
        j = 0
        while j < SIZE_IMAGE:
            blockI = i
            print("Debut de calcul pour le block de coordonnes (", i, "," , j, ")")
            while blockI < (i + SIZE_BLOCK):
                blockJ = j
                while blockJ < (j + SIZE_BLOCK):
                    subBlockI = blockI
                    while subBlockI < (blockI + SUB_SIZE_BLOCK):
                        subBlockJ = blockJ
                        while subBlockJ < (blockJ + SUB_SIZE_BLOCK):
                            #contruire matrice tmp
                            subBlockJ += 1
                        subBlockI += 1
                    #cacul des valeurs propres
                    #retrouner le max 
                    #construire la chaine binaire selon l'arrangement 2
                    blockJ += SUB_SIZE_BLOCK
                blockI += SUB_SIZE_BLOCK
            #mettre a jour la table de hash
            # 1- contruction du code ascii en fonction de la chaine binaire
            # 2- mise a jour de la table
            print("Fin de calcul pour le block de coordonnes (", i, "," , j, ")")
            j += SIZE_BLOCK
        i += SIZE_BLOCK

    

#-------------- PROGRAMME PRINCIPALE -------------------------------------
if __name__ == "__main__" :
    
    
    #verifie que le script a recu exactement deux arguments et que le second est une image
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[2]):
        print("\n\nMauvaise usage du script\nLe script attend deux arguments\nArgument1: Le secret\nArgument2: le chemin vers le repertoire contenant l'image\n\n")
        print("Pour lancer le script entrer la commande: |\n")
        print("                                          |-> python3 ", sys.argv[0], " \"votre secret\" chemin_vers_image\n\n")
        exit(1)


    secret = str(sys.argv[1])
    generationTableHachage(sys.argv[2])

    #for id in range(MAX_HASH_CODE):
     #   print("id = ", id, " x = ", hashTable[id].x, " y = ", hashTable[id].y, " mask = ", hashTable[id].mask)
