import hashlib
import hmac
import io
import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
import smtplib

try:
    import speech_recognition as sr
except Exception:
    sr = None

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =============================================================================
# DACRE ANALYSIS ENGINE
# DI = DAVID'S INTELLIGENCE
# Enhanced build: landing page + natural DI chat + voice + company admin portal
# + audit/notifications + optional online knowledge.
# Existing analytics, formulas, charts, vault and exports are retained.
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "").strip()

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png",
    "dacre_logo.png",
    "logo.png",
]
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

ONLINE_IMAGES = {
    "analytics": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=82",
    "cleaning": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=82",
    "charts": "https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=1200&q=82",
    "conversation": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=82",
}
DI_AVATAR_PATH = BASE_DIR / "di_avatar.png"

# =============================================================================
# BRAND / FAVICON
# =============================================================================

def prepare_favicon():
    if not LOGO_PATH.exists():
        return None
    try:
        source = Image.open(LOGO_PATH).convert("RGBA")
        width, height = source.size
        top = int(height * 0.08)
        bottom = int(height * 0.64)
        crop = source.crop((0, top, width, bottom))
        side = min(crop.size)
        left = (crop.width - side) // 2
        crop_top = max(0, (crop.height - side) // 2)
        crop = crop.crop((left, crop_top, left + side, crop_top + side))
        crop.thumbnail((128, 128), Image.Resampling.LANCZOS)
        crop.save(FAVICON_PATH, format="PNG", optimize=True)
        return str(FAVICON_PATH)
    except Exception:
        return str(LOGO_PATH)

FAVICON = prepare_favicon()

st.set_page_config(
    page_title=f"{APP_NAME} | {DI_NAME}",
    page_icon=FAVICON if FAVICON else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DATABASE
# =============================================================================

def db():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


PBKDF2_ITERATIONS = 600_000

def hash_password(value, salt=None, iterations=PBKDF2_ITERATIONS):
    """Create a salted PBKDF2 password hash. Format: pbkdf2_sha256$iterations$salt$hash."""
    if salt is None:
        salt = os.urandom(16)
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)
    digest = hashlib.pbkdf2_hmac("sha256", str(value).encode("utf-8"), salt, int(iterations))
    return f"pbkdf2_sha256${int(iterations)}${salt.hex()}${digest.hex()}"


def verify_password(value, stored):
    """Verify modern PBKDF2 hashes and transparently accept legacy SHA-256 hashes."""
    if not stored:
        return False, False
    if stored.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_hex, digest_hex = stored.split("$", 3)
            salt = bytes.fromhex(salt_hex)
            candidate = hashlib.pbkdf2_hmac("sha256", str(value).encode("utf-8"), salt, int(iterations)).hex()
            return hmac.compare_digest(candidate, digest_hex), False
        except Exception:
            return False, False
    legacy = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored), True


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            email_password TEXT,
            password_hash TEXT NOT NULL,
            passkey_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            login_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            project_name TEXT NOT NULL,
            active_filename TEXT,
            raw_json TEXT,
            processed_json TEXT,
            formula_logs TEXT,
            chart_config TEXT,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_email TEXT NOT NULL,
            recipient_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            sender_email TEXT,
            status TEXT NOT NULL,
            sent_at TEXT NOT NULL
        )
    """)

    # New additions; IF NOT EXISTS keeps existing databases intact.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            target_username TEXT,
            event_type TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Master DI workforce registry. Existing databases are preserved.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS di_agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            di_name TEXT UNIQUE NOT NULL,
            di_code TEXT UNIQUE NOT NULL,
            specialty TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            assigned_company TEXT,
            system_role TEXT,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_active TEXT
        )
    """)

    con.commit()
    con.close()


init_db()


def ensure_master():
    if not MASTER_PASSKEY:
        # Do not create a usable master account until the deployment secret is configured.
        return
    con = db()
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (MASTER_USERNAME,))
    if not cur.fetchone():
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute("""
            INSERT INTO users
            (first_name, last_name, username, company_name, email, email_password,
             password_hash, passkey_hash, role, login_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "David", "Emenike", MASTER_USERNAME, "DACRE MASTER", "master@dacre.local", "",
            hash_password(MASTER_PASSKEY), hash_password(MASTER_PASSKEY), "master", 0, now,
        ))
        con.commit()
    con.close()


ensure_master()


def maybe_upgrade_password_hash(con, username, supplied_value, stored_hash, column="passkey_hash"):
    """Upgrade a legacy SHA-256 credential after a successful login."""
    ok, legacy = verify_password(supplied_value, stored_hash)
    if ok and legacy:
        con.execute(f"UPDATE users SET {column}=? WHERE username=?", (hash_password(supplied_value), username))
        con.commit()
    return ok


def log_activity(username, company, action, notify_admin=True):
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    con.execute(
        "INSERT INTO activity(username, company_name, action, created_at) VALUES (?, ?, ?, ?)",
        (username, company, action, now),
    )
    if notify_admin and company and company.upper() != "DACRE MASTER":
        con.execute(
            "INSERT INTO notifications(company_name, target_username, event_type, message, created_at) VALUES (?, ?, ?, ?, ?)",
            (company, None, "activity", f"{username}: {action}", now),
        )
    con.commit()
    con.close()


def notify_company_admin(company, message, event_type="system"):
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    con.execute(
        "INSERT INTO notifications(company_name, target_username, event_type, message, created_at) VALUES (?, ?, ?, ?, ?)",
        (company, None, event_type, message, now),
    )
    con.commit()
    con.close()

# =============================================================================
# EMAIL / ADMIN DI MAIL SOURCE
# =============================================================================

def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
    full_name = f"{first_name} {last_name}".strip()
    subject = f"Welcome to DACRE Analysis — DI is now active for {company_name}!"
    body = (
        f"Hello {first_name},\n\n"
        "Welcome to DACRE Analysis. I am DI (David's Intelligence), your business and data intelligence copilot.\n\n"
        f"Your workspace for {company_name} is now active. You can upload datasets, clean and analyse them, build charts, "
        "export results and chat naturally with DI about your workspace.\n\n"
        "Please keep your DACRE Account Passkey private and do not share it with anyone. "
        "If you did not create this account, please contact the DACRE administrator.\n\n"
        "Warm regards,\nDI — David's Intelligence\nDACRE Analysis Platform"
    )

    status = "Logged & Dispatched (SMTP if configured; otherwise simulated)"
    smtp_host = os.getenv("DACRE_SMTP_HOST", "")
    smtp_port = int(os.getenv("DACRE_SMTP_PORT", "587"))
    smtp_user = os.getenv("DACRE_SMTP_USER", "")
    smtp_pass = os.getenv("DACRE_SMTP_PASSWORD", "")
    sender = os.getenv("DACRE_SMTP_FROM", smtp_user or "di-system@dacre.local")

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender, [email], msg.as_string())
            status = "Sent via configured SMTP"
        except Exception as exc:
            status = f"SMTP failed; logged only: {type(exc).__name__}"

    con = db()
    con.execute("""
        INSERT INTO emails_log
        (recipient_email, recipient_name, company_name, subject, body, sender_email, status, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, full_name, company_name, subject, body, sender, status,
        datetime.now().isoformat(timespec="seconds"),
    ))
    con.commit()
    con.close()

# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate(company_name, full_name, passkey, email=""):
    company_clean = (company_name or "").strip().lower()
    full_name_clean = (full_name or "").strip().lower()
    email_clean = (email or "").strip().lower()
    passkey_clean = (passkey or "").strip()

    if not passkey_clean:
        return None, "Please enter your Account Passkey."
    if not company_clean and not email_clean:
        return None, "Please enter your Company / Organization Name or Email Address."

    con = db()
    try:
        if (company_clean == "dacre master" or full_name_clean == "david emenike" or email_clean == "master@dacre.local") and MASTER_PASSKEY and passkey_clean == MASTER_PASSKEY:
            row = con.execute("SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?", (MASTER_USERNAME,)).fetchone()
            if row:
                return dict(row), None

        if email_clean:
            rows = con.execute("SELECT first_name,last_name,username,company_name,email,passkey_hash,role FROM users WHERE lower(email)=?", (email_clean,)).fetchall()
        else:
            rows = con.execute("SELECT first_name,last_name,username,company_name,email,passkey_hash,role FROM users WHERE lower(company_name)=?", (company_clean,)).fetchall()

        valid_rows = []
        for candidate_row in rows:
            if maybe_upgrade_password_hash(con, candidate_row["username"], passkey_clean, candidate_row["passkey_hash"]):
                valid_rows.append(candidate_row)
        rows = valid_rows

        if not rows:
            if email_clean:
                exists = con.execute("SELECT 1 FROM users WHERE lower(email)=? LIMIT 1", (email_clean,)).fetchone()
            else:
                exists = con.execute("SELECT 1 FROM users WHERE lower(company_name)=? LIMIT 1", (company_clean,)).fetchone()
            if exists:
                return None, "This account has already been created, but the passkey does not match. Please check your passkey and try again."
            return None, "This account has not been created. Please go to the Sign Up page and create your account to access DACRE Analysis."

        matched = None
        for r in rows:
            candidate = f"{r['first_name']} {r['last_name']}".strip().lower()
            if not full_name_clean or candidate == full_name_clean:
                matched = r
                break
        if matched is None:
            return None, "The account exists, but the Full Name does not match the account. Please enter the name used during Sign Up."

        now = datetime.now().isoformat(timespec="seconds")
        con.execute("UPDATE users SET login_count=login_count+1,last_login=? WHERE username=?", (now, matched["username"]))
        con.commit()
        result = {"first_name":matched["first_name"],"last_name":matched["last_name"],"username":matched["username"],"company":matched["company_name"],"email":matched["email"],"role":matched["role"]}
    finally:
        con.close()

    log_activity(result["username"], result["company"], "Signed in", notify_admin=result["role"] != "master")
    return result, None


def create_account(first, last, company, email, email_password, passkey):
    company_clean = company.strip()
    email_clean = email.strip().lower()
    passkey_clean = passkey.strip()
    if not company_clean or not email_clean or not passkey_clean:
        return False, "Please fill in Company Name, Email Address, and Account Passkey.", None

    if "@" not in email_clean or "." not in email_clean.split("@")[-1]:
        return False, "Please enter a valid email address.", None

    email_prefix = email_clean.split("@")[0].replace(".", " ").replace("_", " ").title()
    first_clean = first.strip() if first and first.strip() else (email_prefix.split()[0] if email_prefix else "User")
    last_clean = last.strip() if last and last.strip() else (" ".join(email_prefix.split()[1:]) if len(email_prefix.split()) > 1 else "Member")
    username_clean = email_clean

    if username_clean == MASTER_USERNAME:
        return False, "That username/email is reserved for the Master account.", None

    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()

        # Friendly duplicate-account protection. The same email/username cannot
        # be registered twice, even if the user changes the other signup fields.
        existing_account = cur.execute(
            "SELECT first_name, last_name, company_name FROM users WHERE lower(email)=lower(?) OR lower(username)=lower(?) LIMIT 1",
            (email_clean, username_clean),
        ).fetchone()
        if existing_account:
            return False, (
                "This account has already been added. The email address you entered is already registered "
                f"for {existing_account['company_name']}. Please use the Sign In page to access your account."
            ), None

        company_row = cur.execute("SELECT name FROM companies WHERE lower(name)=lower(?)", (company_clean,)).fetchone()

        if company_row:
            # Existing company: creator becomes a normal user unless an admin explicitly grants admin rights.
            role = "user"
        else:
            cur.execute("INSERT INTO companies(name,owner_username,admin_password_hash,created_at) VALUES (?,?,?,?)",
                        (company_clean, username_clean, hash_password(passkey_clean), now))
            role = "company_admin"

        cur.execute("""
            INSERT INTO users
            (first_name,last_name,username,company_name,email,email_password,password_hash,passkey_hash,role,login_count,created_at,last_login)
            VALUES (?,?,?,?,?,?,?,?,?,1,?,?)
        """, (
            first_clean, last_clean, username_clean, company_clean, email_clean, email_password.strip(),
            hash_password(passkey_clean), hash_password(passkey_clean), role, now, now,
        ))
        con.commit()

        send_di_welcome_email(first_clean, last_clean, company_clean, email_clean, email_password.strip())
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))
        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, "Account created successfully!", {
            "first_name": first_clean, "last_name": last_clean, "username": username_clean,
            "company": company_clean, "email": email_clean, "role": role,
        }
    except sqlite3.IntegrityError:
        return False, "An account with this email address is already registered.", None
    finally:
        con.close()

# =============================================================================
# DATA ENGINE
# =============================================================================

SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json"]


def load_dataframe(uploaded_file):
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if extension == "csv":
        return pd.read_csv(uploaded_file)
    if extension == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if extension in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file)
    if extension == "json":
        return pd.read_json(uploaded_file)
    raise ValueError(f"Unsupported file type: .{extension}")


def clean_dataframe(df):
    out = df.copy()
    out.columns = [re.sub(r"\s+", " ", str(c).strip()) if str(c).strip() else f"Column_{i+1}" for i,c in enumerate(out.columns)]
    out = out.dropna(axis=0, how="all").dropna(axis=1, how="all")
    for column in out.columns:
        if out[column].dtype == "object":
            series = out[column].astype(str).replace({"nan": ""}).str.strip()
            numeric_candidate = series.str.replace(r"[\$€£₦,%]", "", regex=True).str.replace(",", "", regex=False)
            numeric = pd.to_numeric(numeric_candidate, errors="coerce")
            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[column] = numeric
            else:
                out[column] = series
    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    return "" if df is None else df.to_json(orient="split", date_format="iso")


def dataframe_from_json(value):
    if not value:
        return None
    try:
        return pd.read_json(io.StringIO(value), orient="split")
    except Exception:
        return None


def save_file(user, uploaded_file, df):
    con = db()
    con.execute("INSERT INTO files(username,company_name,filename,file_type,file_json,created_at) VALUES(?,?,?,?,?,?)",
                (user["username"], user["company"], uploaded_file.name, uploaded_file.name.rsplit(".",1)[-1].lower(), dataframe_to_json(df), datetime.now().isoformat(timespec="seconds")))
    con.commit(); con.close()
    log_activity(user["username"], user["company"], f"Saved file: {uploaded_file.name}")


def get_files(user):
    con = db(); rows = con.execute("SELECT filename,file_type,created_at,file_json FROM files WHERE company_name=? ORDER BY id DESC", (user["company"],)).fetchall(); con.close(); return rows


def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    con = db()
    existing = con.execute("SELECT id FROM projects WHERE username=? AND company_name=?", (user["username"], user["company"])).fetchone()
    payload = (user["username"], user["company"], "Main Workspace", filename or "", dataframe_to_json(raw_df), dataframe_to_json(processed_df), json.dumps(logs), json.dumps(chart_config or {}), datetime.now().isoformat(timespec="seconds"))
    if existing:
        con.execute("""UPDATE projects SET project_name=?,active_filename=?,raw_json=?,processed_json=?,formula_logs=?,chart_config=?,updated_at=? WHERE id=?""", (*payload[2:], existing["id"]))
    else:
        con.execute("""INSERT INTO projects(username,company_name,project_name,active_filename,raw_json,processed_json,formula_logs,chart_config,updated_at) VALUES(?,?,?,?,?,?,?,?,?)""", payload)
    con.commit(); con.close()


def restore_project(user):
    con = db(); row = con.execute("SELECT active_filename,raw_json,processed_json,formula_logs,chart_config FROM projects WHERE username=? AND company_name=? ORDER BY id DESC LIMIT 1", (user["username"],user["company"])).fetchone(); con.close()
    if not row: return None
    try: logs = json.loads(row["formula_logs"]) if row["formula_logs"] else []
    except Exception: logs = []
    try: chart = json.loads(row["chart_config"]) if row["chart_config"] else {}
    except Exception: chart = {}
    return {"filename":row["active_filename"],"raw":dataframe_from_json(row["raw_json"]),"processed":dataframe_from_json(row["processed_json"]),"logs":logs,"chart":chart}


def make_excel(processed_df, chart_df=None):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, sheet_name="Processed Data", index=False)
        if chart_df is not None:
            chart_df.to_excel(writer, sheet_name="Dynamic Chart", index=False)
    output.seek(0); return output.getvalue()

# =============================================================================
# FORMULA ENGINE
# =============================================================================

SHEET_FORMULAS = ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","CONCATENATE","UPPER","LOWER","TRIM"]


def apply_formula(df, formula, options):
    formula = formula.upper()
    if formula == "SUM": return pd.to_numeric(df[options["column"]], errors="coerce").sum()
    if formula == "AVERAGE": return pd.to_numeric(df[options["column"]], errors="coerce").mean()
    if formula == "COUNT": return int(pd.to_numeric(df[options["column"]], errors="coerce").count())
    if formula == "COUNTA": return int(df[options["column"]].notna().sum())
    if formula == "MAX": return pd.to_numeric(df[options["column"]], errors="coerce").max()
    if formula == "MIN": return pd.to_numeric(df[options["column"]], errors="coerce").min()
    if formula == "CONCATENATE":
        result = df[options["first"]].astype(str) + options.get("separator", " ") + df[options["second"]].astype(str)
        return "column", options["new_column"], result
    if formula in ("UPPER","LOWER","TRIM"):
        series = df[options["column"]].astype(str)
        result = series.str.upper() if formula == "UPPER" else series.str.lower() if formula == "LOWER" else series.str.strip()
        return "column", options["column"], result
    return None

# =============================================================================
# BUSINESS INTELLIGENCE LAYER — additive, non-destructive
# =============================================================================

def _numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist() if df is not None else []

def business_health(df):
    if df is None or df.empty:
        return {"score": 0, "rows": 0, "columns": 0, "missing_pct": 100.0, "duplicate_pct": 0.0, "numeric": 0}
    total_cells = max(1, df.shape[0] * df.shape[1])
    missing_pct = float(df.isna().sum().sum() / total_cells * 100)
    duplicate_pct = float(df.duplicated().mean() * 100)
    numeric = len(_numeric_columns(df))
    score = max(0, min(100, round(100 - missing_pct * 0.65 - duplicate_pct * 0.45 + min(numeric, 10) * 0.8)))
    return {"score": score, "rows": len(df), "columns": len(df.columns), "missing_pct": missing_pct, "duplicate_pct": duplicate_pct, "numeric": numeric}

def business_signals(df):
    """Return explainable, dataset-derived signals without pretending to know hidden business facts."""
    if df is None or df.empty:
        return []
    signals = []
    nums = _numeric_columns(df)
    for col in nums[:20]:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(s) < 4:
            continue
        mean = float(s.mean())
        std = float(s.std()) if len(s) > 1 else 0.0
        if std > 0:
            high = int((s > mean + 3 * std).sum())
            low = int((s < mean - 3 * std).sum())
            if high or low:
                signals.append({"type":"anomaly","column":str(col),"message":f"{col} contains {high + low} unusually distant value(s) from its average."})
        if len(s) >= 8:
            first = float(s.head(max(1, len(s)//5)).mean())
            last = float(s.tail(max(1, len(s)//5)).mean())
            if first != 0:
                change = (last - first) / abs(first) * 100
                if abs(change) >= 10:
                    direction = "up" if change > 0 else "down"
                    signals.append({"type":"trend","column":str(col),"message":f"{col} trends {direction} by about {abs(change):.1f}% between the early and recent portions of the dataset."})
    missing = df.isna().sum().sort_values(ascending=False)
    for col, count in missing[missing > 0].head(5).items():
        signals.append({"type":"quality","column":str(col),"message":f"{col} has {int(count):,} missing value(s)."})
    return signals[:12]

def build_executive_brief(df, company):
    if df is None or df.empty:
        return "There is no active dataset to brief yet. Upload your business data and I will prepare an executive review."
    health = business_health(df)
    signals = business_signals(df)
    nums = _numeric_columns(df)
    lines = [f"Executive brief for {company}.", f"The active dataset contains {len(df):,} rows across {len(df.columns):,} columns. Data health is {health['score']}/100, with {health['missing_pct']:.1f}% missing cells and {health['duplicate_pct']:.1f}% duplicate rows."]
    if nums:
        for col in nums[:5]:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if not s.empty:
                lines.append(f"{col}: total {s.sum():,.2f}; average {s.mean():,.2f}; minimum {s.min():,.2f}; maximum {s.max():,.2f}.")
    if signals:
        lines.append("Key signals: " + " ".join(x["message"] for x in signals[:5]))
    else:
        lines.append("I did not detect a strong trend or anomaly from the available numeric fields, so I would review the business context before making a recommendation.")
    return " ".join(lines)

def ask_data_question(question, df):
    """Lightweight natural-language data actions available without an external AI key."""
    if df is None:
        return "Upload a dataset first. Then ask me questions such as 'show the top products by sales', 'what is missing?', or 'give me an executive brief'."
    q = question.lower()
    nums = _numeric_columns(df)
    if any(k in q for k in ["executive brief", "business brief", "management summary", "ceo summary"]):
        return build_executive_brief(df, st.session_state.user["company"] if st.session_state.get("user") else "your organization")
    if "health" in q or "quality score" in q or "data quality" in q:
        h=business_health(df); return f"Data health is {h['score']}/100. Missing cells: {h['missing_pct']:.1f}%. Duplicate rows: {h['duplicate_pct']:.1f}%. Numeric columns: {h['numeric']}."
    if ("top" in q or "highest" in q or "largest" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        view=df[[target]].copy().sort_values(target, ascending=False).head(10)
        return f"Top 10 records by {target}: " + "; ".join(f"{i+1}. {v:,.2f}" for i,v in enumerate(view[target].tolist()))
    if ("total" in q or "sum" in q or "revenue" in q or "sales" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        return f"The total for {target} is {pd.to_numeric(df[target], errors='coerce').sum():,.2f}."
    return None

# =============================================================================
# DI KNOWLEDGE + ONLINE KNOWLEDGE
# =============================================================================

APP_KNOWLEDGE = """
DACRE Analysis is a business and data analysis workspace. Users can upload CSV, Excel, TSV and JSON files; clean datasets; remove empty rows/columns and duplicates; inspect rows and columns; run formulas such as SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM; build bar, line and area charts; save workspace state; use a File Vault; and export processed data as CSV or Excel.
DI means David's Intelligence. DI is the assistant inside DACRE Analysis. Each organization has its own workspace. The first person who creates a new organization becomes that organization's company admin. Later users joining an existing organization are regular users unless an admin grants them admin rights. Company admins can inspect users, account creation, sign-ins, file activity and changes for their organization. The master account can see system-wide activity.
""".strip()


def online_lookup(query, max_results=5):
    """Small dependency-free DuckDuckGo HTML lookup. It is optional and fails safely."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-DI/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I|re.S)
        results = []
        for href, title in items[:max_results]:
            clean_title = re.sub(r"<.*?>", "", title).strip()
            clean_href = urllib.parse.unquote(href)
            results.append((clean_title, clean_href))
        return results
    except Exception:
        return []


def build_di_context(user, df):
    context = [APP_KNOWLEDGE, f"Current organization: {user['company']}. Current user: {user['first_name']} {user['last_name']}. Role: {user['role']}."]
    if df is not None:
        context.append(f"Active dataset has {len(df):,} rows and {len(df.columns):,} columns.")
        context.append("Columns: " + ", ".join(map(str, df.columns)))
    return "\n".join(context)


def ai_generate(system_prompt, user_prompt, max_tokens=900):
    """Optional production reasoning layer. Configure DACRE_AI_API_KEY in the
    deployment environment. Without it, DACRE still uses its deterministic
    local engine and public-web lookup rather than pretending an AI call worked.
    """
    api_key=os.getenv("DACRE_AI_API_KEY","").strip()
    if not api_key:
        return None
    model=os.getenv("DACRE_AI_MODEL","gpt-4o-mini").strip()
    payload={
        "model":model,
        "messages":[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        "temperature":0.2,
        "max_tokens":max_tokens,
    }
    try:
        req=urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req,timeout=35) as response:
            data=json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def di_reply(message, user, df, allow_online=True):
    text=message.strip()
    low=text.lower()
    if not text:
        return "I am ready. Tell me the business result you want to achieve."

    name="Master David" if user["role"]=="master" else user["first_name"]
    greetings=["hello","hi","good morning","good afternoon","good evening","good day"]
    if any(p in low for p in greetings) and len(low.split())<=6:
        return f"Good day {name}. DI is online. What would you like us to work on first?"

    # Deterministic workspace intelligence remains available even without an API.
    if "what can you do" in low or "what can di do" in low:
        return "I can work with your DACRE workspace, inspect and clean data, calculate business metrics, identify missing values and duplicates, build charts, explain results, help plan reports and use current public online information when the question requires it."
    data_answer = ask_data_question(text, df)
    if data_answer:
        return data_answer
    if "how many rows" in low or "row count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df):,} rows."
    if "how many columns" in low or "column count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df.columns):,} columns."
    if "duplicate" in low:
        return "There is no active dataset yet." if df is None else f"The current dataset has {int(df.duplicated().sum()):,} duplicate rows."
    if "columns" in low and df is not None:
        return "The current columns are: " + ", ".join(map(str,df.columns))
    if "missing" in low or "empty" in low:
        if df is None: return "There is no active dataset yet. Upload a dataset and I can inspect it."
        missing=df.isna().sum().sort_values(ascending=False); top=missing[missing>0].head(8)
        if top.empty: return "I checked the active dataset. I do not see missing values in the current columns."
        return "The columns with the most missing values are: " + "; ".join(f"{c}: {int(v)}" for c,v in top.items())
    if any(k in low for k in ["describe","summary","overview"]):
        if df is None: return "There is no active dataset yet. Upload a dataset and I can summarise it."
        return f"Dataset overview: {len(df):,} rows, {len(df.columns):,} columns, {len(df.select_dtypes(include='number').columns)} numeric columns and {int(df.duplicated().sum()):,} duplicate rows."
    if any(k in low for k in ["dacre","file vault","formula lab","export center","admin portal","workspace"]):
        return "DACRE is the business workspace. You can upload and clean data, run formulas, create charts, save project state, use the File Vault, export results and work with DI. Your organization has its own workspace and administration layer."

    # For current/public questions, retrieve sources first. The model is then
    # asked to synthesize the answer and cite the source titles it actually saw.
    needs_online=allow_online and any(k in low for k in ["latest","today","current","news","price","market","recent","this week","this month","now","who is","what is","where is","when is"])
    results=online_lookup(text, max_results=5) if needs_online else []

    context=build_di_context(user,df)
    if results:
        source_text="\n".join([f"SOURCE {i+1}: {title}\nURL: {href}" for i,(title,href) in enumerate(results)])
        prompt=f"""User question: {text}\n\nDACRE context:\n{context}\n\nPublic online sources retrieved now:\n{source_text}\n\nAnswer the user's question directly and professionally. Do not say you understand the question. Use the online sources when they are relevant. If the sources do not establish a fact, say that clearly. Tell the user that you checked current online sources, and name the strongest source titles at the end. Never invent a source or claim you opened information that is not represented above."""
        answer=ai_generate("You are DI, a fast, careful business intelligence assistant inside DACRE.",prompt)
        if answer:
            return answer
        lines=["I checked current online sources for this question. The strongest results I found were:"]
        lines.extend([f"{i+1}. {title} — {href}" for i,(title,href) in enumerate(results)])
        lines.append("I could retrieve the sources, but the reasoning API is not configured on this deployment yet, so I will not pretend that I synthesized an answer from them.")
        return "\n".join(lines)

    # If an AI key is configured, give DI a real reasoning layer for general
    # business questions even when no web lookup is necessary.
    answer=ai_generate(
        "You are DI, a concise and highly capable business intelligence assistant. Answer directly. Be polite, accurate, practical and transparent about uncertainty. Never say 'I understand your request' as filler.",
        f"DACRE context:\n{context}\n\nUser question:\n{text}",
    )
    if answer:
        return answer

    return "I can answer this when it is within the DACRE workspace or when public online lookup is available. Ask me to analyse your data, explain a business problem, create a chart or research a current question, and I will take the next useful step."


def load_chat_history(user, limit=40):
    """Restore DI history safely for both old and new user-record shapes."""
    username = str(user.get("username", "")).strip()
    company = str(user.get("company_name", user.get("company", ""))).strip()
    if not username or not company:
        return []
    con = db()
    rows = con.execute(
        "SELECT sender, message FROM chat_history WHERE username=? AND company_name=? ORDER BY id DESC LIMIT ?",
        (username, company, int(limit)),
    ).fetchall()
    con.close()
    return [{"sender": r["sender"], "text": r["message"]} for r in reversed(rows)]


def verify_recaptcha_token(token):
    """Verify Google's reCAPTCHA token when DACRE_RECAPTCHA_SECRET is configured."""
    secret = os.getenv("DACRE_RECAPTCHA_SECRET", "").strip()
    if not secret or not token:
        return False
    try:
        payload = urllib.parse.urlencode({"secret": secret, "response": token}).encode()
        req = urllib.request.Request(
            "https://www.google.com/recaptcha/api/siteverify",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        return bool(data.get("success"))
    except Exception:
        return False


def transcribe_audio(audio_value):
    """Transcribe a browser recording when SpeechRecognition is installed."""
    if sr is None:
        return None, "Voice transcription package is not installed. Add SpeechRecognition to requirements.txt."
    try:
        recognizer = sr.Recognizer()
        raw = audio_value.getvalue()
        with sr.AudioFile(io.BytesIO(raw)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-NG")
        return text, None
    except sr.UnknownValueError:
        return None, "DI could not clearly understand that recording. Please speak a little slower and try again."
    except sr.RequestError:
        return None, "Voice transcription service is temporarily unavailable. You can still use text chat."
    except Exception as exc:
        return None, f"Voice transcription could not be completed: {type(exc).__name__}."

# =============================================================================
# VOICE
# =============================================================================

def speak(text):
    safe = json.dumps(text)
    components.html(f"""
    <script>
    (function() {{
      const text = {safe};
      if (!('speechSynthesis' in window)) return;
      const speak = () => {{
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-NG';
        u.rate = 0.90;
        u.pitch = 0.72;
        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v => /en-NG/i.test(v.lang)) || voices.find(v => /Nigeria|English.*Male|Male/i.test(v.name + ' ' + v.lang));
        if (preferred) u.voice = preferred;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      }};
      if (window.speechSynthesis.getVoices().length) speak();
      else window.speechSynthesis.onvoiceschanged = speak;
    }})();
    </script>
    """, height=0)

# =============================================================================
# STYLING
# =============================================================================

st.markdown("""
<style>
:root{--dacre-cyan:#18b7ff;--dacre-mint:#00dc96;--dacre-gold:#f4b942;--dacre-line:rgba(24,183,255,.25)}
.stApp{background:radial-gradient(circle at 10% 10%,rgba(24,183,255,.14),transparent 32%),radial-gradient(circle at 90% 20%,rgba(244,185,66,.10),transparent 28%),linear-gradient(135deg,#050914,#091322 55%,#050914);color:#fff}
.stApp::before{content:"";position:fixed;inset:-40%;pointer-events:none;background:conic-gradient(from 0deg at 50% 50%,rgba(24,183,255,.05),transparent 25%,rgba(255,193,7,.04) 45%,transparent 70%,rgba(0,220,150,.04) 85%,transparent 100%);animation:dacreSpin 48s linear infinite;z-index:0}
@keyframes dacreSpin{to{transform:rotate(360deg)}}
.main .block-container{position:relative;z-index:1;padding-top:2rem;max-width:1500px}
html,body,.stApp,.stApp p,.stApp li,.stApp span,.stApp label,.stMarkdown,.stMarkdown p,.stMarkdown li,[data-testid="stWidgetLabel"] p,[data-testid="stWidgetLabel"] label,.stRadio label,.stCheckbox label,.stSelectbox label,.stTextInput label,.stTextArea label,.stFileUploader label{color:#fff!important;font-weight:700!important}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{font-family:'Inter','Segoe UI',sans-serif!important;color:#fff!important;font-weight:800!important;letter-spacing:-.02em}
.stApp h3{margin-top:1.2rem;padding-left:12px;border-left:4px solid var(--dacre-cyan);text-shadow:0 0 18px rgba(24,183,255,.35)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#07101d 0%,#060d18 55%,#050914 100%);border-right:1px solid var(--dacre-line);box-shadow:24px 0 60px -40px rgba(24,183,255,.55)}
[data-testid="stSidebar"] *{color:#fff!important}
.dacre-hero{position:relative;padding:28px 30px;border-radius:22px;border:1px solid rgba(24,183,255,.35);background:linear-gradient(135deg,rgba(6,16,31,.94),rgba(10,28,47,.86));box-shadow:0 24px 60px -28px rgba(0,0,0,.9);backdrop-filter:blur(10px);margin-bottom:22px;overflow:hidden}
.dacre-hero:after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--dacre-cyan),var(--dacre-mint),var(--dacre-gold),var(--dacre-cyan));background-size:300% 100%;animation:dacreFlow 9s linear infinite}
@keyframes dacreFlow{to{background-position:300% 0}}
.dacre-title{font-size:clamp(2.2rem,5vw,4.2rem);font-weight:900;letter-spacing:-.04em;color:#fff}
.dacre-sub{font-size:1.08rem;color:#9edcff!important;font-weight:700}
.feature-card{padding:18px;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:rgba(255,255,255,.045);min-height:145px}.image-card{padding:0;overflow:hidden;min-height:270px}.image-card img{width:100%;height:150px;object-fit:cover;display:block}.image-card-body{padding:16px 18px}.image-card-body h3{margin-top:0}.di-avatar{width:92px;height:92px;border-radius:50%;object-fit:cover;border:3px solid rgba(24,183,255,.65);box-shadow:0 0 28px rgba(24,183,255,.35)}
.chat-card{padding:16px 18px;border-radius:18px;border:1px solid rgba(24,183,255,.25);background:rgba(4,12,24,.72);margin:8px 0}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:rgba(6,16,31,.92)!important;color:#fff!important;font-weight:700!important;border:1.5px solid rgba(24,183,255,.35)!important;border-radius:12px!important;padding:10px 14px!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#9aa4b2!important;font-weight:500!important}
div.stButton>button,div.stFormSubmitButton>button,div.stDownloadButton>button{border-radius:12px;border:1px solid rgba(24,183,255,.45);background:linear-gradient(135deg,#0a2540,#0d3860);color:#fff!important;font-weight:800!important;padding:10px 18px;transition:all .22s ease}
div.stButton>button:hover,div.stFormSubmitButton>button:hover,div.stDownloadButton>button:hover{border-color:var(--dacre-cyan);background:linear-gradient(135deg,#0d3860,#12508c);box-shadow:0 0 20px rgba(24,183,255,.45);transform:translateY(-1px)}
[data-testid="stMetric"]{padding:14px 18px;border-radius:16px;border:1px solid rgba(255,255,255,.10);background:linear-gradient(145deg,rgba(255,255,255,.05),rgba(255,255,255,.015))}
#MainMenu,footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

for key, default in {
    "user": None, "raw_df": None, "processed_df": None, "active_filename": "",
    "formula_logs": [], "chart_config": {}, "chat_history": [], "landing_mode": "home",
    "last_speech": None, "master_route": False,
    "master_captcha_required": False, "master_captcha_passed": False,
    "master_second_attempt": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# =============================================================================
# MASTER ADMIN / CEO OFFICE HELPERS
# =============================================================================

def master_user_record():
    con = db()
    row = con.execute(
        "SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?",
        (MASTER_USERNAME,),
    ).fetchone()
    con.close()
    if row:
        data = dict(row)
        # The application workspace consistently uses `company`. Keep the
        # database field `company_name` too so older code remains compatible.
        data["company"] = data.get("company_name", "DACRE MASTER")
        return data
    return {
        "first_name": "David", "last_name": "Emenike", "username": MASTER_USERNAME,
        "company_name": "DACRE MASTER", "company": "DACRE MASTER",
        "email": "master@dacre.local", "role": "master"
    }


def master_passkey_gate(passkey):
    if not MASTER_PASSKEY:
        return False
    ok, _ = verify_password(passkey.strip(), hash_password(MASTER_PASSKEY))
    return bool(ok)


def get_di_agents():
    con = db()
    rows = con.execute("SELECT * FROM di_agents ORDER BY id DESC").fetchall()
    con.close()
    return rows


def create_di_agent(name, specialty, status="Available", assigned_company="", system_role=""):
    name = (name or "").strip()
    specialty = (specialty or "").strip()
    assigned_company = (assigned_company or "").strip()
    system_role = (system_role or "").strip()
    if not name or not specialty:
        return False, "DI name and specialty are required."
    now = datetime.now().isoformat(timespec="seconds")
    slug = re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-") or "DI"
    code = f"DI-{slug[:24]}-{datetime.now().strftime('%H%M%S')}"
    con = db()
    try:
        con.execute(
            "INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,created_by,created_at,last_active) VALUES(?,?,?,?,?,?,?,?,?)",
            (name, code, specialty, status, assigned_company or None, system_role, MASTER_USERNAME, now, now),
        )
        con.commit()
        return True, code
    except sqlite3.IntegrityError:
        return False, "A DI with that name already exists. Choose a different name."
    finally:
        con.close()


def update_di_agent(di_id, status, assigned_company):
    con = db()
    con.execute("UPDATE di_agents SET status=?, assigned_company=?, last_active=? WHERE id=?", (status, assigned_company or None, datetime.now().isoformat(timespec="seconds"), di_id))
    con.commit()
    con.close()


def admin_metric_counts():
    con = db()
    counts = {
        "users": con.execute("SELECT COUNT(*) FROM users WHERE role!='master'").fetchone()[0],
        "companies": con.execute("SELECT COUNT(*) FROM companies").fetchone()[0],
        "activities": con.execute("SELECT COUNT(*) FROM activity").fetchone()[0],
        "messages": con.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0],
        "files": con.execute("SELECT COUNT(*) FROM files").fetchone()[0],
        "agents": con.execute("SELECT COUNT(*) FROM di_agents").fetchone()[0],
    }
    con.close()
    return counts


def landing_page():
    # Discreet CEO access: double-click the building mark. The master passkey is
    # never displayed on the public landing page.
    gate_requested = str(st.query_params.get("master_gate", "")) == "1"

    # -------------------------------------------------------------------------
    # PRIVATE CEO ENTRY POINT — one unique fixed building card.
    # Any legacy building injected by an older deployment is removed by the
    # small cleanup component before the new card is rendered.
    # -------------------------------------------------------------------------
    components.html("""
    <script>
    (function(){
      try {
        const d = window.parent.document;
        d.querySelectorAll('#dacre-ceo-building-access, #dacre-ceo-building-access-v2').forEach(function(el){ el.remove(); });
      } catch(e) {}
    })();
    </script>
    """, height=0)

    top1, top2, top3 = st.columns([5,1,1])
    with top1:
        st.markdown("### **DACRE Analysis**")
    with top2:
        if st.button("Login", use_container_width=True):
            st.session_state.landing_mode = "login"
            st.rerun()
    with top3:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.landing_mode = "signup"
            st.rerun()

    st.markdown("""
    <a id="dacre-ceo-building-access-v2" href="?master_gate=1"
       title="DACRE-ANALYSIS — CEO Office access"
       aria-label="DACRE-ANALYSIS CEO Office access"
       style="position:fixed;left:24px;bottom:24px;width:190px;height:178px;
              z-index:2147483000;display:block;overflow:hidden;
              border-radius:20px;background:#fff;border:1px solid rgba(232,106,168,.38);
              box-shadow:0 18px 55px rgba(45,25,40,.25);text-decoration:none;
              cursor:pointer;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease;">
      <div style="position:absolute;inset:0;background:#fff;">
        <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=900&q=90"
             alt="DACRE-ANALYSIS company building"
             style="width:100%;height:134px;object-fit:cover;display:block;">
        <div style="position:absolute;left:0;right:0;top:0;height:134px;
                    background:linear-gradient(180deg,rgba(8,12,18,.26),rgba(8,12,18,.02) 48%,rgba(8,12,18,.55));">
        </div>
        <div style="position:absolute;left:11px;top:10px;color:#fff;
                    font:800 12px/1.1 Inter,Segoe UI,sans-serif;letter-spacing:.11em;
                    text-shadow:0 2px 10px rgba(0,0,0,.60);">DACRE-ANALYSIS</div>
        <div style="position:absolute;left:10px;right:10px;bottom:8px;color:#17202b;
                    font:800 11px/1.2 Inter,Segoe UI,sans-serif;letter-spacing:.08em;
                    text-align:center;">CEO OFFICE</div>
      </div>
    </a>
    <style>
      #dacre-ceo-building-access-v2:hover{
        transform:translateY(-7px) scale(1.035);
        box-shadow:0 28px 72px rgba(232,106,168,.34);
        border-color:rgba(232,106,168,.82);
      }
      #dacre-ceo-building-access-v2:active{transform:translateY(-2px) scale(1.01);}
      @media (max-width:700px){
        #dacre-ceo-building-access-v2{left:12px!important;bottom:12px!important;width:154px!important;height:148px!important;}
        #dacre-ceo-building-access-v2 img{height:109px!important;}
      }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # CEO GATE
    # Stage 1: passkey. If it is wrong, require security verification.
    # Stage 2: after verification, request the passkey again. A second wrong
    # attempt sends the visitor back to the ordinary Sign Up page.
    # -------------------------------------------------------------------------
    if gate_requested:
        captcha_required = bool(st.session_state.get("master_captcha_required", False))
        captcha_passed = bool(st.session_state.get("master_captcha_passed", False))
        second_attempt = bool(st.session_state.get("master_second_attempt", False))

        st.markdown("""
        <div class="dacre-hero" style="max-width:720px;margin:35px auto 20px;text-align:center;">
          <div class="dacre-title" style="font-size:2.05rem;">Overall Admin DI — Master Access</div>
          <div class="dacre-sub" style="font-size:1.05rem;">Dear Master David, please kindly put in your account passkey. This is the private Overall Admin DI access for DACRE-ANALYSIS.</div>
        </div>
        """, unsafe_allow_html=True)

        gate_col1, gate_col2, gate_col3 = st.columns([1,2,1])
        with gate_col2:
            if captcha_required and not captcha_passed:
                st.markdown("### Security verification")
                site_key = os.getenv("DACRE_RECAPTCHA_SITE_KEY", "").strip()
                if site_key:
                    st.markdown("Google reCAPTCHA is enabled for this deployment. Complete the verification below, then continue.")
                    components.html(f"""
                    <div style="display:flex;justify-content:center;">
                      <div class="g-recaptcha" data-sitekey="{site_key}"></div>
                    </div>
                    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
                    """, height=100)
                    st.caption("For production verification, set DACRE_RECAPTCHA_SITE_KEY and DACRE_RECAPTCHA_SECRET in Streamlit Secrets. The server verifies the token before access is granted.")
                    if st.button("I completed the reCAPTCHA", use_container_width=True):
                        # The browser widget cannot safely hand its token to Python
                        # through a plain HTML iframe. Therefore production mode
                        # requires the official custom-component token bridge.
                        st.warning("Complete the Google reCAPTCHA widget first. If the verification is not being accepted, configure the DACRE reCAPTCHA component bridge and secrets.")
                else:
                    st.markdown("""
                    <div style="border:1px solid #d9d9d9;border-radius:4px;padding:16px 14px;background:#fff;max-width:430px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,.10);">
                      <div style="display:flex;align-items:center;gap:12px;">
                        <div style="width:28px;height:28px;border:1px solid #b8b8b8;border-radius:3px;background:#fafafa;"></div>
                        <div style="font:500 15px Arial,sans-serif;color:#333;">I'm not a robot</div>
                        <div style="margin-left:auto;font:11px Arial,sans-serif;color:#777;text-align:center;">reCAPTCHA<br>Privacy - Terms</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("Google reCAPTCHA is not configured on this deployment yet. This is a local security-verification fallback, not a claim that Google has verified you.")
                    if st.checkbox("Complete security verification", key="local_captcha_check"):
                        st.session_state.master_captcha_passed = True
                        st.session_state.master_second_attempt = True
                        st.rerun()

                if st.button("Return to DACRE Sign Up", use_container_width=True):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.session_state.landing_mode = "signup"
                    st.query_params.clear()
                    st.rerun()
                return

            master_pk = st.text_input("Account Passkey", type="password", placeholder="Enter your private account passkey", key="master_gate_pk")
            if second_attempt:
                st.info("Security verification completed. Please enter the passkey again.")
            g1, g2 = st.columns(2)
            with g1:
                if st.button("Open Overall Admin DI", use_container_width=True, type="primary"):
                    if master_passkey_gate(master_pk):
                        st.session_state.user = master_user_record()
                        st.session_state.master_route = True
                        st.session_state.master_captcha_required = False
                        st.session_state.master_captcha_passed = False
                        st.session_state.master_second_attempt = False
                        st.session_state.last_speech = "Welcome, Master David. The Overall Admin DI Office is online. I have the organization, user, activity and DI workforce systems ready for your direction."
                        st.query_params.clear()
                        log_activity(MASTER_USERNAME, "DACRE MASTER", "Opened Overall CEO Office", notify_admin=False)
                        st.rerun()
                    else:
                        if second_attempt:
                            st.warning("The second passkey attempt was incorrect. For security, you are being returned to the normal DACRE Sign Up page.")
                            st.session_state.master_captcha_required = False
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.session_state.landing_mode = "signup"
                            st.query_params.clear()
                            st.rerun()
                        else:
                            st.session_state.master_captcha_required = True
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.rerun()
            with g2:
                if st.button("Return to DACRE", use_container_width=True):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.query_params.clear()
                    st.rerun()
        return

    if st.session_state.landing_mode in ("login","signup"):
        c1,c2,c3=st.columns([1,2,1])
        with c2:
            if st.button("← Back to DACRE Introduction"):
                st.session_state.landing_mode="home"; st.rerun()
            tab_login,tab_signup=st.tabs(["Sign In","Sign Up"])
            with tab_login:
                st.markdown("### Access your workspace")
                login_company=st.text_input("Company / Organization Name",placeholder="e.g. Edubridge Consultant Limited",key="lin_comp")
                login_fullname=st.text_input("Full Name",placeholder="e.g. David Emenike",key="lin_fn")
                login_email=st.text_input("Email Address (recommended)",placeholder="Use the email you registered with",key="lin_email")
                login_passkey=st.text_input("Account Passkey",type="password",placeholder="Enter your account passkey",key="lin_pk")
                if st.button("Sign In & Restore Workspace",use_container_width=True):
                    auth, auth_message=authenticate(login_company,login_fullname,login_passkey,login_email)
                    if auth:
                        st.session_state.user=auth
                        st.session_state.last_speech=f"Welcome back, {auth['first_name']}. I am DI. Where would you like to start today? You can ask me a business question, upload data, investigate a problem, or ask me to research something current."
                        project=restore_project(auth)
                        if project:
                            st.session_state.active_filename=project["filename"] or ""
                            st.session_state.raw_df=project["raw"]
                            st.session_state.processed_df=project["processed"]
                            st.session_state.formula_logs=project["logs"]
                            st.session_state.chart_config=project["chart"]
                        st.toast(f"Welcome back, {auth['first_name']}!")
                        st.rerun()
                    else: st.error(auth_message or "This account has not been created. Please go to the Sign Up page and create your account to access DACRE Analysis.")
            with tab_signup:
                st.markdown("### Create a DACRE account")
                s_first=st.text_input("First Name",placeholder="e.g. David",key="su_first")
                s_last=st.text_input("Last Name",placeholder="e.g. Emenike",key="su_last")
                s_company=st.text_input("Company / Organization Name",placeholder="e.g. Edubridge Consultant Limited",key="su_comp")
                s_email=st.text_input("Email Address",placeholder="e.g. name@example.com",key="su_email")
                s_email_pass=st.text_input("Email Password (optional)",type="password",placeholder="Optional — SMTP credentials are safer",key="su_epass")
                s_passkey=st.text_input("Create Account Passkey",type="password",placeholder="Create your account passkey",key="su_passkey")
                if st.button("Create DACRE Account",use_container_width=True):
                    success,msg,created=create_account(s_first,s_last,s_company,s_email,s_email_pass,s_passkey)
                    if success:
                        st.session_state.user=created
                        st.session_state.last_speech=f"Welcome to DACRE, {created['first_name']}. I am DI, your business intelligence assistant. What would you like us to work on first?"
                        st.toast(f"Welcome to DACRE, {created['first_name']}!")
                        st.rerun()
                    else: st.error(msg)
        return

    if LOGO_PATH.exists():
        left,mid,right=st.columns([1,2,1])
        with mid: st.image(str(LOGO_PATH),use_container_width=True)

    st.markdown("""
    <div class="dacre-hero">
      <div class="dacre-title">Turn business data into decisions.</div>
      <div class="dacre-sub">DACRE Analysis combines data cleaning, analysis, visualisation, workspace memory and DI — David's Intelligence — in one business intelligence workspace.</div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("### Meet DI — your business intelligence copilot")
    st.write("DI is designed to communicate naturally with users, understand the DACRE workspace, explain data in plain business language, and help users move from a question to an actionable answer.")

    cols=st.columns(4)
    cards=[("analytics","Analyse","Upload CSV, Excel, TSV or JSON data and inspect it quickly."),("cleaning","Clean","Clean headers, empty rows/columns, numeric fields and duplicates."),("charts","Visualise","Build bar, line and area charts from your active dataset."),("conversation","Talk to DI","Chat naturally with DI about your data, workspace or wider business questions.")]
    for c,(image_key,title,desc) in zip(cols,cards):
        with c:
            st.markdown(f'<div class="feature-card image-card"><img src="{ONLINE_IMAGES[image_key]}" alt="{title}"/><div class="image-card-body"><h3>{title}</h3><p>{desc}</p></div></div>',unsafe_allow_html=True)

    st.markdown("### Built for organizations")
    st.write("Each organization gets its own workspace. The first account that creates a new organization becomes that organization's admin. Organization admins can monitor users, account creation, sign-ins and workspace changes for their organization. The master portal remains separate.")

    a,b=st.columns(2)
    with a:
        if st.button("Start with DACRE",use_container_width=True): st.session_state.landing_mode="signup"; st.rerun()
    with b:
        if st.button("I already have an account",use_container_width=True): st.session_state.landing_mode="login"; st.rerun()


if st.session_state.user is None:
    landing_page()
    st.stop()

# The CEO building belongs ONLY to the public landing page. Remove its
# fixed DOM node as soon as a user enters the application so it cannot
# remain floating over or scrolling with the workspace.
components.html("""
<script>
(function(){
  try {
    const d = window.parent.document;
    const old = d.getElementById('dacre-ceo-building-access');
    if (old) old.remove();
  } catch(e) {}
})();
</script>
""", height=0)

# Restore persistent DI conversation memory for this account.
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history(st.session_state.user, limit=40)

# =============================================================================
# DACRE USER EXPERIENCE V2 — LIGHT / WHITE / SOFT PINK BUSINESS CONSOLE
# =============================================================================
st.markdown("""
<style>
:root{--di-pink:#e86aa8;--di-pink-soft:#fff1f7;--di-pink-line:#f5d7e6;--di-ink:#17202b;--di-muted:#657180;--di-shadow:0 18px 55px rgba(33,24,40,.10)}
.stApp{background:linear-gradient(180deg,#fff 0%,#fff8fb 48%,#fff1f7 100%) !important;color:var(--di-ink) !important}
.stApp::before{display:none !important}
.main .block-container{max-width:1500px;padding-top:1.5rem;padding-bottom:4rem}
.stApp p,.stApp span,.stApp label,.stApp div,.stApp li,.stApp td,.stApp th,.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:var(--di-ink) !important}
[data-testid="stSidebar"]{background:#fff !important;border-right:1px solid var(--di-pink-line) !important;box-shadow:8px 0 30px rgba(60,30,50,.04)}
[data-testid="stSidebar"] *{color:var(--di-ink) !important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:12px;padding:8px 10px;transition:.2s ease}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:var(--di-pink-soft);transform:translateX(3px)}
.stButton>button{border:1px solid var(--di-pink-line)!important;background:#fff!important;color:var(--di-ink)!important;border-radius:12px!important;transition:.22s ease!important;box-shadow:0 5px 18px rgba(30,20,40,.05)!important}
.stButton>button:hover{border-color:var(--di-pink)!important;background:var(--di-pink-soft)!important;transform:translateY(-2px);box-shadow:0 10px 28px rgba(232,106,168,.16)!important}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;border:1px solid var(--di-pink-line)!important;color:var(--di-ink)!important;border-radius:12px!important}
.dacre-user-hero{background:linear-gradient(115deg,#fff,#fff5f9);border:1px solid var(--di-pink-line);border-radius:24px;padding:24px 28px;box-shadow:var(--di-shadow)}
.dacre-user-title{font-size:2.35rem;font-weight:800;letter-spacing:-.04em;margin-bottom:4px}
.dacre-user-sub{color:var(--di-muted)!important;font-size:1rem}
.di-command{background:linear-gradient(135deg,#fff,#fff1f7);border:1px solid #f2d4e3;border-radius:26px;box-shadow:var(--di-shadow);overflow:hidden;position:relative}
.di-stage{height:330px;position:relative;overflow:hidden;background-size:cover;background-position:center;transition:transform .5s ease,filter .5s ease}
.di-command:hover .di-stage{transform:scale(1.018);filter:saturate(1.05)}
.di-stage-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.96) 0%,rgba(255,245,249,.82) 42%,rgba(255,255,255,.20) 100%)}
.di-orb{position:absolute;right:9%;top:18%;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#f6bfd9 35%,#e86aa8 68%,rgba(232,106,168,0) 70%);box-shadow:0 0 80px rgba(232,106,168,.34);animation:diPulse 4s ease-in-out infinite}
.di-orb:after{content:"";position:absolute;inset:28px;border:1px solid rgba(255,255,255,.8);border-radius:50%;animation:diSpin 8s linear infinite}
@keyframes diPulse{50%{transform:scale(1.07);box-shadow:0 0 105px rgba(232,106,168,.42)}}
@keyframes diSpin{to{transform:rotate(360deg)}}
.di-stage-copy{position:absolute;left:30px;top:30px;max-width:58%}
.di-kicker{font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;font-weight:800;color:#b5487e!important}
.di-stage-copy h2{font-size:2.05rem;margin:.45rem 0 .55rem;font-weight:800}
.di-stage-copy p{color:#596573!important;line-height:1.55}
.di-status{display:inline-flex;align-items:center;gap:8px;padding:7px 11px;border-radius:999px;background:#fff;border:1px solid var(--di-pink-line);font-size:.82rem;font-weight:700}
.di-dot{width:8px;height:8px;border-radius:50%;background:#36b37e;box-shadow:0 0 0 5px rgba(54,179,126,.12)}
.di-transcript{padding:18px 22px;background:#fff;border-top:1px solid var(--di-pink-line);min-height:92px}
.di-transcript-label{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#9b6b83!important;font-weight:800}
.di-transcript-text{font-size:1rem;line-height:1.55;margin-top:4px}
.di-quick-card{height:100%;background:#fff;border:1px solid var(--di-pink-line);border-radius:18px;padding:18px;transition:.2s ease;box-shadow:0 10px 30px rgba(40,25,40,.05)}
.di-quick-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(232,106,168,.12);border-color:#eab5cd}
.di-metric{background:#fff;border:1px solid var(--di-pink-line);border-radius:16px;padding:16px 18px;box-shadow:0 8px 25px rgba(40,25,40,.05)}
.di-metric .v{font-size:1.55rem;font-weight:800}.di-metric .l{font-size:.78rem;color:var(--di-muted)!important;margin-top:2px}
</style>
""",unsafe_allow_html=True)

user=st.session_state.user

head_col1,head_col2=st.columns([4,1])
with head_col1:
    st.markdown(f"""<div class="dacre-user-hero"><div class="dacre-user-title">Good to have you here, {user['first_name']}.</div><div class="dacre-user-sub">{DI_NAME} is active for <b>{user['company']}</b>. Your business workspace, data tools and DI conversation are connected.</div></div>""",unsafe_allow_html=True)
with head_col2:
    if st.button("Sign Out",use_container_width=True):
        log_activity(user["username"],user["company"],"Signed out",notify_admin=user["role"] not in ("master","company_admin"))
        st.session_state.user=None
        st.rerun()

with st.sidebar:
    if LOGO_PATH.exists(): st.image(str(LOGO_PATH),use_container_width=True)
    st.markdown(f"### {user['first_name']}'s Workspace")
    st.caption(f"{user['company']} · {user['role']}")
    st.markdown("<div style='font-size:.78rem;color:#8b6577!important;margin:4px 0 14px'>DI is available across your workspace.</div>",unsafe_allow_html=True)
    navigation=["DI Home","Business Command Center","Workspace & Data","Formula Lab","Charts","File Vault","Export Center"]
    if user["role"] in ("company_admin","master"):
        navigation.append("Organization Admin Portal")
    if user["role"]=="master": navigation.append("Overall Admin DI Portal")
    default_page = "Overall Admin DI Portal" if user["role"]=="master" and st.session_state.get("master_route") else navigation[0]
    selected_page=st.radio("Navigation",navigation,index=navigation.index(default_page) if default_page in navigation else 0)

# =============================================================================
# DI HOME / CONTINUOUS BUSINESS CONVERSATION
# =============================================================================

def di_voice_bridge():
    """Browser voice bridge. Speech is captured by Chrome and sent back to the
    Streamlit app through a query parameter. The app then runs the same DI
    engine used by text chat and speaks the response with browser speech synthesis.
    """
    components.html("""
    <script>
    (() => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) return;
      if (window.__dacreVoiceStarted) return;
      window.__dacreVoiceStarted = true;
      const rec = new SpeechRecognition();
      rec.lang = 'en-NG';
      rec.continuous = true;
      rec.interimResults = false;
      rec.maxAlternatives = 1;
      rec.onresult = (event) => {
        const result = event.results[event.results.length - 1];
        if (!result || !result[0]) return;
        const text = result[0].transcript.trim();
        if (!text) return;
        const url = new URL(window.parent.location.href);
        url.searchParams.set('di_voice', text);
        window.parent.location.href = url.toString();
      };
      rec.onerror = () => { setTimeout(() => { try { rec.start(); } catch(e) {} }, 900); };
      rec.onend = () => { setTimeout(() => { try { rec.start(); } catch(e) {} }, 700); };
      try { rec.start(); } catch(e) {}
    })();
    </script>
    """,height=0)

# Process a voice turn before rendering the page. This gives DI a real
# server-side answer instead of pretending the browser itself is the brain.
voice_turn = st.query_params.get("di_voice")
if voice_turn:
    st.query_params.clear()
    spoken = str(voice_turn).strip()
    if spoken:
        st.session_state.chat_history.append({"sender":user["first_name"],"text":spoken})
        reply=di_reply(spoken,user,st.session_state.processed_df,allow_online=True)
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        con=db(); now=datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],spoken,now))
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
        st.session_state.last_speech=reply
        st.rerun()

if selected_page=="DI Home":
    avatar_path = DI_AVATAR_PATH if DI_AVATAR_PATH.exists() else LOGO_PATH
    avatar_html = str(avatar_path).replace("\\", "/") if avatar_path.exists() else ""
    image_url = ONLINE_IMAGES["conversation"]

    st.markdown(f"""
    <div class="di-command">
      <div class="di-stage" style="background-image:url('{image_url}')">
        <div class="di-stage-overlay"></div>
        <div class="di-stage-copy">
          <div class="di-status"><span class="di-dot"></span> DI is online and ready</div>
          <div class="di-kicker" style="margin-top:18px">DACRE BUSINESS INTELLIGENCE</div>
          <h2>Talk to DI. Work with DI. Let DI move the work forward.</h2>
          <p>Ask a business question, upload a dataset, investigate a problem, build a presentation or request current information. DI can switch between your workspace and public online research when the task requires it.</p>
        </div>
        <div class="di-orb"></div>
      </div>
      <div class="di-transcript">
        <div class="di-transcript-label">Live DI conversation</div>
        <div class="di-transcript-text">{"Your conversation with DI will appear here. Speak naturally; Chrome will listen continuously while this page is open." if not st.session_state.chat_history else st.session_state.chat_history[-1]["text"]}</div>
      </div>
    </div>
    """,unsafe_allow_html=True)

    # Continuous voice starts automatically on supported Chromium browsers.
    di_voice_bridge()

    st.markdown("### Start with a business goal")
    q1,q2,q3,q4=st.columns(4)
    cards=[
      ("Investigate", "Find what is changing in my business", "Ask DI to inspect your active dataset and identify important patterns."),
      ("Analyse data", "Explain this dataset to me", "DI can inspect rows, columns, missing values, duplicates and numeric fields."),
      ("Research", "Find the latest information", "DI can attempt a public-web lookup for current topics and tell you that it used online sources."),
      ("Create", "Build something useful", "Ask DI to plan a report, chart, presentation, workflow or business action."),
    ]
    for col,(title,headline,desc) in zip([q1,q2,q3,q4],cards):
        with col:
            st.markdown(f"<div class='di-quick-card'><div style='font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:#b5487e!important;font-weight:800'>{title}</div><h4 style='margin:.45rem 0'>{headline}</h4><p style='color:#657180!important;font-size:.9rem;line-height:1.45'>{desc}</p></div>",unsafe_allow_html=True)

    if st.session_state.processed_df is not None:
        df=st.session_state.processed_df
        a,b,c,d=st.columns(4)
        metrics=[("Rows",f"{len(df):,}"),("Columns",f"{len(df.columns):,}"),("Duplicates",f"{int(df.duplicated().sum()):,}"),("Active file",st.session_state.active_filename or "Workspace")]
        for col,(label,value) in zip([a,b,c,d],metrics):
            with col: st.markdown(f"<div class='di-metric'><div class='v'>{value}</div><div class='l'>{label}</div></div>",unsafe_allow_html=True)

    st.markdown("### Conversation")
    for msg in st.session_state.chat_history[-12:]:
        who="DI" if msg["sender"]=="DI" else msg["sender"]
        st.markdown(f"<div style='background:{'#fff1f7' if who=='DI' else '#fff'};border:1px solid #f5d7e6;border-radius:14px;padding:13px 16px;margin:8px 0'><b>{who}</b><div style='margin-top:5px;line-height:1.55'>{msg['text']}</div></div>",unsafe_allow_html=True)

    with st.form("di_chat_form",clear_on_submit=True):
        chat_text=st.text_input("Ask DI",placeholder="Type here if you prefer text…",label_visibility="collapsed")
        send=st.form_submit_button("Send to DI",use_container_width=True)
    if send and chat_text.strip():
        st.session_state.chat_history.append({"sender":user["first_name"],"text":chat_text.strip()})
        reply=di_reply(chat_text,user,st.session_state.processed_df,allow_online=True)
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        con=db(); now=datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],chat_text.strip(),now))
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
        st.session_state.last_speech=reply
        st.rerun()

    st.caption("Voice mode uses your browser microphone and speech synthesis. If your browser does not expose continuous speech recognition, the text conversation remains available.")

# BUSINESS COMMAND CENTER — additive executive intelligence page
# =============================================================================
elif selected_page=="Business Command Center":
    st.header("Business Command Center")
    df=st.session_state.processed_df
    if df is None:
        st.info("Upload a dataset from Workspace & Data first. Then DACRE will turn the numbers into an executive business view.")
    else:
        h=business_health(df)
        st.markdown(f"<div class='dacre-user-hero'><div class='dacre-user-title'>Executive view</div><div class='dacre-user-sub'>DI has analysed the active workspace for {user['company']}. These signals are calculated from the data currently loaded — no invented business facts.</div></div>",unsafe_allow_html=True)
        k1,k2,k3,k4=st.columns(4)
        k1.metric("Business Data Health",f"{h['score']}/100")
        k2.metric("Records",f"{len(df):,}")
        k3.metric("Missing Cells",f"{int(df.isna().sum().sum()):,}")
        k4.metric("Duplicate Rows",f"{int(df.duplicated().sum()):,}")
        st.markdown("### DI Executive Brief")
        st.write(build_executive_brief(df,user["company"]))
        st.markdown("### Signals requiring attention")
        signals=business_signals(df)
        if not signals:
            st.success("No strong automated warning signals were detected in the current dataset.")
        else:
            for sig in signals:
                icon="📈" if sig["type"]=="trend" else "⚠️" if sig["type"]=="anomaly" else "🧹"
                st.markdown(f"**{icon} {sig['column']}** — {sig['message']}")
        st.markdown("### Ask the data")
        with st.form("command_center_form",clear_on_submit=True):
            q=st.text_input("Business question",placeholder="e.g. Give me an executive brief, show the top products, or check the data health")
            go=st.form_submit_button("Ask DI",use_container_width=True)
        if go and q.strip():
            answer=di_reply(q,user,df,allow_online=True)
            st.markdown(f"<div class='di-quick-card'><b>DI</b><div style='margin-top:8px;line-height:1.65'>{answer}</div></div>",unsafe_allow_html=True)
            st.session_state.last_speech=answer

# PAGE 1 WORKSPACE
# =============================================================================
elif selected_page=="Workspace & Data":
    st.header("Workspace & Data Engine")
    file_upload=st.file_uploader("Upload dataset (CSV, Excel, TSV, JSON)",type=SUPPORTED_EXTENSIONS)
    if file_upload is not None and st.button("Import & Load Dataset"):
        try:
            df_raw=load_dataframe(file_upload)
            st.session_state.raw_df=df_raw
            st.session_state.processed_df=clean_dataframe(df_raw)
            st.session_state.active_filename=file_upload.name
            save_file(user,file_upload,st.session_state.processed_df)
            save_project(user,st.session_state.raw_df,st.session_state.processed_df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
            st.success(f"Loaded '{file_upload.name}' successfully!")
            st.rerun()
        except Exception as exc: st.error(f"Could not load the dataset: {exc}")

    if st.session_state.processed_df is not None:
        df=st.session_state.processed_df
        st.subheader(f"Active File: {st.session_state.active_filename}")
        m1,m2,m3=st.columns(3)
        m1.metric("Total Rows",f"{len(df):,}")
        m2.metric("Total Columns",len(df.columns))
        m3.metric("Duplicates Removed",int(st.session_state.raw_df.duplicated().sum()) if st.session_state.raw_df is not None else 0)
        st.dataframe(df,use_container_width=True)
        if st.button("Save Project State to DI"):
            save_project(user,st.session_state.raw_df,df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
            log_activity(user["username"],user["company"],"Saved project state")
            st.toast("Project saved.")
    else: st.info("No active dataset. Upload a file or restore a saved project by signing in again.")

# =============================================================================
# PAGE 2 FORMULA LAB
# =============================================================================
elif selected_page=="Formula Lab":
    st.header("Formula Lab")
    df=st.session_state.processed_df
    if df is None: st.warning("Please upload or open a dataset first.")
    else:
        formula=st.selectbox("Formula Operation",SHEET_FORMULAS)
        cols=list(df.columns)
        if formula in ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","UPPER","LOWER","TRIM"]:
            target_col=st.selectbox("Target Column",cols)
            if st.button("Run Formula"):
                res=apply_formula(df,formula,{"column":target_col})
                if isinstance(res,tuple) and res[0]=="column":
                    df[res[1]]=res[2]; st.session_state.processed_df=df
                    st.session_state.formula_logs.append(f"Applied {formula} on {target_col}")
                    log_activity(user["username"],user["company"],f"Ran formula {formula} on {target_col}")
                    st.success(f"Applied {formula} on '{target_col}'!")
                else:
                    st.markdown(f"### Result: `{res}`")
                    st.session_state.formula_logs.append(f"{formula}({target_col}) = {res}")
        elif formula=="CONCATENATE":
            first=st.selectbox("First Column",cols); second=st.selectbox("Second Column",cols,index=min(1,len(cols)-1)); new_col=st.text_input("New Column Name",value="Combined"); sep=st.text_input("Separator",value=" ")
            if st.button("Run CONCATENATE"):
                df[new_col]=df[first].astype(str)+sep+df[second].astype(str); st.session_state.processed_df=df; log_activity(user["username"],user["company"],f"Created concatenated column {new_col}"); st.success(f"Created '{new_col}'.")

# =============================================================================
# PAGE 3 CHARTS
# =============================================================================
elif selected_page=="Charts":
    st.header("Add Dynamics — Chart Builder")
    df=st.session_state.processed_df
    if df is None: st.warning("Please upload or open a dataset first.")
    else:
        chart_type=st.selectbox("Chart Type",["Bar Chart","Line Chart","Area Chart"]); cols=list(df.columns); num_cols=df.select_dtypes(include=["number"]).columns.tolist(); x_col=st.selectbox("X-Axis (Category Column)",cols); y_col=st.selectbox("Y-Axis (Numeric Values)",num_cols if num_cols else cols)
        if st.button("Generate Dynamic Chart"):
            st.session_state.chart_config={"type":chart_type,"x":x_col,"y":y_col}; log_activity(user["username"],user["company"],f"Created {chart_type}: {x_col} vs {y_col}"); st.success("Chart attached to workspace!")
        if st.session_state.chart_config:
            cfg=st.session_state.chart_config; chart_data=df[[cfg["x"],cfg["y"]]].dropna().set_index(cfg["x"])
            if cfg["type"]=="Bar Chart": st.bar_chart(chart_data)
            elif cfg["type"]=="Line Chart": st.line_chart(chart_data)
            else: st.area_chart(chart_data)

# =============================================================================
# PAGE 4 FILE VAULT
# =============================================================================
elif selected_page=="File Vault":
    st.header("Organization File Vault")
    saved_files=get_files(user)
    if not saved_files: st.info("No files stored in vault for your organization.")
    else:
        for fname,ftype,created,fjson in saved_files:
            col_a,col_b=st.columns([3,1]); col_a.markdown(f"**{fname}** (`.{ftype}`) — Saved on: {created}")
            if col_b.button(f"Load '{fname}'",key=f"btn_{fname}_{created}"):
                restored_df=dataframe_from_json(fjson); st.session_state.processed_df=restored_df; st.session_state.raw_df=restored_df; st.session_state.active_filename=fname; log_activity(user["username"],user["company"],f"Loaded file from vault: {fname}"); st.success(f"Loaded {fname} from Vault!"); st.rerun()

# =============================================================================
# PAGE 5 EXPORT
# =============================================================================
elif selected_page=="Export Center":
    st.header("Export Center")
    df=st.session_state.processed_df
    if df is None: st.warning("No data available to export.")
    else:
        csv_data=df.to_csv(index=False).encode("utf-8"); excel_data=make_excel(df)
        st.download_button("Download CSV Dataset",data=csv_data,file_name=f"{st.session_state.active_filename or 'dacre'}_processed.csv",mime="text/csv")
        st.download_button("Download Excel Workbook (.xlsx)",data=excel_data,file_name=f"{st.session_state.active_filename or 'dacre'}_workbook.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        log_activity(user["username"],user["company"],"Opened Export Center")

# =============================================================================
# ORGANIZATION ADMIN PORTAL
# =============================================================================
elif selected_page=="Organization Admin Portal" and user["role"] in ("company_admin","master"):
    st.header("Organization Admin Portal")
    if user["role"]=="master":
        st.success("Master access confirmed. You can inspect all organizations.")
        target_company=st.selectbox("Organization",pd.read_sql_query("SELECT name FROM companies ORDER BY name",db())["name"].tolist())
    else:
        target_company=user["company"]
        st.success(f"Admin access confirmed for {target_company}.")

    con=db()
    tabs=st.tabs(["People & Accounts","Changes & Activity","DI Messages"])
    with tabs[0]:
        users_df=pd.read_sql_query("SELECT id,first_name,last_name,username,email,role,login_count,created_at,last_login FROM users WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(users_df,use_container_width=True)
        st.metric("Accounts in organization",len(users_df))

        if user["role"]=="company_admin":
            st.markdown("### Grant or remove admin access")
            usernames=users_df[users_df["role"]!="company_admin"]["username"].tolist()
            if usernames:
                selected_user=st.selectbox("User",usernames)
                action=st.selectbox("Action",["Grant company admin","Revoke company admin"])
                if st.button("Apply account role change"):
                    new_role="company_admin" if action.startswith("Grant") else "user"
                    con.execute("UPDATE users SET role=? WHERE username=? AND company_name=?",(new_role,selected_user,target_company)); con.commit()
                    notify_company_admin(target_company,f"Admin role changed for {selected_user}: {new_role}.","role_change")
                    log_activity(user["username"],target_company,f"Changed role for {selected_user} to {new_role}",notify_admin=False)
                    st.success("Role updated."); st.rerun()
    with tabs[1]:
        activity_df=pd.read_sql_query("SELECT id,username,action,created_at FROM activity WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(activity_df,use_container_width=True)
    with tabs[2]:
        notes_df=pd.read_sql_query("SELECT id,event_type,message,is_read,created_at FROM notifications WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(notes_df,use_container_width=True)
        if not notes_df.empty and st.button("Mark DI messages as read"):
            con.execute("UPDATE notifications SET is_read=1 WHERE company_name=?",(target_company,)); con.commit(); st.rerun()
    con.close()

# =============================================================================
# MASTER ADMIN PORTAL / CEO OFFICE
# =============================================================================
elif selected_page=="Overall Admin DI Portal" and user["role"]=="master":
    counts=admin_metric_counts()
    st.markdown("""
    <div class="dacre-hero">
      <div class="dacre-title" style="font-size:3rem;">CEO Office</div>
      <div class="dacre-sub">DACRE Analysis executive command centre · Overall Administration · DI Workforce</div>
      <div style="margin-top:14px;color:#9edcff;font-weight:700;">Master: David Emenike · System authority: Overall Administrator</div>
    </div>
    """,unsafe_allow_html=True)

    m1,m2,m3,m4,m5,m6=st.columns(6)
    m1.metric("Business Accounts",counts["users"])
    m2.metric("Organizations",counts["companies"])
    m3.metric("Activities",counts["activities"])
    m4.metric("DI Conversations",counts["messages"])
    m5.metric("Stored Files",counts["files"])
    m6.metric("DI Workforce",counts["agents"])

    con=db()
    tabs=st.tabs(["Executive Overview","DI Workforce","Organizations","People & Accounts","Live Activity","DI Conversations","Mail Source","System Controls"])

    with tabs[0]:
        st.subheader("Executive Overview")
        recent= pd.read_sql_query("SELECT username,company_name,action,created_at FROM activity ORDER BY id DESC LIMIT 15",con)
        left,right=st.columns([1.25,1])
        with left:
            st.markdown("#### Recent system activity")
            st.dataframe(recent,use_container_width=True,hide_index=True)
        with right:
            st.markdown("#### Platform position")
            st.write("The CEO Office is the highest DACRE administration layer. This is where master-level oversight, DI workforce creation, organization visibility and platform activity are managed.")
            st.write("All normal company users remain isolated inside their own organization workspaces.")
            if st.button("Refresh executive view",use_container_width=True):
                st.rerun()

    with tabs[1]:
        st.subheader("DI Workforce Command")
        st.write("Create and manage the DI workers that DACRE can make available to organizations. Each DI has a name, code, specialty, status and assignment record.")
        create_left,create_right=st.columns([1,1])
        with create_left:
            di_name=st.text_input("DI Name",placeholder="e.g. DI Finance")
            di_specialty=st.text_input("Specialty",placeholder="e.g. Financial analysis and forecasting")
            di_role=st.text_area("DI System Role",placeholder="Describe how this DI should serve businesses.",height=100)
        with create_right:
            companies=[r[0] for r in con.execute("SELECT name FROM companies ORDER BY name").fetchall()]
            di_status=st.selectbox("Initial Status",["Available","Assigned","Training","Paused"])
            di_company=st.selectbox("Assign to Organization",["Unassigned"]+companies)
            if st.button("Create DI Worker",use_container_width=True,type="primary"):
                ok,msg=create_di_agent(di_name,di_specialty,di_status,"" if di_company=="Unassigned" else di_company,di_role)
                if ok:
                    log_activity(MASTER_USERNAME,"DACRE MASTER",f"Created DI worker {di_name} ({msg})",notify_admin=False)
                    st.success(f"DI created successfully. Worker code: {msg}")
                    st.rerun()
                else: st.error(msg)
        agents=get_di_agents()
        if agents:
            st.markdown("#### Available DI workers")
            agent_df=pd.DataFrame([dict(r) for r in agents])
            st.dataframe(agent_df,use_container_width=True,hide_index=True)
            selected_id=st.selectbox("Select DI worker",[r["id"] for r in agents],format_func=lambda x: next((r["di_name"] for r in agents if r["id"]==x),str(x)))
            selected_agent=next(r for r in agents if r["id"]==selected_id)
            e1,e2=st.columns(2)
            with e1:
                new_status=st.selectbox("Change status",["Available","Assigned","Training","Paused"],index=["Available","Assigned","Training","Paused"].index(selected_agent["status"]))
            with e2:
                company_options=["Unassigned"]+companies
                current_company=selected_agent["assigned_company"] or "Unassigned"
                new_company=st.selectbox("Change assignment",company_options,index=company_options.index(current_company) if current_company in company_options else 0)
            if st.button("Update DI Worker",use_container_width=True):
                update_di_agent(selected_id,new_status,"" if new_company=="Unassigned" else new_company)
                log_activity(MASTER_USERNAME,"DACRE MASTER",f"Updated DI worker {selected_agent['di_name']}",notify_admin=False)
                st.success("DI worker updated."); st.rerun()
        else:
            st.info("No DI workers have been created yet. This is the command centre where you create them.")

    with tabs[2]:
        st.subheader("All Organizations")
        companies_df=pd.read_sql_query("SELECT id,name,owner_username,created_at FROM companies ORDER BY id DESC",con)
        st.dataframe(companies_df,use_container_width=True,hide_index=True)
        st.metric("Organizations",len(companies_df))

    with tabs[3]:
        st.subheader("All People & Accounts")
        users_df=pd.read_sql_query("SELECT id,first_name,last_name,username,company_name,email,role,login_count,created_at,last_login FROM users ORDER BY id DESC",con)
        st.dataframe(users_df,use_container_width=True,hide_index=True)
        st.metric("Registered accounts excluding master",len(users_df[users_df["role"]!="master"]))

    with tabs[4]:
        st.subheader("System Activity")
        activity_df=pd.read_sql_query("SELECT id,username,company_name,action,created_at FROM activity ORDER BY id DESC",con)
        st.dataframe(activity_df,use_container_width=True,hide_index=True)

    with tabs[5]:
        st.subheader("DI Conversations Across DACRE")
        chat_df=pd.read_sql_query("SELECT id,username,company_name,sender,message,created_at FROM chat_history ORDER BY id DESC",con)
        st.dataframe(chat_df,use_container_width=True,hide_index=True)
        st.caption("This view gives the master administration layer system-wide visibility into DI conversations. It is not shown to ordinary users.")

    with tabs[6]:
        st.subheader("DI Mail Source")
        mails_df=pd.read_sql_query("SELECT id,recipient_name,recipient_email,company_name,subject,sender_email,status,sent_at,body FROM emails_log ORDER BY id DESC",con)
        st.dataframe(mails_df,use_container_width=True,hide_index=True)

    with tabs[7]:
        st.subheader("System Controls")
        st.write("Master-level controls are deliberately separated from normal company administration.")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**Master identity**")
            st.write("David Emenike")
            st.write("Overall Administrator")
            st.write("DACRE MASTER")
        with c2:
            st.markdown("**Security**")
            st.write("The master passkey is checked server-side against its hash. It is not displayed in the CEO Office.")
            if st.button("Lock CEO Office",use_container_width=True):
                st.session_state.user=None
                st.session_state.master_route=False
                st.query_params.clear()
                st.rerun()
    con.close()

# =============================================================================
# PERSISTENT DI DOCK
# =============================================================================

st.markdown("---")
with st.expander("Chat with DI — quick assistant",expanded=False):
    for msg in st.session_state.chat_history[-10:]: st.write(f"**{msg['sender']}**: {msg['text']}")
    with st.form("quick_di_form",clear_on_submit=True):
        q=st.text_input("Chat with DI",placeholder="Chat with DI — ask a question...",label_visibility="collapsed")
        send=st.form_submit_button("Send")
    if send and q.strip():
        st.session_state.chat_history.append({"sender":user["first_name"],"text":q.strip()})
        reply=di_reply(q,user,st.session_state.processed_df,allow_online=True)
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        st.session_state.last_speech=reply
        st.rerun()

if st.session_state.last_speech:
    speech=st.session_state.last_speech
    st.session_state.last_speech=None
    speak(speech)
