# Load the ML Model and Make the prediction with Redis Cashing
import joblib
import hashlib
import json
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction

model = joblib.load(settings.MODEL_PATH)

# We get the data from user in json and convert it to python dict
# So data: dict
def predict_car_price(data: dict):
    """
    # comibe the values of features as key
    # json.dumps - convert data to json string
    # sort-keys - use sorted to avoid mismatch values

    cache_key = json.dumps(data, sort_keys=True)
    """
    # Best practice
    cache_key = hashlib.sha256(
        json.dumps(data, sort_keys= True).encode()
    ).hexdigest()
    


    cached = get_cached_prediction(cache_key)
    if cached:
        return cached
    
    # our model is trained on dataframe so converting to df
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)[0] # for getting a scaler val
    
    #set the cache
    # Convert to dict format 
    result = {'prediction': float(prediction)}
    set_cached_prediction(cache_key, result)

    return result
