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

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

		#Variable

#Les chemins
url = 'https://www.mouser.fr/'
csvpath = 'D:/.../MyCSVFile.csv'
Chromepath = 'D:/.../chromedriver.exe' #Chemin pour le chromedriver

#Variable lié a la navigation a travers les différentes pages, currentpage etant la page actuelle
currentpage = 1 #Par defaut 1

#Variable de vérificarion d'arriver jusqu'au bout, et empeche de continuer si il manque des informations
arriver, dataEnt, arret = False, False, 0

#Nom de la base
dbname = 'PCBComposantScrapDB'

#Variable lié a la navigation entre les catégories et sous-catégories
typeresistance = 1
typecurrentres = 1

#Variable lié aux noms des catégories de Resistances
categorieResistance = "Vide"
catRes = "Vide"

#Verifie si on est sur la page ou l'on test si on est un robot
pagedeban = False

#Différentes listes ou l'on stock les valeurs
nbProdAffiche = 25
tabRef = [None] * nbProdAffiche #Référence
tabFab = [None] * nbProdAffiche #Fabricant
tabDesc = [None] * nbProdAffiche #Description
tabQtte = [None] * nbProdAffiche #Disponibilité
tabOhms = [None] * nbProdAffiche #ESR
tabOhmsUnite = [None] * nbProdAffiche #ESR
tabVolt = [None] * nbProdAffiche #
tabVoltUnite = [None] * nbProdAffiche #
tabVoltAC = [None] * nbProdAffiche #
tabUniteAC = [None] * nbProdAffiche #
tabVoltDC = [None] * nbProdAffiche #
tabUniteDC = [None] * nbProdAffiche #
tabCapacitance = [None] * nbProdAffiche #
tabCapacitanceUnite = [None] * nbProdAffiche #
tabDureeVie = [None] * nbProdAffiche #Durée de vie
tabHoursCycles = [None] * nbProdAffiche #
tabTole = [None] * nbProdAffiche #Tolerance
tabSeries = [None] * nbProdAffiche #Series
tabPackage = [None] * nbProdAffiche #Packaging
tabTypePackage = [None] * nbProdAffiche #Type de package  
tabRating = [None] * nbProdAffiche #Ratings
tabFeature = [None] * nbProdAffiche #Feature
tabTempsUtiDeb = [None] * nbProdAffiche #Température de fonctionnement min.
tabTempsUtiFin = [None] * nbProdAffiche #Température de fonctionnement max.
tabCourantRejec = [None] * nbProdAffiche #Courant de réjection
tabUniteCourantRejet = [None] * nbProdAffiche #Courant de réjection
tabCourantNominal = [None] * nbProdAffiche #Courant nominal
tabUniteCourantNominal = [None] * nbProdAffiche #Courant nominal
tabCourantFuite = [None] * nbProdAffiche #Courant de fuite
tabUniteCourantFuite = [None] * nbProdAffiche #Courant de fuite
tabLength = [None] * nbProdAffiche #Longueur
tabWidth = [None] * nbProdAffiche #Largeur
tabDiametre = [None] * nbProdAffiche #Diamètre
tabHeight = [None] * nbProdAffiche #Hauteur
tabType = [None] * nbProdAffiche #Type
tabBoitier = [None] * nbProdAffiche #
tabDielectric = [None] * nbProdAffiche #
tabRaccord = [None] * nbProdAffiche #Style du raccordement
tabTermination = [None] * nbProdAffiche #Termination STRING
tabManufacturerCode = [None] * nbProdAffiche #Code caisse du fabricant
tabPins = [None] * nbProdAffiche #Number of Pins / Broche
tabElement = [None] * nbProdAffiche #Nombre d'éléments
tabProduct = [None] * nbProdAffiche #Produit
tabEspacementFils = [None] * nbProdAffiche #
tabUniteEspacementFils = [None] * nbProdAffiche #
tabStyleFilSortie = [None] * nbProdAffiche #
tabBorneTerre = [None] * nbProdAffiche #Borne de terre
tabProfondeurEpaisseur = [None] * nbProdAffiche #Profondeur / Épaisseur
tabOrientation = [None] * nbProdAffiche #Orientation
tabCodeCaisse = [None] * nbProdAffiche #Package/Boîte   Code de caisse - po

#Recherche groupé car demande les memes "condition"
nomcolumn = ["Série", "Style du raccordement", "Diélectrique", "Package/Boîte", "Code de caisse - po", "Style à fil de sortie", "Qualification", "Conditionnement", "Style à fil de sortie", "Produit", "Terminaison", "Style du boîtier", "Type de package", "Type", "Nombre d'éléments", "Code caisse du fabricant", "Orientation"]
nomtabcolumn = [tabSeries, tabRaccord, tabDielectric, tabCodeCaisse, tabCodeCaisse, tabStyleFilSortie, tabRating, tabPackage, tabStyleFilSortie, tabProduct, tabTermination, tabBoitier, tabTypePackage, tabType, tabElement, tabManufacturerCode, tabOrientation]

#Recherche groupé pour les champs ayant mm
nommesure = ['Longueur', 'Largeur', 'Hauteur', 'Diamètre', 'Borne de terre', 'Longueur / Hauteur', 'Longueur / Hauteur', 'Profondeur / Épaisseur']
tabmesure = [tabLength, tabWidth, tabHeight, tabDiametre, tabBorneTerre, tabLength, tabHeight, tabProfondeurEpaisseur]

#Recherche groupé pour les champs ou l'on doit récupérer la valeur et l'unité de la valeur
tabnomPower = ["Capacité électrique", "Tension de voltage CC", "Tension de fonctionnement CA", "Espacement des fils", "ESR", "Courant de réjection", "Courant nominal", "Courant de fuite"]
tabvaluePower = [tabCapacitance, tabVoltDC, tabVoltAC, tabEspacementFils, tabOhms, tabCourantRejec, tabCourantNominal, tabOhms, tabCourantFuite]
tabunitPower = [tabCapacitanceUnite, tabUniteDC, tabUniteAC, tabUniteEspacementFils, tabOhmsUnite, tabUniteCourantRejet, tabUniteCourantNominal, tabOhmsUnite, tabUniteCourantFuite]

#Recherche groupé pour les champs ou l'on doit récupérer uniquement la valeur
tabnomPower2 = ["Nombre de broches"]
tabvaluePower2 = [tabPins]

nomUpdate = ['Fabricant','Description','Quantites','Ohms','UniteOhms', 'Volt', 'UniteVolt','VoltageAC','UniteAC','VoltageDC','UniteDC','Capacitance','UniteCapacitance','DureeDeVie','HeureOuCycle', 'Tolerance','Series', 'Package', 'TypePackage', 'Rating','Feature', 'TemperatureMin', 'TemperatureMax', 'CourantDeRejection','UniteCourantRejection','CourantNominal','UniteCourantNominal','CourantFuite','UniteCourantFuite','Longueur','Largeur', 'Diametre','Hauteur','Type','StyleBoitier','Dielectric','Raccordement','Terminaison','ManufacturerCode', 'NombreBroche','NombreElement','Produit','EspacementFil','UniteEspacementFil','FilSortie','BorneDeTerre','ProfondeurEpaisseur','Orientation', 'CodeCaisse']
tabUpdate = [tabFab, tabDesc,tabQtte,tabOhms, tabOhmsUnite,tabVolt, tabVoltUnite, tabVoltAC, tabUniteAC,tabVoltDC, tabUniteDC,tabCapacitance, tabCapacitanceUnite, tabDureeVie, tabHoursCycles,tabTole,tabSeries,tabPackage,tabTypePackage, tabRating, tabFeature,tabTempsUtiDeb,tabTempsUtiFin,tabCourantRejec,tabUniteCourantRejet,tabCourantNominal,tabUniteCourantNominal,tabCourantFuite,tabUniteCourantFuite,tabLength, tabWidth, tabDiametre, tabHeight, tabType,  tabBoitier, tabDielectric,tabRaccord,tabTermination,  tabManufacturerCode, tabPins,tabElement,tabProduct,tabEspacementFils,tabUniteEspacementFils,tabStyleFilSortie,tabBorneTerre,tabProfondeurEpaisseur,tabOrientation,tabCodeCaisse]

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
if os.path.isfile(csvpath):
	pass
else:
	with open(csvpath,'w',newline='') as unFichierCSV:
		writer = csv.writer(unFichierCSV)
		# writer.writerow(['Reference', 'Fabriquant', 'Description', 'Quantites', 'Raccordement', 'Ohms' ,'Puissance' ,'Tolerance' ,'Coefficient de temperature', 'Code de caisse'])
		writer.writerow(['Reference', 'Site', 'Fabricant', 'Description', 'Categorie de Resistance', 'Quantites', 'Ohms','Unite des Ohms', 'Voltage', 'Unite des Volt', 'Frequence', 'Unite de Frequence', 'Voltage AC', 'Unite de volt AC', 'Frequence de voltage AC','Voltage DC', 'Unite de volt DC', 'Frequence de voltage DC', 'Capacitance', 'Unite de capacitance', 'Duree de Vie', 'Heure/Cycle de Vie', 'Tolerance', 'Leakage', 'Facteur de dissipation', 'Series', 'Package', 'Type de Package', 'Rating', 'Feature', 'Temperature Minimum', 'Temperature Maximum', 'Courant de rejection', 'Unite du courant de rejection', 'Courant nominal', 'Unite du courant nominal', 'Courant de fuite', 'Unite du courant de fuite','Courant d ondulation faible', 'Unite du courant faible', 'Frequence du courant faible','Courant d ondulation haute', 'Unite du courant haute', 'Frequence du courant haute','Longueur', 'Largeur',  'Diametre', 'Hauteur', 'Thickness', 'Mounting Type', 'Application','Circuit', 'Nombre de condensateurs', 'Coefficient de Temperature', 'Type','Lead', 'Style de boitier', 'Polarisation', 'Q', 'Q @ Freq', 'Dielectric','Lead Style', 'Raccordement', 'Terminaison', 'ESL', 'Code de fabricant', 'Ajustement','Nombre de broches', 'Nombre d element', 'Produit', 'Espacement des fils','Unite espacement des fils', 'Fil de sortie', 'Borne de terre', 'Profondeur / Epaisseur', 'Orientation', 'Code de Caisse / Package / Case'])





    #Creation et connexion de la base de données
con = sqlite3.connect(dbname + '.db')
cur = con.cursor()

#Créer la base Condensateur
cur.execute('''CREATE TABLE IF NOT EXISTS Condensateur(
    Reference text NOT NULL,
    SiteWeb text NOT NULL,
    Fabricant text,
    Description text,
    Categorie text,
    Quantites int,
    ValeurOhms real,
    UniteOhms text,
    ValeurVolt real,
    UniteVolt text,
    Frequence real,
    UniteFrequence text,
    VoltageAC real,
    UniteAC text,
    VoltageDC real,
    UniteDC text,
    Capacitance real,
    UniteCapacitance text,
    DureeDeVie real,
    HeureOuCycle text,
    Tolerance real,
    Leakage real,
    DissipationFactor real,
    Series text,
    Package text,
    TypePackage text,
    Rating text,
    Feature text,
    TemperatureMin int,
    TemperatureMax int,
    CourantDeRejection real,
    UniteCourantRejection text,
    CourantNominal real,
    UniteCourantNominal text,
    CourantFuite real,
    UniteCourantFuite text,
    AmpereLowHZ real,
    AmpereLowUnite text,
    LowFrequence real,
    AmpereHighKHZ real,
    AmpereHighUnite text,
    HighFrequence real,
    Longueur real,
    Largeur real,
    Diametre real,
    Hauteur real,
    Thickness real,
    MountingType text,
    Application text,
    Circuit text,
    NombreCapacitors real,
    TemperatureCoef text,
    Type text,
    Lead text,
    StyleBoitier text,
    Polarization text,
    Q real,
    QFrequence real,
    Dielectric text,
    LeadStyle text,
    Raccordement text,
    Terminaison text,
    ESLph real,
    ManufacturerCode text,
    Ajustement text,
    NombreBroche real,
    NombreElement real,
    Produit text,
    EspacementFil real,
    UniteEspacementFil text,
    FilSortie text,
    BorneDeTerre real,
    ProfondeurEpaisseur real,
    Orientation text,
    CodeCaisse text,
    PRIMARY KEY (Reference, SiteWeb))
''');

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////

def retour(undriver): #Permet de revenir a la page précédente
    progression = undriver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
    nbprog = len(progression) - 1
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

def changementdelangue(undriver): #Switch en anglais pour récupérer le nom de la categ en anglais
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
        driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li[4]/div/div[2]/a').click()
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
        sleep(3)

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
while(1): #Toujours vrai, boucle infini
    
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

            arriver = False
            begin_time = datetime.datetime.now()
    
            #Permet de récuperer le nombre d'article afficher dans la page actuel (seulement utile pour la dernière page)
            nbArticle = len(driver.find_elements_by_class_name('mpart-number-lbl'))
            nbA = nbArticle + 1

            #Permet de récupérer le nombre de colonne afficher
            nbCol = len(driver.find_elements_by_xpath("//thead[@class='tblHeader']/tr/th"))

            ref = driver.find_elements_by_xpath("//thead[@class='tblHeader']/tr/th")


            #Modele de ECAO est la premiere colonne avant de le debut des column hide (si on ne compte pas les 2 premieres)
            for i in range(1, len(ref)):
                ECAO = driver.find_element_by_xpath("//thead[@class='tblHeader']/tr/th["+str(i)+"]/span")
                if ECAO.text == "Modèle de ECAO":
                    start = i
                    break
                else:
                    pass

            #Reference, Fabriquant, Description et Disponibilité sont fixes dans leurs placements, en plus d'avoir des classes particulière
            # Obtentions des references
            for i in range(1,nbA):
                objID = 'lnkMfrPartNumber_' + str(i)
                ref = driver.find_elements_by_id(objID)
                for element in ref:
                    tabRef[i-1] = element.text


             # Obtentions des fabriquants
            for i in range(1,nbA):
                objID = 'lnkSupplierPage_' + str(i)
                ref = driver.find_elements_by_xpath("//a[@id='"+objID+"']")
                for element in ref:
                    if "/" in element.text:
                        value = element.text.replace("/", "")
                        r = value.strip()
                        r = " ".join(r.split())
                        tabFab[i-1] = r
                    else:
                        tabFab[i-1] = element.text

             #Description des produits
            ref = driver.find_elements_by_xpath("//td[@class='column desc-column hide-xsmall']")
            i=0
            for element in ref:    
                r = element.text.split()
                if "En savoir plus" in element.text:
                    value = element.text.replace("En savoir plus", "")
                    r = value.strip()
                    r = unidecode.unidecode(r)
                    tabDesc[i] = r
                    i = i+1
                else:
                    tabDesc[i] = element.text
                    i = i+1

             # Quantites des resistances disponible
            ref = driver.find_elements_by_xpath("//span[@class='available-amount' and not(@id)]")
            i=0
            for element in ref:    
                if str(element.text.isdigit()):
                    r = element.text.split()
                    if len(r)<2:
                        tabQtte[i] = element.text
                        i = i+1
                    else:
                        tabQtte[i] = str(r[0]) + str(r[1])
                        i = i+1
                else:
                    tabQtte[i] = None
                    i = i+1

            #/////////////////////////////////////////////////////////////////////////////////////////////////////////

            #Recuperer les valeurs n'ayant pas besoin de conversion ou modification. (les champs dans nomcolumn)

            for i in range(1, nbCol):
                colonne = driver.find_element_by_xpath("//thead[@class='tblHeader']/tr/th["+str(i)+"]/span")
                for nom in nomcolumn:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = nomcolumn.index(colonne.text)
                        j=0
                        for value in element:
                            if value.text != "" and value.text != "-":
                                value = value.text.replace(",", "")
                                nomtabcolumn[numerotableau][j] = value
                                # print(nomtabcolumn[numerotableau][j] + " a l'index " + str(j))
                                j = j+1
                            else:
                                nomtabcolumn[numerotableau][j] = None
                                # print("rien " + str(j))
                                j = j+1
                    else:
                        pass

                #(les champs dans tabmesure)
                for nom in nommesure:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = nommesure.index(colonne.text)
                        j=0
                        for value in element:
                            if len(value.text) > 1:
                                val = value.text.replace(' mm', '')
                                try:
                                    tabmesure[numerotableau][j] = val
                                    # print(tabmesure[numerotableau][j] + " a l'index " + str(j))
                                    j = j+1
                                except:
                                    val = val.split()
                                    tabmesure[numerotableau][j] = val[0]
                                    # print(tabmesure[numerotableau][j] + " a l'index " + str(j))
                                    j = j+1
                            else:
                                tabmesure[numerotableau][j] = None
                                # print("rien " + str(j))
                                j = j+1
                    else:
                        pass

                #Les champs dans tabPower, Ohms, Watts, Volt...
                for nom in tabnomPower:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = tabnomPower.index(colonne.text)
                        j=0
                        # print(colonne.text)
                        for value in element:
                            if value.text != "" and value.text != "-":
                                val = value.text.replace("AC", "")
                                val = val.replace("DC", "")
                                val = val.replace("+/-", "")
                                val = val.split()
                                tabvaluePower[numerotableau][j] = val[0]
                                tabunitPower[numerotableau][j] = val[1]
                                j = j+1
                            else:
                                tabvaluePower[numerotableau][j] = None
                                tabunitPower[numerotableau][j] = None
                                # print("rien " + str(j))
                                j = j+1
                    else:
                        pass

                #Les champs dans tabPower2, Broche...
                for nom in tabnomPower2:
                    if nom == colonne.text:
                        nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                        element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                        numerotableau = tabnomPower2.index(colonne.text)
                        j=0
                        # print(colonne.text)
                        for value in element:
                            if value.text != "" and value.text != "-":
                                val = value.text.split()
                                tabvaluePower2[numerotableau][j] = val[0]
                                j = j+1
                            else:
                                tabvaluePower[numerotableau][j] = None
                                # print("rien " + str(j))
                                j = j+1
                    else:
                        pass

                #//////////////////////////////////////////////////////////////////////////////////////////////////////////
                #Les valeurs a récupérer nécessitant des modifications lors de leur prise

                if colonne.text == "Résistance":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        r = value.text.split()  
                        if len(r) > 1:
                            if r[0] != "Zero" and str(r[0]).isdigit() or re.findall('\d+\.\d+', r[0]):
                                tabOhms[i] = r[0]
                                tabOhmsUnite[i] = r[1]
                                i = i+1
                            else:
                                tabOhms[i] = None
                                tabOhmsUnite[i] = None
                                i = i+1
                        else:
                            tabOhms[i] = None
                            tabOhmsUnite[i] = None
                            i = i+1


                if colonne.text == 'Données de puissance':
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:   
                        r = value.text.split()
                        if len(r) == 2 or len(r) > 2: #Straight aura donc la valeur None
                            tabWatts[i] = r[0]
                            tabWattsUnite[i] = r[1]
                            i = i+1
                        else:
                            tabWatts[i] = None
                            tabWattsUnite[i] = None
                            i = i+1

                if colonne.text == 'Tolérance':
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    j=0
                    for value in element:
                        if value.text != "" and value.text != "-":
                            val = value.text.replace("pF", "")
                            val = val.replace("%", "")
                            val = val.split()
                            if len(val) == 1:
                                tabTole[j] = "".join(val)
                                j+=1
                            elif val[0] == "-" and len(val) == 2:
                                tabTole[j] = "-" + str(val[1])
                                j+=1
                            elif val[0] == "-":
                                tabTole[j] = "-" + str(val[1])
                                j+=1
                            elif len(tabTole)>0:
                                tabTole[j] = "".join(val[0])
                                j+=1
                            else:
                                tabTole[j] = None
                                j+=1
                        else:
                            tabTole[j] = None
                            j+=1

                if colonne.text == "Coefficient de température":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:    
                        r = value.text.split()
                        if len(r) > 2:
                            if r[0] != "-" and str(r[0]).isdigit() and r[0] != "0":
                                tabCoef[i] = r[0]
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i=i+1
                            elif r[0] == "-" and str(r[1]).isdigit():
                                tabCoef[i] = "-" + str(r[1])
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i = i+1

                            elif len(r)<5 and r[0] == "0" and str(r[0]).isdigit():
                                tabCoef[i] = str(r[0])
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i = i+1

                            elif len(r)>4 and r[0] == "0" and str(r[5]).isdigit():
                                tabCoef[i] = str(r[5])
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i = i+1
                            elif len(r)>5 and r[0] == "0" and str(r[6]).isdigit():
                                tabCoef[i] = str(r[6])
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i = i+1
                            elif len(r)>6 and r[0] == "0" and str(r[4]).isdigit():
                                tabCoef[i] = str(r[4])
                                if "C" in element.text:
                                    tabDegres[i] = "Celsius"
                                else:
                                    tabDegres[i] = "Kelvin"
                                i = i+1
                        else:    #Si aucune valeur
                            tabCoef[i] = None
                            tabDegres[i] = None
                            i = i+1

                if colonne.text == "Température de fonctionnement min.":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element: 
                        value = value.text.split()
                        if len(value) > 0:
                            if value[0] != "-":
                                tabTempsUtiDeb[i] = "".join(value[0])
                                i = i+1
                            elif value[0] == "-" and str(value[1]).isdigit():
                                tabTempsUtiDeb[i] = "".join("-" + str(value[1]))
                                i = i+1
                            else:
                                tabTempsUtiDeb[i] = "".join(value[1])
                                i = i+1
                        else:
                            tabTempsUtiDeb[i] = None
                            i = i+1

                if colonne.text == "Température de fonctionnement max.":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        value = value.text.split()
                        if len(value) > 0:
                            if value[0] != "+":
                                tabTempsUtiFin[i] = "".join(value[0])
                                i = i+1
                            elif value[0] == "+" and str(value[1]).isdigit():
                                tabTempsUtiFin[i] = "".join(value[1])
                                i = i+1
                            else:
                                tabTempsUtiFin[i] = None
                                i = i+1
                        else:
                            tabTempsUtiDeb[i] = None
                            i = i+1
                
                if colonne.text == "Nombre de tours":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        value = value.text.split()
                        if len(value) > 0:
                            if str(value[0]).isdigit() and len(value) == 1:
                                tabNbTour[i] = "".join(value[0])
                                i = i+1
                            elif str(value[0]).isdigit() and len(value) == 2:
                                tabNbTour[i] = "".join(value[1])
                                i = i+1
                            elif value[0] == 'Multiturn':
                                tabNbTour[i] = None
                                tabProd[i] = 'Multiturn'
                                i = i+1
                        else:
                            tabNbTour[i] = None
                            i = i+1

                if colonne.text == "Plage de résistance": #Aucune idée de comment gérer celui la (Kits de résistance)
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        if value.text != "":
                            tabOhms[i] = value.text
                            i+=1
                        else:
                            tabOhms[i] = None
                            i+=1

                if colonne.text == "Package/Boîte":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        if value.text != "-" or value.text != "":
                            tabCodeCaisse[i] = value.text
                            i+=1
                        else:
                            tabCodeCaisse[i] = None
                            i+=1

                if colonne.text == "Espacement des fils":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        if value.text != "-" and value.text != "":
                            val = value.text.split()
                            tabEspacementFils[i] = val[0]
                            i+=1
                        else:
                            tabEspacementFils[i] = None
                            i+=1

                if colonne.text == "Durée de vie":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        if value.text != "-" and value.text != "":
                            if "Cycle" in value.text:
                                value = value.text.split()
                                tabDureeVie[i] = value[0]
                                tabHoursCycles[i] = "Cycles"
                                i+=1
                            elif "Hour" in value.text:
                                value = value.text.split()
                                tabDureeVie[i] = value[0]
                                tabHoursCycles[i] = "Hours"
                                i+=1
                            elif len(value) == 1 :
                                value = value.text.split()
                                tabDureeVie[i] = value[0]
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


                if colonne.text == "Nombre de broches":
                    nb = i - start + 2 # +2 car il y a toujours 2 column hide xmall avant (Qte et Fiche technique)
                    element = driver.find_elements_by_xpath("//td[@class='column hide-xsmall']["+str(nb)+"]")
                    i=0
                    for value in element:
                        if value.text != "-" and value.text != "":
                            val = value.text.split()
                            tabPins[i] = val[0]
                            i+=1
                        else:
                            tabPins[i] = None
                            i+=1

            arriver = True

        except: #Probleme avec la récupération des données
        #Permet de passer la variable arriver, et donc de refresh ensuite
            print("Erreur lors de la collecte des données, veuillez patientez")

    else: #arriver veut dire l'on n'arrive pas inscrire les données, mais elle sont déja dans les tableaux.
        pass
            
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Ouverture et écriture des données dans le fichier CSV
        if arriver == True:
            
            for i in range(int(nbArticle)):
                with open(csvpath,'a',newline='') as unFichierCSV:
                    writer=csv.writer(unFichierCSV)
                    writer.writerow([tabRef[i], "Mouser",tabFab[i], tabDesc[i],categorieResistance,tabQtte[i],tabOhms[i], tabOhmsUnite[i],tabVolt[i], tabVoltUnite[i], None,None, tabVoltAC[i], tabUniteAC[i],tabVoltDC[i], tabUniteDC[i],tabCapacitance[i], tabCapacitanceUnite[i], tabDureeVie[i], tabHoursCycles[i],tabTole[i],None,None,tabSeries[i],tabPackage[i],tabTypePackage[i], tabRating[i], tabFeature[i],tabTempsUtiDeb[i],tabTempsUtiFin[i],tabCourantRejec[i],tabUniteCourantRejet[i],tabCourantNominal[i],tabUniteCourantNominal[i],tabCourantFuite[i],tabUniteCourantFuite[i],None,None,None,None,None,None,tabLength[i], tabWidth[i], tabDiametre[i], tabHeight[i], None,None,None,None,None,None,tabType[i], None, tabBoitier[i], None,None,None,tabDielectric[i],None,tabRaccord[i],tabTermination[i], None, tabManufacturerCode[i], None,tabPins[i],tabElement[i],tabProduct[i],tabEspacementFils[i],tabUniteEspacementFils[i],tabStyleFilSortie[i],tabBorneTerre[i],tabProfondeurEpaisseur[i],tabOrientation[i],tabCodeCaisse[i]])

                    insertdata = '''INSERT INTO Condensateur VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    data = (tabRef[i], "Mouser",tabFab[i], tabDesc[i],categorieResistance,tabQtte[i],tabOhms[i], tabOhmsUnite[i],tabVolt[i], tabVoltUnite[i], None,None, tabVoltAC[i], tabUniteAC[i],tabVoltDC[i], tabUniteDC[i],tabCapacitance[i], tabCapacitanceUnite[i], tabDureeVie[i], tabHoursCycles[i],tabTole[i],None,None,tabSeries[i],tabPackage[i],tabTypePackage[i], tabRating[i], tabFeature[i],tabTempsUtiDeb[i],tabTempsUtiFin[i],tabCourantRejec[i],tabUniteCourantRejet[i],tabCourantNominal[i],tabUniteCourantNominal[i],tabCourantFuite[i],tabUniteCourantFuite[i],None,None,None,None,None,None,tabLength[i], tabWidth[i], tabDiametre[i], tabHeight[i], None,None,None,None,None,None,tabType[i], None, tabBoitier[i], None,None,None,tabDielectric[i],None,tabRaccord[i],tabTermination[i], None, tabManufacturerCode[i], None,tabPins[i],tabElement[i],tabProduct[i],tabEspacementFils[i],tabUniteEspacementFils[i],tabStyleFilSortie[i],tabBorneTerre[i],tabProfondeurEpaisseur[i],tabOrientation[i],tabCodeCaisse[i])

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
                                    insertdata = '''UPDATE Condensateur SET '''+nom+''' = ? WHERE Reference = ? AND SiteWeb = ?;'''
                                    data = (tabUpdate[nbcat][i], tabRef[i], 'Mouser')
                                    cur.execute(insertdata, data)
                                    con.commit()
                                else:
                                    pass

                                if categorieResistance != None:
                                    insertdata = '''UPDATE Condensateur SET Categorie = ? WHERE Reference = ? AND SiteWeb = ?;'''
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
                print("page" + str(currentpage) + "fini !" + str(datetime.datetime.now() - begin_time))
                print(driver.current_url)
                arret = 0
                currentpage = currentpage + 1
                sleep(2)
                dataEnt = False
                arriver = False
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

    # # //////////////////////////////////////////////////////////////////////////////////////////////////////////

                    #Partie permettant le changement de categorie
                    sleep(3)

                    retour(driver)

                    incretyperes = driver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
                    if len(incretyperes) == 3:
                        onlyactive(driver)
                        typeresistance +=1
                        categorieResistance = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance.click()
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
                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance = catRes.text
                        if categorieResistance != "Matériel de condensateurs":
                            catRes.click()
                        else:
                            typeresistance +=2
                            catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                            categorieResistance = catRes.text
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

                    incretyperes = driver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
                    if len(incretyperes) == 3:
                        onlyactive(driver)
                        typeresistance +=1
                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance = catRes.text
                        if categorieResistance != "Matériel de condensateurs":
                            catRes.click()
                        else:
                            typeresistance +=2
                            catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                            categorieResistance = catRes.text
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

                    incretyperes = driver.find_elements_by_xpath('//div[@class="breadcrumb-container"]/div/nav/ol/li')
                    if len(incretyperes) == 3:
                        onlyactive(driver)
                        typeresistance +=1
                        catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                        categorieResistance = catRes.text
                        if categorieResistance != "Matériel de condensateurs":
                            catRes.click()
                        else:
                            typeresistance +=2
                            catRes = driver.find_element_by_xpath('//div[@class="types-of-category"]/div/ul/li['+str(typeresistance)+']/div/div[2]/a')
                            categorieResistance = catRes.text
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
            sleep(randint(300,600))
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