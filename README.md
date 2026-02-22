# 🚗 Car Price Prediction API

A machine learning-powered REST API built with **FastAPI** that predicts used car prices based on vehicle features. This project was built to explore how to integrate ML models with a production-ready API stack — including authentication, caching, monitoring, and containerization.

---

## 📁 Project Structure

```
Learning-FastAPI/
├── app/
│   ├── api/
│   │   ├── routes_auth.py        # Login & token generation
│   │   └── routes_predict.py     # Car price prediction endpoint
│   ├── cache/
│   │   └── redis_cache.py        # Redis caching logic
│   ├── core/
│   │   ├── config.py             # App settings & env variables
│   │   ├── dependencies.py       # JWT & API key auth dependencies
│   │   ├── exceptions.py         # Custom exception handlers
│   │   └── security.py           # JWT token creation & verification
│   ├── middleware/
│   │   └── logging_middleware.py # Request/response logging
│   ├── models/
│   │   └── model.joblib          # Trained ML model (serialized)
│   ├── services/
│   │   └── model_service.py      # Model loading & prediction logic
│   ├── utils/
│   │   └── logger.py             # Logger setup
│   └── main.py                   # FastAPI app entry point
├── data/
│   └── car-details.csv           # Training dataset
├── training/
│   ├── train_model.py            # Model training script
│   └── train_utils.py            # Training helper utilities
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── render.yml
└── requirements.txt
```

---

## ✨ Features

- **Car Price Prediction** — Accepts 12 vehicle features and returns an estimated price using a trained Gradient Boosting model.
- **JWT Authentication** — Login endpoint issues a JWT token required for prediction requests.
- **API Key Verification** — An additional layer of security on protected routes.
- **Redis Caching** — Prediction results are cached using a SHA-256 hash of the input to avoid redundant model inference.
- **Prometheus Monitoring** — Metrics are exposed at `/metrics` for scraping by Prometheus.
- **Grafana Dashboard** — Visualize metrics from Prometheus using a pre-configured Grafana service.
- **Logging Middleware** — Every request and response is logged via custom middleware.
- **Docker Support** — Fully containerized with Docker Compose for easy local setup.

---

## 🧠 Machine Learning Model

**Task:** Regression — predicting the selling price of used cars.

**Dataset:** `data/car-details.csv` — contains features like fuel type, transmission, mileage, engine specs, and more.

**Pipeline:**

The training pipeline (`training/train_model.py`) applies the following steps:

- Drops duplicates and irrelevant columns (`name`, `model`, `edition`)
- Groups rare car companies (frequency < 100) under `"Others"`
- Applies a `ColumnTransformer` with:
  - **Median imputation + StandardScaler** for numeric features
  - **Mean imputation + StandardScaler** for torque
  - **OneHotEncoder** for categorical features (`fuel`, `transmission`, `seller_type`, `company`)
  - **OrdinalEncoder** for `owner` (ordered: Test Drive → First → ... → Fourth & Above)
  - **KBinsDiscretizer** (10 bins) for `year`
- Final estimator: **Gradient Boosting Regressor** (`n_estimators=200`, `learning_rate=0.05`, `max_depth=5`)

The trained pipeline is serialized to `app/models/model.joblib` using `joblib`.

---

## 🔌 API Endpoints

### `POST /login`
Authenticate and get a JWT token.

**Request body:**
```json
{
  "username": "admin",
  "password": "admin"
}
```

**Response:**
```json
{
  "accessed_token": "<jwt_token>"
}
```

---

### `POST /predict`
Predict the price of a used car.

**Headers required:**
- `Authorization: Bearer <jwt_token>`
- `x-api-key: <your_api_key>`

**Request body:**
```json
{
  "company": "Maruti",
  "year": 2018,
  "owner": "First",
  "fuel": "Petrol",
  "seller_type": "Individual",
  "transmission": "Manual",
  "km_driven": 45000,
  "mileage_mpg": 22.5,
  "engine_cc": 1197,
  "max_power_bhp": 82,
  "torque_nm": 113,
  "seats": 5
}
```

**Response:**
```json
{
  "predicted_price": "450,000.00"
}
```

---

## ⚙️ Setup & Running

### Prerequisites
- Docker & Docker Compose installed
- Python 3.10+ (for local development)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Learning-FastAPI
```

### 2. Configure environment variables
Create a `.env` file in the project root:
```env
API_KEY=your_api_key_here
JWT_SECRET_KEY=your_secret_key_here
REDIS_URL=redis://localhost:6379
ENV=development
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

This starts four services:

| Service    | Port | Description                  |
|------------|------|------------------------------|
| API        | 8000 | FastAPI application          |
| Redis      | 6379 | Prediction result cache      |
| Prometheus | 9090 | Metrics collection           |
| Grafana    | 3000 | Metrics visualization        |

### 4. Access the interactive API docs
Open your browser at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🏋️ Train the Model (Optional)

If you want to retrain the model from scratch:

```bash
pip install -r requirements.txt
python -m training.train_model
```

This will overwrite `app/models/model.joblib` with the newly trained model.

---

## 📦 Dependencies

| Package                          | Purpose                        |
|----------------------------------|--------------------------------|
| `fastapi`                        | Web framework                  |
| `uvicorn`                        | ASGI server                    |
| `scikit-learn`                   | ML model training & inference  |
| `joblib`                         | Model serialization            |
| `pandas`, `numpy`                | Data processing                |
| `redis`                          | Prediction caching             |
| `python-jose`                    | JWT token handling             |
| `python-dotenv`                  | Environment variable loading   |
| `prometheus-fastapi-instrumentator` | Metrics exposure            |

---

## 📈 Monitoring

Prometheus scrapes metrics from `/metrics` every 15 seconds (configured in `prometheus.yml`). You can then connect Grafana to Prometheus at `http://prometheus:9090` to build dashboards tracking request counts, latency, and error rates.

---

## 🚀 Deployment

A `render.yml` file is included for one-click deployment on [Render](https://render.com).

---

## 🔮 Future Improvements

- Integrate a real database (e.g., SQLite/PostgreSQL) for user management
- Replace hardcoded admin credentials with a proper user registration flow
- Add model versioning and A/B testing support
- Write unit and integration tests