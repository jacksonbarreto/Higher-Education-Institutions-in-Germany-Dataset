###
#

#
###
import csv
import re
import itertools
from collections import Counter

FUNDING_MAP = {}
TYPE_MAP = {}
TYPE_MAP_ABBREV = {}
TYPE_MAP_ABBREV_ALT = {}
REGION_MAP = {}
TYPE_REGEX = re.compile(r'\((.*?)\)')
TYPE_REGEX_PREFIX = re.compile(r'(FH|TH|PH|(T|F)?(U))\s')

csvreader = csv.reader(open("hei-funding.csv"))
next(csvreader) # skip header

for line in csvreader:
	funding_id, funding_type = line
	FUNDING_MAP[funding_id] = funding_type

csvreader = csv.reader(open("hei-types.csv"))
next(csvreader) # skip header

for line in csvreader:
	type_id, type_name, type_abrrev1, type_abrrev2 = line
	TYPE_MAP[type_id] = {
		'name': type_name,
		'abbrev': type_abrrev1,
		'abbrev_alt': type_abrrev2
	}
	TYPE_MAP_ABBREV[type_abrrev1] = {
		'id': type_id,
		'name': type_name,
		'abbrev_alt': type_abrrev2
	}
	TYPE_MAP_ABBREV_ALT[type_abrrev2] = {
		'id': type_id,
		'name': type_name,
		'abbrev': type_abrrev1
	}

csvreader = csv.reader(open("region-signing+sortkey.csv"))
next(csvreader) # skip header

for line in csvreader:
	_, sortkey, region_name, region_abbrev = line
	REGION_MAP[int(sortkey)] = {
		'name': region_name,
		'abbrev': region_abbrev
	}

csvreader = csv.reader(open("heis.csv"))
next(csvreader) # skip header

csvwriter = csv.writer(open("heis-mapped.csv", "w"))
csvwriter.writerow(["HEI name", "Type", "Region", "Funding"])

region_counter = Counter()
type_counter = Counter()
funding_counter = Counter()

for line in csvreader:
	_,sortkey, name, funding_id = line
	name = name.strip()
	for k in ['Priv. ', 'Priv.-', 'Private ','Priv.', "Kirchl. ", "Kirchl.-"]:
		name = name.replace(k,"")

	try:
		region_name = REGION_MAP[int(sortkey)]['name']
		funding = FUNDING_MAP[funding_id]
		type_name_matches = TYPE_REGEX.findall(name)
		type_name_matches_prefix = list(itertools.chain(*TYPE_REGEX_PREFIX.findall(name))) # list(map(lambda x: x[0][0], TYPE_REGEX_PREFIX.findall(name)))
		type_matches = type_name_matches + type_name_matches_prefix
		if 'Berufsakademie'.lower() in name.lower():
			type_matches.append("BA")
		elif 'Universität'.lower() in name.lower():
			type_matches.append("U")
		elif 'Hochschule'.lower() in name.lower():
			type_matches.append("H")


		for  type_extracted in type_matches:
			type_extracted = type_extracted.strip()
			try:
				type_name = TYPE_MAP_ABBREV[type_extracted]['name']
				break
			except Exception as e:
				print("e1", e)
			try:
				type_name = TYPE_MAP_ABBREV_ALT[type_extracted]['name']
				break
			except Exception as e:
				print("e2", e)
		else:
			type_name = "Unknown"
		print("csv:", [name, type_name, region_name, funding])
		csvwriter.writerow([name, type_name, region_name, funding])

		type_counter.update([type_name])
		region_counter.update([region_name])
		funding_counter.update([funding])
	except Exception as e:
		print(e)
print(type_counter)
print(region_counter)
print(funding_counter)
