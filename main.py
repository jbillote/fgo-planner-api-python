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

def class_icon_filename(rarity, class_id):
    if rarity == 3 or rarity == 2:
        rarity -= 1
    else:
        rarity = min(3, rarity)

    return f"{rarity}_{class_id}"
