# get user  input and give prediction
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.dependencies import get_current_user, verify_api_key
from app.services.model_service import predict_car_price

router = APIRouter()

# Car Features
class CarFeatures(BaseModel):
    company: str
    year: int
    owner: str
    fuel: str
    seller_type: str
    transmission: str
    km_driven: float
    mileage_mpg: float
    engine_cc: float
    max_power_bhp: float
    torque_nm: float
    seats: float


@router.post('/predict')
def predict_price(car: CarFeatures, user=Depends(get_current_user), _ = Depends(verify_api_key)):
    # convert the car data from json to dict
    result = predict_car_price(car.model_dump())
    price = float(result['prediction'])
    return {"predicted_price": f"{price:,.2f}"}
