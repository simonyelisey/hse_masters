from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO, StringIO
from pydantic import BaseModel
import pickle
from ML.cars_prices_modeling.preparing_functions import *


app = FastAPI()

# target name
target = 'selling_price'
# category features encoder
ohe = pickle.load(open('ML/cars_prices_modeling/pickle_files/ohe.pkl', 'rb'))
# standard scaler
ss = pickle.load(open('ML/cars_prices_modeling/pickle_files/standardscaler.pkl', 'rb'))
# simple imputer
si = pickle.load(open('ML/cars_prices_modeling/pickle_files/simple_imputer.pkl', 'rb'))
# list of features names
with open('ML/cars_prices_modeling/pickle_files/features.pkl', 'rb') as f:
    features = pickle.load(f)
# predicting model
gs = pickle.load(open('ML/cars_prices_modeling/pickle_files/gs_best_estimator.pkl', 'rb'))


class Item(BaseModel):
    name: str
    year: int
    selling_price: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


@app.get('/')
async def root():
    return "Cars prices predicting service"


@app.post("/predict_item")
def predict_item(item: Item) -> float:
    # create dataframe from Item class
    data = pd.DataFrame(dict(item), index=[0])
    # preprocessing
    preprocessed_data = preprocess_data(data, target, treat_torque, extract_numbers, si, ss, ohe, features)
    # predicting
    prediction = np.exp(gs.predict(preprocessed_data)[0]).round(2)

    return prediction


@app.post("/predict_items")
def predict_items(csv_file: UploadFile = File(...)) -> File():
    # read the csv file
    contents = csv_file.file.read()
    buffer = BytesIO(contents)
    data = pd.read_csv(buffer)
    buffer.close()
    csv_file.file.close()

    # preprocessing
    preprocessed_data = preprocess_data(data, target, treat_torque, extract_numbers, si, ss, ohe, features)
    # predicting
    prediction = pd.Series(np.exp(gs.predict(preprocessed_data)).round(2), name='prediction')
    # concat prediction to original data
    data = pd.concat([data, prediction], axis=1)

    # save the csv
    stream = StringIO()
    data.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )
    response.headers["Content-Disposition"] = "attachment; filename=prediction.csv"

    return response
