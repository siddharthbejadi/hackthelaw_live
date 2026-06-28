"""
Legal AI Supervisor — Entry / Onboarding
"""
import streamlit as st

st.set_page_config(page_title="Lex AI — Legal Intelligence Platform", layout="wide", page_icon="⚖️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background:#0a0f1e; }
section[data-testid="stSidebar"] { display:none; }
#MainMenu, footer, header { visibility:hidden; }

.hero {
    min-height:100vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    padding:40px 20px;
}
.badge {
    background:rgba(37,99,235,0.15);
    border:1px solid rgba(37,99,235,0.4);
    color:#60a5fa;
    border-radius:20px;
    padding:6px 16px;
    font-size:0.72rem;
    font-weight:600;
    letter-spacing:1.5px;
    text-transform:uppercase;
    margin-bottom:28px;
    display:inline-block;
}
.hero-title {
    font-size:clamp(2.4rem, 5vw, 4rem);
    font-weight:800;
    color:#f8fafc;
    text-align:center;
    line-height:1.15;
    margin-bottom:16px;
    letter-spacing:-1px;
}
.hero-title span { color:#3b82f6; }
.hero-sub {
    color:#94a3b8;
    font-size:1.05rem;
    text-align:center;
    max-width:560px;
    line-height:1.8;
    margin-bottom:52px;
}
.role-grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:16px;
    max-width:820px;
    width:100%;
    margin-bottom:36px;
}
.role-card {
    background:#111827;
    border:2px solid #1e293b;
    border-radius:14px;
    padding:28px 22px;
    cursor:pointer;
    transition:all 0.2s;
    text-align:center;
}
.role-card:hover { border-color:#3b82f6; background:#0f1f3d; }
.role-card.selected { border-color:#3b82f6; background:#0f1f3d; box-shadow:0 0 0 3px rgba(59,130,246,0.2); }
.role-icon { font-size:2.2rem; margin-bottom:12px; }
.role-name { color:#f1f5f9; font-weight:700; font-size:1rem; margin-bottom:6px; }
.role-desc { color:#64748b; font-size:0.78rem; line-height:1.5; }
.stat-row {
    display:flex;
    gap:32px;
    justify-content:center;
    margin-top:52px;
    flex-wrap:wrap;
}
.stat { text-align:center; }
.stat-val { color:#f8fafc; font-size:1.6rem; font-weight:800; }
.stat-lbl { color:#475569; font-size:0.72rem; margin-top:2px; letter-spacing:.5px; }
.divider { width:1px; background:#1e293b; height:40px; align-self:center; }
</style>
""", unsafe_allow_html=True)

# ── If already logged in, go to their page ───────────────────────────────────
if st.session_state.get("user_name") and st.session_state.get("user_role"):
    role = st.session_state["user_role"]
    if role == "partner":
        st.switch_page("pages/1_Partner.py")
    elif role == "junior":
        st.switch_page("pages/2_Junior.py")
    elif role == "senior":
        st.switch_page("pages/3_Senior.py")

# ── Landing / onboarding ─────────────────────────────────────────────────────
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="badge">⚖️ &nbsp; Legal AI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">AI that works <span>with</span> your firm,<br>not around it.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Every draft reviewed. Every risk flagged. Every decision audited — by AI agents supervised in real time.</div>', unsafe_allow_html=True)

# ── Role picker ───────────────────────────────────────────────────────────────
ROLES = {
    "partner":  ("👔", "Partner",        "Submit client matters, track every AI decision, oversee the firm."),
    "junior":   ("✍️", "Junior Lawyer",  "Draft documents with AI assistance. Get instant feedback on your work."),
    "senior":   ("👁️", "Senior Lawyer",  "Review flagged matters, approve or reject AI-drafted documents."),
}

selected_role = st.session_state.get("_onboard_role", None)

cols = st.columns(3, gap="medium")
for i, (role_key, (icon, name, desc)) in enumerate(ROLES.items()):
    with cols[i]:
        is_sel = selected_role == role_key
        border = "#3b82f6" if is_sel else "#1e293b"
        bg     = "#0f1f3d" if is_sel else "#111827"
        shadow = "box-shadow:0 0 0 3px rgba(59,130,246,0.2);" if is_sel else ""
        if st.button(
            f"{icon}\n\n**{name}**\n\n{desc}",
            key=f"role_{role_key}",
            use_container_width=True,
        ):
            st.session_state["_onboard_role"] = role_key
            st.rerun()
        # Visual selected state via markdown overlay
        st.markdown(
            f'<div style="background:{bg};border:2px solid {border};border-radius:14px;padding:28px 20px;text-align:center;margin-top:-58px;pointer-events:none;{shadow}">'
            f'<div style="font-size:2rem;margin-bottom:10px;">{icon}</div>'
            f'<div style="color:#f1f5f9;font-weight:700;font-size:0.95rem;margin-bottom:6px;">{name}</div>'
            f'<div style="color:#64748b;font-size:0.75rem;line-height:1.5;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Name input + Enter ────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    name_input = st.text_input(
        "Your name",
        placeholder="e.g. Sarah Chen",
        label_visibility="collapsed",
        key="name_field",
    )

    role_label = ROLES[selected_role][1] if selected_role else "a role"
    btn_ready  = bool(name_input.strip()) and selected_role is not None
    btn_label  = f"Enter as {role_label} →" if selected_role else "Select a role above"

    if st.button(btn_label, type="primary", use_container_width=True, disabled=not btn_ready):
        st.session_state["user_name"] = name_input.strip()
        st.session_state["user_role"] = selected_role
        if selected_role == "partner":
            st.switch_page("pages/1_Partner.py")
        elif selected_role == "junior":
            st.switch_page("pages/2_Junior.py")
        elif selected_role == "senior":
            st.switch_page("pages/3_Senior.py")

# ── Stats row ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat"><div class="stat-val">550B</div><div class="stat-lbl">Parameter Model</div></div>
  <div class="divider"></div>
  <div class="stat"><div class="stat-val">4</div><div class="stat-lbl">Specialist AI Agents</div></div>
  <div class="divider"></div>
  <div class="stat"><div class="stat-val">100%</div><div class="stat-lbl">Audited Decisions</div></div>
  <div class="divider"></div>
  <div class="stat"><div class="stat-val">UK Law</div><div class="stat-lbl">Jurisdiction</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
