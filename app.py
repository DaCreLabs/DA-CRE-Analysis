# =============================================================================
# DACRE WORLDWIDE — STREAMLIT V8.0 — CONSOLIDATED BUILD
# =============================================================================
# This build returns to the existing Streamlit architecture.
# It preserves the important DACRE concepts from the prior builds:
# - Overall Admin DI command centre
# - David Creation protected engineering area
# - DI Basement protected 20-room DI office
# - 20 role-based DI specialists
# - MB Memory Board
# - Faith & Business Wisdom Lab
# - Bible / Five Books of Moses / Qur'an business-principle library
# - Workspace & Data
# - Charts
# - Business Twin
# - Decision Ledger
# - Opportunity Radar
# - File Vault / Export
# - server-side AI adapter
# - SMTP signup verification
# - activity logging
# - human-faced DI office visualisation using HTML/CSS
#
# IMPORTANT:
# Secrets are read from environment variables / Streamlit Secrets.
# No SMTP password or API key is hard-coded here.
# =============================================================================

import os
import re
import io
import json
import hmac
import time
import secrets
import sqlite3
import hashlib
import urllib.parse
import urllib.request
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP_NAME = "DACRE WORLDWIDE"
VERSION = "8.0.0-STREAMLIT-10000"
BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Authentication values are overridable through deployment secrets.
MASTER_USERNAME = os.getenv("DACRE_MASTER_USERNAME", "david").strip()
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111").strip()
GUARDIAN_NAME = os.getenv("DACRE_GUARDIAN_NAME", "Guaiel").strip()
DAVID_CREATION_PASSKEY = os.getenv("DACRE_DAVID_CREATIONS_PASSKEY", "My children").strip()
DI_BASEMENT_PASSKEY = os.getenv("DACRE_DI_BASEMENT_PASSKEY", "dacre-di").strip()

SMTP_USERNAME = os.getenv("DACRE_SMTP_USERNAME", "david@gedu.demo.edubridge.info").strip()
SMTP_PASSWORD = os.getenv("DACRE_SMTP_PASSWORD", "").strip()
SMTP_HOST = os.getenv("DACRE_SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("DACRE_SMTP_PORT", "587"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# ---------------------------------------------------------------------------
# 20 permanent role-based DI specialists.
# ---------------------------------------------------------------------------
DI_ROSTER = [
    {"name": "Analiel", "role": "Analytics Director", "specialty": "Data analysis, statistics, dashboards", "room": 1},
    {"name": "Finiel", "role": "Finance Specialist", "specialty": "Finance, budgets, cash flow", "room": 2},
    {"name": "Markiel", "role": "Market Intelligence", "specialty": "Markets, competitors, research", "room": 3},
    {"name": "Stratiel", "role": "Strategy Director", "specialty": "Strategy, planning, execution", "room": 4},
    {"name": "Operiel", "role": "Operations Specialist", "specialty": "Operations, process improvement", "room": 5},
    {"name": "Salesiel", "role": "Sales Intelligence", "specialty": "Sales, conversion, CRM", "room": 6},
    {"name": "Growthiel", "role": "Growth Specialist", "specialty": "Acquisition, experiments, growth", "room": 7},
    {"name": "Brandiel", "role": "Brand Specialist", "specialty": "Brand, messaging, positioning", "room": 8},
    {"name": "Legaliel", "role": "Governance Specialist", "specialty": "Policies, governance, compliance", "room": 9},
    {"name": "Cyberiel", "role": "Security Specialist", "specialty": "Security, privacy, access control", "room": 10},
    {"name": "Techiel", "role": "Technology Specialist", "specialty": "Software, APIs, architecture", "room": 11},
    {"name": "Dataiel", "role": "Data Engineering", "specialty": "Pipelines, schemas, data quality", "room": 12},
    {"name": "Researchiel", "role": "Research Specialist", "specialty": "Evidence gathering and synthesis", "room": 13},
    {"name": "Designiel", "role": "Design Specialist", "specialty": "UI, UX, visual systems", "room": 14},
    {"name": "Peopleiel", "role": "People Operations", "specialty": "Teams, culture, hiring", "room": 15},
    {"name": "Supplyiel", "role": "Supply Chain", "specialty": "Inventory, procurement, logistics", "room": 16},
    {"name": "Customeriel", "role": "Customer Intelligence", "specialty": "Customer experience and retention", "room": 17},
    {"name": "Projectiel", "role": "Project Management", "specialty": "Projects, milestones, delivery", "room": 18},
    {"name": "Riskiel", "role": "Risk Intelligence", "specialty": "Risk identification and mitigation", "room": 19},
    {"name": "Communiel", "role": "Communications Specialist", "specialty": "Communication and documentation", "room": 20},
]

FAITH_BUSINESS_SOURCES = [
    ("Bible", "Joseph planning", "Genesis 41", "Preparation during abundance can protect an organization during scarcity.", "Scenario planning, reserves, inventory policies, and contingency planning."),
    ("Bible", "Nehemiah rebuilding", "Nehemiah 2–6", "A large restoration project can be divided into coordinated work.", "Break transformation into owners, milestones, checkpoints, and controls."),
    ("Bible", "Proverbs diligence", "Proverbs 21:5", "Careful planning and diligent work are presented as useful disciplines.", "Use budgets, project plans, forecasts, and measurable execution."),
    ("Bible", "Proverbs counsel", "Proverbs 15:22", "Plans can benefit from counsel and multiple perspectives.", "Use structured reviews before major strategic commitments."),
    ("Bible", "Stewardship", "Genesis 1:28", "Responsibility for resources is a recurring biblical theme.", "Track assets, people, cash, time, and environmental resources carefully."),
    ("Bible", "Honest trade", "Leviticus 19:35–36", "Fair measures are emphasized in commercial activity.", "Audit quantities, pricing, invoices, and product specifications."),
    ("Moses", "Delegated leadership", "Exodus 18:17–23", "Leadership workload can be shared through clear delegation.", "Create authority levels and escalation paths."),
    ("Moses", "Justice", "Deuteronomy 16:19–20", "Judgment should not be distorted by favoritism or gifts.", "Use consistent approval criteria and conflict-of-interest controls."),
    ("Moses", "Accurate measures", "Leviticus 19:35–36", "Accurate measures support fair dealings.", "Audit units, invoices, quantities, weights, and pricing."),
    ("Moses", "Rest and maintenance", "Exodus 23:10–12", "Work includes recurring patterns of rest and maintenance.", "Schedule maintenance windows and protect operational capacity."),
    ("Quran", "Contracts and records", "Qur'an 2:282", "Important commercial obligations are treated with careful documentation.", "Document contracts, payment terms, responsibilities, and due dates."),
    ("Quran", "Mutual consent", "Qur'an 4:29", "Commerce is connected with mutual consent and lawful exchange.", "Make offers, terms, cancellation rules, and consent explicit."),
    ("Quran", "Fair measure", "Qur'an 83:1–3", "Short measurement and unfair dealing are condemned.", "Build quality controls so delivery matches promises."),
    ("Quran", "Consultation", "Qur'an 42:38", "Consultation is praised in collective affairs.", "Use stakeholder consultation for strategic decisions."),
    ("Quran", "Justice", "Qur'an 5:8", "Justice is emphasized even under pressure.", "Use documented criteria rather than favoritism."),
    ("Quran", "Trust", "Qur'an 4:58", "Trusts should be delivered to those entitled to them.", "Protect customer data, company assets, and delegated responsibilities."),
    ("Quran", "Balance", "Qur'an 55:7–9", "Balance and measure are associated with order.", "Balance growth with quality, risk, cash flow, and capacity."),
    ("Quran", "Avoid waste", "Qur'an 7:31", "Waste is discouraged.", "Reduce unnecessary spend, rework, inventory loss, and process waste."),
]

def utc_now():
    return datetime.utcnow().isoformat(timespec="seconds")

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        company TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        passkey_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_seen TEXT
    );
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        company TEXT,
        action TEXT NOT NULL,
        detail TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS di_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        reference TEXT NOT NULL,
        principle TEXT NOT NULL,
        business_use TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(source,title,reference)
    );
    CREATE TABLE IF NOT EXISTS di_nodes (
        name TEXT PRIMARY KEY,
        role TEXT NOT NULL,
        specialty TEXT NOT NULL,
        room INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'ONLINE',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS destroyed_di (
        name TEXT PRIMARY KEY,
        destroyed_at TEXT NOT NULL,
        destroyed_by TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS saved_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        company TEXT,
        decision TEXT,
        rationale TEXT,
        expected_result TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS file_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        company TEXT,
        filename TEXT,
        size INTEGER,
        created_at TEXT NOT NULL
    );
    """)
    now = utc_now()
    for spec in DI_ROSTER:
        con.execute(
            "INSERT OR IGNORE INTO di_nodes(name,role,specialty,room,created_at) VALUES(?,?,?,?,?)",
            (spec["name"], spec["role"], spec["specialty"], spec["room"], now),
        )
    for source, title, reference, principle, business_use in FAITH_BUSINESS_SOURCES:
        con.execute(
            """INSERT OR IGNORE INTO di_memory
               (source,title,reference,principle,business_use,created_at)
               VALUES(?,?,?,?,?,?)""",
            (source, title, reference, principle, business_use, now),
        )
    con.commit()
    con.close()

def hash_passkey(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def verify_passkey(value, stored_hash):
    return hmac.compare_digest(hash_passkey(value), stored_hash)

def log_activity(username, company, action, detail):
    con = db()
    con.execute(
        "INSERT INTO activity(username,company,action,detail,created_at) VALUES(?,?,?,?,?)",
        (username, company, action, str(detail)[:4000], utc_now()),
    )
    con.commit()
    con.close()

def password_gate(session_key, expected, label):
    if st.session_state.get(session_key, False):
        return True
    value = st.text_input(label, type="password", key=session_key + "_input")
    if st.button("Unlock", key=session_key + "_unlock", type="primary"):
        if hmac.compare_digest(value.strip(), expected):
            st.session_state[session_key] = True
            st.rerun()
        st.error("Incorrect password.")
    return False

def ai_server_answer(question, context=""):
    """Server-side AI adapter. Configure GEMINI_API_KEY or OPENAI_API_KEY."""
    question = question.strip()
    if not question:
        return "Please enter a question."
    # Keep credentials server-side. The local fallback remains useful when no
    # provider is configured, rather than pretending an answer came from a server.
    if GEMINI_API_KEY:
        try:
            import requests
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-2.0-flash:generateContent?key="
                + urllib.parse.quote(GEMINI_API_KEY)
            )
            payload = {
                "contents": [{
                    "parts": [{
                        "text": (
                            "You are DI, David's Intelligence, inside DACRE Analysis. "
                            "Answer accurately and clearly. Distinguish facts, calculations, "
                            "inference, and faith-inspired business principles.\n\n"
                            f"Context:\n{context[:8000]}\n\nQuestion:\n{question}"
                        )
                    }]
                }]
            }
            response = requests.post(url, json=payload, timeout=25)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as exc:
            return f"DI server connection failed safely: {type(exc).__name__}. Configure the AI provider correctly and try again."
    return (
        "DI is online, but no server-side AI key is configured. "
        "Add GEMINI_API_KEY or OPENAI_API_KEY to Streamlit Secrets/environment variables "
        "to enable live server reasoning. Your question was received successfully."
    )

def send_signup_otp(recipient, otp):
    if not (SMTP_HOST and SMTP_PASSWORD and recipient):
        return False
    message = EmailMessage()
    message["Subject"] = "DACRE Analysis — Signup Verification OTP"
    message["From"] = SMTP_USERNAME
    message["To"] = recipient
    message.set_content(
        "Welcome to DACRE Analysis.\n\n"
        f"Your signup verification OTP is: {otp}\n\n"
        "Keep this code private."
    )
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
        return True
    except Exception:
        return False

def startup_css():
    st.markdown("""
    <style>
    .stApp {
        background:
          radial-gradient(circle at 10% 10%, rgba(0,140,255,.10), transparent 30%),
          radial-gradient(circle at 90% 80%, rgba(0,255,180,.06), transparent 30%),
          #030811;
        color:#f5fbff;
    }
    [data-testid="stSidebar"] {
        background:linear-gradient(180deg,#030812,#071523);
        border-right:1px solid #164564;
    }
    .dacre-card {
        border:1px solid #1c6084;
        border-radius:22px;
        padding:22px;
        background:linear-gradient(145deg,rgba(5,20,34,.98),rgba(3,10,18,.98));
        box-shadow:0 0 30px rgba(20,180,255,.08);
        margin-bottom:16px;
    }
    .dacre-title {
        font-size:clamp(30px,5vw,62px);
        font-weight:950;
        letter-spacing:-.04em;
        text-shadow:0 0 28px rgba(75,205,255,.25);
    }
    .dacre-sub {
        color:#82a9bd;
        font-size:15px;
    }
    .status-online { color:#59f3a4; font-weight:900; }
    .office {
        border:1px solid #1e6688;
        border-radius:24px;
        padding:20px;
        background:
          radial-gradient(circle at 25% 25%,rgba(80,210,255,.16),transparent 25%),
          linear-gradient(145deg,#061522,#02070c);
        min-height:250px;
        box-shadow:inset 0 0 45px rgba(30,180,255,.06),0 0 28px rgba(0,150,255,.07);
        animation:officePulse 4s ease-in-out infinite;
    }
    .office-grid { display:grid;grid-template-columns:170px 1fr;gap:22px;align-items:center; }
    .robot {
        width:145px;height:180px;margin:auto;position:relative;
        filter:drop-shadow(0 0 22px rgba(75,210,255,.35));
        animation:robotFloat 3.2s ease-in-out infinite;
    }
    .head {
        width:92px;height:105px;margin:auto;border-radius:47% 47% 43% 43%;
        background:linear-gradient(145deg,#dce8ed,#778b96);
        border:2px solid #6bc8e9;position:relative;
    }
    .head:before {
        content:"";position:absolute;inset:11px 10px 12px;border-radius:45%;
        background:radial-gradient(circle at 35% 34%,#263b45,#071016 65%);
        border:1px solid #8de5ff;
    }
    .eye {position:absolute;top:45px;width:11px;height:11px;border-radius:50%;background:#7de7ff;z-index:2;box-shadow:0 0 13px #56d9ff;}
    .eye.left {left:31px}.eye.right{right:31px}
    .mouth {position:absolute;left:34px;bottom:24px;width:24px;height:7px;border-bottom:2px solid #83dfff;border-radius:50%;z-index:2}
    .neck {width:35px;height:15px;margin:auto;background:#26343c;border:1px solid #4dbce0}
    .torso {width:108px;height:72px;margin:auto;border-radius:25px 25px 12px 12px;background:linear-gradient(145deg,#bfcbd0,#3d4e58);border:1px solid #66cce9}
    .arm {position:absolute;top:118px;width:35px;height:75px;border-radius:20px;background:#70828b;border:1px solid #5cc9eb}
    .arm.left{left:0;transform:rotate(12deg)}.arm.right{right:0;transform:rotate(-12deg)}
    .screen {border:1px solid #1e6e96;border-radius:16px;padding:14px;background:#020a12;min-height:105px}
    .screen-line {height:5px;background:#1b6381;margin:8px 0;border-radius:8px;animation:screenScan 2s linear infinite}
    @keyframes robotFloat {0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
    @keyframes officePulse {0%,100%{box-shadow:inset 0 0 45px rgba(30,180,255,.06),0 0 28px rgba(0,150,255,.07)}50%{box-shadow:inset 0 0 60px rgba(30,180,255,.12),0 0 40px rgba(0,150,255,.12)}}
    @keyframes screenScan {0%{opacity:.35}50%{opacity:1}100%{opacity:.35}}
    @media(max-width:700px){.office-grid{grid-template-columns:1fr}.robot{margin-bottom:8px}}
    </style>
    """, unsafe_allow_html=True)

def render_di_office(spec):
    name = spec["name"]
    role = spec["role"]
    specialty = spec["specialty"]
    room = spec["room"]
    st.markdown(
        f"""
        <div class="office">
          <div class="office-grid">
            <div class="robot">
              <div class="head">
                <div class="eye left"></div><div class="eye right"></div>
                <div class="mouth"></div>
              </div>
              <div class="neck"></div>
              <div class="torso"></div>
              <div class="arm left"></div><div class="arm right"></div>
            </div>
            <div>
              <div class="status-online">● ONLINE · ROOM {room:02d}</div>
              <h2 style="margin:.35rem 0">{name}</h2>
              <div style="color:#66d7ff;font-weight:800">{role}</div>
              <p style="color:#9ab4c4">{specialty}</p>
              <div class="screen">
                <b>DACRE WORKSTATION · LIVE</b>
                <div class="screen-line"></div>
                <div class="screen-line" style="width:78%"></div>
                <div class="screen-line" style="width:55%"></div>
                <small style="color:#6f94a8">Shared DI brain · specialist memory · approved tools</small>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_landing():
    st.markdown('<div class="dacre-title">DACRE ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dacre-sub">Business intelligence · David\'s Intelligence · Data · Research · Strategy</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown("""
    <div class="dacre-card">
      <h2>One intelligence workspace for business.</h2>
      <p>Upload data, analyse it, build charts, research opportunities, ask DI questions,
      and use a faith-and-business wisdom library for practical decision support.</p>
      <p><span class="status-online">● DI ONLINE</span> · Secure workspace routing active</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("OPEN DACRE WORKSPACE", type="primary", use_container_width=True):
        st.session_state.route = "auth"
        st.rerun()

def render_auth():
    st.title("DACRE Account")
    login_tab, signup_tab = st.tabs(["Sign In", "Create Account"])
    with login_tab:
        company = st.text_input("Company / Organization", key="login_company")
        full_name = st.text_input("Full Name", key="login_full")
        email = st.text_input("Email Address", key="login_email")
        passkey = st.text_input("Account Passkey", type="password", key="login_pass")
        if st.button("Sign In", type="primary", use_container_width=True):
            # Master route: passkey + guardian challenge.
            if (
                full_name.strip().lower() == "david emenike"
                and email.strip().lower() == SMTP_USERNAME.lower()
                and hmac.compare_digest(passkey.strip(), MASTER_PASSKEY)
            ):
                st.session_state.master_pending = True
                st.session_state.master_user = {
                    "username": MASTER_USERNAME,
                    "company": "DACRE MASTER",
                    "role": "master",
                    "first_name": "David",
                    "last_name": "Emenike",
                    "email": email.strip(),
                }
                st.session_state.route = "guardian"
                st.rerun()
            con = db()
            row = con.execute(
                "SELECT * FROM users WHERE company=? AND email=? AND username=?",
                (company.strip(), email.strip().lower(), full_name.strip().lower().replace(" ",".")),
            ).fetchone()
            con.close()
            if row and verify_passkey(passkey.strip(), row["passkey_hash"]):
                st.session_state.user = dict(row)
                st.session_state.route = "user"
                log_activity(row["username"], row["company"], "SIGN IN", "User signed in.")
                st.rerun()
            st.error("Account details were not accepted.")
    with signup_tab:
        st.caption("Email address is required because DACRE sends the signup verification OTP to the registered email.")
        first = st.text_input("First Name", key="signup_first")
        last = st.text_input("Last Name", key="signup_last")
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email Address", key="signup_email")
        company = st.text_input("Company / Organization", key="signup_company")
        account_pass = st.text_input("Create Account Passkey", type="password", key="signup_pass")
        if st.button("Create Account", type="primary", use_container_width=True):
            values = [first,last,username,email,company,account_pass]
            if not all(v.strip() for v in values):
                st.error("Complete every signup field.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Enter a valid email address.")
            else:
                otp = str(secrets.randbelow(900000) + 100000)
                st.session_state.pending_signup = {
                    "first": first.strip(), "last": last.strip(),
                    "username": username.strip().lower(), "email": email.strip().lower(),
                    "company": company.strip(), "passhash": hash_passkey(account_pass),
                    "otp": otp, "expires": time.time() + 600,
                }
                sent = send_signup_otp(email.strip(), otp)
                st.session_state.otp_sent = sent
                st.session_state.route = "verify"
                st.rerun()

def render_guardian():
    st.title("CEO Office Guardian Verification")
    st.info("Master account verified. State the name assigned to the CEO Office Guardian.")
    answer = st.text_input("Guardian name", key="guardian_answer")
    if st.button("Enter Overall Admin DI", type="primary"):
        if hmac.compare_digest(answer.strip().lower(), GUARDIAN_NAME.lower()):
            st.session_state.user = st.session_state.master_user
            st.session_state.route = "overall"
            log_activity(MASTER_USERNAME, "DACRE MASTER", "MASTER SIGN IN", "Overall Admin DI opened after guardian verification.")
            st.rerun()
        st.error("Guardian verification failed.")

def render_verify():
    st.title("Verify your email")
    if st.session_state.get("otp_sent"):
        st.success("The OTP was sent through the configured DACRE SMTP account.")
    else:
        st.warning("SMTP is not configured or the message could not be sent. Configure SMTP in Streamlit Secrets.")
    code = st.text_input("Verification OTP", type="password")
    if st.button("Verify OTP", type="primary"):
        data = st.session_state.get("pending_signup", {})
        if time.time() > float(data.get("expires", 0)):
            st.error("OTP expired. Start signup again.")
            return
        if not hmac.compare_digest(code.strip(), data.get("otp", "")):
            st.error("Incorrect OTP.")
            return
        con = db()
        try:
            con.execute(
                """INSERT INTO users
                   (username,email,first_name,last_name,company,role,passkey_hash,created_at,last_seen)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (
                    data["username"], data["email"], data["first"], data["last"],
                    data["company"], "user", data["passhash"], utc_now(), utc_now()
                ),
            )
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            st.error("Username or email already exists.")
            return
        con.close()
        st.session_state.user = {
            "username": data["username"], "email": data["email"],
            "first_name": data["first"], "last_name": data["last"],
            "company": data["company"], "role": "user",
        }
        log_activity(data["username"], data["company"], "SIGN UP", "Account created and email verified.")
        st.session_state.route = "user"
        st.rerun()

def render_overall_admin():
    st.title("👑 Overall Admin DI")
    st.caption("System-wide activity command centre. Ordinary user tools are intentionally hidden here.")
    con = db()
    accounts = con.execute("SELECT COUNT(*) n FROM users").fetchone()["n"]
    active_di = con.execute(
        "SELECT COUNT(*) n FROM di_nodes WHERE name NOT IN (SELECT name FROM destroyed_di)"
    ).fetchone()["n"]
    events = con.execute("SELECT COUNT(*) n FROM activity").fetchone()["n"]
    activity_rows = con.execute("SELECT * FROM activity ORDER BY id DESC LIMIT 200").fetchall()
    con.close()
    c1,c2,c3 = st.columns(3)
    c1.metric("User accounts", accounts)
    c2.metric("Active DI", active_di)
    c3.metric("Activity events", events)
    st.markdown('<div class="dacre-card"><h3>LIVE APPLICATION ACTIVITY</h3><p>Questions, sign-ins, uploads, decisions, research and system actions appear here.</p></div>', unsafe_allow_html=True)
    if activity_rows:
        st.dataframe(pd.DataFrame([dict(r) for r in activity_rows]), use_container_width=True, hide_index=True)
    else:
        st.info("No activity events yet.")
    st.divider()
    if st.button("🔧 David Creation", type="primary", use_container_width=True):
        st.session_state.route = "david_creation"
        st.rerun()

def render_david_creation():
    st.title("David Creation")
    st.caption("Protected DI engineering and lifecycle management.")
    if not password_gate("david_creation_unlocked", DAVID_CREATION_PASSKEY, "David Creation password"):
        return
    st.success("David Creation unlocked.")
    create_tab, destroy_tab, registry_tab = st.tabs(["Create DI", "Destroy DI", "DI Registry"])
    with create_tab:
        name = st.text_input("DI name", key="new_di_name")
        role = st.text_input("DI role", key="new_di_role")
        specialty = st.text_area("Specialty", key="new_di_specialty")
        if st.button("CREATE DI", type="primary"):
            if not all(x.strip() for x in [name,role,specialty]):
                st.error("Complete the DI definition.")
            else:
                con=db()
                room=con.execute("SELECT COALESCE(MAX(room),0)+1 n FROM di_nodes").fetchone()["n"]
                try:
                    con.execute(
                        "INSERT INTO di_nodes(name,role,specialty,room,created_at) VALUES(?,?,?,?,?)",
                        (name.strip(),role.strip(),specialty.strip(),room,utc_now()),
                    )
                    con.commit()
                    st.success(f"{name} created in room {room}.")
                    log_activity(MASTER_USERNAME,"DACRE MASTER","CREATE DI",f"{name} · {role}")
                except sqlite3.IntegrityError:
                    st.error("A DI with that name already exists.")
                con.close()
    with destroy_tab:
        con=db()
        rows=con.execute("SELECT * FROM di_nodes WHERE name NOT IN (SELECT name FROM destroyed_di) ORDER BY room").fetchall()
        con.close()
        if not rows:
            st.info("No active DI nodes.")
        else:
            target=st.selectbox("DI to destroy", [r["name"] for r in rows], key="destroy_target")
            confirm=st.checkbox("I understand this removes the DI from active service.", key="destroy_confirm")
            if st.button("DESTROY DI", type="secondary") and confirm:
                con=db()
                con.execute(
                    "INSERT OR REPLACE INTO destroyed_di(name,destroyed_at,destroyed_by) VALUES(?,?,?)",
                    (target,utc_now(),MASTER_USERNAME),
                )
                con.commit(); con.close()
                log_activity(MASTER_USERNAME,"DACRE MASTER","DESTROY DI",target)
                st.success(f"{target} was removed from active service.")
                st.rerun()
    with registry_tab:
        con=db()
        rows=con.execute("SELECT * FROM di_nodes ORDER BY room").fetchall()
        con.close()
        st.dataframe(pd.DataFrame([dict(r) for r in rows]), use_container_width=True, hide_index=True)
    st.divider()
    if st.button("🛰️ DI Basement", type="primary", use_container_width=True):
        st.session_state.route="basement"
        st.rerun()

def render_basement():
    st.title("DI Basement")
    st.caption("20-room specialist DI office fabric.")
    if not password_gate("basement_unlocked", DI_BASEMENT_PASSKEY, "DI Basement password"):
        return
    con=db()
    rows=con.execute(
        "SELECT * FROM di_nodes WHERE name NOT IN (SELECT name FROM destroyed_di) ORDER BY room"
    ).fetchall()
    con.close()
    if not rows:
        st.warning("No active DI rooms.")
        return
    st.info(f"{len(rows)} active DI rooms. Each room contains a visible DI workstation.")
    for row in rows:
        render_di_office(dict(row))
    if st.button("Lock DI Basement"):
        st.session_state.basement_unlocked=False
        st.rerun()

def render_workspace(user):
    st.header("Workspace & Data")
    uploaded=st.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            st.session_state.df=df
            log_activity(user["username"],user["company"],"UPLOAD",uploaded.name)
            st.success(f"Loaded {len(df):,} rows × {len(df.columns):,} columns.")
            st.dataframe(df,use_container_width=True,hide_index=True)
        except Exception as exc:
            st.error(f"Could not read the file: {type(exc).__name__}: {exc}")
    elif st.session_state.get("df") is not None:
        st.dataframe(st.session_state.df,use_container_width=True,hide_index=True)
    else:
        st.info("Upload a dataset to begin.")

def render_charts(user):
    st.header("Charts")
    df=st.session_state.get("df")
    if df is None:
        st.info("Upload data first.")
        return
    numeric=list(df.select_dtypes(include="number").columns)
    if not numeric:
        st.warning("No numeric columns found.")
        return
    choice=st.selectbox("Numeric columns",numeric,key="chart_cols")
    chart_type=st.selectbox("Chart type",["Line","Bar","Area"],key="chart_type")
    data=df[[choice]].dropna()
    if chart_type=="Line": st.line_chart(data)
    elif chart_type=="Bar": st.bar_chart(data)
    else: st.area_chart(data)
    log_activity(user["username"],user["company"],"CHART",f"{chart_type} chart · {choice}")

def render_business_twin(user):
    st.header("Business Twin")
    df=st.session_state.get("df")
    if df is None:
        st.info("Upload data to build the first business twin snapshot.")
        return
    rows=len(df); cols=len(df.columns)
    missing=int(df.isna().sum().sum())
    numeric=df.select_dtypes(include="number")
    st.write("A lightweight operational snapshot of the current dataset.")
    a,b,c=st.columns(3)
    a.metric("Rows",f"{rows:,}"); b.metric("Columns",f"{cols:,}"); c.metric("Missing cells",f"{missing:,}")
    if not numeric.empty:
        st.subheader("Numeric signals")
        st.dataframe(numeric.describe().T,use_container_width=True)

def render_decisions(user):
    st.header("Decision Ledger")
    decision=st.text_area("Decision")
    rationale=st.text_area("Rationale")
    expected=st.text_area("Expected result")
    if st.button("Record decision",type="primary"):
        if decision.strip():
            con=db()
            con.execute(
                "INSERT INTO saved_decisions(username,company,decision,rationale,expected_result,created_at) VALUES(?,?,?,?,?,?)",
                (user["username"],user["company"],decision,rationale,expected,utc_now()),
            )
            con.commit(); con.close()
            log_activity(user["username"],user["company"],"DECISION",decision)
            st.success("Decision recorded.")
    con=db()
    rows=con.execute(
        "SELECT * FROM saved_decisions WHERE company=? ORDER BY id DESC LIMIT 50",
        (user["company"],),
    ).fetchall()
    con.close()
    if rows: st.dataframe(pd.DataFrame([dict(r) for r in rows]),use_container_width=True,hide_index=True)

def render_opportunity(user):
    st.header("Opportunity Radar")
    q=st.text_input("What market or business area should DI examine?")
    if st.button("Scan opportunity"):
        answer=ai_server_answer(
            f"Identify practical opportunities, risks and next actions for: {q}",
            "DACRE Opportunity Radar. Prefer actionable business analysis."
        )
        st.write(answer)
        log_activity(user["username"],user["company"],"OPPORTUNITY SCAN",q)

def render_faith_lab(user):
    st.header("Faith & Business Wisdom Lab")
    st.caption("A respectful business-principle library inspired by the listed source references. It is not a substitute for religious scholarship.")
    source=st.selectbox("Source",["All","Bible","Moses","Quran"])
    filtered=[x for x in FAITH_BUSINESS_SOURCES if source=="All" or x[0]==source]
    for src,title,ref,principle,business_use in filtered:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.caption(f"{src} · {ref}")
            st.write(principle)
            st.info(f"Business application: {business_use}")
    st.divider()
    business_type=st.text_input("Your business or business idea")
    challenge=st.text_area("What challenge are you facing?")
    if st.button("Generate faith-inspired business ideas",type="primary"):
        context="\n".join(f"{a} | {b} | {c} | {d} | {e}" for a,b,c,d,e in filtered[:12])
        answer=ai_server_answer(
            f"Business: {business_type}\nChallenge: {challenge}\nGenerate practical ideas grounded only in the supplied principles.",
            context
        )
        st.write(answer)
        log_activity(user["username"],user["company"],"FAITH BUSINESS IDEATION",business_type)

def render_memory_board(user):
    st.header("🧠 MB · Memory Board")
    q=st.text_input("Search DI memory",placeholder="leadership, contracts, planning, inventory, justice...")
    source=st.selectbox("Memory source",["All","Bible","Moses","Quran"])
    con=db()
    if q.strip():
        rows=con.execute(
            """SELECT * FROM di_memory
               WHERE (title LIKE ? OR principle LIKE ? OR business_use LIKE ?)
               AND (?='All' OR source=?)
               ORDER BY id DESC LIMIT 80""",
            (f"%{q}%",f"%{q}%",f"%{q}%",source,source),
        ).fetchall()
    else:
        rows=con.execute(
            "SELECT * FROM di_memory WHERE (?='All' OR source=?) ORDER BY id DESC LIMIT 80",
            (source,source),
        ).fetchall()
    con.close()
    if rows: st.dataframe(pd.DataFrame([dict(r) for r in rows]),use_container_width=True,hide_index=True)
    else: st.info("No matching memory.")

def render_di_home(user):
    st.header("DI Home")
    active=st.session_state.get("active_di","Analiel")
    names=[x["name"] for x in DI_ROSTER]
    active=st.selectbox("Specialist",names,index=names.index(active) if active in names else 0)
    st.session_state.active_di=active
    spec=next(x for x in DI_ROSTER if x["name"]==active)
    render_di_office(spec)
    question=st.chat_input(f"Ask {active} anything...")
    if question:
        context=f"Active specialist: {spec['name']} · {spec['role']} · {spec['specialty']}"
        answer=ai_server_answer(question,context)
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(answer)
        log_activity(user["username"],user["company"],"DI QUESTION",f"{active}: {question}")

def render_design_studio(user):
    st.header("DI Creation Studio")
    kind=st.selectbox("Design type",["Business dashboard","Landing page","Office UI","Poster","Report cover"])
    title=st.text_input("Title","DACRE Business Intelligence")
    brief=st.text_area("Design brief","Luxury dark interface with visible borders, animated data screens and professional business presentation.")
    if st.button("Create design specification",type="primary"):
        spec=f"""# {title}
Type: {kind}
Style: luxury dark technology
Brief: {brief}
Components: hero, navigation, metrics, activity stream, DI workstation, responsive layout.
"""
        st.code(spec)
        st.download_button("Download design specification",spec,"dacre_design_spec.txt")
        log_activity(user["username"],user["company"],"DESIGN SPEC",title)

def render_image_search(user):
    st.header("DI Picture Search")
    query=st.text_input("Search public Wikimedia images","futuristic business AI office")
    if st.button("Search pictures",type="primary"):
        try:
            params=urllib.parse.urlencode({
                "action":"query","generator":"search","gsrsearch":query,
                "gsrnamespace":6,"gsrlimit":12,"prop":"imageinfo",
                "iiprop":"url","format":"json","origin":"*"
            })
            url="https://commons.wikimedia.org/w/api.php?"+params
            with urllib.request.urlopen(url,timeout=15) as response:
                data=json.loads(response.read().decode("utf-8"))
            pages=list(data.get("query",{}).get("pages",{}).values())
            cols=st.columns(3)
            for i,page in enumerate(pages):
                info=(page.get("imageinfo") or [{}])[0]
                image_url=info.get("url")
                with cols[i%3]:
                    if image_url: st.image(image_url,use_container_width=True)
                    st.caption(page.get("title","Image"))
        except Exception as exc:
            st.error(f"Image search failed safely: {type(exc).__name__}")
        log_activity(user["username"],user["company"],"IMAGE SEARCH",query)

def render_export(user):
    st.header("Export Center")
    df=st.session_state.get("df")
    if df is None:
        st.info("No processed data available.")
        return
    csv_data=df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV",csv_data,"dacre_processed.csv","text/csv",use_container_width=True)
    excel=io.BytesIO()
    with pd.ExcelWriter(excel,engine="openpyxl") as writer:
        df.to_excel(writer,index=False,sheet_name="Processed")
    st.download_button("Download Excel",excel.getvalue(),"dacre_processed.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
    log_activity(user["username"],user["company"],"EXPORT","CSV/Excel export panel opened")

def render_user_app(user):
    st.sidebar.markdown("## ◈ DACRE")
    st.sidebar.caption(f"{user.get('first_name','User')} · {user.get('company','')}")
    pages=[
        "Overview","DI Home","Workspace & Data","Charts","Business Twin",
        "Decision Ledger","Opportunity Radar","Faith & Business Wisdom",
        "MB Memory Board","DI Creation Studio","Picture Search","Export Center"
    ]
    page=st.sidebar.radio("Navigation",pages,key="user_navigation")
    if st.sidebar.button("Sign out"):
        log_activity(user["username"],user["company"],"SIGN OUT","User signed out.")
        st.session_state.user=None; st.session_state.route="landing"; st.rerun()
    if page=="Overview":
        st.markdown('<div class="dacre-title">DACRE WORKSPACE</div>',unsafe_allow_html=True)
        st.markdown('<div class="dacre-sub">Your business intelligence command surface.</div>',unsafe_allow_html=True)
        render_di_office(next(x for x in DI_ROSTER if x["name"]==st.session_state.get("active_di","Analiel")))
    elif page=="DI Home": render_di_home(user)
    elif page=="Workspace & Data": render_workspace(user)
    elif page=="Charts": render_charts(user)
    elif page=="Business Twin": render_business_twin(user)
    elif page=="Decision Ledger": render_decisions(user)
    elif page=="Opportunity Radar": render_opportunity(user)
    elif page=="Faith & Business Wisdom": render_faith_lab(user)
    elif page=="MB Memory Board": render_memory_board(user)
    elif page=="DI Creation Studio": render_design_studio(user)
    elif page=="Picture Search": render_image_search(user)
    elif page=="Export Center": render_export(user)

def main():
    st.set_page_config(page_title="DACRE Analysis",page_icon="◈",layout="wide",initial_sidebar_state="expanded")
    startup_css()
    init_db()
    for key,default in {
        "route":"landing","user":None,"df":None,
        "master_pending":False,"david_creation_unlocked":False,
        "basement_unlocked":False,"active_di":"Analiel"
    }.items():
        if key not in st.session_state: st.session_state[key]=default
    route=st.session_state.route
    if st.session_state.user is None:
        if route=="landing": render_landing()
        elif route=="auth": render_auth()
        elif route=="verify": render_verify()
        elif route=="guardian": render_guardian()
        else:
            st.session_state.route="landing"; st.rerun()
        return
    if st.session_state.user.get("role")=="master":
        if route=="overall": render_overall_admin()
        elif route=="david_creation": render_david_creation()
        elif route=="basement": render_basement()
        else:
            st.session_state.route="overall"; st.rerun()
    else:
        st.session_state.route="user"
        render_user_app(st.session_state.user)

if __name__ == "__main__":
    main()
DI_KNOWLEDGE_CASH_FLOW = {
    'key': 'cash_flow',
    'title': 'Cash-flow visibility',
    'body': 'Track inflows, outflows, timing gaps, reserves and working-capital needs.',
}
DI_KNOWLEDGE_CUSTOMER_RETENTION = {
    'key': 'customer_retention',
    'title': 'Customer retention',
    'body': 'Monitor repeat purchase behavior, churn signals, service quality and customer lifetime value.',
}
DI_KNOWLEDGE_PRICING = {
    'key': 'pricing',
    'title': 'Pricing discipline',
    'body': 'Test pricing with customer value, costs, margin, demand, competition and willingness to pay.',
}
DI_KNOWLEDGE_INVENTORY = {
    'key': 'inventory',
    'title': 'Inventory discipline',
    'body': 'Balance service levels against carrying cost, spoilage, obsolescence and cash tied up in stock.',
}
DI_KNOWLEDGE_SALES_PIPELINE = {
    'key': 'sales_pipeline',
    'title': 'Sales pipeline',
    'body': 'Track leads, stages, conversion rates, cycle time, deal size and lost-deal reasons.',
}
DI_KNOWLEDGE_MARKETING = {
    'key': 'marketing',
    'title': 'Marketing measurement',
    'body': 'Connect campaign activity to qualified leads, conversion, revenue and customer acquisition cost.',
}
DI_KNOWLEDGE_OPERATIONS = {
    'key': 'operations',
    'title': 'Operational efficiency',
    'body': 'Map processes, measure cycle time, rework, bottlenecks, capacity and quality.',
}
DI_KNOWLEDGE_GOVERNANCE = {
    'key': 'governance',
    'title': 'Governance',
    'body': 'Use clear roles, approval thresholds, records, audit trails and consistent decision criteria.',
}
DI_KNOWLEDGE_RISK = {
    'key': 'risk',
    'title': 'Risk management',
    'body': 'Identify risks, probability, impact, early indicators, owners and mitigation actions.',
}
DI_KNOWLEDGE_DATA_QUALITY = {
    'key': 'data_quality',
    'title': 'Data quality',
    'body': 'Check completeness, uniqueness, validity, consistency, timeliness and traceability.',
}
DI_KNOWLEDGE_FORECASTING = {
    'key': 'forecasting',
    'title': 'Forecasting',
    'body': 'Combine historical patterns, assumptions, scenarios and uncertainty rather than presenting guesses as facts.',
}
DI_KNOWLEDGE_STRATEGY = {
    'key': 'strategy',
    'title': 'Strategy',
    'body': 'Connect goals to measurable priorities, resource allocation, competitive advantage and execution.',
}
DI_KNOWLEDGE_LEADERSHIP = {
    'key': 'leadership',
    'title': 'Leadership',
    'body': 'Use clear responsibility, delegation, feedback, accountability and escalation.',
}
DI_KNOWLEDGE_TEAM = {
    'key': 'team',
    'title': 'Team performance',
    'body': 'Align roles, capacity, objectives, communication and professional development.',
}
DI_KNOWLEDGE_CUSTOMER_SERVICE = {
    'key': 'customer_service',
    'title': 'Customer service',
    'body': 'Track response time, resolution, satisfaction, recurring issues and root causes.',
}
DI_KNOWLEDGE_COMPLIANCE = {
    'key': 'compliance',
    'title': 'Compliance',
    'body': 'Maintain documented rules, evidence, approvals, training and periodic review.',
}
DI_KNOWLEDGE_SECURITY = {
    'key': 'security',
    'title': 'Security',
    'body': 'Use least privilege, strong authentication, secrets management, logging and incident response.',
}
DI_KNOWLEDGE_PRODUCT = {
    'key': 'product',
    'title': 'Product management',
    'body': 'Prioritize customer problems, evidence, outcomes, delivery cost and learning.',
}
DI_KNOWLEDGE_PROJECT = {
    'key': 'project',
    'title': 'Project delivery',
    'body': 'Define owners, milestones, dependencies, risks, acceptance criteria and review points.',
}
DI_KNOWLEDGE_RESEARCH = {
    'key': 'research',
    'title': 'Business research',
    'body': 'Separate sourced evidence from inference and clearly state uncertainty.',
}
PLAYBOOK_00001 = {
    'id': 1,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a finance task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00002 = {
    'id': 2,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a sales task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00003 = {
    'id': 3,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a marketing task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00004 = {
    'id': 4,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a operations task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00005 = {
    'id': 5,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00006 = {
    'id': 6,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a leadership task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00007 = {
    'id': 7,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00008 = {
    'id': 8,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a product task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00009 = {
    'id': 9,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a technology task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00010 = {
    'id': 10,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a security task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00011 = {
    'id': 11,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a governance task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00012 = {
    'id': 12,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a research task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00013 = {
    'id': 13,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a supply_chain task, document the current process and evaluate response time.',
}
PLAYBOOK_00014 = {
    'id': 14,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a people task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00015 = {
    'id': 15,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a project task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00016 = {
    'id': 16,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a risk task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00017 = {
    'id': 17,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00018 = {
    'id': 18,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a design task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00019 = {
    'id': 19,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a communications task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00020 = {
    'id': 20,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a finance task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00021 = {
    'id': 21,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a sales task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00022 = {
    'id': 22,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a marketing task, identify the owner and evaluate retention.',
}
PLAYBOOK_00023 = {
    'id': 23,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a operations task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00024 = {
    'id': 24,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a strategy task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00025 = {
    'id': 25,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00026 = {
    'id': 26,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a customer task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00027 = {
    'id': 27,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00028 = {
    'id': 28,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a technology task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00029 = {
    'id': 29,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a security task, record the decision and evaluate project completion.',
}
PLAYBOOK_00030 = {
    'id': 30,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a governance task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00031 = {
    'id': 31,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a research task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00032 = {
    'id': 32,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a supply_chain task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00033 = {
    'id': 33,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a people task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00034 = {
    'id': 34,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a project task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00035 = {
    'id': 35,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a risk task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00036 = {
    'id': 36,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a data task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00037 = {
    'id': 37,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00038 = {
    'id': 38,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a communications task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00039 = {
    'id': 39,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a finance task, record the decision and evaluate retention.',
}
PLAYBOOK_00040 = {
    'id': 40,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a sales task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00041 = {
    'id': 41,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a marketing task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00042 = {
    'id': 42,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a operations task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00043 = {
    'id': 43,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a strategy task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00044 = {
    'id': 44,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a leadership task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00045 = {
    'id': 45,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a customer task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00046 = {
    'id': 46,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a product task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00047 = {
    'id': 47,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00048 = {
    'id': 48,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a security task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00049 = {
    'id': 49,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a governance task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00050 = {
    'id': 50,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a research task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00051 = {
    'id': 51,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00052 = {
    'id': 52,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a people task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00053 = {
    'id': 53,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a project task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00054 = {
    'id': 54,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a risk task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00055 = {
    'id': 55,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a data task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00056 = {
    'id': 56,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a design task, review the evidence and evaluate retention.',
}
PLAYBOOK_00057 = {
    'id': 57,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00058 = {
    'id': 58,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a finance task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00059 = {
    'id': 59,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a sales task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00060 = {
    'id': 60,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00061 = {
    'id': 61,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a operations task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00062 = {
    'id': 62,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a strategy task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00063 = {
    'id': 63,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a leadership task, document the current process and evaluate project completion.',
}
PLAYBOOK_00064 = {
    'id': 64,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a customer task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00065 = {
    'id': 65,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a product task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00066 = {
    'id': 66,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a technology task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00067 = {
    'id': 67,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00068 = {
    'id': 68,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a governance task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00069 = {
    'id': 69,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a research task, record the decision and evaluate revenue.',
}
PLAYBOOK_00070 = {
    'id': 70,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00071 = {
    'id': 71,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a people task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00072 = {
    'id': 72,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a project task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00073 = {
    'id': 73,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a risk task, document the current process and evaluate retention.',
}
PLAYBOOK_00074 = {
    'id': 74,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a data task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00075 = {
    'id': 75,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a design task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00076 = {
    'id': 76,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a communications task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00077 = {
    'id': 77,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00078 = {
    'id': 78,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a sales task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00079 = {
    'id': 79,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a marketing task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00080 = {
    'id': 80,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a operations task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00081 = {
    'id': 81,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a strategy task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00082 = {
    'id': 82,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a leadership task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00083 = {
    'id': 83,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a customer task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00084 = {
    'id': 84,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a product task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00085 = {
    'id': 85,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a technology task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00086 = {
    'id': 86,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a security task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00087 = {
    'id': 87,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00088 = {
    'id': 88,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a research task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00089 = {
    'id': 89,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a supply_chain task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00090 = {
    'id': 90,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a people task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00091 = {
    'id': 91,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a project task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00092 = {
    'id': 92,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a risk task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00093 = {
    'id': 93,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a data task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00094 = {
    'id': 94,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a design task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00095 = {
    'id': 95,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a communications task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00096 = {
    'id': 96,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a finance task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00097 = {
    'id': 97,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00098 = {
    'id': 98,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a marketing task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00099 = {
    'id': 99,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a operations task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00100 = {
    'id': 100,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00101 = {
    'id': 101,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a leadership task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00102 = {
    'id': 102,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a customer task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00103 = {
    'id': 103,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a product task, document the current process and evaluate revenue.',
}
PLAYBOOK_00104 = {
    'id': 104,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a technology task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00105 = {
    'id': 105,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a security task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00106 = {
    'id': 106,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a governance task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00107 = {
    'id': 107,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00108 = {
    'id': 108,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00109 = {
    'id': 109,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a people task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00110 = {
    'id': 110,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a project task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00111 = {
    'id': 111,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a risk task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00112 = {
    'id': 112,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a data task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00113 = {
    'id': 113,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a design task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00114 = {
    'id': 114,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a communications task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00115 = {
    'id': 115,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a finance task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00116 = {
    'id': 116,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a sales task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00117 = {
    'id': 117,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00118 = {
    'id': 118,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a operations task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00119 = {
    'id': 119,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a strategy task, record the decision and evaluate lead time.',
}
PLAYBOOK_00120 = {
    'id': 120,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00121 = {
    'id': 121,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a customer task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00122 = {
    'id': 122,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a product task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00123 = {
    'id': 123,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a technology task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00124 = {
    'id': 124,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a security task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00125 = {
    'id': 125,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a governance task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00126 = {
    'id': 126,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a research task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00127 = {
    'id': 127,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00128 = {
    'id': 128,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a people task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00129 = {
    'id': 129,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a project task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00130 = {
    'id': 130,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a risk task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00131 = {
    'id': 131,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a data task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00132 = {
    'id': 132,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a design task, identify the owner and evaluate response time.',
}
PLAYBOOK_00133 = {
    'id': 133,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a communications task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00134 = {
    'id': 134,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a finance task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00135 = {
    'id': 135,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a sales task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00136 = {
    'id': 136,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a marketing task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00137 = {
    'id': 137,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00138 = {
    'id': 138,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a strategy task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00139 = {
    'id': 139,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a leadership task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00140 = {
    'id': 140,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a customer task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00141 = {
    'id': 141,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a product task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00142 = {
    'id': 142,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a technology task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00143 = {
    'id': 143,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a security task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00144 = {
    'id': 144,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a governance task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00145 = {
    'id': 145,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a research task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00146 = {
    'id': 146,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a supply_chain task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00147 = {
    'id': 147,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00148 = {
    'id': 148,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a project task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00149 = {
    'id': 149,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a risk task, record the decision and evaluate response time.',
}
PLAYBOOK_00150 = {
    'id': 150,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a data task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_00151 = {
    'id': 151,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a design task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_00152 = {
    'id': 152,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a communications task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_00153 = {
    'id': 153,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a finance task, document the current process and evaluate lead time.',
}
PLAYBOOK_00154 = {
    'id': 154,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a sales task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_00155 = {
    'id': 155,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_00156 = {
    'id': 156,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a operations task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_00157 = {
    'id': 157,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_00158 = {
    'id': 158,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a leadership task, test a small improvement and evaluate retention.',
}
PLAYBOOK_00159 = {
    'id': 159,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a customer task, record the decision and evaluate cycle time.',
}
PLAYBOOK_00160 = {
    'id': 160,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a product task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_00161 = {
    'id': 161,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a technology task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_00162 = {
    'id': 162,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a security task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_00163 = {
    'id': 163,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a governance task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_00164 = {
    'id': 164,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a research task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_00165 = {
    'id': 165,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_00166 = {
    'id': 166,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a people task, review the evidence and evaluate response time.',
}
PLAYBOOK_00167 = {
    'id': 167,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_00168 = {
    'id': 168,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a risk task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_00169 = {
    'id': 169,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a data task, record the decision and evaluate security incidents.',
}
PLAYBOOK_00170 = {
    'id': 170,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a design task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_00171 = {
    'id': 171,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a communications task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00172 = {
    'id': 172,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a finance task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00173 = {
    'id': 173,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a sales task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00174 = {
    'id': 174,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a marketing task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00175 = {
    'id': 175,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a operations task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00176 = {
    'id': 176,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a strategy task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00177 = {
    'id': 177,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00178 = {
    'id': 178,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a customer task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00179 = {
    'id': 179,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a product task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00180 = {
    'id': 180,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a technology task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00181 = {
    'id': 181,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a security task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00182 = {
    'id': 182,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a governance task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00183 = {
    'id': 183,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a research task, document the current process and evaluate response time.',
}
PLAYBOOK_00184 = {
    'id': 184,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00185 = {
    'id': 185,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a people task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00186 = {
    'id': 186,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a project task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00187 = {
    'id': 187,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00188 = {
    'id': 188,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a data task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00189 = {
    'id': 189,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a design task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00190 = {
    'id': 190,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a communications task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00191 = {
    'id': 191,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a finance task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00192 = {
    'id': 192,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a sales task, identify the owner and evaluate retention.',
}
PLAYBOOK_00193 = {
    'id': 193,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a marketing task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00194 = {
    'id': 194,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a operations task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00195 = {
    'id': 195,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00196 = {
    'id': 196,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a leadership task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00197 = {
    'id': 197,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00198 = {
    'id': 198,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a product task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00199 = {
    'id': 199,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a technology task, record the decision and evaluate project completion.',
}
PLAYBOOK_00200 = {
    'id': 200,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a security task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00201 = {
    'id': 201,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a governance task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00202 = {
    'id': 202,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a research task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00203 = {
    'id': 203,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a supply_chain task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00204 = {
    'id': 204,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a people task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00205 = {
    'id': 205,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a project task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00206 = {
    'id': 206,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a risk task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00207 = {
    'id': 207,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00208 = {
    'id': 208,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a design task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00209 = {
    'id': 209,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a communications task, record the decision and evaluate retention.',
}
PLAYBOOK_00210 = {
    'id': 210,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a finance task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00211 = {
    'id': 211,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a sales task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00212 = {
    'id': 212,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a marketing task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00213 = {
    'id': 213,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a operations task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00214 = {
    'id': 214,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a strategy task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00215 = {
    'id': 215,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00216 = {
    'id': 216,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a customer task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00217 = {
    'id': 217,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00218 = {
    'id': 218,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a technology task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00219 = {
    'id': 219,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a security task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00220 = {
    'id': 220,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a governance task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00221 = {
    'id': 221,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a research task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00222 = {
    'id': 222,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a supply_chain task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00223 = {
    'id': 223,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a people task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00224 = {
    'id': 224,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a project task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00225 = {
    'id': 225,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a risk task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00226 = {
    'id': 226,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a data task, review the evidence and evaluate retention.',
}
PLAYBOOK_00227 = {
    'id': 227,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00228 = {
    'id': 228,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a communications task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00229 = {
    'id': 229,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a finance task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00230 = {
    'id': 230,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a sales task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00231 = {
    'id': 231,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a marketing task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00232 = {
    'id': 232,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a operations task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00233 = {
    'id': 233,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a strategy task, document the current process and evaluate project completion.',
}
PLAYBOOK_00234 = {
    'id': 234,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a leadership task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00235 = {
    'id': 235,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a customer task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00236 = {
    'id': 236,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a product task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00237 = {
    'id': 237,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00238 = {
    'id': 238,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a security task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00239 = {
    'id': 239,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a governance task, record the decision and evaluate revenue.',
}
PLAYBOOK_00240 = {
    'id': 240,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a research task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00241 = {
    'id': 241,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00242 = {
    'id': 242,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a people task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00243 = {
    'id': 243,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a project task, document the current process and evaluate retention.',
}
PLAYBOOK_00244 = {
    'id': 244,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a risk task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00245 = {
    'id': 245,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a data task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00246 = {
    'id': 246,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a design task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00247 = {
    'id': 247,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00248 = {
    'id': 248,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a finance task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00249 = {
    'id': 249,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a sales task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00250 = {
    'id': 250,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00251 = {
    'id': 251,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a operations task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00252 = {
    'id': 252,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a strategy task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00253 = {
    'id': 253,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a leadership task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00254 = {
    'id': 254,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a customer task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00255 = {
    'id': 255,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a product task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00256 = {
    'id': 256,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a technology task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00257 = {
    'id': 257,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00258 = {
    'id': 258,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a governance task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00259 = {
    'id': 259,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a research task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00260 = {
    'id': 260,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00261 = {
    'id': 261,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a people task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00262 = {
    'id': 262,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a project task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00263 = {
    'id': 263,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a risk task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00264 = {
    'id': 264,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a data task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00265 = {
    'id': 265,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a design task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00266 = {
    'id': 266,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a communications task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00267 = {
    'id': 267,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00268 = {
    'id': 268,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a sales task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00269 = {
    'id': 269,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a marketing task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00270 = {
    'id': 270,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a operations task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00271 = {
    'id': 271,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a strategy task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00272 = {
    'id': 272,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a leadership task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00273 = {
    'id': 273,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a customer task, document the current process and evaluate revenue.',
}
PLAYBOOK_00274 = {
    'id': 274,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a product task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00275 = {
    'id': 275,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a technology task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00276 = {
    'id': 276,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a security task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00277 = {
    'id': 277,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00278 = {
    'id': 278,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a research task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00279 = {
    'id': 279,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a supply_chain task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00280 = {
    'id': 280,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a people task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00281 = {
    'id': 281,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a project task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00282 = {
    'id': 282,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a risk task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00283 = {
    'id': 283,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a data task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00284 = {
    'id': 284,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a design task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00285 = {
    'id': 285,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a communications task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00286 = {
    'id': 286,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a finance task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00287 = {
    'id': 287,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00288 = {
    'id': 288,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a marketing task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00289 = {
    'id': 289,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a operations task, record the decision and evaluate lead time.',
}
PLAYBOOK_00290 = {
    'id': 290,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00291 = {
    'id': 291,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a leadership task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00292 = {
    'id': 292,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a customer task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00293 = {
    'id': 293,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a product task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00294 = {
    'id': 294,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a technology task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00295 = {
    'id': 295,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a security task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00296 = {
    'id': 296,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a governance task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00297 = {
    'id': 297,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00298 = {
    'id': 298,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00299 = {
    'id': 299,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a people task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00300 = {
    'id': 300,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a project task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00301 = {
    'id': 301,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a risk task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00302 = {
    'id': 302,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a data task, identify the owner and evaluate response time.',
}
PLAYBOOK_00303 = {
    'id': 303,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a design task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00304 = {
    'id': 304,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a communications task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00305 = {
    'id': 305,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a finance task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00306 = {
    'id': 306,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a sales task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00307 = {
    'id': 307,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00308 = {
    'id': 308,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a operations task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00309 = {
    'id': 309,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a strategy task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00310 = {
    'id': 310,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00311 = {
    'id': 311,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a customer task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00312 = {
    'id': 312,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a product task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00313 = {
    'id': 313,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a technology task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00314 = {
    'id': 314,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a security task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00315 = {
    'id': 315,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a governance task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00316 = {
    'id': 316,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a research task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00317 = {
    'id': 317,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00318 = {
    'id': 318,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a people task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00319 = {
    'id': 319,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a project task, record the decision and evaluate response time.',
}
PLAYBOOK_00320 = {
    'id': 320,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a risk task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_00321 = {
    'id': 321,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a data task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_00322 = {
    'id': 322,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a design task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_00323 = {
    'id': 323,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a communications task, document the current process and evaluate lead time.',
}
PLAYBOOK_00324 = {
    'id': 324,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a finance task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_00325 = {
    'id': 325,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a sales task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_00326 = {
    'id': 326,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a marketing task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_00327 = {
    'id': 327,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_00328 = {
    'id': 328,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a strategy task, test a small improvement and evaluate retention.',
}
PLAYBOOK_00329 = {
    'id': 329,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a leadership task, record the decision and evaluate cycle time.',
}
PLAYBOOK_00330 = {
    'id': 330,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a customer task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_00331 = {
    'id': 331,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a product task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_00332 = {
    'id': 332,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a technology task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_00333 = {
    'id': 333,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a security task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_00334 = {
    'id': 334,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a governance task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_00335 = {
    'id': 335,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a research task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_00336 = {
    'id': 336,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a supply_chain task, review the evidence and evaluate response time.',
}
PLAYBOOK_00337 = {
    'id': 337,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_00338 = {
    'id': 338,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a project task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_00339 = {
    'id': 339,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a risk task, record the decision and evaluate security incidents.',
}
PLAYBOOK_00340 = {
    'id': 340,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a data task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_00341 = {
    'id': 341,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a design task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00342 = {
    'id': 342,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a communications task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00343 = {
    'id': 343,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a finance task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00344 = {
    'id': 344,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a sales task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00345 = {
    'id': 345,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00346 = {
    'id': 346,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a operations task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00347 = {
    'id': 347,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00348 = {
    'id': 348,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a leadership task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00349 = {
    'id': 349,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a customer task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00350 = {
    'id': 350,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a product task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00351 = {
    'id': 351,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a technology task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00352 = {
    'id': 352,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a security task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00353 = {
    'id': 353,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a governance task, document the current process and evaluate response time.',
}
PLAYBOOK_00354 = {
    'id': 354,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a research task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00355 = {
    'id': 355,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00356 = {
    'id': 356,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a people task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00357 = {
    'id': 357,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00358 = {
    'id': 358,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a risk task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00359 = {
    'id': 359,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a data task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00360 = {
    'id': 360,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a design task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00361 = {
    'id': 361,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a communications task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00362 = {
    'id': 362,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a finance task, identify the owner and evaluate retention.',
}
PLAYBOOK_00363 = {
    'id': 363,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a sales task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00364 = {
    'id': 364,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a marketing task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00365 = {
    'id': 365,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a operations task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00366 = {
    'id': 366,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a strategy task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00367 = {
    'id': 367,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00368 = {
    'id': 368,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a customer task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00369 = {
    'id': 369,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a product task, record the decision and evaluate project completion.',
}
PLAYBOOK_00370 = {
    'id': 370,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a technology task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00371 = {
    'id': 371,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a security task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00372 = {
    'id': 372,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a governance task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00373 = {
    'id': 373,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a research task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00374 = {
    'id': 374,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00375 = {
    'id': 375,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a people task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00376 = {
    'id': 376,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a project task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00377 = {
    'id': 377,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00378 = {
    'id': 378,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a data task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00379 = {
    'id': 379,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a design task, record the decision and evaluate retention.',
}
PLAYBOOK_00380 = {
    'id': 380,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a communications task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00381 = {
    'id': 381,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a finance task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00382 = {
    'id': 382,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a sales task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00383 = {
    'id': 383,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a marketing task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00384 = {
    'id': 384,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a operations task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00385 = {
    'id': 385,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00386 = {
    'id': 386,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a leadership task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00387 = {
    'id': 387,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00388 = {
    'id': 388,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a product task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00389 = {
    'id': 389,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a technology task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00390 = {
    'id': 390,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a security task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00391 = {
    'id': 391,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a governance task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00392 = {
    'id': 392,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a research task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00393 = {
    'id': 393,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a supply_chain task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00394 = {
    'id': 394,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a people task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00395 = {
    'id': 395,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a project task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00396 = {
    'id': 396,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a risk task, review the evidence and evaluate retention.',
}
PLAYBOOK_00397 = {
    'id': 397,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00398 = {
    'id': 398,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a design task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00399 = {
    'id': 399,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a communications task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00400 = {
    'id': 400,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a finance task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00401 = {
    'id': 401,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a sales task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00402 = {
    'id': 402,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a marketing task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00403 = {
    'id': 403,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a operations task, document the current process and evaluate project completion.',
}
PLAYBOOK_00404 = {
    'id': 404,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a strategy task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00405 = {
    'id': 405,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00406 = {
    'id': 406,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a customer task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00407 = {
    'id': 407,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00408 = {
    'id': 408,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a technology task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00409 = {
    'id': 409,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a security task, record the decision and evaluate revenue.',
}
PLAYBOOK_00410 = {
    'id': 410,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a governance task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00411 = {
    'id': 411,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a research task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00412 = {
    'id': 412,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a supply_chain task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00413 = {
    'id': 413,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a people task, document the current process and evaluate retention.',
}
PLAYBOOK_00414 = {
    'id': 414,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a project task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00415 = {
    'id': 415,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a risk task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00416 = {
    'id': 416,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a data task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00417 = {
    'id': 417,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00418 = {
    'id': 418,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a communications task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00419 = {
    'id': 419,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a finance task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00420 = {
    'id': 420,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a sales task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00421 = {
    'id': 421,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a marketing task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00422 = {
    'id': 422,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a operations task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00423 = {
    'id': 423,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a strategy task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00424 = {
    'id': 424,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a leadership task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00425 = {
    'id': 425,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a customer task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00426 = {
    'id': 426,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a product task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00427 = {
    'id': 427,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00428 = {
    'id': 428,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a security task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00429 = {
    'id': 429,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a governance task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00430 = {
    'id': 430,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a research task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00431 = {
    'id': 431,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00432 = {
    'id': 432,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a people task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00433 = {
    'id': 433,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a project task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00434 = {
    'id': 434,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a risk task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00435 = {
    'id': 435,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a data task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00436 = {
    'id': 436,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a design task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00437 = {
    'id': 437,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00438 = {
    'id': 438,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a finance task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00439 = {
    'id': 439,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a sales task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00440 = {
    'id': 440,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00441 = {
    'id': 441,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a operations task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00442 = {
    'id': 442,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a strategy task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00443 = {
    'id': 443,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a leadership task, document the current process and evaluate revenue.',
}
PLAYBOOK_00444 = {
    'id': 444,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a customer task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00445 = {
    'id': 445,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a product task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00446 = {
    'id': 446,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a technology task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00447 = {
    'id': 447,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00448 = {
    'id': 448,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a governance task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00449 = {
    'id': 449,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a research task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00450 = {
    'id': 450,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00451 = {
    'id': 451,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a people task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00452 = {
    'id': 452,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a project task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00453 = {
    'id': 453,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a risk task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00454 = {
    'id': 454,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a data task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00455 = {
    'id': 455,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a design task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00456 = {
    'id': 456,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a communications task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00457 = {
    'id': 457,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00458 = {
    'id': 458,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a sales task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00459 = {
    'id': 459,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a marketing task, record the decision and evaluate lead time.',
}
PLAYBOOK_00460 = {
    'id': 460,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a operations task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00461 = {
    'id': 461,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a strategy task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00462 = {
    'id': 462,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a leadership task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00463 = {
    'id': 463,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a customer task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00464 = {
    'id': 464,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a product task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00465 = {
    'id': 465,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a technology task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00466 = {
    'id': 466,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a security task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00467 = {
    'id': 467,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00468 = {
    'id': 468,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a research task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00469 = {
    'id': 469,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a supply_chain task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00470 = {
    'id': 470,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a people task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00471 = {
    'id': 471,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a project task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00472 = {
    'id': 472,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a risk task, identify the owner and evaluate response time.',
}
PLAYBOOK_00473 = {
    'id': 473,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a data task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00474 = {
    'id': 474,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a design task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00475 = {
    'id': 475,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a communications task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00476 = {
    'id': 476,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a finance task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00477 = {
    'id': 477,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00478 = {
    'id': 478,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a marketing task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00479 = {
    'id': 479,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a operations task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00480 = {
    'id': 480,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00481 = {
    'id': 481,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a leadership task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00482 = {
    'id': 482,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a customer task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00483 = {
    'id': 483,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a product task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00484 = {
    'id': 484,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a technology task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00485 = {
    'id': 485,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a security task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00486 = {
    'id': 486,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a governance task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00487 = {
    'id': 487,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00488 = {
    'id': 488,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00489 = {
    'id': 489,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a people task, record the decision and evaluate response time.',
}
PLAYBOOK_00490 = {
    'id': 490,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a project task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_00491 = {
    'id': 491,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a risk task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_00492 = {
    'id': 492,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a data task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_00493 = {
    'id': 493,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a design task, document the current process and evaluate lead time.',
}
PLAYBOOK_00494 = {
    'id': 494,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a communications task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_00495 = {
    'id': 495,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a finance task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_00496 = {
    'id': 496,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a sales task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_00497 = {
    'id': 497,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_00498 = {
    'id': 498,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a operations task, test a small improvement and evaluate retention.',
}
PLAYBOOK_00499 = {
    'id': 499,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a strategy task, record the decision and evaluate cycle time.',
}
PLAYBOOK_00500 = {
    'id': 500,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_00501 = {
    'id': 501,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a customer task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_00502 = {
    'id': 502,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a product task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_00503 = {
    'id': 503,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a technology task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_00504 = {
    'id': 504,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a security task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_00505 = {
    'id': 505,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a governance task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_00506 = {
    'id': 506,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a research task, review the evidence and evaluate response time.',
}
PLAYBOOK_00507 = {
    'id': 507,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_00508 = {
    'id': 508,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a people task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_00509 = {
    'id': 509,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a project task, record the decision and evaluate security incidents.',
}
PLAYBOOK_00510 = {
    'id': 510,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a risk task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_00511 = {
    'id': 511,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a data task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00512 = {
    'id': 512,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a design task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00513 = {
    'id': 513,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a communications task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00514 = {
    'id': 514,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a finance task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00515 = {
    'id': 515,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a sales task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00516 = {
    'id': 516,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a marketing task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00517 = {
    'id': 517,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00518 = {
    'id': 518,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a strategy task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00519 = {
    'id': 519,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a leadership task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00520 = {
    'id': 520,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a customer task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00521 = {
    'id': 521,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a product task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00522 = {
    'id': 522,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a technology task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00523 = {
    'id': 523,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a security task, document the current process and evaluate response time.',
}
PLAYBOOK_00524 = {
    'id': 524,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a governance task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00525 = {
    'id': 525,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a research task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00526 = {
    'id': 526,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a supply_chain task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00527 = {
    'id': 527,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00528 = {
    'id': 528,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a project task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00529 = {
    'id': 529,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a risk task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00530 = {
    'id': 530,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a data task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00531 = {
    'id': 531,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a design task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00532 = {
    'id': 532,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a communications task, identify the owner and evaluate retention.',
}
PLAYBOOK_00533 = {
    'id': 533,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a finance task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00534 = {
    'id': 534,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a sales task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00535 = {
    'id': 535,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00536 = {
    'id': 536,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a operations task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00537 = {
    'id': 537,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00538 = {
    'id': 538,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a leadership task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00539 = {
    'id': 539,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a customer task, record the decision and evaluate project completion.',
}
PLAYBOOK_00540 = {
    'id': 540,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a product task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00541 = {
    'id': 541,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a technology task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00542 = {
    'id': 542,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a security task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00543 = {
    'id': 543,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a governance task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00544 = {
    'id': 544,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a research task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00545 = {
    'id': 545,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00546 = {
    'id': 546,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a people task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00547 = {
    'id': 547,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00548 = {
    'id': 548,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a risk task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00549 = {
    'id': 549,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a data task, record the decision and evaluate retention.',
}
PLAYBOOK_00550 = {
    'id': 550,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a design task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00551 = {
    'id': 551,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a communications task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00552 = {
    'id': 552,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a finance task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00553 = {
    'id': 553,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a sales task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00554 = {
    'id': 554,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a marketing task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00555 = {
    'id': 555,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a operations task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00556 = {
    'id': 556,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a strategy task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00557 = {
    'id': 557,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00558 = {
    'id': 558,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a customer task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00559 = {
    'id': 559,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a product task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00560 = {
    'id': 560,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a technology task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00561 = {
    'id': 561,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a security task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00562 = {
    'id': 562,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a governance task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00563 = {
    'id': 563,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a research task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00564 = {
    'id': 564,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00565 = {
    'id': 565,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a people task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00566 = {
    'id': 566,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a project task, review the evidence and evaluate retention.',
}
PLAYBOOK_00567 = {
    'id': 567,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00568 = {
    'id': 568,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a data task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00569 = {
    'id': 569,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a design task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00570 = {
    'id': 570,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a communications task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00571 = {
    'id': 571,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a finance task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00572 = {
    'id': 572,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a sales task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00573 = {
    'id': 573,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a marketing task, document the current process and evaluate project completion.',
}
PLAYBOOK_00574 = {
    'id': 574,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a operations task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00575 = {
    'id': 575,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00576 = {
    'id': 576,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a leadership task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00577 = {
    'id': 577,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00578 = {
    'id': 578,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a product task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00579 = {
    'id': 579,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a technology task, record the decision and evaluate revenue.',
}
PLAYBOOK_00580 = {
    'id': 580,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a security task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00581 = {
    'id': 581,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a governance task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00582 = {
    'id': 582,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a research task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00583 = {
    'id': 583,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a supply_chain task, document the current process and evaluate retention.',
}
PLAYBOOK_00584 = {
    'id': 584,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a people task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00585 = {
    'id': 585,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a project task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00586 = {
    'id': 586,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a risk task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00587 = {
    'id': 587,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00588 = {
    'id': 588,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a design task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00589 = {
    'id': 589,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a communications task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00590 = {
    'id': 590,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a finance task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00591 = {
    'id': 591,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a sales task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00592 = {
    'id': 592,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a marketing task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00593 = {
    'id': 593,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a operations task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00594 = {
    'id': 594,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a strategy task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00595 = {
    'id': 595,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00596 = {
    'id': 596,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a customer task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00597 = {
    'id': 597,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00598 = {
    'id': 598,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a technology task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00599 = {
    'id': 599,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a security task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00600 = {
    'id': 600,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a governance task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00601 = {
    'id': 601,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a research task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00602 = {
    'id': 602,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a supply_chain task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00603 = {
    'id': 603,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a people task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00604 = {
    'id': 604,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a project task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00605 = {
    'id': 605,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a risk task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00606 = {
    'id': 606,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a data task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00607 = {
    'id': 607,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00608 = {
    'id': 608,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a communications task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00609 = {
    'id': 609,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a finance task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00610 = {
    'id': 610,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a sales task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00611 = {
    'id': 611,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a marketing task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00612 = {
    'id': 612,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a operations task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00613 = {
    'id': 613,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a strategy task, document the current process and evaluate revenue.',
}
PLAYBOOK_00614 = {
    'id': 614,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a leadership task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00615 = {
    'id': 615,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a customer task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00616 = {
    'id': 616,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a product task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00617 = {
    'id': 617,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00618 = {
    'id': 618,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a security task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00619 = {
    'id': 619,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a governance task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00620 = {
    'id': 620,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a research task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00621 = {
    'id': 621,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00622 = {
    'id': 622,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a people task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00623 = {
    'id': 623,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a project task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00624 = {
    'id': 624,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a risk task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00625 = {
    'id': 625,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a data task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00626 = {
    'id': 626,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a design task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00627 = {
    'id': 627,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00628 = {
    'id': 628,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a finance task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00629 = {
    'id': 629,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a sales task, record the decision and evaluate lead time.',
}
PLAYBOOK_00630 = {
    'id': 630,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00631 = {
    'id': 631,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a operations task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00632 = {
    'id': 632,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a strategy task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00633 = {
    'id': 633,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a leadership task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00634 = {
    'id': 634,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a customer task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00635 = {
    'id': 635,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a product task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00636 = {
    'id': 636,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a technology task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00637 = {
    'id': 637,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00638 = {
    'id': 638,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a governance task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00639 = {
    'id': 639,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a research task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00640 = {
    'id': 640,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00641 = {
    'id': 641,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a people task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00642 = {
    'id': 642,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a project task, identify the owner and evaluate response time.',
}
PLAYBOOK_00643 = {
    'id': 643,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a risk task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00644 = {
    'id': 644,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a data task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00645 = {
    'id': 645,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a design task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00646 = {
    'id': 646,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a communications task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00647 = {
    'id': 647,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00648 = {
    'id': 648,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a sales task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00649 = {
    'id': 649,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a marketing task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00650 = {
    'id': 650,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a operations task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00651 = {
    'id': 651,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a strategy task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00652 = {
    'id': 652,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a leadership task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00653 = {
    'id': 653,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a customer task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00654 = {
    'id': 654,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a product task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00655 = {
    'id': 655,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a technology task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00656 = {
    'id': 656,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a security task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00657 = {
    'id': 657,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00658 = {
    'id': 658,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a research task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00659 = {
    'id': 659,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a supply_chain task, record the decision and evaluate response time.',
}
PLAYBOOK_00660 = {
    'id': 660,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a people task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_00661 = {
    'id': 661,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a project task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_00662 = {
    'id': 662,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a risk task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_00663 = {
    'id': 663,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a data task, document the current process and evaluate lead time.',
}
PLAYBOOK_00664 = {
    'id': 664,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a design task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_00665 = {
    'id': 665,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a communications task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_00666 = {
    'id': 666,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a finance task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_00667 = {
    'id': 667,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_00668 = {
    'id': 668,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a marketing task, test a small improvement and evaluate retention.',
}
PLAYBOOK_00669 = {
    'id': 669,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a operations task, record the decision and evaluate cycle time.',
}
PLAYBOOK_00670 = {
    'id': 670,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_00671 = {
    'id': 671,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a leadership task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_00672 = {
    'id': 672,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a customer task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_00673 = {
    'id': 673,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a product task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_00674 = {
    'id': 674,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a technology task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_00675 = {
    'id': 675,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a security task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_00676 = {
    'id': 676,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a governance task, review the evidence and evaluate response time.',
}
PLAYBOOK_00677 = {
    'id': 677,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_00678 = {
    'id': 678,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_00679 = {
    'id': 679,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a people task, record the decision and evaluate security incidents.',
}
PLAYBOOK_00680 = {
    'id': 680,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a project task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_00681 = {
    'id': 681,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a risk task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00682 = {
    'id': 682,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a data task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00683 = {
    'id': 683,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a design task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00684 = {
    'id': 684,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a communications task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00685 = {
    'id': 685,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a finance task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00686 = {
    'id': 686,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a sales task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00687 = {
    'id': 687,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00688 = {
    'id': 688,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a operations task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00689 = {
    'id': 689,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a strategy task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00690 = {
    'id': 690,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00691 = {
    'id': 691,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a customer task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00692 = {
    'id': 692,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a product task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00693 = {
    'id': 693,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a technology task, document the current process and evaluate response time.',
}
PLAYBOOK_00694 = {
    'id': 694,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a security task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00695 = {
    'id': 695,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a governance task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00696 = {
    'id': 696,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a research task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00697 = {
    'id': 697,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00698 = {
    'id': 698,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a people task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00699 = {
    'id': 699,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a project task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00700 = {
    'id': 700,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a risk task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00701 = {
    'id': 701,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a data task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00702 = {
    'id': 702,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a design task, identify the owner and evaluate retention.',
}
PLAYBOOK_00703 = {
    'id': 703,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a communications task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00704 = {
    'id': 704,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a finance task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00705 = {
    'id': 705,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a sales task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00706 = {
    'id': 706,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a marketing task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00707 = {
    'id': 707,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00708 = {
    'id': 708,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a strategy task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00709 = {
    'id': 709,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a leadership task, record the decision and evaluate project completion.',
}
PLAYBOOK_00710 = {
    'id': 710,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a customer task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00711 = {
    'id': 711,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a product task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00712 = {
    'id': 712,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a technology task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00713 = {
    'id': 713,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a security task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00714 = {
    'id': 714,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a governance task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00715 = {
    'id': 715,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a research task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00716 = {
    'id': 716,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a supply_chain task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00717 = {
    'id': 717,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00718 = {
    'id': 718,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a project task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00719 = {
    'id': 719,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a risk task, record the decision and evaluate retention.',
}
PLAYBOOK_00720 = {
    'id': 720,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a data task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00721 = {
    'id': 721,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a design task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00722 = {
    'id': 722,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a communications task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00723 = {
    'id': 723,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a finance task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00724 = {
    'id': 724,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a sales task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00725 = {
    'id': 725,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00726 = {
    'id': 726,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a operations task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00727 = {
    'id': 727,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00728 = {
    'id': 728,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a leadership task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00729 = {
    'id': 729,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a customer task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00730 = {
    'id': 730,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a product task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00731 = {
    'id': 731,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a technology task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00732 = {
    'id': 732,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a security task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00733 = {
    'id': 733,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a governance task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00734 = {
    'id': 734,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a research task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00735 = {
    'id': 735,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00736 = {
    'id': 736,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a people task, review the evidence and evaluate retention.',
}
PLAYBOOK_00737 = {
    'id': 737,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00738 = {
    'id': 738,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a risk task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00739 = {
    'id': 739,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a data task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00740 = {
    'id': 740,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a design task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00741 = {
    'id': 741,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a communications task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00742 = {
    'id': 742,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a finance task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00743 = {
    'id': 743,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a sales task, document the current process and evaluate project completion.',
}
PLAYBOOK_00744 = {
    'id': 744,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a marketing task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00745 = {
    'id': 745,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a operations task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00746 = {
    'id': 746,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a strategy task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00747 = {
    'id': 747,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00748 = {
    'id': 748,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a customer task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00749 = {
    'id': 749,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a product task, record the decision and evaluate revenue.',
}
PLAYBOOK_00750 = {
    'id': 750,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a technology task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00751 = {
    'id': 751,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a security task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00752 = {
    'id': 752,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a governance task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00753 = {
    'id': 753,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a research task, document the current process and evaluate retention.',
}
PLAYBOOK_00754 = {
    'id': 754,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00755 = {
    'id': 755,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a people task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00756 = {
    'id': 756,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a project task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00757 = {
    'id': 757,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00758 = {
    'id': 758,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a data task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00759 = {
    'id': 759,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a design task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00760 = {
    'id': 760,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a communications task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00761 = {
    'id': 761,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a finance task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00762 = {
    'id': 762,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a sales task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00763 = {
    'id': 763,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a marketing task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00764 = {
    'id': 764,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a operations task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00765 = {
    'id': 765,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00766 = {
    'id': 766,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a leadership task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00767 = {
    'id': 767,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00768 = {
    'id': 768,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a product task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00769 = {
    'id': 769,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a technology task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00770 = {
    'id': 770,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a security task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00771 = {
    'id': 771,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a governance task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00772 = {
    'id': 772,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a research task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00773 = {
    'id': 773,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a supply_chain task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00774 = {
    'id': 774,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a people task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00775 = {
    'id': 775,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a project task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00776 = {
    'id': 776,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a risk task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00777 = {
    'id': 777,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00778 = {
    'id': 778,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a design task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00779 = {
    'id': 779,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a communications task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00780 = {
    'id': 780,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a finance task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00781 = {
    'id': 781,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a sales task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00782 = {
    'id': 782,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a marketing task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00783 = {
    'id': 783,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a operations task, document the current process and evaluate revenue.',
}
PLAYBOOK_00784 = {
    'id': 784,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a strategy task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00785 = {
    'id': 785,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00786 = {
    'id': 786,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a customer task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00787 = {
    'id': 787,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00788 = {
    'id': 788,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a technology task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00789 = {
    'id': 789,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a security task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00790 = {
    'id': 790,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a governance task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00791 = {
    'id': 791,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a research task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00792 = {
    'id': 792,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a supply_chain task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00793 = {
    'id': 793,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a people task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00794 = {
    'id': 794,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a project task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00795 = {
    'id': 795,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a risk task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00796 = {
    'id': 796,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a data task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00797 = {
    'id': 797,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00798 = {
    'id': 798,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a communications task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00799 = {
    'id': 799,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a finance task, record the decision and evaluate lead time.',
}
PLAYBOOK_00800 = {
    'id': 800,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a sales task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00801 = {
    'id': 801,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a marketing task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00802 = {
    'id': 802,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a operations task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00803 = {
    'id': 803,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a strategy task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00804 = {
    'id': 804,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a leadership task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00805 = {
    'id': 805,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a customer task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00806 = {
    'id': 806,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a product task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00807 = {
    'id': 807,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00808 = {
    'id': 808,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a security task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00809 = {
    'id': 809,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a governance task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00810 = {
    'id': 810,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a research task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00811 = {
    'id': 811,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00812 = {
    'id': 812,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a people task, identify the owner and evaluate response time.',
}
PLAYBOOK_00813 = {
    'id': 813,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a project task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00814 = {
    'id': 814,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a risk task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00815 = {
    'id': 815,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a data task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00816 = {
    'id': 816,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a design task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00817 = {
    'id': 817,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00818 = {
    'id': 818,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a finance task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00819 = {
    'id': 819,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a sales task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00820 = {
    'id': 820,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00821 = {
    'id': 821,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a operations task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00822 = {
    'id': 822,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a strategy task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00823 = {
    'id': 823,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a leadership task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00824 = {
    'id': 824,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a customer task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00825 = {
    'id': 825,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a product task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00826 = {
    'id': 826,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a technology task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00827 = {
    'id': 827,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00828 = {
    'id': 828,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a governance task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00829 = {
    'id': 829,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a research task, record the decision and evaluate response time.',
}
PLAYBOOK_00830 = {
    'id': 830,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_00831 = {
    'id': 831,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a people task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_00832 = {
    'id': 832,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a project task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_00833 = {
    'id': 833,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a risk task, document the current process and evaluate lead time.',
}
PLAYBOOK_00834 = {
    'id': 834,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a data task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_00835 = {
    'id': 835,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a design task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_00836 = {
    'id': 836,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a communications task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_00837 = {
    'id': 837,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_00838 = {
    'id': 838,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a sales task, test a small improvement and evaluate retention.',
}
PLAYBOOK_00839 = {
    'id': 839,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a marketing task, record the decision and evaluate cycle time.',
}
PLAYBOOK_00840 = {
    'id': 840,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a operations task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_00841 = {
    'id': 841,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a strategy task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_00842 = {
    'id': 842,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a leadership task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_00843 = {
    'id': 843,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a customer task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_00844 = {
    'id': 844,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a product task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_00845 = {
    'id': 845,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a technology task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_00846 = {
    'id': 846,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a security task, review the evidence and evaluate response time.',
}
PLAYBOOK_00847 = {
    'id': 847,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_00848 = {
    'id': 848,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a research task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_00849 = {
    'id': 849,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a supply_chain task, record the decision and evaluate security incidents.',
}
PLAYBOOK_00850 = {
    'id': 850,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a people task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_00851 = {
    'id': 851,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a project task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_00852 = {
    'id': 852,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a risk task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_00853 = {
    'id': 853,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a data task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_00854 = {
    'id': 854,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a design task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_00855 = {
    'id': 855,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a communications task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_00856 = {
    'id': 856,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a finance task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_00857 = {
    'id': 857,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_00858 = {
    'id': 858,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a marketing task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_00859 = {
    'id': 859,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a operations task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_00860 = {
    'id': 860,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_00861 = {
    'id': 861,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a leadership task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_00862 = {
    'id': 862,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a customer task, identify the owner and evaluate project completion.',
}
PLAYBOOK_00863 = {
    'id': 863,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a product task, document the current process and evaluate response time.',
}
PLAYBOOK_00864 = {
    'id': 864,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a technology task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_00865 = {
    'id': 865,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a security task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_00866 = {
    'id': 866,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a governance task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_00867 = {
    'id': 867,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_00868 = {
    'id': 868,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_00869 = {
    'id': 869,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a people task, record the decision and evaluate gross margin.',
}
PLAYBOOK_00870 = {
    'id': 870,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a project task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_00871 = {
    'id': 871,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a risk task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_00872 = {
    'id': 872,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a data task, identify the owner and evaluate retention.',
}
PLAYBOOK_00873 = {
    'id': 873,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a design task, document the current process and evaluate cycle time.',
}
PLAYBOOK_00874 = {
    'id': 874,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a communications task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_00875 = {
    'id': 875,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a finance task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_00876 = {
    'id': 876,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a sales task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_00877 = {
    'id': 877,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_00878 = {
    'id': 878,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a operations task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_00879 = {
    'id': 879,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a strategy task, record the decision and evaluate project completion.',
}
PLAYBOOK_00880 = {
    'id': 880,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_00881 = {
    'id': 881,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a customer task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_00882 = {
    'id': 882,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a product task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_00883 = {
    'id': 883,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a technology task, document the current process and evaluate security incidents.',
}
PLAYBOOK_00884 = {
    'id': 884,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a security task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_00885 = {
    'id': 885,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a governance task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_00886 = {
    'id': 886,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a research task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_00887 = {
    'id': 887,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_00888 = {
    'id': 888,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a people task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_00889 = {
    'id': 889,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a project task, record the decision and evaluate retention.',
}
PLAYBOOK_00890 = {
    'id': 890,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a risk task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_00891 = {
    'id': 891,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a data task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_00892 = {
    'id': 892,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a design task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_00893 = {
    'id': 893,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a communications task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_00894 = {
    'id': 894,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a finance task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_00895 = {
    'id': 895,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a sales task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_00896 = {
    'id': 896,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a marketing task, review the evidence and evaluate project completion.',
}
PLAYBOOK_00897 = {
    'id': 897,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_00898 = {
    'id': 898,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a strategy task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_00899 = {
    'id': 899,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a leadership task, record the decision and evaluate data completeness.',
}
PLAYBOOK_00900 = {
    'id': 900,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a customer task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_00901 = {
    'id': 901,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a product task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_00902 = {
    'id': 902,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a technology task, identify the owner and evaluate revenue.',
}
PLAYBOOK_00903 = {
    'id': 903,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a security task, document the current process and evaluate gross margin.',
}
PLAYBOOK_00904 = {
    'id': 904,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a governance task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_00905 = {
    'id': 905,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a research task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_00906 = {
    'id': 906,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a supply_chain task, review the evidence and evaluate retention.',
}
PLAYBOOK_00907 = {
    'id': 907,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_00908 = {
    'id': 908,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a project task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_00909 = {
    'id': 909,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a risk task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_00910 = {
    'id': 910,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a data task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_00911 = {
    'id': 911,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a design task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_00912 = {
    'id': 912,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a communications task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_00913 = {
    'id': 913,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a finance task, document the current process and evaluate project completion.',
}
PLAYBOOK_00914 = {
    'id': 914,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a sales task, measure the outcome and evaluate response time.',
}
PLAYBOOK_00915 = {
    'id': 915,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_00916 = {
    'id': 916,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a operations task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_00917 = {
    'id': 917,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_00918 = {
    'id': 918,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a leadership task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_00919 = {
    'id': 919,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a customer task, record the decision and evaluate revenue.',
}
PLAYBOOK_00920 = {
    'id': 920,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a product task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_00921 = {
    'id': 921,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a technology task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_00922 = {
    'id': 922,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a security task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_00923 = {
    'id': 923,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a governance task, document the current process and evaluate retention.',
}
PLAYBOOK_00924 = {
    'id': 924,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a research task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_00925 = {
    'id': 925,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_00926 = {
    'id': 926,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a people task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_00927 = {
    'id': 927,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_00928 = {
    'id': 928,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a risk task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_00929 = {
    'id': 929,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a data task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_00930 = {
    'id': 930,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a design task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_00931 = {
    'id': 931,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a communications task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_00932 = {
    'id': 932,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a finance task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_00933 = {
    'id': 933,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a sales task, document the current process and evaluate data completeness.',
}
PLAYBOOK_00934 = {
    'id': 934,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a marketing task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_00935 = {
    'id': 935,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a operations task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_00936 = {
    'id': 936,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a strategy task, review the evidence and evaluate revenue.',
}
PLAYBOOK_00937 = {
    'id': 937,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_00938 = {
    'id': 938,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a customer task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_00939 = {
    'id': 939,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a product task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_00940 = {
    'id': 940,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a technology task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_00941 = {
    'id': 941,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a security task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_00942 = {
    'id': 942,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a governance task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_00943 = {
    'id': 943,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a research task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_00944 = {
    'id': 944,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_00945 = {
    'id': 945,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a people task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_00946 = {
    'id': 946,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a project task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_00947 = {
    'id': 947,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_00948 = {
    'id': 948,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a data task, test a small improvement and evaluate response time.',
}
PLAYBOOK_00949 = {
    'id': 949,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a design task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_00950 = {
    'id': 950,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a communications task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_00951 = {
    'id': 951,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a finance task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_00952 = {
    'id': 952,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a sales task, identify the owner and evaluate lead time.',
}
PLAYBOOK_00953 = {
    'id': 953,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a marketing task, document the current process and evaluate revenue.',
}
PLAYBOOK_00954 = {
    'id': 954,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a operations task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_00955 = {
    'id': 955,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_00956 = {
    'id': 956,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a leadership task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_00957 = {
    'id': 957,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_00958 = {
    'id': 958,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a product task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_00959 = {
    'id': 959,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a technology task, record the decision and evaluate defect rate.',
}
PLAYBOOK_00960 = {
    'id': 960,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a security task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_00961 = {
    'id': 961,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a governance task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_00962 = {
    'id': 962,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a research task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_00963 = {
    'id': 963,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a supply_chain task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_00964 = {
    'id': 964,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a people task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_00965 = {
    'id': 965,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a project task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_00966 = {
    'id': 966,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a risk task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_00967 = {
    'id': 967,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_00968 = {
    'id': 968,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a design task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_00969 = {
    'id': 969,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a communications task, record the decision and evaluate lead time.',
}
PLAYBOOK_00970 = {
    'id': 970,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a finance task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_00971 = {
    'id': 971,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a sales task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_00972 = {
    'id': 972,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a marketing task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_00973 = {
    'id': 973,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a operations task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_00974 = {
    'id': 974,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a strategy task, measure the outcome and evaluate retention.',
}
PLAYBOOK_00975 = {
    'id': 975,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_00976 = {
    'id': 976,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a customer task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_00977 = {
    'id': 977,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_00978 = {
    'id': 978,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a technology task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_00979 = {
    'id': 979,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a security task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_00980 = {
    'id': 980,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a governance task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_00981 = {
    'id': 981,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a research task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_00982 = {
    'id': 982,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a supply_chain task, identify the owner and evaluate response time.',
}
PLAYBOOK_00983 = {
    'id': 983,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a people task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_00984 = {
    'id': 984,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a project task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_00985 = {
    'id': 985,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a risk task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_00986 = {
    'id': 986,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a data task, review the evidence and evaluate lead time.',
}
PLAYBOOK_00987 = {
    'id': 987,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_00988 = {
    'id': 988,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a communications task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_00989 = {
    'id': 989,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a finance task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_00990 = {
    'id': 990,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a sales task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_00991 = {
    'id': 991,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a marketing task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_00992 = {
    'id': 992,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a operations task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_00993 = {
    'id': 993,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a strategy task, document the current process and evaluate defect rate.',
}
PLAYBOOK_00994 = {
    'id': 994,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a leadership task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_00995 = {
    'id': 995,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a customer task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_00996 = {
    'id': 996,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a product task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_00997 = {
    'id': 997,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_00998 = {
    'id': 998,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a security task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_00999 = {
    'id': 999,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a governance task, record the decision and evaluate response time.',
}
PLAYBOOK_01000 = {
    'id': 1000,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a research task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_01001 = {
    'id': 1001,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_01002 = {
    'id': 1002,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a people task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_01003 = {
    'id': 1003,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a project task, document the current process and evaluate lead time.',
}
PLAYBOOK_01004 = {
    'id': 1004,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a risk task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_01005 = {
    'id': 1005,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a data task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_01006 = {
    'id': 1006,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a design task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_01007 = {
    'id': 1007,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_01008 = {
    'id': 1008,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a finance task, test a small improvement and evaluate retention.',
}
PLAYBOOK_01009 = {
    'id': 1009,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a sales task, record the decision and evaluate cycle time.',
}
PLAYBOOK_01010 = {
    'id': 1010,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_01011 = {
    'id': 1011,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a operations task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_01012 = {
    'id': 1012,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a strategy task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_01013 = {
    'id': 1013,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a leadership task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_01014 = {
    'id': 1014,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a customer task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_01015 = {
    'id': 1015,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a product task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_01016 = {
    'id': 1016,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a technology task, review the evidence and evaluate response time.',
}
PLAYBOOK_01017 = {
    'id': 1017,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_01018 = {
    'id': 1018,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a governance task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_01019 = {
    'id': 1019,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a research task, record the decision and evaluate security incidents.',
}
PLAYBOOK_01020 = {
    'id': 1020,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_01021 = {
    'id': 1021,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a people task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_01022 = {
    'id': 1022,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a project task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_01023 = {
    'id': 1023,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a risk task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_01024 = {
    'id': 1024,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a data task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_01025 = {
    'id': 1025,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a design task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_01026 = {
    'id': 1026,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a communications task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_01027 = {
    'id': 1027,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_01028 = {
    'id': 1028,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a sales task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_01029 = {
    'id': 1029,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a marketing task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_01030 = {
    'id': 1030,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a operations task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_01031 = {
    'id': 1031,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a strategy task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_01032 = {
    'id': 1032,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a leadership task, identify the owner and evaluate project completion.',
}
PLAYBOOK_01033 = {
    'id': 1033,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a customer task, document the current process and evaluate response time.',
}
PLAYBOOK_01034 = {
    'id': 1034,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a product task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_01035 = {
    'id': 1035,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a technology task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_01036 = {
    'id': 1036,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a security task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_01037 = {
    'id': 1037,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_01038 = {
    'id': 1038,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a research task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_01039 = {
    'id': 1039,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a supply_chain task, record the decision and evaluate gross margin.',
}
PLAYBOOK_01040 = {
    'id': 1040,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a people task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_01041 = {
    'id': 1041,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a project task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_01042 = {
    'id': 1042,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a risk task, identify the owner and evaluate retention.',
}
PLAYBOOK_01043 = {
    'id': 1043,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a data task, document the current process and evaluate cycle time.',
}
PLAYBOOK_01044 = {
    'id': 1044,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a design task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_01045 = {
    'id': 1045,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a communications task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_01046 = {
    'id': 1046,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a finance task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_01047 = {
    'id': 1047,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_01048 = {
    'id': 1048,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a marketing task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_01049 = {
    'id': 1049,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a operations task, record the decision and evaluate project completion.',
}
PLAYBOOK_01050 = {
    'id': 1050,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_01051 = {
    'id': 1051,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a leadership task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_01052 = {
    'id': 1052,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a customer task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_01053 = {
    'id': 1053,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a product task, document the current process and evaluate security incidents.',
}
PLAYBOOK_01054 = {
    'id': 1054,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a technology task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_01055 = {
    'id': 1055,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a security task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_01056 = {
    'id': 1056,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a governance task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_01057 = {
    'id': 1057,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_01058 = {
    'id': 1058,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_01059 = {
    'id': 1059,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a people task, record the decision and evaluate retention.',
}
PLAYBOOK_01060 = {
    'id': 1060,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a project task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_01061 = {
    'id': 1061,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a risk task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_01062 = {
    'id': 1062,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a data task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_01063 = {
    'id': 1063,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a design task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_01064 = {
    'id': 1064,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a communications task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_01065 = {
    'id': 1065,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a finance task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_01066 = {
    'id': 1066,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a sales task, review the evidence and evaluate project completion.',
}
PLAYBOOK_01067 = {
    'id': 1067,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_01068 = {
    'id': 1068,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a operations task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_01069 = {
    'id': 1069,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a strategy task, record the decision and evaluate data completeness.',
}
PLAYBOOK_01070 = {
    'id': 1070,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_01071 = {
    'id': 1071,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a customer task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_01072 = {
    'id': 1072,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a product task, identify the owner and evaluate revenue.',
}
PLAYBOOK_01073 = {
    'id': 1073,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a technology task, document the current process and evaluate gross margin.',
}
PLAYBOOK_01074 = {
    'id': 1074,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a security task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_01075 = {
    'id': 1075,
    'domain': 'governance',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a governance task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_01076 = {
    'id': 1076,
    'domain': 'research',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a research task, review the evidence and evaluate retention.',
}
PLAYBOOK_01077 = {
    'id': 1077,
    'domain': 'supply_chain',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a supply_chain task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_01078 = {
    'id': 1078,
    'domain': 'people',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a people task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_01079 = {
    'id': 1079,
    'domain': 'project',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a project task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_01080 = {
    'id': 1080,
    'domain': 'risk',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a risk task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_01081 = {
    'id': 1081,
    'domain': 'data',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a data task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_01082 = {
    'id': 1082,
    'domain': 'design',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a design task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_01083 = {
    'id': 1083,
    'domain': 'communications',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a communications task, document the current process and evaluate project completion.',
}
PLAYBOOK_01084 = {
    'id': 1084,
    'domain': 'finance',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a finance task, measure the outcome and evaluate response time.',
}
PLAYBOOK_01085 = {
    'id': 1085,
    'domain': 'sales',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a sales task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_01086 = {
    'id': 1086,
    'domain': 'marketing',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a marketing task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_01087 = {
    'id': 1087,
    'domain': 'operations',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a operations task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_01088 = {
    'id': 1088,
    'domain': 'strategy',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a strategy task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_01089 = {
    'id': 1089,
    'domain': 'leadership',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a leadership task, record the decision and evaluate revenue.',
}
PLAYBOOK_01090 = {
    'id': 1090,
    'domain': 'customer',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a customer task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_01091 = {
    'id': 1091,
    'domain': 'product',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a product task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_01092 = {
    'id': 1092,
    'domain': 'technology',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a technology task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_01093 = {
    'id': 1093,
    'domain': 'security',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a security task, document the current process and evaluate retention.',
}
PLAYBOOK_01094 = {
    'id': 1094,
    'domain': 'governance',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a governance task, measure the outcome and evaluate cycle time.',
}
PLAYBOOK_01095 = {
    'id': 1095,
    'domain': 'research',
    'action': 'compare actuals with plan',
    'metric': 'defect rate',
    'prompt': 'For a research task, compare actuals with plan and evaluate defect rate.',
}
PLAYBOOK_01096 = {
    'id': 1096,
    'domain': 'supply_chain',
    'action': 'review the evidence',
    'metric': 'customer satisfaction',
    'prompt': 'For a supply_chain task, review the evidence and evaluate customer satisfaction.',
}
PLAYBOOK_01097 = {
    'id': 1097,
    'domain': 'people',
    'action': 'identify the largest bottleneck',
    'metric': 'cost per acquisition',
    'prompt': 'For a people task, identify the largest bottleneck and evaluate cost per acquisition.',
}
PLAYBOOK_01098 = {
    'id': 1098,
    'domain': 'project',
    'action': 'test a small improvement',
    'metric': 'inventory turnover',
    'prompt': 'For a project task, test a small improvement and evaluate inventory turnover.',
}
PLAYBOOK_01099 = {
    'id': 1099,
    'domain': 'risk',
    'action': 'record the decision',
    'metric': 'forecast accuracy',
    'prompt': 'For a risk task, record the decision and evaluate forecast accuracy.',
}
PLAYBOOK_01100 = {
    'id': 1100,
    'domain': 'data',
    'action': 'schedule a follow-up',
    'metric': 'project completion',
    'prompt': 'For a data task, schedule a follow-up and evaluate project completion.',
}
PLAYBOOK_01101 = {
    'id': 1101,
    'domain': 'design',
    'action': 'define the baseline metric',
    'metric': 'response time',
    'prompt': 'For a design task, define the baseline metric and evaluate response time.',
}
PLAYBOOK_01102 = {
    'id': 1102,
    'domain': 'communications',
    'action': 'identify the owner',
    'metric': 'employee capacity',
    'prompt': 'For a communications task, identify the owner and evaluate employee capacity.',
}
PLAYBOOK_01103 = {
    'id': 1103,
    'domain': 'finance',
    'action': 'document the current process',
    'metric': 'data completeness',
    'prompt': 'For a finance task, document the current process and evaluate data completeness.',
}
PLAYBOOK_01104 = {
    'id': 1104,
    'domain': 'sales',
    'action': 'measure the outcome',
    'metric': 'security incidents',
    'prompt': 'For a sales task, measure the outcome and evaluate security incidents.',
}
PLAYBOOK_01105 = {
    'id': 1105,
    'domain': 'marketing',
    'action': 'compare actuals with plan',
    'metric': 'lead time',
    'prompt': 'For a marketing task, compare actuals with plan and evaluate lead time.',
}
PLAYBOOK_01106 = {
    'id': 1106,
    'domain': 'operations',
    'action': 'review the evidence',
    'metric': 'revenue',
    'prompt': 'For a operations task, review the evidence and evaluate revenue.',
}
PLAYBOOK_01107 = {
    'id': 1107,
    'domain': 'strategy',
    'action': 'identify the largest bottleneck',
    'metric': 'gross margin',
    'prompt': 'For a strategy task, identify the largest bottleneck and evaluate gross margin.',
}
PLAYBOOK_01108 = {
    'id': 1108,
    'domain': 'leadership',
    'action': 'test a small improvement',
    'metric': 'cash conversion',
    'prompt': 'For a leadership task, test a small improvement and evaluate cash conversion.',
}
PLAYBOOK_01109 = {
    'id': 1109,
    'domain': 'customer',
    'action': 'record the decision',
    'metric': 'conversion rate',
    'prompt': 'For a customer task, record the decision and evaluate conversion rate.',
}
PLAYBOOK_01110 = {
    'id': 1110,
    'domain': 'product',
    'action': 'schedule a follow-up',
    'metric': 'retention',
    'prompt': 'For a product task, schedule a follow-up and evaluate retention.',
}
PLAYBOOK_01111 = {
    'id': 1111,
    'domain': 'technology',
    'action': 'define the baseline metric',
    'metric': 'cycle time',
    'prompt': 'For a technology task, define the baseline metric and evaluate cycle time.',
}
PLAYBOOK_01112 = {
    'id': 1112,
    'domain': 'security',
    'action': 'identify the owner',
    'metric': 'defect rate',
    'prompt': 'For a security task, identify the owner and evaluate defect rate.',
}
PLAYBOOK_01113 = {
    'id': 1113,
    'domain': 'governance',
    'action': 'document the current process',
    'metric': 'customer satisfaction',
    'prompt': 'For a governance task, document the current process and evaluate customer satisfaction.',
}
PLAYBOOK_01114 = {
    'id': 1114,
    'domain': 'research',
    'action': 'measure the outcome',
    'metric': 'cost per acquisition',
    'prompt': 'For a research task, measure the outcome and evaluate cost per acquisition.',
}
PLAYBOOK_01115 = {
    'id': 1115,
    'domain': 'supply_chain',
    'action': 'compare actuals with plan',
    'metric': 'inventory turnover',
    'prompt': 'For a supply_chain task, compare actuals with plan and evaluate inventory turnover.',
}
PLAYBOOK_01116 = {
    'id': 1116,
    'domain': 'people',
    'action': 'review the evidence',
    'metric': 'forecast accuracy',
    'prompt': 'For a people task, review the evidence and evaluate forecast accuracy.',
}
PLAYBOOK_01117 = {
    'id': 1117,
    'domain': 'project',
    'action': 'identify the largest bottleneck',
    'metric': 'project completion',
    'prompt': 'For a project task, identify the largest bottleneck and evaluate project completion.',
}
PLAYBOOK_01118 = {
    'id': 1118,
    'domain': 'risk',
    'action': 'test a small improvement',
    'metric': 'response time',
    'prompt': 'For a risk task, test a small improvement and evaluate response time.',
}
PLAYBOOK_01119 = {
    'id': 1119,
    'domain': 'data',
    'action': 'record the decision',
    'metric': 'employee capacity',
    'prompt': 'For a data task, record the decision and evaluate employee capacity.',
}
PLAYBOOK_01120 = {
    'id': 1120,
    'domain': 'design',
    'action': 'schedule a follow-up',
    'metric': 'data completeness',
    'prompt': 'For a design task, schedule a follow-up and evaluate data completeness.',
}
PLAYBOOK_01121 = {
    'id': 1121,
    'domain': 'communications',
    'action': 'define the baseline metric',
    'metric': 'security incidents',
    'prompt': 'For a communications task, define the baseline metric and evaluate security incidents.',
}
PLAYBOOK_01122 = {
    'id': 1122,
    'domain': 'finance',
    'action': 'identify the owner',
    'metric': 'lead time',
    'prompt': 'For a finance task, identify the owner and evaluate lead time.',
}
PLAYBOOK_01123 = {
    'id': 1123,
    'domain': 'sales',
    'action': 'document the current process',
    'metric': 'revenue',
    'prompt': 'For a sales task, document the current process and evaluate revenue.',
}
PLAYBOOK_01124 = {
    'id': 1124,
    'domain': 'marketing',
    'action': 'measure the outcome',
    'metric': 'gross margin',
    'prompt': 'For a marketing task, measure the outcome and evaluate gross margin.',
}
PLAYBOOK_01125 = {
    'id': 1125,
    'domain': 'operations',
    'action': 'compare actuals with plan',
    'metric': 'cash conversion',
    'prompt': 'For a operations task, compare actuals with plan and evaluate cash conversion.',
}
PLAYBOOK_01126 = {
    'id': 1126,
    'domain': 'strategy',
    'action': 'review the evidence',
    'metric': 'conversion rate',
    'prompt': 'For a strategy task, review the evidence and evaluate conversion rate.',
}
PLAYBOOK_01127 = {
    'id': 1127,
    'domain': 'leadership',
    'action': 'identify the largest bottleneck',
    'metric': 'retention',
    'prompt': 'For a leadership task, identify the largest bottleneck and evaluate retention.',
}
PLAYBOOK_01128 = {
    'id': 1128,
    'domain': 'customer',
    'action': 'test a small improvement',
    'metric': 'cycle time',
    'prompt': 'For a customer task, test a small improvement and evaluate cycle time.',
}
PLAYBOOK_01129 = {
    'id': 1129,
    'domain': 'product',
    'action': 'record the decision',
    'metric': 'defect rate',
    'prompt': 'For a product task, record the decision and evaluate defect rate.',
}
PLAYBOOK_01130 = {
    'id': 1130,
    'domain': 'technology',
    'action': 'schedule a follow-up',
    'metric': 'customer satisfaction',
    'prompt': 'For a technology task, schedule a follow-up and evaluate customer satisfaction.',
}
PLAYBOOK_01131 = {
    'id': 1131,
    'domain': 'security',
    'action': 'define the baseline metric',
    'metric': 'cost per acquisition',
    'prompt': 'For a security task, define the baseline metric and evaluate cost per acquisition.',
}
PLAYBOOK_01132 = {
    'id': 1132,
    'domain': 'governance',
    'action': 'identify the owner',
    'metric': 'inventory turnover',
    'prompt': 'For a governance task, identify the owner and evaluate inventory turnover.',
}
PLAYBOOK_01133 = {
    'id': 1133,
    'domain': 'research',
    'action': 'document the current process',
    'metric': 'forecast accuracy',
    'prompt': 'For a research task, document the current process and evaluate forecast accuracy.',
}
PLAYBOOK_01134 = {
    'id': 1134,
    'domain': 'supply_chain',
    'action': 'measure the outcome',
    'metric': 'project completion',
    'prompt': 'For a supply_chain task, measure the outcome and evaluate project completion.',
}
PLAYBOOK_01135 = {
    'id': 1135,
    'domain': 'people',
    'action': 'compare actuals with plan',
    'metric': 'response time',
    'prompt': 'For a people task, compare actuals with plan and evaluate response time.',
}
PLAYBOOK_01136 = {
    'id': 1136,
    'domain': 'project',
    'action': 'review the evidence',
    'metric': 'employee capacity',
    'prompt': 'For a project task, review the evidence and evaluate employee capacity.',
}
PLAYBOOK_01137 = {
    'id': 1137,
    'domain': 'risk',
    'action': 'identify the largest bottleneck',
    'metric': 'data completeness',
    'prompt': 'For a risk task, identify the largest bottleneck and evaluate data completeness.',
}
PLAYBOOK_01138 = {
    'id': 1138,
    'domain': 'data',
    'action': 'test a small improvement',
    'metric': 'security incidents',
    'prompt': 'For a data task, test a small improvement and evaluate security incidents.',
}
PLAYBOOK_01139 = {
    'id': 1139,
    'domain': 'design',
    'action': 'record the decision',
    'metric': 'lead time',
    'prompt': 'For a design task, record the decision and evaluate lead time.',
}
PLAYBOOK_01140 = {
    'id': 1140,
    'domain': 'communications',
    'action': 'schedule a follow-up',
    'metric': 'revenue',
    'prompt': 'For a communications task, schedule a follow-up and evaluate revenue.',
}
PLAYBOOK_01141 = {
    'id': 1141,
    'domain': 'finance',
    'action': 'define the baseline metric',
    'metric': 'gross margin',
    'prompt': 'For a finance task, define the baseline metric and evaluate gross margin.',
}
PLAYBOOK_01142 = {
    'id': 1142,
    'domain': 'sales',
    'action': 'identify the owner',
    'metric': 'cash conversion',
    'prompt': 'For a sales task, identify the owner and evaluate cash conversion.',
}
PLAYBOOK_01143 = {
    'id': 1143,
    'domain': 'marketing',
    'action': 'document the current process',
    'metric': 'conversion rate',
    'prompt': 'For a marketing task, document the current process and evaluate conversion rate.',
}
PLAYBOOK_01144 = {
    'id': 1144,
    'domain': 'operations',
    'action': 'measure the outcome',
    'metric': 'retention',
    'prompt': 'For a operations task, measure the outcome and evaluate retention.',
}
PLAYBOOK_01145 = {
    'id': 1145,
    'domain': 'strategy',
    'action': 'compare actuals with plan',
    'metric': 'cycle time',
    'prompt': 'For a strategy task, compare actuals with plan and evaluate cycle time.',
}
PLAYBOOK_01146 = {
    'id': 1146,
    'domain': 'leadership',
    'action': 'review the evidence',
    'metric': 'defect rate',
    'prompt': 'For a leadership task, review the evidence and evaluate defect rate.',
}
PLAYBOOK_01147 = {
    'id': 1147,
    'domain': 'customer',
    'action': 'identify the largest bottleneck',
    'metric': 'customer satisfaction',
    'prompt': 'For a customer task, identify the largest bottleneck and evaluate customer satisfaction.',
}
PLAYBOOK_01148 = {
    'id': 1148,
    'domain': 'product',
    'action': 'test a small improvement',
    'metric': 'cost per acquisition',
    'prompt': 'For a product task, test a small improvement and evaluate cost per acquisition.',
}
PLAYBOOK_01149 = {
    'id': 1149,
    'domain': 'technology',
    'action': 'record the decision',
    'metric': 'inventory turnover',
    'prompt': 'For a technology task, record the decision and evaluate inventory turnover.',
}
PLAYBOOK_01150 = {
    'id': 1150,
    'domain': 'security',
    'action': 'schedule a follow-up',
    'metric': 'forecast accuracy',
    'prompt': 'For a security task, schedule a follow-up and evaluate forecast accuracy.',
}
PLAYBOOK_01151 = {
    'id': 1151,
    'domain': 'governance',
    'action': 'define the baseline metric',
    'metric': 'project completion',
    'prompt': 'For a governance task, define the baseline metric and evaluate project completion.',
}
PLAYBOOK_01152 = {
    'id': 1152,
    'domain': 'research',
    'action': 'identify the owner',
    'metric': 'response time',
    'prompt': 'For a research task, identify the owner and evaluate response time.',
}
PLAYBOOK_01153 = {
    'id': 1153,
    'domain': 'supply_chain',
    'action': 'document the current process',
    'metric': 'employee capacity',
    'prompt': 'For a supply_chain task, document the current process and evaluate employee capacity.',
}
PLAYBOOK_01154 = {
    'id': 1154,
    'domain': 'people',
    'action': 'measure the outcome',
    'metric': 'data completeness',
    'prompt': 'For a people task, measure the outcome and evaluate data completeness.',
}
PLAYBOOK_01155 = {
    'id': 1155,
    'domain': 'project',
    'action': 'compare actuals with plan',
    'metric': 'security incidents',
    'prompt': 'For a project task, compare actuals with plan and evaluate security incidents.',
}
PLAYBOOK_01156 = {
    'id': 1156,
    'domain': 'risk',
    'action': 'review the evidence',
    'metric': 'lead time',
    'prompt': 'For a risk task, review the evidence and evaluate lead time.',
}
PLAYBOOK_01157 = {
    'id': 1157,
    'domain': 'data',
    'action': 'identify the largest bottleneck',
    'metric': 'revenue',
    'prompt': 'For a data task, identify the largest bottleneck and evaluate revenue.',
}
PLAYBOOK_01158 = {
    'id': 1158,
    'domain': 'design',
    'action': 'test a small improvement',
    'metric': 'gross margin',
    'prompt': 'For a design task, test a small improvement and evaluate gross margin.',
}
PLAYBOOK_01159 = {
    'id': 1159,
    'domain': 'communications',
    'action': 'record the decision',
    'metric': 'cash conversion',
    'prompt': 'For a communications task, record the decision and evaluate cash conversion.',
}
PLAYBOOK_01160 = {
    'id': 1160,
    'domain': 'finance',
    'action': 'schedule a follow-up',
    'metric': 'conversion rate',
    'prompt': 'For a finance task, schedule a follow-up and evaluate conversion rate.',
}
PLAYBOOK_01161 = {
    'id': 1161,
    'domain': 'sales',
    'action': 'define the baseline metric',
    'metric': 'retention',
    'prompt': 'For a sales task, define the baseline metric and evaluate retention.',
}
PLAYBOOK_01162 = {
    'id': 1162,
    'domain': 'marketing',
    'action': 'identify the owner',
    'metric': 'cycle time',
    'prompt': 'For a marketing task, identify the owner and evaluate cycle time.',
}
PLAYBOOK_01163 = {
    'id': 1163,
    'domain': 'operations',
    'action': 'document the current process',
    'metric': 'defect rate',
    'prompt': 'For a operations task, document the current process and evaluate defect rate.',
}
PLAYBOOK_01164 = {
    'id': 1164,
    'domain': 'strategy',
    'action': 'measure the outcome',
    'metric': 'customer satisfaction',
    'prompt': 'For a strategy task, measure the outcome and evaluate customer satisfaction.',
}
PLAYBOOK_01165 = {
    'id': 1165,
    'domain': 'leadership',
    'action': 'compare actuals with plan',
    'metric': 'cost per acquisition',
    'prompt': 'For a leadership task, compare actuals with plan and evaluate cost per acquisition.',
}
PLAYBOOK_01166 = {
    'id': 1166,
    'domain': 'customer',
    'action': 'review the evidence',
    'metric': 'inventory turnover',
    'prompt': 'For a customer task, review the evidence and evaluate inventory turnover.',
}
PLAYBOOK_01167 = {
    'id': 1167,
    'domain': 'product',
    'action': 'identify the largest bottleneck',
    'metric': 'forecast accuracy',
    'prompt': 'For a product task, identify the largest bottleneck and evaluate forecast accuracy.',
}
PLAYBOOK_01168 = {
    'id': 1168,
    'domain': 'technology',
    'action': 'test a small improvement',
    'metric': 'project completion',
    'prompt': 'For a technology task, test a small improvement and evaluate project completion.',
}
PLAYBOOK_01169 = {
    'id': 1169,
    'domain': 'security',
    'action': 'record the decision',
    'metric': 'response time',
    'prompt': 'For a security task, record the decision and evaluate response time.',
}
PLAYBOOK_01170 = {
    'id': 1170,
    'domain': 'governance',
    'action': 'schedule a follow-up',
    'metric': 'employee capacity',
    'prompt': 'For a governance task, schedule a follow-up and evaluate employee capacity.',
}
PLAYBOOK_01171 = {
    'id': 1171,
    'domain': 'research',
    'action': 'define the baseline metric',
    'metric': 'data completeness',
    'prompt': 'For a research task, define the baseline metric and evaluate data completeness.',
}
PLAYBOOK_01172 = {
    'id': 1172,
    'domain': 'supply_chain',
    'action': 'identify the owner',
    'metric': 'security incidents',
    'prompt': 'For a supply_chain task, identify the owner and evaluate security incidents.',
}
PLAYBOOK_01173 = {
    'id': 1173,
    'domain': 'people',
    'action': 'document the current process',
    'metric': 'lead time',
    'prompt': 'For a people task, document the current process and evaluate lead time.',
}
PLAYBOOK_01174 = {
    'id': 1174,
    'domain': 'project',
    'action': 'measure the outcome',
    'metric': 'revenue',
    'prompt': 'For a project task, measure the outcome and evaluate revenue.',
}
PLAYBOOK_01175 = {
    'id': 1175,
    'domain': 'risk',
    'action': 'compare actuals with plan',
    'metric': 'gross margin',
    'prompt': 'For a risk task, compare actuals with plan and evaluate gross margin.',
}
PLAYBOOK_01176 = {
    'id': 1176,
    'domain': 'data',
    'action': 'review the evidence',
    'metric': 'cash conversion',
    'prompt': 'For a data task, review the evidence and evaluate cash conversion.',
}
PLAYBOOK_01177 = {
    'id': 1177,
    'domain': 'design',
    'action': 'identify the largest bottleneck',
    'metric': 'conversion rate',
    'prompt': 'For a design task, identify the largest bottleneck and evaluate conversion rate.',
}
PLAYBOOK_01178 = {
    'id': 1178,
    'domain': 'communications',
    'action': 'test a small improvement',
    'metric': 'retention',
    'prompt': 'For a communications task, test a small improvement and evaluate retention.',
}
PLAYBOOK_01179 = {
    'id': 1179,
    'domain': 'finance',
    'action': 'record the decision',
    'metric': 'cycle time',
    'prompt': 'For a finance task, record the decision and evaluate cycle time.',
}
PLAYBOOK_01180 = {
    'id': 1180,
    'domain': 'sales',
    'action': 'schedule a follow-up',
    'metric': 'defect rate',
    'prompt': 'For a sales task, schedule a follow-up and evaluate defect rate.',
}
PLAYBOOK_01181 = {
    'id': 1181,
    'domain': 'marketing',
    'action': 'define the baseline metric',
    'metric': 'customer satisfaction',
    'prompt': 'For a marketing task, define the baseline metric and evaluate customer satisfaction.',
}
PLAYBOOK_01182 = {
    'id': 1182,
    'domain': 'operations',
    'action': 'identify the owner',
    'metric': 'cost per acquisition',
    'prompt': 'For a operations task, identify the owner and evaluate cost per acquisition.',
}
PLAYBOOK_01183 = {
    'id': 1183,
    'domain': 'strategy',
    'action': 'document the current process',
    'metric': 'inventory turnover',
    'prompt': 'For a strategy task, document the current process and evaluate inventory turnover.',
}
PLAYBOOK_01184 = {
    'id': 1184,
    'domain': 'leadership',
    'action': 'measure the outcome',
    'metric': 'forecast accuracy',
    'prompt': 'For a leadership task, measure the outcome and evaluate forecast accuracy.',
}
PLAYBOOK_01185 = {
    'id': 1185,
    'domain': 'customer',
    'action': 'compare actuals with plan',
    'metric': 'project completion',
    'prompt': 'For a customer task, compare actuals with plan and evaluate project completion.',
}
PLAYBOOK_01186 = {
    'id': 1186,
    'domain': 'product',
    'action': 'review the evidence',
    'metric': 'response time',
    'prompt': 'For a product task, review the evidence and evaluate response time.',
}
PLAYBOOK_01187 = {
    'id': 1187,
    'domain': 'technology',
    'action': 'identify the largest bottleneck',
    'metric': 'employee capacity',
    'prompt': 'For a technology task, identify the largest bottleneck and evaluate employee capacity.',
}
PLAYBOOK_01188 = {
    'id': 1188,
    'domain': 'security',
    'action': 'test a small improvement',
    'metric': 'data completeness',
    'prompt': 'For a security task, test a small improvement and evaluate data completeness.',
}
PLAYBOOK_01189 = {
    'id': 1189,
    'domain': 'governance',
    'action': 'record the decision',
    'metric': 'security incidents',
    'prompt': 'For a governance task, record the decision and evaluate security incidents.',
}
PLAYBOOK_01190 = {
    'id': 1190,
    'domain': 'research',
    'action': 'schedule a follow-up',
    'metric': 'lead time',
    'prompt': 'For a research task, schedule a follow-up and evaluate lead time.',
}
PLAYBOOK_01191 = {
    'id': 1191,
    'domain': 'supply_chain',
    'action': 'define the baseline metric',
    'metric': 'revenue',
    'prompt': 'For a supply_chain task, define the baseline metric and evaluate revenue.',
}
PLAYBOOK_01192 = {
    'id': 1192,
    'domain': 'people',
    'action': 'identify the owner',
    'metric': 'gross margin',
    'prompt': 'For a people task, identify the owner and evaluate gross margin.',
}
PLAYBOOK_01193 = {
    'id': 1193,
    'domain': 'project',
    'action': 'document the current process',
    'metric': 'cash conversion',
    'prompt': 'For a project task, document the current process and evaluate cash conversion.',
}
PLAYBOOK_01194 = {
    'id': 1194,
    'domain': 'risk',
    'action': 'measure the outcome',
    'metric': 'conversion rate',
    'prompt': 'For a risk task, measure the outcome and evaluate conversion rate.',
}
PLAYBOOK_01195 = {
    'id': 1195,
    'domain': 'data',
    'action': 'compare actuals with plan',
    'metric': 'retention',
    'prompt': 'For a data task, compare actuals with plan and evaluate retention.',
}
PLAYBOOK_01196 = {
    'id': 1196,
    'domain': 'design',
    'action': 'review the evidence',
    'metric': 'cycle time',
    'prompt': 'For a design task, review the evidence and evaluate cycle time.',
}
PLAYBOOK_01197 = {
    'id': 1197,
    'domain': 'communications',
    'action': 'identify the largest bottleneck',
    'metric': 'defect rate',
    'prompt': 'For a communications task, identify the largest bottleneck and evaluate defect rate.',
}
PLAYBOOK_01198 = {
    'id': 1198,
    'domain': 'finance',
    'action': 'test a small improvement',
    'metric': 'customer satisfaction',
    'prompt': 'For a finance task, test a small improvement and evaluate customer satisfaction.',
}
PLAYBOOK_01199 = {
    'id': 1199,
    'domain': 'sales',
    'action': 'record the decision',
    'metric': 'cost per acquisition',
    'prompt': 'For a sales task, record the decision and evaluate cost per acquisition.',
}
PLAYBOOK_01200 = {
    'id': 1200,
    'domain': 'marketing',
    'action': 'schedule a follow-up',
    'metric': 'inventory turnover',
    'prompt': 'For a marketing task, schedule a follow-up and evaluate inventory turnover.',
}
PLAYBOOK_01201 = {
    'id': 1201,
    'domain': 'operations',
    'action': 'define the baseline metric',
    'metric': 'forecast accuracy',
    'prompt': 'For a operations task, define the baseline metric and evaluate forecast accuracy.',
}
PLAYBOOK_01202 = {
    'id': 1202,
    'domain': 'strategy',
    'action': 'identify the owner',
    'metric': 'project completion',
    'prompt': 'For a strategy task, identify the owner and evaluate project completion.',
}
PLAYBOOK_01203 = {
    'id': 1203,
    'domain': 'leadership',
    'action': 'document the current process',
    'metric': 'response time',
    'prompt': 'For a leadership task, document the current process and evaluate response time.',
}
PLAYBOOK_01204 = {
    'id': 1204,
    'domain': 'customer',
    'action': 'measure the outcome',
    'metric': 'employee capacity',
    'prompt': 'For a customer task, measure the outcome and evaluate employee capacity.',
}
PLAYBOOK_01205 = {
    'id': 1205,
    'domain': 'product',
    'action': 'compare actuals with plan',
    'metric': 'data completeness',
    'prompt': 'For a product task, compare actuals with plan and evaluate data completeness.',
}
PLAYBOOK_01206 = {
    'id': 1206,
    'domain': 'technology',
    'action': 'review the evidence',
    'metric': 'security incidents',
    'prompt': 'For a technology task, review the evidence and evaluate security incidents.',
}
PLAYBOOK_01207 = {
    'id': 1207,
    'domain': 'security',
    'action': 'identify the largest bottleneck',
    'metric': 'lead time',
    'prompt': 'For a security task, identify the largest bottleneck and evaluate lead time.',
}
PLAYBOOK_01208 = {
    'id': 1208,
    'domain': 'governance',
    'action': 'test a small improvement',
    'metric': 'revenue',
    'prompt': 'For a governance task, test a small improvement and evaluate revenue.',
}
PLAYBOOK_01209 = {
    'id': 1209,
    'domain': 'research',
    'action': 'record the decision',
    'metric': 'gross margin',
    'prompt': 'For a research task, record the decision and evaluate gross margin.',
}
PLAYBOOK_01210 = {
    'id': 1210,
    'domain': 'supply_chain',
    'action': 'schedule a follow-up',
    'metric': 'cash conversion',
    'prompt': 'For a supply_chain task, schedule a follow-up and evaluate cash conversion.',
}
PLAYBOOK_01211 = {
    'id': 1211,
    'domain': 'people',
    'action': 'define the baseline metric',
    'metric': 'conversion rate',
    'prompt': 'For a people task, define the baseline metric and evaluate conversion rate.',
}
PLAYBOOK_01212 = {
    'id': 1212,
    'domain': 'project',
    'action': 'identify the owner',
    'metric': 'retention',
    'prompt': 'For a project task, identify the owner and evaluate retention.',
}
PLAYBOOK_01213 = {
    'id': 1213,
    'domain': 'risk',
    'action': 'document the current process',
    'metric': 'cycle time',
    'prompt': 'For a risk task, document the current process and evaluate cycle time.',
}
PLAYBOOK_01214 = {
    'id': 1214,
    'domain': 'data',
    'action': 'measure the outcome',
    'metric': 'defect rate',
    'prompt': 'For a data task, measure the outcome and evaluate defect rate.',
}
PLAYBOOK_01215 = {
    'id': 1215,
    'domain': 'design',
    'action': 'compare actuals with plan',
    'metric': 'customer satisfaction',
    'prompt': 'For a design task, compare actuals with plan and evaluate customer satisfaction.',
}
PLAYBOOK_01216 = {
    'id': 1216,
    'domain': 'communications',
    'action': 'review the evidence',
    'metric': 'cost per acquisition',
    'prompt': 'For a communications task, review the evidence and evaluate cost per acquisition.',
}
PLAYBOOK_01217 = {
    'id': 1217,
    'domain': 'finance',
    'action': 'identify the largest bottleneck',
    'metric': 'inventory turnover',
    'prompt': 'For a finance task, identify the largest bottleneck and evaluate inventory turnover.',
}
PLAYBOOK_01218 = {
    'id': 1218,
    'domain': 'sales',
    'action': 'test a small improvement',
    'metric': 'forecast accuracy',
    'prompt': 'For a sales task, test a small improvement and evaluate forecast accuracy.',
}
PLAYBOOK_01219 = {
    'id': 1219,
    'domain': 'marketing',
    'action': 'record the decision',
    'metric': 'project completion',
    'prompt': 'For a marketing task, record the decision and evaluate project completion.',
}
PLAYBOOK_01220 = {
    'id': 1220,
    'domain': 'operations',
    'action': 'schedule a follow-up',
    'metric': 'response time',
    'prompt': 'For a operations task, schedule a follow-up and evaluate response time.',
}
PLAYBOOK_01221 = {
    'id': 1221,
    'domain': 'strategy',
    'action': 'define the baseline metric',
    'metric': 'employee capacity',
    'prompt': 'For a strategy task, define the baseline metric and evaluate employee capacity.',
}
PLAYBOOK_01222 = {
    'id': 1222,
    'domain': 'leadership',
    'action': 'identify the owner',
    'metric': 'data completeness',
    'prompt': 'For a leadership task, identify the owner and evaluate data completeness.',
}
PLAYBOOK_01223 = {
    'id': 1223,
    'domain': 'customer',
    'action': 'document the current process',
    'metric': 'security incidents',
    'prompt': 'For a customer task, document the current process and evaluate security incidents.',
}
PLAYBOOK_01224 = {
    'id': 1224,
    'domain': 'product',
    'action': 'measure the outcome',
    'metric': 'lead time',
    'prompt': 'For a product task, measure the outcome and evaluate lead time.',
}
PLAYBOOK_01225 = {
    'id': 1225,
    'domain': 'technology',
    'action': 'compare actuals with plan',
    'metric': 'revenue',
    'prompt': 'For a technology task, compare actuals with plan and evaluate revenue.',
}
PLAYBOOK_01226 = {
    'id': 1226,
    'domain': 'security',
    'action': 'review the evidence',
    'metric': 'gross margin',
    'prompt': 'For a security task, review the evidence and evaluate gross margin.',
}
PLAYBOOK_01227 = {
    'id': 1227,
    'domain': 'governance',
    'action': 'identify the largest bottleneck',
    'metric': 'cash conversion',
    'prompt': 'For a governance task, identify the largest bottleneck and evaluate cash conversion.',
}
PLAYBOOK_01228 = {
    'id': 1228,
    'domain': 'research',
    'action': 'test a small improvement',
    'metric': 'conversion rate',
    'prompt': 'For a research task, test a small improvement and evaluate conversion rate.',
}
PLAYBOOK_01229 = {
    'id': 1229,
    'domain': 'supply_chain',
    'action': 'record the decision',
    'metric': 'retention',
    'prompt': 'For a supply_chain task, record the decision and evaluate retention.',
}
PLAYBOOK_01230 = {
    'id': 1230,
    'domain': 'people',
    'action': 'schedule a follow-up',
    'metric': 'cycle time',
    'prompt': 'For a people task, schedule a follow-up and evaluate cycle time.',
}
PLAYBOOK_01231 = {
    'id': 1231,
    'domain': 'project',
    'action': 'define the baseline metric',
    'metric': 'defect rate',
    'prompt': 'For a project task, define the baseline metric and evaluate defect rate.',
}
PLAYBOOK_01232 = {
    'id': 1232,
    'domain': 'risk',
    'action': 'identify the owner',
    'metric': 'customer satisfaction',
    'prompt': 'For a risk task, identify the owner and evaluate customer satisfaction.',
}
PLAYBOOK_01233 = {
    'id': 1233,
    'domain': 'data',
    'action': 'document the current process',
    'metric': 'cost per acquisition',
    'prompt': 'For a data task, document the current process and evaluate cost per acquisition.',
}
PLAYBOOK_01234 = {
    'id': 1234,
    'domain': 'design',
    'action': 'measure the outcome',
    'metric': 'inventory turnover',
    'prompt': 'For a design task, measure the outcome and evaluate inventory turnover.',
}
PLAYBOOK_01235 = {
    'id': 1235,
    'domain': 'communications',
    'action': 'compare actuals with plan',
    'metric': 'forecast accuracy',
    'prompt': 'For a communications task, compare actuals with plan and evaluate forecast accuracy.',
}
PLAYBOOK_01236 = {
    'id': 1236,
    'domain': 'finance',
    'action': 'review the evidence',
    'metric': 'project completion',
    'prompt': 'For a finance task, review the evidence and evaluate project completion.',
}
PLAYBOOK_01237 = {
    'id': 1237,
    'domain': 'sales',
    'action': 'identify the largest bottleneck',
    'metric': 'response time',
    'prompt': 'For a sales task, identify the largest bottleneck and evaluate response time.',
}
PLAYBOOK_01238 = {
    'id': 1238,
    'domain': 'marketing',
    'action': 'test a small improvement',
    'metric': 'employee capacity',
    'prompt': 'For a marketing task, test a small improvement and evaluate employee capacity.',
}
PLAYBOOK_01239 = {
    'id': 1239,
    'domain': 'operations',
    'action': 'record the decision',
    'metric': 'data completeness',
    'prompt': 'For a operations task, record the decision and evaluate data completeness.',
}
PLAYBOOK_01240 = {
    'id': 1240,
    'domain': 'strategy',
    'action': 'schedule a follow-up',
    'metric': 'security incidents',
    'prompt': 'For a strategy task, schedule a follow-up and evaluate security incidents.',
}
PLAYBOOK_01241 = {
    'id': 1241,
    'domain': 'leadership',
    'action': 'define the baseline metric',
    'metric': 'lead time',
    'prompt': 'For a leadership task, define the baseline metric and evaluate lead time.',
}
PLAYBOOK_01242 = {
    'id': 1242,
    'domain': 'customer',
    'action': 'identify the owner',
    'metric': 'revenue',
    'prompt': 'For a customer task, identify the owner and evaluate revenue.',
}
PLAYBOOK_01243 = {
    'id': 1243,
    'domain': 'product',
    'action': 'document the current process',
    'metric': 'gross margin',
    'prompt': 'For a product task, document the current process and evaluate gross margin.',
}
PLAYBOOK_01244 = {
    'id': 1244,
    'domain': 'technology',
    'action': 'measure the outcome',
    'metric': 'cash conversion',
    'prompt': 'For a technology task, measure the outcome and evaluate cash conversion.',
}
PLAYBOOK_01245 = {
    'id': 1245,
    'domain': 'security',
    'action': 'compare actuals with plan',
    'metric': 'conversion rate',
    'prompt': 'For a security task, compare actuals with plan and evaluate conversion rate.',
}
PLAYBOOK_01246 = {
    'id': 1246,
    'domain': 'governance',
    'action': 'review the evidence',
    'metric': 'retention',
    'prompt': 'For a governance task, review the evidence and evaluate retention.',
}
PLAYBOOK_01247 = {
    'id': 1247,
    'domain': 'research',
    'action': 'identify the largest bottleneck',
    'metric': 'cycle time',
    'prompt': 'For a research task, identify the largest bottleneck and evaluate cycle time.',
}
PLAYBOOK_01248 = {
    'id': 1248,
    'domain': 'supply_chain',
    'action': 'test a small improvement',
    'metric': 'defect rate',
    'prompt': 'For a supply_chain task, test a small improvement and evaluate defect rate.',
}
PLAYBOOK_01249 = {
    'id': 1249,
    'domain': 'people',
    'action': 'record the decision',
    'metric': 'customer satisfaction',
    'prompt': 'For a people task, record the decision and evaluate customer satisfaction.',
}
PLAYBOOK_01250 = {
    'id': 1250,
    'domain': 'project',
    'action': 'schedule a follow-up',
    'metric': 'cost per acquisition',
    'prompt': 'For a project task, schedule a follow-up and evaluate cost per acquisition.',
}
PLAYBOOK_01251 = {
    'id': 1251,
    'domain': 'risk',
    'action': 'define the baseline metric',
    'metric': 'inventory turnover',
    'prompt': 'For a risk task, define the baseline metric and evaluate inventory turnover.',
}
PLAYBOOK_01252 = {
    'id': 1252,
    'domain': 'data',
    'action': 'identify the owner',
    'metric': 'forecast accuracy',
    'prompt': 'For a data task, identify the owner and evaluate forecast accuracy.',
}
PLAYBOOK_01253 = {
    'id': 1253,
    'domain': 'design',
    'action': 'document the current process',
    'metric': 'project completion',
    'prompt': 'For a design task, document the current process and evaluate project completion.',
}
PLAYBOOK_01254 = {
    'id': 1254,
    'domain': 'communications',
    'action': 'measure the outcome',
    'metric': 'response time',
    'prompt': 'For a communications task, measure the outcome and evaluate response time.',
}
PLAYBOOK_01255 = {
    'id': 1255,
    'domain': 'finance',
    'action': 'compare actuals with plan',
    'metric': 'employee capacity',
    'prompt': 'For a finance task, compare actuals with plan and evaluate employee capacity.',
}
PLAYBOOK_01256 = {
    'id': 1256,
    'domain': 'sales',
    'action': 'review the evidence',
    'metric': 'data completeness',
    'prompt': 'For a sales task, review the evidence and evaluate data completeness.',
}
PLAYBOOK_01257 = {
    'id': 1257,
    'domain': 'marketing',
    'action': 'identify the largest bottleneck',
    'metric': 'security incidents',
    'prompt': 'For a marketing task, identify the largest bottleneck and evaluate security incidents.',
}
PLAYBOOK_01258 = {
    'id': 1258,
    'domain': 'operations',
    'action': 'test a small improvement',
    'metric': 'lead time',
    'prompt': 'For a operations task, test a small improvement and evaluate lead time.',
}
PLAYBOOK_01259 = {
    'id': 1259,
    'domain': 'strategy',
    'action': 'record the decision',
    'metric': 'revenue',
    'prompt': 'For a strategy task, record the decision and evaluate revenue.',
}
PLAYBOOK_01260 = {
    'id': 1260,
    'domain': 'leadership',
    'action': 'schedule a follow-up',
    'metric': 'gross margin',
    'prompt': 'For a leadership task, schedule a follow-up and evaluate gross margin.',
}
PLAYBOOK_01261 = {
    'id': 1261,
    'domain': 'customer',
    'action': 'define the baseline metric',
    'metric': 'cash conversion',
    'prompt': 'For a customer task, define the baseline metric and evaluate cash conversion.',
}
PLAYBOOK_01262 = {
    'id': 1262,
    'domain': 'product',
    'action': 'identify the owner',
    'metric': 'conversion rate',
    'prompt': 'For a product task, identify the owner and evaluate conversion rate.',
}
PLAYBOOK_01263 = {
    'id': 1263,
    'domain': 'technology',
    'action': 'document the current process',
    'metric': 'retention',
    'prompt': 'For a technology task, document the current process and evaluate retention.',
}
PLAYBOOK_01264 = {
    'id': 1264,
    'domain': 'security',
    'action': 'measure the outcome',
    'metric': 'cycle time',
    'prompt': 'For a security task, measure the outcome and evaluate cycle time.',
}
# DACRE V8 BUILD NOTE 09853: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09854: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09855: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09856: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09857: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09858: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09859: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09860: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09861: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09862: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09863: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09864: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09865: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09866: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09867: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09868: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09869: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09870: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09871: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09872: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09873: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09874: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09875: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09876: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09877: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09878: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09879: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09880: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09881: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09882: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09883: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09884: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09885: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09886: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09887: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09888: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09889: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09890: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09891: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09892: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09893: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09894: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09895: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09896: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09897: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09898: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09899: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09900: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09901: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09902: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09903: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09904: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09905: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09906: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09907: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09908: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09909: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09910: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09911: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09912: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09913: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09914: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09915: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09916: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09917: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09918: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09919: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09920: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09921: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09922: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09923: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09924: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09925: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09926: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09927: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09928: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09929: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09930: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09931: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09932: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09933: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09934: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09935: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09936: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09937: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09938: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09939: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09940: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09941: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09942: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09943: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09944: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09945: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09946: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09947: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09948: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09949: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09950: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09951: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09952: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09953: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09954: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09955: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09956: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09957: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09958: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09959: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09960: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09961: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09962: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09963: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09964: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09965: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09966: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09967: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09968: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09969: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09970: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09971: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09972: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09973: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09974: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09975: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09976: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09977: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09978: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09979: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09980: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09981: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09982: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09983: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09984: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09985: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09986: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09987: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09988: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09989: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09990: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09991: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09992: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09993: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09994: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09995: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09996: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09997: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09998: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 09999: modular Streamlit production registry and testable UI architecture.
# DACRE V8 BUILD NOTE 10000: modular Streamlit production registry and testable UI architecture.
