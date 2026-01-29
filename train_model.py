import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ------------------------
# LOAD DATASET
# ------------------------
df = pd.read_csv("travel_dataset.csv")
df["Activities"] = df["Activities"].apply(lambda x: x.split(","))

# ------------------------
# FEATURES & TARGET
# ------------------------
X_cat = df[["Type","Season","TravelGroup","Duration","HealthCondition","Region"]]
X_num = df[["BudgetPerPerson","NumPeople"]]
y = df["Destination"]

# ------------------------
# ENCODING
# ------------------------
cat_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_cat_enc = cat_encoder.fit_transform(X_cat)

act_encoder = MultiLabelBinarizer()
X_act_enc = act_encoder.fit_transform(df["Activities"])

# ------------------------
# COMBINE FEATURES
# ------------------------
X = pd.concat([
    pd.DataFrame(X_cat_enc),
    pd.DataFrame(X_act_enc),
    X_num.reset_index(drop=True)
], axis=1)

# 🔥 FIX: Convert all column names to strings
X.columns = X.columns.astype(str)

# ------------------------
# SPLIT
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------
# TRAIN MODEL
# ------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ------------------------
# ACCURACY
# ------------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# ------------------------
# SAVE FILES
# ------------------------
pickle.dump(model, open("travel_model.pkl","wb"))
pickle.dump(cat_encoder, open("cat_encoder.pkl","wb"))
pickle.dump(act_encoder, open("activity_encoder.pkl","wb"))

print("Model and encoders saved successfully!")
