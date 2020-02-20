#!/usr/bin/python

import GoogleAPI
import json
import io
import sys
import os


# Helper for looking up cells by column name
def getCell(colName, rowIndex, values):
	return values[rowIndex][values[0].index(colName)]


def parseSheet(values, data, key):
	data[key] = []; 
	for rowIndex in range(1, len(values)):
		assetReady = (getCell("Asset Ready?", rowIndex, values))

		if assetReady == "TRUE": 
			imgObj = {}
			imgObj["number"] = int(getCell("Number", rowIndex, values)); 
			imgObj["portrait_file_name"] = (getCell("Portrait File Name", rowIndex, values));
			imgObj["landscape_file_name"] = (getCell("Landscape File Name", rowIndex, values));
			imgObj["image_type"] = getCell("Image Type", rowIndex, values);
			imgObj["collage_category"] = []
			collage_category = getCell("Collage Category", rowIndex, values);
			collage_categories = collage_category.split(",")
			imgObj["collage_category"] = collage_categories
			print (key + ": " + imgObj["portrait_file_name"])

			# Add this assets to the list
			data[key].append(imgObj)


def downloadData(keyfile, location):
	print "--- BEGIN RETRIEVING DATA ---"

	# Set up JSON
	data = {}
 

	# Download from Google Sheets
	# https://github.com/burnash/gspread
	# https://github.com/googleapis/oauth2client
	gsheet = GoogleAPI.GSheets(keyfile)
	

	# First, download each ollage tab by feeding the ("spreadsheet name", "spreadsheet tab name")
	objects = gsheet.download("ParkModern_CMS", "Park Life") 
	_values = objects.get_all_values()
	parseSheet(_values, data, "park_life")

	objects = gsheet.download("ParkModern_CMS", "Regeneration") 
	_values = objects.get_all_values()
	parseSheet(_values, data, "regeneration")
	
	objects = gsheet.download("ParkModern_CMS", "Fenton Whelan") 
	_values = objects.get_all_values()
	parseSheet(_values, data, "fenton")

	objects = gsheet.download("ParkModern_CMS", "Building Amenities") 
	_values = objects.get_all_values()
	parseSheet(_values, data, "amenities")

	#Second, download the list for each category
	objects = gsheet.download("ParkModern_CMS", "List") 
	values = objects.get_all_values(); 
	data["tags"] = {}; 
	data["tags"]["parklife"] = []
	data["tags"]["amenities"] = []
	data["tags"]["fenton"] = []
	data["tags"]["regeneration"] = []


	for rowIndex in range(1, len(values)):
		regen_value = (getCell("Regeneration", rowIndex, values))
		if len(regen_value): 
			data["tags"]["regeneration"].append(regen_value)

		parklife_value = (getCell("Park Life", rowIndex, values))
		if len(parklife_value): 
			data["tags"]["parklife"].append(parklife_value)

		amenities_value = (getCell("Building Amenities", rowIndex, values))
		if len(amenities_value): 
			data["tags"]["amenities"].append(amenities_value)

		fw_value = (getCell("Fenton Whelan", rowIndex, values))
		if len(fw_value): 
			data["tags"]["fenton"].append(fw_value)

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

