from engine.loader import load_blockchain_data
from engine.reasoner import reason_with_claude

def run_atlas_engine():
    print("=== ATLAS BLOCKCHAIN INTELLIGENCE ENGINE ===")
    
    # 1. Ingest/Load Data Transaksi
    tx_data = load_blockchain_data("0x9f8c...3b1a")
    
    # 2. Proses Analisis & Reasoning AI dengan parameter yang sesuai
    analysis_result = reason_with_claude(tx_data, context_volume="150 ETH", context_gas="0.0045")
    
    print("\n--- FINAL INTELLIGENCE REPORT ---")
    print(analysis_result)

if __name__ == "__main__":
    run_atlas_engine()
