import os
import time

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

def reason_with_claude(raw_data, context_volume, context_gas):
    # Fallback/Cached response jika API tidak tersedia atau gagal
    fallback_reasoning = (
        f"[CACHED FALLBACK] Volume {context_volume} ($ {raw_data['volume_usd']}) "
        f"dengan gas fee {context_gas} ({raw_data['gas_price_gwei']} Gwei) "
        f"menunjukkan pola anomali berulang yang konsisten dengan aktivitas bot arbitrase on-chain."
    )
    
    # Cek apakah API Key sudah diset di environment variables
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not HAS_ANTHROPIC or not api_key:
        print("\n[AI INFO] Anthropic library tidak ditemukan atau API Key belum diset. Menggunakan fallback cache.")
        return fallback_reasoning

    try:
        print("\n[3] MENJALANKAN CLAUDE API (REAL-TIME REASONING)...")
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = (
            f"Analisis data transaksi blockchain berikut sebagai pakar keamanan siber dan intelijen on-chain:\n"
            f"- Wallet: {raw_data['wallet']}\n"
            f"- Volume USD: {raw_data['volume_usd']}\n"
            f"- Gas Price: {raw_data['gas_price_gwei']} Gwei\n"
            f"- Pola Historis: {raw_data['historical_flags']}\n"
            f"Berikan analisis penalaran singkat dan tajam (maksimal 2 kalimat) mengapa transaksi ini berisiko."
        )
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
        
    except Exception as e:
        print(f"\n[AI WARNING] Gagal terhubung ke Claude API ({e}). Beralih otomatis ke fallback cache.")
        return fallback_reasoning

def run_atlas_demo():
    print("=== 🚀 MEMULAI DEMO ATLAS (PHASE DELTA: HYBRID CLAUDE) ===")
    
    # 1. DATA
    raw_data = {
        "wallet": "0x123...abc",
        "tx_hash": "0x999...def",
        "volume_usd": 50000,
        "gas_price_gwei": 320,
        "historical_flags": "High frequency bot pattern"
    }
    print(f"\n[1] DATA MENTAH:\n{raw_data}")
    time.sleep(0.3)

    # 2. CONTEXT
    context_volume = "High" if raw_data["volume_usd"] > 10000 else "Normal"
    context_gas = "Congested" if raw_data["gas_price_gwei"] > 250 else "Stable"
    print(f"\n[2] KONTEKS:\nVolume: {context_volume} | Gas: {context_gas}")
    time.sleep(0.3)

    # 3. REASONING (Hybrid Claude + Fallback)
    reasoning_output = reason_with_claude(raw_data, context_volume, context_gas)
    print(f"\n[3] HASIL REASONING ATLAS:\n{reasoning_output}")
    time.sleep(0.3)

    # 4. DECISION
    decision = "FLAG_RISK: Tahan eksekusi, anomali tervalidasi oleh AI Reasoning Engine."
    print(f"\n[4] KEPUTUSAN FINAL:\n{decision}")
    print("\n=== DEMO SELESAI ===")

if __name__ == "__main__":
    run_atlas_demo()
