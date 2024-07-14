from flask import Flask
from flask import request
import os
import json
import uuid
import base64

def is_float(element):
    #If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Server Operational</p>"

@app.route("/signup", methods = ['POST'])
def signup():
    if request.method == 'POST':
        print("recived signup call")
        data = request.get_json()
        print(data["email"])
        print(data["username"])
        print(data["password"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        if ((data["username"] in same_name_dirs) == False):
            os.mkdir("./users/"+data["type"]+"/" + data["username"])
            print("made " + "./users/"+data["type"]+"/" + data["username"])
            def_json_data = {
                "authtoken": "",
                "password": data["password"],
                "classes": []
            }
            def_json_ser = json.dumps(def_json_data, indent=4)

            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "w") as outfile:
                outfile.write(def_json_ser)
                return "True"
            # make file containing authtoken and classes
        else:
            return "False"
    else:
        return "POST requests only"
@app.route("/login", methods = ['POST'])
def login():
    if request.method == 'POST':
        print("recived login call")
        data = request.get_json()
        print(data["username"])
        print(data["password"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        print(os.listdir("./users/" + data["type"]))
        print("./users/" + data["type"])
        print(same_name_dirs)
        if ((data["username"] in same_name_dirs) == True):
            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "r") as outfile:
                user_data = json.load(outfile)
                if user_data["password"] == data["password"]:
                    authtoken = uuid.uuid4().hex
                    with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "w") as outfile:
                        user_data["authtoken"] = authtoken
                        def_json_ser = json.dumps(user_data, indent=4)
                        outfile.write(def_json_ser)
                        return authtoken
                else:
                    return "Incorrect Password"
        else:
            return "Username Does Not Exist"
    else:
        return "POST requests only"

@app.route("/classes", methods = ['POST'])
def classes():
    if request.method == 'POST':
        print("recived classes call")
        data = request.get_json()
        print(data["username"])
        print(data["authtoken"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        if ((data["username"] in same_name_dirs) == True):
            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "r") as outfile:
                user_data = json.load(outfile)
                if user_data["authtoken"] == data["authtoken"]:
                    classes_data = []
                    for clas in user_data["classes"]:
                        outfile = open(f'./classes/{clas}/0', "r")
                        class_name = outfile.read()
                        class_id = clas
                        class_image = f"/classes/{clas}/image.png"
                        clasio = [class_name, class_id, class_image]
                        classes_data.append(clasio)
                    return classes_data

                        
                else:
                    return "Incorrect Authtoken"
        else:
            return "Username Does Not Exist"
    else:
        return "POST requests only"

@app.route("/addclasses", methods=['POST'])
def addclasses():
    if request.method == "POST":
        print("recived classes call")
        data = request.get_json()
        print(data["username"])
        print(data["authtoken"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        if ((data["username"] in same_name_dirs) == True):
            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "r") as outfile:
                user_data = json.load(outfile)
                if user_data["authtoken"] == data["authtoken"]:
                    if data["type"] == "teachers":
                        classtoken = uuid.uuid4().hex
                        os.mkdir("./classes/" + classtoken)
                        with open("./classes/" + classtoken + "/" + "0", 'w') as outfoil:
                            outfoil.write(data["name"])
                        image = base64.b64decode(data["image"], validate=True)
                        print(image)
                        with open(f'./classes/{classtoken}/image.png', "wb") as f:
                            f.write(image)
                            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "w") as outfile:
                                user_data["classes"].append(classtoken)
                                def_json_ser = json.dumps(user_data, indent=4)
                                outfile.write(def_json_ser)
                            for student in data["students"]:
                                with open(f'./users/students/{student}/data.json', "w") as outfile:
                                    user_data["classes"].append(classtoken)
                                    def_json_ser = json.dumps(user_data, indent=4)
                                    outfile.write(def_json_ser)
                                    return "True"
                    else:
                        return "User is not a Teacher"
                else:
                    return "Authtoken is invalid"
        else:
            return "Username Not Found"

@app.route("/clas", methods = ['POST'])
def clas():
    if request.method == 'POST':
        print("recived clas call")
        data = request.get_json()
        print(data["username"])
        print(data["authtoken"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        if ((data["username"] in same_name_dirs) == True):
            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "r") as outfile:
                user_data = json.load(outfile)
                if user_data["authtoken"] == data["authtoken"]:
                    same_name_dirs = [name for name in os.listdir("./classes/" + data["classtoken"]) if is_float(name.split(".")[0])]
                    clas_data = []
                    for assignment in same_name_dirs:
                        if assignment == "0" or assignment == "image.png":
                            continue
                        if assignment.split(".")[1] == "mp4":
                            clas_data.append(f'/classes/{data["classtoken"]}/{assignment}')
                        elif assignment.split(".")[1] == "json":
                            with open(f'./classes/{data["classtoken"]}/{assignment}') as jsony:
                                quiz_data = json.load(jsony)
                                clas_data.append(quiz_data)
                    return clas_data
                else:
                    return "Authtoken is invalid"
        else:
            return "Username Not Found"
    else:
        return "POST requests only"

@app.route("/editclas", methods = ['POST'])
def editclas():
    if request.method == 'POST':
        print("recived editclas call")
        data = request.get_json()
        if data["type"] == "students":
            return "Only Teachers Can Edit Classes"
        print(data["username"])
        print(data["authtoken"])
        print(data["type"])
        same_name_dirs = [name for name in os.listdir("./users/" + data["type"]) if os.path.isdir("./users/" + data["type"] + "/" + name)]
        if ((data["username"] in same_name_dirs) == True):
            with open("./users/"+data["type"]+"/" + data["username"] + "/data.json", "r") as outfile:
                user_data = json.load(outfile)
                if user_data["authtoken"] == data["authtoken"]:
                    # start editing class
                    same_name_dirs = [name for name in os.listdir("./classes/" + data["classtoken"]) if is_float(name.split(".")[0])]
                    if data["change"] == "delete":
                        index = int(data["num"])
                        if (index > len(same_name_dirs)):
                            return "Index Too Large"
                        to_be_deleted_name = same_name_dirs[index]
                        os.remove(f'./classes/{data["classtoken"]}/{to_be_deleted_name}')
                        # change numbering for elements after
                        for i in range(index+1, len(same_name_dirs)):
                            os.rename(f'./classes/{data["classtoken"]}/{same_name_dirs[i]}', f'./classes/{data["classtoken"]}/{str(int(same_name_dirs[i].split(".")[0])-1)}.{same_name_dirs[i].split(".")[1]}')
                        return "Assignment Deleted"
                    if data["change"] == "add":
                        index = int(data["num"])
                        if data["changetype"] == "video":
                            # do video stuff
                            return "Video Uploaded"
                        elif data["changetype"] == "quiz":
                            for i in range(index+1, len(same_name_dirs)):
                                os.rename(f'./classes/{data["classtoken"]}/{same_name_dirs[i]}', f'./classes/{data["classtoken"]}/{str(int(same_name_dirs[i].split(".")[0])+1)}.{same_name_dirs[i].split(".")[1]}')
                            new_filename = f'./classes/{data["classtoken"]}/{data["num"]}.json'
                            jsoned_data = json.dumps(data["changedata"])
                            with open(new_filename, "w") as new_assignment:
                                new_assignment.write(jsoned_data)
                            return "Quiz Added"
                else:
                    return "Authtoken is invalid"
        else:
            return "Username Not Found"
    else:
        return "POST requests only"

@app.route("/getvid", methods = ['POST'])
def getvid():
    return "<p>Server Operational</p>"

@app.route("/interaction", methods = ['POST'])
def interaction():
    return "<p>Server Operational</p>"

app.run(debug=True)