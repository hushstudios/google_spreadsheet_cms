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
    data = { "images": []}
 

    # Download from Google Sheets
    # https://github.com/burnash/gspread
    # https://github.com/googleapis/oauth2client
    gsheet = GoogleAPI.GSheets(keyfile)
    

    # First, download lay out data tab by feeding the ("spreadsheet name", "spreadsheet tab name")
    objects = gsheet.download("ParkModern_Collage_Image_Tracker", "Layout Data") 
    values = objects.get_all_values()
    
    for rowIndex in range(1, len(values)):
        imgObj = {}
        imgObj["uid"] = (getCell("UID", rowIndex, values));
        imgObj["category"] = getCell("Category", rowIndex, values);
        imgObj["num_images"] = getCell("# of Images", rowIndex, values);
        
        #1
        imgObj["box1_width"] = getCell("Box 1 Width", rowIndex, values);
        imgObj["box1_height"] = getCell("Box 1 Height", rowIndex, values);
        imgObj["box1_xpos"] = (getCell("Box 1 X Pos", rowIndex, values));
        imgObj["box1_ypos"] = (getCell("Box 1 Y Pos", rowIndex, values)); 

        #2
        #3
        #4
        #5
        #6

        print imgObj["uid"]

        # Add this assets to the list
        data["images"].append(imgObj)

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

