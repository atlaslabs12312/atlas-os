import sys
import os

# Biar bisa import folder engine/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from engine.reasoner import analyze_contract

st.set_page_config(page_title="ATLAS Intelligence Engine", layout="wide")
st.title("ATLAS: AI Explainable Reasoning Engine")
st.write("ATLAS NEVER GUESSES. ATLAS REASONS.")

contract = st.text_input("Masukkan alamat kontrak/token:")

if st.button("ANALISA SEKARANG"):
    with st.spinner("ATLAS sedang reasoning..."):
        decision = analyze_contract(contract)
        st.success(decision)

