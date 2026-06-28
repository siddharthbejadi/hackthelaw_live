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

# ── If already logged in, show the agent demo instead of the landing page ────
if st.session_state.get("user_name") and st.session_state.get("user_role"):
    # Re-show sidebar for logged-in users
    st.markdown("<style>section[data-testid='stSidebar'] { display:flex !important; }</style>", unsafe_allow_html=True)
    import json, sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from agents import _get_client, MODEL, AGENT_PROMPTS, _extract_json, log_event

    user_name = st.session_state["user_name"]
    st.markdown(f"""
    <div style="padding:16px 0 8px;">
      <div style="font-size:1.8rem;font-weight:800;color:#f8fafc;">⚖️ Supervise AI</div>
      <div style="color:#94a3b8;font-size:0.85rem;">Logged in as <b style="color:#60a5fa;">{user_name}</b> · Watch AI agents analyse legal matters in real time</div>
    </div>
    """, unsafe_allow_html=True)

    demo_mode = st.radio("Pipeline mode",
        ["⚡ Review + Risk (fast)", "🔬 Full: Research + Draft + Review + Risk"],
        label_visibility="collapsed", horizontal=True)
    full_pipeline = "Full" in demo_mode

    task = st.chat_input("Describe a legal matter or paste a clause…")

    AGENT_META = {
        "research":     {"label": "🔍 RESEARCH",  "css": "msg-research",  "color": "#2563eb"},
        "drafting":     {"label": "✍️ DRAFTING",  "css": "msg-drafting",  "color": "#9333ea"},
        "review":       {"label": "🔎 REVIEW",    "css": "msg-review",    "color": "#d97706"},
        "risk_analysis":{"label": "⚠️ RISK",      "css": "msg-risk",      "color": "#dc2626"},
        "supervisor":   {"label": "🧠 SUPERVISOR","css": "msg-supervisor","color": "#7c3aed"},
    }

    def stream_agent(agent_name, task, context=""):
        system_prompt = AGENT_PROMPTS[agent_name]
        user_content  = f"TASK:\n{task}" + (f"\n\nCONTEXT:\n{context}" if context else "")
        try:
            stream = _get_client().chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_content}],
                temperature=0.6, top_p=0.95, max_tokens=3000,
                extra_body={"chat_template_kwargs":{"enable_thinking":True},"reasoning_budget":2048},
                stream=True,
            )
        except Exception as e:
            yield f"[ERROR: {str(e)[:100]}]"; return
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def parse_out(raw):
        try: return json.loads(_extract_json(raw))
        except: return {"output":raw,"confidence":0,"risk":100,"citations":[],"flags":[]}

    if task:
        st.markdown("---")
        agent_order = ["research","drafting","review","risk_analysis"] if full_pipeline else ["review","risk_analysis"]
        results = {}
        for agent_name in agent_order:
            meta = AGENT_META[agent_name]
            st.markdown(f'<div style="font-size:0.7rem;font-weight:700;color:{meta["color"]};letter-spacing:1px;text-transform:uppercase;margin:12px 0 4px;">{meta["label"]} · streaming…</div>', unsafe_allow_html=True)
            box = st.empty()
            full_text = ""
            for token in stream_agent(agent_name, task):
                full_text += token
                box.markdown(f'<div style="background:#1e293b;border-left:3px solid {meta["color"]};border-radius:6px;padding:10px 14px;font-size:0.83rem;color:#e2e8f0;">{full_text[:500]}{"▌" if len(full_text)<500 else "…"}</div>', unsafe_allow_html=True)
            parsed = parse_out(full_text)
            results[agent_name] = parsed
            conf = parsed.get("confidence","—"); risk = parsed.get("risk","—")
            box.markdown(f'<div style="background:#1e293b;border-left:3px solid {meta["color"]};border-radius:6px;padding:10px 14px;font-size:0.83rem;color:#e2e8f0;">{parsed.get("output",full_text)[:300]}…<br><span style="font-size:0.7rem;color:#94a3b8;">conf {conf}% · risk {risk}%</span></div>', unsafe_allow_html=True)

        # Supervisor decision
        all_flags  = [f for r in results.values() for f in r.get("flags",[])]
        high_flags = [f for f in all_flags if "HIGH" in str(f).upper()]
        confs      = [r.get("confidence",0) for r in results.values() if isinstance(r.get("confidence"),int)]
        risks      = [r.get("risk",0) for r in results.values() if isinstance(r.get("risk"),int)]
        avg_conf   = sum(confs)//len(confs) if confs else 0
        max_risk   = max(risks) if risks else 0
        escalate   = bool(high_flags) or max_risk > 50
        decision_color = "#dc2626" if escalate else "#16a34a"
        decision_label = "ESCALATE → Senior Lawyer" if escalate else "APPROVE — no HIGH flags"
        st.markdown(f'<div style="background:#1e2235;border:1px solid {decision_color}44;border-radius:8px;padding:14px;margin-top:12px;"><div style="color:#7c3aed;font-size:0.7rem;font-weight:700;letter-spacing:1px;">🧠 SUPERVISOR DECISION</div><div style="color:{decision_color};font-size:1rem;font-weight:700;margin-top:4px;">→ {decision_label}</div><div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">confidence {avg_conf}% · risk {max_risk}% · {len(high_flags)} HIGH flag(s)</div></div>', unsafe_allow_html=True)

    st.stop()  # Don't show landing page to logged-in users

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
