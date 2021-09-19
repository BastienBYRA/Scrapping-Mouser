#Bibliotheque disponible par defaut
from random import *
import requests
from time import sleep
import re
import os.path
import csv
import sqlite3
import datetime

                                        #Biblotheque a installer
try:
	from selenium import webdriver
except:
	os.system('cmd /c "py -m pip install selenium"')

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
	from seleniumwire import webdriver
except:
	os.system('cmd /c "py -m pip install selenium-wire"')

try:
	import unidecode
except:
	os.system('cmd /c "py -m pip install Unidecode"')

                                        #Variable

#Les chemins
url = 'https://www.mouser.fr/'

csvpath = 'D:/SCRAPPING/PCBComposantScrapCSV.csv'
Chromepath = 'D:/SCRAPPING/chromedriver.exe' #Chemin pour le chromedriver

#Variable lié a la navigation a travers les différentes pages, currentpage etant la page actuelle
currentpage = 1 #Par defaut 1

#Variable de vérificarion d'arriver jusqu'au bout, et empeche de continuer si il manque des informations
arriver, dataEnt, arret, pagedeban = False, False, 0, False

#Nom de la base
dbname = 'PCBComposantScrapDB'

#Variable lié aux noms des catégories de Resistances
categorieResistance = "Vide"
catRes = "Vide"

#Variable lié a la navigation entre les catégories et sous-catégories
typeresistance = 1
typecurrentres = 1

#Différentes listes ou l'on stock les valeurs
nbProdAffiche = 25 #Nombre de resultats afficher dans une page sur le site
tabRef = [None] * nbProdAffiche
tabFab = [None] * nbProdAffiche
tabDesc = [None] * nbProdAffiche
tabQtte = [None] * nbProdAffiche
tabRaccord = [None] * nbProdAffiche
tabOhms = [None] * nbProdAffiche #Valeurs de résistance
tabOhmsUnite = [None] * nbProdAffiche #Valeurs de résistance
tabWatts = [None] * nbProdAffiche
tabWattsUnite = [None] * nbProdAffiche
tabTole = [None] * nbProdAffiche
tabCoef = [None] * nbProdAffiche
tabDegres = [None] * nbProdAffiche
tabCodeCaisse = [None] * nbProdAffiche #Package/Boîte et Code caisse po
tabCondtionnement = [None] * nbProdAffiche
tabSerie = [None] * nbProdAffiche #Série
tabProdTechno = [None] * nbProdAffiche #Produit / Technologie
tabQuali = [None] * nbProdAffiche
tabCircuit = [None] * nbProdAffiche #Type de circuit
tabBroche = [None] * nbProdAffiche #Nombre de broches
tabNbRes = [None] * nbProdAffiche #Nombre de résistances
tabTermination = [None] * nbProdAffiche
tabTempMin = [None] * nbProdAffiche 
tabTempMax = [None] * nbProdAffiche
tabNbTour = [None] * nbProdAffiche
tabVolt = [None] * nbProdAffiche
tabVoltUnite = [None] * nbProdAffiche
tabLength = [None] * nbProdAffiche
tabWidth = [None] * nbProdAffiche
tabHeight = [None] * nbProdAffiche
tabDiam = [None] * nbProdAffiche
tabFreq = [None] * nbProdAffiche
tabCadre = [None] * nbProdAffiche #Cadre ouvert/fermé
tabFonction = [None] * nbProdAffiche
tabType = [None] * nbProdAffiche #Type
tabEmplFils = [None] * nbProdAffiche #Espacement des fils
tabDiamFils = [None] * nbProdAffiche #Diamètre du fil de sortie
tabStyleMontage = [None] * nbProdAffiche
tabNbvoie = [None] * nbProdAffiche
tabBandeResistive = [None] * nbProdAffiche
tabOrientation = [None] * nbProdAffiche
tabElement = [None] * nbProdAffiche
tabTypeArbre = [None] * nbProdAffiche
tabDiamArbre = [None] * nbProdAffiche
tabDiamArbreUnite = [None] * nbProdAffiche
tabLongueurArbre = [None] * nbProdAffiche
tabLongueurArbreUnite = [None] * nbProdAffiche
tabTypeInterrupteur = [None] * nbProdAffiche
tabNbCrans = [None] * nbProdAffiche
tabDureeVie = [None] * nbProdAffiche
tabHoursCycles = [None] * nbProdAffiche
tabClasseIP = [None] * nbProdAffiche
tabLinearite = [None] * nbProdAffiche
tabReglage = [None] * nbProdAffiche

#Recherche groupé ou l'on prend les valeurs tels quels
nomcolumn = ["Conditionnement", "Série", "Style du raccordement", "Produit", "Qualification", "Type de circuit", "Nombre de broches", "Technologie", "Cadre ouvert/fermé", "Code de caisse - po", "Style de montage", "Type de bande résistive", "Orientation", "Type d'élément", "Type d'arbre", "Type d'interrupteur", "Nombre de crans", "Classe IP", "Linéarité", "Réglage"]
nomtabcolumn = [tabCondtionnement, tabSerie, tabRaccord, tabProdTechno, tabQuali, tabCircuit, tabBroche, tabProdTechno, tabCadre, tabCodeCaisse, tabStyleMontage, tabBandeResistive, tabOrientation, tabElement, tabTypeArbre, tabTypeInterrupteur, tabNbCrans, tabClasseIP, tabLinearite, tabReglage]

#Valeur ou l'on ne cherche a prendre que la valeur et non son unité
nommesure = ['Longueur', 'Largeur', 'Hauteur', 'Fréquence', 'Fonctionnalités', "Diamètre", "Nombre de voies", "Diamètre du fil de sortie"]
tabmesure = [tabLength, tabWidth, tabHeight, tabFreq, tabFonction, tabDiam, tabNbvoie, tabDiamFils]

#Valeurs et unités
nomarbremesure = ["Diamètre de l'arbre", "Longueur de l'arbre"]
tabarbremesure = [tabDiamArbre, tabLongueurArbre]
tabarbreunite = [tabDiamArbreUnite, tabLongueurArbreUnite]

#Tableaux pour éviter de faire plusieurs fois les memes lignes de code dans l'update sqlite
nomUpdate = ['Fabriquant', 'Description', 'Quantites', 'Ohms','UniteOhms', 'Watts', 'UniteWatts', 'Voltage', 'UniteVoltage', 'Frequence', 'Tolerance', 'Series', 'Package','Rating', 'Feature', 'TemperatureMin', 'TemperatureMax', 'CoefficientTemperature', 'Degres','CompoTechno', 'StyleRaccordement', 'Terminaison', 'Longueur', 'Largeur', 'Hauteur', 'Diametre', 'NombreTours', 'EmplacementFils', 'DiametreFils', 'Circuit', 'NombrePins', 'NombreResistance', 'Type', 'StyleMontage', 'BandeResistive', 'Orientation', 'TypeElement', 'TypeArbre', 'LongueurArbre', 'UniteLongArb', 'DiametreArbre', 'UniteDiamArbre', 'NombreCrans', 'TypeInterrupteur','DureeVie', 'HeureCycleVie', 'ClasseIP', 'Linearite', 'Reglage', 'Cadre', 'Fonction', 'NombreVoie', 'CodeCaisse']
tabUpdate = [tabFab, tabDesc, tabQtte, tabOhms, tabOhmsUnite, tabWatts, tabWattsUnite, tabVolt, tabVoltUnite, tabFreq, tabTole, tabSerie, tabCondtionnement,tabQuali, tabType, tabTempMin, tabTempMax,tabCoef, tabDegres,tabProdTechno, tabRaccord,tabTermination, tabLength,tabWidth, tabHeight, tabDiam, tabNbTour, tabEmplFils, tabDiamFils, tabCircuit, tabBroche, tabNbRes, tabType,tabStyleMontage, tabBandeResistive, tabOrientation, tabElement, tabTypeArbre,tabLongueurArbre,tabLongueurArbreUnite,tabDiamArbre, tabDiamArbreUnite, tabNbCrans, tabTypeInterrupteur, tabDureeVie, tabHoursCycles, tabClasseIP, tabLinearite, tabReglage, tabCadre, tabFonction, tabNbvoie, tabCodeCaisse]

                                        #Initialisation de Selenium
chrome_options = Options()

#Divers arguments permettant le bon fonctionnement
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-extensions")         
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--allow-running-insecure-content')

#Cette partie me permet de pouvoir me debloquer des "Access Denied"
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options, executable_path=Chromepath)

driver.get(url)

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

	                                               #Creation d'un fichier csv
if os.path.isfile(csvpath): #Si le fichier CSV existe
	pass
else: #Sinon non existant
	with open(csvpath,'w',newline='') as unFichierCSV:
		writer = csv.writer(unFichierCSV)
		# writer.writerow(['Reference', 'Fabriquant', 'Description', 'Quantites', 'Raccordement', 'Ohms' ,'Puissance' ,'Tolerance' ,'Coefficient de temperature', 'Code de caisse'])
		writer.writerow(['Reference', 'Site', 'Fabriquant', 'Description', 'Quantites', 'Categorie de Resistance', 'Ohms','Unite des Ohms', 'Watts', 'Unite des Watts', 'Voltage', 'Unite du Voltage', 'Frequence', 'Tolerance', 'Series', 'Package','Rating', 'Feature', 'Temperature Minimum', 'Temperature Maximum', 'Coefficient de Temperature', 'Degres','Composition/Technologie', 'Raccordement', 'Terminaison', 'Longueur', 'Largeur', 'Hauteur', 'Diametre', 'Nombre de Tour', 'Coating','Mounting Feature', 'Mounting Type', 'Lead', 'Espacement des fils', 'Diametre du fil de sortie', 'Circuit', 'Nombre de Resistance', 'Nombre de Pins / Broche', 'Broche', 'Matching Radio','Radio Drift', 'Application', 'Type', 'Style de Montage', 'Bande Resistive', 'Orientation', 'Type Element', 'Type Arbre', 'Longueur Arbre', 'Unite de la longueur Arbre', 'Diametre Arbre', 'Unite de diametre Arbre', 'Nombre de Crans', 'Type Interrupteur','Duree de Vie', 'Heure/Cycle de Vie', 'Classe IP', 'Linearite', 'Reglage', 'Cadre', 'Fonction', 'NombreVoie', 'Code de Caisse / Package / Case'])


	                                               #Creation et connexion de la base de données
con = sqlite3.connect(dbname + '.db')
cur = con.cursor()

try:
    #Créer la base Resistance
    cur.execute('''CREATE TABLE IF NOT EXISTS Resistance(
        Reference text NOT NULL,
        SiteWeb text NOT NULL,
        Fabricant text,
        Description text,
        Quantites int,
        CategorieDeResistance text,
        Ohms real,
        UniteOhms text,
        Watts real,
        UniteWatts text,
        Voltage real,
        UniteVoltage text,
        Frequence real,
        Tolerance real,
        Series text,
        Package text,
        Rating text,
        Feature text,
        TemperatureMin int,
        TemperatureMax int,
        CoefficientTemperature real,
        Degres text,
        CompoTechno text,
        StyleRaccordement text,
        Terminaison int,
        Longueur real,
        Largeur real,
        Hauteur real,
        Diametre real,
        NombreTours real,
        Coating text,
        MountingFeature text,
        MountingType text,
        Lead text,
        EmplacementFils real,
        DiametreFils real,
        Circuit text,
        NombrePins int,
        NombreResistance real,
        MatchingRadio real,
        RadioDrift real,
        Application text,
        Type text,
        StyleMontage text,
        BandeResistive text,
        Orientation text,
        TypeElement text,
        TypeArbre text,
        LongueurArbre real,
        UniteLongArb text,
        DiametreArbre real,
        UniteDiamArbre text,
        NombreCrans real,
        TypeInterrupteur text,
        DureeVie real,
        HeureCycleVie text,
        ClasseIP text,
        Linearite text,
        Reglage text,
        Cadre text,
        Fonction text,
        NombreVoie real,
        CodeCaisse text,
        PRIMARY KEY (Reference, SiteWeb))
    ''');
except:
    pass

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////


def retour(undriver): #Permet de revenir a la page précédente
    progression = undriver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
    nbprog = len(progression) - 1 #nbprog est le nombre de categorie afficher a l'écran (tout les produits > composant > resistance par exemple)
    if len(progression) > 3:
        try:
            # driver.find_element_by_xpath('//div[@class="breadcrumb-container]/div/nav/ol/li[6]/a').click()
            undriver.find_element_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li['+str(nbprog)+']/a').click()
            sleep(5)
        except:
            pass
    else:
        pass

def onlyactive(undriver): #Permet de cliquer sur la checkbox n'affichant que les resistances vendus et l'appliquer
	undriver.find_element_by_xpath('//div[@class="optional-filters"]/table/tbody/tr/td[2]/div/div/input').click()
	sleep(8)
	undriver.find_element_by_xpath('//table[@class="apply-filter-row"]/tbody/tr/td/input').click()
	sleep(5)

def changementdelangue(undriver): #Switch en anglais pour récupérer le nom de la categ en anglais, ainsi que du lien pour cliquer sur la première catagorie
    sleep(5)
    undriver.find_element_by_xpath('//div[@class="navbar-right"]/div/button').click()
    sleep(5)
    undriver.find_element_by_xpath('//div[@class="navbar-right"]/div/ul/li/button').click()
    sleep(10)

try:
    if url == 'https://www.mouser.fr/':
        #Accepter les cookies
        driver.find_element_by_xpath('//div[@id="gdpr-container"]/div[2]/div/div[2]/form/button').click()
        sleep(5)
        # Connexion a Mouser, va jusqu'a l'onglet Resistance, et va au maximum qu'il peut de la premiere proposition de resistance
        driver.find_element_by_xpath('//div[@id="ProdMenu"]/div/ul/li[5]/a').click()
        sleep(5)
        driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li[12]/div/div[2]/a').click()
        sleep(5)
        onlyactive(driver)

        #Switch en anglais pour récupérer le nom de la categ en anglais
        changementdelangue(driver)

        #Récupération du lien de la première catégorie voulue (typeresistance)
        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
        categorieResistance = catRes.text

        #Reviens en français pour la collecte des données, essentiel car les noms de colonnes utilisés sont en français
        changementdelangue(driver)

        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
        catRes.click()

        #Navigation dans les sous-catégorie si il y a.
        try:
        	driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typecurrentres)+']/div/div[2]/a').click()
        	sleep(5)
        except:
        	pass
        try:
        	driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typecurrentres)+']/div/div[2]/a').click()
        	sleep(5)
        except:
        	pass
    else:
        pass
except:
    sleep(3)
    try:
        ban = len(driver.find_elements_by_xpath('//div[@class="content"]/div[3]/div/div'))
        if ban > 1:
            pagedeban = True
        else:
            pass
    except:
        pass

	                           # #Recherche des différentes valeurs voulues
while(1):

    try:
        ban = len(driver.find_elements_by_xpath('//div[@class="content"]/div[3]/div/div'))
        if ban > 1:
            pagedeban = True
        else:
            pass
    except:
        pass

    if arriver == False and pagedeban == False:
        try:
            sleep(randint(30,90))    #Les sleeps permettent d'essayer d'éviter d'etre ban

            begin_time = datetime.datetime.now()
    
            #Permet de récuperer le nombre d'article afficher dans la page actuel (seulement utile pour la dernière page)
            nbArticle = len(driver.find_elements_by_class_name('mpart-number-lbl'))
            nbA = nbArticle + 1

            #Permet de récupérer le nombre de colonne afficher
            nbCol = len(driver.find_elements_by_xpath("//thead[@class='tblHeader']/tr/th"))

            ref = driver.find_elements_by_xpath("//thead[@class='tblHeader']/tr/th")

            #//////////////////////////////////////////////////////////////////////////////////////////////////////////
            #Modele de ECAO est la premiere colonne avant de le debut des column hide (si on ne compte pas les 2 premieres)
            for i in range(1, len(ref)):
                ECAO = driver.find_element_by_xpath("//thead[@class='tblHeader']/tr/th["+str(i)+"]/span")
                if ECAO.text == "Modèle de ECAO":
                    start = i #Start correspond au numéro de colonne ECAO, la ou commence les colonne xmall
                    break
                else:
                    pass

            #Reference, Fabriquant, Description et Disponibilité sont fixes dans leurs placements, en plus d'avoir des classes particulière
            # Obtentions des references
            for i in range(1,nbA):
                objID = 'lnkMfrPartNumber_' + str(i)
                elements = driver.find_elements_by_id(objID)
                for element in elements:
                    tabRef[i-1] = element.text


            # Obtentions des fabricants
            for i in range(1,nbA):
                objID = 'lnkSupplierPage_' + str(i)
                elements = driver.find_elements_by_xpath("//a[@id='"+objID+"']")
                for element in elements:
                    if "/" in element.text:
                        valeurFabricant = element.text.replace("/", "")
                        valeurFabricant = valeurFabricant.strip()
                        valeurFabricant = " ".join(valeurFabricant.split())
                        tabFab[i-1] = valeurFabricant
                    else:
                        tabFab[i-1] = element.text

            #Description des produits
            elements = driver.find_elements_by_xpath("//td[@class='column desc-column hide-xsmall']")
            i=0
            for element in elements:    
                valeurDescription = element.text.split()
                if "En savoir plus" in element.text:
                    value = element.text.replace("En savoir plus", "")
                    valeurDescription = value.strip()
                    valeurDescription = unidecode.unidecode(valeurDescription)
                    tabDesc[i] = valeurDescription
                    i = i+1
                else:
                    tabDesc[i] = element.text
                    i = i+1

            # Quantites des resistances disponible
            elements = driver.find_elements_by_xpath("//span[@class='available-amount' and not(@id)]")
            i=0
            for element in elements:    
                if str(element.text.isdigit()):
                    valeurQtte = element.text.split()
                    if len(valeurQtte)<2:
                        tabQtte[i] = element.text
                        i = i+1
                    else:
                        tabQtte[i] = str(valeurQtte[0]) + str(valeurQtte[1])
                        i = i+1
                else:
                    tabQtte[i] = None
                    i = i+1


            #Recuperer les valeurs n'ayant pas besoin de conversion ou modification. (les champs dans nomcolumn)
            for i in range(1, nbCol):
                colonne = driver.find_element_by_xpath("//thead[@class='tblHeader']/tr/th["+str(i)+"]/span")
                for nom in nomcolumn:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = nomcolumn.index(colonne.text)
                        j=0
                        for element in elements:
                            if element.text != "" and element.text != "-":
                                element = element.text.replace(",", "")
                                nomtabcolumn[numerotableau][j] = element
                                j = j+1
                            else:
                                nomtabcolumn[numerotableau][j] = None
                                j = j+1
                    else:
                        pass

                #(les champs dans tabmesure)
                for nom in nommesure:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = nommesure.index(colonne.text)
                        j=0
                        for element in elements:
                            if len(element.text) > 1:
                                valeurCol = element.text.replace(' mm', '')
                                valeurCol = valeurCol.replace(' GHz', '')
                                valeurCol = valeurCol.replace(' Gangs', '')
                                valeurCol = valeurCol.replace(' Gang', '')
                                try:
                                    tabmesure[numerotableau][j] = valeurCol
                                    j = j+1
                                except:
                                    valeurCol = valeurCol.split()
                                    tabmesure[numerotableau][j] = valeurCol[0]
                                    j = j+1
                            else:
                                tabmesure[numerotableau][j] = None
                                j = j+1
                    else:
                        pass


                for nom in nomarbremesure:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = nommesure.index(colonne.text)
                        j=0
                        for element in elements:
                            if len(element.text) > 1 and element.text != "No Shaft":
                                if "in" in element.text:
                                    element = element.text.replace("in", "")
                                    tabarbremesure[numerotableau][j] = element
                                    tabarbreunite[numerotableau][j] = "in"
                                    j = j+1
                                elif "mm" in element.text:
                                    element = element.text.replace("mm", "")
                                    tabarbremesure[numerotableau][j] = element
                                    tabarbreunite[numerotableau][j] = "mm"
                                    j = j+1
                                else:
                                    tabarbremesure[numerotableau][j] = None
                                    tabarbreunite[numerotableau][j] = None
                                    j = j+1
                            else:
                                tabarbremesure[numerotableau][j] = None
                                tabarbreunite[numerotableau][j] = None
                                j = j+1
                    else:
                        pass

                #//////////////////////////////////////////////////////////////////////////////////////////////////////////
                #Les valeurs a récupérer nécessitant des modifications lors de leur prise

                if colonne.text == "Résistance":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for value in element:
                        valeurRes = value.text.split()  
                        if len(valeurRes) > 1:
                            valeurOhms = valeurRes[0]
                            UniteOhms = valeurRes[1]

                            if valeurOhms != "Zero" and str(valeurOhms).isdigit() or re.findall('\d+\.\d+', valeurOhms):
                                tabOhms[j] = valeurOhms
                                tabOhmsUnite[j] = UniteOhms
                                j = j+1
                            else:
                                tabOhms[j] = None
                                tabOhmsUnite[j] = None
                                j = j+1
                        else:
                            tabOhms[j] = None
                            tabOhmsUnite[j] = None
                            j = j+1


                if colonne.text == 'Données de puissance':
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for value in element:    
                        valeurPuissance = value.text.split()
                        if len(valeurPuissance) == 2 or len(valeurPuissance) > 2: #Straight aura donc la valeur None
                            valeurWatts = valeurPuissance[0]
                            uniteWatts = valeurPuissance[1]

                            tabWatts[j] = valeurWatts
                            tabWattsUnite[j] = uniteWatts
                            j = j+1
                        else:
                            tabWatts[j] = None
                            tabWattsUnite[j] = None
                            j = j+1

                if colonne.text == 'Tolérance':
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    cptTour=0
                    for element in elements:
                        valeurTole = element.text.split()
                        if len(valeurTole)> 0 and valeurTole[0] != "-":

                            valeurTolerance = valeurTole[0]

                            if valeurTolerance == "Jumper":
                                tabTole[cptTour] = 0
                                cptTour = cptTour+1
                            elif len(valeurTole) == 1:
                                val = valeurTolerance.replace('±', "")
                                val = val.replace('+', "")
                                val = val.replace(',', "")
                                val = val.replace('%', "")
                                tabTole[cptTour] = val
                                cptTour = cptTour+1
                            elif len(valeurTole) > 1 and valeurTolerance == "0%," or valeurTolerance == "-0%,":
                                valeurTolerance2 = valeurTole[1]
                                val = valeurTolerance2.replace('±', "")
                                val = val.replace('+', "")
                                val = val.replace(',', "")
                                val = val.replace('%', "")
                                tabTole[cptTour] = val
                                cptTour = cptTour+1
                            else:
                                val = valeurTolerance.replace('±', "")
                                val = val.replace('+', "")
                                val = val.replace(',', "")
                                val = val.replace('%', "")
                                tabTole[cptTour] = val
                                cptTour = cptTour+1
                        else:
                            tabTole[cptTour] = None
                            cptTour = cptTour+1
                else:
                    pass

                if colonne.text == "Coefficient de température":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:    
                        valeurCoef = element.text.split()
                        if len(valeurCoef) > 2:
                            if valeurCoef[0] != "-" and str(valeurCoef[0]).isdigit() and valeurCoef[0] != "0":
                                tabCoef[j] = valeurCoef[0]
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1
                            elif valeurCoef[0] == "-" and str(valeurCoef[1]).isdigit():
                                tabCoef[j] = "-" + str(valeurCoef[1])
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1

                            elif len(valeurCoef)<5 and valeurCoef[0] == "0" and str(valeurCoef[0]).isdigit():
                                tabCoef[i] = str(valeurCoef[0])
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1

                            elif len(valeurCoef)>4 and valeurCoef[0] == "0" and str(valeurCoef[5]).isdigit():
                                tabCoef[i] = str(valeurCoef[5])
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1
                            elif len(valeurCoef)>5 and valeurCoef[0] == "0" and str(valeurCoef[6]).isdigit():
                                tabCoef[i] = str(valeurCoef[6])
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1
                            elif len(valeurCoef)>6 and valeurCoef[0] == "0" and str(valeurCoef[4]).isdigit():
                                tabCoef[i] = str(valeurCoef[4])
                                if "C" in element.text:
                                    tabDegres[j] = "Celsius"
                                else:
                                    tabDegres[j] = "Kelvin"
                                j+=1
                            else:
                                tabCoef[i] = None
                                tabDegres[i] = None
                                j+=1
                        else:    #Si aucune valeur
                            tabCoef[i] = None
                            tabDegres[i] = None
                            j+=1

                if colonne.text == "Terminaison":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        valeurTerminaison = element.text.split()
                        if len(valeurTerminaison) > 0:
                            tabTermination[j] = "".join(valeurTerminaison[0])
                            j+=1
                        else:
                            tabTermination[j] = None
                            j+=1

                if colonne.text == "Température de fonctionnement min.":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        valeurTempMin = element.text.split()
                        if len(valeurTempMin) > 0:
                            if valeurTempMin[0] != "-":
                                tabTempMin[j] = "".join(valeurTempMin[0])
                                j+=1

                            #Negative
                            elif valeurTempMin[0] == "-" and str(valeurTempMin[1]).isdigit():
                                tabTempMin[j] = "".join("-" + str(valeurTempMin[1]))
                                j+=1
                            else:
                                tabTempMin[j] = "".join(valeurTempMin[1])
                                j+=1
                        else:
                            tabTempMin[j] = None
                            j+=1

                if colonne.text == "Température de fonctionnement max.":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        valeurTempMax = element.text.split()
                        if len(valeurTempMax) > 0:
                            if valeurTempMax[0] != "+":
                                tabTempMax[j] = "".join(valeurTempMax[0])
                                j+=1
                            elif valeurTempMax[0] == "+" and str(valeurTempMax[1]).isdigit():
                                tabTempMax[j] = "".join(valeurTempMax[1])
                                j+=1
                            else:
                                tabTempMax[j] = None
                                j+=1
                        else:
                            tabTempMax[j] = None
                            i = i+1
                
                if colonne.text == "Nombre de tours":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        valeurNbTour = element.text.split()
                        if len(valeurNbTour) > 0:
                            if str(valeurNbTour[0]).isdigit() and len(valeurNbTour) >= 1:
                                tabNbTour[j] = "".join(valeurNbTour[0])
                                j+=1
                            elif valeurNbTour[0] == 'Multiturn':
                                tabNbTour[j] = None
                                tabProd[j] = 'Multiturn'
                                j+=1
                        else:
                            tabNbTour[i] = None
                            j+=1

                if colonne.text == "Tension de voltage":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        valeurVoltage = value.text.split()
                        if len(valeurVoltage) > 1:
                            valeurVolt = valeurVoltage[0]
                            uniteVolt = valeurVoltage[1]

                            tabVolt[j] = "".join(valeurVolt)
                            tabVoltUnite[j] = "".join(uniteVolt)
                            j+=1
                        else:
                            tabVolt[i] = None
                            tabVoltUnite[j] = None
                            j+=1

                if colonne.text == "Plage de résistance": #Aucune idée de comment gérer celui la (Kits de résistance)
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        if element.text != "":
                            tabOhms[j] = element.text
                            j+=1
                        else:
                            tabOhms[j] = None
                            j+=1

                if colonne.text == "Package/Boîte":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        if element.text != "-" or element.text != "":
                            tabCodeCaisse[j] = element.text
                            j+=1
                        else:
                            tabCodeCaisse[j] = None
                            j+=1


                if colonne.text == "Espacement des fils":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        if element.text != "-" or element.text != "":
                            valeurEspacementFil = element.text.split()
                            tabEmplFils[j] = valeurEspacementFil[0]
                            j+=1
                        else:
                            tabEmplFils[j] = None
                            j+=1

                if colonne.text == "Durée de vie":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        if element.text != "-" or element.text != "":
                            valeurDureeVie = value.text.split()

                            if "Cycle" in element.text:
                                tabDureeVie[j] = valeurDureeVie[0]
                                tabHoursCycles[j] = "Cycles"
                                j+=1

                            elif "Hour" in element.text:
                                tabDureeVie[j] = valeurDureeVie[0]
                                tabHoursCycles[j] = "Hours"
                                j+=1

                            elif len(element) == 1 :
                                tabDureeVie[i] = valeurDureeVie[0]
                                tabHoursCycles[i] = None
                                i+=1
                            else:
                                tabDureeVie[i] = None
                                tabHoursCycles[i] = None
                                i+=1
                        else:
                            tabDureeVie[i] = None
                            tabHoursCycles[i] = None
                            i+=1

                if colonne.text == "Nombre de résistances":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    elements = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for element in elements:
                        if element.text != "-" or element.text != "":
                            valeurNbRes = element.text.split()
                            tabNbRes[j] = valeurNbRes[0]
                            j+=1
                        else:
                            tabNbRes[j] = None
                            j+=1

            arriver = True

        except Exception as e: #Probleme avec la récupération des données
            #Permet de passer la variable arriver, et donc de refresh ensuite
            print(e)
            print("Erreur lors de la collecte des données, veuillez patientez")
            print(driver.current_url)

    else: #arriver veut dire l'on n'arrive pas inscrire les données, mais elle sont déja dans les tableaux.
        pass
   
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Ouverture et écriture des données dans le fichier CSV
        if arriver == True:
            
            for i in range(int(nbArticle)):

                with open(csvpath,'a',newline='') as unFichierCSV:
                    writer=csv.writer(unFichierCSV)
                    writer.writerow([tabRef[i], "Mouser", tabFab[i], tabDesc[i], tabQtte[i], categorieResistance, tabOhms[i], tabOhmsUnite[i],tabWatts[i], tabWattsUnite[i],tabVolt[i], tabVoltUnite[i], tabFreq[i], tabTole[i], tabSerie[i], tabCondtionnement[i],tabQuali[i], tabType[i], tabTempMin[i], tabTempMax[i],tabCoef[i], tabDegres[i],tabProdTechno[i], tabRaccord[i],tabTermination[i], tabLength[i],tabWidth[i], tabHeight[i], tabDiam[i], tabNbTour[i], None, None, None,None,tabEmplFils[i], tabDiamFils[i], tabCircuit[i], tabNbRes[i], tabBroche[i], None, None, None, None, tabStyleMontage[i], tabBandeResistive[i], tabOrientation[i], tabElement[i], tabTypeArbre[i],tabLongueurArbre[i],tabLongueurArbreUnite[i],tabDiamArbre[i], tabDiamArbreUnite[i], tabNbCrans[i], tabTypeInterrupteur[i], tabDureeVie[i], tabHoursCycles[i], tabClasseIP[i], tabLinearite[i], tabReglage[i], tabCadre[i],tabFonction[i], tabNbvoie[i], tabCodeCaisse[i]])

                    insertdata = '''INSERT INTO Resistance VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    data = (tabRef[i], "Mouser", tabFab[i], tabDesc[i], tabQtte[i], categorieResistance, tabOhms[i], tabOhmsUnite[i],tabWatts[i], tabWattsUnite[i], tabVolt[i], tabVoltUnite[i], tabFreq[i], tabTole[i], tabSerie[i], tabCondtionnement[i],tabQuali[i], tabType[i], tabTempMin[i], tabTempMax[i],tabCoef[i], tabDegres[i],tabProdTechno[i], tabRaccord[i],tabTermination[i], tabLength[i],tabWidth[i], tabHeight[i], tabDiam[i], tabNbTour[i], None, None, None,None,tabEmplFils[i], tabDiamFils[i], tabCircuit[i], tabBroche[i], tabNbRes[i], None, None, None, None, tabStyleMontage[i], tabBandeResistive[i], tabOrientation[i], tabElement[i], tabTypeArbre[i],tabLongueurArbre[i],tabLongueurArbreUnite[i],tabDiamArbre[i], tabDiamArbreUnite[i], tabNbCrans[i], tabTypeInterrupteur[i], tabDureeVie[i], tabHoursCycles[i], tabClasseIP[i], tabLinearite[i], tabReglage[i], tabCadre[i], tabFonction[i], tabNbvoie[i], tabCodeCaisse[i])

                    try: #Entrer les valeurs une première fois
                        cur.execute(insertdata, data)
                        con.commit()
                    except sqlite3.IntegrityError: #Permet de pouvoir entrer les valeurs actuels pour une reference déja entrer 
                    #Update seulement si les valeurs sont non vides, permet de ne pas update a des valeurs existante avec des null
                        for nom in nomUpdate:
                            # numerotableau = categorie.index(nom) #index de categorie correspondant a nom
                            nbcat = nomUpdate.index(nom)
                            try:
                                if tabUpdate[nbcat][i] != None:
                                    insertdata = '''UPDATE Resistance SET '''+nom+''' = ? WHERE Reference = ? AND SiteWeb = ?;'''
                                    data = (tabUpdate[nbcat][i], tabRef[i], 'Mouser')
                                    cur.execute(insertdata, data)
                                    con.commit()
                                else:
                                    pass

                                if categorieResistance != None:
                                    insertdata = '''UPDATE Resistance SET CategorieDeResistance = ? WHERE Reference = ? AND SiteWeb = ?;'''
                                    data = (categorieResistance, tabRef[i], 'Mouser')
                                    cur.execute(insertdata, data)
                                    con.commit()

                            except sqlite3.OperationalError: #Si les deux script envoie trop de données en meme temps
                                print("Base en cours d'utilisation")
                                sleep(randint(3, 10))

                    except sqlite3.OperationalError: #Si les deux script envoie trop de données en meme temps
                        print("Base en cours d'utilisation")
                        sleep(randint(3, 10))

            dataEnt = True

    # # //////////////////////////////////////////////////////////////////////////////////////////////////////////

            if dataEnt == True:

                #Cette partie permet passer a la page suivante
                dataEnt = False
                arriver = False
                print("page" + str(currentpage) + "fini !" + str(datetime.datetime.now() - begin_time))
                print(driver.current_url)
                arret = 0
                currentpage = currentpage + 1
                sleep(randint(15,40))
                aleatoire = 0
                aleatoire = randint(0,10)
                if aleatoire % 3 == 0:
                    sleep(randint(7,12))
                else:
                    pass
                try:
                    driver.find_element_by_xpath("//a[@id='lnkPager_lnkNext']").click()
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@id='lnkMfrPartNumber_1']")))
                except:

                    #Partie permettant le changement de categorie
                    sleep(3)
                    retour(driver)
                    incretyperes = driver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
                    if len(incretyperes) == 3:
                        onlyactive(driver)
                        typeresistance +=1
                        changementdelangue(driver)
                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance = catRes.text
                        changementdelangue(driver)

                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        catRes.click()
                    else:
                        sleep(5)
                    nbres = 0
                    try:
                        nbres = driver.find_elements_by_xpath('//div[@class="types-of-category"]/div/ul/li')
                        if len(nbres) > 1:
                            try:
                                driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typecurrentres)+']/div/div[2]/a').click()
                                typecurrentres += 1
                            except:
                                typecurrentres = 1
                                retour(driver)
                        else:
                            pass
                    except:
                        pass

                    incretyperes = driver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
                    if len(incretyperes) == 3:
                        onlyactive(driver)
                        typeresistance +=1
                        changementdelangue(driver)
                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance = catRes.text
                        changementdelangue(driver)

                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        catRes.click()

                    nbres = 0
                    try:
                        nbres = driver.find_elements_by_xpath('//div[@class="types-of-category"]/div/ul/li')
                        if len(nbres) > 1:
                            try:
                                driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typecurrentres)+']/div/div[2]/a').click()
                                typecurrentres += 1
                            except:
                                typecurrentres = 1
                                retour(driver)
                        else:
                            pass
                    except:
                        pass

                    sleep(5)
                            ######################################################################################

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Permet de refresh si il y a eu des probleme, voir d'arreter le programme, en evitant que currentpage s'incrémente.

        else:
            print("Probleme lors de la récupération des données, refresh de la page a venir.")
            sleep(2)
            arret = arret+1

            pagedeban = True
            if arret == 5:
                driver.save_screenshot("erreurMOUSER.png")
                sleep(2)
                print("Probleme persistant, arret du script a la page ." + str(currentpage))
                print(driver.current_url)
                driver.quit()
            elif arret>2:
                curl = driver.current_url
                driver.quit()
                sleep(15)
                driver.get(curl)
            else:
                driver.refresh()
                sleep(5)