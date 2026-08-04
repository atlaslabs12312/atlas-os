

# Memastikan modul internal 'engine' terbaca sempurna tanpa error path
 sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from engine.loader import load_blockchain_data
from engine.reasoner import reason_with_data

def run_atlas_engine():
    print("=== ATLAS BLOCKCHAIN INTELLIGENCE ENGINE ===")
    
    # 1. Ingest/Load Data Transaksi
    tx_data = load_blockchain_data()
    
    # 2. Proses Analisis & Reasoning
    analysis_result = reason_with_data(tx_data)
    
    print("\n--- FINAL INTELLIGENCE REPORT ---")
    print(analysis_result)

if __name__ == "__main__":
    run_atlas_engine()
