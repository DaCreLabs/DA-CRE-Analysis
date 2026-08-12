import hashlib
import hmac
import io
import json
import os
import re
import sqlite3
import smtplib
import threading
import time
import urllib.parse
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# Optional desktop/audio-file speech recognition. Browser voice uses the Web Speech API
# and does not require the SpeechRecognition Python package.
sr = None

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
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111").strip()

# The default master credential is stored as a SHA-256 hash so the private
# passkey is not exposed in the source code. If DACRE_MASTER_PASSKEY is set
# in Streamlit Secrets/environment, that value takes precedence.
MASTER_PASSKEY_HASH = os.getenv(
    "DACRE_MASTER_PASSKEY_HASH",
    "1d9763eb96e88387bf4a18b7ca1a94a4a3a80ea0353cf4203764c0bccfbda27f"
).strip()

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png",
    "dacre_logo.png",
    "logo.png",
]
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Streamlit Community Cloud does not guarantee persistence for local files.
def cloud_persistence_configured():
    try:
        return bool(st.secrets.get("DACRE_DATABASE_URL", "") or st.secrets.get("DATABASE_URL", "") or st.secrets.get("SUPABASE_DB_URL", ""))
    except Exception:
        return bool(os.getenv("DACRE_DATABASE_URL") or os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL"))

ONLINE_IMAGES = {
    "analytics": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=82",
    "cleaning": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=82",
    "charts": "https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=1200&q=82",
    "conversation": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=82",
}

DI_AVATAR_PATH = BASE_DIR / "di_avatar.png"

# DI voice/language profiles. Browser speech recognition and speech synthesis
# are used first so DACRE works without requiring a paid voice service.
DI_LANGUAGE_PROFILES = {
    "English — Nigeria": {"code": "en-NG", "label": "English (Nigeria)"},
    "Yorùbá": {"code": "yo-NG", "label": "Yorùbá"},
    "Igbo": {"code": "ig-NG", "label": "Igbo"},
    "Hausa": {"code": "ha-NG", "label": "Hausa"},
    "Spanish": {"code": "es-ES", "label": "Spanish"},
    "French": {"code": "fr-FR", "label": "French"},
    "Hindi — India": {"code": "hi-IN", "label": "Hindi"},
    "English — UK": {"code": "en-GB", "label": "English (UK)"},
    "Arabic": {"code": "ar-SA", "label": "Arabic"},
    "Chinese — Mandarin": {"code": "zh-CN", "label": "Mandarin Chinese"},
    "Portuguese — Brazil": {"code": "pt-BR", "label": "Brazilian Portuguese"},
    "German": {"code": "de-DE", "label": "German"},
}

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
_DB_SCHEMA_LOCK = threading.RLock()
_DB_SCHEMA_VERSION = 9

@contextmanager
def _db_file_lock(timeout=90):
    """Serialize SQLite schema migrations across Streamlit processes."""
    lock_path = Path(DB_PATH).with_name(".dacre_platform.schema.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(lock_path, "a+")
    try:
        try:
            import fcntl
            deadline = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Timed out waiting for the DACRE database migration lock.")
                    time.sleep(0.25)
        except ImportError:
            pass
        yield
    finally:
        try:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except (ImportError, OSError):
            pass
        handle.close()

def db():
    con = sqlite3.connect(DB_PATH, timeout=60, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        con.execute("PRAGMA busy_timeout=60000")
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("PRAGMA synchronous=NORMAL")
    except sqlite3.DatabaseError:
        pass
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS loan_clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            client_name TEXT NOT NULL,
            whatsapp_number TEXT NOT NULL,
            loan_amount REAL NOT NULL DEFAULT 0,
            lent_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            reminder_2_sent INTEGER NOT NULL DEFAULT 0,
            due_sent INTEGER NOT NULL DEFAULT 0,
            reminder_2_message_id TEXT,
            due_message_id TEXT,
            last_whatsapp_status TEXT,
            last_whatsapp_error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    for _column, _dtype in [
        ("reminder_2_message_id", "TEXT"),
        ("due_message_id", "TEXT"),
        ("last_whatsapp_status", "TEXT"),
        ("last_whatsapp_error", "TEXT"),
    ]:
        try:
            cur.execute(f"ALTER TABLE loan_clients ADD COLUMN {_column} {_dtype}")
        except sqlite3.OperationalError:
            pass

    cur.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_delivery_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER,
            company_name TEXT NOT NULL,
            client_name TEXT NOT NULL,
            whatsapp_number TEXT NOT NULL,
            reminder_type TEXT NOT NULL,
            template_name TEXT NOT NULL,
            message_id TEXT,
            status TEXT NOT NULL,
            response TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS di_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            priority INTEGER NOT NULL DEFAULT 100,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS di_agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            di_name TEXT UNIQUE NOT NULL,
            di_code TEXT UNIQUE NOT NULL,
            specialty TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            assigned_company TEXT,
            system_role TEXT,
            avatar_url TEXT,
            voice_profile TEXT,
            thinking_style TEXT,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_active TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS call_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            room_name TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            host_username TEXT NOT NULL,
            mode TEXT NOT NULL DEFAULT 'team',
            created_at TEXT NOT NULL,
            ended_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS call_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            participant_type TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            joined_at TEXT NOT NULL,
            left_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS decision_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            context TEXT NOT NULL,
            decision TEXT NOT NULL,
            expected_outcome TEXT,
            review_date TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            outcome TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS opportunity_radar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            impact TEXT NOT NULL,
            evidence TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()

init_db()

def _table_exists(con, table_name):
    return con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
        (table_name,),
    ).fetchone() is not None

def _table_columns(con, table_name):
    try:
        return {row["name"] for row in con.execute(f"PRAGMA table_info({table_name})").fetchall()}
    except Exception:
        return set()

def _schema_exec(con, sql, params=(), retries=20):
    last = None
    for attempt in range(retries):
        try:
            return con.execute(sql, params)
        except sqlite3.OperationalError as exc:
            last = exc
            msg = str(exc).lower()
            if "locked" not in msg and "busy" not in msg:
                raise
            time.sleep(min(1.5, 0.15 * (attempt + 1)))
    raise last

def _ensure_columns(con, table_name, columns):
    if not _table_exists(con, table_name):
        return
    current = _table_columns(con, table_name)
    for name, dtype in columns.items():
        if name not in current:
            _schema_exec(con, f"ALTER TABLE {table_name} ADD COLUMN {name} {dtype}")

def _rebuild_call_rooms(con):
    """Canonicalize every historical call_rooms schema without losing records."""
    if not _table_exists(con, "call_rooms"):
        con.execute("""
            CREATE TABLE call_rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL DEFAULT '',
                room_name TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL DEFAULT 'DACRE Call',
                host_username TEXT NOT NULL DEFAULT '',
                mode TEXT NOT NULL DEFAULT 'team',
                created_at TEXT NOT NULL DEFAULT '',
                ended_at TEXT
            )
        """)
        return

    cols = _table_columns(con, "call_rooms")
    canonical = {"id", "company_name", "room_name", "title", "host_username", "mode", "created_at", "ended_at"}
    if canonical.issubset(cols) and "room_code" not in cols:
        con.execute("UPDATE call_rooms SET room_name='DACRE-LEGACY-'||id WHERE room_name IS NULL OR TRIM(room_name)=''")
        con.execute("UPDATE call_rooms SET title='DACRE Call' WHERE title IS NULL OR TRIM(title)=''")
        con.execute("UPDATE call_rooms SET host_username='' WHERE host_username IS NULL")
        con.execute("UPDATE call_rooms SET mode='team' WHERE mode IS NULL OR TRIM(mode)=''")
        con.execute("UPDATE call_rooms SET created_at='' WHERE created_at IS NULL")
        return

    old_name = "call_rooms_legacy_v9"
    con.execute(f"DROP TABLE IF EXISTS {old_name}")
    con.execute(f"ALTER TABLE call_rooms RENAME TO {old_name}")
    con.execute("""
        CREATE TABLE call_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL DEFAULT '',
            room_name TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL DEFAULT 'DACRE Call',
            host_username TEXT NOT NULL DEFAULT '',
            mode TEXT NOT NULL DEFAULT 'team',
            created_at TEXT NOT NULL DEFAULT '',
            ended_at TEXT
        )
    """)
    old_cols = _table_columns(con, old_name)

    def expr(name, fallback):
        return name if name in old_cols else fallback

    room_expr = "COALESCE(NULLIF(TRIM(room_name),''), NULLIF(TRIM(room_code),''), 'DACRE-LEGACY-'||id)" if "room_name" in old_cols and "room_code" in old_cols else (
        "COALESCE(NULLIF(TRIM(room_name),''), 'DACRE-LEGACY-'||id)" if "room_name" in old_cols else (
            "COALESCE(NULLIF(TRIM(room_code),''), 'DACRE-LEGACY-'||id)" if "room_code" in old_cols else "'DACRE-LEGACY-'||id"
        )
    )
    company_expr = expr("company_name", "''")

    t_col = expr("title", "''")
    title_expr = f"COALESCE(NULLIF(TRIM({t_col}),''),'DACRE Call')" if "title" in old_cols else "'DACRE Call'"

    host_expr = "COALESCE(NULLIF(TRIM(host_username),''), NULLIF(TRIM(created_by),''), '')" if "host_username" in old_cols and "created_by" in old_cols else (
        "COALESCE(NULLIF(TRIM(host_username),''), '')" if "host_username" in old_cols else (
            "COALESCE(NULLIF(TRIM(created_by),''), '')" if "created_by" in old_cols else "''"
        )
    )
    mode_expr = "COALESCE(NULLIF(TRIM(mode),''),'team')" if "mode" in old_cols else "'team'"
    created_expr = "COALESCE(NULLIF(TRIM(created_at),''), created)" if "created_at" in old_cols and "created" in old_cols else (
        "COALESCE(NULLIF(TRIM(created_at),''),'')" if "created_at" in old_cols else (
            "COALESCE(NULLIF(TRIM(created),''),'')" if "created" in old_cols else "''"
        )
    )
    ended_expr = "ended_at" if "ended_at" in old_cols else "NULL"

    query = f"SELECT id, {company_expr} AS company_name, {room_expr} AS room_name, {title_expr} AS title, {host_expr} AS host_username, {mode_expr} AS mode, {created_expr} AS created_at, {ended_expr} AS ended_at FROM {old_name}"
    rows = con.execute(query).fetchall()
    seen = set()
    for r in rows:
        room = str(r["room_name"] or f"DACRE-LEGACY-{r['id']}")
        if room in seen:
            room = f"{room}-{r['id']}"
        seen.add(room)
        con.execute(
            "INSERT INTO call_rooms(id, company_name, room_name, title, host_username, mode, created_at, ended_at) VALUES(?,?,?,?,?,?,?,?)",
            (r["id"], str(r["company_name"] or ""), room, str(r["title"] or "DACRE Call"), str(r["host_username"] or ""), str(r["mode"] or "team"), str(r["created_at"] or ""), r["ended_at"])
        )
    con.execute(f"DROP TABLE {old_name}")

def _rebuild_call_participants(con):
    """Canonicalize call_participants and import old call_members rows when present."""
    if not _table_exists(con, "call_participants"):
        con.execute("""
            CREATE TABLE call_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT NOT NULL,
                company_name TEXT NOT NULL DEFAULT '',
                participant_type TEXT NOT NULL DEFAULT 'user',
                participant_id TEXT NOT NULL DEFAULT '',
                display_name TEXT NOT NULL DEFAULT '',
                joined_at TEXT NOT NULL DEFAULT '',
                left_at TEXT
            )
        """)
    else:
        cols = _table_columns(con, "call_participants")
        canonical = {"id", "room_name", "company_name", "participant_type", "participant_id", "display_name", "joined_at", "left_at"}
        if not canonical.issubset(cols) or "room_code" in cols:
            old_name = "call_participants_legacy_v9"
            con.execute(f"DROP TABLE IF EXISTS {old_name}")
            con.execute(f"ALTER TABLE call_participants RENAME TO {old_name}")
            con.execute("""
                CREATE TABLE call_participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT NOT NULL,
                    company_name TEXT NOT NULL DEFAULT '',
                    participant_type TEXT NOT NULL DEFAULT 'user',
                    participant_id TEXT NOT NULL DEFAULT '',
                    display_name TEXT NOT NULL DEFAULT '',
                    joined_at TEXT NOT NULL DEFAULT '',
                    left_at TEXT
                )
            """)
            old_cols = _table_columns(con, old_name)

            def col_or(name, fallback):
                return name if name in old_cols else fallback

            room_expr = "COALESCE(NULLIF(TRIM(room_name),''), NULLIF(TRIM(room_code),''), '')" if "room_name" in old_cols and "room_code" in old_cols else (
                "COALESCE(NULLIF(TRIM(room_name),''), '')" if "room_name" in old_cols else (
                    "COALESCE(NULLIF(TRIM(room_code),''), '')" if "room_code" in old_cols else "''"
                )
            )
            type_expr = col_or("participant_type", "'user'")
            pid_expr = col_or("participant_id", col_or("username", "''"))
            name_expr = col_or("display_name", col_or("username", "''"))
            joined_expr = col_or("joined_at", "''")
            company_expr = col_or("company_name", "''")
            left_expr = col_or("left_at", "NULL")

            query = f"SELECT id, {room_expr} AS room_name, {company_expr} AS company_name, {type_expr} AS participant_type, {pid_expr} AS participant_id, {name_expr} AS display_name, {joined_expr} AS joined_at, {left_expr} AS left_at FROM {old_name}"
            rows = con.execute(query).fetchall()
            for r in rows:
                con.execute(
                    "INSERT INTO call_participants(id, room_name, company_name, participant_type, participant_id, display_name, joined_at, left_at) VALUES(?,?,?,?,?,?,?,?)",
                    (r["id"], str(r["room_name"] or ""), str(r["company_name"] or ""), str(r["participant_type"] or "user"), str(r["participant_id"] or ""), str(r["display_name"] or ""), str(r["joined_at"] or ""), r["left_at"])
                )
            con.execute(f"DROP TABLE {old_name}")

    if _table_exists(con, "call_members"):
        mcols = _table_columns(con, "call_members")
        room_expr = "room_code" if "room_code" in mcols else ("room_name" if "room_name" in mcols else "''")
        user_expr = "username" if "username" in mcols else "''"
        company_expr = "company_name" if "company_name" in mcols else "''"
        joined_expr = "joined_at" if "joined_at" in mcols else "NULL"
        left_expr = "left_at" if "left_at" in mcols else "NULL"
        rows = con.execute(f"SELECT id, {room_expr} AS room_name, {company_expr} AS company_name, {user_expr} AS username, {joined_expr} AS joined_at, {left_expr} AS left_at FROM call_members").fetchall()
        for r in rows:
            exists = con.execute("SELECT 1 FROM call_participants WHERE room_name=? AND participant_id=? LIMIT 1", (str(r["room_name"] or ""), str(r["username"] or ""))).fetchone()
            if not exists:
                con.execute(
                    "INSERT INTO call_participants(room_name, company_name, participant_type, participant_id, display_name, joined_at, left_at) VALUES(?,?,?,?,?,?,?)",
                    (str(r["room_name"] or ""), str(r["company_name"] or ""), "user", str(r["username"] or ""), str(r["username"] or ""), str(r["joined_at"] or ""), r["left_at"])
                )

def ensure_runtime_schema():
    """One canonical, idempotent migration for all historical DACRE call schemas."""
    with _DB_SCHEMA_LOCK:
        with _db_file_lock():
            con = db()
            try:
                con.execute("CREATE TABLE IF NOT EXISTS dacre_schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
                row = con.execute("SELECT value FROM dacre_schema_meta WHERE key='schema_version'").fetchone()
                try:
                    current = int(row["value"]) if row else 0
                except Exception:
                    current = 0
                if current < _DB_SCHEMA_VERSION:
                    con.execute("BEGIN IMMEDIATE")
                    _rebuild_call_rooms(con)
                    _rebuild_call_participants(con)
                    con.execute("CREATE TABLE IF NOT EXISTS decision_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT,company_name TEXT,username TEXT,title TEXT,context TEXT,decision TEXT,expected_outcome TEXT,review_date TEXT,status TEXT DEFAULT 'Open',outcome TEXT,created_at TEXT,updated_at TEXT)")
                    con.execute("CREATE TABLE IF NOT EXISTS opportunity_radar (id INTEGER PRIMARY KEY AUTOINCREMENT,company_name TEXT,username TEXT,title TEXT,impact TEXT,evidence TEXT,action TEXT,created_at TEXT)")
                    con.execute("CREATE TABLE IF NOT EXISTS di_action_log (id INTEGER PRIMARY KEY AUTOINCREMENT,company_name TEXT,username TEXT,agent_name TEXT,action_type TEXT,request TEXT,result TEXT,created_at TEXT)")
                    for table, cols in {
                        "decision_ledger": {"company_name": "TEXT", "username": "TEXT", "title": "TEXT", "context": "TEXT", "decision": "TEXT", "expected_outcome": "TEXT", "review_date": "TEXT", "status": "TEXT DEFAULT 'Open'", "outcome": "TEXT", "created_at": "TEXT", "updated_at": "TEXT"},
                        "opportunity_radar": {"company_name": "TEXT", "username": "TEXT", "title": "TEXT", "impact": "TEXT", "evidence": "TEXT", "action": "TEXT", "created_at": "TEXT"},
                    }.items():
                        _ensure_columns(con, table, cols)
                    con.execute("UPDATE call_rooms SET mode='team' WHERE mode IS NULL OR TRIM(mode)=''")
                    con.execute("UPDATE call_participants SET participant_type='user' WHERE participant_type IS NULL OR TRIM(participant_type)=''")
                    con.execute("INSERT INTO dacre_schema_meta(key,value) VALUES('schema_version',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(_DB_SCHEMA_VERSION),))
                    con.commit()
            except Exception:
                try:
                    con.rollback()
                except Exception:
                    pass
                raise
            finally:
                con.close()

ensure_runtime_schema()

def ensure_di_agent_columns():
    """Safely upgrade older DACRE databases without duplicate-column errors."""
    con = db()
    try:
        existing = {row["name"] for row in con.execute("PRAGMA table_info(di_agents)").fetchall()}
        additions = {
            "avatar_url": "TEXT",
            "voice_profile": "TEXT",
            "thinking_style": "TEXT",
        }
        for column, dtype in additions.items():
            if column not in existing:
                con.execute(f"ALTER TABLE di_agents ADD COLUMN {column} {dtype}")
        con.commit()
    finally:
        con.close()

def seed_named_di_workforce():
    """Create/update the named English DI workforce."""
    roster = [
        ("Emiel", "Email & Messaging", "Prepare, organize and manage business email and messaging workflows.", "Polite, concise, organized and communication-focused.", "male", "https://i.pravatar.cc/160?img=12"),
        ("Oliver", "Data Analysis", "Inspect datasets, calculate metrics, find trends and produce analytical insights.", "Logical, numerical, evidence-first and precise.", "male", "https://i.pravatar.cc/160?img=13"),
        ("Sophie", "Research & Intelligence", "Research business, market and general information and summarize reliable findings.", "Curious, investigative, source-conscious and analytical.", "female", "https://i.pravatar.cc/160?img=47"),
        ("Daniel", "Data Entry & Processing", "Structure, clean, validate and process repetitive business data accurately.", "Careful, systematic, consistent and detail-oriented.", "male", "https://i.pravatar.cc/160?img=14"),
        ("Grace", "Business Intelligence", "Turn business data into KPIs, dashboards, executive insights and recommendations.", "Strategic, practical and outcome-focused.", "female", "https://i.pravatar.cc/160?img=44"),
        ("Henry", "Files & Documents", "Organize, inspect, summarize and manage business documents and files.", "Organized, careful and document-focused.", "male", "https://i.pravatar.cc/160?img=15"),
        ("James", "Security & Administration", "Support account administration, access controls, audit trails and system operations.", "Cautious, disciplined and security-first.", "male", "https://i.pravatar.cc/160?img=11"),
        ("Amelia", "Client Support & Communication", "Help users understand DACRE features and communicate business information clearly.", "Calm, respectful, patient and user-focused.", "female", "https://i.pravatar.cc/160?img=45"),
    ]
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        for name, specialty, role, style, voice, avatar in roster:
            row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (name,)).fetchone()
            if row:
                con.execute("""
                    UPDATE di_agents
                    SET specialty=?, system_role=?, avatar_url=?, voice_profile=?,
                        thinking_style=?, last_active=?
                    WHERE id=?
                """, (specialty, role, avatar, voice, style, now, row["id"]))
            else:
                code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")
                con.execute("""
                    INSERT INTO di_agents
                    (di_name, di_code, specialty, status, assigned_company,
                     system_role, avatar_url, voice_profile, thinking_style,
                     created_by, created_at, last_active)
                    VALUES (?, ?, ?, 'Available', NULL, ?, ?, ?, ?, ?, ?, ?)
                """, (name, code, specialty, role, avatar, voice, style,
                      MASTER_USERNAME, now, now))
        con.commit()
    finally:
        con.close()

ensure_di_agent_columns()
seed_named_di_workforce()

def get_di_agents():
    con = db()
    rows = con.execute("SELECT * FROM di_agents ORDER BY id DESC").fetchall()
    con.close()
    return rows

def create_di_agent(name, specialty, status="Available", assigned_company=None, system_role="", avatar_url="", voice_profile="male", thinking_style="", created_by="david"):
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")
    try:
        con.execute("""
            INSERT INTO di_agents
            (di_name, di_code, specialty, status, assigned_company,
             system_role, avatar_url, voice_profile, thinking_style,
             created_by, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, code, specialty, status, assigned_company, system_role, avatar_url, voice_profile, thinking_style, created_by, now, now))
        con.commit()
    finally:
        con.close()
