import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, KBinsDiscretizer, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

# Import local modules
from training.train_utils import DATA_FILE_PATH, MODEL_DIR, MODEL_PATH

# Load the dataset
df = (
    pd.read_csv(DATA_FILE_PATH)
      .drop_duplicates()
      .drop(columns=['name', 'model', 'edition'])
      .assign(
          company=lambda x: x['company'].where(
              x['company'].map(x['company'].value_counts()) > 100,
              'Others'
          )
      )
)

# Train Test Split
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define our Imputers and encoders
mean_spi = SimpleImputer(strategy='mean')
median_spi = SimpleImputer(strategy='median')
ohe = OneHotEncoder(drop='first', sparse_output=False)
ode = OrdinalEncoder(categories=[['Test Drive Car', 'Fourth & Above', 'Third', 'Second', 'First']])
kbin = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform') # Discretization
scaler = StandardScaler()


#Handele Numeric val
num_pipeline = Pipeline(steps=[
    ("median_spi", median_spi),
    ("scaler", StandardScaler())
])

torque_pipe = Pipeline(steps=[
    ("mean_spi", mean_spi),
    ("scaler", StandardScaler())
])

# Preprocession data using Column Transformer
preprocessor = ColumnTransformer(
    [
        ("other_num", num_pipeline,['km_driven', 'mileage_mpg', 'engine_cc', 'max_power_bhp','seats']),
        ("torque", torque_pipe, ['torque_nm']),
        ("ohe", ohe, ['fuel', 'transmission', 'seller_type', 'company']),
        ("ode", ode, ['owner']),
        ("kbin", kbin, ['year'])
    ]
)

# Train of Random Forest Regressor
rfReg = RandomForestRegressor(
    n_estimators=100,
    max_depth= 13,
    max_features= 0.5,
    max_samples= 1.0,
    bootstrap=True,
    random_state= 42
)

#Make pipeline of out model
rf_model = Pipeline(
    steps=[
        ('Preprocessing', preprocessor),
        ('model', rfReg)
    ]
)

# Train the model
rf_model.fit(X_train, y_train)


# Store the model
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(rf_model, MODEL_PATH)