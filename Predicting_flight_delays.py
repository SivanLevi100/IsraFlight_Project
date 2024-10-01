import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta


# Step 1: Create CSV file (we'll simulate this with a pandas DataFrame)
def create_flight_data():
    num_flights = 100
    current_date = datetime.now()
    data = {
        'FlightID': range(1, num_flights + 1),
        'Occupancy': np.random.choice(['full', 'partial', 'minimal'], num_flights, p=[0.4, 0.4, 0.2]),
        'PlaneNickname': np.random.choice(['Plane A', 'Plane B', 'Plane C'], num_flights),
        'DepartureTime': [current_date + timedelta(hours=np.random.randint(0, 168)) for _ in range(num_flights)],
        'DayOfWeek': np.random.randint(0, 7, num_flights),
        'DepartureLocation': np.random.choice(['TLV', 'JFK', 'LHR', 'CDG', 'FRA'], num_flights),
        'Delayed': np.random.choice([0, 1], num_flights, p=[0.6, 0.4])  # 30% chance of delay
    }
    df = pd.DataFrame(data)

    # Extract hour and convert to categorical
    df['DepartureHour'] = df['DepartureTime'].dt.hour
    df['DepartureDay'] = df['DepartureTime'].dt.dayofweek
    df.drop(columns=['DepartureTime'], inplace=True)

    df.to_csv('flight_data.csv', index=False)
    return df


# Step 2: Create and train random forest model
def train_model(df):
    features = ['Occupancy', 'PlaneNickname', 'DepartureHour', 'DayOfWeek', 'DepartureLocation']
    X = pd.get_dummies(df[features], columns=['Occupancy', 'PlaneNickname', 'DepartureLocation'])
    y = df['Delayed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")

    return model, X.columns


# Step 3: Save the trained model
def save_model(model, columns):
    joblib.dump(model, 'flight_delay_model.joblib')
    joblib.dump(columns, 'model_columns.joblib')


# Step 4: Create FastAPI service
app = FastAPI()


class FlightData(BaseModel):
    Occupancy: str
    PlaneNickname: str
    DepartureHour: int
    DayOfWeek: int  # 0 = Monday, 6 = Sunday
    DepartureLocation: str


@app.post("/predict")
def predict_delay(flight: FlightData):
    model = joblib.load('flight_delay_model.joblib')
    model_columns = joblib.load('model_columns.joblib')

    # Prepare input data
    input_data = {
        'Occupancy': flight.Occupancy,
        'PlaneNickname': flight.PlaneNickname,
        'DepartureHour': flight.DepartureHour,
        'DayOfWeek': flight.DayOfWeek,
        'DepartureLocation': flight.DepartureLocation,
    }

    input_df = pd.DataFrame([input_data])
    input_encoded = pd.get_dummies(input_df, columns=['Occupancy', 'PlaneNickname', 'DepartureLocation'])
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(input_encoded)
    probability = model.predict_proba(input_encoded)[0][1]  # Probability of delay

    return {
        "delay_prediction": "Delayed" if prediction[0] == 1 else "On Time",
        "delay_probability": round(probability * 100, 2)
    }


if __name__ == "__main__":
    # Run these steps once to prepare the model
    df = create_flight_data()
    model, columns = train_model(df)
    save_model(model, columns)

    # Then you can run the FastAPI server
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

# For API documentation, go to: http://localhost:8000/docs
