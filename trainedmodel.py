import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

print("Connecting to MySQL to fetch training data...")

# 1. Connect to your MySQL database using your exact schema
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sonoffarmer",  # <-- Put your actual MySQL root password here
    database="omniintel_db"
)

# 2. Query data using your exact table ('shipments') and columns
query = """
    SELECT shipping_cost, delivery_time_days, delay_status 
    FROM shipments
"""
df = pd.read_sql(query, conn)
conn.close()

print(f"Data fetched successfully! Shape: {df.shape}")

# 3. Define features (X) and target (y)
X = df[['shipping_cost', 'delivery_time_days']]
y = df['delay_status']

# 4. Train/Test Split & Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Save the trained model artifact
model_filename = "delay_model.pkl"
with open(model_filename, "wb") as f:
    pickle.dump(model, f)

print(f"Model trained and saved successfully as '{model_filename}'!")