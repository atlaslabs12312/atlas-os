import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.loader import load_contract
from engine.reasoner import analyze_contract
from engine.decision import evaluate_risk

st.set_page_config(page_title="ATLAS Intelligence Engine", layout="centered")
st.title("ATLAS Intelligence Engine")

contract_address = st.text_input("Contract Address Target:", placeholder="0x...")

if st.button("Jalankan Analisis"):
    if not contract_address.strip():
        st.warning("⚠️ Alamat smart contract tidak boleh kosong.")
    else:
        try:
            with st.spinner("ATLAS Loader: Mengekstraksi bytecode..."):
                raw_data = load_contract(contract_address)
            
            with st.spinner("ATLAS Reasoner: Membedah kerentanan secara deterministik..."):
                reasoning_data = analyze_contract(raw_data)
            
            with st.spinner("ATLAS Decision: Merumuskan verdict akhir..."):
                final_result = evaluate_risk(reasoning_data)
            
            st.success(f"✅ Analisis Selesai. Status: {final_result.get('status', 'SECURE')} | Skor Keamanan: {final_result.get('score', 100)}/100")
            
            with st.expander("🔍 Lihat Laporan Explainable Intelligence"):
                st.json(final_result)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan pada pipeline backend: {e}")
