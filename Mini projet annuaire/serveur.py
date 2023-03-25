import os
from flask import Flask, render_template, request, redirect
from csv import writer
import shutil
import csv
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# Flask est un micro framework open-source de developpement
# web en Python
# creation de l'application web

app = Flask('annuaire', template_folder=template_dir)
lstrecherch = ["Vous avez recherché aucun contact","Vous avez recherché aucun Numéro"]
lstaffchcontact = []

@app.route('/annuaire.html')
def annuaire():
    triercontact()
    return render_template('annuaire.html',message=lstrecherch, affchcontact = lstaffchcontact )



'''La fonction nouveau_contact récupére le nom du contact dans le 
formulaire l'ajoute dans une liste et ensuite ouvre le fichier.csv et ecrit la liste 
dans le fichier et revient à la ligne'''
@app.route('/ajtcontact', methods=['POST'])

def nouveau_contact():
    
        nom = request.form['nom'] 
        numtel = request.form['numtel']
        nom = nom.title()
        lst = [nom,numtel]
        with open('Fichier.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            writer_object.writerow(lst)  
            f_object.close()
        
        return redirect('annuaire.html')




'''La fonction supprimer contact récupere le nom du contact dans le formulaire 
copie le ficher.csv, après avoir copier le fichier.csv l'efface ouvre le fichiercopy.csv le lit et 
réecrit tout dans fichier.csv vide sauf le nom et le numéros sauf de celui qu'on veut supprimer'''
@app.route('/supprcontact', methods=['POST'])
def supprimer_contact():
    nomsuppr = request.form['nomsuppr']
    
    copie()
    supprimer("Fichier.csv")
      
    input = open('Fichiercopy.csv', 'r')
    output = open('Fichier.csv', 'w',newline='')
    writer = csv.writer(output)
    for row in csv.reader(input):
        if row[0] != nomsuppr:
            writer.writerow(row)
    
    input.close()
    output.close()
    
    supprimer("Fichiercopy.csv")
   
    return redirect('/annuaire.html')


'''La fonction recherchecontact récupére le nom du contact à rechercher lit le fichier.csv
et dès quel trouve dans le fichier.csv un contact avec le même nom que le contact rechercher,
elle renvoi ce contact et le numéros dans une liste'''
@app.route('/rechercher', methods=['POST'])
def recherchercontact():
   
    nbligne = csvcount()
    lstrecherch.clear()
    cpt1 = 0
    search = request.form['recherch']
    search = search.title()
    if nbligne != 0 :   
        input = open('Fichier.csv', 'r')
        for row in csv.reader(input):
            if row[0] == search:
                nomcontact = row[0]
                numcontact = row[1]
                cpt1 += 1
                lstrecherch.append(nomcontact)
                lstrecherch.append(numcontact)
        input.close()
        
        
    if cpt1 == 0:
        lstrecherch.append("aucun contact avec ce nom dans l'annuaire")
        lstrecherch.append("aucun numéro associé à  ce contact")

            
    return redirect('annuaire.html')
    


'''La fonction modifier_contact récupère le nom à modifier, le nouveau nom du
contact et le nouveau numéro puis cherche dans le fichier csv le contact à
modifier et remplace les informations par les nouveaux nom et numéros avant de
renvoyer à la page de l'annuaire '''
@app.route('/modifiercontact', methods=['POST'])
def modifier_contact():
    nom_modif = request.form['nom_modif']
    nouv_nom = request.form['nouveaunom']
    nouv_nom = nouv_nom.title()
    nouv_num = request.form['nouveaunum']
    lst = [nouv_nom, nouv_num]
    
    copie()
    supprimer("Fichier.csv")
      
    input = open('Fichiercopy.csv', 'r')
    output = open('Fichier.csv', 'w',newline='')
    writer = csv.writer(output)
    for row in csv.reader(input):
        if row[0] != nom_modif:
            writer.writerow(row)
        else:
            writer.writerow(lst)
    
    input.close()
    output.close()
    
    supprimer("Fichiercopy.csv")
        
    return redirect('/annuaire.html')
 

'''La fonction trier contact copie le fichier CSV ensuite l’effacer ensuite  prends le 
fichier le copie tri tous les noms notamment avec la fonction lambda, reécrit ensuite 
tous ces nom là dans le fichier. csv et ensuite créer une liste de tuples 
avec le numéro et le nom pour pouvoir y avoir accès dans l' HTML avec Jinja.'''
def triercontact():
    
    copie()
    supprimer("Fichier.csv") 
    
    with open('Fichiercopy.csv',newline='') as fichier_source:
    	lecteur=csv.reader(fichier_source,delimiter=',')
            # on fait le tri
    	lignes_ordonnees = sorted(lecteur, key=lambda test: test[0])

    	with open('Fichier.csv', 'w', newline='') as fichier_sortie:

    		ecriteur = csv.writer(fichier_sortie, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    # on ecrit les lignes triées dans le nouveau fichier
    		for ligne in lignes_ordonnees:
    			ecriteur.writerow(ligne)
    
    supprimer("Fichiercopy.csv")
    
    lstaffchcontact.clear()
    
    input = open('Fichier.csv', 'r')
    for row in csv.reader(input):
            nomcontact = row[0]
            numcontact = row[1]
            lstaffchcontact.append((nomcontact,numcontact))
    
    input.close() 
    
def supprimer(delete):
    with open(delete, 'r+') as f:
         f.truncate(0)
    
def copie():
    source=r'C:\Users\wassi\Desktop\Mini projet annuaire\Fichier.csv'
    destination=r'C:\Users\wassi\Desktop\Mini projet annuaire\Fichiercopy.csv'
    shutil.copyfile(source, destination)
    
'''csvcount sert à vérifier si fichier.csv est vide '''    
def csvcount():
    with open("Fichier.csv", 'r') as f:
        i = 0
        for ligne in f:
            i += 1
    return i



if __name__ == "__main__":
    app.run()
