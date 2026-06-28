"""
Legal AI Supervisor — Entry / Onboarding
"""
import streamlit as st

st.set_page_config(page_title="Lex AI — Legal Intelligence Platform", layout="centered", page_icon="⚖️")

st.markdown("""
<style>
.stApp { background:#0a0f1e; }
section[data-testid="stSidebar"] { display:none; }
#MainMenu, footer, header { visibility:hidden; }

h1, h2, h3, p, label, div { color:#f8fafc; }

/* Name input */
.stTextInput input {
    background:#111827 !important;
    border:1px solid #1e293b !important;
    color:#f8fafc !important;
    border-radius:10px !important;
    padding:14px 16px !important;
    font-size:1rem !important;
}
.stTextInput input::placeholder { color:#475569 !important; }
.stTextInput input:focus { border-color:#3b82f6 !important; box-shadow:0 0 0 3px rgba(59,130,246,0.2) !important; }

/* Role radio buttons */
div[data-testid="stRadio"] > div { gap:12px; }
div[data-testid="stRadio"] label {
    background:#111827;
    border:2px solid #1e293b;
    border-radius:14px;
    padding:22px 20px !important;
    cursor:pointer;
    transition:all 0.2s;
    width:100%;
}
div[data-testid="stRadio"] label:hover { border-color:#3b82f6 !important; background:#0f1f3d !important; }
div[data-testid="stRadio"] label[data-checked="true"] {
    border-color:#3b82f6 !important;
    background:#0f1f3d !important;
    box-shadow:0 0 0 3px rgba(59,130,246,0.2);
}
div[data-testid="stRadio"] label p { color:#f1f5f9 !important; font-size:0.95rem !important; }

/* Enter button */
.stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#2563eb,#1d4ed8) !important;
    border:none !important;
    border-radius:10px !important;
    color:#fff !important;
    font-size:1rem !important;
    font-weight:600 !important;
    padding:14px !important;
    letter-spacing:0.3px !important;
    transition:all 0.2s !important;
}
.stButton > button[kind="primary"]:hover { background:linear-gradient(135deg,#3b82f6,#2563eb) !important; }
.stButton > button[disabled] { background:#1e293b !important; color:#475569 !important; }
</style>
""", unsafe_allow_html=True)

# ── If already logged in, route directly ─────────────────────────────────────
if st.session_state.get("user_name") and st.session_state.get("user_role"):
    role = st.session_state["user_role"]
    if role == "Partner":
        st.switch_page("pages/1_Partner.py")
    elif role == "Junior Lawyer":
        st.switch_page("pages/2_Junior.py")
    elif role == "Senior Lawyer":
        st.switch_page("pages/3_Senior.py")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-bottom:40px;">
  <div style="display:inline-block;background:rgba(37,99,235,0.15);border:1px solid rgba(37,99,235,0.4);
              color:#60a5fa;border-radius:20px;padding:6px 18px;font-size:0.72rem;font-weight:600;
              letter-spacing:1.5px;text-transform:uppercase;margin-bottom:24px;">
    ⚖️ &nbsp; Legal AI Platform
  </div>
  <div style="font-size:2.8rem;font-weight:800;color:#f8fafc;line-height:1.15;
              letter-spacing:-1px;margin-bottom:14px;">
    AI that works <span style="color:#3b82f6;">with</span> your firm,<br>not around it.
  </div>
  <div style="color:#94a3b8;font-size:1rem;line-height:1.8;max-width:480px;margin:0 auto;">
    Every draft reviewed. Every risk flagged. Every decision audited — by AI agents supervised in real time.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Role picker ───────────────────────────────────────────────────────────────
st.markdown("<p style='color:#64748b;font-size:0.8rem;text-align:center;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;'>Select your role</p>", unsafe_allow_html=True)

role = st.radio(
    "role",
    ["👔  Partner — Submit matters, oversee the firm",
     "👁️  Senior Lawyer — Review and approve flagged work",
     "✍️  Junior Lawyer — Draft with AI assistance"],
    label_visibility="collapsed",
)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Name input ────────────────────────────────────────────────────────────────
name = st.text_input("Your name", placeholder="Enter your full name", label_visibility="collapsed")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Enter button ──────────────────────────────────────────────────────────────
role_clean = role.split("—")[0].strip().lstrip("👔✍️👁️ ")
btn_label  = f"Enter as {role_clean} →" if name.strip() else "Enter your name above"
ready      = bool(name.strip())

if st.button(btn_label, type="primary", use_container_width=True, disabled=not ready):
    st.session_state["user_name"] = name.strip()
    st.session_state["user_role"] = role_clean
    if "Partner" in role_clean:
        st.switch_page("pages/1_Partner.py")
    elif "Senior" in role_clean:
        st.switch_page("pages/3_Senior.py")
    elif "Junior" in role_clean:
        st.switch_page("pages/2_Junior.py")

# ── Footer stats ──────────────────────────────────────────────────────────────
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;justify-content:center;gap:40px;border-top:1px solid #1e293b;padding-top:28px;">
  <div style="text-align:center;">
    <div style="color:#f8fafc;font-size:1.4rem;font-weight:800;">550B</div>
    <div style="color:#475569;font-size:0.7rem;margin-top:2px;">Parameter Model</div>
  </div>
  <div style="width:1px;background:#1e293b;"></div>
  <div style="text-align:center;">
    <div style="color:#f8fafc;font-size:1.4rem;font-weight:800;">4</div>
    <div style="color:#475569;font-size:0.7rem;margin-top:2px;">Specialist AI Agents</div>
  </div>
  <div style="width:1px;background:#1e293b;"></div>
  <div style="text-align:center;">
    <div style="color:#f8fafc;font-size:1.4rem;font-weight:800;">100%</div>
    <div style="color:#475569;font-size:0.7rem;margin-top:2px;">Audited Decisions</div>
  </div>
  <div style="width:1px;background:#1e293b;"></div>
  <div style="text-align:center;">
    <div style="color:#f8fafc;font-size:1.4rem;font-weight:800;">UK Law</div>
    <div style="color:#475569;font-size:0.7rem;margin-top:2px;">Jurisdiction</div>
  </div>
</div>
""", unsafe_allow_html=True)
