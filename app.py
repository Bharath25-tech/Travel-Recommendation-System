from flask import Flask, render_template, request, session
import pickle
import pandas as pd
import os
import json

app = Flask(__name__)
app.secret_key = "travelmate_secret"

# ---------------------------
# Load trained model & encoders
model = pickle.load(open("travel_model.pkl", "rb"))
cat_encoder = pickle.load(open("cat_encoder.pkl", "rb"))
act_encoder = pickle.load(open("activity_encoder.pkl", "rb"))

# ---------------------------
# Load destination info
with open("destinations.json", "r") as f:
    destination_data = json.load(f)

# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # -------- Get form inputs --------
    trip_type = request.form["type"]
    season = request.form["season"]
    group = request.form["group"]
    duration = request.form["duration"]
    health = request.form["health"]
    region = request.form["region"]
    budget = int(request.form["budget"])
    people = int(request.form["people"])
    activities = request.form.getlist("activities")

    # -------- Encode inputs --------
    cat_df = pd.DataFrame([[trip_type, season, group, duration, health, region]],
        columns=["Type","Season","TravelGroup","Duration","HealthCondition","Region"])

    cat_enc = cat_encoder.transform(cat_df)
    act_enc = act_encoder.transform([activities])

    num_df = pd.DataFrame([[budget, people]],
        columns=["BudgetPerPerson","NumPeople"])

    X = pd.concat([
        pd.DataFrame(cat_enc),
        pd.DataFrame(act_enc),
        num_df
    ], axis=1)

    X.columns = X.columns.astype(str)

    # -------- Predict probabilities --------
    probs = model.predict_proba(X)[0]
    classes = model.classes_

    top3_idx = probs.argsort()[-3:][::-1]
    top3_places = [classes[i] for i in top3_idx]

    results = []

    for dest in top3_places:

        info = destination_data.get(dest, {})

        avg_cost = info.get("avg_cost_per_person", 0)

        if budget >= avg_cost:
            budget_msg = "Fits your budget ✅"
        else:
            budget_msg = "May exceed your budget ⚠"

        # Images
        image_folder = os.path.join("static","images",dest)
        images = []
        if os.path.exists(image_folder):
            for img in os.listdir(image_folder):
                if img.lower().endswith((".jpg",".jpeg",".png")):
                    images.append(f"images/{dest}/{img}")

        results.append({
            "name": dest,
            "description": info.get("description",""),
            "rating": info.get("rating",4.0),
            "avg_cost": avg_cost,
            "budget_msg": budget_msg,
            "places": info.get("attractions",[]),
            "hotels": info.get("hotels",[]),
            "images": images,
            "map": f"https://www.google.com/maps/search/{dest}",
            "google_attr": f"https://www.google.com/search?q={dest}+attractions",
            "google_hotels": f"https://www.google.com/search?q={dest}+hotels"
        })

    # Save similar destinations
    session["similar_results"] = results[1:]

    return render_template("result.html", result=results[0])

# ---------------------------
@app.route("/similar")
def similar():
    sims = session.get("similar_results", [])
    return render_template("similar.html", results=sims)

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
