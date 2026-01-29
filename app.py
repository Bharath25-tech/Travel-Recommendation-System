from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import json

app = Flask(__name__)

# ---------------------------
# Load trained model and encoders
model = pickle.load(open("travel_model.pkl", "rb"))
cat_encoder = pickle.load(open("cat_encoder.pkl", "rb"))
act_encoder = pickle.load(open("activity_encoder.pkl", "rb"))

# ---------------------------
# Load destinations data dynamically
with open("destinations.json", "r") as f:
    destination_data = json.load(f)

# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # 1 Get form data
    trip_type = request.form["type"]
    season = request.form["season"]
    group = request.form["group"]
    duration = request.form["duration"]
    health = request.form["health"]
    region = request.form["region"]
    budget = int(request.form["budget"])
    people = int(request.form["people"])
    activities = request.form.getlist("activities")

    # 2️ Prepare data for model
    cat_df = pd.DataFrame([[trip_type, season, group, duration, health, region]],
                          columns=["Type", "Season", "TravelGroup", "Duration", "HealthCondition", "Region"])
    cat_enc = cat_encoder.transform(cat_df)
    act_enc = act_encoder.transform([activities])
    num_df = pd.DataFrame([[budget, people]], columns=["BudgetPerPerson", "NumPeople"])
    X = pd.concat([pd.DataFrame(cat_enc), pd.DataFrame(act_enc), num_df], axis=1)
    X.columns = X.columns.astype(str)

    # 3️ Predict destination
    destination = model.predict(X)[0]

    # 4️ Get destination info dynamically
    destination_info = destination_data.get(destination, {})

    description = destination_info.get("description", "")
    rating = destination_info.get("rating", 4.0)
    attractions = destination_info.get("attractions", [])
    hotels = destination_info.get("hotels", [])
    similar = destination_info.get("similar_destinations", [])

    # 5️ Google / Map links
    google_links = [
        f"https://www.google.com/search?q={destination}+attractions",
        f"https://www.google.com/search?q={destination}+top+hotels"
    ]
    map_link = f"https://www.google.com/maps/search/{destination}"

    # 6️ Images
    image_folder = os.path.join("static", "images", destination)
    images = []
    if os.path.exists(image_folder):
        for img_file in os.listdir(image_folder):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                images.append(f"images/{destination}/{img_file}")

    # 7️ Render result page
    return render_template("result.html",
                           result=destination,
                           description=description,
                           rating=rating,
                           places=attractions,
                           hotels=hotels,
                           similar=similar,
                           google_links=google_links,
                           map_link=map_link,
                           images=images)

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
