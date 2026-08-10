
import hashlib
import hmac
import io
import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =============================================================================
# DACRE ANALYSIS ENGINE
# DI = DAVID'S INTELLIGENCE
# Unified foundation + upgraded features
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"

# Master secret MUST come from deployment secrets/environment.
# No production fallback is embedded in source code.
def get_master_passkey():
    env_value = os.getenv("DACRE_MASTER_PASSKEY")
    if env_value:
        return env_value
    try:
        secret_value = st.secrets.get("DACRE_MASTER_PASSKEY")
        if secret_value:
            return str(secret_value)
    except Exception:
        pass
    return ""


MASTER_PASSKEY = get_master_passkey()

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"


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
        left = max(0, (crop.width - side) // 2)
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
# VISUAL SYSTEM
# =============================================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(24,183,255,.10), transparent 25%),
            radial-gradient(circle at 90% 15%, rgba(255,193,7,.08), transparent 22%),
            linear-gradient(135deg, #050914, #091322 55%, #050914);
        color: #eef6ff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07101d, #050914);
        border-right: 1px solid rgba(24,183,255,.20);
    }

    .dacre-hero {
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(24,183,255,.35);
        background: linear-gradient(135deg, rgba(6,16,31,.96), rgba(10,28,47,.88));
        box-shadow: 0 0 35px rgba(24,183,255,.08);
    }

    .gold-card {
        padding: 24px;
        border-radius: 22px;
        border: 1px solid rgba(255,193,7,.55);
        background: linear-gradient(145deg, #030303, #16120a);
        box-shadow: 0 0 35px rgba(255,193,7,.10);
    }

    .metric-card {
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,.10);
        background: rgba(255,255,255,.035);
    }

    .badge {
        display: inline-block;
        padding: 5px 11px;
        margin: 3px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.14);
        background: rgba(255,255,255,.05);
        font-size: .80rem;
    }

    .chat-dock {
        position: fixed;
        left: 20px;
        right: 20px;
        bottom: 10px;
        z-index: 9999;
        padding: 10px 15px;
        border-radius: 16px;
        background: rgba(5,10,19,.96);
        border: 1px solid rgba(24,183,255,.45);
        box-shadow: 0 10px 35px rgba(0,0,0,.35);
    }

    .small-muted {
        color: #9db0c5;
        font-size: .88rem;
    }

    .success-glow {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid rgba(0,220,150,.35);
        background: rgba(0,220,150,.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_logo(width=210):
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=width)


# =============================================================================
# DATABASE
# =============================================================================

PBKDF2_ITERATIONS = 600_000
PBKDF2_ALGORITHM = "sha256"


def db():
    con = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    con.execute("PRAGMA busy_timeout = 30000")
    return con


def hash_password(value):
    """Create a salted, CPU-hard password hash."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        str(value).encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(value, stored_hash):
    """Verify modern PBKDF2 hashes and transparently accept legacy SHA-256 hashes once."""
    if not stored_hash:
        return False, False

    if stored_hash.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_hex, digest_hex = stored_hash.split("$", 3)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac(
                "sha256",
                str(value).encode("utf-8"),
                salt,
                int(iterations),
            )
            return hmac.compare_digest(actual, expected), False
        except (ValueError, TypeError):
            return False, False

    # Legacy SHA-256 migration path. A successful login is immediately upgraded.
    legacy = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    if hmac.compare_digest(legacy, stored_hash):
        return True, True
    return False, False


def valid_password(value):
    value = str(value or "")
    return (
        len(value) >= 10
        and bool(re.search(r"[A-Z]", value))
        and bool(re.search(r"[a-z]", value))
        and bool(re.search(r"\d", value))
    )


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

    con.commit()
    con.close()


def ensure_master():
    if not MASTER_PASSKEY:
        return
    con = db()
    cur = con.cursor()
    row = cur.execute(
        "SELECT id FROM users WHERE username = ?", (MASTER_USERNAME,)
    ).fetchone()

    if not row:
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute("""
            INSERT INTO users (
                first_name, last_name, username, company_name, email,
                password_hash, passkey_hash, role, login_count, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "David",
            "Emenike",
            MASTER_USERNAME,
            "DACRE MASTER",
            "master@dacre.local",
            hash_password(MASTER_PASSKEY),
            hash_password(MASTER_PASSKEY),
            "master",
            0,
            now,
        ))
        con.commit()
    con.close()


init_db()
ensure_master()


def log_activity(username, company, action):
    con = db()
    con.execute("""
        INSERT INTO activity(username, company_name, action, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        username, company, action,
        datetime.now().isoformat(timespec="seconds"),
    ))
    con.commit()
    con.close()


# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate(username, password, passkey):
    username = str(username).strip().lower()

    con = db()
    row = con.execute("""
        SELECT first_name, last_name, username, company_name, email,
               password_hash, passkey_hash, role
        FROM users
        WHERE lower(username) = lower(?)
    """, (username,)).fetchone()

    if not row:
        con.close()
        return None

    password_ok, password_legacy = verify_password(password, row[5])
    passkey_ok, passkey_legacy = verify_password(passkey, row[6])

    if not password_ok or not passkey_ok:
        con.close()
        return None

    now = datetime.now().isoformat(timespec="seconds")
    if password_legacy or passkey_legacy:
        con.execute("""
            UPDATE users
            SET password_hash = ?, passkey_hash = ?
            WHERE username = ?
        """, (
            hash_password(password),
            hash_password(passkey),
            row[2],
        ))

    con.execute("""
        UPDATE users
        SET login_count = login_count + 1, last_login = ?
        WHERE username = ?
    """, (now, row[2]))
    con.commit()
    con.close()

    log_activity(row[2], row[3], "Signed in")

    return {
        "first_name": row[0],
        "last_name": row[1],
        "username": row[2],
        "company": row[3],
        "email": row[4],
        "role": row[7],
    }


def create_account(first, last, username, company, email, password, passkey):
    values = [first, last, username, company, email, password, passkey]
    if not all(str(v).strip() for v in values):
        return False, "Please complete every required field."

    username_clean = username.strip().lower()
    company_clean = company.strip()
    email_clean = email.strip().lower()

    if username_clean == MASTER_USERNAME:
        return False, "That username is reserved for Master David."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email_clean):
        return False, "Please enter a valid email address."

    if not valid_password(password):
        return False, "Password must be at least 10 characters and include uppercase, lowercase, and a number."

    if len(passkey.strip()) < 8:
        return False, "Account Passkey must contain at least 8 characters."

    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()

        company_row = cur.execute(
            "SELECT id FROM companies WHERE lower(name) = lower(?)",
            (company_clean,),
        ).fetchone()

        if not company_row:
            cur.execute("""
                INSERT INTO companies
                (name, owner_username, admin_password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                company_clean,
                username_clean,
                hash_password(passkey),
                now,
            ))

        cur.execute("""
            INSERT INTO users
            (first_name, last_name, username, company_name, email,
             password_hash, passkey_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first.strip(),
            last.strip(),
            username_clean,
            company_clean,
            email_clean,
            hash_password(password),
            hash_password(passkey),
            "company_admin",
            now,
        ))

        con.commit()
        log_activity(username_clean, company_clean, "Created company account")
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username or email is already registered."
    finally:
        con.close()


def create_company_user(first, last, username, email, password, passkey, company):
    values = [first, last, username, email, password, passkey, company]
    if not all(str(v).strip() for v in values):
        return False, "Complete every field."

    username = username.strip().lower()
    email = email.strip().lower()

    if username == MASTER_USERNAME:
        return False, "That username is reserved."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."
    if not valid_password(password):
        return False, "Password must be at least 10 characters and include uppercase, lowercase, and a number."
    if len(passkey) < 8:
        return False, "Passkey must contain at least 8 characters."

    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        con.execute("""
            INSERT INTO users
            (first_name, last_name, username, company_name, email,
             password_hash, passkey_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first.strip(), last.strip(), username, company, email,
            hash_password(password), hash_password(passkey), "user", now
        ))
        con.commit()
        log_activity(
            username,
            company,
            f"User account created by company admin"
        )
        return True, "Company user created."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."
    finally:
        con.close()


# =============================================================================
# DATA ENGINE
# =============================================================================

def load_dataframe(uploaded_file):
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()

    if ext == "csv":
        return pd.read_csv(uploaded_file)
    if ext == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if ext in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file)
    if ext == "json":
        return pd.read_json(uploaded_file)

    raise ValueError(f"Unsupported file type: .{ext}")


def clean_dataframe(df):
    out = df.copy()

    out.columns = [
        re.sub(r"\s+", " ", str(col).strip()) if str(col).strip()
        else f"Column_{i + 1}"
        for i, col in enumerate(out.columns)
    ]

    out = out.dropna(axis=0, how="all").dropna(axis=1, how="all")

    for col in out.columns:
        if out[col].dtype == "object":
            series = out[col].astype(str).replace({"nan": ""}).str.strip()
            numeric_candidate = (
                series
                .str.replace(r"[\$€£₦,%]", "", regex=True)
                .str.replace(",", "", regex=False)
            )
            numeric = pd.to_numeric(numeric_candidate, errors="coerce")

            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[col] = numeric
            else:
                out[col] = series

    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    if df is None:
        return ""
    return df.to_json(orient="split", date_format="iso")


def dataframe_from_json(value):
    if not value:
        return None
    try:
        return pd.read_json(io.StringIO(value), orient="split")
    except Exception:
        return None


def data_profile(df):
    if df is None:
        return None

    rows = len(df)
    cols = len(df.columns)
    duplicates = int(df.duplicated().sum())
    missing = int(df.isna().sum().sum())
    numeric_cols = len(df.select_dtypes(include="number").columns)

    return {
        "Rows": rows,
        "Columns": cols,
        "Duplicates": duplicates,
        "Missing Cells": missing,
        "Numeric Columns": numeric_cols,
        "Memory (KB)": round(df.memory_usage(deep=True).sum() / 1024, 1),
    }


def save_file(user, uploaded_file, df):
    con = db()
    con.execute("""
        INSERT INTO files
        (username, company_name, filename, file_type, file_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user["username"],
        user["company"],
        uploaded_file.name,
        uploaded_file.name.rsplit(".", 1)[-1].lower(),
        dataframe_to_json(df),
        datetime.now().isoformat(timespec="seconds"),
    ))
    con.commit()
    con.close()

    log_activity(
        user["username"],
        user["company"],
        f"Saved file: {uploaded_file.name}"
    )


def get_files(user):
    con = db()
    if user["role"] in ("company_admin", "master"):
        rows = con.execute("""
            SELECT id, filename, file_type, created_at, file_json
            FROM files
            WHERE company_name = ?
            ORDER BY id DESC
        """, (user["company"],)).fetchall()
    else:
        rows = con.execute("""
            SELECT id, filename, file_type, created_at, file_json
            FROM files
            WHERE company_name = ? AND username = ?
            ORDER BY id DESC
        """, (user["company"], user["username"])).fetchall()
    con.close()
    return rows


def delete_file(file_id, user):
    con = db()
    if user["role"] in ("company_admin", "master"):
        con.execute(
            "DELETE FROM files WHERE id = ? AND company_name = ?",
            (file_id, user["company"]),
        )
    else:
        con.execute(
            "DELETE FROM files WHERE id = ? AND company_name = ? AND username = ?",
            (file_id, user["company"], user["username"]),
        )
    con.commit()
    con.close()
    log_activity(
        user["username"],
        user["company"],
        f"Deleted vault file ID {file_id}"
    )


def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    con = db()

    existing = con.execute("""
        SELECT id FROM projects
        WHERE username = ? AND company_name = ?
        ORDER BY id DESC LIMIT 1
    """, (user["username"], user["company"])).fetchone()

    payload = (
        user["username"],
        user["company"],
        "Main Workspace",
        filename or "",
        dataframe_to_json(raw_df),
        dataframe_to_json(processed_df),
        json.dumps(logs),
        json.dumps(chart_config or {}),
        datetime.now().isoformat(timespec="seconds"),
    )

    if existing:
        con.execute("""
            UPDATE projects
            SET project_name = ?, active_filename = ?, raw_json = ?,
                processed_json = ?, formula_logs = ?, chart_config = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            payload[2], payload[3], payload[4], payload[5],
            payload[6], payload[7], payload[8], existing[0]
        ))
    else:
        con.execute("""
            INSERT INTO projects
            (username, company_name, project_name, active_filename,
             raw_json, processed_json, formula_logs, chart_config, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, payload)

    con.commit()
    con.close()


def restore_project(user):
    con = db()
    row = con.execute("""
        SELECT active_filename, raw_json, processed_json,
               formula_logs, chart_config
        FROM projects
        WHERE username = ? AND company_name = ?
        ORDER BY id DESC LIMIT 1
    """, (user["username"], user["company"])).fetchone()
    con.close()

    if not row:
        return None

    try:
        logs = json.loads(row[3]) if row[3] else []
    except Exception:
        logs = []

    try:
        chart = json.loads(row[4]) if row[4] else {}
    except Exception:
        chart = {}

    return {
        "filename": row[0],
        "raw": dataframe_from_json(row[1]),
        "processed": dataframe_from_json(row[2]),
        "logs": logs,
        "chart": chart,
    }


# =============================================================================
# FORMULA ENGINE
# =============================================================================

SHEET_FORMULAS = [
    "SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN",
    "CONCATENATE", "UPPER", "LOWER", "TRIM"
]


def apply_formula(df, formula, options):
    formula = formula.upper()
    col = options.get("column")

    if formula == "SUM":
        return pd.to_numeric(df[col], errors="coerce").sum()

    if formula == "AVERAGE":
        return pd.to_numeric(df[col], errors="coerce").mean()

    if formula == "COUNT":
        return int(pd.to_numeric(df[col], errors="coerce").count())

    if formula == "COUNTA":
        return int(df[col].notna().sum())

    if formula == "MAX":
        return pd.to_numeric(df[col], errors="coerce").max()

    if formula == "MIN":
        return pd.to_numeric(df[col], errors="coerce").min()

    if formula == "CONCATENATE":
        first = options["first"]
        second = options["second"]
        separator = options.get("separator", " ")
        new_col = options["new_column"]

        result = (
            df[first].fillna("").astype(str)
            + separator
            + df[second].fillna("").astype(str)
        )
        return ("column", new_col, result)

    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[col].fillna("").astype(str)
        if formula == "UPPER":
            result = series.str.upper()
        elif formula == "LOWER":
            result = series.str.lower()
        else:
            result = series.str.strip()
        return ("column", col, result)

    return None


# =============================================================================
# SQL ENGINE
# =============================================================================

def run_sql_query(df, query):
    """
    Executes a read-only SQL query against a temporary SQLite table called dataset.
    This supports normal SELECT / WHERE / GROUP BY / ORDER BY / LIMIT queries.
    """
    if df is None:
        raise ValueError("No active dataset.")

    query_clean = query.strip().rstrip(";")
    if not re.match(r"(?is)^\s*select\b", query_clean):
        raise ValueError("Only SELECT queries are allowed in the SQL Lab.")

    con = sqlite3.connect(":memory:")
    try:
        safe_df = df.copy()
        safe_df.to_sql("dataset", con, index=False, if_exists="replace")
        result = pd.read_sql_query(query_clean, con)
        return result
    finally:
        con.close()


# =============================================================================
# EXCEL EXPORT WITH REAL OPENPYXL CHART
# =============================================================================

def make_excel(processed_df, chart_df=None, chart_type="Bar Chart",
               x_col=None, y_col=None):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(
            writer, sheet_name="Processed Data", index=False
        )

        if chart_df is not None:
            chart_df.to_excel(
                writer, sheet_name="Dynamic Chart Data", index=False
            )

            workbook = writer.book
            chart_sheet = workbook.create_sheet("Dynamic Chart")

            try:
                from openpyxl.chart import BarChart, LineChart, PieChart, AreaChart
                from openpyxl.chart.label import DataLabelList
                from openpyxl.utils import get_column_letter

                chart_data_sheet = workbook["Dynamic Chart Data"]

                if not x_col or not y_col:
                    raise ValueError("Chart columns are not configured.")

                x_idx = list(chart_df.columns).index(x_col) + 1
                y_idx = list(chart_df.columns).index(y_col) + 1
                max_row = len(chart_df) + 1

                if chart_type == "Pie Chart":
                    chart = PieChart()
                    labels = openpyxl_ref(
                        chart_data_sheet, x_idx, 2, max_row
                    )
                    data = openpyxl_ref(
                        chart_data_sheet, y_idx, 1, max_row
                    )
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(labels)
                    chart.title = f"{y_col} by {x_col}"
                    chart.dataLabels = DataLabelList()
                    chart.dataLabels.showPercent = True
                else:
                    if chart_type == "Line Chart":
                        chart = LineChart()
                    elif chart_type == "Area Chart":
                        chart = AreaChart()
                    else:
                        chart = BarChart()
                        chart.type = "col"

                    data = openpyxl_ref(
                        chart_data_sheet, y_idx, 1, max_row
                    )
                    cats = openpyxl_ref(
                        chart_data_sheet, x_idx, 2, max_row
                    )
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(cats)
                    chart.title = f"{y_col} by {x_col}"
                    chart.y_axis.title = y_col
                    chart.x_axis.title = x_col

                chart_sheet.add_chart(chart, "B2")
            except Exception:
                # Keep export usable even if chart construction fails.
                chart_sheet["A1"] = "Dynamic chart could not be embedded."
                chart_sheet["A2"] = "Use the Dynamic Chart Data sheet."

    output.seek(0)
    return output.getvalue()


def openpyxl_ref(ws, col_idx, min_row, max_row):
    from openpyxl.chart.reference import Reference
    return Reference(
        ws,
        min_col=col_idx,
        max_col=col_idx,
        min_row=min_row,
        max_row=max_row,
    )


# =============================================================================
# DI ASSISTANT
# =============================================================================

LANGUAGES = {
    "English": "en-NG",
    "Nigerian Pidgin": "en-NG",
    "Yoruba": "yo-NG",
    "Igbo": "ig-NG",
    "Hausa": "ha-NG",
    "French": "fr-FR",
    "German": "de-DE",
    "Chinese": "zh-CN",
    "Hindi": "hi-IN",
    "Russian": "ru-RU",
}


def di_reply(message, user, df):
    text = message.strip()
    low = text.lower()

    if not text:
        return "I am ready. Tell me what you want me to do."

    name = (
        "Master David"
        if user["role"] == "master"
        else user["first_name"]
    )

    profile = data_profile(df) if df is not None else None

    if any(x in low for x in [
        "hello", "hi", "good morning",
        "good afternoon", "good day"
    ]):
        return (
            f"Good day {name}. DI is online and ready to work "
            "with your data."
        )

    if "row count" in low or "how many rows" in low:
        return (
            "No active dataset."
            if df is None
            else f"The active dataset contains {len(df):,} rows."
        )

    if "column count" in low or "how many columns" in low:
        return (
            "No active dataset."
            if df is None
            else f"The active dataset contains {len(df.columns):,} columns."
        )

    if "profile" in low or "summary" in low:
        if not profile:
            return "There is no active dataset to profile."
        return (
            f"Dataset profile: {profile['Rows']:,} rows, "
            f"{profile['Columns']:,} columns, "
            f"{profile['Duplicates']:,} duplicate rows, "
            f"{profile['Missing Cells']:,} missing cells."
        )

    if "clean" in low:
        return (
            "Use Process & Clean Data. I will standardize headers, "
            "remove empty rows/columns, normalize numeric-looking values, "
            "and remove duplicate rows."
        )

    if "master" in low and user["role"] == "master":
        return (
            "With all due respect, Master David, the sovereign DI portal "
            "is available to you."
        )

    if "export" in low:
        return "Open Export Center to download the current processed workbook."

    if user["role"] == "master":
        return (
            f"With all due respect, Master David, I received: "
            f"'{text}'. The request is recorded in the DI session."
        )

    return f"DI received your request: '{text}'."


def speak(text, language="en-NG"):
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language)

    components.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance({safe_text});
        message.rate = 0.95;
        message.pitch = 0.82;
        message.lang = {safe_lang};
        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        }}
        </script>
        """,
        height=0,
    )


# =============================================================================
# SESSION STATE
# =============================================================================

defaults = {
    "user": None,
    "page": "Workspace",
    "raw_df": None,
    "df": None,
    "active_filename": "",
    "formula_logs": [],
    "chart_config": {},
    "chat": [],
    "auth_mode": "Sign In",
    "language": "English",
    "last_clean_report": None,
    "last_sql_result": None,
    "last_upload_signature": None,
    "failed_login_attempts": 0,
    "locked_until": None,
    "presentation_running": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def set_user(user):
    st.session_state.user = user
    restored = restore_project(user)

    st.session_state.raw_df = restored["raw"] if restored else None
    st.session_state.df = restored["processed"] if restored else None
    st.session_state.active_filename = (
        restored["filename"] if restored else ""
    )
    st.session_state.formula_logs = (
        restored["logs"] if restored else []
    )
    st.session_state.chart_config = (
        restored["chart"] if restored else {}
    )
    st.session_state.chat = []
    st.session_state.page = "Workspace"


# =============================================================================
# PUBLIC LANDING + AUTH
# =============================================================================

if not st.session_state.user:
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        show_logo(240)

        st.markdown(
            """
            <div class="dacre-hero">
                <h1>DACRE Analysis</h1>
                <p style="font-size:1.05rem;">
                    Data today. Smarter tomorrows.
                    Powered by DI — David's Intelligence.
                </p>
                <span class="badge">DATA CLEANING</span>
                <span class="badge">FORMULAS</span>
                <span class="badge">SQL</span>
                <span class="badge">DYNAMICS</span>
                <span class="badge">EXPORT</span>
                <span class="badge">FILE VAULT</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.info(
            "DACRE turns business data into a structured workspace: "
            "upload → clean → analyze → visualize → export."
        )

        if not MASTER_PASSKEY:
            st.warning(
                "Master account is not initialized because DACRE_MASTER_PASSKEY "
                "is not configured. Set it in your environment or Streamlit Secrets "
                "before using the Master DI Portal."
            )

        st.session_state.auth_mode = st.radio(
            "Portal",
            ["Sign In", "Sign Up"],
            horizontal=True,
        )

        if st.session_state.auth_mode == "Sign In":
            st.subheader("🔐 Sign In")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            passkey = st.text_input("Account Passkey", type="password")

            if st.button(
                "Enter DACRE",
                use_container_width=True,
                type="primary",
            ):
                from time import time as _time
                locked_until = st.session_state.get("locked_until")
                if locked_until and _time() < locked_until:
                    remaining = int(locked_until - _time()) + 1
                    st.error(f"Too many failed attempts. Try again in {remaining} seconds.")
                    st.stop()

                user = authenticate(username, password, passkey)

                if user:
                    st.session_state.failed_login_attempts = 0
                    st.session_state.locked_until = None
                    set_user(user)
                    if user["role"] == "master":
                        st.toast("Good day Master David")
                    else:
                        st.toast(
                            f"Welcome {user['first_name']} "
                            f"to {user['company']}"
                        )
                    st.rerun()
                else:
                    st.session_state.failed_login_attempts += 1
                    if st.session_state.failed_login_attempts >= 5:
                        st.session_state.locked_until = __import__("time").time() + 60
                        st.error("Too many failed attempts. Sign-in is temporarily locked for 60 seconds.")
                    else:
                        left = 5 - st.session_state.failed_login_attempts
                        st.error(f"Invalid credentials or security passkey. {left} attempt(s) remaining.")

        else:
            st.subheader("🏢 Register Business Account")

            col_a, col_b = st.columns(2)

            with col_a:
                first = st.text_input("First Name")
                username = st.text_input("Username")
                company = st.text_input("Company / Business Name")
                email = st.text_input("Email Address")

            with col_b:
                last = st.text_input("Last Name")
                password = st.text_input(
                    "Password",
                    type="password",
                )
                passkey = st.text_input(
                    "Account Passkey",
                    type="password",
                )

            if st.button(
                "Create DACRE Account",
                use_container_width=True,
                type="primary",
            ):
                ok, msg = create_account(
                    first, last, username, company,
                    email, password, passkey
                )

                if ok:
                    st.success(msg)
                    user = authenticate(
                        username, password, passkey
                    )
                    if user:
                        set_user(user)
                        st.rerun()
                else:
                    st.error(msg)

    st.stop()


# =============================================================================
# AUTHENTICATED SHELL
# =============================================================================

user = st.session_state.user
is_master = user["role"] == "master"

with st.sidebar:
    show_logo(180)

    st.markdown(f"### {DI_NAME}")
    st.caption(
        f"Signed in: **{user['first_name']} {user['last_name']}**"
    )
    st.caption(f"Company: **{user['company']}**")
    st.caption(f"Role: **{user['role'].replace('_', ' ').title()}**")

    st.divider()

    language = st.selectbox(
        "🗣️ DI Voice Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(
            st.session_state.language
        ),
    )
    st.session_state.language = language

    st.divider()

    nav_items = [
        "Workspace",
        "File Vault",
        "Formula Lab",
        "SQL Lab",
        "ADD DYNAMICS",
        "Data Insights",
        "Presentation Engine",
        "Export Center",
        "Company Admin",
    ]

    if is_master:
        nav_items.append("Master DI Portal")

    nav = st.radio("Navigation", nav_items)

    st.divider()

    if st.button("🚪 Sign Out", use_container_width=True):
        log_activity(
            user["username"],
            user["company"],
            "Signed out"
        )
        st.session_state.user = None
        st.session_state.page = "Workspace"
        st.rerun()


df = st.session_state.df


# =============================================================================
# WORKSPACE
# =============================================================================

if nav == "Workspace":
    st.title("📂 Workspace & Intelligent Data Processing")

    st.markdown(
        """
        <div class="dacre-hero">
            <h2>Clean → Build → Analyze</h2>
            <p>
                Your active project is automatically restored from the
                DACRE SQLite vault when you sign back in.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    upload = st.file_uploader(
        "Collect Data File",
        type=["csv", "xlsx", "xls", "tsv", "json"],
        help="Supported: CSV, XLSX, XLS, TSV and JSON.",
    )

    if upload is not None:
        try:
            upload_bytes = upload.getvalue()
            upload_signature = hashlib.sha256(upload_bytes).hexdigest()

            # Streamlit reruns the script after every interaction while the
            # uploader remains populated. Only persist a file once per content.
            if upload_signature != st.session_state.last_upload_signature:
                raw = load_dataframe(upload)

                st.session_state.raw_df = raw.copy()
                st.session_state.df = raw.copy()
                st.session_state.active_filename = upload.name
                st.session_state.last_upload_signature = upload_signature

                save_file(user, upload, raw)
                save_project(
                    user, raw, raw, upload.name,
                    st.session_state.formula_logs,
                    st.session_state.chart_config,
                )

                log_activity(
                    user["username"],
                    user["company"],
                    f"Loaded active dataset: {upload.name}"
                )

                st.success(
                    f"'{upload.name}' is now the active DACRE dataset."
                )
                st.rerun()

        except Exception as exc:
            st.error(f"Could not load file: {exc}")

    if df is None:
        st.info(
            "No active dataset. Upload a file above or load one "
            "from File Vault."
        )
    else:
        profile = data_profile(df)

        st.markdown("### ⚡ Dataset Command Center")

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Rows", f"{profile['Rows']:,}")
        m2.metric("Columns", f"{profile['Columns']:,}")
        m3.metric("Duplicates", f"{profile['Duplicates']:,}")
        m4.metric("Missing Cells", f"{profile['Missing Cells']:,}")
        m5.metric("Numeric Columns", f"{profile['Numeric Columns']:,}")

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(
                "✨ Process & Clean Data",
                use_container_width=True,
                type="primary",
            ):
                before_rows = len(df)
                before_dupes = int(df.duplicated().sum())

                cleaned = clean_dataframe(df)

                st.session_state.df = cleaned

                report = {
                    "Rows Before": before_rows,
                    "Rows After": len(cleaned),
                    "Duplicates Removed": before_dupes,
                    "Missing Cells After": int(
                        cleaned.isna().sum().sum()
                    ),
                }

                st.session_state.last_clean_report = report

                save_project(
                    user,
                    st.session_state.raw_df,
                    cleaned,
                    st.session_state.active_filename,
                    st.session_state.formula_logs,
                    st.session_state.chart_config,
                )

                log_activity(
                    user["username"],
                    user["company"],
                    "Processed and cleaned active dataset"
                )

                st.success("Dataset cleaned and auto-saved.")
                st.rerun()

        with c2:
            if st.button(
                "💾 Save Project Now",
                use_container_width=True,
            ):
                save_project(
                    user,
                    st.session_state.raw_df,
                    df,
                    st.session_state.active_filename,
                    st.session_state.formula_logs,
                    st.session_state.chart_config,
                )
                log_activity(
                    user["username"],
                    user["company"],
                    "Manually saved project"
                )
                st.success("Project saved to the persistent vault.")

        with c3:
            if st.button(
                "🔄 Restore Original Upload",
                use_container_width=True,
            ):
                if st.session_state.raw_df is not None:
                    st.session_state.df = (
                        st.session_state.raw_df.copy()
                    )
                    st.success("Original upload restored.")
                    st.rerun()

        if st.session_state.last_clean_report:
            st.markdown("### 🧹 Last Cleaning Report")
            st.dataframe(
                pd.DataFrame(
                    [st.session_state.last_clean_report]
                ),
                use_container_width=True,
                hide_index=True,
            )

        st.divider()

        st.markdown("### ✏️ Editable Intelligent Workflow Grid")

        edited = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="main_data_editor",
        )

        if st.button(
            "💾 Commit Grid Changes",
            use_container_width=True,
        ):
            st.session_state.df = edited.copy()

            save_project(
                user,
                st.session_state.raw_df,
                edited,
                st.session_state.active_filename,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )

            log_activity(
                user["username"],
                user["company"],
                "Saved grid edits"
            )

            st.success("Grid changes committed and auto-saved.")
            st.rerun()

        with st.expander("📋 Read-Only Processed View"):
            st.dataframe(
                st.session_state.df,
                use_container_width=True,
                hide_index=True,
            )


# =============================================================================
# FILE VAULT
# =============================================================================

elif nav == "File Vault":
    st.title("🗄️ Company File Vault")

    files = get_files(user)

    if not files:
        st.info("No files have been saved to this company vault yet.")
    else:
        search = st.text_input(
            "🔎 Search vault",
            placeholder="Type part of a filename..."
        )

        filtered = [
            row for row in files
            if not search
            or search.lower() in row[1].lower()
        ]

        st.caption(
            f"{len(filtered)} matching file(s) "
            f"from {len(files)} total."
        )

        for file_id, fname, ftype, fdate, fjson in filtered:
            a, b, c = st.columns([5, 1, 1])

            with a:
                st.write(
                    f"📄 **{fname}** · {ftype.upper()} · {fdate}"
                )

            with b:
                if st.button(
                    "Load",
                    key=f"load_{file_id}",
                    use_container_width=True,
                ):
                    loaded = dataframe_from_json(fjson)
                    st.session_state.raw_df = loaded.copy()
                    st.session_state.df = loaded.copy()
                    st.session_state.active_filename = fname

                    save_project(
                        user,
                        loaded,
                        loaded,
                        fname,
                        st.session_state.formula_logs,
                        st.session_state.chart_config,
                    )

                    log_activity(
                        user["username"],
                        user["company"],
                        f"Loaded vault file: {fname}"
                    )

                    st.success(f"Loaded {fname}.")
                    st.rerun()

            with c:
                if st.button(
                    "Delete",
                    key=f"delete_{file_id}",
                    use_container_width=True,
                ):
                    delete_file(file_id, user)
                    st.success(f"Deleted {fname}.")
                    st.rerun()


# =============================================================================
# FORMULA LAB
# =============================================================================

elif nav == "Formula Lab":
    st.title("🧮 Intelligent Formula Lab")

    if df is None:
        st.info("Load a dataset first.")
    else:
        formula = st.selectbox(
            "Sheet Formula",
            SHEET_FORMULAS
        )

        if formula in (
            "SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN",
            "UPPER", "LOWER", "TRIM"
        ):
            target = st.selectbox(
                "Target Column",
                list(df.columns)
            )

            if st.button(
                f"Execute {formula}",
                type="primary",
            ):
                try:
                    result = apply_formula(
                        df,
                        formula,
                        {"column": target},
                    )

                    if isinstance(result, tuple):
                        _, col_name, series = result
                        st.session_state.df[col_name] = series
                        result_message = (
                            f"Applied {formula} to '{col_name}'."
                        )
                        st.success(result_message)
                    else:
                        st.success(
                            f"{formula}({target}) = {result}"
                        )

                    st.session_state.formula_logs.append(
                        f"{datetime.now().isoformat(timespec='seconds')} "
                        f"| {formula}({target})"
                    )

                    save_project(
                        user,
                        st.session_state.raw_df,
                        st.session_state.df,
                        st.session_state.active_filename,
                        st.session_state.formula_logs,
                        st.session_state.chart_config,
                    )

                    st.rerun()

                except Exception as exc:
                    st.error(f"Formula error: {exc}")

        elif formula == "CONCATENATE":
            c1, c2, c3 = st.columns(3)

            with c1:
                first_col = st.selectbox(
                    "First Column",
                    list(df.columns),
                    key="concat_first"
                )

            with c2:
                second_col = st.selectbox(
                    "Second Column",
                    list(df.columns),
                    key="concat_second"
                )

            with c3:
                separator = st.text_input(
                    "Separator",
                    value=" ",
                    key="concat_sep"
                )

            new_col = st.text_input(
                "New Column Name",
                value="Combined",
            )

            if st.button(
                "Execute CONCATENATE",
                type="primary",
            ):
                if not new_col.strip():
                    st.error("Enter a new column name.")
                else:
                    _, _, series = apply_formula(
                        df,
                        "CONCATENATE",
                        {
                            "first": first_col,
                            "second": second_col,
                            "separator": separator,
                            "new_column": new_col,
                        },
                    )

                    st.session_state.df[new_col] = series
                    st.session_state.formula_logs.append(
                        f"{datetime.now().isoformat(timespec='seconds')} "
                        f"| CONCATENATE({first_col},{second_col}) "
                        f"-> {new_col}"
                    )

                    save_project(
                        user,
                        st.session_state.raw_df,
                        st.session_state.df,
                        st.session_state.active_filename,
                        st.session_state.formula_logs,
                        st.session_state.chart_config,
                    )

                    st.success(
                        f"Created '{new_col}' successfully."
                    )
                    st.rerun()

        if st.session_state.formula_logs:
            with st.expander("📜 Formula History", expanded=False):
                for item in st.session_state.formula_logs[-20:]:
                    st.write(f"• {item}")


# =============================================================================
# SQL LAB
# =============================================================================

elif nav == "SQL Lab":
    st.title("🗄️ SQL Formula / Query Lab")

    st.caption(
        "The active DataFrame is exposed to SQL as a read-only table "
        "named dataset."
    )

    if df is None:
        st.info("Load a dataset first.")
    else:
        default_query = (
            "SELECT * FROM dataset LIMIT 100"
        )

        query = st.text_area(
            "SQL Query",
            value=default_query,
            height=140,
            help=(
                "Examples: SELECT * FROM dataset WHERE Price > 100000; "
                "SELECT Category, SUM(Price) FROM dataset GROUP BY Category"
            ),
        )

        if st.button(
            "▶ Run SQL",
            type="primary",
            use_container_width=True,
        ):
            try:
                result = run_sql_query(df, query)
                st.session_state.last_sql_result = result

                log_activity(
                    user["username"],
                    user["company"],
                    "Executed SQL query"
                )

                st.success(
                    f"Query returned {len(result):,} row(s)."
                )

            except Exception as exc:
                st.error(f"SQL error: {exc}")

        if st.session_state.last_sql_result is not None:
            st.markdown("### SQL Result")
            st.dataframe(
                st.session_state.last_sql_result,
                use_container_width=True,
                hide_index=True,
            )

            result_csv = (
                st.session_state.last_sql_result
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                "📥 Download SQL Result CSV",
                data=result_csv,
                file_name="dacre_sql_result.csv",
                mime="text/csv",
            )


# =============================================================================
# ADD DYNAMICS
# =============================================================================

elif nav == "ADD DYNAMICS":
    st.markdown(
        """
        <div class="gold-card">
            <h1>✨ ADD DYNAMICS</h1>
            <p>
                DACRE's black-and-gold visualization hub for turning
                processed data into executive-ready insight.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if df is None:
        st.info("Load a dataset first.")
    else:
        chart_types = [
            "Bar Chart",
            "Line Chart",
            "Area Chart",
            "Pie Chart",
        ]

        chart_type = st.selectbox(
            "Chart Type",
            chart_types,
        )

        all_cols = list(df.columns)

        numeric_cols = [
            c for c in df.columns
            if pd.to_numeric(
                df[c].astype(str).str.replace(
                    r"[^\d.\-]",
                    "",
                    regex=True,
                ),
                errors="coerce",
            ).notna().mean() >= 0.50
        ]

        if not numeric_cols:
            st.warning(
                "No numeric-looking columns were detected. "
                "Clean or convert a numeric column first."
            )
        else:
            x_col = st.selectbox(
                "X-Axis / Category",
                all_cols,
            )

            y_col = st.selectbox(
                "Y-Axis / Value",
                numeric_cols,
            )

            max_points = st.slider(
                "Maximum chart rows",
                5,
                min(500, max(5, len(df))),
                min(50, max(5, len(df))),
            )

            chart_df = df[[x_col, y_col]].copy()
            chart_df[y_col] = pd.to_numeric(
                chart_df[y_col].astype(str).str.replace(
                    r"[^\d.\-]",
                    "",
                    regex=True,
                ),
                errors="coerce",
            )
            chart_df = chart_df.dropna(subset=[y_col]).head(max_points)

            st.session_state.chart_config = {
                "type": chart_type,
                "x": x_col,
                "y": y_col,
            }

            st.markdown("### 📊 Live Dynamic Preview")

            if chart_type == "Bar Chart":
                st.bar_chart(
                    chart_df.set_index(x_col)[y_col]
                )

            elif chart_type == "Line Chart":
                st.line_chart(
                    chart_df.set_index(x_col)[y_col]
                )

            elif chart_type == "Area Chart":
                st.area_chart(
                    chart_df.set_index(x_col)[y_col]
                )

            elif chart_type == "Pie Chart":
                try:
                    import plotly.express as px

                    pie_fig = px.pie(
                        chart_df,
                        names=x_col,
                        values=y_col,
                        title=f"{y_col} by {x_col}",
                    )
                    st.plotly_chart(
                        pie_fig,
                        use_container_width=True,
                    )
                except ImportError:
                    st.warning(
                        "Install plotly to enable the interactive pie chart."
                    )

            st.divider()

            attach = st.radio(
                "Chart Attachment Target",
                [
                    "Existing Sheet",
                    "New Sheet",
                ],
                horizontal=True,
            )

            if st.button(
                "📎 Attach Dynamic Configuration",
                use_container_width=True,
            ):
                st.session_state.chart_config["attachment"] = attach

                save_project(
                    user,
                    st.session_state.raw_df,
                    st.session_state.df,
                    st.session_state.active_filename,
                    st.session_state.formula_logs,
                    st.session_state.chart_config,
                )

                log_activity(
                    user["username"],
                    user["company"],
                    f"Configured {chart_type} dynamics"
                )

                st.success(
                    f"{chart_type} is attached to: {attach}"
                )

            st.markdown("### 🧾 Chart Data")
            st.dataframe(
                chart_df,
                use_container_width=True,
                hide_index=True,
            )


# =============================================================================
# DATA INSIGHTS
# =============================================================================

elif nav == "Data Insights":
    st.title("🔎 Data Intelligence Center")

    if df is None:
        st.info("Load a dataset first.")
    else:
        profile = data_profile(df)

        st.markdown("### Dataset Health")

        health_score = 100

        if profile["Duplicates"] > 0:
            health_score -= min(
                30,
                int(
                    profile["Duplicates"]
                    / max(profile["Rows"], 1)
                    * 100
                )
            )

        if profile["Missing Cells"] > 0:
            health_score -= min(
                30,
                int(
                    profile["Missing Cells"]
                    / max(profile["Rows"] * max(profile["Columns"], 1), 1)
                    * 100
                )
            )

        health_score = max(0, health_score)

        a, b, c = st.columns(3)
        a.metric("Data Health Score", f"{health_score}/100")
        b.metric("Rows", f"{len(df):,}")
        c.metric("Columns", f"{len(df.columns):,}")

        st.divider()

        st.markdown("### Missing Values by Column")
        missing_table = pd.DataFrame({
            "Column": df.columns,
            "Missing": [
                int(df[c].isna().sum())
                for c in df.columns
            ],
            "Missing %": [
                round(
                    df[c].isna().mean() * 100,
                    2
                )
                for c in df.columns
            ],
        })

        st.dataframe(
            missing_table,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Numeric Column Statistics")
        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            st.info("No true numeric columns are currently available.")
        else:
            st.dataframe(
                numeric.describe().T,
                use_container_width=True,
            )


# =============================================================================
# PRESENTATION ENGINE
# =============================================================================

elif nav == "Presentation Engine":
    st.title("🎬 Dynamic Presentation Engine")

    if df is None:
        st.info("Load a dataset first.")
    else:
        profile = data_profile(df)
        numeric = df.select_dtypes(include="number")

        st.markdown(
            f"""
            <div class="gold-card">
                <h2>Executive Data Story</h2>
                <p>{profile['Rows']:,} rows · {profile['Columns']:,} columns · {profile['Missing Cells']:,} missing cells</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        slide_count = st.slider("Presentation length", 3, 6, 4)
        slides = [
            ("Executive Overview", f"The active dataset contains {profile['Rows']:,} records across {profile['Columns']:,} columns."),
            ("Data Quality", f"There are {profile['Duplicates']:,} duplicate rows and {profile['Missing Cells']:,} missing cells requiring attention."),
        ]

        if not numeric.empty:
            top_numeric = numeric.columns[0]
            total = pd.to_numeric(numeric[top_numeric], errors="coerce").sum()
            slides.append(("Key Numeric Signal", f"The total of {top_numeric} is {total:,.2f}."))
        else:
            slides.append(("Key Numeric Signal", "No numeric column is currently available for a quantitative summary."))

        slides.append(("Recommended Action", "Review data quality, confirm the most important business metric, then use ADD DYNAMICS to present the strongest pattern."))
        slides.append(("Next Step", "Export the processed workbook and share the executive-ready result with your team."))
        slides = slides[:slide_count]

        if st.button("▶️ Start DI Presentation", type="primary", use_container_width=True):
            st.session_state.presentation_running = True
            st.rerun()

        if st.session_state.get("presentation_running"):
            for i, (title, body) in enumerate(slides, 1):
                st.markdown(
                    f"""
                    <div class="gold-card" style="min-height:180px;margin:14px 0;">
                        <div class="badge">SLIDE {i}</div>
                        <h2>{title}</h2>
                        <p style="font-size:1.15rem;">{body}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("⏹️ Close Presentation", use_container_width=True):
                st.session_state.presentation_running = False
                st.rerun()


# =============================================================================
# EXPORT CENTER
# =============================================================================

elif nav == "Export Center":
    st.title("📦 Export Center")

    if df is None:
        st.info("No processed dataset available.")
    else:
        chart_cfg = st.session_state.chart_config or {}

        st.markdown(
            """
            <div class="success-glow">
                <strong>2-in-1 export:</strong>
                Processed Data + Dynamic Chart Data + Excel chart sheet.
            </div>
            """,
            unsafe_allow_html=True,
        )

        chart_df_for_export = None

        if (
            chart_cfg.get("x") in df.columns
            and chart_cfg.get("y") in df.columns
        ):
            x = chart_cfg["x"]
            y = chart_cfg["y"]
            chart_df_for_export = df[[x, y]].copy()
            chart_df_for_export[y] = pd.to_numeric(
                chart_df_for_export[y].astype(str).str.replace(
                    r"[^\d.\-]",
                    "",
                    regex=True,
                ),
                errors="coerce",
            )
            chart_df_for_export = chart_df_for_export.dropna(
                subset=[y]
            )

        excel_data = make_excel(
            df,
            chart_df=chart_df_for_export,
            chart_type=chart_cfg.get(
                "type",
                "Bar Chart",
            ),
            x_col=chart_cfg.get("x"),
            y_col=chart_cfg.get("y"),
        )

        st.download_button(
            label="📥 Download DACRE Excel Workbook",
            data=excel_data,
            file_name=(
                f"dacre_export_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            ),
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
            type="primary",
        )

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📄 Download Processed CSV",
            data=csv_data,
            file_name="dacre_processed.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if chart_df_for_export is not None:
            st.markdown("### Current Dynamic Configuration")
            st.json(chart_cfg)


# =============================================================================
# COMPANY ADMIN
# =============================================================================

elif nav == "Company Admin":
    st.title("🏢 Company Administration")

    company = user["company"]

    if user["role"] not in ("company_admin", "master"):
        st.warning(
            "Only a Company Admin or Master can manage company users."
        )
    else:
        con = db()

        company_users = pd.read_sql_query(
            """
            SELECT id, first_name, last_name, username,
                   email, role, login_count, created_at, last_login
            FROM users
            WHERE company_name = ?
            ORDER BY id
            """,
            con,
            params=(company,),
        )

        company_activity = pd.read_sql_query(
            """
            SELECT username, action, created_at
            FROM activity
            WHERE company_name = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            con,
            params=(company,),
        )

        con.close()

        st.markdown("### 👥 Users in Your Company")
        st.dataframe(
            company_users,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        if user["role"] == "company_admin":
            st.markdown("### ➕ Create Company User")

            c1, c2 = st.columns(2)

            with c1:
                uf = st.text_input(
                    "User First Name",
                    key="new_user_first"
                )
                ul = st.text_input(
                    "User Last Name",
                    key="new_user_last"
                )
                uu = st.text_input(
                    "User Username",
                    key="new_user_username"
                )

            with c2:
                ue = st.text_input(
                    "User Email",
                    key="new_user_email"
                )
                up = st.text_input(
                    "Temporary Password",
                    type="password",
                    key="new_user_password"
                )
                uk = st.text_input(
                    "User Passkey",
                    type="password",
                    key="new_user_passkey"
                )

            if st.button(
                "Create User",
                type="primary",
                use_container_width=True,
            ):
                ok, msg = create_company_user(
                    uf, ul, uu, ue, up, uk, company
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("### 📜 Company Activity")
        st.dataframe(
            company_activity,
            use_container_width=True,
            hide_index=True,
        )


# =============================================================================
# MASTER DI PORTAL
# =============================================================================

elif nav == "Master DI Portal" and is_master:
    st.markdown(
        """
        <div class="gold-card">
            <h1>👑 Sovereign Master DI Portal</h1>
            <p>
                Good day Master David. This is the highest DACRE
                administration level.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    con = db()

    users_df = pd.read_sql_query(
        """
        SELECT id, username, first_name, last_name,
               company_name, email, role, login_count,
               created_at, last_login
        FROM users
        ORDER BY id
        """,
        con,
    )

    companies_df = pd.read_sql_query(
        """
        SELECT id, name, owner_username, created_at
        FROM companies
        ORDER BY id
        """,
        con,
    )

    activity_df = pd.read_sql_query(
        """
        SELECT id, username, company_name, action, created_at
        FROM activity
        ORDER BY id DESC
        LIMIT 100
        """,
        con,
    )

    con.close()

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Platform Users",
        f"{len(users_df):,}"
    )
    m2.metric(
        "Companies",
        f"{len(companies_df):,}"
    )
    m3.metric(
        "Total Logins",
        f"{int(users_df['login_count'].sum()):,}"
    )
    m4.metric(
        "Audit Events",
        f"{len(activity_df):,}"
    )

    st.divider()

    st.markdown("### 🔐 Master Credential Reset")
    st.caption("For security, Master DI never displays plaintext passwords or passkeys. It can reset them instead.")
    reset_user = st.selectbox(
        "Account to reset",
        users_df["username"].tolist() if not users_df.empty else [],
        key="master_reset_user",
    )
    rc1, rc2 = st.columns(2)
    with rc1:
        new_pw = st.text_input("New Password", type="password", key="master_reset_password")
    with rc2:
        new_pk = st.text_input("New Passkey", type="password", key="master_reset_passkey")

    if st.button("Reset Credentials", type="primary", use_container_width=True):
        if reset_user == MASTER_USERNAME and not MASTER_PASSKEY:
            st.error("Master secret configuration is missing.")
        elif not valid_password(new_pw):
            st.error("New password must be at least 10 characters and include uppercase, lowercase, and a number.")
        elif len(new_pk) < 8:
            st.error("New passkey must contain at least 8 characters.")
        else:
            with db() as reset_con:
                reset_con.execute(
                    "UPDATE users SET password_hash = ?, passkey_hash = ? WHERE username = ?",
                    (hash_password(new_pw), hash_password(new_pk), reset_user),
                )
            log_activity(user["username"], user["company"], f"Reset credentials for {reset_user}")
            st.success(f"Credentials reset for {reset_user}.")
            st.rerun()

    st.markdown("### 👥 All Platform Accounts")
    st.dataframe(
        users_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        """
        **Security note:** passwords and passkeys are stored as
        cryptographic hashes in this upgraded build, so the Master portal
        can audit accounts and reset credentials in a future admin module,
        but cannot recover the original secret text.
        """
    )

    st.markdown("### 🏢 All Companies")
    st.dataframe(
        companies_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### 🛡️ Global Audit Log")
    st.dataframe(
        activity_df,
        use_container_width=True,
        hide_index=True,
    )


# =============================================================================
# FLOATING DI CHAT DOCK
# =============================================================================

st.markdown(
    '<div class="chat-dock"></div>',
    unsafe_allow_html=True,
)

st.write("")
st.write("")

chat1, chat2 = st.columns([5, 1])

with chat1:
    user_message = st.text_input(
        "🎙️ Command DI",
        key="di_dock_input",
        placeholder=(
            "Ask DI about your dataset, rows, columns, cleaning, "
            "export, or analysis..."
        ),
    )

with chat2:
    st.write("")
    if st.button(
        "Send to DI",
        use_container_width=True,
    ):
        if user_message:
            reply = di_reply(
                user_message,
                user,
                st.session_state.df,
            )

            st.session_state.chat.append(
                ("You", user_message)
            )
            st.session_state.chat.append(
                ("DI", reply)
            )

            log_activity(
                user["username"],
                user["company"],
                f"DI command: {user_message[:120]}"
            )

            speak(
                reply,
                LANGUAGES.get(
                    st.session_state.language,
                    "en-NG"
                ),
            )

            st.rerun()

if st.session_state.chat:
    with st.expander(
        "💬 DI Dialogue Stream",
        expanded=False,
    ):
        for sender, message in st.session_state.chat[-10:]:
            if sender == "DI":
                st.markdown(f"**🤖 DI:** {message}")
            else:
                st.markdown(f"**👤 You:** {message}")
