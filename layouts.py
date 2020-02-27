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
    objects = gsheet.download("ParkModern_CMS", "Layouts") 
    values = objects.get_all_values()
    
    for rowIndex in range(1, len(values)):
        imgObj = {}
        imgObj["uid"] = (getCell("UID", rowIndex, values));
        imgObj["num_images"] = int(getCell("# of Images", rowIndex, values));
        imgObj["boxes"] = []; 
        
        #1
        box = {}
        box["xpos"] = int(getCell("Box A X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box A Y Pos", rowIndex, values)); 
        box["type"] = (getCell("Box A Type", rowIndex, values));
        box["animation"] = (getCell("Box A Animation", rowIndex, values));
        box["order"] = "a"; 
        imgObj["boxes"].append(box);

        #2
        box = {}
        box["xpos"] = int(getCell("Box B X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box B Y Pos", rowIndex, values)); 
        box["type"] = (getCell("Box B Type", rowIndex, values));
        box["animation"] = (getCell("Box B Animation", rowIndex, values));
        box["order"] = "b"
        imgObj["boxes"].append(box);

        #3
        box = {}
        box["xpos"] = int(getCell("Box C X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box C Y Pos", rowIndex, values));
        box["type"] = (getCell("Box C Type", rowIndex, values));
        box["animation"] = (getCell("Box C Animation", rowIndex, values)); 
        box["order"] = "c"
        imgObj["boxes"].append(box);

        #4
        box = {}
        box["xpos"] = int(getCell("Box D X Pos", rowIndex, values));
        box["ypos"] = int(getCell("Box D Y Pos", rowIndex, values));
        box["type"] = (getCell("Box D Type", rowIndex, values));
        box["animation"] = (getCell("Box D Animation", rowIndex, values));
        box["order"] = "d"
        imgObj["boxes"].append(box);

        if imgObj["num_images"] >= 5:
            #5
            box = {}
            box["xpos"] = int(getCell("Box E X Pos", rowIndex, values));
            box["ypos"] = int(getCell("Box E Y Pos", rowIndex, values));
            box["type"] = (getCell("Box E Type", rowIndex, values));
            box["animation"] = (getCell("Box E Animation", rowIndex, values));
            box["order"] = "e"
            imgObj["boxes"].append(box); 

        if imgObj["num_images"] == 6:
            #6
            box = {}
            box["xpos"] = int(getCell("Box F X Pos", rowIndex, values));
            box["ypos"] = int(getCell("Box F Y Pos", rowIndex, values));
            box["type"] = (getCell("Box F Type", rowIndex, values));
            box["animation"] = (getCell("Box F Animation", rowIndex, values)); 
            box["order"] = "f"
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

