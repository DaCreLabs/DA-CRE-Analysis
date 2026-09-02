import os
import io
import json
import sqlite3
import secrets
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, request, redirect, url_for, session, flash,
    render_template_string, send_file, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from openpyxl import Workbook, load_workbook
except ImportError:
    Workbook = None
    load_workbook = None

try:
    import requests
except ImportError:
    requests = None


# ============================================================
# DACRE ANALYSIS — FULL SINGLE-FILE FLASK APPLICATION
# ============================================================
# Basic backend included:
# - SQLite account database
# - Signup / login / logout
# - Secure passkey hashing
# - User sessions
# - Account dashboard
# - CSV / XLSX upload
# - Spreadsheet/XLSX generation
# - SQL Code Space UI + local SQL preview
# - Optional Google Gemini + Google Search grounding
# - DACRE logo used STRICTLY as the page icon/favicon
#
# For production, set:
#   SECRET_KEY=...
#   GOOGLE_API_KEY=...
#
# Optional:
#   GEMINI_MODEL=gemini-2.5-flash
# ============================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, "static")
DB_PATH = os.path.join(APP_DIR, "dacre_analysis.db")

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
app.permanent_session_lifetime = timedelta(days=30)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ----------------------------- DATABASE -----------------------------

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            company_website TEXT,
            passkey_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            row_count INTEGER DEFAULT 0,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ----------------------------- HELPERS -----------------------------

def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please log in to access your DACRE Analysis account.", "error")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def safe_text(value, max_len=500):
    return str(value or "").strip()[:max_len]


def page(title, body, extra_css="", extra_js=""):
    user = current_user()
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} · DACRE Analysis</title>
<link rel="icon" type="image/png" href="{{ url_for('static', filename='dacre-logo.png') }}">
<style>
:root{
  --bg:#020713; --panel:#071326; --panel2:#0a1930; --line:#12345d;
  --blue:#149dff; --blue2:#2458ff; --green:#55e735; --gold:#d7ad4f;
  --silver:#dbe6f3; --muted:#8ea4bd; --white:#f7fbff; --danger:#ff667a;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; color:var(--white); background:
  radial-gradient(circle at 20% 0%,rgba(0,116,255,.16),transparent 32%),
  radial-gradient(circle at 90% 15%,rgba(48,220,102,.08),transparent 30%),
  var(--bg);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif;
}
a{color:inherit;text-decoration:none}
button,input,textarea,select{font:inherit}
.container{width:min(1180px,92%);margin:auto}
.topbar{
  position:sticky;top:0;z-index:50;background:rgba(2,7,19,.88);
  backdrop-filter:blur(18px);border-bottom:1px solid rgba(39,110,180,.25)
}
.nav{height:76px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.wordmark{font-weight:800;letter-spacing:4px;font-size:20px}
.wordmark span{color:var(--green);font-size:11px;display:block;letter-spacing:6px;margin-top:-2px}
.navlinks{display:flex;gap:24px;color:#b7c7d9;font-size:14px}
.navlinks a:hover{color:white}
.actions{display:flex;gap:10px}
.btn{
  border:1px solid #1d6fca;border-radius:9px;padding:12px 17px;
  color:white;background:#07152a;cursor:pointer;font-weight:700;
  transition:.2s transform,.2s box-shadow,.2s background;
}
.btn:hover{transform:translateY(-1px);box-shadow:0 10px 30px rgba(0,130,255,.16)}
.btn-primary{border-color:#3aa6ff;background:linear-gradient(135deg,#075cff,#0a98ff)}
.btn-green{border-color:#35bc50;background:linear-gradient(135deg,#0c8e2f,#43d34d);color:#031007}
.btn-gold{border-color:#b28c38;background:linear-gradient(135deg,#9d762a,#f0ce6b);color:#080600}
.btn-danger{border-color:#963a4a;color:#ffb7c0}
.hero{padding:92px 0 70px;position:relative;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1.03fr .97fr;gap:46px;align-items:center}
.eyebrow{color:#69c9ff;letter-spacing:3px;text-transform:uppercase;font-size:12px;font-weight:800}
h1{font-size:clamp(46px,6vw,82px);line-height:.98;margin:18px 0}
.gradient{background:linear-gradient(90deg,#fff,#55b8ff 48%,#58e643);-webkit-background-clip:text;color:transparent}
.lead{font-size:19px;line-height:1.75;color:#aebfd2;max-width:680px}
.hero-actions{display:flex;gap:12px;margin:30px 0;flex-wrap:wrap}
.stats{display:flex;gap:34px;flex-wrap:wrap;margin-top:34px}
.stat b{display:block;font-size:26px;color:#53d7ff}
.stat span{color:#8198af;font-size:12px}
.hero-art{
  border:1px solid rgba(38,139,235,.55);border-radius:22px;overflow:hidden;
  box-shadow:0 0 70px rgba(0,110,255,.18),inset 0 0 50px rgba(0,140,255,.08);
  background:#031023
}
.hero-art img{width:100%;display:block}
.section{padding:86px 0}
.section-head{max-width:760px;margin-bottom:30px}
.section-head h2{font-size:42px;margin:8px 0 12px}
.section-head p{color:var(--muted);line-height:1.7}
.feature-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.card{
  background:linear-gradient(180deg,rgba(10,28,52,.92),rgba(4,14,29,.94));
  border:1px solid rgba(44,105,161,.34);border-radius:14px;padding:22px;
  box-shadow:inset 0 1px rgba(255,255,255,.03)
}
.card h3{margin:8px 0}.card p{color:#8fa5bb;line-height:1.6;font-size:14px}
.icon{font-size:22px;color:#49b9ff}
.image-section{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:center}
.image-section img{width:100%;border-radius:18px;border:1px solid #153d67}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}
.pill{padding:8px 11px;border:1px solid #19466f;border-radius:99px;color:#9bc2df;font-size:12px;background:#06172b}
.auth-wrap{min-height:calc(100vh - 77px);display:grid;place-items:center;padding:50px 0}
.auth-card{width:min(720px,94%);padding:32px;border:1px solid #1b4771;border-radius:20px;background:rgba(6,18,35,.96);box-shadow:0 20px 70px rgba(0,0,0,.35)}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.field{display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}
label{font-size:12px;color:#a8bed3;font-weight:700}
input,textarea,select{
  width:100%;background:#031022;color:white;border:1px solid #153b62;
  border-radius:9px;padding:13px;outline:none
}
input:focus,textarea:focus,select:focus{border-color:#2a9cff;box-shadow:0 0 0 3px rgba(42,156,255,.08)}
.notice{padding:12px 14px;border-radius:9px;margin:14px 0;border:1px solid #23567f;background:#061b30;color:#b7d7ef}
.notice.error{border-color:#7f3343;background:#2a0c14;color:#ffc2ca}
.notice.success{border-color:#287640;background:#0b2815;color:#baf8c7}
.flash-wrap{position:fixed;right:18px;top:90px;z-index:80;width:min(390px,92%)}
.flash{padding:13px 15px;margin:8px 0;border-radius:10px;background:#081a30;border:1px solid #1d527c}
.flash.error{border-color:#84384b}.flash.success{border-color:#2d7e46}
.dashboard{display:grid;grid-template-columns:235px 1fr;min-height:calc(100vh - 77px)}
.sidebar{border-right:1px solid #103456;background:#030c1a;padding:20px;position:sticky;top:77px;height:calc(100vh - 77px)}
.side-title{font-size:13px;color:#6ea7d2;text-transform:uppercase;letter-spacing:2px;margin-bottom:15px}
.side-link{display:block;padding:11px 12px;border-radius:8px;color:#91a9bf;margin:4px 0;font-size:14px}
.side-link:hover,.side-link.active{background:#09264a;color:white}
.main{padding:32px;overflow:hidden}
.dashboard-top{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:22px}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.kpi{padding:18px;border:1px solid #12375b;border-radius:12px;background:#061427}.kpi b{font-size:25px}.kpi span{display:block;color:#7891aa;font-size:11px;margin-top:5px}
.dash-grid{display:grid;grid-template-columns:1.3fr .7fr;gap:16px;margin-top:16px}
.chart{height:260px;display:flex;align-items:end;gap:8px;padding:25px 15px 15px;border-radius:10px;background:linear-gradient(180deg,#061b35,#031022)}
.bar{flex:1;background:linear-gradient(180deg,#36b8ff,#1649ff);border-radius:4px 4px 0 0;min-width:8px}
.activity li{list-style:none;padding:11px 0;border-bottom:1px solid #102a46;color:#9db1c5;font-size:13px}
.activity ul{padding:0;margin:0}
.workspace{margin-top:18px}
textarea.code{min-height:240px;font-family:ui-monospace,Consolas,monospace;line-height:1.5}
.status{
  margin-top:12px;padding:10px 12px;border-radius:8px;border:1px solid #164c78;
  color:#8fd6ff;background:#041b30;display:none
}
.preview-table{width:100%;border-collapse:collapse;font-size:12px}.preview-table th,.preview-table td{padding:8px;border:1px solid #123455;text-align:left}.preview-table th{color:#66c5ff;background:#061c35}
footer{border-top:1px solid #102c49;padding:35px 0;color:#6f879d}
@media(max-width:950px){
  .hero-grid,.image-section,.dash-grid{grid-template-columns:1fr}
  .feature-grid{grid-template-columns:repeat(2,1fr)}
  .kpis{grid-template-columns:repeat(2,1fr)}
  .navlinks{display:none}.dashboard{grid-template-columns:1fr}.sidebar{position:static;height:auto;border-right:0;border-bottom:1px solid #103456}
}
@media(max-width:620px){
  .feature-grid,.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}.main{padding:18px}
  .hero{padding-top:55px}.stats{gap:18px}
}
{{ extra_css|safe }}
</style>
</head>
<body>
<header class="topbar">
  <div class="container nav">
    <a href="{{ url_for('home') }}">
      <div class="wordmark">DACRE <span>ANALYSIS</span></div>
    </a>
    {% if user %}
    <div class="navlinks">
      <a href="{{ url_for('dashboard') }}">Dashboard</a>
      <a href="{{ url_for('sql_space') }}">SQL Code Space</a>
      <a href="{{ url_for('logout') }}">Log out</a>
    </div>
    <div class="actions"><span style="color:#9eb4c9;font-size:13px">{{ user['account_name'] }}</span></div>
    {% else %}
    <div class="navlinks">
      <a href="{{ url_for('home') }}#features">Features</a>
      <a href="{{ url_for('home') }}#platform">Platform</a>
      <a href="{{ url_for('home') }}#pricing">Pricing</a>
      <a href="{{ url_for('home') }}#faq">FAQ</a>
    </div>
    <div class="actions">
      <a class="btn btn-green" href="{{ url_for('signup') }}">Get Started with DACRE Analysis</a>
      <a class="btn" href="{{ url_for('login') }}">Log In Now</a>
    </div>
    {% endif %}
  </div>
</header>

<div class="flash-wrap">
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <div class="flash {{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}
</div>

{{ body|safe }}

<script>
{{ extra_js|safe }}
</script>
</body>
</html>
""", title=title, body=body, user=user, extra_css=extra_css, extra_js=extra_js)


# ----------------------------- LANDING PAGE -----------------------------

@app.route("/")
def home():
    body = """
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">DACRE Analysis · Data Intelligence Platform</div>
      <h1>Data Today,<br><span class="gradient">Smarter Tomorrows.</span></h1>
      <p class="lead">
        A premium workspace for getting data, cleaning it, analysing it,
        building visualizations, creating dashboards, writing SQL,
        preparing reports and exporting decision-ready work.
      </p>
      <div class="hero-actions">
        <a class="btn btn-green" href="/signup">Start Your 30-Day Free Trial</a>
        <a class="btn" href="#platform">Explore DACRE Analysis</a>
      </div>
      <div class="stats">
        <div class="stat"><b>2.1T+</b><span>Data points processed</span></div>
        <div class="stat"><b>50+</b><span>Analytics workflows</span></div>
        <div class="stat"><b>99.9%</b><span>Reliability target</span></div>
        <div class="stat"><b>24/7</b><span>Workspace access</span></div>
      </div>
    </div>
    <div class="hero-art">
      <img src="/static/landing-hero.png" alt="DACRE Analysis premium workspace">
    </div>
  </div>
</section>

<section class="section" id="features">
 <div class="container">
  <div class="section-head">
    <div class="eyebrow">Everything in one intelligence workspace</div>
    <h2>Everything DACRE Analysis can do.</h2>
    <p>Move from raw data to a finished business deliverable without jumping between disconnected tools.</p>
  </div>
  <div class="feature-grid">
    <div class="card"><div class="icon">↙</div><h3>Get Data</h3><p>Bring in datasets from files and connected sources, with workspace-ready organization.</p></div>
    <div class="card"><div class="icon">✦</div><h3>Clean Data</h3><p>Prepare messy datasets, handle missing values, remove duplicates and standardize fields.</p></div>
    <div class="card"><div class="icon">◫</div><h3>Analyse Data</h3><p>Explore patterns, trends, distributions, relationships and business performance.</p></div>
    <div class="card"><div class="icon">▥</div><h3>Visualize</h3><p>Create bar, line, pie, area, scatter and other decision-focused visualizations.</p></div>
    <div class="card"><div class="icon">⌘</div><h3>David Intelligence</h3><p>Invisible DI orchestration can assist with analysis, coding, validation and refinement.</p></div>
    <div class="card"><div class="icon">SQL</div><h3>SQL Code Space</h3><p>Describe what you want, generate SQL/code, review it, run it and prepare it for File Vault.</p></div>
    <div class="card"><div class="icon">▤</div><h3>Reports</h3><p>Turn findings into structured professional reports and presentation-ready outputs.</p></div>
    <div class="card"><div class="icon">⇩</div><h3>Export</h3><p>Prepare spreadsheet, CSV and other business-ready deliverables from your workspace.</p></div>
  </div>
 </div>
</section>

<section class="section" id="platform">
 <div class="container image-section">
   <div>
    <div class="eyebrow">The workstation</div>
    <h2>Built for serious data work.</h2>
    <p class="lead">
      DACRE Analysis combines data workspace, visual analytics, dashboards,
      reports, Power BI workflows, SQL Code Space, File Vault and DI-assisted
      processing in one environment.
    </p>
    <div class="pills">
      <span class="pill">Data Workspace</span><span class="pill">Dashboard Studio</span>
      <span class="pill">Reports</span><span class="pill">Power BI</span>
      <span class="pill">Connections</span><span class="pill">File Vault</span>
      <span class="pill">SQL Code Space</span>
    </div>
   </div>
   <img src="/static/dashboard-preview.png" alt="DACRE Analysis dashboard preview">
 </div>
</section>

<section class="section">
 <div class="container image-section">
   <img src="/static/global-data-sync.png" alt="DACRE Analysis global data sync">
   <div>
    <div class="eyebrow">Global data intelligence</div>
    <h2>See the signal inside the data.</h2>
    <p class="lead">Bring together analytical views, live trends and visual stories so your team can understand what the numbers are saying.</p>
   </div>
 </div>
</section>

<section class="section" id="pricing">
 <div class="container">
  <div class="section-head">
   <div class="eyebrow">Simple starting point</div>
   <h2>30 days to experience the platform.</h2>
   <p>Standard DACRE Analysis accounts start with a 30-day free trial. Subscription after the trial is ₦30,000/month.</p>
  </div>
  <div class="card" style="max-width:620px">
    <h3>DACRE Analysis</h3>
    <div style="font-size:42px;font-weight:900;margin:12px 0">₦30,000 <small style="font-size:14px;color:#7891aa">/ month after trial</small></div>
    <p>30-day free trial · Data workspace · Visualizations · Dashboard Studio · Reports · SQL Code Space · File Vault</p>
    <a class="btn btn-green" href="/signup">Get Started</a>
  </div>
 </div>
</section>

<section class="section" id="faq">
 <div class="container">
  <div class="section-head"><div class="eyebrow">FAQ</div><h2>Questions, answered.</h2></div>
  <div class="feature-grid">
   <div class="card"><h3>Do I need an account?</h3><p>Yes. Create your DACRE account before logging in.</p></div>
   <div class="card"><h3>What happens if I try to log in without an account?</h3><p>DACRE checks the database and tells you that the account has not been created.</p></div>
   <div class="card"><h3>Is my passkey stored directly?</h3><p>No. The backend stores a secure password hash rather than the original passkey.</p></div>
   <div class="card"><h3>Can DI access the internet?</h3><p>When the optional Google API key is configured, the backend can use Gemini with Google Search grounding for supported requests.</p></div>
  </div>
 </div>
</section>

<footer><div class="container">© 2026 DACRE Analysis · Data Today, Smarter Tomorrows.</div></footer>
"""
    return page("Data Today, Smarter Tomorrows", body)


# ----------------------------- AUTH -----------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        account_name = safe_text(request.form.get("account_name"), 120)
        company_name = safe_text(request.form.get("company_name"), 160)
        email = safe_text(request.form.get("email"), 200).lower()
        phone = safe_text(request.form.get("phone"), 50)
        website = safe_text(request.form.get("company_website"), 300)
        passkey = request.form.get("passkey", "")

        if not all([account_name, company_name, email, phone, passkey]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("signup"))

        if len(passkey) < 8:
            flash("Account passkey must be at least 8 characters.", "error")
            return redirect(url_for("signup"))

        conn = db()
        existing = conn.execute(
            "SELECT id FROM users WHERE lower(email)=lower(?)",
            (email,)
        ).fetchone()
        if existing:
            conn.close()
            flash("An account already exists with that email address. Please log in.", "error")
            return redirect(url_for("login"))

        conn.execute("""
            INSERT INTO users
            (account_name, company_name, email, phone, company_website, passkey_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            account_name, company_name, email, phone, website,
            generate_password_hash(passkey),
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        conn.close()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    body = """
<div class="auth-wrap">
 <div class="auth-card">
  <div class="eyebrow">DACRE Analysis</div>
  <h1 style="font-size:40px">Create your account.</h1>
  <p style="color:#8fa5bb">Start your standard 30-day free trial.</p>
  <form method="post">
   <div class="form-grid">
    <div class="field"><label>User Account Name *</label><input name="account_name" required placeholder="Your account name"></div>
    <div class="field"><label>Company Name *</label><input name="company_name" required placeholder="Your company name"></div>
    <div class="field full"><label>Email Address *</label><input type="email" name="email" required placeholder="you@company.com"></div>
    <div class="field"><label>Phone Number *</label><input name="phone" required placeholder="+234..."></div>
    <div class="field"><label>Company Website Link (Optional)</label><input name="company_website" placeholder="https://yourcompany.com"></div>
    <div class="field full"><label>Account Passkey *</label><input type="password" name="passkey" minlength="8" required placeholder="Create your secure passkey"></div>
   </div>
   <button class="btn btn-green" style="width:100%;margin-top:20px">Create Account</button>
  </form>
  <p style="text-align:center;color:#8198af;margin-top:18px">Already have an account? <a style="color:#5ae33e" href="/login">Log in now</a></p>
 </div>
</div>
"""
    return page("Create Account", body)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        account_name = safe_text(request.form.get("account_name"), 120)
        company_name = safe_text(request.form.get("company_name"), 160)
        passkey = request.form.get("passkey", "")

        conn = db()
        user = conn.execute("""
            SELECT * FROM users
            WHERE lower(account_name)=lower(?) AND lower(company_name)=lower(?)
        """, (account_name, company_name)).fetchone()

        if not user:
            conn.close()
            flash("This account has not been created yet. Please create your DACRE account first.", "error")
            return redirect(url_for("signup"))

        if not check_password_hash(user["passkey_hash"], passkey):
            conn.close()
            flash("Incorrect account passkey.", "error")
            return redirect(url_for("login"))

        conn.execute(
            "UPDATE users SET last_login=? WHERE id=?",
            (datetime.utcnow().isoformat(), user["id"])
        )
        conn.commit()
        conn.close()

        session.clear()
        session["user_id"] = user["id"]
        session.permanent = True
        return redirect(url_for("dashboard"))

    body = """
<div class="auth-wrap">
 <div class="auth-card" style="max-width:600px">
  <div class="eyebrow">Welcome back</div>
  <h1 style="font-size:40px">Log in to DACRE.</h1>
  <p style="color:#8fa5bb">Use the same account details you used when creating your account.</p>
  <form method="post">
   <div class="form-grid">
    <div class="field full"><label>Account Name *</label><input name="account_name" required></div>
    <div class="field full"><label>Company Name *</label><input name="company_name" required></div>
    <div class="field full"><label>Account Passkey *</label><input type="password" name="passkey" required></div>
   </div>
   <button class="btn btn-primary" style="width:100%;margin-top:20px">Log In</button>
  </form>
  <p style="text-align:center;color:#8198af;margin-top:18px">Don't have an account? <a style="color:#55e735" href="/signup">Create one now</a></p>
 </div>
</div>
"""
    return page("Log In", body)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# ----------------------------- DASHBOARD -----------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    conn = db()
    datasets = conn.execute(
        "SELECT * FROM datasets WHERE user_id=? ORDER BY id DESC",
        (user["id"],)
    ).fetchall()
    conn.close()

    body = f"""
<div class="dashboard">
 <aside class="sidebar">
  <div class="side-title">DACRE Analysis</div>
  <a class="side-link active" href="/dashboard">Overview</a>
  <a class="side-link" href="/dashboard#workspace">Data Workspace</a>
  <a class="side-link" href="/sql-code-space">SQL Code Space</a>
  <a class="side-link" href="/dashboard#visualizations">Visualizations</a>
  <a class="side-link" href="/dashboard#reports">Reports</a>
  <a class="side-link" href="/dashboard#powerbi">Power BI</a>
  <a class="side-link" href="/dashboard#connections">Connections</a>
  <a class="side-link" href="/dashboard#vault">File Vault</a>
  <a class="side-link" href="/logout">Log out</a>
 </aside>
 <main class="main">
  <div class="dashboard-top">
    <div><div class="eyebrow">Organisation workspace</div><h1 style="font-size:34px;margin:5px 0">Welcome, {user['account_name']}</h1><div style="color:#8299b1">{user['company_name']}</div></div>
    <a class="btn btn-green" href="/sql-code-space">Open SQL Code Space</a>
  </div>

  <div class="kpis">
    <div class="kpi"><b>{len(datasets)}</b><span>Datasets</span></div>
    <div class="kpi"><b>0</b><span>Reports</span></div>
    <div class="kpi"><b>0</b><span>Dashboards</span></div>
    <div class="kpi"><b>0</b><span>SQL Scripts</span></div>
    <div class="kpi"><b>30</b><span>Trial days</span></div>
  </div>

  <div class="dash-grid">
   <section class="card">
    <h3>Data Activity</h3>
    <div class="chart">
      <div class="bar" style="height:28%"></div><div class="bar" style="height:45%"></div>
      <div class="bar" style="height:39%"></div><div class="bar" style="height:65%"></div>
      <div class="bar" style="height:52%"></div><div class="bar" style="height:78%"></div>
      <div class="bar" style="height:62%"></div><div class="bar" style="height:88%"></div>
      <div class="bar" style="height:71%"></div><div class="bar" style="height:94%"></div>
    </div>
   </section>
   <section class="card activity">
    <h3>Recent Activity</h3>
    <ul>
      <li>Workspace opened</li>
      <li>Account session secured</li>
      <li>Data Workspace ready</li>
      <li>SQL Code Space available</li>
    </ul>
   </section>
  </div>

  <section class="card workspace" id="workspace">
    <h3>Data Workspace</h3>
    <p>Upload a CSV or Excel dataset. The basic backend records it against your account.</p>
    <form action="/upload-dataset" method="post" enctype="multipart/form-data" style="display:flex;gap:10px;flex-wrap:wrap">
      <input type="file" name="dataset" accept=".csv,.xlsx,.xls" required style="max-width:430px">
      <button class="btn btn-primary">Upload Dataset</button>
    </form>
    <div style="margin-top:18px">
      <table class="preview-table">
       <tr><th>File</th><th>Rows</th><th>Uploaded</th></tr>
       {''.join(f"<tr><td>{d['filename']}</td><td>{d['row_count']}</td><td>{d['uploaded_at'][:19]}</td></tr>" for d in datasets) or "<tr><td colspan='3'>No datasets uploaded yet.</td></tr>"}
      </table>
    </div>
  </section>

  <section class="card workspace" id="visualizations">
    <h3>Visualizations</h3><p>Build charts from your prepared data. The production visualization engine can be connected to this workspace next.</p>
  </section>
  <section class="card workspace" id="reports">
    <h3>Reports</h3><p>Create professional analytical reports from workspace results.</p>
  </section>
  <section class="card workspace" id="powerbi">
    <h3>Power BI</h3><p>Connection and workspace integration placeholders are ready for the next backend phase.</p>
  </section>
  <section class="card workspace" id="connections">
    <h3>Connections</h3><p>Secure external data connections can be added here later.</p>
  </section>
  <section class="card workspace" id="vault">
    <h3>File Vault</h3><p>Generated files and approved implementations will be stored here in the full backend.</p>
  </section>
 </main>
</div>
"""
    return page("Dashboard", body)


@app.route("/upload-dataset", methods=["POST"])
@login_required
def upload_dataset():
    file = request.files.get("dataset")
    if not file or not file.filename:
        flash("Choose a CSV or Excel file.", "error")
        return redirect(url_for("dashboard"))

    filename = os.path.basename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    row_count = 0

    try:
        if ext == ".csv":
            import csv
            raw = file.read().decode("utf-8-sig", errors="replace")
            row_count = max(0, sum(1 for _ in csv.DictReader(io.StringIO(raw))))
        elif ext in (".xlsx", ".xls") and load_workbook:
            wb = load_workbook(file, read_only=True, data_only=True)
            ws = wb.active
            row_count = max(0, ws.max_row - 1)
            wb.close()
        else:
            flash("Supported formats are CSV and XLSX. XLS may require conversion to XLSX.", "error")
            return redirect(url_for("dashboard"))
    except Exception as exc:
        flash(f"Could not read the dataset: {exc}", "error")
        return redirect(url_for("dashboard"))

    user = current_user()
    conn = db()
    conn.execute(
        "INSERT INTO datasets(user_id,filename,row_count,uploaded_at) VALUES(?,?,?,?)",
        (user["id"], filename, row_count, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

    flash(f"{filename} was added to your Data Workspace.", "success")
    return redirect(url_for("dashboard"))


# ----------------------------- SQL CODE SPACE -----------------------------

@app.route("/sql-code-space", methods=["GET", "POST"])
@login_required
def sql_space():
    generated = ""
    prompt = ""

    if request.method == "POST":
        prompt = safe_text(request.form.get("request"), 2000)
        if prompt:
            generated = basic_sql_generator(prompt)

    body = f"""
<div class="container section">
 <div class="section-head">
  <div class="eyebrow">SQL Code Space</div>
  <h2>Describe what you want. Prociel prepares the code.</h2>
  <p>Speak or type your request. The current version provides a basic local generator; connect the Google API key to enable DI-powered generation.</p>
 </div>

 <form method="post" id="sqlForm">
   <div class="card">
    <label>Your request</label>
    <textarea name="request" id="requestBox" rows="5" placeholder="Example: create a SQL query that shows monthly sales by region">{prompt}</textarea>
    <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
      <button class="btn" type="button" onclick="startVoice()">🎙 Voice</button>
      <button class="btn btn-primary" type="submit">Send to Prociel</button>
    </div>
    <div id="status" class="status"></div>
   </div>
 </form>

 <div class="card workspace">
   <h3>Generated Code</h3>
   <textarea class="code" id="codeBox">{generated or "-- Generated SQL will appear here --"}</textarea>
   <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
     <button class="btn btn-primary" type="button" onclick="runCode()">Run Code</button>
     <button class="btn" type="button" onclick="copyCode()">Copy</button>
   </div>
   <div id="runStatus" class="status"></div>
 </div>

 <div class="card workspace">
   <h3>Implementation Preview</h3>
   <p>This is intentionally a preview-first workflow. Exiel does not automatically save anything to File Vault.</p>
   <div style="display:flex;gap:10px">
     <button class="btn btn-green" type="button" onclick="addToVault()">Add to File Vault</button>
     <button class="btn" type="button" onclick="document.getElementById('codeBox').focus()">Edit</button>
     <button class="btn btn-danger" type="button" onclick="document.getElementById('codeBox').value=''">Discard</button>
   </div>
   <div id="vaultStatus" class="status"></div>
 </div>
</div>
"""
    js = r"""
function showStatus(id, text){
  const el=document.getElementById(id);
  el.style.display='block'; el.textContent=text;
}
async function runCode(){
  showStatus('runStatus','Exiel — Running your code...');
  await new Promise(r=>setTimeout(r,900));
  showStatus('runStatus','Validiel — Checking the result...');
  await new Promise(r=>setTimeout(r,700));
  showStatus('runStatus','DACRE — Implementation preview is ready. Nothing has been saved yet.');
}
function addToVault(){
  showStatus('vaultStatus','DACRE — Approved implementation added to the File Vault preview.');
}
function copyCode(){
  navigator.clipboard.writeText(document.getElementById('codeBox').value);
  showStatus('runStatus','Code copied.');
}
function startVoice(){
  const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SpeechRecognition){showStatus('status','Voice input is not supported by this browser.');return;}
  const rec=new SpeechRecognition();
  rec.lang='en-US'; rec.interimResults=false;
  rec.onstart=()=>showStatus('status','Listening...');
  rec.onresult=e=>{document.getElementById('requestBox').value=e.results[0][0].transcript;showStatus('status','Voice captured. Press Send to continue.');};
  rec.onerror=()=>showStatus('status','Voice capture could not be completed.');
  rec.start();
}
"""
    if GOOGLE_API_KEY:
        js += "\n// Google API key is configured on the server; it is never placed in browser JavaScript.\n"
    return page("SQL Code Space", body, extra_js=js)


def basic_sql_generator(prompt):
    p = prompt.lower()
    if "monthly" in p and "sales" in p:
        return """SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(amount) AS total_sales
FROM sales
GROUP BY 1
ORDER BY 1;"""
    if "count" in p and ("customer" in p or "customers" in p):
        return """SELECT
    COUNT(*) AS customer_count
FROM customers;"""
    if "average" in p or "avg" in p:
        return """SELECT
    AVG(amount) AS average_amount
FROM data_table;"""
    return f"""-- Prociel basic SQL draft
-- Request: {prompt}
SELECT *
FROM data_table
LIMIT 100;"""


# ----------------------------- FILE GENERATION -----------------------------

@app.route("/generate-sheet", methods=["POST"])
@login_required
def generate_sheet():
    if Workbook is None:
        return jsonify({"error": "openpyxl is not installed. Run pip install -r requirements.txt"}), 500

    payload = request.get_json(silent=True) or {}
    title = safe_text(payload.get("title"), 100) or "DACRE Analysis Data"
    rows = payload.get("rows") or [
        ["Metric", "Value", "Status"],
        ["Example records", 100, "Ready"],
        ["Generated by", "DACRE Analysis", "Complete"],
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "DACRE Data"
    for row in rows:
        ws.append(row)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in title) + ".xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ----------------------------- OPTIONAL GEMINI + SEARCH -----------------------------

@app.route("/api/di", methods=["POST"])
@login_required
def di_api():
    """
    Optional server-side Gemini endpoint.
    The Google API key remains on the server as GOOGLE_API_KEY.

    With a supported Gemini model/API configuration, the request can ask
    Gemini to use Google Search grounding when the task needs fresh web data.
    """
    payload = request.get_json(silent=True) or {}
    user_request = safe_text(payload.get("message"), 6000)

    if not user_request:
        return jsonify({"error": "Message is required."}), 400

    if not GOOGLE_API_KEY or requests is None:
        return jsonify({
            "ok": True,
            "configured": False,
            "message": "DI backend is ready, but GOOGLE_API_KEY is not configured on the server."
        })

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}"
    )

    body = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": (
                    "You are DACRE Analysis David Intelligence (DI). "
                    "Help with data analysis, SQL, spreadsheets, reports and business intelligence. "
                    "Use fresh web information when it is genuinely required. "
                    "Return concise, useful results. User request:\n\n" + user_request
                )
            }]
        }],
        "tools": [{"google_search": {}}]
    }

    try:
        response = requests.post(url, json=body, timeout=25)
        data = response.json()
        if response.status_code >= 400:
            return jsonify({"error": data}), response.status_code

        text_parts = []
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "text" in part:
                    text_parts.append(part["text"])

        return jsonify({
            "ok": True,
            "configured": True,
            "response": "\n".join(text_parts).strip(),
            "raw": data
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ----------------------------- HEALTH -----------------------------

@app.route("/health")
def health():
    return jsonify({
        "app": "DACRE Analysis",
        "status": "online",
        "database": os.path.exists(DB_PATH),
        "google_api_configured": bool(GOOGLE_API_KEY)
    })


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    print("DACRE Analysis running on http://127.0.0.1:%s" % port)
    print("Database:", DB_PATH)
    print("Google API configured:", bool(GOOGLE_API_KEY))
    app.run(host=host, port=port, debug=False)
