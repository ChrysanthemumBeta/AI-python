#Bulk Save
import os, json, Helper

Data = os.listdir("Data")
SimplifiedData = []

#Simplify
for file in Data:
    with open("Data\\" + file, "r") as f:
        fileData = json.load(f)
        SimplifiedData.append(Helper.Simplify(fileData))

#Convert to json
for data in SimplifiedData:
    json_data = json.dumps(data)
    with open("Training\\" + data["name"] + ".json", "w") as jsonFile:
        jsonFile.write(json_data)
