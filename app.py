import hashlib
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
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111")

BASE_DIR = Path(__file__).resolve().parent
LOGO_FILENAME = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"
LOGO_PATH = BASE_DIR / LOGO_FILENAME
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# =============================================================================
# BRAND / FAVICON
# =============================================================================
# The full DACRE artwork remains the visible application logo. At browser-tab
# size, a compact square crop is much more recognizable than the full poster.
# The crop is generated locally from the exact PNG already in the repository,
# so no second logo file is required.
def prepare_favicon():
    if not LOGO_PATH.exists():
        return None

    try:
        source = Image.open(LOGO_PATH).convert("RGBA")
        width, height = source.size

        # Keep the upper/middle DA emblem area.
        top = int(height * 0.08)
        bottom = int(height * 0.64)
        crop = source.crop((0, top, width, bottom))

        side = min(crop.size)
        left = (crop.width - side) // 2
        crop_top = max(0, (crop.height - side) // 2)
        crop = crop.crop(
            (left, crop_top, left + side, crop_top + side)
        )
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
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def hash_password(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # -------------------------------------------------------------------------
    # Compatibility migration: older DACRE builds used different users /
    # companies column names (for example full_name/salt or company).
    # SQLite CREATE TABLE IF NOT EXISTS does NOT change an existing table,
    # which is why a newer build can crash at its first INSERT.
    # Keep the existing database and add/map the canonical columns instead
    # of deleting the user's saved data.
    # -------------------------------------------------------------------------
    def columns(table):
        return {row[1] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()}

    user_cols = columns("users")
    user_additions = {
        "first_name": "TEXT",
        "last_name": "TEXT",
        "username": "TEXT",
        "company_name": "TEXT",
        "email": "TEXT",
        "password_hash": "TEXT",
        "passkey_hash": "TEXT",
        "role": "TEXT",
        "login_count": "INTEGER DEFAULT 0",
        "created_at": "TEXT",
        "last_login": "TEXT",
    }
    for name, definition in user_additions.items():
        if name not in user_cols:
            cur.execute(f"ALTER TABLE users ADD COLUMN {name} {definition}")

    # Map common legacy fields into the canonical authentication fields.
    user_cols = columns("users")
    if "full_name" in user_cols:
        cur.execute(
            """
            UPDATE users
            SET first_name = CASE
                    WHEN first_name IS NULL OR trim(first_name) = ''
                    THEN trim(substr(full_name, 1, instr(trim(full_name), ' ') - 1))
                    ELSE first_name END,
                last_name = CASE
                    WHEN last_name IS NULL OR trim(last_name) = ''
                    THEN trim(substr(trim(full_name), instr(trim(full_name), ' ') + 1))
                    ELSE last_name END
            WHERE full_name IS NOT NULL AND trim(full_name) <> ''
            """
        )
    if "company" in user_cols:
        cur.execute(
            "UPDATE users SET company_name = company WHERE (company_name IS NULL OR trim(company_name) = '') AND company IS NOT NULL"
        )
    cur.execute(
        "UPDATE users SET username = lower(trim(email)) WHERE (username IS NULL OR trim(username) = '') AND email IS NOT NULL"
    )
    cur.execute(
        "UPDATE users SET email = lower(trim(username)) || '@dacre.local' WHERE (email IS NULL OR trim(email) = '') AND username IS NOT NULL"
    )
    cur.execute(
        "UPDATE users SET first_name = 'User' WHERE first_name IS NULL OR trim(first_name) = ''"
    )
    cur.execute(
        "UPDATE users SET last_name = 'Account' WHERE last_name IS NULL OR trim(last_name) = ''"
    )
    cur.execute(
        "UPDATE users SET company_name = 'DACRE' WHERE company_name IS NULL OR trim(company_name) = ''"
    )
    cur.execute(
        "UPDATE users SET password_hash = passkey_hash WHERE (password_hash IS NULL OR trim(password_hash) = '') AND passkey_hash IS NOT NULL"
    )
    cur.execute(
        "UPDATE users SET passkey_hash = password_hash WHERE (passkey_hash IS NULL OR trim(passkey_hash) = '') AND password_hash IS NOT NULL"
    )
    cur.execute(
        "UPDATE users SET role = 'user' WHERE role IS NULL OR trim(role) = ''"
    )
    cur.execute(
        "UPDATE users SET login_count = 0 WHERE login_count IS NULL"
    )
    cur.execute(
        "UPDATE users SET created_at = ? WHERE created_at IS NULL OR trim(created_at) = ''",
        (datetime.now().isoformat(timespec='seconds'),),
    )

    # Companies had the same kind of naming drift in older builds.
    company_cols = columns("companies")
    if "admin_password_hash" not in company_cols and "admin_secret_hash" in company_cols:
        cur.execute("ALTER TABLE companies ADD COLUMN admin_password_hash TEXT")
        cur.execute("UPDATE companies SET admin_password_hash = admin_secret_hash WHERE admin_password_hash IS NULL")

    con.commit()
    con.close()


init_db()


def ensure_master():
    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username = ?",
        (MASTER_USERNAME,),
    )

    if not cur.fetchone():
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute(
            """
            INSERT INTO users
            (
                first_name, last_name, username, company_name, email,
                password_hash, passkey_hash, role, login_count, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
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
            ),
        )
        con.commit()

    con.close()


ensure_master()


def log_activity(username, company, action):
    con = db()
    con.execute(
        """
        INSERT INTO activity(username, company_name, action, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            company,
            action,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    con.commit()
    con.close()


def authenticate(username, password, passkey):
    con = db()

    row = con.execute(
        """
        SELECT
            first_name,
            last_name,
            username,
            company_name,
            email,
            password_hash,
            passkey_hash,
            role
        FROM users
        WHERE lower(username) = lower(?)
        """,
        (username.strip(),),
    ).fetchone()

    if not row:
        con.close()
        return None

    if row[5] != hash_password(password):
        con.close()
        return None

    if row[6] != hash_password(passkey):
        con.close()
        return None

    now = datetime.now().isoformat(timespec="seconds")

    con.execute(
        """
        UPDATE users
        SET login_count = login_count + 1, last_login = ?
        WHERE username = ?
        """,
        (now, row[2]),
    )
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

    if not all(str(value).strip() for value in values):
        return False, "Please complete every required field."

    username_clean = username.strip().lower()
    company_clean = company.strip()
    email_clean = email.strip().lower()

    if username_clean == MASTER_USERNAME:
        return False, "That username is reserved for the Master account."

    con = db()

    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()

        cur.execute(
            "SELECT id FROM companies WHERE lower(name) = lower(?)",
            (company_clean,),
        )

        if not cur.fetchone():
            cur.execute(
                """
                INSERT INTO companies
                (name, owner_username, admin_password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    company_clean,
                    username_clean,
                    hash_password(passkey),
                    now,
                ),
            )

        cur.execute(
            """
            INSERT INTO users
            (
                first_name, last_name, username, company_name, email,
                password_hash, passkey_hash, role, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                first.strip(),
                last.strip(),
                username_clean,
                company_clean,
                email_clean,
                hash_password(password),
                hash_password(passkey),
                "company_admin",
                now,
            ),
        )

        con.commit()
        log_activity(username_clean, company_clean, "Created account")
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Username or email is already registered."

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

    out.columns = [
        re.sub(r"\s+", " ", str(column).strip())
        if str(column).strip()
        else f"Column_{index + 1}"
        for index, column in enumerate(out.columns)
    ]

    out = out.dropna(axis=0, how="all")
    out = out.dropna(axis=1, how="all")

    for column in out.columns:
        if out[column].dtype == "object":
            series = (
                out[column]
                .astype(str)
                .replace({"nan": ""})
                .str.strip()
            )

            numeric_candidate = (
                series
                .str.replace(r"[\$€£₦,%]", "", regex=True)
                .str.replace(",", "", regex=False)
            )

            numeric = pd.to_numeric(
                numeric_candidate,
                errors="coerce",
            )

            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[column] = numeric
            else:
                out[column] = series

    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    if df is None:
        return ""
    return df.to_json(
        orient="split",
        date_format="iso",
    )


def dataframe_from_json(value):
    if not value:
        return None

    try:
        return pd.read_json(
            io.StringIO(value),
            orient="split",
        )
    except Exception:
        return None


def save_file(user, uploaded_file, df):
    con = db()

    con.execute(
        """
        INSERT INTO files
        (
            username, company_name, filename, file_type,
            file_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user["username"],
            user["company"],
            uploaded_file.name,
            uploaded_file.name.rsplit(".", 1)[-1].lower(),
            dataframe_to_json(df),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    con.commit()
    con.close()

    log_activity(
        user["username"],
        user["company"],
        f"Saved file: {uploaded_file.name}",
    )


def get_files(user):
    con = db()

    rows = con.execute(
        """
        SELECT filename, file_type, created_at, file_json
        FROM files
        WHERE company_name = ?
        ORDER BY id DESC
        """,
        (user["company"],),
    ).fetchall()

    con.close()
    return rows


def save_project(
    user,
    raw_df,
    processed_df,
    filename,
    logs,
    chart_config=None,
):
    con = db()

    existing = con.execute(
        """
        SELECT id
        FROM projects
        WHERE username = ? AND company_name = ?
        """,
        (
            user["username"],
            user["company"],
        ),
    ).fetchone()

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
        con.execute(
            """
            UPDATE projects
            SET
                project_name = ?,
                active_filename = ?,
                raw_json = ?,
                processed_json = ?,
                formula_logs = ?,
                chart_config = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                payload[2],
                payload[3],
                payload[4],
                payload[5],
                payload[6],
                payload[7],
                payload[8],
                existing[0],
            ),
        )
    else:
        con.execute(
            """
            INSERT INTO projects
            (
                username, company_name, project_name, active_filename,
                raw_json, processed_json, formula_logs,
                chart_config, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            payload,
        )

    con.commit()
    con.close()


def restore_project(user):
    con = db()

    row = con.execute(
        """
        SELECT
            active_filename,
            raw_json,
            processed_json,
            formula_logs,
            chart_config
        FROM projects
        WHERE username = ? AND company_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            user["username"],
            user["company"],
        ),
    ).fetchone()

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


def make_excel(processed_df, chart_df=None):
    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        processed_df.to_excel(
            writer,
            sheet_name="Processed Data",
            index=False,
        )

        if chart_df is not None:
            chart_df.to_excel(
                writer,
                sheet_name="Dynamic Chart",
                index=False,
            )

    output.seek(0)
    return output.getvalue()


# =============================================================================
# FORMULA ENGINE
# =============================================================================
SHEET_FORMULAS = [
    "SUM",
    "AVERAGE",
    "COUNT",
    "COUNTA",
    "MAX",
    "MIN",
    "SUMIF",
    "COUNTIF",
    "IF",
    "IFERROR",
    "CONCATENATE",
    "UPPER",
    "LOWER",
    "TRIM",
    "UNIQUE",
    "SORT",
    "FILTER",
    "VLOOKUP",
    "XLOOKUP",
]

SQL_FORMULAS = [
    "SELECT",
    "WHERE",
    "GROUP BY",
    "ORDER BY",
    "COUNT",
    "SUM",
    "AVG",
]


def apply_formula(df, formula, options):
    formula = formula.upper()

    if formula == "SUM":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).sum()

    if formula == "AVERAGE":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).mean()

    if formula == "COUNT":
        return int(
            pd.to_numeric(
                df[options["column"]],
                errors="coerce",
            ).count()
        )

    if formula == "COUNTA":
        return int(
            df[options["column"]].notna().sum()
        )

    if formula == "MAX":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).max()

    if formula == "MIN":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).min()

    if formula == "CONCATENATE":
        first = options["first"]
        second = options["second"]

        result = (
            df[first].astype(str)
            + options.get("separator", " ")
            + df[second].astype(str)
        )

        return (
            "column",
            options["new_column"],
            result,
        )

    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[options["column"]].astype(str)

        if formula == "UPPER":
            result = series.str.upper()
        elif formula == "LOWER":
            result = series.str.lower()
        else:
            result = series.str.strip()

        return (
            "column",
            options["column"],
            result,
        )

    if formula == "SUMIF":
        mask = (
            df[options["condition_column"]].astype(str)
            == str(options["condition"])
        )

        return pd.to_numeric(
            df.loc[mask, options["sum_column"]],
            errors="coerce",
        ).sum()

    if formula == "COUNTIF":
        mask = (
            df[options["condition_column"]].astype(str)
            == str(options["condition"])
        )
        return int(mask.sum())

    if formula in ("VLOOKUP", "XLOOKUP"):
        mask = (
            df[options["lookup_column"]].astype(str)
            == str(options["lookup_value"])
        )

        matches = df.loc[
            mask,
            options["return_column"],
        ]

        return (
            matches.iloc[0]
            if not matches.empty
            else "No match"
        )

    if formula == "FILTER":
        mask = (
            df[options["column"]].astype(str)
            == str(options["value"])
        )
        return df.loc[mask].copy()

    if formula == "SORT":
        return df.sort_values(
            options["column"],
            ascending=options.get("ascending", True),
        )

    return None


# =============================================================================
# DI — LOCAL DATA / BUSINESS INTELLIGENCE
# =============================================================================
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

    if any(
        phrase in low
        for phrase in [
            "hello",
            "hi",
            "good morning",
            "good afternoon",
            "good day",
        ]
    ):
        return (
            f"Good day {name}. DI is online and ready "
            "to work with your data."
        )

    if "how many rows" in low or "row count" in low:
        if df is None:
            return (
                "There is no active dataset yet. "
                "Open or upload a file first."
            )
        return f"The active dataset contains {len(df):,} rows."

    if "how many columns" in low or "column count" in low:
        if df is None:
            return "There is no active dataset yet."
        return (
            f"The active dataset contains "
            f"{len(df.columns):,} columns."
        )

    if "duplicate" in low and df is not None:
        return (
            f"The current dataset has "
            f"{int(df.duplicated().sum()):,} duplicate rows."
        )

    if "columns" in low and df is not None:
        return (
            "Current columns: "
            + ", ".join(map(str, df.columns))
        )

    if "clean" in low and df is not None:
        return (
            "Use Process Data. I will remove empty "
            "rows/columns, normalize headers and text, "
            "convert obvious numeric fields and remove "
            "duplicate rows."
        )

    if "chart" in low or "visual" in low:
        return (
            "Open ADD DYNAMICS. Choose a chart type, "
            "category column and numeric value column, "
            "then attach the chart to the project."
        )

    if "formula" in low:
        return (
            "Open Formula Lab. Choose a Sheet Formula "
            "or SQL-style operation, configure its fields "
            "and execute it against the active dataset."
        )

    if "export" in low:
        return (
            "Open Export Center. DACRE can produce CSV "
            "or an Excel workbook containing processed "
            "data and dynamic-chart data."
        )

    if user["role"] == "master":
        return (
            f"With respect, Master David: I understand "
            f"the command '{text}'. I can operate on the "
            "workspace, files, formulas, charts and "
            "administration available in this build."
        )

    return (
        f"DI received your request: '{text}'. "
        "I can help with data cleaning, formulas, "
        "charts, files and exports."
    )


def speak(text):
    safe_text = json.dumps(text)

    components.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance({safe_text});
        message.rate = 0.95;
        message.pitch = 0.85;
        message.lang = "en-NG";

        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        }}
        </script>
        """,
        height=0,
    )


# =============================================================================
# VISUAL SYSTEM
# =============================================================================
st.markdown(
    """
    <style>
    :root {
        --blue: #18b7ff;
        --gold: #f4b942;
        --green: #7df56b;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(24,183,255,.14),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(244,185,66,.10),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #050914,
                #091322 55%,
                #050914
            );
        color: #eef6ff;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 7rem;
    }

    .dacre-hero {
        padding: 24px;
        border: 1px solid rgba(24,183,255,.35);
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                rgba(6,16,31,.94),
                rgba(10,28,47,.88)
            );
        box-shadow: 0 18px 60px rgba(0,0,0,.28);
    }

    .dacre-title {
        font-size: 2.7rem;
        font-weight: 900;
        letter-spacing: .8px;
    }

    .dacre-sub {
        color: #9edcff;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 3px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.15);
        background: rgba(255,255,255,.05);
    }

    .section-card {
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 18px;
        padding: 18px;
        background: rgba(255,255,255,.035);
        margin: 8px 0;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 800;
        min-height: 42px;
        border: 1px solid rgba(24,183,255,.45);
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #040a14,
                #071423
            );
        border-right: 1px solid rgba(24,183,255,.28);
    }

    .gold-panel {
        border: 1px solid rgba(244,185,66,.55);
        border-radius: 22px;
        padding: 20px;
        background:
            radial-gradient(
                circle at 50% 0,
                rgba(244,185,66,.14),
                transparent 45%
            ),
            #080807;
    }

    .chat-dock {
        position: fixed;
        left: 22px;
        right: 22px;
        bottom: 12px;
        z-index: 999;
        padding: 10px 14px;
        border-radius: 18px;
        background: rgba(5,10,19,.93);
        border: 1px solid rgba(24,183,255,.35);
        box-shadow: 0 10px 40px rgba(0,0,0,.45);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# RESTORED DACRE VISUAL LAYER
# =============================================================================
st.markdown(
    """
    <style>
    :root {
        --dacre-cyan: #18b7ff;
        --dacre-mint: #00dc96;
        --dacre-gold: #ffc107;
        --dacre-line: rgba(24,183,255,.22);
    }
    .stApp::before { content: ""; position: fixed; inset: -40%; pointer-events: none;
        background: conic-gradient(from 0deg at 50% 50%, rgba(24,183,255,.05), transparent 25%, rgba(255,193,7,.04) 45%, transparent 70%, rgba(0,220,150,.04) 85%, transparent 100%);
        animation: dacreSpin 48s linear infinite; z-index: 0; }
    @keyframes dacreSpin { to { transform: rotate(360deg); } }
    .main .block-container { position: relative; z-index: 1; padding-top: 2rem; max-width: 1500px; }
    html, body, .stApp, .stApp p, .stApp li, .stApp span, .stApp label, .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stRadio label, .stCheckbox label,
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label, .stDateInput label {
        color: #ffffff !important; font-weight: 700 !important; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        font-family: 'Sora', 'Inter', sans-serif !important; color: #ffffff !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    .stApp h3 { margin-top: 1.4rem; padding-left: 12px; border-left: 4px solid var(--dacre-cyan); text-shadow: 0 0 18px rgba(24,183,255,.35); }
    .stApp code, .stApp kbd, .stCode { font-family: 'JetBrains Mono', monospace !important; color: #7fe3ff !important; background: rgba(24,183,255,.10) !important; border: 1px solid rgba(24,183,255,.25); border-radius: 6px; font-weight: 600 !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #07101d 0%, #060d18 55%, #050914 100%); border-right: 1px solid var(--dacre-line); box-shadow: 24px 0 60px -40px rgba(24,183,255,.55); }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .dacre-hero { position: relative; padding: 24px 30px; border-radius: 20px; border: 1px solid rgba(24,183,255,.35); background: linear-gradient(135deg, rgba(6,16,31,.94), rgba(10,28,47,.86)); box-shadow: 0 24px 60px -28px rgba(0,0,0,.9); backdrop-filter: blur(10px); margin-bottom: 22px; overflow: hidden; }
    .dacre-hero::after { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 3px; background: linear-gradient(90deg, var(--dacre-cyan), var(--dacre-mint), var(--dacre-gold), var(--dacre-cyan)); background-size: 300% 100%; animation: dacreFlow 9s linear infinite; }
    @keyframes dacreFlow { to { background-position: 300% 0; } }
    .stTextInput input, .stTextArea textarea, .stNumberInput input { background: rgba(6,16,31,.92) !important; color: #ffffff !important; font-weight: 700 !important; border: 1.5px solid rgba(24,183,255,.35) !important; border-radius: 12px !important; padding: 10px 14px !important; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--dacre-cyan) !important; box-shadow: 0 0 18px rgba(24,183,255,.3) !important; }
    div.stButton > button, div.stFormSubmitButton > button, div.stDownloadButton > button { border-radius: 12px; border: 1px solid rgba(24,183,255,.45); background: linear-gradient(135deg, #0a2540, #0d3860); color: #ffffff !important; font-weight: 800 !important; padding: 10px 18px; transition: all .22s ease; }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover, div.stDownloadButton > button:hover { border-color: var(--dacre-cyan); background: linear-gradient(135deg, #0d3860, #12508c); box-shadow: 0 0 20px rgba(24,183,255,.45); transform: translateY(-1px); }
    [data-testid="stMetric"] { padding: 14px 18px; border-radius: 16px; border: 1px solid rgba(255,255,255,.10); background: linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.015)); }
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_logo(width=220):
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=width)


def set_user(user):
    st.session_state.user = user

    restored = restore_project(user)

    st.session_state.raw_df = (
        restored["raw"] if restored else None
    )
    st.session_state.df = (
        restored["processed"] if restored else None
    )
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
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =============================================================================
# PUBLIC / AUTH
# =============================================================================
if not st.session_state.user:
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        st.markdown(
            '<div class="dacre-hero">',
            unsafe_allow_html=True,
        )

        show_logo(260)

        st.markdown(
            '<div class="dacre-title">'
            'DACRE Analysis'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="dacre-sub">'
            "Data today. Smarter tomorrows. "
            "Powered by DI — David's Intelligence."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <span class="badge">GET DATA</span>
            <span class="badge">CLEAN</span>
            <span class="badge">ANALYZE</span>
            <span class="badge">VISUALIZE</span>
            <span class="badge">DI INSIGHTS</span>
            <span class="badge">EXPORT</span>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        st.write("")

        st.session_state.auth_mode = st.radio(
            "Portal",
            ["Sign In", "Sign Up"],
            horizontal=True,
            index=(
                0
                if st.session_state.auth_mode == "Sign In"
                else 1
            ),
        )

        if st.session_state.auth_mode == "Sign In":
            st.subheader("Sign In")

            username = st.text_input(
                "Username",
                placeholder="Your DACRE username",
            )

            password = st.text_input(
                "Password",
                type="password",
            )

            passkey = st.text_input(
                "Account Passkey",
                type="password",
            )

            if st.button(
                "Enter DACRE",
                use_container_width=True,
            ):
                authenticated_user = authenticate(
                    username,
                    password,
                    passkey,
                )

                if authenticated_user:
                    set_user(authenticated_user)

                    if (
                        authenticated_user["role"]
                        == "master"
                    ):
                        st.toast(
                            "Good day Master David"
                        )

                    st.rerun()

                st.error(
                    "The username, password or "
                    "passkey is incorrect."
                )

        else:
            st.subheader(
                "Create a company account"
            )

            col_a, col_b = st.columns(2)

            with col_a:
                first = st.text_input("First Name")
                username = st.text_input("Username")
                company = st.text_input(
                    "Company / Business Name"
                )
                email = st.text_input(
                    "Email Address"
                )

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
            ):
                ok, message = create_account(
                    first,
                    last,
                    username,
                    company,
                    email,
                    password,
                    passkey,
                )

                if ok:
                    st.success(message)

                    authenticated_user = authenticate(
                        username,
                        password,
                        passkey,
                    )

                    if authenticated_user:
                        set_user(authenticated_user)
                        st.rerun()
                else:
                    st.error(message)

    st.stop()


# =============================================================================
# AUTHENTICATED SHELL
# =============================================================================
user = st.session_state.user

with st.sidebar:
    show_logo(190)

    st.markdown(
        f"### {DI_NAME}"
    )

    st.caption(
        f"Signed in: "
        f"{user['first_name']} "
        f"{user['last_name']}"
    )

    st.caption(
        f"Company: {user['company']}"
    )

    st.caption(
        "Role: "
        f"{user['role'].replace('_', ' ').title()}"
    )

    st.divider()

    nav_items = [
        "Workspace",
        "File Vault",
        "Formula Lab",
        "ADD DYNAMICS",
        "Export Center",
    ]

    if user["role"] == "master":
        nav_items.append("Master DI Portal")

    nav = st.radio(
        "DACRE Navigation",
        nav_items,
        index=0,
    )

    if st.button(
        "Sign Out",
        use_container_width=True,
    ):
        log_activity(
            user["username"],
            user["company"],
            "Signed out",
        )
        st.session_state.user = None
        st.rerun()


if nav == "ADD DYNAMICS":
    st.markdown(
        """
        <div class="gold-panel">
        <h2>ADD DYNAMICS — Charting & Presentation Hub</h2>
        <p>
        Turn processed data into a presentation-ready dynamic view.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"## {APP_NAME}"
    )


# =============================================================================
# WORKSPACE
# =============================================================================
if nav == "Workspace":
    if user["role"] == "master":
        st.success(
            "Good day Master David. "
            "DI recognizes the master account."
        )
    else:
        st.info(
            f"Welcome back, "
            f"{user['first_name']}."
        )

    st.markdown(
        """
        <div class="dacre-hero">
            <div class="dacre-title">
                Intelligent Workflow
            </div>
            <div class="dacre-sub">
                Get data → clean → analyze →
                visualize → export.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Get Data — upload CSV, Excel or JSON",
        type=SUPPORTED_EXTENSIONS,
    )

    if uploaded and st.button(
        "Open File in Workspace",
        use_container_width=True,
    ):
        try:
            loaded = load_dataframe(uploaded)

            st.session_state.raw_df = loaded.copy()
            st.session_state.df = loaded.copy()
            st.session_state.active_filename = (
                uploaded.name
            )

            save_file(
                user,
                uploaded,
                loaded,
            )

            save_project(
                user,
                loaded,
                loaded,
                uploaded.name,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )

            st.success(
                f"{uploaded.name} is now active."
            )
            st.rerun()

        except Exception as exc:
            st.error(
                f"Could not read the file: {exc}"
            )

    if st.session_state.df is None:
        st.info(
            "No active data yet. Start with "
            "Get Data or open a file from "
            "File Vault."
        )

    else:
        df = st.session_state.df

        metric_a, metric_b, metric_c, metric_d = (
            st.columns(4)
        )

        metric_a.metric(
            "Rows",
            f"{len(df):,}",
        )

        metric_b.metric(
            "Columns",
            f"{len(df.columns):,}",
        )

        metric_c.metric(
            "Duplicates",
            f"{int(df.duplicated().sum()):,}",
        )

        metric_d.metric(
            "Missing Cells",
            f"{int(df.isna().sum().sum()):,}",
        )

        st.subheader(
            "Processed Data — Read Only Preview"
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=360,
        )

        st.subheader(
            "Intelligent Workflow — Editable"
        )

        edited = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="main_editor",
        )

        if not edited.equals(df):
            st.session_state.df = edited

            save_project(
                user,
                st.session_state.raw_df,
                edited,
                st.session_state.active_filename,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )

            st.toast(
                "DACRE auto-saved your changes."
            )

        action_a, action_b, action_c, action_d = (
            st.columns(4)
        )

        with action_a:
            if st.button(
                "✨ Process Data",
                use_container_width=True,
            ):
                st.session_state.df = clean_dataframe(
                    st.session_state.df
                )

                st.session_state.formula_logs.append(
                    "Processed data: cleaned, normalized, "
                    "converted and deduplicated."
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
                    "DI processed the dataset."
                )
                st.rerun()

        with action_b:
            if st.button(
                "🧹 Remove Duplicates",
                use_container_width=True,
            ):
                st.session_state.df = (
                    st.session_state.df
                    .drop_duplicates()
                    .reset_index(drop=True)
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
                    "Duplicate rows removed."
                )
                st.rerun()

        with action_c:
            sort_column = st.selectbox(
                "Sort",
                list(st.session_state.df.columns),
                key="sort_column",
            )

        with action_d:
            if st.button(
                "Sort Ascending",
                use_container_width=True,
            ):
                st.session_state.df = (
                    st.session_state.df
                    .sort_values(sort_column)
                    .reset_index(drop=True)
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


# =============================================================================
# FILE VAULT
# =============================================================================
elif nav == "File Vault":
    st.subheader("File Vault")

    st.caption(
        "Files are isolated by company."
    )

    rows = get_files(user)

    if not rows:
        st.info(
            "No files are stored for this company yet."
        )

    else:
        table = pd.DataFrame(
            rows,
            columns=[
                "Filename",
                "Type",
                "Saved At",
                "Data",
            ],
        )

        st.dataframe(
            table[
                [
                    "Filename",
                    "Type",
                    "Saved At",
                ]
            ],
            use_container_width=True,
        )

        selected = st.selectbox(
            "Open from Vault",
            table["Filename"].tolist(),
        )

        if st.button(
            "Open Selected File",
            use_container_width=True,
        ):
            selected_row = next(
                row
                for row in rows
                if row[0] == selected
            )

            loaded = dataframe_from_json(
                selected_row[3]
            )

            st.session_state.raw_df = (
                loaded.copy()
            )

            st.session_state.df = (
                loaded.copy()
            )

            st.session_state.active_filename = (
                selected
            )

            save_project(
                user,
                loaded,
                loaded,
                selected,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )

            st.success(
                f"{selected} opened."
            )

            st.rerun()


# =============================================================================
# FORMULA LAB
# =============================================================================
elif nav == "Formula Lab":
    st.subheader("Formula Lab")

    if st.session_state.df is None:
        st.info(
            "Open a dataset first."
        )

    else:
        df = st.session_state.df

        formula_family = st.radio(
            "Formula family",
            [
                "Sheet Formulas",
                "SQL-style Formulas",
            ],
            horizontal=True,
        )

        formulas = (
            SHEET_FORMULAS
            if formula_family == "Sheet Formulas"
            else SQL_FORMULAS
        )

        formula = st.selectbox(
            "Formula",
            formulas,
        )

        if formula in [
            "SUM",
            "AVERAGE",
            "COUNT",
            "COUNTA",
            "MAX",
            "MIN",
        ]:
            column = st.selectbox(
                "Target column",
                list(df.columns),
            )

            if st.button(
                "Execute Formula",
                use_container_width=True,
            ):
                result = apply_formula(
                    df,
                    formula,
                    {"column": column},
                )

                st.success(
                    f"{formula}({column}) = {result}"
                )

        elif formula == "CONCATENATE":
            col_a, col_b = st.columns(2)

            with col_a:
                first = st.selectbox(
                    "First column",
                    list(df.columns),
                )

            with col_b:
                second = st.selectbox(
                    "Second column",
                    list(df.columns),
                )

            new_column = st.text_input(
                "New column name",
                "Combined",
            )

            if st.button(
                "Execute CONCATENATE",
                use_container_width=True,
            ):
                _, name, series = apply_formula(
                    df,
                    formula,
                    {
                        "first": first,
                        "second": second,
                        "new_column": new_column,
                    },
                )

                st.session_state.df[name] = series

                st.session_state.formula_logs.append(
                    f"CONCATENATE({first},{second}) "
                    f"→ {name}"
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
                    f"Created column: {name}"
                )
                st.rerun()

        elif formula in [
            "UPPER",
            "LOWER",
            "TRIM",
        ]:
            column = st.selectbox(
                "Target column",
                list(df.columns),
            )

            if st.button(
                f"Execute {formula}",
                use_container_width=True,
            ):
                _, name, series = apply_formula(
                    df,
                    formula,
                    {"column": column},
                )

                st.session_state.df[name] = series

                st.session_state.formula_logs.append(
                    f"{formula}({column})"
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

        elif formula in [
            "SUMIF",
            "COUNTIF",
        ]:
            col_a, col_b, col_c = (
                st.columns(3)
            )

            with col_a:
                condition_column = st.selectbox(
                    "Condition column",
                    list(df.columns),
                )

            with col_b:
                condition = st.text_input(
                    "Condition value"
                )

            with col_c:
                target_column = st.selectbox(
                    "Target column",
                    list(df.columns),
                )

            if st.button(
                f"Execute {formula}",
                use_container_width=True,
            ):
                result = apply_formula(
                    df,
                    formula,
                    {
                        "condition_column":
                            condition_column,
                        "condition":
                            condition,
                        "sum_column":
                            target_column,
                    },
                )

                st.success(
                    f"{formula} result = {result}"
                )

        elif formula in [
            "VLOOKUP",
            "XLOOKUP",
        ]:
            col_a, col_b, col_c = (
                st.columns(3)
            )

            with col_a:
                lookup_column = st.selectbox(
                    "Lookup column",
                    list(df.columns),
                )

            with col_b:
                return_column = st.selectbox(
                    "Return column",
                    list(df.columns),
                )

            with col_c:
                lookup_value = st.text_input(
                    "Lookup value"
                )

            if st.button(
                f"Execute {formula}",
                use_container_width=True,
            ):
                result = apply_formula(
                    df,
                    formula,
                    {
                        "lookup_column":
                            lookup_column,
                        "return_column":
                            return_column,
                        "lookup_value":
                            lookup_value,
                    },
                )

                st.success(
                    f"Result = {result}"
                )

        elif formula == "FILTER":
            column = st.selectbox(
                "Filter column",
                list(df.columns),
            )

            value = st.text_input(
                "Value equals"
            )

            if st.button(
                "Execute FILTER",
                use_container_width=True,
            ):
                result = apply_formula(
                    df,
                    formula,
                    {
                        "column": column,
                        "value": value,
                    },
                )

                st.dataframe(
                    result,
                    use_container_width=True,
                )

        elif formula == "SORT":
            column = st.selectbox(
                "Sort column",
                list(df.columns),
            )

            ascending = st.toggle(
                "Ascending",
                True,
            )

            if st.button(
                "Execute SORT",
                use_container_width=True,
            ):
                st.session_state.df = (
                    apply_formula(
                        df,
                        formula,
                        {
                            "column": column,
                            "ascending": ascending,
                        },
                    )
                )

                st.session_state.formula_logs.append(
                    f"SORT({column}, ascending={ascending})"
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

        else:
            st.info(
                "SQL-style controls are intentionally "
                "kept separate from arbitrary SQL execution "
                "in this first production-safe build."
            )


# =============================================================================
# ADD DYNAMICS
# =============================================================================
elif nav == "ADD DYNAMICS":
    if st.session_state.df is None:
        st.info(
            "Open a dataset first."
        )

    else:
        df = st.session_state.df

        chart_type = st.selectbox(
            "Chart type",
            [
                "Bar",
                "Line",
                "Area",
            ],
        )

        category = st.selectbox(
            "Category / X-axis",
            list(df.columns),
        )

        numeric_columns = [
            column
            for column in df.columns
            if pd.api.types.is_numeric_dtype(
                df[column]
            )
        ]

        if not numeric_columns:
            st.warning(
                "The active dataset has no numeric "
                "columns for a chart."
            )

        else:
            value = st.selectbox(
                "Value / Y-axis",
                numeric_columns,
            )

            chart_data = (
                df[
                    [
                        category,
                        value,
                    ]
                ]
                .dropna()
                .groupby(
                    category,
                    as_index=False,
                )[value]
                .sum()
                .head(100)
            )

            chart_indexed = (
                chart_data.set_index(category)
            )

            if chart_type == "Bar":
                st.bar_chart(
                    chart_indexed[value]
                )
            elif chart_type == "Line":
                st.line_chart(
                    chart_indexed[value]
                )
            else:
                st.area_chart(
                    chart_indexed[value]
                )

            st.session_state.chart_config = {
                "type": chart_type,
                "category": category,
                "value": value,
            }

            attachment = st.radio(
                "Attach chart",
                [
                    "Existing Sheet",
                    "New Sheet",
                ],
                horizontal=True,
            )

            if st.button(
                "Attach Dynamic Chart",
                use_container_width=True,
            ):
                st.session_state.formula_logs.append(
                    f"Attached {chart_type} chart "
                    f"({category} → {value}) "
                    f"to {attachment}."
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
                    "Dynamic chart attached to the project."
                )


# =============================================================================
# EXPORT CENTER
# =============================================================================
elif nav == "Export Center":
    st.subheader("Export Center")

    if st.session_state.df is None:
        st.info(
            "There is no processed dataset to export."
        )

    else:
        df = st.session_state.df

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Processed CSV",
            csv_data,
            file_name="DACRE_Processed_Data.csv",
            mime="text/csv",
            use_container_width=True,
        )

        chart_df = None

        if st.session_state.chart_config:
            chart_config = (
                st.session_state.chart_config
            )

            category = chart_config.get(
                "category"
            )
            value = chart_config.get(
                "value"
            )

            if (
                category in df.columns
                and value in df.columns
            ):
                chart_df = df[
                    [
                        category,
                        value,
                    ]
                ].copy()

        xlsx_data = make_excel(
            df,
            chart_df,
        )

        st.download_button(
            "Download Excel — Data + Dynamic Chart",
            xlsx_data,
            file_name="DACRE_Analysis.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

        st.subheader(
            "Formula / Action Log"
        )

        if st.session_state.formula_logs:
            for action in (
                st.session_state.formula_logs[-20:]
            ):
                st.write(
                    "•",
                    action,
                )
        else:
            st.caption(
                "No actions recorded yet."
            )


# =============================================================================
# MASTER DI PORTAL
# =============================================================================
elif (
    nav == "Master DI Portal"
    and user["role"] == "master"
):
    st.subheader(
        "👑 Overall DI Portal"
    )

    st.success(
        "Good day Master David. "
        "Absolute master access confirmed."
    )

    con = db()

    users = pd.read_sql_query(
        """
        SELECT
            id,
            first_name,
            last_name,
            username,
            company_name,
            email,
            role,
            login_count,
            created_at,
            last_login
        FROM users
        ORDER BY id DESC
        """,
        con,
    )

    companies = pd.read_sql_query(
        """
        SELECT
            id,
            name,
            owner_username,
            created_at
        FROM companies
        ORDER BY id DESC
        """,
        con,
    )

    activity = pd.read_sql_query(
        """
        SELECT
            username,
            company_name,
            action,
            created_at
        FROM activity
        ORDER BY id DESC
        LIMIT 200
        """,
        con,
    )

    con.close()

    stat_a, stat_b, stat_c, stat_d = (
        st.columns(4)
    )

    stat_a.metric(
        "Users",
        len(users),
    )

    stat_b.metric(
        "Companies",
        len(companies),
    )

    stat_c.metric(
        "Total Logins",
        (
            int(users["login_count"].sum())
            if not users.empty
            else 0
        ),
    )

    stat_d.metric(
        "Activity Events",
        len(activity),
    )

    users_tab, companies_tab, activity_tab = (
        st.tabs(
            [
                "Users",
                "Companies",
                "Activity",
            ]
        )
    )

    with users_tab:
        st.dataframe(
            users,
            use_container_width=True,
        )

    with companies_tab:
        st.dataframe(
            companies,
            use_container_width=True,
        )

    with activity_tab:
        st.dataframe(
            activity,
            use_container_width=True,
        )


# =============================================================================
# DI CHAT DOCK
# =============================================================================
st.markdown(
    '<div class="chat-dock">',
    unsafe_allow_html=True,
)

chat_input_col, chat_button_col = (
    st.columns([5, 1])
)

with chat_input_col:
    message = st.text_input(
        "💬 Talk to DI",
        placeholder=(
            "Ask DI about your data, formulas, "
            "charts or workflow..."
        ),
        key="di_message",
        label_visibility="visible",
    )

with chat_button_col:
    send_message = st.button(
        "Send to DI",
        use_container_width=True,
    )

if send_message and message:
    reply = di_reply(
        message,
        user,
        st.session_state.df,
    )

    st.session_state.chat.append(
        ("You", message)
    )

    st.session_state.chat.append(
        ("DI", reply)
    )

    log_activity(
        user["username"],
        user["company"],
        f"DI chat: {message[:120]}",
    )

    speak(reply)

    st.rerun()

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

if st.session_state.chat:
    with st.expander(
        "DI Conversation",
        expanded=False,
    ):
        for speaker, text in (
            st.session_state.chat[-8:]
        ):
            st.markdown(
                f"**{speaker}:** {text}"
            )
