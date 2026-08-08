# -*- coding: utf-8 -*-
"""
ATLAS - Blockchain Intelligence Engine
app.py - PURE FRONTEND LAYER

File ini sengaja ditulis 100% ASCII di level source code (emoji dibuat
lewat chr(), bukan karakter literal) supaya tahan terhadap korupsi
karakter saat copy-paste lintas HP/clipboard/browser.

Aturan arsitektur:
- Tidak ada logic yang MENGHITUNG risk_score/confidence/metrics/verdict.
- Tidak ada keyword matching pada teks verdict untuk menentukan
  HIGH RISK / LOW RISK. Pewarnaan kartu HANYA memakai angka
  report["risk_score"] yang datang dari backend.
- Semua field dibaca dengan .get() yang aman. Field kosong -> "N/A",
  bukan angka karangan.
"""

import os
import streamlit as st

# ==============================================================================
# ICON - didefinisikan lewat chr() supaya source file tetap ASCII murni
# ==============================================================================
ICON_SATELLITE = chr(0x1F6F0)
ICON_SEARCH = chr(0x1F50D)
ICON_INBOX = chr(0x1F4E5)
ICON_DNA = chr(0x1F9EC)
ICON_SCALE = chr(0x2696)
ICON_BRAIN = chr(0x1F9E0)
ICON_PAGE = chr(0x1F4C4)
ICON_LINK = chr(0x1F517)
ICON_WARNING = chr(0x26A0)
ICON_BULLET = chr(0x25B8)
ICON_DOT_RED = chr(0x1F534)
ICON_DOT_YELLOW = chr(0x1F7E1)
ICON_DOT_GREEN = chr(0x1F7E2)
ICON_DOT_WHITE = chr(0x26AA)
ICON_SEP = chr(0x2022)

# ==============================================================================
# BACKEND WIRING - app.py hanya memanggil, tidak menghitung apa pun
# ==============================================================================
try:
    from engine.reasoner import analyze_contract
    BACKEND_AVAILABLE = True
    BACKEND_IMPORT_ERROR = None
except ImportError as import_error:
    BACKEND_AVAILABLE = False
    BACKEND_IMPORT_ERROR = str(import_error)

PIPELINE_STAGES = [
    (ICON_INBOX, "Loader", "Menerima dan memvalidasi input"),
    (ICON_SEARCH, "Scanner", "Ekstraksi struktur kontrak"),
    (ICON_DNA, "Feature Extractor", "Deteksi pola risiko"),
    (ICON_SCALE, "Risk Engines", "Ownership, Liquidity, Tax, Blacklist, Honeypot"),
    (ICON_BRAIN, "AI Reasoner", "Penyusunan penjelasan hasil"),
    (ICON_PAGE, "Report Builder", "Kompilasi verdict akhir"),
]

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="ATLAS - Blockchain Intelligence Engine",
    page_icon=ICON_SATELLITE,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# THEME - hitam / merah / putih / abu gelap. Tidak ada biru.
# ==============================================================================
ATLAS_CSS = """
<style>
:root{
    --atlas-bg:#050505;
    --atlas-panel:#121214;
    --atlas-panel-border:#232326;
    --atlas-red:#FF1A1A;
    --atlas-red-dim:#7A0F0F;
    --atlas-white:#F5F5F5;
    --atlas-gray:#9A9A9E;
    --atlas-green:#22C55E;
    --atlas-amber:#F59E0B;
}
.stApp{ background:var(--atlas-bg); color:var(--atlas-white); font-family:'Inter',system-ui,-apple-system,sans-serif; }
.block-container{ padding-top:1.6rem !important; padding-bottom:3rem !important; max-width:980px; }

@keyframes atlas-blink{
    0%,88%,100%{ transform:scaleY(1); opacity:1; }
    94%{ transform:scaleY(0.12); opacity:0.75; }
}
.atlas-eye{
    width:64px; height:64px; border-radius:50%; margin:0 auto 16px auto;
    background:radial-gradient(circle, var(--atlas-red) 0%, var(--atlas-red-dim) 65%, transparent 100%);
    box-shadow:0 0 45px rgba(255,26,26,0.45);
    animation:atlas-blink 3.2s infinite ease-in-out;
}
.atlas-hero{ text-align:center; margin-bottom:22px; }
.atlas-hero-title{ font-size:2.6rem; font-weight:900; letter-spacing:-1px; color:var(--atlas-white); margin:0; }
.atlas-hero-sub{ font-size:1.05rem; font-weight:700; color:var(--atlas-red); letter-spacing:1px; margin-top:2px; }
.atlas-hero-tagline{ font-size:.82rem; color:var(--atlas-gray); letter-spacing:2px; margin-top:10px; text-transform:uppercase; }

.status-bar{
    display:flex; flex-wrap:wrap; gap:22px; justify-content:center;
    background:var(--atlas-panel); border:1px solid var(--atlas-panel-border);
    border-radius:14px; padding:14px 20px; margin-bottom:22px; font-size:.82rem;
}
.status-item{ display:flex; align-items:center; gap:7px; color:var(--atlas-gray); }
.status-dot{ width:8px; height:8px; border-radius:50%; }
.status-on{ background:var(--atlas-green); box-shadow:0 0 8px var(--atlas-green); }
.status-off{ background:var(--atlas-amber); box-shadow:0 0 8px var(--atlas-amber); }
.status-item b{ color:var(--atlas-white); }

.atlas-panel{
    background:var(--atlas-panel); border:1px solid var(--atlas-panel-border);
    border-radius:14px; padding:22px; margin-bottom:16px;
}
.section-label{
    font-size:.72rem; font-weight:800; letter-spacing:2.5px; color:var(--atlas-gray);
    text-transform:uppercase; margin-bottom:14px;
}

.pipeline-grid{ display:grid; grid-template-columns:repeat(6,1fr); gap:8px; }
.pipeline-stage{
    background:#0c0c0e; border:1px solid var(--atlas-panel-border); border-radius:10px;
    padding:12px 8px; text-align:center;
}
.pipeline-stage-icon{ font-size:1.2rem; }
.pipeline-stage-name{ font-size:.72rem; font-weight:800; color:var(--atlas-white); margin-top:4px; }
.pipeline-stage-desc{ font-size:.64rem; color:var(--atlas-gray); margin-top:3px; line-height:1.3; }

.severity-pill{
    display:inline-block; padding:6px 18px; border-radius:999px;
    font-weight:800; font-size:.72rem; letter-spacing:2px;
}
.sev-critical{ background:rgba(255,26,26,.14); border:1px solid var(--atlas-red); color:var(--atlas-red); }
.sev-medium{ background:rgba(245,158,11,.14); border:1px solid var(--atlas-amber); color:var(--atlas-amber); }
.sev-low{ background:rgba(34,197,94,.14); border:1px solid var(--atlas-green); color:var(--atlas-green); }
.sev-unknown{ background:rgba(154,154,158,.14); border:1px solid var(--atlas-gray); color:var(--atlas-gray); }

.verdict-card{ border-radius:20px; padding:44px 26px; text-align:center; margin:14px 0 16px 0; }
.verdict-card.sev-critical{ background:radial-gradient(circle at top, rgba(255,26,26,.16), #0a0505 75%); border:2px solid var(--atlas-red); }
.verdict-card.sev-medium{ background:radial-gradient(circle at top, rgba(245,158,11,.14), #0a0805 75%); border:2px solid var(--atlas-amber); }
.verdict-card.sev-low{ background:radial-gradient(circle at top, rgba(34,197,94,.14), #050a06 75%); border:2px solid var(--atlas-green); }
.verdict-card.sev-unknown{ background:#0c0c0e; border:2px solid var(--atlas-panel-border); }
.verdict-title{ font-size:2.4rem; font-weight:900; margin:12px 0 6px 0; letter-spacing:-1px; }
.verdict-meta{ font-size:.82rem; color:var(--atlas-gray); display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-top:16px; }
.verdict-meta b{ color:var(--atlas-white); }
.addr-chip{
    font-family:'JetBrains Mono', ui-monospace, monospace; background:rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.1); padding:2px 8px; border-radius:6px; font-size:.85em;
}

.reasoning-item{
    display:flex; gap:10px; padding:10px 0; border-bottom:1px solid var(--atlas-panel-border);
    font-size:.88rem; color:#E5E5E5; line-height:1.6;
}
.reasoning-item:last-child{ border-bottom:none; }
.reasoning-bullet{ color:var(--atlas-red); flex-shrink:0; }

.risk-grid{ display:grid; grid-template-columns:1fr 1fr; gap:16px 22px; }
.risk-row-top{ display:flex; justify-content:space-between; font-size:.82rem; color:#D4D4D4; margin-bottom:6px; font-weight:600; }
.risk-track{ background:rgba(255,255,255,.06); border-radius:999px; height:7px; overflow:hidden; }
.risk-fill{ height:100%; border-radius:999px; }

.meta-grid{ display:flex; flex-wrap:wrap; gap:20px; justify-content:center; }
.meta-item{ font-size:.74rem; color:var(--atlas-gray); }
.meta-item b{ color:var(--atlas-white); }

.error-card{
    background:#150808; border:1px solid var(--atlas-red); border-radius:14px;
    padding:26px; text-align:center; margin:14px 0;
}
.error-card .error-title{ font-size:1.3rem; font-weight:900; color:var(--atlas-red); margin-bottom:8px; }
.error-card .error-detail{ font-size:.85rem; color:var(--atlas-gray); }

div.stButton > button{
    background:linear-gradient(135deg, var(--atlas-red-dim) 0%, #0c0c0e 100%) !important;
    color:var(--atlas-white) !important; border:1px solid var(--atlas-red) !important;
    font-weight:700 !important; letter-spacing:.5px !important; border-radius:10px !important;
    padding:13px 0 !important; cursor:pointer !important; transition:all .18s ease;
}
div.stButton > button:hover{
    background:var(--atlas-red) !important; box-shadow:0 0 22px rgba(255,26,26,.5) !important;
    transform:translateY(-1px);
}
div[data-baseweb="tab-list"]{ gap:6px; }
div[data-baseweb="tab"]{ background:var(--atlas-panel) !important; border-radius:8px !important; }

@media (max-width:900px){ .pipeline-grid{ grid-template-columns:repeat(3,1fr); } }
@media (max-width:640px){
    .atlas-hero-title{ font-size:1.9rem; }
    .pipeline-grid{ grid-template-columns:repeat(2,1fr); }
    .risk-grid{ grid-template-columns:1fr; }
    .verdict-card{ padding:30px 18px; }
    .verdict-title{ font-size:1.8rem; }
    .status-bar{ gap:12px; padding:12px; }
    .atlas-panel{ padding:16px; }
}
</style>
"""
st.markdown(ATLAS_CSS, unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "atlas_report" not in st.session_state:
    st.session_state.atlas_report = None
if "source_prefill" not in st.session_state:
    st.session_state.source_prefill = ""


def use_example(source_code):
    st.session_state.source_prefill = source_code
    st.session_state.atlas_report = None


# ==============================================================================
# HEADER
# ==============================================================================
def render_header():
    html = (
        '<div class="atlas-hero">'
        '<div class="atlas-eye"></div>'
        '<div class="atlas-hero-title">' + ICON_SATELLITE + ' ATLAS</div>'
        '<div class="atlas-hero-sub">Blockchain Intelligence Engine</div>'
        '<div class="atlas-hero-tagline">ATLAS NEVER GUESSES. ATLAS REASONS.</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ==============================================================================
# STATUS ENGINE - status nyata dari konfigurasi environment
# ==============================================================================
def render_status_engine():
    gemini_ready = bool(os.environ.get("GEMINI_API_KEY", "").strip())
    onchain_ready = bool(os.environ.get("EXPLORER_API_KEY", "").strip())

    def status_item(label, ready, ready_text, fallback_text):
        css_class = "status-on" if ready else "status-off"
        text = ready_text if ready else fallback_text
        return (
            '<div class="status-item"><span class="status-dot ' + css_class + '"></span>'
            + label + ': <b>' + text + '</b></div>'
        )

    backend_class = "status-on" if BACKEND_AVAILABLE else "status-off"
    backend_text = "Connected" if BACKEND_AVAILABLE else "Not Found"

    parts = ['<div class="status-bar">']
    parts.append(
        '<div class="status-item"><span class="status-dot ' + backend_class + '"></span>'
        'Engine Backend: <b>' + backend_text + '</b></div>'
    )
    parts.append(status_item("AI Reasoning", gemini_ready, "Gemini Active", "Rule Engine Fallback"))
    parts.append(status_item("On-Chain Data", onchain_ready, "RPC Connected", "Source Code Mode"))
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


# ==============================================================================
# INPUT SECTION - Mode A (source code, utama) / Mode B (address, lanjutan)
# ==============================================================================
EXAMPLE_HIGH_RISK = """pragma solidity ^0.8.0;

contract SampleToken {
    address public owner;
    mapping(address => bool) public isBlacklisted;
    uint256 public sellTax = 5;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function setSellTax(uint256 newTax) public onlyOwner {
        sellTax = newTax;
    }

    function blacklist(address wallet, bool status) public onlyOwner {
        isBlacklisted[wallet] = status;
    }

    function emergencyWithdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
"""

EXAMPLE_SAFE = """pragma solidity ^0.8.0;

contract SampleSafeToken {
    string public name = "SafeToken";
    uint256 public totalSupply;

    constructor(uint256 supply) {
        totalSupply = supply;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        return true;
    }
}
"""


def render_input_section():
    tab_source, tab_address = st.tabs(["Paste Solidity Source", "Contract Address"])
    input_data = None

    with tab_source:
        st.caption("Mode utama - analisis pattern deterministik, tidak butuh API key.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Contoh: Pola Berisiko Tinggi", use_container_width=True, key="ex_high"):
                use_example(EXAMPLE_HIGH_RISK)
        with col2:
            if st.button("Contoh: Pola Standar/Aman", use_container_width=True, key="ex_safe"):
                use_example(EXAMPLE_SAFE)

        source_code = st.text_area(
            "Solidity Source Code",
            value=st.session_state.source_prefill,
            height=180,
            placeholder="pragma solidity ^0.8.0;\n\ncontract MyToken { ... }",
            label_visibility="collapsed",
        )
        token_name_a = st.text_input(
            "Nama Token", key="tn_a", label_visibility="collapsed",
            placeholder="Nama token (opsional)",
        )
        analyze_a = st.button(
            "JALANKAN AUDIT INTELIJEN ATLAS", use_container_width=True,
            type="primary", key="analyze_source",
        )
        if analyze_a:
            input_data = {
                "mode": "source_code",
                "source_code": source_code,
                "token_name": token_name_a,
                "network": "N/A",
                "address": "N/A",
            }

    with tab_address:
        st.caption("Mode lanjutan - butuh RPC/Explorer API key aktif di server untuk data on-chain real. Tanpa API key, sistem akan melaporkan data tidak cukup, bukan mengarang hasil.")
        network = st.selectbox("Blockchain Network", ["BNB Chain (BEP-20)", "Ethereum (ERC-20)"], key="net_b")
        address = st.text_input("Contract Address", placeholder="0x...", key="addr_b")
        token_name_b = st.text_input(
            "Nama Token B", key="tn_b", label_visibility="collapsed",
            placeholder="Nama token (opsional)",
        )
        analyze_b = st.button(
            "JALANKAN AUDIT INTELIJEN ATLAS", use_container_width=True,
            type="primary", key="analyze_address",
        )
        if analyze_b:
            input_data = {
                "mode": "address",
                "address": address,
                "token_name": token_name_b,
                "network": network,
                "source_code": "",
            }

    return input_data


# ==============================================================================
# PIPELINE - dilabel sebagai arsitektur, bukan progress real-time
# ==============================================================================
def render_pipeline_diagram():
    parts = [
        '<div class="atlas-panel">',
        '<div class="section-label">ATLAS PIPELINE ARCHITECTURE</div>',
        '<div class="pipeline-grid">',
    ]
    for icon, name, desc in PIPELINE_STAGES:
        parts.append(
            '<div class="pipeline-stage">'
            '<div class="pipeline-stage-icon">' + icon + '</div>'
            '<div class="pipeline-stage-name">' + name + '</div>'
            '<div class="pipeline-stage-desc">' + desc + '</div>'
            '</div>'
        )
    parts.append('</div></div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


# ==============================================================================
# ERROR CARD
# ==============================================================================
def render_error_card(title, detail):
    html = (
        '<div class="error-card">'
        '<div class="error-title">' + ICON_WARNING + ' ' + title + '</div>'
        '<div class="error-detail">' + detail + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ==============================================================================
# HELPER TAMPILAN - tidak ada keyword matching, tidak ada angka karangan
# ==============================================================================
def severity_tier(risk_score):
    """Tier visual HANYA dari angka risk_score. Bukan membaca teks verdict."""
    if risk_score is None:
        return "sev-unknown", ICON_DOT_WHITE
    try:
        score = float(risk_score)
    except (TypeError, ValueError):
        return "sev-unknown", ICON_DOT_WHITE
    if score >= 70:
        return "sev-critical", ICON_DOT_RED
    if score >= 40:
        return "sev-medium", ICON_DOT_YELLOW
    return "sev-low", ICON_DOT_GREEN


def fmt(value, suffix=""):
    if value is None:
        return "N/A"
    return str(value) + suffix


def fmt_address(addr):
    addr = str(addr) if addr else "N/A"
    if len(addr) <= 18 or addr == "N/A":
        return addr
    return addr[:8] + "..." + addr[-6:]


# ==============================================================================
# RENDER HASIL - 100% dibaca dari report backend
# ==============================================================================
def render_report(report):
    if not isinstance(report, dict):
        render_error_card("Format Respons Tidak Dikenali", "Backend tidak mengembalikan struktur data yang diharapkan.")
        return

    if report.get("frontend_error"):
        render_error_card("Analisis Tidak Dapat Diselesaikan", report["frontend_error"])
        return

    verdict = report.get("verdict") or "N/A"
    risk_score = report.get("risk_score")
    confidence = report.get("confidence")
    metrics = report.get("metrics") or {}
    reasoning = report.get("reasoning") or []
    metadata = report.get("metadata") or {}

    status = metadata.get("status", "")
    if status in ("INSUFFICIENT_DATA", "ERROR"):
        title = "Data Tidak Cukup" if status == "INSUFFICIENT_DATA" else "Analisis Gagal"
        detail = reasoning[0] if reasoning else "Backend tidak dapat menyelesaikan analisis untuk input ini."
        render_error_card(title, detail)
        return

    sev_class, sev_icon = severity_tier(risk_score)
    address_display = fmt_address(metadata.get("address"))

    verdict_html = (
        '<div style="text-align:center;">'
        '<span class="severity-pill ' + sev_class + '">' + sev_icon + ' ' + verdict + '</span>'
        '</div>'
        '<div class="verdict-card ' + sev_class + '">'
        '<div class="verdict-title">' + verdict + '</div>'
        '<div class="verdict-meta">'
        '<span>RISK SCORE <b>' + fmt(risk_score, "/100") + '</b></span>'
        '<span>' + ICON_SEP + '</span>'
        '<span>CONFIDENCE <b>' + fmt(confidence, "%") + '</b></span>'
        '<span>' + ICON_SEP + '</span>'
        '<span>TARGET <span class="addr-chip">' + address_display + '</span></span>'
        '</div></div>'
    )
    st.markdown(verdict_html, unsafe_allow_html=True)

    summary_parts = ['<div class="atlas-panel"><div class="section-label">EXECUTIVE SUMMARY & REASONING</div>']
    if reasoning:
        for point in reasoning:
            summary_parts.append(
                '<div class="reasoning-item"><span class="reasoning-bullet">' + ICON_BULLET + '</span><span>' + str(point) + '</span></div>'
            )
    else:
        summary_parts.append('<div class="reasoning-item">Backend tidak menyertakan reasoning untuk hasil ini.</div>')
    summary_parts.append('</div>')
    st.markdown("".join(summary_parts), unsafe_allow_html=True)

    if metrics:
        dash_parts = ['<div class="atlas-panel"><div class="section-label">RISK DASHBOARD</div><div class="risk-grid">']
        for key, value in metrics.items():
            label = key.replace("_score", "").replace("_", " ").title()
            numeric_ok = True
            try:
                pct = float(value)
                pct = max(0.0, min(100.0, pct))
            except (TypeError, ValueError):
                numeric_ok = False
                pct = 0.0
            if not numeric_ok:
                bar_color = "#3a3a3d"
            elif pct >= 60:
                bar_color = "var(--atlas-red)"
            elif pct >= 30:
                bar_color = "var(--atlas-amber)"
            else:
                bar_color = "var(--atlas-green)"
            dash_parts.append(
                '<div><div class="risk-row-top"><span>' + label + '</span>'
                '<span style="color:' + bar_color + ';font-weight:800;">' + fmt(value, "%") + '</span></div>'
                '<div class="risk-track"><div class="risk-fill" style="width:' + str(pct) + '%;background:' + bar_color + ';"></div></div></div>'
            )
        dash_parts.append('</div></div>')
        st.markdown("".join(dash_parts), unsafe_allow_html=True)

    if metadata:
        label_map = {
            "scan_id": "Scan ID", "timestamp": "Timestamp", "engine_version": "Engine Version",
            "token_name": "Token", "network": "Network", "address": "Address",
            "status": "Status", "processing_time": "Processing Time",
        }
        meta_parts = ['<div class="atlas-panel"><div class="section-label">AUDIT METADATA</div><div class="meta-grid">']
        for key, value in metadata.items():
            label = label_map.get(key, key.replace("_", " ").title())
            meta_parts.append('<div class="meta-item">' + label + ': <b>' + str(value) + '</b></div>')
        meta_parts.append('</div></div>')
        st.markdown("".join(meta_parts), unsafe_allow_html=True)


# ==============================================================================
# MAIN FLOW
# ==============================================================================
render_header()
render_status_engine()

if not BACKEND_AVAILABLE:
    render_error_card(
        "Backend Engine Tidak Ditemukan",
        "Gagal mengimpor engine.reasoner: " + str(BACKEND_IMPORT_ERROR),
    )

new_input = render_input_section()
render_pipeline_diagram()

if new_input is not None:
    if not BACKEND_AVAILABLE:
        st.session_state.atlas_report = {"frontend_error": "Backend belum tersedia - lihat pesan di atas."}
    else:
        try:
            with st.spinner("ATLAS sedang menjalankan pipeline analisis..."):
                st.session_state.atlas_report = analyze_contract(new_input)
        except TypeError as type_error:
            st.session_state.atlas_report = {
                "frontend_error": "Signature analyze_contract() belum sesuai kontrak input_data: " + str(type_error)
            }
        except Exception as backend_error:
            st.session_state.atlas_report = {
                "frontend_error": "Backend melempar error saat memproses: " + str(backend_error)
            }
    st.rerun()

if st.session_state.atlas_report is not None:
    render_report(st.session_state.atlas_report)
