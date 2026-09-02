import os
import io
import csv
import json
import re
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, request, redirect, url_for, session, flash, render_template_string, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from openpyxl import Workbook, load_workbook

try:
    import requests
except ImportError:
    requests = None

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
DB_PATH = APP_DIR / "dacre_analysis.db"
UPLOAD_DIR = APP_DIR / "user_files"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
    MAX_CONTENT_LENGTH=25 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(days=30),
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
ALLOWED_UPLOADS = {"csv", "xlsx"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL COLLATE NOCASE,
            company_name TEXT NOT NULL COLLATE NOCASE,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            phone TEXT NOT NULL,
            company_website TEXT,
            passkey_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT
        )''')
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_account_company ON users(account_name, company_name)")
        conn.execute('''CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            row_count INTEGER NOT NULL DEFAULT 0,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS vault_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )''')


init_db()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    with get_db() as conn:
        return conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()


def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in to access your DACRE Analysis account.", "error")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped


def csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def require_csrf():
    token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
    if not token or not secrets.compare_digest(token, session.get("csrf_token", "")):
        return False
    return True


def clean(value, max_len=500):
    return str(value or "").strip()[:max_len]


def esc_json(value):
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


BASE_CSS = r'''<style>
:root{--bg:#020713;--panel:#071326;--panel2:#0a1930;--line:#14365f;--blue:#159cff;--blue2:#2458ff;--green:#55e735;--gold:#d7ad4f;--silver:#dbe6f3;--muted:#8ea4bd;--white:#f7fbff;--danger:#ff667a}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--white);background:radial-gradient(circle at 15% 0%,rgba(0,116,255,.18),transparent 30%),radial-gradient(circle at 90% 20%,rgba(48,220,102,.09),transparent 28%),var(--bg);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif}a{color:inherit;text-decoration:none}button,input,textarea,select{font:inherit}.container{width:min(1200px,92%);margin:auto}
.topbar{position:sticky;top:0;z-index:100;background:rgba(2,7,19,.84);backdrop-filter:blur(18px);border-bottom:1px solid rgba(39,110,180,.26)}.nav{min-height:76px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{font-weight:900;letter-spacing:5px;font-size:19px}.brand small{display:block;color:var(--green);font-size:9px;letter-spacing:6px;margin-top:2px}.navlinks{display:flex;gap:22px;color:#b7c7d9;font-size:14px}.navlinks a:hover{color:#fff}.actions{display:flex;gap:9px;align-items:center}.btn{display:inline-flex;align-items:center;justify-content:center;border:1px solid #1d6fca;border-radius:10px;padding:12px 17px;color:white;background:#07152a;cursor:pointer;font-weight:800;transition:.2s transform,.2s box-shadow,.2s background}.btn:hover{transform:translateY(-1px);box-shadow:0 12px 30px rgba(0,130,255,.16)}.btn-primary{border-color:#3aa6ff;background:linear-gradient(135deg,#075cff,#0a98ff)}.btn-green{border-color:#35bc50;background:linear-gradient(135deg,#0c8e2f,#43d34d);color:#031007}.btn-gold{border-color:#b28c38;background:linear-gradient(135deg,#9d762a,#f0ce6b);color:#080600}.btn-danger{border-color:#963a4a;color:#ffb7c0}.section{padding:82px 0}.hero{padding:92px 0 74px;overflow:hidden}.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:44px;align-items:center}.eyebrow{color:#69c9ff;letter-spacing:3px;text-transform:uppercase;font-size:12px;font-weight:900}.hero h1{font-size:clamp(46px,6vw,84px);line-height:.97;margin:18px 0}.gradient{background:linear-gradient(90deg,#fff,#55b8ff 48%,#58e643);-webkit-background-clip:text;background-clip:text;color:transparent}.lead{font-size:18px;line-height:1.75;color:#b7c7d9}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:35px}.stat{padding:15px;border:1px solid rgba(58,166,255,.18);background:rgba(7,19,38,.58);border-radius:12px}.stat b{font-size:21px;display:block}.stat span{font-size:11px;color:var(--muted)}.hero-art img,.wide-img{width:100%;display:block;border-radius:18px;border:1px solid rgba(75,174,255,.35);box-shadow:0 30px 80px rgba(0,0,0,.45)}.section-head{max-width:760px;margin-bottom:35px}.section-head h2{font-size:clamp(30px,4vw,52px);margin:10px 0}.section-head p{color:var(--muted);line-height:1.7}.feature-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:linear-gradient(180deg,rgba(10,25,48,.9),rgba(4,12,25,.9));border:1px solid rgba(43,113,179,.24);border-radius:16px;padding:22px;box-shadow:0 18px 45px rgba(0,0,0,.18)}.card h3{margin:8px 0}.card p{color:var(--muted);line-height:1.65;font-size:14px}.icon{color:#55c6ff;font-weight:900;font-size:22px}.split{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center}.pills{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}.pill{padding:9px 12px;border-radius:999px;border:1px solid #1c4f80;color:#c9d9ea;background:#061226;font-size:12px}.pricing{display:grid;grid-template-columns:1fr 1fr;gap:18px}.price{font-size:44px;font-weight:900;margin:12px 0}.muted{color:var(--muted)}.form-shell{width:min(620px,92%);margin:70px auto}.form-card{padding:32px;border-radius:20px;background:linear-gradient(180deg,rgba(9,23,44,.98),rgba(3,10,21,.98));border:1px solid rgba(58,166,255,.28);box-shadow:0 30px 80px rgba(0,0,0,.4)}.fields{display:grid;grid-template-columns:1fr 1fr;gap:15px}.field{display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}.field label{font-size:12px;color:#a9bdd3;font-weight:700}.field input,.field textarea,.field select{width:100%;padding:13px 14px;border-radius:10px;border:1px solid #204a76;background:#030b19;color:#fff;outline:none}.field input:focus,.field textarea:focus{border-color:#38a7ff;box-shadow:0 0 0 3px rgba(21,156,255,.1)}.notice{padding:12px 14px;border-radius:10px;margin:14px 0;font-size:13px}.notice.error{background:rgba(255,67,91,.1);border:1px solid rgba(255,67,91,.3);color:#ffb7c0}.notice.success{background:rgba(74,218,87,.09);border:1px solid rgba(74,218,87,.3);color:#aef2b5}.dashboard-layout{display:grid;grid-template-columns:240px 1fr;min-height:calc(100vh - 76px)}.sidebar{padding:25px 15px;border-right:1px solid rgba(39,110,180,.2);background:rgba(3,10,21,.78)}.side-link{display:block;padding:12px 13px;border-radius:9px;color:#a9bdd3;margin-bottom:5px}.side-link:hover,.side-link.active{background:#082040;color:#fff}.main{padding:35px}.dashboard-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.kpi{padding:20px}.kpi strong{font-size:30px}.table-wrap{overflow:auto}.table{width:100%;border-collapse:collapse}.table th,.table td{padding:12px;border-bottom:1px solid #14365f;text-align:left;font-size:13px}.table th{color:#8fb4d7}.code{min-height:270px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}.status{display:none;margin-top:12px;padding:10px 12px;border:1px solid #174d7d;background:#06162a;border-radius:9px;color:#9bd5ff}.download-box{padding:24px;border:1px solid rgba(215,173,79,.3);background:linear-gradient(135deg,rgba(32,25,9,.45),rgba(6,19,37,.8));border-radius:16px}.footer{padding:45px 0;border-top:1px solid rgba(39,110,180,.2);color:#8ea4bd}.reveal{opacity:0;transform:translateY(18px);transition:.7s}.reveal.show{opacity:1;transform:none}
@media(max-width:950px){.hero-grid,.split,.pricing{grid-template-columns:1fr}.feature-grid{grid-template-columns:repeat(2,1fr)}.stats{grid-template-columns:repeat(2,1fr)}.dashboard-layout{grid-template-columns:1fr}.sidebar{position:static;border-right:0;border-bottom:1px solid rgba(39,110,180,.2)}.navlinks{display:none}.main{padding:25px}.dashboard-grid{grid-template-columns:1fr}}
@media(max-width:600px){.feature-grid{grid-template-columns:1fr}.fields{grid-template-columns:1fr}.field.full{grid-column:auto}.hero{padding-top:60px}.hero h1{font-size:48px}.nav{min-height:68px}.actions .btn{padding:10px 11px;font-size:12px}}
</style>'''


def layout(title, body, scripts="", dashboard=False):
    user = current_user()
    nav = f'''<header class="topbar"><div class="container nav"><a class="brand" href="{url_for('home')}">DACRE<small>ANALYSIS</small></a><nav class="navlinks"><a href="{url_for('home')}#features">Capabilities</a><a href="{url_for('home')}#workspace">Workspace</a><a href="{url_for('home')}#pricing">Pricing</a></nav><div class="actions">{('<a class="btn" href="'+url_for('dashboard')+'">Workspace</a>' if user else '<a class="btn" href="'+url_for('login')+'">Log in</a><a class="btn btn-green" href="'+url_for('signup')+'">Get started</a>')}</div></div></header>'''
    if dashboard:
        nav = ''
    flashes = ''.join(f'<div class="notice {cat}">{clean(msg,1000)}</div>' for cat,msg in session.pop('_flashes', []))
    return render_template_string(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#020713"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="DACRE Analysis"><title>{clean(title,100)} · DACRE Analysis</title><link rel="manifest" href="{{{{ url_for('manifest') }}}}"><link rel="icon" type="image/png" sizes="192x192" href="{{{{ url_for('static', filename='dacre-logo.png') }}}}"><link rel="apple-touch-icon" sizes="512x512" href="{{{{ url_for('static', filename='dacre-icon-512.png') }}}}">{BASE_CSS}</head><body>{nav}<main class="container">{flashes}{body}</main><script>{scripts}</script></body></html>''')


@app.context_processor
def inject_globals():
    return {"csrf": csrf_token()}


@app.route('/manifest.webmanifest')
def manifest():
    return jsonify({
        "name":"DACRE Analysis", "short_name":"DACRE", "description":"Premium data analysis workspace",
        "start_url":"/", "scope":"/", "display":"standalone", "background_color":"#020713", "theme_color":"#020713",
        "icons":[{"src":"/static/dacre-icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/static/dacre-icon-512.png","sizes":"512x512","type":"image/png"}]
    })


@app.route('/sw.js')
def service_worker():
    js = '''const CACHE='dacre-static-v2'; const STATIC=['/static/dacre-logo.png','/static/landing-hero.png','/static/dashboard-preview.png','/static/global-data-sync.png']; self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(STATIC)).then(()=>self.skipWaiting()))); self.addEventListener('activate',e=>e.waitUntil(self.clients.claim())); self.addEventListener('fetch',e=>{if(e.request.method!=='GET') return; const u=new URL(e.request.url); if(u.origin!==self.location.origin) return; if(u.pathname.startsWith('/static/')){e.respondWith(caches.match(e.request).then(x=>x||fetch(e.request).then(r=>{const copy=r.clone(); caches.open(CACHE).then(c=>c.put(e.request,copy)); return r;}))); return;} if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).then(r=>{const copy=r.clone(); caches.open(CACHE).then(c=>c.put('/',copy)); return r;}).catch(()=>caches.match('/')));}});'''
    return app.response_class(js, mimetype='application/javascript')


@app.route('/')
def home():
    body = '''<section class="hero"><div class="hero-grid"><div><div class="eyebrow">DACRE Analysis · Premium Data Intelligence</div><h1>Data Today,<br><span class="gradient">Smarter Tomorrows.</span></h1><p class="lead">A premium workspace for getting data, cleaning it, analysing it, visualizing it, building dashboards, writing SQL, preparing reports and exporting decision-ready work.</p><div class="hero-actions"><a class="btn btn-green" href="/signup">Get started with DACRE Analysis</a><a class="btn" href="/login">Log in now</a><button class="btn btn-gold" id="installBtn">Download DACRE App</button></div><div id="installNote" class="muted" style="font-size:12px"></div><div class="stats"><div class="stat"><b>Data</b><span>Workspace & cleaning</span></div><div class="stat"><b>SQL</b><span>Code Space</span></div><div class="stat"><b>BI</b><span>Dashboards & reports</span></div><div class="stat"><b>DI</b><span>Intelligence assistance</span></div></div></div><div class="hero-art"><img src="/static/landing-hero.png" alt="DACRE Analysis workspace"></div></div></section>
<section class="section" id="features"><div class="section-head"><div class="eyebrow">One serious workspace</div><h2>Everything DACRE Analysis is built to do.</h2><p>Move from raw data to professional deliverables without jumping between disconnected tools.</p></div><div class="feature-grid"><div class="card reveal"><div class="icon">01</div><h3>Get Data</h3><p>Bring datasets into a structured workspace from supported files and, later, connected sources.</p></div><div class="card reveal"><div class="icon">02</div><h3>Clean Data</h3><p>Prepare datasets, identify missing values, duplicates and inconsistent fields.</p></div><div class="card reveal"><div class="icon">03</div><h3>Analyse Data</h3><p>Explore trends, distributions, relationships, performance and useful business signals.</p></div><div class="card reveal"><div class="icon">04</div><h3>Visualize</h3><p>Create decision-focused charts including bar, line, pie, area and scatter visualizations.</p></div><div class="card reveal"><div class="icon">05</div><h3>Dashboard Studio</h3><p>Arrange important metrics and visualizations into polished dashboard experiences.</p></div><div class="card reveal"><div class="icon">06</div><h3>Reports</h3><p>Turn findings into structured, presentation-ready business reports.</p></div><div class="card reveal"><div class="icon">07</div><h3>Power BI</h3><p>Prepare the product architecture for Power BI connections, reports and workspace workflows.</p></div><div class="card reveal"><div class="icon">08</div><h3>File Vault</h3><p>Keep approved outputs and implementations organized in your account workspace.</p></div><div class="card reveal"><div class="icon">09</div><h3>SQL Code Space</h3><p>Describe a data task, generate SQL/code, review it, run it and approve implementation.</p></div><div class="card reveal"><div class="icon">10</div><h3>Connections</h3><p>Design a central place for future database and service connections.</p></div><div class="card reveal"><div class="icon">11</div><h3>David Intelligence</h3><p>DI workers operate behind the interface to assist with coding, analysis, validation and refinement.</p></div><div class="card reveal"><div class="icon">12</div><h3>Export</h3><p>Create spreadsheet-ready outputs and other professional data deliverables.</p></div></div></section>
<section class="section" id="workspace"><div class="split"><div><div class="eyebrow">The real workspace</div><h2>From the landing page into the actual DACRE environment.</h2><p class="lead">The dashboard preview below represents the application workspace users enter after account creation. The landing page is the front door; the authenticated workspace is where the data work happens.</p><div class="pills"><span class="pill">Data Workspace</span><span class="pill">Dashboard Studio</span><span class="pill">Reports</span><span class="pill">Power BI</span><span class="pill">Connections</span><span class="pill">File Vault</span><span class="pill">SQL Code Space</span></div></div><img class="wide-img" src="/static/dashboard-preview.png" alt="DACRE Analysis dashboard"></div></section>
<section class="section"><div class="split"><img class="wide-img" src="/static/global-data-sync.png" alt="Global Data Sync visualization"><div><div class="eyebrow">Data intelligence at scale</div><h2>See the data. Understand the signal.</h2><p class="lead">A visual-first environment designed for analysts, teams and organizations that need their data presented clearly and professionally.</p></div></div></section>
<section class="section" id="pricing"><div class="section-head"><div class="eyebrow">Simple access</div><h2>Start with a 30-day free trial.</h2></div><div class="pricing"><div class="card"><h3>DACRE Analysis</h3><div class="price">₦30,000<span style="font-size:15px"> / month</span></div><p>30-day free trial for standard DACRE Analysis accounts.</p><a class="btn btn-green" href="/signup">Create account</a></div><div class="download-box"><h3>Keep DACRE on your phone</h3><p class="muted">Use the download/install button above to install DACRE Analysis as a persistent app on supported phones. Your account and data remain on the server; the installed app is the phone's secure shortcut/workspace shell.</p></div></div></section>'''
    scripts = '''let deferredPrompt=null; const btn=document.getElementById('installBtn'), note=document.getElementById('installNote'); window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferredPrompt=e;}); btn?.addEventListener('click',async()=>{if(deferredPrompt){deferredPrompt.prompt(); await deferredPrompt.userChoice; deferredPrompt=null;}else{note.textContent='On iPhone: open this site in Safari → Share → Add to Home Screen. On Android: use the browser menu → Install app / Add to Home screen.';}}); window.addEventListener('appinstalled',()=>{note.textContent='DACRE Analysis is installed on this device.';}); if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(()=>{}); const obs=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting&&e.target.classList.add('show')),{threshold:.12}); document.querySelectorAll('.reveal').forEach(x=>obs.observe(x));'''
    return layout('Premium Data Intelligence', body, scripts)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        if not require_csrf():
            flash('Security check failed. Please try again.', 'error'); return redirect(url_for('signup'))
        account=clean(request.form.get('account_name'),100); company=clean(request.form.get('company_name'),150); email=clean(request.form.get('email'),200).lower(); phone=clean(request.form.get('phone'),40); website=clean(request.form.get('company_website'),300); passkey=request.form.get('passkey','')
        if not all([account,company,email,phone,passkey]): flash('Please complete all required fields.', 'error')
        elif not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',email): flash('Enter a valid email address.', 'error')
        elif len(passkey)<8: flash('Account passkey must be at least 8 characters.', 'error')
        else:
            try:
                with get_db() as conn:
                    conn.execute('INSERT INTO users(account_name,company_name,email,phone,company_website,passkey_hash,created_at) VALUES(?,?,?,?,?,?,?)',(account,company,email,phone,website,generate_password_hash(passkey),utc_now()))
                flash('Account created successfully. You can now log in.', 'success'); return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('An account with that email or account/company combination already exists.', 'error')
    body='''<div class="form-shell"><div class="form-card"><div class="eyebrow">Create your DACRE account</div><h1 style="font-size:40px;margin:12px 0">Get started.</h1><p class="muted">30-day free trial · ₦30,000/month after trial</p><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf }}"><div class="fields"><div class="field"><label>Account name *</label><input name="account_name" required maxlength="100"></div><div class="field"><label>Company name *</label><input name="company_name" required maxlength="150"></div><div class="field"><label>Email address *</label><input type="email" name="email" required maxlength="200"></div><div class="field"><label>Phone number *</label><input name="phone" required maxlength="40"></div><div class="field full"><label>Company website — optional</label><input type="url" name="company_website" placeholder="https://example.com" maxlength="300"></div><div class="field full"><label>Account passkey *</label><input type="password" name="passkey" minlength="8" required autocomplete="new-password"></div></div><button class="btn btn-green" style="width:100%;margin-top:18px">Create account</button></form><p class="muted" style="text-align:center;margin-top:18px">Already have an account? <a href="/login" style="color:#62c5ff">Log in</a></p></div></div>'''
    return layout('Create Account', body)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if not require_csrf(): flash('Security check failed. Please try again.','error'); return redirect(url_for('login'))
        account=clean(request.form.get('account_name'),100); company=clean(request.form.get('company_name'),150); passkey=request.form.get('passkey','')
        with get_db() as conn:
            user=conn.execute('SELECT * FROM users WHERE account_name=? AND company_name=?',(account,company)).fetchone()
            if not user: flash('This account has not been created yet. Please create a DACRE Analysis account first.','error')
            elif not check_password_hash(user['passkey_hash'],passkey): flash('Incorrect account passkey.','error')
            else:
                session.clear(); session.permanent=True; session['user_id']=user['id']; session['csrf_token']=secrets.token_urlsafe(32)
                conn.execute('UPDATE users SET last_login=? WHERE id=?',(utc_now(),user['id'])); conn.commit(); return redirect(url_for('dashboard'))
    body='''<div class="form-shell"><div class="form-card"><div class="eyebrow">DACRE Analysis access</div><h1 style="font-size:40px;margin:12px 0">Welcome back.</h1><p class="muted">Use the account details you created during signup.</p><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf }}"><div class="field"><label>Account name *</label><input name="account_name" required></div><div class="field" style="margin-top:14px"><label>Company name *</label><input name="company_name" required></div><div class="field" style="margin-top:14px"><label>Account passkey *</label><input type="password" name="passkey" required autocomplete="current-password"></div><button class="btn btn-primary" style="width:100%;margin-top:18px">Log in now</button></form><p class="muted" style="text-align:center;margin-top:18px">No account? <a href="/signup" style="color:#62c5ff">Create one</a></p></div></div>'''
    return layout('Log In', body)


@app.route('/logout')
@login_required
def logout():
    session.clear(); return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    user=current_user()
    with get_db() as conn:
        datasets=conn.execute('SELECT * FROM datasets WHERE user_id=? ORDER BY id DESC',(user['id'],)).fetchall()
        vault=conn.execute('SELECT * FROM vault_items WHERE user_id=? ORDER BY id DESC LIMIT 10',(user['id'],)).fetchall()
    rows=''.join(f'<tr><td>{clean(d["filename"],100)}</td><td>{d["row_count"]}</td><td>{clean(d["uploaded_at"],40)}</td></tr>' for d in datasets) or '<tr><td colspan="3">No datasets yet.</td></tr>'
    vrows=''.join(f'<tr><td>{clean(v["name"],100)}</td><td>{clean(v["kind"],50)}</td><td>{clean(v["created_at"],40)}</td></tr>' for v in vault) or '<tr><td colspan="3">No approved File Vault items yet.</td></tr>'
    body=f'''<div class="dashboard-layout" style="width:100vw;margin-left:calc((1200px - 100vw)/2);max-width:100vw"><aside class="sidebar"><div class="brand" style="padding:5px 13px 20px">DACRE<small>ANALYSIS</small></div><a class="side-link active" href="/dashboard">Overview</a><a class="side-link" href="#data">Data Workspace</a><a class="side-link" href="/sql-code-space">SQL Code Space</a><a class="side-link" href="#vault">File Vault</a><a class="side-link" href="#reports">Reports</a><a class="side-link" href="#powerbi">Power BI</a><a class="side-link" href="#connections">Connections</a><a class="side-link" href="/logout">Log out</a></aside><main class="main" style="min-width:0"><div style="display:flex;justify-content:space-between;gap:15px;align-items:center;flex-wrap:wrap"><div><div class="eyebrow">Authenticated workspace</div><h1 style="margin:7px 0">Welcome, {clean(user['account_name'],100)}.</h1><p class="muted">{clean(user['company_name'],150)}</p></div><a class="btn btn-green" href="/sql-code-space">Open SQL Code Space</a></div><div class="dashboard-grid" style="margin-top:25px"><div class="card kpi"><span class="muted">Datasets</span><strong>{len(datasets)}</strong></div><div class="card kpi"><span class="muted">File Vault</span><strong>{len(vault)}</strong></div><div class="card kpi"><span class="muted">Trial</span><strong>30d</strong></div></div><section class="section" id="data" style="padding:45px 0 20px"><div class="section-head"><div class="eyebrow">Data Workspace</div><h2>Bring your data in.</h2></div><div class="card"><form action="/upload-dataset" method="post" enctype="multipart/form-data"><input type="hidden" name="csrf_token" value="{csrf_token()}"><input type="file" name="dataset" accept=".csv,.xlsx" required><button class="btn btn-primary" style="margin-left:8px">Upload dataset</button></form></div><div class="card" style="margin-top:15px"><div class="table-wrap"><table class="table"><thead><tr><th>File</th><th>Rows</th><th>Uploaded</th></tr></thead><tbody>{rows}</tbody></table></div></div></section><section class="section" id="vault" style="padding:25px 0"><div class="section-head"><div class="eyebrow">File Vault</div><h2>Approved outputs.</h2></div><div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Name</th><th>Type</th><th>Created</th></tr></thead><tbody>{vrows}</tbody></table></div></div></section><section id="reports" class="card" style="margin:15px 0"><h3>Reports</h3><p>Professional report workspace is ready for the next implementation phase.</p></section><section id="powerbi" class="card" style="margin:15px 0"><h3>Power BI</h3><p>Connection and report workflows are reserved for backend integration.</p></section><section id="connections" class="card" style="margin:15px 0"><h3>Connections</h3><p>Database and service connection management will be added here.</p></section></main></div>'''
    return layout('Workspace', body, dashboard=True)


@app.route('/upload-dataset', methods=['POST'])
@login_required
def upload_dataset():
    if not require_csrf(): flash('Security check failed.','error'); return redirect(url_for('dashboard'))
    f=request.files.get('dataset'); user=current_user()
    if not f or not f.filename: flash('Choose a CSV or XLSX file.','error'); return redirect(url_for('dashboard'))
    name=secure_filename(f.filename)
    ext=Path(name).suffix.lower().lstrip('.')
    if ext not in ALLOWED_UPLOADS: flash('Only CSV and XLSX files are supported.','error'); return redirect(url_for('dashboard'))
    user_dir=UPLOAD_DIR/str(user['id']); user_dir.mkdir(exist_ok=True)
    stored=user_dir/(secrets.token_hex(8)+'_'+name)
    try:
        if ext=='csv':
            raw=f.read(); text=raw.decode('utf-8-sig',errors='replace'); rows=list(csv.reader(io.StringIO(text))); count=max(0,len(rows)-1); stored.write_bytes(raw)
        else:
            data=f.read(); wb=load_workbook(io.BytesIO(data),read_only=True,data_only=True); ws=wb.active; count=max(0,(ws.max_row or 1)-1); wb.close(); stored.write_bytes(data)
        with get_db() as conn: conn.execute('INSERT INTO datasets(user_id,filename,stored_path,row_count,uploaded_at) VALUES(?,?,?,?,?)',(user['id'],name,str(stored),count,utc_now()))
        flash(f'{name} was added to your Data Workspace.','success')
    except Exception:
        if stored.exists(): stored.unlink(missing_ok=True)
        flash('The dataset could not be read. Please check that the file is a valid CSV or XLSX.','error')
    return redirect(url_for('dashboard'))


def basic_sql_generator(prompt):
    p=prompt.lower()
    if 'monthly' in p and 'sales' in p: return "SELECT DATE_TRUNC('month', sale_date) AS month, SUM(amount) AS total_sales FROM sales GROUP BY 1 ORDER BY 1;"
    if 'count' in p and 'customer' in p: return 'SELECT COUNT(*) AS customer_count FROM customers;'
    if 'average' in p or 'avg' in p: return 'SELECT AVG(amount) AS average_amount FROM data_table;'
    return '-- Prociel draft\n-- Review the schema before running.\nSELECT *\nFROM data_table\nLIMIT 100;'


@app.route('/sql-code-space',methods=['GET','POST'])
@login_required
def sql_space():
    generated=''; prompt=''
    if request.method=='POST':
        if not require_csrf(): flash('Security check failed.','error'); return redirect(url_for('sql_space'))
        prompt=clean(request.form.get('request'),2000)
        if prompt: generated=basic_sql_generator(prompt)
    body=f'''<section class="section"><div class="section-head"><div class="eyebrow">SQL Code Space</div><h1>Describe the task. Prociel prepares the code.</h1><p>Current mode is safe preview-first. Real database execution is deliberately disabled until a database connection is configured.</p></div><div class="card"><form method="post"><input type="hidden" name="csrf_token" value="{csrf_token()}"><div class="field"><label>Your request</label><textarea name="request" rows="5" placeholder="Example: create a SQL query that shows monthly sales by region">{clean(prompt,2000)}</textarea></div><div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap"><button class="btn" type="button" onclick="startVoice()">🎙 Voice</button><button class="btn btn-primary">Send to Prociel</button></div></form><div id="status" class="status"></div></div><div class="card" style="margin-top:15px"><h3>Generated Code</h3><textarea class="code" id="codeBox">{clean(generated,10000) or '-- Generated SQL will appear here --'}</textarea><div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap"><button class="btn btn-primary" type="button" onclick="runCode()">Run Code</button><button class="btn" type="button" onclick="copyCode()">Copy</button></div><div id="runStatus" class="status"></div></div><div class="card" style="margin-top:15px"><h3>Implementation Preview</h3><p class="muted">Exiel never saves code to File Vault automatically. Approval is required.</p><div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-green" type="button" onclick="addToVault()">Add to File Vault</button><button class="btn" type="button" onclick="document.getElementById('codeBox').focus()">Edit</button><button class="btn btn-danger" type="button" onclick="document.getElementById('codeBox').value=''">Discard</button></div><div id="vaultStatus" class="status"></div></div></section>'''
    scripts='''function status(id,t){const e=document.getElementById(id);e.style.display='block';e.textContent=t;} async function runCode(){status('runStatus','Exiel — Running your code...');await new Promise(r=>setTimeout(r,700));status('runStatus','Validiel — Checking the result...');await new Promise(r=>setTimeout(r,500));status('runStatus','DACRE — Implementation preview is ready. Nothing has been saved.');} async function addToVault(){const content=document.getElementById('codeBox').value; const r=await fetch('/api/vault',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':document.querySelector('[name=csrf_token]').value},body:JSON.stringify({name:'SQL implementation',kind:'SQL',content})}); const d=await r.json(); status('vaultStatus',d.ok?'DACRE — Added to File Vault.':'Could not add to File Vault.');} function copyCode(){navigator.clipboard?.writeText(document.getElementById('codeBox').value);status('runStatus','Code copied.');} function startVoice(){const R=window.SpeechRecognition||window.webkitSpeechRecognition;if(!R){status('status','Voice input is not supported by this browser.');return;}const r=new R();r.lang='en-US';r.interimResults=false;r.onstart=()=>status('status','Listening...');r.onresult=e=>{document.querySelector('[name=request]').value=e.results[0][0].transcript;status('status','Voice captured. Press Send to continue.');};r.onerror=()=>status('status','Voice capture could not be completed.');r.start();}'''
    return layout('SQL Code Space',body,scripts)


@app.route('/api/vault',methods=['POST'])
@login_required
def api_vault():
    if not secrets.compare_digest(request.headers.get('X-CSRF-Token',''),session.get('csrf_token','')): return jsonify(error='Security check failed'),403
    data=request.get_json(silent=True) or {}; name=clean(data.get('name'),150); kind=clean(data.get('kind'),50); content=clean(data.get('content'),30000)
    if not content: return jsonify(error='Nothing to save'),400
    with get_db() as conn: conn.execute('INSERT INTO vault_items(user_id,name,kind,content,created_at) VALUES(?,?,?,?,?)',(current_user()['id'],name or 'Untitled',kind or 'File',content,utc_now()))
    return jsonify(ok=True)


@app.route('/generate-sheet',methods=['POST'])
@login_required
def generate_sheet():
    if not require_csrf(): return jsonify(error='Security check failed'),403
    payload=request.get_json(silent=True) or {}; title=clean(payload.get('title'),100) or 'DACRE Analysis Data'; rows=payload.get('rows') or [['Metric','Value','Status'],['Example records',100,'Ready'],['Generated by','DACRE Analysis','Complete']]
    if not isinstance(rows,list) or any(not isinstance(r,list) for r in rows): return jsonify(error='rows must be an array of arrays'),400
    wb=Workbook(); ws=wb.active; ws.title='DACRE Data'
    for row in rows[:10000]: ws.append([clean(v,10000) if isinstance(v,str) else v for v in row[:100]])
    out=io.BytesIO(); wb.save(out); out.seek(0); filename=re.sub(r'[^A-Za-z0-9 _-]','_',title)+'.xlsx'
    return send_file(out,as_attachment=True,download_name=filename,mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/api/di',methods=['POST'])
@login_required
def di_api():
    if not secrets.compare_digest(request.headers.get('X-CSRF-Token',''),session.get('csrf_token','')): return jsonify(error='Security check failed'),403
    payload=request.get_json(silent=True) or {}; msg=clean(payload.get('message'),6000)
    if not msg: return jsonify(error='Message is required.'),400
    if not GOOGLE_API_KEY or requests is None: return jsonify(ok=True,configured=False,response='DI backend is ready. Configure GOOGLE_API_KEY on the server to enable live web-grounded generation.')
    endpoint=f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}'
    body={'contents':[{'role':'user','parts':[{'text':'You are DACRE Analysis David Intelligence (DI). Help with data analysis, SQL, spreadsheets, reports and business intelligence. Use fresh web information when needed. User request:\n\n'+msg}]}],'tools':[{'google_search':{}}]}
    try:
        r=requests.post(endpoint,json=body,timeout=25); data=r.json()
        if r.status_code>=400: return jsonify(error=data),r.status_code
        parts=[p['text'] for c in data.get('candidates',[]) for p in c.get('content',{}).get('parts',[]) if 'text' in p]
        return jsonify(ok=True,configured=True,response='\n'.join(parts).strip())
    except Exception: return jsonify(error='The DI service could not be reached.'),502


@app.route('/health')
def health():
    return jsonify(app='DACRE Analysis',status='online',database=DB_PATH.exists(),google_api_configured=bool(GOOGLE_API_KEY),pwa=True)


@app.errorhandler(413)
def too_large(_):
    return jsonify(error='File is too large. Maximum upload size is 25 MB.'),413


if __name__=='__main__':
    host=os.getenv('HOST','0.0.0.0'); port=int(os.getenv('PORT','5000'))
    print(f'DACRE Analysis running on http://127.0.0.1:{port}')
    app.run(host=host,port=port,debug=False)
