###
#
# Author: Sebastian Neef (@gehaxelt) from TU Berlin, Germany, 2022
#
###
import requests
import csv

r = requests.get("https://www.hs-kompass.de/kompass/xml/download/hs_liste.txt")
with open("hs_liste.csv", "w") as f:
	f.write(r.content.decode("latin-1"))

csvreader = csv.reader(open("hs_liste.csv"), delimiter='\t')
header = next(csvreader) # skip header

#['Hs-Nr.', 'Hochschulkurzname', 'Hochschulname', 'Hochschultyp', 'Trägerschaft', 
# 'Bundesland', 'Anzahl Studierende', 'Gründungsjahr', 'Promotionsrecht', 'Habilitationsrecht',
# 'Straße', 'Postleitzahl (Hausanschrift)', 'Ort (Hausanschrift)', 'Postfach', 'Postleitzahl (Postanschrift)',
# 'Ort (Postanschrift)', 'Telefonvorwahl', 'Telefon', 'Fax', 'Home Page',
# 'Mitglied HRK']

hskompass_heis = []

for line in csvreader:
	hei_name_short = line[1]
	hei_name_full = line[2]
	hei_type = line[3]
	hei_funding = line[4]
	hei_region = line[5]
	hei_website = line[19].replace("http://", "").replace("https://", "").split("/")[0].lower()

	if hei_type == 'Hochschulen eigenen Typs': 
		# TODO?
		pass
	elif hei_type == 'Fachhochschulen / HAW':
		hei_type = 'Fachhochschule'
	elif hei_type == 'Verwaltungshochschule':
		hei_type = 'Verwaltungsfachhochschulen'
	elif hei_type == 'Künstlerische Hochschulen':
		hei_type = 'Kunsthochschulen'
	elif hei_type == 'Universitäten':
		pass
	else:
		raise Exception("Unknown type")

	if hei_funding == 'kirchlich, staatlich anerkannt':
		hei_funding = 'Kirchlich'
	elif hei_funding == 'privat, staatlich anerkannt': 
		hei_funding = 'Privat'
	elif hei_funding == 'öffentlich-rechtlich':
		hei_funding = 'Land'
	else:
		raise Exception("Unknown funding")

	hskompass_heis.append([hei_name_full, hei_type, hei_region, hei_funding, hei_website])

csvwriter = csv.writer(open("hs_heis.csv", "w"))