#Helper function

def Simplify(LevelData):
    LevelDataMinified = {
        "name" : "",
        "data": [],
        }
    LevelDataMinified["name"] = LevelData["name"]
    for Tile in LevelData["objects"]:
        LevelDataMinified["data"].append(
            {"name": Tile["name"],
             "x" : Tile["x"] / 10,
             "y" : Tile["y"] / 10,
             "flag" : Tile["flag"]}
            )   

    for GroundObj in LevelData["ground"]:
        LevelDataMinified["data"].append(
            {"name" : "Ground",
             "x" : GroundObj["x"] * 16 + 8,
             "y" : GroundObj["y"] * 16 + 8,
             "flag" : ""
                })
    

    return LevelDataMinified
