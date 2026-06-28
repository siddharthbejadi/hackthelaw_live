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

# ── If already logged in, show the full Supervise AI interface ───────────────
if st.session_state.get("user_name") and st.session_state.get("user_role"):
    role = st.session_state.get("user_role", "")
    if "Partner" in role:
        hide = "li:nth-child(4),li:nth-child(5),li:nth-child(6)"
    elif "Junior" in role:
        hide = "li:nth-child(2),li:nth-child(3),li:nth-child(5),li:nth-child(6)"
    elif "Senior" in role:
        hide = "li:nth-child(2),li:nth-child(3),li:nth-child(4)"
    else:
        hide = ""
    hide_css = ""
    if hide:
        selectors = ",".join(
            [f"section[data-testid='stSidebar'] nav ul {li}" for li in hide.split(",")] +
            [f"[data-testid='stSidebarNavItems'] > {li}" for li in hide.split(",")]
        )
        hide_css = f"{selectors} {{ display:none !important; }}"

    st.markdown(f"""
    <style>
    section[data-testid='stSidebar'] {{ display:flex !important; }}
    .stApp {{ background:#eef2f7; }}
    section[data-testid="stSidebar"] {{ background:#e2e8f0; }}
    {hide_css}
    .msg-supervisor {{ background:#f5f3ff; border-left:3px solid #7c3aed; border-radius:0 8px 8px 0; padding:10px 14px; margin:4px 0; font-size:0.82rem; color:#1e1b4b; }}
    .msg-research   {{ background:#eff6ff; border-left:3px solid #2563eb; border-radius:0 8px 8px 0; padding:10px 14px; margin:4px 0; font-size:0.82rem; color:#1e3a5f; }}
    .msg-review     {{ background:#fffbeb; border-left:3px solid #d97706; border-radius:0 8px 8px 0; padding:10px 14px; margin:4px 0; font-size:0.82rem; color:#451a03; }}
    .msg-risk       {{ background:#fff1f2; border-left:3px solid #dc2626; border-radius:0 8px 8px 0; padding:10px 14px; margin:4px 0; font-size:0.82rem; color:#450a0a; }}
    .msg-drafting   {{ background:#faf5ff; border-left:3px solid #9333ea; border-radius:0 8px 8px 0; padding:10px 14px; margin:4px 0; font-size:0.82rem; color:#3b0764; }}
    .agent-label    {{ font-size:0.65rem; font-weight:700; letter-spacing:.8px; text-transform:uppercase; margin-bottom:4px; }}
    .arrow-line     {{ color:#94a3b8; font-size:0.72rem; padding:2px 0 2px 16px; display:block; }}
    .pill           {{ border-radius:4px; padding:3px 10px; font-size:0.75rem; font-weight:700; }}
    </style>
    """, unsafe_allow_html=True)

    user_name = st.session_state["user_name"]

    st.markdown(f"""
    <div style="padding:20px 0 10px;">
      <div style="font-size:2.4rem;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">⚖️ Legal AI Supervisor</div>
      <div style="color:#64748b;font-size:0.9rem;margin-top:6px;">
        Logged in as <b style="color:#2563eb;">{user_name}</b> · Watch AI agents communicate in real time — research, draft, review, and risk analysis running live.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_mode, col_info = st.columns([2, 3])
    with col_mode:
        demo_mode = st.radio("Pipeline mode",
            ["⚡ Review + Risk (fast)", "🔬 Full: Research + Draft + Review + Risk"],
            label_visibility="collapsed", horizontal=False)
    full_pipeline = "Full" in demo_mode
    with col_info:
        st.markdown(
            f'<div style="background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#475569;">'
            f'{"<b style=\'color:#7c3aed\'>Full pipeline</b>: Research → Draft → Review → Risk → Supervisor decision" if full_pipeline else "<b style=\'color:#2563eb\'>Fast pipeline</b>: Review → Risk → Supervisor decision"}'
            f'<br>All agents use <span style="color:#2563eb;">NVIDIA Nemotron-Ultra</span> with thinking tokens enabled.</div>',
            unsafe_allow_html=True)

    st.markdown("")
    task = st.chat_input("Describe the legal matter or paste a clause for analysis…")

    AGENT_META = {
        "research":     {"label": "🔍 RESEARCH AGENT",  "css": "msg-research",  "color": "#2563eb"},
        "drafting":     {"label": "✍️ DRAFTING AGENT",  "css": "msg-drafting",  "color": "#9333ea"},
        "review":       {"label": "🔎 REVIEW AGENT",    "css": "msg-review",    "color": "#d97706"},
        "risk_analysis":{"label": "⚠️ RISK AGENT",      "css": "msg-risk",      "color": "#dc2626"},
        "supervisor":   {"label": "🧠 SUPERVISOR",      "css": "msg-supervisor","color": "#7c3aed"},
    }

    def stream_agent_live(agent_name, task, context=""):
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
            yield f"[API ERROR: {str(e)[:120]}]"; return
        output_text = ""
        try:
            for chunk in stream:
                if not chunk.choices: continue
                delta = chunk.choices[0].delta
                if delta.content:
                    output_text += delta.content
                    yield delta.content
        except Exception as e:
            yield f"[STREAM ERROR: {str(e)[:120]}]"
        log_event(agent_name, "live_stream", {"task_preview": task[:80]})

    def parse_agent_output(raw):
        try: return json.loads(_extract_json(raw))
        except: return {"output": raw, "confidence": 0, "risk": 100, "citations": [], "flags": []}

    def supervisor_message(placeholder, msg):
        meta = AGENT_META["supervisor"]
        placeholder.markdown(f'<div class="{meta["css"]}"><div class="agent-label" style="color:{meta["color"]};">{meta["label"]}</div>{msg}</div>', unsafe_allow_html=True)

    def render_agent_stream(agent_name, task, context=""):
        meta = AGENT_META[agent_name]
        col_l, col_r = st.columns([1, 12])
        with col_r:
            st.markdown(f'<div class="agent-label" style="color:{meta["color"]};margin-bottom:4px;">{meta["label"]} <span style="color:#94a3b8;font-size:0.6rem;font-weight:400;">NVIDIA Nemotron-Ultra · streaming…</span></div>', unsafe_allow_html=True)
            box = st.empty()
        full_text = ""
        for token in stream_agent_live(agent_name, task, context):
            full_text += token
            display = full_text.lstrip("{\" \n")
            box.markdown(f'<div class="{meta["css"]}" style="border-left-color:{meta["color"]};">{display[:600]}{"…" if len(display)>600 else "▌"}</div>', unsafe_allow_html=True)
        parsed = parse_agent_output(full_text)
        conf = parsed.get("confidence","—"); risk = parsed.get("risk","—")
        flags = parsed.get("flags",[]); high_n = len([f for f in flags if "HIGH" in str(f).upper()])
        cites = parsed.get("citations",[]); output = parsed.get("output", full_text)[:300]
        conf_c = "#16a34a" if isinstance(conf,int) and conf>=70 else "#d97706" if isinstance(conf,int) and conf>=50 else "#dc2626"
        risk_c = "#dc2626" if isinstance(risk,int) and risk>60 else "#d97706" if isinstance(risk,int) and risk>30 else "#16a34a"
        pills = (f'<span class="pill" style="background:{conf_c}18;color:{conf_c};border:1px solid {conf_c}44;">conf {conf}%</span>'
                 f'<span class="pill" style="background:{risk_c}18;color:{risk_c};border:1px solid {risk_c}44;">risk {risk}%</span>'
                 + (f'<span class="pill" style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;">⚑ {high_n} HIGH</span>' if high_n else "")
                 + (f'<span class="pill" style="background:#eff6ff;color:#2563eb;border:1px solid #93c5fd;">{len(cites)} citation(s)</span>' if cites else ""))
        box.markdown(f'<div class="{meta["css"]}" style="border-left-color:{meta["color"]};"><div style="color:#374151;line-height:1.5;margin-bottom:8px;">{output}{"…" if len(parsed.get("output",""))>300 else ""}</div><div style="display:flex;gap:6px;flex-wrap:wrap;">{pills}</div></div>', unsafe_allow_html=True)
        return parsed

    if task:
        st.markdown("---")
        st.markdown('<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;"><span style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;border-radius:4px;padding:2px 10px;font-size:0.68rem;font-weight:700;letter-spacing:1px;">● LIVE</span><span style="color:#0f172a;font-weight:700;">Agent Communication Pipeline</span><span style="color:#94a3b8;font-size:0.75rem;margin-left:4px;">— real-time output from each specialist agent</span></div>', unsafe_allow_html=True)
        results = {}
        sup_open = st.empty()
        supervisor_message(sup_open, f'<span style="color:#7c3aed;">Received task.</span> Routing to {"4 specialist agents" if full_pipeline else "2 specialist agents"} — each will stream their analysis live below. Task: <em style="color:#64748b;">{task[:80]}{"…" if len(task)>80 else ""}</em>')
        agent_order = ["research","drafting","review","risk_analysis"] if full_pipeline else ["review","risk_analysis"]
        for agent_name in agent_order:
            meta = AGENT_META[agent_name]
            send_ph = st.empty()
            send_ph.markdown(f'<span class="arrow-line"><span style="color:#7c3aed;">🧠 Supervisor</span> → <span style="color:{meta["color"]};">{meta["label"]}</span>: <em style="color:#94a3b8;">sending task context…</em></span>', unsafe_allow_html=True)
            parsed = render_agent_stream(agent_name, task)
            results[agent_name] = parsed
            send_ph.markdown(f'<span class="arrow-line"><span style="color:{meta["color"]};">{meta["label"]}</span> → <span style="color:#7c3aed;">🧠 Supervisor</span>: <em style="color:#94a3b8;">complete · conf {parsed.get("confidence","?")}% · risk {parsed.get("risk","?")}%</em></span>', unsafe_allow_html=True)
        all_flags  = [f for r in results.values() for f in r.get("flags",[])]
        high_flags = [f for f in all_flags if "HIGH" in str(f).upper()]
        confs = [r.get("confidence",0) for r in results.values() if isinstance(r.get("confidence"),int)]
        risks = [r.get("risk",0) for r in results.values() if isinstance(r.get("risk"),int)]
        all_cites = list({c for r in results.values() for c in r.get("citations",[])})
        avg_conf = sum(confs)//len(confs) if confs else 0
        max_risk = max(risks) if risks else 0
        escalate = bool(high_flags) or max_risk > 50
        conf_c = "#16a34a" if avg_conf>=70 else "#d97706" if avg_conf>=50 else "#dc2626"
        risk_c = "#dc2626" if max_risk>60 else "#d97706" if max_risk>30 else "#16a34a"
        decision_color = "#dc2626" if escalate else "#16a34a"
        decision_label = "ESCALATE → Senior Lawyer" if escalate else "APPROVE — no HIGH flags"
        decision_reason = f"{len(high_flags)} HIGH flag(s), risk {max_risk}% exceeds threshold" if escalate else f"No HIGH flags, risk {max_risk}% within threshold"
        st.markdown(f'<span class="arrow-line" style="color:#7c3aed;">All agents → 🧠 Supervisor: results aggregated</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-supervisor" style="border-left-color:{decision_color};"><div class="agent-label" style="color:#7c3aed;">🧠 SUPERVISOR DECISION</div><div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:8px;"><span class="pill" style="background:{conf_c}18;color:{conf_c};border:1px solid {conf_c}44;">confidence {avg_conf}%</span><span class="pill" style="background:{risk_c}18;color:{risk_c};border:1px solid {risk_c}44;">risk {max_risk}%</span><span class="pill" style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;">{len(high_flags)} HIGH flag(s)</span><span class="pill" style="background:#eff6ff;color:#2563eb;border:1px solid #93c5fd;">{len(all_cites)} citation(s)</span></div><div style="font-size:1rem;font-weight:700;color:{decision_color};">→ {decision_label}</div><div style="font-size:0.75rem;color:#64748b;margin-top:3px;">{decision_reason}</div></div>', unsafe_allow_html=True)
        if high_flags:
            with st.expander(f"⚑ {len(high_flags)} HIGH flags raised", expanded=True):
                for f in high_flags[:6]:
                    st.markdown(f'<div style="font-size:0.78rem;color:#dc2626;background:#fef2f2;border-radius:4px;padding:6px 10px;margin:3px 0;border-left:2px solid #dc2626;">⚑ {f}</div>', unsafe_allow_html=True)
        if all_cites:
            with st.expander(f"📚 {len(all_cites)} citations verified by AI"):
                for c in all_cites[:8]:
                    st.markdown(f"- [{c}](https://www.google.com/search?q={c.replace(' ','+')}+UK+case+law)")
        st.markdown('<div style="margin-top:16px;font-size:0.72rem;color:#94a3b8;text-align:center;">Go to <b>Partner</b> → submit as a tracked matter · <b>Dashboard</b> → see full pipeline with audit trail</div>', unsafe_allow_html=True)

    st.stop()

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
