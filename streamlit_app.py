import streamlit as st
import requests
import os
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

API_KEY = "semaphore"  # must match the API_KEY env var

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="🚗 Car Price Predictor",
    page_icon="🚗",
    layout="centered",
)

# ── Session state defaults ────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ── Helper ────────────────────────────────────────────────────────────────────

def auth_headers():
    return {
        "token": st.session_state.token,
        "api-key": API_KEY,
    }


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/car.png", width=80)
    st.title("Car Price Predictor")
    st.caption("Powered by FastAPI + scikit-learn")
    st.divider()

    if st.session_state.token:
        st.success(f"Logged in as\n**{st.session_state.user_email}**")
        if st.button("🚪 Log out", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_email = None
            st.rerun()
    else:
        st.info("Sign up or log in to use the predictor.")


# ── Main tabs ─────────────────────────────────────────────────────────────────

if not st.session_state.token:
    tab_login, tab_signup = st.tabs(["🔑 Log In", "📝 Sign Up"])

    # ── Login tab ─────────────────────────────────────────────────────────────
    with tab_login:
        st.subheader("Welcome back!")
        with st.form("login_form"):
            email = st.text_input("Gmail / Email", placeholder="you@gmail.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Logging in…"):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/login",
                            json={"email": email, "password": password},
                            timeout=10,
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user_email = email
                            st.success("Logged in! 🎉")
                            st.rerun()
                        else:
                            st.error(resp.json().get("detail", "Login failed."))
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot reach the API. Is the server running?")

    # ── Signup tab ────────────────────────────────────────────────────────────
    with tab_signup:
        st.subheader("Create an account")
        with st.form("signup_form"):
            new_email = st.text_input("Gmail / Email", placeholder="you@gmail.com")
            new_pass = st.text_input(
                "Password",
                type="password",
                help="Minimum 8 characters",
            )
            new_pass2 = st.text_input("Confirm Password", type="password")
            submitted_s = st.form_submit_button("Sign Up", use_container_width=True)

        if submitted_s:
            if not new_email or not new_pass or not new_pass2:
                st.error("Please fill in all fields.")
            elif new_pass != new_pass2:
                st.error("Passwords do not match.")
            elif len(new_pass) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                with st.spinner("Creating account…"):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/signup",
                            json={"email": new_email, "password": new_pass},
                            timeout=10,
                        )
                        if resp.status_code == 201:
                            st.success(resp.json()["message"])
                            st.info("Go to the **Log In** tab to sign in.")
                        else:
                            st.error(resp.json().get("detail", "Sign-up failed."))
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot reach the API. Is the server running?")

# ── Prediction page (shown only when logged in) ───────────────────────────────
else:
    st.title("🚗 Car Price Predictor")
    st.write("Fill in the details below and hit **Predict** to get an estimated price.")
    st.divider()

    # ── Form ──────────────────────────────────────────────────────────────────
    with st.form("predict_form"):
        col1, col2 = st.columns(2)

        with col1:
            company = st.selectbox(
                "Car Company",
                [
                    "Maruti", "Hyundai", "Honda", "Toyota", "Ford",
                    "Tata", "Mahindra", "Volkswagen", "Renault",
                    "Kia", "MG", "Skoda", "Jeep", "Others",
                ],
            )
            year = st.number_input("Year of Manufacture", min_value=1990, max_value=2024, value=2018, step=1)
            owner = st.selectbox(
                "Owner Type",
                ["First", "Second", "Third", "Fourth & Above", "Test Drive Car"],
            )
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
            seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
            transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

        with col2:
            km_driven = st.number_input("Kilometres Driven", min_value=0, max_value=1_000_000, value=45000, step=1000)
            mileage_mpg = st.number_input("Mileage (mpg)", min_value=0.0, max_value=100.0, value=22.5, step=0.5)
            engine_cc = st.number_input("Engine (cc)", min_value=500, max_value=6000, value=1197, step=50)
            max_power_bhp = st.number_input("Max Power (bhp)", min_value=10.0, max_value=600.0, value=82.0, step=1.0)
            torque_nm = st.number_input("Torque (Nm)", min_value=0.0, max_value=1000.0, value=113.0, step=1.0)
            seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10], index=2)

        predict_btn = st.form_submit_button("🔍 Predict Price", use_container_width=True)

    # ── Prediction call ───────────────────────────────────────────────────────
    if predict_btn:
        payload = {
            "company": company,
            "year": int(year),
            "owner": owner,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "km_driven": float(km_driven),
            "mileage_mpg": float(mileage_mpg),
            "engine_cc": float(engine_cc),
            "max_power_bhp": float(max_power_bhp),
            "torque_nm": float(torque_nm),
            "seats": float(seats),
        }
        with st.spinner("Predicting…"):
            try:
                resp = requests.post(
                    f"{API_BASE}/predict",
                    json=payload,
                    headers=auth_headers(),
                    timeout=15,
                )
                if resp.status_code == 200:
                    price = resp.json()["predicted_price"]
                    st.success("Prediction complete!")
                    st.metric(
                        label="Estimated Selling Price (₹)",
                        value=f"₹ {price}",
                    )
                elif resp.status_code == 401:
                    st.error("Session expired. Please log in again.")
                    st.session_state.token = None
                    st.session_state.user_email = None
                    st.rerun()
                else:
                    st.error(resp.json().get("detail", "Prediction failed."))
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the API. Is the server running on port 8000?")

    # ── Tip section ───────────────────────────────────────────────────────────
    with st.expander("ℹ️ How does this work?"):
        st.markdown("""
        This app sends your car details to a **Gradient Boosting Regressor** model
        trained on thousands of Indian used-car listings.

        The model considers:
        - Brand, year, and transmission type
        - Fuel type and seller type
        - Kilometres driven and ownership history
        - Engine specs: CC, BHP, Torque, Mileage, Seats

        Predictions are cached in **Redis** so repeated queries are instant.
        """)
