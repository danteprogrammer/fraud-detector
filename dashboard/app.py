import streamlit as st
import requests

st.set_page_config(page_title="Fraud Detection", page_icon="🛡️", layout="centered")

st.title("🛡️ Detector de Transacciones Fraudulentas")
st.markdown("Demo que consume la **Fraud Detection API** construida con FastAPI.")

API_URL = st.text_input("URL de la API", value="http://127.0.0.1:8000")

st.subheader("Ingresa los datos de la transaccion")

col1, col2 = st.columns(2)
with col1:
    time = st.number_input("Time", value=0.0)
with col2:
    amount = st.number_input("Amount", value=149.62, min_value=0.0)

st.markdown("**Variables V1-V28** (anonimizadas por PCA)")
v_values = {}
cols = st.columns(4)
for i in range(1, 29):
    with cols[(i - 1) % 4]:
        v_values[f"V{i}"] = st.number_input(f"V{i}", value=0.0, format="%.2f")

if st.button("🔍 Analizar transaccion", type="primary"):
    payload = {"Time": time, "Amount": amount, **v_values}
    try:
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        if data["is_fraud"]:
            st.error(f"⚠️ FRAUDE DETECTADO - Riesgo {data['risk_level']}")
        else:
            st.success(f"✅ Transaccion legitima - Riesgo {data['risk_level']}")

        st.metric("Probabilidad de fraude", f"{data['fraud_probability']*100:.2f}%")
    except Exception as e:
        st.warning(f"No se pudo conectar con la API: {e}")
