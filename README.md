# 🚗 Car Price Prediction API

A machine learning-powered REST API built with **FastAPI** that predicts used car prices based on vehicle features. Built to learn how to integrate ML models into a production-ready stack — covering email/password auth with SQLite, Redis caching, Prometheus monitoring, Docker, a Streamlit frontend, and deployment on Render.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| 🖥️ Streamlit UI | https://car-price-prediction-ui-47e7.onrender.com |
| 📄 API Docs (Swagger) | https://learning-fastapi-dmyo.onrender.com/docs |

> ⚠️ Hosted on Render's free tier — the first request after inactivity may take ~50 seconds to wake up.

---

## 📁 Project Structure

```
Learning-FastAPI/
├── app/
│   ├── api/
│   │   ├── routes_auth.py        # Signup & login endpoints
│   │   └── routes_predict.py     # Car price prediction endpoint
│   ├── cache/
│   │   └── redis_cache.py        # Redis caching logic
│   ├── core/
│   │   ├── config.py             # App settings & env variables
│   │   ├── dependencies.py       # JWT & API key auth dependencies
│   │   ├── exceptions.py         # Custom exception handlers
│   │   └── security.py           # JWT + bcrypt password hashing
│   ├── db/
│   │   └── database.py           # SQLite setup & user CRUD
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
│   └── train_utils.py            # Path constants & helpers
├── streamlit_app.py              # Streamlit frontend UI
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── pyproject.toml                # Project metadata & deps (uv)
├── render.yml                    # Render deployment config
└── requirements.txt
```

---

## ✨ Features

- **Car Price Prediction** — Accepts 12 vehicle features and returns an estimated price using a trained Gradient Boosting model.
- **Email Sign-Up & Login** — Register with any email and password; credentials stored securely in SQLite with bcrypt hashing.
- **JWT Authentication** — Login returns a JWT token required for all prediction requests.
- **API Key Verification** — An additional security layer on all protected routes.
- **SQLite Database** — Lightweight file-based user store, zero external DB setup needed locally.
- **Redis Caching** — Prediction results cached using SHA-256 hash of input to skip redundant inference.
- **Prometheus + Grafana** — Metrics exposed at `/metrics` and visualized via Grafana.
- **Logging Middleware** — Every request and response automatically logged.
- **Streamlit Frontend** — Clean web UI to sign up, log in, and get predictions without touching the API directly.
- **Docker Support** — Fully containerized with Docker Compose.
- **Deployed on Render** — Both the API and Streamlit UI live on Render's free tier.

---

## 🧠 Machine Learning Model

**Task:** Regression — predicting the selling price of used cars.

**Dataset:** `data/car-details.csv`

**Pipeline:**

- Drops duplicates and irrelevant columns (`name`, `model`, `edition`)
- Groups rare car companies (frequency < 100) under `"Others"`
- `ColumnTransformer` with:
  - **Median imputation + StandardScaler** for numeric features (`km_driven`, `mileage_mpg`, `engine_cc`, `max_power_bhp`, `seats`)
  - **Mean imputation + StandardScaler** for `torque_nm`
  - **OneHotEncoder** for `fuel`, `transmission`, `seller_type`, `company`
  - **OrdinalEncoder** for `owner` (Test Drive → First → Second → Third → Fourth & Above)
  - **KBinsDiscretizer** (10 bins, uniform) for `year`
- Estimator: **Gradient Boosting Regressor** (`n_estimators=200`, `learning_rate=0.05`, `max_depth=5`)

Serialized to `app/models/model.joblib` via `joblib`.

---

## 🔌 API Endpoints

### `POST /signup`
Register a new account.

**Request body:**
```json
{
  "email": "you@gmail.com",
  "password": "yourpassword"
}
```

**Response (201):**
```json
{
  "message": "Account created for you@gmail.com. You can now log in."
}
```

---

### `POST /login`
Authenticate and receive a JWT token.

**Request body:**
```json
{
  "email": "you@gmail.com",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

### `POST /predict`
Predict the selling price of a used car.

**Headers required:**
- `token: <jwt_token>`
- `api-key: <your_api_key>`

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

## ⚙️ Setup & Running Locally

### Prerequisites
- **Python 3.11** (pinned via `.python-version`)
- **Docker** (for Redis)
- **`uv`** (recommended) — [install here](https://github.com/astral-sh/uv)

### 1. Clone the repository
```bash
git clone https://github.com/sema-phore/Learning-FastAPI.git
cd Learning-FastAPI
```

### 2. Create a `.env` file
```env
API_KEY=semaphore
JWT_SECRET_KEY=your_secret_key_here
REDIS_URL=redis://localhost:6379
ENV=development
DB_PATH=app/db/users.db
```

### 3. Start Redis
```bash
docker run -d -p 6379:6379 redis:alpine
```

### 4a. Run with `uv` (recommended)
```bash
# Terminal 1 — API
uv sync
uv run uvicorn app.main:app --reload

# Terminal 2 — Streamlit UI
uv run streamlit run streamlit_app.py
```

### 4b. Run with `pip`
```bash
pip install -r requirements.txt

# Terminal 1
uvicorn app.main:app --reload

# Terminal 2
streamlit run streamlit_app.py
```

### 4c. Run everything with Docker Compose
```bash
docker-compose up --build
```

| Service    | Port | Description           |
|------------|------|-----------------------|
| API        | 8000 | FastAPI application   |
| Streamlit  | 8501 | Frontend UI           |
| Redis      | 6379 | Prediction cache      |
| Prometheus | 9090 | Metrics collection    |
| Grafana    | 3000 | Metrics visualization |

### 5. Open the app
- **Streamlit UI:** http://localhost:8501
- **Swagger docs:** http://localhost:8000/docs

---

## 🏋️ Train the Model (Optional)

```bash
python -m training.train_model
```

Overwrites `app/models/model.joblib` with a freshly trained model.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `scikit-learn` | ML training & inference |
| `joblib` | Model serialization |
| `pandas`, `numpy` | Data processing |
| `bcrypt` | Password hashing |
| `python-jose` | JWT token handling |
| `python-dotenv` | Environment variable loading |
| `redis` | Prediction caching |
| `prometheus-fastapi-instrumentator` | Metrics exposure |
| `streamlit` | Frontend UI |
| `requests` | HTTP client (used by Streamlit) |

---

## 📈 Monitoring

Prometheus scrapes `/metrics` every 15 seconds (configured in `prometheus.yml`). Connect Grafana to Prometheus at `http://prometheus:9090` to visualize request rate, latency, and error rates.

---

## 🚀 Deployment (Render)

Both services are deployed on [Render](https://render.com) via `render.yml` with auto-deploy on every push to `main`.

**Environment variables set on Render:**

| Key | Value |
|-----|-------|
| `API_KEY` | `semaphore` |
| `JWT_SECRET_KEY` | your secret |
| `REDIS_URL` | Render Redis internal URL |
| `ENV` | `production` |
| `DB_PATH` | `app/db/users.db` |

> ⚠️ **Note:** Render's free tier has an ephemeral filesystem — the SQLite database resets on every redeploy. For persistent user storage in production, switch to Render's PostgreSQL.

---

## 🔮 Future Improvements

- Email verification on sign-up
- Password reset via email
- Persistent user storage with PostgreSQL
- User dashboard with prediction history
- Model versioning and A/B testing
- Unit and integration tests