#!/usr/bin/python

import GoogleAPI
import json
import io
import sys
import os


# Helper for looking up cells by column name
def getCell(colName, rowIndex, values):
	return values[rowIndex][values[0].index(colName)]


def downloadData(keyfile, location):
	print "--- BEGIN RETRIEVING DATA ---"

	# Set up JSON
	data = {}
	data["floors"] = {};
	data["asset_ids"] = [];

	# Download from Google Sheets
	# https://github.com/burnash/gspread
	# https://github.com/googleapis/oauth2client
	gsheet = GoogleAPI.GSheets(keyfile)


	#Download floor plates
	objects = gsheet.download("ParkModern_CMS", "Floorplates") 
	values = objects.get_all_values(); 

	for rowIndex in range(1, len(values)):
		level = getCell("Floor", rowIndex, values); 
		data["floors"][level] = {}; 
		data["floors"][level]["svgs"] = getCell("Floorplate SVG", rowIndex, values)
		data["floors"][level]["apartments"] = []; 

	# download each apartment tab by feeding the ("spreadsheet name", "spreadsheet tab name")
	objects = gsheet.download("ParkModern_CMS", "Apartment Overview") 
	values = objects.get_all_values();

	for rowIndex in range(1, len(values)):
		aptLevel = getCell("Level", rowIndex, values)
		aptObj = {}
		aptObj["number"] = getCell("Apartment #", rowIndex, values)
		aptObj["unit"] = getCell("Unit #", rowIndex, values)
		aptObj["area"] = getCell("Area", rowIndex, values)
		aptObj["terraces"] = getCell("Terraces", rowIndex, values)
		aptObj["bedrooms"] = getCell("Bedrooms", rowIndex, values)
		aptObj["bedrooms"] = getCell("Bedroom Strings", rowIndex, values)
		aptObj["image1"] = getCell("Image 1", rowIndex, values)
		aptObj["image2"] = getCell("Image 3", rowIndex, values)
		data["floors"][aptLevel]["apartments"].append(aptObj) 

	# Write to file
	with io.open(location, 'w+', encoding='utf8') as json_file:
		data = json.dumps(data, indent=4, ensure_ascii=False)
		json_file.write(unicode(data))

	print "--- FINISHED RETRIEVING DATA ---"

if __name__ == "__main__":

	print(sys.argv)
	if len(sys.argv) != 3:
		print "usage: <path/to/api/keyfile> <path/to/downloaded/json>"
		exit()
	elif os.path.exists(sys.argv[1]):
		downloadData(sys.argv[1], sys.argv[2])
	else:
		print "ERROR: keyfile arg is not valid path!"
		exit()
