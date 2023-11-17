from flask import Flask, request
import requests

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/api/fgo/v1/servant", methods=["GET"])
def servant_search():
    if request.args.get("query") is None:
        return {
            "error": "Missing param"
        }, 400
    
    query = request.args.get("query")
    url = f"https://api.atlasacademy.io/nice/JP/servant/search?name={query}&lang=en"
    response = requests.get(url)
    data = response.json()

    results = []
    for s in data:
        results.append({
            "id": s["id"],
            "name": s["name"],
            "classIcon": f"https://static.atlasacademy.io/JP/ClassIcons/class{class_icon_filename(s["rarity"], s["classId"])}.png",
            "icon": s["extraAssets"]["faces"]["ascension"]["1"]
        })

    return results

@app.route("/api/fgo/v1/servant/<int:id>", methods=["GET"])
def get_servant_info(id):
    url = f"https://api.atlasacademy.io/nice/JP/servant/{id}?lang=en"
    response = requests.get(url)
    data = response.json()

    portraits = []
    portraits_response_keys = list(data["extraAssets"]["charaGraph"]["ascension"].keys())
    portraits_response_keys.sort()
    for k in portraits_response_keys:
        portraits.append(data["extraAssets"]["charaGraph"]["ascension"][k])

    skills = []
    for s in data["skills"]:
        skills.append({
            "name": s["name"],
            "icon": s["icon"]
        })

    appends = []
    for a in data["appendPassive"]:
        appends.append({
            "name": a["skill"]["name"],
            "icon": a["skill"]["icon"]
        })

    return {
        "id": data["id"],
        "name": data["name"],
        "classIcon": f"https://static.atlasacademy.io/JP/ClassIcons/class{class_icon_filename(data["rarity"], data["classId"])}.png",
        "icon": data["extraAssets"]["faces"]["ascension"]["1"],
        "portraits": portraits,
        "skills": skills,
        "appends": appends,
        "ascensionMaterials": process_materials(data["ascensionMaterials"]),
        "skillMaterials": process_materials(data["skillMaterials"]),
        "appendMaterials": process_materials(data["appendSkillMaterials"])
    }

def class_icon_filename(rarity, class_id):
    if rarity == 3 or rarity == 2:
        rarity -= 1
    else:
        rarity = min(3, rarity)

    return f"{rarity}_{class_id}"

def process_materials(materials):
    processed = []

    materials_keys = list(materials.keys())
    materials_keys.sort()

    for k in materials_keys:
        items = []
        for i in materials[k]["items"]:
            items.append({
                "id": i["item"]["id"],
                "name": i["item"]["name"],
                "icon": i["item"]["icon"],
                "amount": i["amount"]
            })
        processed.append({
            "materials": items,
            "qp": materials[k]["qp"]
        })
    
    return processed
