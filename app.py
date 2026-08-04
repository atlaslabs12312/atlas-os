import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.loader import load_contract
from engine.reasoner import analyze_contract
from engine.decision import evaluate_risk

st.set_page_config(page_title="ATLAS Intelligence Engine", layout="wide")
st.title("ATLAS Intelligence Engine")

contract_address = st.text_input("Contract Address Target:", placeholder="0x...")

if st.button("Jalankan Analisis"):
    if not contract_address.strip():
        st.warning("⚠️ Alamat smart contract wajib diisi!")
        st.stop()
        
    try:
        with st.spinner('ATLAS: Menarik data on-chain...'):
            raw_data = load_contract(contract_address)
            
        with st.spinner('ATLAS: Membedah kerentanan smart contract...'):
            reasoning_data = analyze_contract(raw_data)
            
        with st.spinner('ATLAS: Merumuskan verdict akhir risiko pasar...'):
            final_result = evaluate_risk(reasoning_data)
            
        st.success("✅ Analisis Selesai.")
        
        with st.expander("📋 Lihat Laporan Explainable Intelligence"):
            st.json(final_result)
            
    except Exception as e:
        st.error(f"🚨 Terjadi kesalahan pada pipeline backend: {str(e)}")

