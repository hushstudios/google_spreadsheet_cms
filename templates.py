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
    data = { "collages": []}
 

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
        imgObj["num_images"] = int(getCell("# of Images", rowIndex, values));
        imgObj["boxes"] = []; 
        
        #1
        box = {}
        box["width"] = int(getCell("Box 1 Width", rowIndex, values));
        box["height"] = int(getCell("Box 1 Height", rowIndex, values));
        box["xpos"] = int(getCell("Box 1 X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box 1 Y Pos", rowIndex, values)); 
        imgObj["boxes"].append(box);

        #2
        box = {}
        box["width"] = int(getCell("Box 2 Width", rowIndex, values));
        box["height"] = int(getCell("Box 2 Height", rowIndex, values));
        box["xpos"] = int(getCell("Box 2 X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box 2 Y Pos", rowIndex, values)); 
        imgObj["boxes"].append(box);

        #3
        box = {}
        box["width"] = int(getCell("Box 3 Width", rowIndex, values));
        box["height"] = int(getCell("Box 3 Height", rowIndex, values));
        box["xpos"] = int(getCell("Box 3 X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box 3 Y Pos", rowIndex, values)); 
        imgObj["boxes"].append(box);

        #4
        box = {}
        box["width"] = int(getCell("Box 4 Width", rowIndex, values));
        box["height"] = int(getCell("Box 4 Height", rowIndex, values));
        box["xpos"] = int(getCell("Box 4 X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box 4 Y Pos", rowIndex, values)); 
        imgObj["boxes"].append(box);

        if imgObj["num_images"] >= 5:
            #5
            box = {}
            box["width"] = int(getCell("Box 5 Width", rowIndex, values));
            box["height"] = int(getCell("Box 5 Height", rowIndex, values));
            box["xpos"] = int(getCell("Box 5 X Pos", rowIndex, values));
            box["ypos"] = int(getCell("Box 5 Y Pos", rowIndex, values));
            imgObj["boxes"].append(box); 

        if imgObj["num_images"] == 6:
            #6
            box = {}
            box["width"] = int(getCell("Box 6 Width", rowIndex, values));
            box["height"] = int(getCell("Box 6 Height", rowIndex, values));
            box["xpos"] = int(getCell("Box 6 X Pos", rowIndex, values));
            box["ypos"] = int(getCell("Box 6 Y Pos", rowIndex, values));
            imgObj["boxes"].append(box); 

        print imgObj["uid"]

        # Add this assets to the list
        data["collages"].append(imgObj)

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

