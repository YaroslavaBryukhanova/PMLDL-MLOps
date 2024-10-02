from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = FastAPI()

with open("../../../models/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../../datasets/encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

with open("../../datasets/object_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("../../datasets/label_scaler.pkl", "rb") as f:
    label_scaler = pickle.load(f)


class Item(BaseModel):
    Company: str
    Product: str
    TypeName: str
    Inches: float
    ScreenResolution: str
    CPU_Company: str
    CPU_Type: str
    CPU_Frequency: float
    RAM: str
    Memory: str
    GPU_Company: str
    GPU_Type: str
    OpSys: str
    Weight: float

class Prediction(BaseModel):
    Price: float

@app.post("/predict", response_model=Prediction)
def predict(item: Item):
    
    item_dict = item.dict()

    for col, encoder in encoders.items():
        item_dict[col] = int(encoder.transform([str(item_dict[col])])[0])

    data = np.array([item_dict['Company'], item_dict['Product'], item_dict['TypeName'], item_dict['Inches'],
             item_dict['ScreenResolution'], item_dict['CPU_Company'], item_dict['CPU_Type'],
             item_dict['CPU_Frequency'], item_dict['RAM'], item_dict['Memory'], item_dict['GPU_Company'],
             item_dict['GPU_Type'], item_dict['OpSys'], item_dict['Weight']])

    data = data.reshape(1, -1)

    data = scaler.transform(data)

    print(data)

    prediction = model.predict(data)

    prediction = label_scaler.inverse_transform(prediction.reshape(-1, 1))

    print(prediction)

    return Prediction(Price=prediction[0])

    
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI model prediction service!"}