import json

# loads the json file
def loadjson(): 
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "user.json")
    with open(file_path, "r") as file:
        return json.load(file)

#saves updates to a json file
def savejson(file, data):
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "user.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent = 4)