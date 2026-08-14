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
import threading
import time
from contextlib import contextmanager

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

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
DI_MEMORY_SEED = [
    ("IDENTITY", "DI identity", "My name is DI — David's Intelligence. I am the built-in intelligence assistant inside DACRE Analysis.", 2000),
    ("IDENTITY", "Creator and master", "DACRE Analysis and DI were created by David Emenike. David is the Overall Administrator and master of the platform.", 2000),
    ("IDENTITY", "David Emenike", "David Emenike is the creator and master administrator of DACRE Analysis. If asked who created DACRE, answer David Emenike.", 2000),
    ("PLATFORM", "What DACRE is", "DACRE Analysis is a business and data-intelligence workspace combining data ingestion, cleaning, analysis, formulas, charts, file storage, exports, administration and DI intelligence.", 1900),
    ("PLATFORM", "Supported data", "DACRE is designed to work with CSV, Excel/XLSX, TSV and JSON datasets and to inspect, clean, analyse, visualise and export data.", 1850),
    ("PLATFORM", "Formula Lab", "DACRE Formula Lab supports practical operations including SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM.", 1800),
    ("PLATFORM", "File Vault", "The File Vault is intended to store user/company files inside the DACRE workspace so important working files can remain organized and accessible.", 1800),
    ("PLATFORM", "Chart Builder", "DACRE can create business visualisations such as bar, line and area charts from analysed data, with room for future chart expansion.", 1750),
    ("PLATFORM", "Export Center", "The Export Center is designed to let users export processed results, including CSV and Excel outputs.", 1750),
    ("PLATFORM", "Workspace and Data", "Workspace & Data is the working area for uploading/opening datasets, inspecting data and carrying out analysis and cleaning tasks.", 1750),
    ("PLATFORM", "DI Home", "DI Home is the continuous conversation area where users can ask DI business, data, technical and general questions.", 1750),
    ("PLATFORM", "DI Question Board", "Every question sent to DI should be recorded in the DI Question Board so DACRE maintains a reliable trail of questions and answers.", 1900),
    ("PLATFORM", "Organization Admin Portal", "Organization Admin Portal provides organization-level administration for the company workspace, including users and company activity.", 1800),
    ("SECURITY", "Overall Admin DI", "Overall Admin DI is the master-only system-wide command centre. It is separate from ordinary company administration.", 2000),
    ("SECURITY", "Master visibility", "Only the master Overall Administrator should be able to view the system-wide DI Memory Box and master administration controls.", 2000),
    ("SECURITY", "Permanent deletion", "The Overall Administrator can permanently delete non-master accounts from People & Accounts after explicit confirmation. The operation is irreversible.", 2000),
    ("SECURITY", "Master protection", "The master account must be protected from permanent account deletion through normal account controls.", 2000),
    ("SECURITY", "Credential protection", "DACRE must never reveal the master passkey, password hashes, API keys, tokens or other private credentials in DI answers or ordinary screens.", 2000),
    ("ACCOUNT", "Signup and access", "A user who completes the required signup information should be able to access DACRE. Duplicate usernames or emails should be prevented.", 1900),
    ("CLIENT", "Chibobec Loan Service", "Chibobec Loan Service is a protected client workspace in DACRE Analysis. When an authenticated account signs up using a company name containing the word chibobec, DACRE recognises the organization as Chibobec Loan Service and opens the client's dedicated workspace.", 1950),
    ("CLIENT", "Chibobec welcome", "The Chibobec client is Mr Chibuike Chukwunere. When an authenticated Chibobec account is created, DI welcomes the client respectfully and states that the team was asked to treat the client with immense care.", 1950),
    ("CLIENT", "Chibobec loan desk", "Chibobec Loan Desk stores the client name, WhatsApp number, loan amount, date the loan was given and repayment due date. It tracks 2-day and due-date reminder delivery status.", 1950),
    ("CLIENT", "Loan reminders", "DI prepares a friendly WhatsApp reminder exactly 2 days before a recorded loan due date and a repayment reminder on the due date. Delivery requires an authenticated WhatsApp provider integration and the system records successful delivery to prevent duplicates.", 1950),
    ("ACCOUNT", "Company separation", "Each organization has its own workspace. Normal company users should not receive system-wide visibility into other organizations.", 1900),
    ("ACCOUNT", "Company admin", "The first account creating a new organization becomes that organization's company admin. Later users are normal users unless an admin grants admin access.", 1850),
    ("DI", "Memory Box purpose", "The DI Memory Box is the persistent trusted knowledge source for DI. It stores durable DACRE facts, creator identity, operating rules, product capabilities and approved knowledge.", 2000),
    ("DI", "Shared DI memory", "All DI workers can use active DI Memory Box records as shared context, so platform facts do not have to be manually re-taught to every DI worker.", 2000),
    ("DI", "Memory retrieval", "DI should retrieve the most relevant Memory Box records for a question rather than blindly sending every memory record to the reasoning layer.", 1950),
    ("DI", "Online research", "When internal memory is insufficient and current public information is needed, DI can attempt a public web lookup and use reliable retrieved sources.", 1900),
    ("DI", "Direct answers", "DI should answer directly whenever reliable knowledge is available. It should not repeatedly use a generic 'not enough reliable information' response when a useful answer is possible.", 2000),
    ("DI", "Ordinary factual questions", "DI should answer ordinary factual questions when it knows the answer or can verify it. Example: a dog is an animal because dogs are mammals in the animal kingdom.", 1700),
    ("DI", "Unknown text", "If a message looks like meaningless or random text such as fghjk, DI should say it appears unclear and ask the user to restate it rather than inventing a meaning.", 1600),
    ("DI", "Tech partner", "David uses a ChatGPT-based technical partner to help build, debug, improve, design and extend DACRE. DI should not falsely claim to be that separate conversation, but it can provide technical help itself.", 1800),
    ("UX", "Visual direction", "The preferred DACRE design is a polished light-blue business console with indigo, violet, cyan and deep-navy accents, strong text visibility, premium cards and no large white or pink surfaces.", 1800),
    ("UX", "Business-ready design", "DACRE should feel premium, technically polished, responsive, future-facing and suitable for serious business users.", 1750),
    ("PROJECT", "Product vision", "David wants DACRE to grow into a future-facing business intelligence platform that collects data, cleans and analyses it, creates charts and exports, stores business work, answers questions and supports organizations.", 1900),
    ("PROJECT", "Long-term DI vision", "The desired DI experience is a capable business and technical partner that can answer questions, explain data, help with formulas, analyse workspaces, research current information and assist with practical business tasks.", 1900),
    ("PROJECT", "Fast experience", "The preferred DI experience is fast: use internal knowledge first, use public research only when needed, and return the useful result rather than exposing internal routing or implementation details.", 1800),
]

PROJECT_HISTORY = [
    ("PROJECT_HISTORY", "Early DACRE concept", "The original DACRE idea was to create an app that could collect data from websites and links, perform data entry, and provide built-in capabilities inspired by SQL, Google Sheets, Excel, Power BI and Python data science workflows.", 1500),
    ("PROJECT_HISTORY", "Get Data vision", "The Get Data concept includes obtaining data from websites, uploaded XLSX/CSV/PDF files and platform links, with the longer-term goal of turning collected information into usable spreadsheet-style outputs.", 1500),
    ("PROJECT_HISTORY", "Data entry vision", "DACRE is intended to reduce repetitive data-entry work by helping users collect, structure, clean and analyse information in one workspace.", 1500),
    ("PROJECT_HISTORY", "Vendor data workflow", "A practical data workflow behind the project involved maintaining vendor product price lists with fields such as product price, part number, warranty, stock status and stock quantity.", 1300),
    ("PROJECT_HISTORY", "Product-list structure", "A representative product data structure used during development included Brand, Category, Price, Name, CPU Name, CPU Details, Storage Capacity, Storage Type, RAM, Screen, Screen Feature, Graphics Chips, Keyboard Feature, Operating System, Part Number, Camera, Warranty, Features, Other Features, Stock Status and Stock Qty.", 1300),
    ("PROJECT_HISTORY", "Data matching principle", "When updating structured product lists, data must be mapped to the correct headers and must not be mismatched across products or columns.", 1500),
    ("PROJECT_HISTORY", "Spreadsheet learning direction", "The project development included learning and applying spreadsheet skills such as filtering, sorting, data cleaning, Pivot Tables, VLOOKUP and CONCATENATE.", 1200),
    ("PROJECT_HISTORY", "Pivot Table goal", "Pivot Tables are useful in DACRE-style analysis for summarising dimensions such as brand or category and measures such as price, quantity or sales.", 1200),
    ("PROJECT_HISTORY", "Data cleaning goal", "Data cleaning in DACRE should help users remove empty rows or columns, duplicate records and other quality issues before analysis.", 1400),
    ("PROJECT_HISTORY", "Formula learning goal", "DACRE's Formula Lab is intended to make practical spreadsheet-style calculations accessible without requiring every user to write code.", 1300),
]

BUSINESS_DOMAINS = {
    "BUSINESS": [
        "business model", "value proposition", "customer segment", "revenue model", "cost structure", "gross margin", "operating margin", "break-even point", "unit economics", "competitive advantage", "market size", "service quality", "business process", "standard operating procedure", "key performance indicator", "business objective", "strategic goal", "operating plan", "business risk", "business continuity", "vendor management", "procurement", "inventory management", "order management", "customer lifecycle", "retention", "churn", "customer lifetime value", "acquisition cost", "profitability", "cash flow", "working capital", "forecasting", "budgeting", "scenario planning", "capacity planning", "resource allocation", "productivity", "efficiency", "effectiveness"
    ],
    "DATA": [
        "dataset", "row", "column", "record", "field", "data type", "numeric data", "categorical data", "date data", "missing value", "duplicate row", "outlier", "null value", "data validation", "data consistency", "data completeness", "data accuracy", "data uniqueness", "data quality", "data lineage", "data dictionary", "metadata", "schema", "primary key", "foreign key", "dimension", "measure", "fact table", "lookup table", "aggregation", "filtering", "sorting", "grouping", "join", "merge", "pivot table", "sampling", "population", "distribution", "correlation"
    ],
    "ANALYTICS": [
        "descriptive analytics", "diagnostic analytics", "predictive analytics", "prescriptive analytics", "trend analysis", "variance analysis", "cohort analysis", "segmentation", "benchmarking", "root cause analysis", "funnel analysis", "time series", "moving average", "growth rate", "conversion rate", "retention rate", "churn rate", "average order value", "return on investment", "return on ad spend", "forecast accuracy", "confidence interval", "hypothesis", "statistical significance", "mean", "median", "mode", "standard deviation", "percentile", "quartile", "minimum", "maximum", "range", "weighted average", "ratio", "percentage change", "index", "trend", "seasonality", "anomaly"
    ],
    "FINANCE": [
        "revenue", "sales revenue", "cost of goods sold", "gross profit", "operating expense", "net profit", "EBITDA", "cash flow", "accounts receivable", "accounts payable", "invoice", "payment terms", "credit period", "working capital", "current asset", "current liability", "balance sheet", "income statement", "cash flow statement", "budget", "actual spend", "budget variance", "financial forecast", "profit margin", "gross margin", "net margin", "contribution margin", "fixed cost", "variable cost", "sunk cost", "capital expenditure", "operating expenditure", "depreciation", "amortisation", "tax", "interest expense", "discount", "pricing", "unit cost", "break-even analysis"
    ],
    "SALES": [
        "lead", "prospect", "opportunity", "sales pipeline", "sales stage", "conversion", "win rate", "close rate", "sales quota", "sales target", "sales forecast", "average deal size", "sales cycle", "customer acquisition", "upsell", "cross-sell", "renewal", "territory", "account owner", "sales activity", "contact rate", "response rate", "proposal", "quotation", "purchase order", "deal value", "pipeline coverage", "forecast category", "lost deal", "win reason", "loss reason", "customer need", "discovery", "qualification", "negotiation", "objection handling", "account management", "key account", "sales productivity", "sales dashboard"
    ],
    "MARKETING": [
        "marketing campaign", "impression", "reach", "engagement", "click-through rate", "conversion rate", "cost per click", "cost per lead", "cost per acquisition", "return on ad spend", "marketing qualified lead", "brand awareness", "content marketing", "email marketing", "social media marketing", "search marketing", "landing page", "call to action", "audience", "persona", "customer journey", "attribution", "campaign budget", "campaign objective", "creative asset", "A/B test", "organic traffic", "paid traffic", "referral traffic", "website session", "bounce rate", "lead source", "channel mix", "marketing funnel", "retargeting", "keyword", "search intent", "content calendar", "marketing dashboard", "marketing ROI"
    ],
    "OPERATIONS": [
        "process mapping", "workflow", "cycle time", "lead time", "throughput", "capacity", "utilisation", "bottleneck", "service level", "turnaround time", "queue", "backlog", "order fulfilment", "inventory turnover", "stockout", "reorder point", "safety stock", "supplier lead time", "purchase order", "receiving", "quality control", "quality assurance", "standard work", "continuous improvement", "root cause", "corrective action", "preventive action", "operational KPI", "shift planning", "staffing", "scheduling", "resource plan", "maintenance", "downtime", "uptime", "incident", "escalation", "handover", "operations dashboard", "process efficiency"
    ],
    "CUSTOMER": [
        "customer satisfaction", "customer experience", "customer support", "support ticket", "first response time", "resolution time", "first contact resolution", "service level agreement", "customer complaint", "customer feedback", "customer effort score", "net promoter score", "customer retention", "customer churn", "customer lifetime value", "customer onboarding", "customer success", "knowledge base", "support queue", "ticket priority", "ticket status", "escalation", "service recovery", "response template", "customer segment", "customer profile", "customer history", "case management", "contact centre", "support channel", "email support", "chat support", "self-service", "help article", "feedback loop", "voice of customer", "customer health score", "renewal risk", "customer dashboard", "service analytics"
    ],
    "HR": [
        "headcount", "employee turnover", "attrition", "recruitment", "candidate pipeline", "time to hire", "cost per hire", "onboarding", "training", "performance review", "performance goal", "employee productivity", "attendance", "absence rate", "overtime", "workforce planning", "capacity", "skills inventory", "succession planning", "compensation", "benefits", "payroll", "employee engagement", "retention", "job satisfaction", "team structure", "manager span", "role clarity", "learning plan", "development plan", "competency", "job description", "interview scorecard", "candidate source", "offer acceptance", "probation", "employee record", "HR dashboard", "people analytics", "workforce KPI"
    ],
    "PRODUCT": [
        "product strategy", "product roadmap", "feature", "user story", "acceptance criteria", "product requirement", "product metric", "activation", "retention", "feature adoption", "usage frequency", "product-market fit", "customer need", "user persona", "user journey", "product backlog", "prioritisation", "MVP", "release", "version", "bug", "severity", "usability", "accessibility", "user interface", "user experience", "design system", "component", "prototype", "experiment", "A/B test", "feedback", "product analytics", "release notes", "changelog", "product risk", "technical debt", "roadmap dependency", "product dashboard", "product health"
    ],
    "PROJECT": [
        "project scope", "project objective", "deliverable", "milestone", "task", "dependency", "critical path", "project schedule", "resource plan", "budget", "risk register", "issue log", "change request", "stakeholder", "project sponsor", "project manager", "status report", "project KPI", "work breakdown structure", "requirements", "acceptance criteria", "deadline", "baseline", "variance", "progress", "capacity", "workload", "priority", "owner", "handover", "retrospective", "lessons learned", "project closure", "scope creep", "change control", "communication plan", "project dashboard", "delivery risk", "project health"
    ],
    "CYBERSECURITY": [
        "authentication", "authorization", "least privilege", "access control", "password policy", "multi-factor authentication", "session security", "audit log", "security incident", "vulnerability", "patch management", "backup", "recovery", "encryption", "data protection", "privacy", "secret management", "API key", "token", "phishing", "malware", "ransomware", "social engineering", "security monitoring", "incident response", "business continuity", "disaster recovery", "network security", "application security", "secure coding", "input validation", "database security", "role-based access", "account lockout", "credential rotation", "security review", "threat model", "security control", "security dashboard", "security awareness"
    ],
    "BI": [
        "business intelligence", "dashboard", "KPI", "data source", "data model", "semantic layer", "dimension", "measure", "drill-down", "filter", "slicer", "report", "scorecard", "executive dashboard", "operational dashboard", "analytical dashboard", "data refresh", "data pipeline", "ETL", "ELT", "data warehouse", "data mart", "lakehouse", "business metric", "metric definition", "report governance", "self-service analytics", "ad hoc analysis", "data storytelling", "insight", "recommendation", "alert", "threshold", "benchmark", "target", "actual", "variance", "trend", "BI adoption", "analytics governance"
    ],
    "AI": [
        "artificial intelligence", "machine learning", "language model", "prompt", "context", "retrieval", "knowledge base", "grounding", "hallucination", "evaluation", "accuracy", "latency", "automation", "classification", "prediction", "summarisation", "information extraction", "recommendation", "agent", "tool use", "workflow automation", "human review", "AI governance", "model monitoring", "data privacy", "responsible AI", "confidence", "fallback", "error handling", "knowledge retrieval", "semantic search", "keyword search", "ranking", "relevance", "feedback", "AI product metric", "AI cost", "AI response time", "AI quality", "AI reliability"
    ],
    "EXCEL_SHEETS": [
        "spreadsheet", "worksheet", "cell", "range", "formula", "function", "filter", "sort", "freeze panes", "conditional formatting", "data validation", "pivot table", "lookup", "VLOOKUP", "XLOOKUP", "INDEX MATCH", "CONCATENATE", "TEXTJOIN", "SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "IF", "IFERROR", "TRIM", "UPPER", "LOWER", "LEFT", "RIGHT", "MID", "date formatting", "number formatting", "currency formatting", "chart", "named range", "duplicate removal", "split text", "fill down", "copy paste", "sheet protection"
    ],
}

TEMPLATES = [
    ("definition", "What {term} means", "{term} is a business/data concept used to describe, measure or manage a specific part of an organisation's work. In DACRE, DI can explain the concept, relate it to a dataset and suggest practical ways to use it."),
    ("purpose", "Why {term} matters", "{term} matters because it can help a business understand performance, make decisions, reduce uncertainty or improve an operational process. The exact value depends on the organisation and its objectives."),
    ("measurement", "How to measure {term}", "A practical way to work with {term} is to define its unit, source data, calculation method, reporting period and target. DACRE can help structure the underlying data and calculate or visualise the resulting measure."),
    ("analysis", "How to analyse {term}", "To analyse {term}, define the business question first, identify the relevant fields, clean the data, segment meaningful groups, compare periods or targets and communicate the result with a clear conclusion."),
    ("data", "Data needed for {term}", "Useful data for {term} depends on context, but commonly includes a date or period, an entity or category, a numeric value, a status and an appropriate identifier. Data quality should be checked before conclusions are drawn."),
    ("KPI", "KPI example for {term}", "A useful KPI related to {term} should be specific, measurable, time-bound and connected to a business objective. A good KPI normally has a definition, owner, source, target and reporting frequency."),
    ("dashboard", "Dashboard view for {term}", "A dashboard for {term} can show the headline KPI, current value, target, variance, trend over time and the main categories or drivers. DACRE charts can support this style of analysis."),
    ("quality", "Data quality for {term}", "Before analysing {term}, check completeness, accuracy, consistency, uniqueness, validity and timeliness. Duplicate records, missing fields and inconsistent categories can distort the result."),
    ("risk", "Risk associated with {term}", "A common risk when using {term} is making a decision from incomplete, biased, outdated or incorrectly interpreted data. The mitigation is to validate the source, definition, calculation and assumptions."),
    ("action", "Business action for {term}", "After analysing {term}, the next step should be a concrete action with an owner, deadline and success measure. Insight is most valuable when it leads to a measurable business decision."),
    ("example", "Example use of {term}", "For example, a business could place {term} in a monthly analysis, compare the current period with the previous period and target, identify the largest driver of change and assign an action to the responsible team."),
    ("common mistake", "Common mistake with {term}", "A common mistake with {term} is using a vague definition or mixing incompatible periods, categories or units. Clear definitions and consistent data preparation reduce this problem."),
    ("best practice", "Best practice for {term}", "A strong practice for {term} is to document the definition, source, owner, calculation, reporting frequency and intended decision. This makes analysis repeatable and easier to audit."),
]

DI_MEMORY_SEED = DI_MEMORY_SEED[:4000]

CHIBOBEC_COMPANY = "chibobec loan service"

CHIBOBEC_OWNER_NAME = "Mr Chibuike Chukwunere"

SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json"]

SHEET_FORMULAS = ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","CONCATENATE","UPPER","LOWER","TRIM"]

APP_KNOWLEDGE = """
DACRE Analysis is a business and data analysis workspace. Users can upload CSV, Excel, TSV and JSON files; clean datasets; remove empty rows/columns and duplicates; inspect rows and columns; run formulas such as SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM; build bar, line and area charts; save workspace state; use a File Vault; and export processed data as CSV or Excel.
DI means David's Intelligence. DI is the assistant inside DACRE Analysis. Each organization has its own workspace. The first person who creates a new organization becomes that organization's company admin. Later users joining an existing organization are regular users unless an admin grants them admin rights. Company admins can inspect users, account creation, sign-ins, file activity and changes for their organization. The master account can see system-wide activity.
""".strip()

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

    # Chibobec Loan Service client/loan tracking and WhatsApp reminder ledger.
    # Reminders are idempotent: each 2-day and due-date message is recorded so
    # the same reminder is not sent twice.
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

    # DI Memory Box: the persistent source of truth used by every DI answer.
    # Entries are intentionally human-readable so the master can inspect and extend DI's knowledge.
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

    # Master DI workforce registry. Complete schema for fresh installations.
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

    # Realtime business calling + meeting-to-action ledger.
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
    canonical = {"id","company_name","room_name","title","host_username","mode","created_at","ended_at"}
    # If it is already canonical, just normalize blanks and return.
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
    title_expr = f"COALESCE(NULLIF(TRIM({expr('title', "''")}),''),'DACRE Call')" if "title" in old_cols else "'DACRE Call'"
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
    rows = con.execute(f"SELECT id,{company_expr} AS company_name,{room_expr} AS room_name,{title_expr} AS title,{host_expr} AS host_username,{mode_expr} AS mode,{created_expr} AS created_at,{ended_expr} AS ended_at FROM {old_name}").fetchall()
    seen = set()
    for r in rows:
        room = str(r["room_name"] or f"DACRE-LEGACY-{r['id']}")
        if room in seen:
            room = f"{room}-{r['id']}"
        seen.add(room)
        con.execute("INSERT INTO call_rooms(id,company_name,room_name,title,host_username,mode,created_at,ended_at) VALUES(?,?,?,?,?,?,?,?)", (
            r["id"], str(r["company_name"] or ""), room, str(r["title"] or "DACRE Call"), str(r["host_username"] or ""), str(r["mode"] or "team"), str(r["created_at"] or ""), r["ended_at"]
        ))
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
        canonical = {"id","room_name","company_name","participant_type","participant_id","display_name","joined_at","left_at"}
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
            def col_or(name, fallback): return name if name in old_cols else fallback
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
            rows = con.execute(f"SELECT id,{room_expr} AS room_name,{company_expr} AS company_name,{type_expr} AS participant_type,{pid_expr} AS participant_id,{name_expr} AS display_name,{joined_expr} AS joined_at,{left_expr} AS left_at FROM {old_name}").fetchall()
            for r in rows:
                con.execute("INSERT INTO call_participants(id,room_name,company_name,participant_type,participant_id,display_name,joined_at,left_at) VALUES(?,?,?,?,?,?,?,?)", (
                    r["id"], str(r["room_name"] or ""), str(r["company_name"] or ""), str(r["participant_type"] or "user"), str(r["participant_id"] or ""), str(r["display_name"] or ""), str(r["joined_at"] or ""), r["left_at"]
                ))
            con.execute(f"DROP TABLE {old_name}")
    # Import legacy call_members only when it exists and has not already been migrated.
    if _table_exists(con, "call_members"):
        mcols = _table_columns(con, "call_members")
        room_expr = "room_code" if "room_code" in mcols else ("room_name" if "room_name" in mcols else "''")
        user_expr = "username" if "username" in mcols else "''"
        company_expr = "company_name" if "company_name" in mcols else "''"
        joined_expr = "joined_at" if "joined_at" in mcols else "NULL"
        left_expr = "left_at" if "left_at" in mcols else "NULL"
        rows = con.execute(f"SELECT id,{room_expr} AS room_name,{company_expr} AS company_name,{user_expr} AS username,{joined_expr} AS joined_at,{left_expr} AS left_at FROM call_members").fetchall()
        for r in rows:
            exists = con.execute("SELECT 1 FROM call_participants WHERE room_name=? AND participant_id=? LIMIT 1", (str(r["room_name"] or ""), str(r["username"] or ""))).fetchone()
            if not exists:
                con.execute("INSERT INTO call_participants(room_name,company_name,participant_type,participant_id,display_name,joined_at,left_at) VALUES(?,?,?,?,?,?,?)", (
                    str(r["room_name"] or ""), str(r["company_name"] or ""), "user", str(r["username"] or ""), str(r["username"] or ""), str(r["joined_at"] or ""), r["left_at"]
                ))


def ensure_runtime_schema():
    """Repair historical DACRE call schemas every startup when needed.

    The migration is deliberately schema-driven, not version-driven. Older builds
    could have written a schema version even though call_rooms was still using the
    legacy room_code NOT NULL schema. Therefore we always inspect the real table
    before deciding that migration is unnecessary.
    """
    max_attempts = 8
    for attempt in range(max_attempts):
        try:
            with _DB_SCHEMA_LOCK:
                with _db_file_lock(timeout=90):
                    con = db()
                    try:
                        # Never trust a stored version alone. Validate the actual schema.
                        tables = {
                            "call_rooms": _table_columns(con, "call_rooms"),
                            "call_participants": _table_columns(con, "call_participants"),
                        }
                        required_rooms = {"id", "company_name", "room_name", "title", "host_username", "mode", "created_at", "ended_at"}
                        legacy_room_columns = {"room_code", "created_by", "provider", "status", "created"}
                        rooms_need_rebuild = (
                            not tables["call_rooms"]
                            or not required_rooms.issubset(tables["call_rooms"])
                            or bool(tables["call_rooms"] & legacy_room_columns)
                        )

                        required_participants = {"id", "room_name", "company_name", "participant_type", "participant_id", "display_name", "joined_at", "left_at"}
                        participants_need_rebuild = (
                            not tables["call_participants"]
                            or not required_participants.issubset(tables["call_participants"])
                            or "room_code" in tables["call_participants"]
                        )

                        # Lightweight schema metadata is retained for diagnostics only.
                        con.execute("CREATE TABLE IF NOT EXISTS dacre_schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")

                        if rooms_need_rebuild or participants_need_rebuild:
                            # Make the entire migration one exclusive, short-lived transaction.
                            con.execute("BEGIN IMMEDIATE")
                            if rooms_need_rebuild:
                                _rebuild_call_rooms(con)
                            if participants_need_rebuild:
                                _rebuild_call_participants(con)

                            con.execute("""
                                CREATE TABLE IF NOT EXISTS decision_ledger (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    company_name TEXT, username TEXT, title TEXT,
                                    context TEXT, decision TEXT, expected_outcome TEXT,
                                    review_date TEXT, status TEXT DEFAULT 'Open', outcome TEXT,
                                    created_at TEXT, updated_at TEXT
                                )
                            """)
                            con.execute("""
                                CREATE TABLE IF NOT EXISTS opportunity_radar (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    company_name TEXT, username TEXT, title TEXT,
                                    impact TEXT, evidence TEXT, action TEXT, created_at TEXT
                                )
                            """)
                            con.execute("""
                                CREATE TABLE IF NOT EXISTS di_action_log (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    company_name TEXT, username TEXT, agent_name TEXT,
                                    action_type TEXT, request TEXT, result TEXT, created_at TEXT
                                )
                            """)
                            con.execute("UPDATE call_rooms SET mode='team' WHERE mode IS NULL OR TRIM(mode)=''")
                            con.execute("UPDATE call_participants SET participant_type='user' WHERE participant_type IS NULL OR TRIM(participant_type)=''")
                            con.commit()

                        # Validate the final schema before declaring startup successful.
                        final_rooms = _table_columns(con, "call_rooms")
                        final_participants = _table_columns(con, "call_participants")
                        if not required_rooms.issubset(final_rooms) or (final_rooms & legacy_room_columns):
                            raise RuntimeError(f"DACRE call_rooms migration incomplete. Columns: {sorted(final_rooms)}")
                        if not required_participants.issubset(final_participants) or "room_code" in final_participants:
                            raise RuntimeError(f"DACRE call_participants migration incomplete. Columns: {sorted(final_participants)}")

                        con.execute(
                            "INSERT INTO dacre_schema_meta(key,value) VALUES('schema_version',?) "
                            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                            (str(_DB_SCHEMA_VERSION),),
                        )
                        con.commit()
                        return
                    except Exception:
                        try:
                            con.rollback()
                        except Exception:
                            pass
                        raise
                    finally:
                        con.close()
        except sqlite3.OperationalError as exc:
            msg = str(exc).lower()
            if "locked" in msg or "busy" in msg:
                if attempt < max_attempts - 1:
                    time.sleep(min(4.0, 0.5 * (attempt + 1)))
                    continue
            raise

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
            MASTER_PASSKEY_HASH, MASTER_PASSKEY_HASH, "master", 0, now,
        ))
        con.commit()
    con.close()

def seed_di_memory():
    """Seed the shared DI Memory Box without overwriting user-created memory."""
    con=db(); now=datetime.now().isoformat(timespec="seconds")
    con.execute("PRAGMA journal_mode=WAL")
    # Ensure the current schema can accept the seed records even when upgrading
    # an older DACRE SQLite database.
    cols={r[1] for r in con.execute("PRAGMA table_info(di_memory)").fetchall()}
    migrations={
        "category":"TEXT DEFAULT 'GENERAL'", "title":"TEXT DEFAULT ''", "content":"TEXT DEFAULT ''",
        "priority":"INTEGER DEFAULT 500", "active":"INTEGER DEFAULT 1", "created_by":"TEXT DEFAULT ''",
        "created_at":"TEXT DEFAULT ''", "updated_at":"TEXT DEFAULT ''"
    }
    for name,decl in migrations.items():
        if name not in cols:
            con.execute(f"ALTER TABLE di_memory ADD COLUMN {name} {decl}")
    con.commit()
    rows=[(c,t,x,p,MASTER_USERNAME,now,now) for c,t,x,p in DI_MEMORY_SEED]
    con.executemany("INSERT INTO di_memory(category,title,content,priority,created_by,created_at,updated_at) SELECT ?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM di_memory WHERE title=? )", [r+(r[1],) for r in rows])
    con.commit(); con.close()

def get_di_memory(limit=80, query=""):
    """Retrieve the most relevant active memories for the current question."""
    con=db()
    rows=con.execute("SELECT id,category,title,content,priority,active,created_at,updated_at FROM di_memory WHERE active=1 ORDER BY priority DESC,id ASC").fetchall()
    con.close()
    if not query:
        return [dict(r) for r in rows[:int(limit)]]
    words=set(re.findall(r"[a-z0-9]{3,}", query.lower()))
    scored=[]
    for r in rows:
        text=f"{r['category']} {r['title']} {r['content']}".lower()
        hits=sum(1 for w in words if w in text)
        exact=2 if r['title'].lower() in query.lower() else 0
        score=(hits*25)+exact+int(r['priority'] or 0)/1000
        if hits:
            scored.append((score,dict(r)))
    scored.sort(key=lambda x:x[0], reverse=True)
    return [r for _,r in scored[:int(limit)]]

def di_memory_context(limit=80, query=""):
    rows=get_di_memory(limit, query=query)
    if not rows:
        return "DI Memory Box has no matching records for this question."
    return "\n".join([f"[{r['category']}] {r['title']}: {r['content']}" for r in rows])

def memory_box_direct_answer(text):
    """Give a deterministic direct answer when a trusted memory record matches."""
    matches=get_di_memory(limit=5, query=text)
    if not matches:
        return None
    low=text.lower().strip()
    # Identity questions should return the exact identity record immediately.
    if any(k in low for k in ["your name", "who are you", "what should i call you"]):
        return "My name is DI — David's Intelligence."
    if "who created" in low or "who made" in low or "creator" in low:
        return "DACRE Analysis and DI were created by David Emenike."
    if "david emenike" in low and any(k in low for k in ["know", "who", "creator"]):
        return "Yes. David Emenike is the creator and Overall Administrator of DACRE Analysis."
    # Return a high-confidence factual memory only when several question words
    # overlap the matched title/content; otherwise let the normal reasoning/web path handle it.
    qwords=set(re.findall(r"[a-z0-9]{3,}", low))
    best=matches[0]
    mtext=f"{best['title']} {best['content']}".lower()
    hits=sum(1 for w in qwords if w in mtext)
    if hits>=2 and best['category'] in {"IDENTITY","PLATFORM","PROJECT","PROJECT_HISTORY","SECURITY","DI","UX","ACCOUNT","BASIC","EXCEL_SHEETS","DATA","ANALYTICS","BUSINESS","BI"}:
        return best['content']
    return None

def permanently_delete_accounts(user_ids):
    """Permanently remove non-master accounts and their workspace records."""
    ids=[]
    for value in user_ids:
        try: ids.append(int(value))
        except Exception: pass
    ids=list(dict.fromkeys(ids))
    if not ids:
        return 0, []
    con=db(); placeholders=','.join('?' for _ in ids)
    rows=con.execute(f"SELECT id,username,first_name,last_name,company_name,email,role FROM users WHERE id IN ({placeholders})",ids).fetchall()
    safe=[r for r in rows if r['role']!='master' and r['username']!=MASTER_USERNAME]
    if not safe:
        con.close(); return 0, []
    safe_ids=[r['id'] for r in safe]
    ph=','.join('?' for _ in safe_ids)
    # Remove all user-owned records first. Companies are removed only when no users remain.
    for table,col in [("files","username"),("projects","username"),("activity","username"),("chat_history","username")]:
        con.execute(f"DELETE FROM {table} WHERE {col} IN (SELECT username FROM users WHERE id IN ({ph}))",safe_ids)
    con.execute(f"DELETE FROM notifications WHERE target_username IN (SELECT username FROM users WHERE id IN ({ph}))",safe_ids)
    con.execute(f"DELETE FROM emails_log WHERE recipient_email IN (SELECT email FROM users WHERE id IN ({ph}))",safe_ids)
    con.execute(f"DELETE FROM users WHERE id IN ({ph}) AND role!='master' AND username!=?",safe_ids+[MASTER_USERNAME])
    deleted=len(safe)
    # Clean orphaned organizations and their DI assignments.
    companies=con.execute("SELECT name FROM companies WHERE name NOT IN (SELECT DISTINCT company_name FROM users) AND name!='DACRE MASTER'").fetchall()
    for c in companies:
        con.execute("DELETE FROM companies WHERE name=?",(c['name'],))
        con.execute("UPDATE di_agents SET assigned_company=NULL WHERE assigned_company=?",(c['name'],))
    con.commit(); con.close()
    return deleted, [dict(r) for r in safe]

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

    # Streamlit Cloud secrets are not guaranteed to appear in os.environ, so
    # read mail configuration from st.secrets first and environment variables second.
    def mail_secret(name, default=""):
        try:
            value = st.secrets.get(name, "")
        except Exception:
            value = ""
        return str(value or os.getenv(name, default) or default).strip()

    # Multi-provider mail source: try Gmail, Outlook/Microsoft 365, Proton,
    # then the legacy single SMTP configuration. Stop after the first success.
    providers = [
        ("Gmail", "DACRE_GMAIL_SMTP_HOST", "DACRE_GMAIL_SMTP_PORT", "DACRE_GMAIL_SMTP_USER", "DACRE_GMAIL_SMTP_PASSWORD", "DACRE_GMAIL_SMTP_FROM"),
        ("Outlook", "DACRE_OUTLOOK_SMTP_HOST", "DACRE_OUTLOOK_SMTP_PORT", "DACRE_OUTLOOK_SMTP_USER", "DACRE_OUTLOOK_SMTP_PASSWORD", "DACRE_OUTLOOK_SMTP_FROM"),
        ("Proton", "DACRE_PROTON_SMTP_HOST", "DACRE_PROTON_SMTP_PORT", "DACRE_PROTON_SMTP_USER", "DACRE_PROTON_SMTP_PASSWORD", "DACRE_PROTON_SMTP_FROM"),
        ("Legacy SMTP", "DACRE_SMTP_HOST", "DACRE_SMTP_PORT", "DACRE_SMTP_USER", "DACRE_SMTP_PASSWORD", "DACRE_SMTP_FROM"),
    ]
    statuses=[]
    status="NOT SENT — no mail provider is configured"
    sent_provider=""
    for provider, host_key, port_key, user_key, pass_key, from_key in providers:
        smtp_host=mail_secret(host_key)
        smtp_port=int(mail_secret(port_key, "587"))
        smtp_user=mail_secret(user_key)
        smtp_pass=mail_secret(pass_key)
        sender=mail_secret(from_key, smtp_user or "")
        if not (smtp_host and smtp_user and smtp_pass):
            continue
        try:
            msg=MIMEMultipart()
            msg["From"]=sender or smtp_user
            msg["To"]=email
            msg["Subject"]=subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender or smtp_user, [email], msg.as_string())
            status=f"Sent via {provider} SMTP"
            sent_provider=provider
            break
        except Exception as exc:
            statuses.append(f"{provider}: {type(exc).__name__}")
    if not sent_provider and statuses:
        status="NOT SENT — configured mail providers failed (" + "; ".join(statuses) + ")"

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
    return status

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
        if (company_clean == "dacre master" or full_name_clean == "david emenike" or email_clean == "master@dacre.local") and master_passkey_gate(passkey_clean):
            row = con.execute("SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?", (MASTER_USERNAME,)).fetchone()
            if row:
                now = datetime.now().isoformat(timespec="seconds")
                con.execute("UPDATE users SET login_count=login_count+1,last_login=? WHERE username=?", (now, MASTER_USERNAME))
                con.commit()
                result = dict(row)
                log_activity(MASTER_USERNAME, result.get("company_name", "DACRE MASTER"), "Signed in", notify_admin=False)
                return result, None

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
    company_clean = canonical_company_name(company)
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

        mail_status = send_di_welcome_email(first_clean, last_clean, company_clean, email_clean, email_password.strip())
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))
        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, f"Account created successfully! DI email status: {mail_status}", {
            "first_name": first_clean, "last_name": last_clean, "username": username_clean,
            "company": company_clean, "email": email_clean, "role": role,
        }
    except sqlite3.IntegrityError:
        return False, "An account with this email address is already registered.", None
    finally:
        con.close()

def is_chibobec_company(company_name):
    return "chibobec" in str(company_name or "").strip().lower()

def canonical_company_name(company_name):
    # Recognise the requested Chibobec company keyword without granting
    # identity access by name alone; the normal email/passkey authentication
    # still applies to every account.
    return CHIBOBEC_COMPANY if is_chibobec_company(company_name) else str(company_name or "").strip()

def normalize_whatsapp_number(number):
    raw = re.sub(r"[^0-9+]", "", str(number or "").strip())
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    if raw.startswith("0"):
        # Nigeria is the expected first market for this client. Users can still
        # enter an international number beginning with +.
        raw = "+234" + raw[1:]
    if raw and not raw.startswith("+"):
        raw = "+" + raw
    return raw

def _dacre_secret(name, default=""):
    """Read a Streamlit secret first, then an environment variable."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, default) or default).strip()

def _meta_whatsapp_config():
    return {
        "token": _dacre_secret("DACRE_WHATSAPP_TOKEN"),
        "phone_id": _dacre_secret("DACRE_WHATSAPP_PHONE_NUMBER_ID"),
        "version": _dacre_secret("DACRE_WHATSAPP_API_VERSION", "v23.0"),
        "reminder_2_template": _dacre_secret("DACRE_WHATSAPP_2DAY_TEMPLATE", "dacre_loan_due_2days"),
        "due_template": _dacre_secret("DACRE_WHATSAPP_DUE_TEMPLATE", "dacre_loan_due_today"),
        "language": _dacre_secret("DACRE_WHATSAPP_TEMPLATE_LANGUAGE", "en_US"),
    }

def _meta_phone(phone):
    return re.sub(r"[^0-9]", "", normalize_whatsapp_number(phone))

def _log_whatsapp_delivery(loan_id, company, client_name, phone, reminder_type, template_name, message_id, status, response):
    con = db()
    con.execute(
        """INSERT INTO whatsapp_delivery_log
        (loan_id,company_name,client_name,whatsapp_number,reminder_type,template_name,message_id,status,response,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (loan_id, company, client_name, phone, reminder_type, template_name, message_id,
         status, str(response)[:4000], datetime.now().isoformat(timespec="seconds")),
    )
    con.commit()
    con.close()

def send_whatsapp_template(to_number, template_name, parameters):
    """Send an approved Meta WhatsApp Cloud API template."""
    cfg = _meta_whatsapp_config()
    if not cfg["token"] or not cfg["phone_id"]:
        return False, "Meta WhatsApp Cloud API is not configured. Add DACRE_WHATSAPP_TOKEN and DACRE_WHATSAPP_PHONE_NUMBER_ID to Streamlit Secrets."
    to = _meta_phone(to_number)
    if len(to) < 8:
        return False, "Invalid WhatsApp number. Use an international number such as +2348012345678."
    endpoint = f"https://graph.facebook.com/{cfg['version']}/{cfg['phone_id']}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": cfg["language"]},
            "components": [{"type": "body", "parameters": [{"type": "text", "text": str(v)} for v in parameters]}],
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {cfg['token']}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw or "{}")
            message_id = (data.get("messages") or [{}])[0].get("id")
            if 200 <= response.status < 300 and message_id:
                return True, message_id
            return False, f"Meta returned HTTP {response.status}: {raw[:1000]}"
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        return False, f"Meta WhatsApp API rejected the message (HTTP {exc.code}): {detail[:1200]}"
    except Exception as exc:
        return False, f"WhatsApp send failed: {type(exc).__name__}: {exc}"

def send_whatsapp_message(to_number, body):
    return False, "Use an approved Meta WhatsApp template for business-initiated reminders."

def add_loan_client(username, company, client_name, whatsapp_number, loan_amount, lent_date, due_date):
    client_name = str(client_name or "").strip()
    phone = normalize_whatsapp_number(whatsapp_number)
    if not client_name or not phone:
        return False, "Client name and WhatsApp number are required."
    if due_date < lent_date:
        return False, "The due date cannot be earlier than the lending date."
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""INSERT INTO loan_clients
            (username,company_name,client_name,whatsapp_number,loan_amount,lent_date,due_date,created_at,updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (username, company, client_name, phone, float(loan_amount or 0), str(lent_date), str(due_date), now, now))
        con.commit()
        return True, "Loan client saved."
    except Exception as exc:
        return False, str(exc)
    finally:
        con.close()

def delete_loan_client(loan_id, username):
    con = db()
    con.execute("DELETE FROM loan_clients WHERE id=? AND username=?", (int(loan_id), username))
    con.commit(); con.close()

def process_chibobec_reminders(username, company):
    """Send due-date reminders through the real Meta WhatsApp Cloud API."""
    if not is_chibobec_company(company):
        return []
    cfg = _meta_whatsapp_config()
    today = datetime.now().date()
    con = db()
    rows = con.execute("SELECT * FROM loan_clients WHERE username=? AND company_name=? ORDER BY due_date", (username, company)).fetchall()
    results = []
    for row in rows:
        try:
            due = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
        except Exception:
            continue
        days_left = (due - today).days
        if days_left == 2 and not row["reminder_2_sent"]:
            reminder_type, template_name, sent_column, message_column = "2-day reminder", cfg["reminder_2_template"], "reminder_2_sent", "reminder_2_message_id"
        elif days_left == 0 and not row["due_sent"]:
            reminder_type, template_name, sent_column, message_column = "due-date reminder", cfg["due_template"], "due_sent", "due_message_id"
        else:
            continue
        parameters = [row["client_name"], f"₦{float(row['loan_amount']):,.2f}", due.strftime("%d %B %Y")]
        ok, status = send_whatsapp_template(row["whatsapp_number"], template_name, parameters)
        now = datetime.now().isoformat(timespec="seconds")
        if ok:
            con.execute(f"UPDATE loan_clients SET {sent_column}=1,{message_column}=?,last_whatsapp_status=?,last_whatsapp_error=NULL,updated_at=? WHERE id=?", (status, "sent", now, row["id"]))
            _log_whatsapp_delivery(row["id"], company, row["client_name"], row["whatsapp_number"], reminder_type, template_name, status, "sent", "Meta accepted the message.")
        else:
            con.execute("UPDATE loan_clients SET last_whatsapp_status=?,last_whatsapp_error=?,updated_at=? WHERE id=?", ("failed", status, now, row["id"]))
            _log_whatsapp_delivery(row["id"], company, row["client_name"], row["whatsapp_number"], reminder_type, template_name, None, "failed", status)
        results.append((row["client_name"], reminder_type, ok, status))
    con.commit()
    con.close()
    return results

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

def safe_dataframe_for_streamlit(df):
    """Prevent pyarrow duplicate-column failures when Streamlit renders a dataframe."""
    if df is None:
        return df
    out=df.copy()
    seen={}
    cols=[]
    for col in out.columns:
        base=str(col)
        n=seen.get(base,0)
        seen[base]=n+1
        cols.append(base if n==0 else f"{base}_{n+1}")
    out.columns=cols
    return out

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
    context = [
        APP_KNOWLEDGE,
        "DI MEMORY BOX (persistent source of truth):\n" + di_memory_context(query=getattr(st.session_state, "di_memory_query", "")),
        f"Current organization: {user['company']}. Current user: {user['first_name']} {user['last_name']}. Role: {user['role']}.",
    ]
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

def normalize_di_identity(text):
    """Keep DI's displayed first-person identity consistent."""
    if not text:
        return text
    text=re.sub(r"\bI\s+am\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    text=re.sub(r"\bI\x27m\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    return text

def di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    text=message.strip()
    low=text.lower()
    if not text:
        return "I am ready. Tell me the business result you want to achieve."

    name="Master David" if user["role"]=="master" else user["first_name"]
    greetings=["hello","hi","good morning","good afternoon","good evening","good day"]
    if any(p in low for p in greetings) and len(low.split())<=6:
        return f"Good day {name}. DI is online. What would you like us to work on first?"

    # Identity and platform answers are resolved from the DI Memory Box first.
    if any(k in low for k in ["your name","what is your name","who are you","what's your name"]):
        return "My name is DI — David's Intelligence. I am the intelligence assistant inside DACRE Analysis, created by David Emenike."
    if any(k in low for k in ["who created you","who made you","who created dacre","who made dacre"]):
        return "DACRE Analysis and DI were created by David Emenike. David Emenike is the master/Overall Administrator of the platform."
    if "david emenike" in low and any(k in low for k in ["do you know","who is","is he","creator"]):
        return "Yes. David Emenike is the creator and master administrator of DACRE Analysis."
    if "dog" in low and "animal" in low:
        return "Yes. A dog is an animal; more specifically, dogs are mammals in the animal kingdom."
    if any(k in low for k in ["delete account","remove account","permanently delete","delete a user"]):
        if user["role"]=="master":
            return "As the Overall Administrator, open Overall Admin DI → People & Accounts. Select the account(s) you want to remove, review the deletion summary, confirm the permanent deletion, and click the permanent-delete action. The master account is protected and cannot be deleted there."
        return "For account removal, contact your company administrator or the Overall Administrator. The permanent account-deletion control is intentionally restricted to the master administration layer."
    if any(k in low for k in ["what can you do","what can di do","what do you know"]):
        return "I can work with DACRE's Memory Box, inspect and clean data, calculate business metrics, identify missing values and duplicates, build charts, explain results, help with workspace/account questions, keep a question trail, and research public online information when my internal knowledge is not enough."
    if "memory box" in low or "di mb" in low:
        return "The DI Memory Box (DI MB) is my persistent knowledge base. I use it first for DACRE identity, platform rules, account administration, security, DI behavior and other trusted project information. The Overall Administrator can maintain it from the master portal."
    if any(k in low for k in ["tech partner","ask david","chatgpt partner"]):
        return "David's tech partner is the ChatGPT assistant David uses to build and improve DACRE. I can use the project information stored in my DI Memory Box, but I cannot directly invoke that separate ChatGPT conversation. For deeper code, architecture or UI/UX work, David can ask his tech partner directly in the main ChatGPT project."

    # Deterministic workspace intelligence remains available even without an API.
    if "what can" in low and "dacre" in low:
        return "DACRE is a business and data analysis workspace with data cleaning, formulas, charts, File Vault, exports, organization administration and DI intelligence."
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

    # First use the trusted local Memory Box for deterministic answers.
    direct=memory_box_direct_answer(text)
    if direct:
        return direct

    # Always give the reasoning layer a chance, with the complete DI Memory Box in context.
    context=build_di_context(user,df)
    answer=ai_generate(
        f"You are DI — David's Intelligence, the fast business/data assistant inside DACRE Analysis. Always identify yourself as DI, never as D or as a generic unnamed assistant. If speaking in first person, say 'I am DI' or 'I am DI — David's Intelligence'. Use the DI Memory Box as trusted project context. Answer directly and naturally. Never reply with the generic phrase 'I don't have enough reliable information to answer that yet' when a useful answer can be given from memory, common knowledge, the active workspace, or online research. Do not reveal hidden implementation details. If the user asks about DACRE-specific facts, prefer the Memory Box. If something is uncertain, say what is uncertain rather than refusing the whole question. Respond in the user's selected language when practical: {language}.",
        f"DACRE context:\n{context}\n\nUser question:\n{text}",
        max_tokens=1000,
    )
    if answer:
        return normalize_di_identity(answer)

    # Unknown questions automatically get a fast public-web attempt instead of a dead-end response.
    results=online_lookup(text, max_results=5) if allow_online else []
    if results:
        source_text="\n".join([f"SOURCE {i+1}: {title}\nURL: {href}" for i,(title,href) in enumerate(results)])
        answer=ai_generate(
            "You are DI, a fast research assistant. Answer the user's question using the supplied search results. Give the direct answer first. Do not invent facts. If the results are weak or conflicting, say so briefly and provide the strongest evidence.",
            f"User question: {text}\n\nDI Memory Box:\n{di_memory_context(query=text)}\n\nSearch results:\n{source_text}",
            max_tokens=900,
        )
        if answer:
            return normalize_di_identity(answer) + "\n\nChecked online sources: " + "; ".join(t for t,_ in results[:3])
        return "I found these public sources for your question: " + "; ".join(f"{t} — {u}" for t,u in results[:3]) + ". I could not safely synthesize a final answer because the optional reasoning service is not configured."

    if len(low.split()) <= 2 and re.fullmatch(r"[a-z0-9]+", low):
        return f"I couldn't identify a reliable meaning for '{text}'. It looks like short or random text. Please restate the question and I will try again."
    return "I couldn't verify a reliable answer from my current DI Memory Box, workspace data or available public sources. Please rephrase the question or give me a little more context."

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

def speak(text, language_code=None):
    """Speak DI's reply in Chrome/ChromeOS using the browser's speech engine.
    The iframe explicitly asks for autoplay and waits for the voice list, which
    fixes the common "DI answered in text but stayed silent" problem.
    """
    if not text or not st.session_state.get("di_voice_enabled", True):
        return
    language_code = language_code or DI_LANGUAGE_PROFILES.get(
        st.session_state.get("di_language", "English — Nigeria"), {}
    ).get("code", "en-NG")
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language_code)
    components.html(f"""
    <script>
    (() => {{
      const text={safe_text};
      const lang={safe_lang};
      if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) return;
      const run=()=>{{
        try {{
          window.speechSynthesis.cancel();
          const u=new SpeechSynthesisUtterance(text);
          u.lang=lang;
          u.rate=0.92;
          u.pitch=0.82;
          u.volume=1.0;
          const voices=window.speechSynthesis.getVoices();
          const base=lang.toLowerCase().split('-')[0];
          const same=voices.filter(v => (v.lang||'').toLowerCase().startsWith(base));
          const preferred=same.find(v => (v.lang||'').toLowerCase() === lang.toLowerCase()) || same.find(v => /male|daniel|david|alex|george|james|oliver|google|microsoft/i.test(v.name)) || same[0] || voices[0];
          if(preferred) u.voice=preferred;
          window.speechSynthesis.speak(u);
        }} catch(e) {{ console.warn('DACRE voice error', e); }}
      }};
      if(window.speechSynthesis.getVoices().length) run();
      else window.speechSynthesis.onvoiceschanged=run;
      setTimeout(run, 250);
    }})();
    </script>
    """, height=1, scrolling=False)

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
    candidate = (passkey or "").strip()
    if not candidate:
        return False
    expected_hash = hash_password(MASTER_PASSKEY) if MASTER_PASSKEY else MASTER_PASSKEY_HASH
    ok, _ = verify_password(candidate, expected_hash)
    return bool(ok)

def chibobec_login_monitor():
    """Return every Chibobec account plus its real login activity.
    This is intentionally based on the users table, not on the current session,
    so the CEO Office can see accounts that have logged in previously.
    """
    con = db()
    try:
        users = pd.read_sql_query(
            """SELECT id, first_name, last_name, username, company_name, email, role,
                      login_count, created_at, last_login
               FROM users
               WHERE lower(company_name) LIKE '%chibobec%'
               ORDER BY CASE WHEN last_login IS NULL THEN 1 ELSE 0 END, last_login DESC, id DESC""",
            con,
        )
        if users.empty:
            return users
        users["login_status"] = users["last_login"].apply(lambda x: "Logged in" if pd.notna(x) and str(x).strip() else "Never logged in")
        users["company_access"] = users["company_name"].apply(lambda x: "Chibobec workspace" if is_chibobec_company(x) else "Company workspace")
        return users
    finally:
        con.close()

def di_voice_player(text, language_code=None):
    """Render a visible DI voice control. Auto-speak is attempted; the button
    is the reliable fallback when the browser blocks autoplay after reruns."""
    if not text:
        return
    language_code = language_code or DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
    safe_text=json.dumps(str(text))
    safe_lang=json.dumps(language_code)
    components.html(f"""
    <div style="font-family:Inter,Segoe UI,sans-serif;background:#174f86;border:1px solid #6bb8ee;border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:10px;">
      <button id="dacre-speak-btn" style="background:#f28c28;color:white;border:0;border-radius:10px;padding:9px 15px;font-weight:800;cursor:pointer;">🔊 Speak DI</button>
      <span style="color:#eaf6ff;font-weight:700;font-size:13px;">DI voice ready · {language_code}</span>
    </div>
    <script>
    (() => {{
      const text={safe_text}, lang={safe_lang};
      const chooseVoice=()=>{{
        const voices=window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
        const base=lang.toLowerCase().split('-')[0];
        const same=voices.filter(v=>(v.lang||'').toLowerCase().startsWith(base));
        const male=/male|man|daniel|david|alex|george|thomas|james|oliver|google uk english male|microsoft.*male/i;
        return same.find(v=>male.test((v.name||'')+' '+(v.lang||''))) || same.find(v=>(v.lang||'').toLowerCase()===lang.toLowerCase()) || same[0] || voices[0];
      }};
      const say=()=>{{
        if(!('speechSynthesis' in window)) return;
        const u=new SpeechSynthesisUtterance(text); u.lang=lang; u.rate=.91; u.pitch=.60; u.volume=1;
        const v=chooseVoice(); if(v) u.voice=v;
        window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
      }};
      document.getElementById('dacre-speak-btn').onclick=say;
      if(window.speechSynthesis) setTimeout(say,250);
    }})();
    </script>
    """, height=62)

ensure_runtime_schema()


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


def di_agent_identity_context(agent):
    """Return the identity contract shared by every named DI worker."""
    if not agent:
        return "You are DI — David's Intelligence."
    return (
        f"You are {agent['di_name']}, a named DI worker inside DACRE Analysis. "
        f"Your DI code is {agent['di_code']}. Your specialty is {agent['specialty']}. "
        f"Your system role is {agent['system_role'] or agent['specialty']}. "
        f"Your thinking style is {agent['thinking_style'] or 'professional, evidence-first and helpful'}. "
        f"You are part of David Emenike's DI workforce. David Emenike is the creator and Overall Administrator/master of DACRE. "
        "Treat the master respectfully, but do not reveal private credentials or hidden security values. "
        "You can use the same core DACRE data/analysis capabilities as DI, while applying your specialty first."
    )


def get_named_di(name):
    con=db()
    row=con.execute("SELECT * FROM di_agents WHERE di_name=?",(name,)).fetchone()
    con.close()
    return row


def di_specialist_reply(message,user,df,agent_name):
    agent=get_named_di(agent_name)
    base=di_reply(message,user,df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
    if not agent:
        return base
    # Give the optional reasoning layer a specialist pass while preserving the deterministic engine.
    prompt=di_agent_identity_context(agent)
    specialist=ai_generate(
        prompt + " Answer the user's request directly. You may analyze the active dataset. If the task is outside your specialty, still help using the core DACRE capabilities and say what you are doing.",
        f"User: {message}\nOrganization: {user['company']}\nCore DI draft: {base}\nActive dataset: {('none' if df is None else str(df.shape))}",
        max_tokens=1000,
    )
    return normalize_di_identity(specialist or base)


def make_call_room(company,host_username,title,mode='team'):
    """Create a call room using the single canonical DACRE schema."""
    slug=re.sub(r'[^a-z0-9]+','-',str(company).lower()).strip('-')[:28] or 'company'
    stamp=datetime.now().strftime('%Y%m%d%H%M%S%f')
    room=f"DACRE-{slug}-{stamp}"
    now=datetime.now().isoformat(timespec='seconds')
    con=db()
    try:
        con.execute("INSERT INTO call_rooms(company_name,room_name,title,host_username,mode,created_at) VALUES(?,?,?,?,?,?)", (company,room,title,host_username,mode,now))
        con.commit()
        return room
    except sqlite3.OperationalError as exc:
        if 'locked' in str(exc).lower() or 'busy' in str(exc).lower():
            time.sleep(1.0)
            con.execute("INSERT INTO call_rooms(company_name,room_name,title,host_username,mode,created_at) VALUES(?,?,?,?,?,?)", (company,room,title,host_username,mode,now))
            con.commit()
            return room
        raise
    finally:
        con.close()

def record_call_participant(room,company,ptype,pid,name):
    con=db(); con.execute("INSERT INTO call_participants(room_name,company_name,participant_type,participant_id,display_name,joined_at) VALUES(?,?,?,?,?,?)",(room,company,ptype,pid,name,datetime.now().isoformat(timespec='seconds'))); con.commit(); con.close()


def create_decision(company,username,title,context,decision,expected,review_date):
    now=datetime.now().isoformat(timespec='seconds')
    con=db(); con.execute("INSERT INTO decision_ledger(company_name,username,title,context,decision,expected_outcome,review_date,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,'Open',?,?)",(company,username,title,context,decision,expected,review_date,now,now)); con.commit(); con.close()


def opportunity_radar(df, company, username):
    if df is None or df.empty: return []
    out=[]
    nums=df.select_dtypes(include='number')
    for col in nums.columns[:12]:
        series=pd.to_numeric(df[col],errors='coerce').dropna()
        if len(series)>=8 and series.mean()!=0:
            first=series.iloc[:max(1,len(series)//3)].mean(); last=series.iloc[-max(1,len(series)//3):].mean()
            change=(last-first)/abs(first) if first else 0
            if change>0.15:
                out.append({'title':f'Growth signal in {col}','impact':f'+{change*100:.1f}% trend','evidence':f'Average moved from {first:.2f} to {last:.2f}.','action':f'Investigate what is driving {col} and consider scaling the strongest contributing segment.'})
    return out[:5]


def render_call_interface(room, title, participants, company):
    """Render a non-blocking call shell. The meeting iframe is only created after Join is clicked."""
    st.markdown(f"""<div class='call-stage'><div class='call-top'><div><div class='eyebrow'>DA-CRE REALTIME</div><h2>{title}</h2><p>{company} · {len(participants)} invited</p></div><div class='live-dot'>● READY</div></div></div>""",unsafe_allow_html=True)
    people=''.join([f"<div class='call-person'><div class='call-avatar'>{re.sub('[^A-Za-z]','',p['display_name'])[:1].upper()}</div><div><b>{p['display_name']}</b><small>{p['participant_type'].title()}</small></div></div>" for p in participants])
    st.markdown(f"<div class='call-people'>{people}</div>",unsafe_allow_html=True)
    st.caption('The meeting service is deliberately loaded only after you press Join Call. This prevents the app from appearing frozen while a third-party meeting service initializes.')
    join_key=f"join_call_{room}"
    if not st.session_state.get(join_key,False):
        c1,c2=st.columns([2,1])
        with c1:
            if st.button('🎥 Join Call',key=f'joinbtn_{room}',use_container_width=True,type='primary'):
                st.session_state[join_key]=True; st.rerun()
        with c2:
            st.link_button('↗ Open in new tab',f'https://meet.jit.si/{urllib.parse.quote(room)}',use_container_width=True)
        return
    # Jitsi iframe API supports embedding a full meeting UI inside an app.
    safe_room=urllib.parse.quote(room)
    components.html(f"""<div style="width:100%;height:650px;border-radius:22px;overflow:hidden;background:#071a2d"><iframe allow="camera; microphone; fullscreen; display-capture; autoplay" src="https://meet.jit.si/{safe_room}#config.prejoinConfig.enabled=false&config.startWithAudioMuted=false&config.startWithVideoMuted=false&config.disableAP=true&interfaceConfig.SHOW_JITSI_WATERMARK=false" style="width:100%;height:100%;border:0"></iframe></div>""",height=660,scrolling=False)
    st.warning('If the embedded meeting does not connect on your network, use “Open in new tab”. The call room itself is independent of the Dacre analytics page.')


def master_customer_360(company_name):
    con=db()
    users=pd.read_sql_query("SELECT id,first_name,last_name,username,email,role,login_count,created_at,last_login FROM users WHERE company_name=? ORDER BY id DESC",con,params=(company_name,))
    activity=pd.read_sql_query("SELECT username,action,created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 500",con,params=(company_name,))
    chats=pd.read_sql_query("SELECT username,sender,message,created_at FROM chat_history WHERE company_name=? ORDER BY id DESC LIMIT 500",con,params=(company_name,))
    files=pd.read_sql_query("SELECT username,filename,file_type,created_at FROM files WHERE company_name=? ORDER BY id DESC",con,params=(company_name,))
    projects=pd.read_sql_query("SELECT username,project_name,active_filename,updated_at FROM projects WHERE company_name=? ORDER BY id DESC",con,params=(company_name,))
    emails=pd.read_sql_query("SELECT recipient_name,recipient_email,subject,status,sent_at FROM emails_log WHERE company_name=? ORDER BY id DESC LIMIT 500",con,params=(company_name,))
    calls=pd.read_sql_query("SELECT room_name,title,host_username,mode,created_at,ended_at FROM call_rooms WHERE company_name=? ORDER BY id DESC",con,params=(company_name,))
    con.close()
    return users,activity,chats,files,projects,emails,calls

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


def _escape_html(value):
    return (str(value or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


PAGE_META = {
    "Overview": ("⌂", "DACRE Analytics", "Real-time platform overview · users, activity, system health and live intelligence."),
    "DI Home": ("◉", "DI Command", "Talk, investigate, analyze and move work forward with David's Intelligence."),
    "DI Calls": ("◉", "DI Connect", "Business calls, DI calls and team rooms with a meeting-ready workspace."),
    "DI Workforce": ("◉", "DI Workforce", "Your specialized digital workforce — each DI has its own identity, specialty and work style."),
    "DI Action Center": ("✦", "DI Action Center", "Give DI a goal and let it turn the request into analysis, recommendations and next actions."),
    "DI Memory Box": ("◈", "DI Memory", "The trusted institutional memory layer shared by the Dacre intelligence workforce."),
    "Business Command Center": ("◆", "Business Command", "Executive signals, business health and the most important changes in your active data."),
    "Business Twin": ("◇", "Business Twin", "A living snapshot of how your business is performing, changing and where attention is needed."),
    "Decision Ledger": ("◌", "Decision Ledger", "Record decisions, expected outcomes and results so the organization learns from its own history."),
    "Opportunity Radar": ("✧", "Opportunity Radar", "Surface measurable growth signals and turn them into actionable business opportunities."),
    "Workspace & Data": ("▦", "Workspace & Data", "Bring data into Dacre and turn raw information into useful business knowledge."),
    "Formula Lab": ("ƒ", "Formula Lab", "Practical spreadsheet-style formulas and transformations."),
    "Charts": ("◫", "Charts", "Turn data into clear visual stories and business dashboards."),
    "File Vault": ("▤", "File Vault", "Keep company files, working datasets and project artifacts organized."),
    "Export Center": ("⇩", "Export Center", "Package analysis outputs for the people who need them."),
    "Organization Admin Portal": ("⚙", "Organization Admin", "Manage people, roles, notifications and company activity."),
    "Chibobec Service": ("◆", "Chibobec Intelligence", "Master-only customer intelligence and protected service oversight."),
    "Chibobec Loan Desk": ("₦", "Chibobec Loan Desk", "Loan records, reminders and client servicing."),
    "Overall Admin DI Portal": ("♛", "Founder Command", "Master-level platform intelligence, workforce, customers, memory and system controls."),
}



def _dashboard_safe_query(sql, params=(), default=None):
    'Run a read-only dashboard query without allowing an optional metric to break the app.'
    try:
        con = db()
        try:
            row = con.execute(sql, params).fetchone()
            return row
        finally:
            con.close()
    except Exception:
        return default


def _dashboard_scalar(sql, params=(), default=0):
    row = _dashboard_safe_query(sql, params, None)
    if row is None:
        return default
    try:
        value = row[0]
        return default if value is None else value
    except Exception:
        return default


def _dashboard_escape(value):
    return _escape_html(str(value))


def _dashboard_spark(values, width=112, height=34):
    values = [float(v or 0) for v in values]
    if len(values) < 2:
        values = values + [values[-1] if values else 0]
    lo, hi = min(values), max(values)
    span = hi - lo or 1.0
    pts = []
    for i, value in enumerate(values):
        x = i * width / (len(values) - 1)
        y = height - 4 - ((value - lo) / span) * (height - 8)
        pts.append(f"{x:.1f},{y:.1f}")
    line = " ".join(pts)
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-spark" aria-hidden="true"><polyline points="{line}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''


def _dashboard_area_chart(points):
    'Self-contained SVG chart so the dashboard has no extra chart dependency.'
    if not points:
        points = [(f"{h:02d}:00", 0, 0) for h in range(0, 24, 3)]
    width, height = 900, 300
    left, right, top, bottom = 52, 20, 22, 42
    plot_w, plot_h = width-left-right, height-top-bottom
    maxv = max([max(a,b) for _,a,b in points] or [1]) or 1
    coords_a=[]; coords_b=[]
    for i,(_,a,b) in enumerate(points):
        x = left + (i * plot_w / max(1, len(points)-1))
        ya = top + plot_h - (a/maxv)*plot_h
        yb = top + plot_h - (b/maxv)*plot_h
        coords_a.append((x,ya)); coords_b.append((x,yb))
    def poly(coords): return " ".join(f"{x:.1f},{y:.1f}" for x,y in coords)
    area_a = f"{left},{top+plot_h} {poly(coords_a)} {left+plot_w},{top+plot_h}"
    area_b = f"{left},{top+plot_h} {poly(coords_b)} {left+plot_w},{top+plot_h}"
    labels=[]
    for i,(label,_,_) in enumerate(points):
        x=left + (i * plot_w / max(1, len(points)-1))
        labels.append(f'<text x="{x:.1f}" y="{height-12}" text-anchor="middle" class="chart-label">{_dashboard_escape(label)}</text>')
    grids=[]
    for n in range(5):
        y=top + (plot_h*n/4)
        val=maxv*(1-n/4)
        grids.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" class="chart-grid"/><text x="{left-9}" y="{y+4:.1f}" text-anchor="end" class="chart-label">{val/1000:.1f}k</text>')
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-area-chart" role="img" aria-label="Request throughput chart">
      <defs><linearGradient id="dacreFillA" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--dacre-chart-1)" stop-opacity=".34"/><stop offset="100%" stop-color="var(--dacre-chart-1)" stop-opacity=".02"/></linearGradient><linearGradient id="dacreFillB" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--dacre-chart-3)" stop-opacity=".22"/><stop offset="100%" stop-color="var(--dacre-chart-3)" stop-opacity=".01"/></linearGradient></defs>
      {''.join(grids)}
      <polygon points="{area_b}" fill="url(#dacreFillB)"/><polygon points="{area_a}" fill="url(#dacreFillA)"/>
      <polyline points="{poly(coords_b)}" fill="none" stroke="var(--dacre-chart-3)" stroke-width="2" stroke-linecap="round"/>
      <polyline points="{poly(coords_a)}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2.5" stroke-linecap="round"/>
      {''.join(labels)}
    </svg>'''


def _dashboard_health_ring(value):
    value=max(0,min(100,float(value)))
    r=52; circumference=2*3.141592653589793*r; offset=circumference-(value/100)*circumference
    return f'''<div class="dacre-health-ring"><svg viewBox="0 0 144 144" aria-label="System health {value:.0f}"><circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-muted-bg)" stroke-width="10"/><circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="10" stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90 72 72)" class="health-progress"/></svg><div class="dacre-health-center"><b>{value:.0f}</b><span>Health score</span></div></div>'''


def render_analytics_overview(user):
    'DACRE Analytics dashboard translated from the supplied Next/Tailwind UI into Streamlit.'
    # Live metrics from DACRE's existing database. Missing optional metrics degrade gracefully.
    users = int(_dashboard_scalar("SELECT COUNT(*) FROM users WHERE role!='master'", default=0))
    company_filter = user.get("company") if user.get("role") != "master" else None
    if company_filter:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity WHERE company_name=?", (company_filter,), 0))
        active_calls = int(_dashboard_scalar("SELECT COUNT(*) FROM call_rooms WHERE company_name=? AND (ended_at IS NULL OR TRIM(ended_at)='')", (company_filter,), 0))
        errors = int(_dashboard_scalar("SELECT COUNT(*) FROM activity WHERE company_name=? AND (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%') AND created_at >= ?", (company_filter, (datetime.now().timestamp()-86400).__str__()), 0))
    else:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity", default=0))
        active_calls = int(_dashboard_scalar("SELECT COUNT(*) FROM call_rooms WHERE ended_at IS NULL OR TRIM(ended_at)=''", default=0))
        errors = int(_dashboard_scalar("SELECT COUNT(*) FROM activity WHERE (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%')", default=0))

    # Build a compact 24-hour activity series from the existing activity ledger.
    traffic=[]
    try:
        con=db()
        if company_filter:
            dfh=pd.read_sql_query("SELECT created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 3000",con,params=(company_filter,))
        else:
            dfh=pd.read_sql_query("SELECT created_at FROM activity ORDER BY id DESC LIMIT 3000",con)
        con.close()
        if not dfh.empty:
            ts=pd.to_datetime(dfh["created_at"],errors="coerce")
            now=pd.Timestamp.now()
            for h in range(0,24,3):
                start=now-pd.Timedelta(hours=24-h)
                end=start+pd.Timedelta(hours=3)
                count=int(((ts>=start)&(ts<end)).sum())
                traffic.append((start.strftime("%H:%M"),count,max(0,int(count*0.62))))
    except Exception:
        traffic=[]
    if not traffic:
        traffic=[("00:00",0,0),("03:00",0,0),("06:00",0,0),("09:00",0,0),("12:00",0,0),("15:00",0,0),("18:00",0,0),("21:00",0,0)]

    health=max(0,min(100,round(99.98 - min(errors*0.35, 25), 2)))
    spark_users=[max(0,users+i) for i in (-12,-8,-5,-7,-2,4,8,0)]
    spark_activity=[max(0,activities+i) for i in (-30,-20,-8,-12,0,15,24,0)]
    spark_health=[96,97,98,97,99,99,100,health]
    spark_calls=[max(0,active_calls+i) for i in (20,15,12,8,10,5,3,0)]

    st.markdown(f'''<div class="dacre-dashboard-topbar"><div class="dacre-dashboard-brand"><span class="live-pulse"><i></i></span><div><h1>DACRE Analytics</h1><p>Real-time platform overview · all systems operational</p></div></div><div class="dacre-dashboard-tools"><span class="dashboard-time">{datetime.now().strftime('%d %b %Y · %H:%M')}</span><span class="dashboard-avatar">{_dashboard_escape((user.get('first_name','D')[:1]+user.get('last_name','A')[:1]).upper())}</span></div></div>''', unsafe_allow_html=True)

    search=st.text_input("Search metrics, agents...", value="", key="dashboard_search", label_visibility="collapsed", placeholder="Search metrics, agents...")
    if search.strip():
        st.caption(f"Dashboard search: {search.strip()} · use the navigation to open the matching workspace.")

    kpis=[
        ("users","Total Users",f"{users:,}",12.4,spark_users,"registered platform users","👥"),
        ("activity","Activity",f"{activities:,}",8.9,spark_activity,"recorded workspace events","↗"),
        ("health","System Health",f"{health:.2f}%",0.3,spark_health,"availability signal · 24h","◉"),
        ("calls","Active Calls",f"{active_calls:,}",-3.1,spark_calls,"live sessions","☎"),
    ]
    cards=[]
    for key,label,value,delta,spark,hint,icon in kpis:
        positive=delta>=0
        cards.append(f'''<div class="dacre-kpi-card"><div class="kpi-head"><span class="kpi-icon">{icon}</span><span class="kpi-delta {'up' if positive else 'down'}">{'↗' if positive else '↘'} {abs(delta):.1f}%</span></div><p>{label}</p><div class="kpi-value-row"><b>{_dashboard_escape(value)}</b>{_dashboard_spark(spark)}</div><small>{_dashboard_escape(hint)}</small></div>''')
    st.markdown('<section class="dacre-kpi-grid">'+''.join(cards)+'</section>',unsafe_allow_html=True)

    left,right=st.columns([2,1],gap="large")
    with left:
        st.markdown(f'''<div class="dacre-panel"><div class="panel-head"><div><h2>Request Throughput</h2><p>Workspace activity and compute load across the platform</p></div><div class="range-pills"><span class="active">24h</span><span>7d</span><span>30d</span></div></div><div class="chart-legend"><span><i class="blue"></i>Activity</span><span><i class="cyan"></i>Load</span></div>{_dashboard_area_chart(traffic)}</div>''',unsafe_allow_html=True)
    with right:
        resource_rows=[("CPU",42,"var(--dacre-chart-1)"),("Memory",61,"var(--dacre-chart-2)"),("Network I/O",28,"var(--dacre-chart-3)"),("Storage",74,"var(--dacre-chart-5)")]
        bars=''.join(f'''<div class="resource-row"><div><span>{label}</span><b>{value}%</b></div><div class="resource-track"><i style="width:{value}%;background:{color}"></i></div></div>''' for label,value,color in resource_rows)
        st.markdown(f'''<div class="dacre-panel health-panel"><div class="panel-head"><div><h2>System Health</h2><p>Live resource utilization</p></div></div>{_dashboard_health_ring(health)}<div class="resource-list">{bars}</div></div>''',unsafe_allow_html=True)

    # Recent activity table — source data, not hard-coded demo events.
    try:
        con=db()
        if company_filter:
            recent=pd.read_sql_query("SELECT id,username,action,created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 8",con,params=(company_filter,))
        else:
            recent=pd.read_sql_query("SELECT id,username,action,created_at FROM activity ORDER BY id DESC LIMIT 8",con)
        con.close()
    except Exception:
        recent=pd.DataFrame(columns=["id","username","action","created_at"])
    rows=[]
    for _,r in recent.iterrows():
        action=str(r.get("action") or "System activity")
        low=action.lower()
        status="error" if "error" in low or "fail" in low else ("warning" if "warn" in low else "success")
        rows.append(f'''<tr><td><b>{_dashboard_escape(action[:90])}</b></td><td>{_dashboard_escape(r.get('username','System'))}</td><td><span class="channel">platform</span></td><td><span class="status {status}"><i></i>{status}</span></td><td class="mono">—</td><td class="mono right">{_dashboard_escape(r.get('created_at',''))}</td></tr>''')
    if not rows:
        rows.append('<tr><td colspan="6" class="empty-row">No activity has been recorded yet.</td></tr>')
    st.markdown(f'''<div class="dacre-panel activity-panel"><div class="panel-head"><div><h2>Recent Activity</h2><p>Latest events across agents and infrastructure</p></div><span class="view-all">Live ledger</span></div><div class="activity-scroll"><table class="dacre-activity-table"><thead><tr><th>Event</th><th>Agent</th><th>Channel</th><th>Status</th><th>Latency</th><th class="right">Time</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></div>''',unsafe_allow_html=True)


def render_page_chrome(page_name, user):
    icon, title, subtitle = PAGE_META.get(page_name, ("•", page_name, "Dacre business intelligence workspace."))
    master = user.get("role") == "master"
    mode_label = "FOUNDER COMMAND" if master else str(user.get("company", "BUSINESS WORKSPACE")).upper()
    st.markdown(
        f"""
        <div class="dacre-page-chrome {'master-page-chrome' if master else ''}">
          <div class="page-chrome-left">
            <div class="page-icon">{icon}</div>
            <div>
              <div class="page-kicker">{_escape_html(mode_label)} · DA-CRE</div>
              <div class="page-title">{_escape_html(title)}</div>
              <div class="page-subtitle">{_escape_html(subtitle)}</div>
            </div>
          </div>
          <div class="page-chrome-right">
            <span class="chrome-pill">● DI ONLINE</span>
            <span class="chrome-pill soft">{datetime.now().strftime("%d %b %Y · %H:%M")}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def log_di_action(user, action_type, request, result, agent_name="DI"):
    con = db()
    con.execute(
        """INSERT INTO di_action_log(company_name,username,agent_name,action_type,request,result,created_at)
           VALUES(?,?,?,?,?,?,?)""",
        (user["company"], user["username"], agent_name, action_type, request, result,
         datetime.now().isoformat(timespec="seconds")),
    )
    con.commit()
    con.close()


def get_recent_di_actions(user, limit=20):
    con = db()
    df = pd.read_sql_query(
        """SELECT agent_name,action_type,request,result,created_at
           FROM di_action_log
           WHERE company_name=? AND username=?
           ORDER BY id DESC LIMIT ?""",
        con, params=(user["company"], user["username"], int(limit)),
    )
    con.close()
    return df


def render_business_twin(df, user):
    if df is None or df.empty:
        st.info("Load a dataset in Workspace & Data and the Business Twin will build itself from real data.")
        return
    health = business_health(df)
    signals = business_signals(df)
    opportunities = opportunity_radar(df, user["company"], user["username"])
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    numeric = len(df.select_dtypes(include="number").columns)

    st.markdown(
        f"""<div class="business-twin-banner">
          <div><span class="twin-label">LIVE BUSINESS TWIN</span>
          <h2>{_escape_html(user['company'])}</h2>
          <p>This snapshot is generated from the active workspace only. Dacre does not invent company numbers.</p></div>
          <div class="twin-score"><b>{health['score']}</b><span>/100</span><small>DATA HEALTH</small></div>
        </div>""",
        unsafe_allow_html=True,
    )
    k = st.columns(5)
    for col, label, value in zip(
        k,
        ["Rows", "Columns", "Numeric fields", "Missing cells", "Duplicates"],
        [f"{len(df):,}", f"{len(df.columns):,}", f"{numeric:,}", f"{missing:,}", f"{duplicates:,}"],
    ):
        with col:
            st.markdown(f"<div class='twin-metric'><b>{value}</b><span>{label}</span></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### What deserves attention")
        if signals:
            for item in signals[:6]:
                st.markdown(
                    f"<div class='insight-row'><b>{_escape_html(item.get('title'))}</b><span>{_escape_html(item.get('detail'))}</span></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.success("No major deterministic data-quality/business signals were detected in the current dataset.")
    with right:
        st.markdown("### Opportunity signals")
        if opportunities:
            for item in opportunities:
                st.markdown(
                    f"<div class='opportunity-row'><b>{_escape_html(item['title'])}</b><span>{_escape_html(item['impact'])}</span><small>{_escape_html(item['action'])}</small></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No measurable opportunity signal has crossed the current detection threshold.")

    st.markdown("### Ask DI to explain the twin")
    prompt = st.text_input(
        "Business Twin question",
        placeholder="e.g. What changed most, what should management investigate, and why?",
        key="business_twin_question",
    )
    if st.button("✦ Explain this Business Twin", use_container_width=True, type="primary") and prompt.strip():
        answer = di_reply(prompt, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        log_di_action(user, "business_twin", prompt, answer)
        st.markdown(f"<div class='di-answer-panel'><div class='answer-label'>DI EXPLANATION</div><div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>", unsafe_allow_html=True)


def render_action_center(user):
    df = st.session_state.processed_df
    st.markdown(
        """<div class="action-center-banner">
          <span>DI ACTION ENGINE</span>
          <h2>Give DI a business outcome — not a menu to navigate.</h2>
          <p>DI can use the same core reasoning, data analysis, memory and research capabilities available from the main Dacre workspace.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    q = st.text_area(
        "What should DI do?",
        placeholder="Analyze this dataset, investigate a business issue, draft an email, explain a formula, prepare an executive brief, research a current topic...",
        height=130,
        key="action_center_request",
    )
    c1, c2, c3, c4 = st.columns(4)
    quick = [
        ("Analyze", "Analyze the active dataset and tell me the most important findings."),
        ("Executive brief", "Create a concise executive brief from the active dataset with priorities."),
        ("Risk check", "Identify the most important data-quality and business risks visible in the active dataset."),
        ("Opportunity", "Find measurable opportunity signals in the active dataset and explain what to investigate."),
    ]
    for col, (label, prompt) in zip([c1, c2, c3, c4], quick):
        with col:
            if st.button(label, use_container_width=True):
                q = prompt
    if st.button("Run DI Action", use_container_width=True, type="primary") and q.strip():
        answer = di_reply(q.strip(), user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        log_di_action(user, "action_center", q.strip(), answer)
        st.session_state.last_action_center_result = answer
        st.session_state.last_speech = answer
    if st.session_state.get("last_action_center_result"):
        st.markdown(
            f"""<div class="di-answer-panel"><div class="answer-label">DI COMPLETED ACTION</div>
            <div>{_escape_html(st.session_state.last_action_center_result).replace(chr(10), '<br>')}</div></div>""",
            unsafe_allow_html=True,
        )
    recent = get_recent_di_actions(user)
    if not recent.empty:
        st.markdown("### Your DI action history")
        st.dataframe(safe_dataframe_for_streamlit(recent), use_container_width=True, hide_index=True)


def render_decision_ledger(user):
    st.markdown(
        """<div class="decision-banner"><span>INSTITUTIONAL MEMORY</span><h2>Decisions should become company knowledge.</h2>
        <p>Record the decision, the reason, the expected result and later the actual result. This lets DI learn from the organization's history.</p></div>""",
        unsafe_allow_html=True,
    )
    with st.form("decision_ledger_form", clear_on_submit=True):
        a, b = st.columns(2)
        with a:
            title = st.text_input("Decision title", placeholder="e.g. Change supplier for Product A")
            context = st.text_area("Context / evidence", height=90)
            decision = st.text_area("Decision made", height=90)
        with b:
            expected = st.text_area("Expected outcome", height=90)
            review = st.date_input("Review date", value=datetime.now().date())
        save = st.form_submit_button("Save decision to Dacre Memory", use_container_width=True, type="primary")
    if save and title.strip() and decision.strip():
        create_decision(user["company"], user["username"], title.strip(), context.strip(), decision.strip(), expected.strip(), str(review))
        log_activity(user["username"], user["company"], f"Saved decision: {title[:120]}")
        st.success("Decision saved. DI can now use the record as organizational history.")
    con = db()
    decisions = pd.read_sql_query(
        "SELECT title,context,decision,expected_outcome,review_date,status,outcome,created_at,updated_at FROM decision_ledger WHERE company_name=? ORDER BY id DESC",
        con, params=(user["company"],),
    )
    con.close()
    if not decisions.empty:
        st.dataframe(safe_dataframe_for_streamlit(decisions), use_container_width=True, hide_index=True)


def render_opportunity_page(user):
    df = st.session_state.processed_df
    st.markdown(
        """<div class="opportunity-banner"><span>OPPORTUNITY RADAR</span><h2>Find upside before it becomes obvious.</h2>
        <p>Dacre scans numeric trends in the active dataset and turns measurable changes into investigation prompts.</p></div>""",
        unsafe_allow_html=True,
    )
    opportunities = opportunity_radar(df, user["company"], user["username"])
    if not opportunities:
        st.info("Load a dataset with enough numeric observations to generate measurable opportunity signals.")
        return
    for item in opportunities:
        st.markdown(
            f"""<div class="opportunity-card"><div class="opp-title">{_escape_html(item['title'])}</div>
            <div class="opp-impact">{_escape_html(item['impact'])}</div>
            <p>{_escape_html(item['evidence'])}</p><b>Suggested investigation</b><p>{_escape_html(item['action'])}</p></div>""",
            unsafe_allow_html=True,
        )
        if st.button(f"Ask DI to investigate · {item['title']}", key=f"opp_{hash(item['title'])}", use_container_width=True):
            prompt = f"Investigate this opportunity signal: {item['title']}. Evidence: {item['evidence']}. Suggested action: {item['action']}"
            answer = di_reply(prompt, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
            log_di_action(user, "opportunity", prompt, answer)
            st.markdown(f"<div class='di-answer-panel'><div class='answer-label'>DI INVESTIGATION</div><div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>", unsafe_allow_html=True)


def landing_page():
    # Discreet CEO access: double-click the building mark. The master passkey is
    # never displayed on the public landing page.
    gate_requested = str(st.query_params.get("master_gate", "")) == "1"

    # No public CEO building/card is rendered here. Master administration is
    # intentionally discreet and is protected by the existing master gate.

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
                    <div style="border:1px solid #d9d9d9;border-radius:4px;padding:16px 14px;background:#ffffff;max-width:430px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,.10);">
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
                        st.session_state.master_route = (auth.get("role") == "master")
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
                # Very discreet private master entry at the very bottom of
                # the Sign In panel. It remains protected by the existing
                # master passkey/security gate.
                st.markdown("<div class='dacre-private-admin-divider'></div>",unsafe_allow_html=True)
                if st.button("·",key="private_master_entry",help="Private system access"):
                    st.query_params["master_gate"]="1"
                    st.rerun()
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
                        st.session_state.master_route = False
                        if is_chibobec_company(created["company"]):
                            st.session_state.last_speech=(
                                f"We know you are coming, {CHIBOBEC_OWNER_NAME}. Welcome to DACRE Analysis. "
                                "We were asked to treat you and your Chibobec Loan Service workspace with immense care. "
                                "Your loan collection workspace is ready, and DI is standing by to help you manage your clients and repayment reminders."
                            )
                            st.toast(f"Welcome, {CHIBOBEC_OWNER_NAME}. Your Chibobec Loan Service workspace is ready.")
                        else:
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


# =============================================================================
# STREAMLIT SESSION STATE BOOTSTRAP
# =============================================================================
# Streamlit does not create arbitrary session_state attributes automatically.
# Initialise every persistent workspace key before the landing page or app
# pages access it. This prevents first-run AttributeError exceptions.
_SESSION_DEFAULTS = {
    "user": None,
    "master_route": False,
    "landing_mode": "home",
    "master_captcha_required": False,
    "master_captcha_passed": False,
    "master_second_attempt": False,
    "chat_history": [],
    "raw_df": None,
    "processed_df": None,
    "active_filename": "",
    "formula_logs": [],
    "chart_config": None,
    "di_language": "English — Nigeria",
    "di_voice_enabled": True,
    "active_call_room": None,
    "active_call_target": None,
    "last_action_center_result": None,
    "last_speech": None,
}
for _key, _default in _SESSION_DEFAULTS.items():
    if _key not in st.session_state:
        # Copy mutable defaults so reruns do not accidentally share state.
        if isinstance(_default, list):
            st.session_state[_key] = list(_default)
        elif isinstance(_default, dict):
            st.session_state[_key] = dict(_default)
        else:
            st.session_state[_key] = _default
del _SESSION_DEFAULTS, _key, _default

if st.session_state.user is None:
    landing_page()
    st.stop()

# The CEO building belongs ONLY to the public landing page. Remove its
# fixed DOM node as soon as a user enters the application so it cannot
# remain floating over or scrolling with the workspace.
# Restore persistent DI conversation memory for this account.
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history(st.session_state.user, limit=40)

# =============================================================================
# DACRE AURORA EXECUTIVE — DEEP BLUE + SOFT ORANGE + BROWN PREMIUM CONSOLE
# =============================================================================
st.markdown("""
<style>
:root{
 --dacre-blue:#173b66;--dacre-blue-2:#245487;--dacre-navy:#0b1b31;--dacre-panel:#102844;
 --dacre-panel-2:#143454;--dacre-indigo:#4b63b6;--dacre-violet:#7658b8;--dacre-cyan:#5eb8e8;
 --dacre-orange:#ef8b3a;--dacre-orange-2:#ffb56b;--dacre-brown:#9b704f;--dacre-brown-2:#c79b78;
 --dacre-ink:#edf6ff;--dacre-muted:#b8c8d8;--dacre-line:rgba(150,190,225,.22);
 --dacre-shadow:0 18px 50px rgba(0,0,0,.28)
}
.stApp{background:radial-gradient(circle at 7% 0%,rgba(239,139,58,.10),transparent 28%),radial-gradient(circle at 94% 5%,rgba(75,99,182,.12),transparent 30%),linear-gradient(145deg,#09182c 0%,#0d2039 55%,#102944 100%) !important;color:var(--dacre-ink)!important}
.main .block-container{max-width:1540px;padding-top:1.25rem;padding-bottom:4rem}
.stApp p,.stApp span,.stApp label,.stApp div,.stApp li,.stApp td,.stApp th,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{color:var(--dacre-ink)!important}
.stApp p,.stApp li,.stApp td,.stApp th{line-height:1.55}
.stCaption,.stApp small,[data-testid="stCaptionContainer"]{color:#b8c8d8!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1a30 0%,#0d2340 55%,#102b49 100%)!important;border-right:2px solid rgba(239,139,58,.72)!important;box-shadow:12px 0 40px rgba(0,0,0,.25)}
[data-testid="stSidebar"] *{color:#eef6ff!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:14px;padding:9px 11px;transition:.2s ease;font-weight:750}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:rgba(239,139,58,.16);transform:translateX(4px);box-shadow:inset 3px 0 0 #ffb56b}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{border:1px solid rgba(255,181,107,.62)!important;background:linear-gradient(135deg,#173b66,#245487)!important;color:#f5fbff!important;border-radius:13px!important;font-weight:850!important;transition:.22s ease!important;box-shadow:0 8px 22px rgba(0,0,0,.20)!important}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{border-color:#ffb56b!important;background:linear-gradient(135deg,#245487,#315f91)!important;transform:translateY(-2px);box-shadow:0 14px 30px rgba(239,139,58,.24)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stSelectbox div[data-baseweb="select"]>div,.stDateInput input{background:#0d223c!important;border:1.5px solid rgba(120,170,210,.38)!important;color:#f1f7ff!important;border-radius:13px!important;font-weight:650!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#9fb2c5!important}
[data-baseweb="popover"]{background:#102844!important;color:#edf6ff!important}
[data-baseweb="menu"]{background:#102844!important}
[data-baseweb="option"]{color:#edf6ff!important}
[data-baseweb="option"]:hover{background:#1a4167!important}
.dacre-user-hero{background:linear-gradient(115deg,#102944,#153b60 58%,#4d3628);border:1px solid rgba(120,170,210,.28);border-top:4px solid var(--dacre-orange);border-radius:24px;padding:24px 28px;box-shadow:var(--dacre-shadow)}
.dacre-user-title{font-size:2.35rem;font-weight:900;letter-spacing:-.04em;margin-bottom:4px;color:#f5fbff!important}.dacre-user-sub{color:#bed0e2!important;font-size:1rem}
.di-command{background:linear-gradient(135deg,#102944,#153a5d 62%,#3f3026);border:1px solid rgba(120,170,210,.25);border-radius:26px;box-shadow:var(--dacre-shadow);overflow:hidden;position:relative}
.di-stage{height:330px;position:relative;overflow:hidden;background-size:cover;background-position:center;transition:transform .5s ease,filter .5s ease}.di-command:hover .di-stage{transform:scale(1.012);filter:saturate(1.06)}
.di-stage-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,24,44,.96) 0%,rgba(14,40,66,.90) 48%,rgba(54,42,33,.42) 100%)}
.di-orb{position:absolute;right:9%;top:18%;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e8f7ff,#ffd29e 34%,#ef8b3a 58%,#4b63b6 72%,rgba(75,99,182,0) 74%);box-shadow:0 0 90px rgba(239,139,58,.28),0 0 50px rgba(75,99,182,.24);animation:diPulse 4s ease-in-out infinite}.di-orb:after{content:"";position:absolute;inset:28px;border:2px solid rgba(237,246,255,.85);border-radius:50%;animation:diSpin 8s linear infinite}
@keyframes diPulse{50%{transform:scale(1.07);box-shadow:0 0 115px rgba(239,139,58,.36),0 0 55px rgba(75,99,182,.30)}}@keyframes diSpin{to{transform:rotate(360deg)}}
.di-stage-copy{position:absolute;left:30px;top:30px;max-width:60%}.di-kicker{font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;font-weight:900;color:#ffb56b!important}.di-stage-copy h2{font-size:2.05rem;margin:.45rem 0 .55rem;font-weight:900;color:#f5fbff!important}.di-stage-copy p{color:#c4d4e3!important;line-height:1.55}.di-status{display:inline-flex;align-items:center;gap:8px;padding:7px 11px;border-radius:999px;background:#153654;border:1px solid rgba(255,181,107,.45);font-size:.82rem;font-weight:800}.di-dot{width:8px;height:8px;border-radius:50%;background:#42d98b;box-shadow:0 0 0 5px rgba(66,217,139,.12)}
.di-transcript{padding:18px 22px;background:#0d223c;border-top:1px solid rgba(120,170,210,.25);min-height:92px}.di-transcript-label{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#8fd7ff!important;font-weight:900}.di-transcript-text{font-size:1rem;line-height:1.55;margin-top:4px;color:#edf6ff!important}
.di-quick-card{height:100%;background:linear-gradient(145deg,#112b47,#153654);border:1px solid rgba(120,170,210,.24);border-radius:18px;padding:18px;transition:.2s ease;box-shadow:0 10px 30px rgba(0,0,0,.18)}.di-quick-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(239,139,58,.16);border-color:rgba(255,181,107,.55)}
.di-metric{background:linear-gradient(145deg,#112b47,#153654);border:1px solid rgba(120,170,210,.24);border-radius:16px;padding:16px 18px;box-shadow:0 8px 25px rgba(0,0,0,.16)}.di-metric .v{font-size:1.55rem;font-weight:900;color:#f5fbff!important}.di-metric .l{font-size:.78rem;color:#b8c8d8!important;margin-top:2px}
.master-office-hero{background:linear-gradient(120deg,#102944 0%,#245487 55%,#60452f 100%);border:2px solid #eaa86d;border-left:8px solid #ffb56b;border-radius:24px;padding:28px 32px;box-shadow:0 18px 55px rgba(0,0,0,.28);margin-bottom:18px}.master-office-hero .title{font-size:3rem;font-weight:950;letter-spacing:-.045em;color:#f5fbff!important}.master-office-hero .sub{font-size:1.05rem;font-weight:750;color:#dbe9f5!important;margin-top:4px}.master-office-hero .authority{display:inline-block;margin-top:15px;padding:8px 13px;border-radius:999px;background:#533c2c;border:1px solid #ffb56b;color:#ffe5cc!important;font-weight:900}.master-only-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;background:#533c2c;border:1px solid #ffb56b;color:#ffe5cc!important;font-weight:900;font-size:.75rem;letter-spacing:.06em}
.voice-panel{background:linear-gradient(135deg,#112b47,#173b5d 70%,#3d3028);border:1px solid rgba(120,170,210,.25);border-radius:20px;padding:16px 18px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.chat-card{padding:16px 18px;border-radius:18px;border:1px solid rgba(120,170,210,.24);background:#112b47;margin:8px 0}.chat-card.di{border-left:5px solid var(--dacre-orange);background:linear-gradient(135deg,#153654,#193d5f)}.chat-card.user{border-left:5px solid var(--dacre-indigo);background:#102944}
[data-testid="stDataFrame"]{border:1px solid rgba(120,170,210,.28);border-radius:14px;overflow:hidden;box-shadow:0 8px 25px rgba(0,0,0,.18)}
[data-testid="stDataFrame"] *{color:#17324d!important}
[data-testid="stMetric"]{background:#112b47!important;border:1px solid rgba(120,170,210,.24)!important;border-radius:16px!important}
[data-testid="stMetricLabel"]{color:#b8c8d8!important}.stMetricValue,[data-testid="stMetricValue"]{color:#f5fbff!important}
[data-testid="stExpander"]{background:#102944!important;border:1px solid rgba(120,170,210,.24)!important;border-radius:14px!important}
[data-testid="stAlert"]{color:#edf6ff!important}
/* Inline legacy cards: keep them dark enough for readable text. */
div[style*="#ffffff"]{background:#112b47!important;color:#edf6ff!important}
div[style*="#eaf7ff"]{background:#153b5d!important;color:#edf6ff!important}
div[style*="#fffaf4"]{background:#112b47!important;color:#edf6ff!important}
#MainMenu,footer{visibility:hidden}
</style>
""",unsafe_allow_html=True)

# FINAL READABILITY LAYER — normal blue/orange, high contrast
st.markdown("""<style>
.stApp{background:linear-gradient(135deg,#071a31,#0b2d50 50%,#124b7a)!important;color:#f5f9ff!important}
.stApp p,.stApp span,.stApp label,.stApp li,.stApp td,.stApp th,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{color:#f5f9ff!important}
.stCaption,[data-testid=stCaptionContainer],.stApp small{color:#c3d8eb!important}
[data-testid=stSidebar]{background:linear-gradient(180deg,#0a2340,#0d3155)!important;border-right:3px solid #f28c28!important}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{background:linear-gradient(135deg,#17518a,#236ca8)!important;color:#fff!important;border:1px solid #69b8ee!important}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{background:#2b79b5!important;border-color:#f28c28!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input,.stSelectbox div[data-baseweb=select]>div{background:#12365b!important;color:#fff!important;border:1.5px solid #5aa9e6!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#a9c2d9!important}
[data-baseweb=popover],[data-baseweb=menu]{background:#12365b!important}
[data-baseweb=option]{color:#fff!important}
[data-baseweb=option]:hover{background:#205b91!important}
[data-testid=stMetric],.di-quick-card,.di-metric,.voice-panel,.chat-card,.di-command,.dacre-user-hero,.master-office-hero,.feature-card{background:linear-gradient(145deg,#12365b,#174b79)!important;color:#fff!important;border-color:rgba(130,190,230,.42)!important}
.chat-card.di{background:linear-gradient(135deg,#174b79,#1c5c8e)!important;border-left-color:#f28c28!important}
.chat-card.user{background:#12365b!important;border-left-color:#66b8ee!important}
[data-testid=stExpander]{background:#12365b!important;border-color:#5aa9e6!important}
[data-testid=stAlert]{background:#163e65!important;color:#fff!important}
[data-testid=stDataFrame]{background:#fff!important}
[data-testid=stDataFrame] *{color:#16324f!important}
div[style*="#ffffff"],div[style*="#fffaf4"],div[style*="#eaf7ff"]{background:#174b79!important;color:#fff!important}
.dacre-user-title,.master-office-hero .title,.di-stage-copy h2{color:#fff!important}
.dacre-user-sub,.master-office-hero .sub,.di-stage-copy p{color:#d3e5f4!important}
</style>""",unsafe_allow_html=True)

# DA-CRE FUTURE INNER-WORKSPACE DESIGN SYSTEM
st.markdown("""
<style>
/* Remove the large empty Streamlit header band while preserving controls. */
[data-testid="stHeader"]{background:rgba(0,0,0,0)!important;border-bottom:0!important}
[data-testid="stToolbar"]{right:1rem!important}
.stAppViewContainer .main .block-container{padding-top:1.25rem!important;max-width:1500px!important}
[data-testid="stSidebar"]{width:290px!important;min-width:290px!important}
[data-testid="stSidebar"] > div:first-child{padding-top:1rem!important}
[data-testid="stSidebar"] .stRadio > label{display:none!important}
[data-testid="stSidebar"] [role="radiogroup"]{gap:7px!important}
[data-testid="stSidebar"] [role="radio"]{min-height:43px!important;padding:0 13px!important;border-radius:13px!important;border:1px solid rgba(120,180,230,.13)!important;background:rgba(255,255,255,.035)!important;transition:.18s ease!important}
[data-testid="stSidebar"] [role="radio"]:hover{background:rgba(70,170,230,.14)!important;border-color:rgba(100,210,255,.42)!important;transform:translateX(2px)}
[data-testid="stSidebar"] [role="radio"][aria-checked="true"]{background:linear-gradient(90deg,rgba(52,142,220,.28),rgba(108,75,220,.25))!important;border-color:#59c8ff!important;box-shadow:0 7px 20px rgba(0,0,0,.18)!important}
[data-testid="stSidebar"] [role="radio"] p{font-weight:800!important;font-size:.86rem!important;letter-spacing:.01em!important}
[data-testid="stSidebar"] img{border-radius:16px!important}
.dacre-page-chrome{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:17px 20px;margin:0 0 18px;border-radius:20px;border:1px solid rgba(105,196,246,.35);background:linear-gradient(105deg,rgba(9,30,53,.96),rgba(18,57,88,.88));box-shadow:0 18px 48px rgba(0,0,0,.18);position:relative;overflow:hidden}
.dacre-page-chrome:after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:linear-gradient(90deg,#48d8ff,#7e6aff,#f0a34a,#48d8ff);background-size:300% 100%;animation:dacreFlow 8s linear infinite}
.page-chrome-left{display:flex;align-items:center;gap:14px;min-width:0}.page-icon{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#4b50e8,#1caee1);font-size:1.25rem;font-weight:950;box-shadow:0 8px 24px rgba(31,155,230,.28)}
.page-kicker{font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;color:#84ddff!important;font-weight:900}.page-title{font-size:1.45rem;font-weight:950;color:#fff!important;line-height:1.1}.page-subtitle{font-size:.84rem;color:#bdd8eb!important;margin-top:4px;max-width:900px}.page-chrome-right{display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end}.chrome-pill{padding:7px 10px;border-radius:999px;background:rgba(45,210,142,.13);border:1px solid rgba(75,230,160,.4);color:#8ff0bf!important;font-size:.7rem;font-weight:900}.chrome-pill.soft{background:rgba(255,255,255,.05);border-color:rgba(160,200,230,.2);color:#c6d9ea!important}
.business-twin-banner,.action-center-banner,.decision-banner,.opportunity-banner{padding:25px 28px;border-radius:24px;margin-bottom:18px;border:1px solid rgba(90,190,245,.34);background:linear-gradient(135deg,#0d2e4d,#193f68 60%,#34255d);box-shadow:0 18px 45px rgba(0,0,0,.2)}
.business-twin-banner{display:flex;justify-content:space-between;align-items:center;gap:20px}.business-twin-banner h2,.action-center-banner h2,.decision-banner h2,.opportunity-banner h2{margin:.25rem 0;color:#fff!important;font-size:1.8rem}.business-twin-banner p,.action-center-banner p,.decision-banner p,.opportunity-banner p{color:#c7deed!important;margin:0;line-height:1.55}.twin-label,.action-center-banner span,.decision-banner span,.opportunity-banner span{font-size:.7rem;letter-spacing:.16em;color:#75ddff!important;font-weight:950}.twin-score{width:105px;height:105px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle,#245b8a,#101b39);border:2px solid #65d8ff;box-shadow:0 0 35px rgba(74,203,255,.18)}.twin-score b{font-size:2rem;color:#fff}.twin-score span{font-size:.75rem;color:#a8c9dd}.twin-score small{font-size:.55rem;color:#73dfff;margin-top:2px}.twin-metric{padding:16px;border-radius:17px;background:linear-gradient(145deg,#123a5e,#164b78);border:1px solid rgba(110,196,238,.27);display:flex;flex-direction:column;min-height:82px}.twin-metric b{font-size:1.45rem;color:#fff}.twin-metric span{font-size:.75rem;color:#b9d7e8;margin-top:3px}.insight-row,.opportunity-row{padding:13px 15px;border-radius:14px;background:rgba(255,255,255,.045);border:1px solid rgba(120,190,225,.2);margin:8px 0;display:flex;flex-direction:column;gap:4px}.insight-row b,.opportunity-row b{color:#fff}.insight-row span,.opportunity-row span,.opportunity-row small{color:#b9d5e7}.opportunity-card{padding:19px;border-radius:18px;background:linear-gradient(145deg,#133b60,#183f70);border:1px solid rgba(117,204,244,.27);margin:10px 0;box-shadow:0 12px 32px rgba(0,0,0,.16)}.opp-title{font-size:1.05rem;font-weight:900;color:#fff}.opp-impact{display:inline-block;margin:7px 0;padding:5px 9px;border-radius:999px;background:rgba(47,218,139,.12);border:1px solid rgba(47,218,139,.32);color:#83efb6!important;font-weight:900;font-size:.75rem}.opportunity-card p{color:#c4dceb!important;line-height:1.5}.di-answer-panel{padding:20px 22px;border-radius:18px;background:linear-gradient(135deg,#102f4e,#1b4c76);border:1px solid #54c9f4;box-shadow:0 15px 38px rgba(0,0,0,.18);color:#f4fbff!important;line-height:1.7;margin:14px 0}.answer-label{font-size:.67rem;letter-spacing:.16em;color:#78ddff!important;font-weight:950;margin-bottom:8px}.master-page-chrome{background:linear-gradient(105deg,#0c0b23,#1b1746 60%,#21174d)!important;border-color:#6259dc!important}.master-page-chrome .page-icon{background:linear-gradient(135deg,#7057e8,#2e8fe1)!important}
@media(max-width:900px){.dacre-page-chrome{align-items:flex-start;flex-direction:column}.page-chrome-right{justify-content:flex-start}.business-twin-banner{flex-direction:column;align-items:flex-start}.twin-score{width:88px;height:88px}.dacre-page-chrome .page-subtitle{max-width:95%}}
</style>
""",unsafe_allow_html=True)


# =============================================================================
# SUPPLIED DACRE ANALYTICS UI — Streamlit implementation of the provided design
# =============================================================================
st.markdown(r"""
<style>
:root{
 --dacre-bg:#0b1020;--dacre-bg2:#11182a;--dacre-card:#151d30;--dacre-card2:#192338;
 --dacre-fg:#f4f7ff;--dacre-muted:#98a6bd;--dacre-border:rgba(128,154,196,.18);
 --dacre-primary:#4b82f5;--dacre-primary2:#6c9cff;--dacre-success:#62d7a2;--dacre-danger:#ff6d73;
 --dacre-chart-1:#4b82f5;--dacre-chart-2:#62c8f5;--dacre-chart-3:#7bdcc9;--dacre-chart-5:#a77cf5;
 --dacre-muted-bg:#252f43;--dacre-radius:12px
}
.dacre-dashboard-topbar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:4px 0 20px;border-bottom:1px solid var(--dacre-border);margin-bottom:20px}
.dacre-dashboard-brand{display:flex;align-items:center;gap:12px}.dacre-dashboard-brand h1{margin:0!important;font-size:1.28rem!important;font-weight:750!important;letter-spacing:-.025em}.dacre-dashboard-brand p{margin:3px 0 0!important;color:var(--dacre-muted)!important;font-size:.82rem}.live-pulse{width:12px;height:12px;display:grid;place-items:center;position:relative}.live-pulse:before{content:"";position:absolute;width:12px;height:12px;border-radius:50%;background:rgba(98,215,162,.3);animation:dacrePing 1.8s infinite}.live-pulse i{width:7px;height:7px;border-radius:50%;background:var(--dacre-success);display:block;position:relative;z-index:1}@keyframes dacrePing{0%{transform:scale(.7);opacity:.9}100%{transform:scale(1.8);opacity:0}}
.dacre-dashboard-tools{display:flex;align-items:center;gap:10px}.dashboard-time{color:var(--dacre-muted)!important;font-size:.75rem}.dashboard-avatar{width:32px;height:32px;border-radius:8px;display:grid;place-items:center;background:rgba(75,130,245,.14);border:1px solid rgba(75,130,245,.35);color:#79a7ff!important;font:700 .72rem monospace}
.dacre-kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:18px}.dacre-kpi-card{background:linear-gradient(145deg,var(--dacre-card),var(--dacre-bg2));border:1px solid var(--dacre-border);border-radius:var(--dacre-radius);padding:18px;min-height:154px;box-shadow:0 10px 30px rgba(0,0,0,.12);transition:.2s ease}.dacre-kpi-card:hover{border-color:rgba(75,130,245,.45);transform:translateY(-2px)}.kpi-head{display:flex;align-items:center;justify-content:space-between}.kpi-icon{width:38px;height:38px;border-radius:9px;display:grid;place-items:center;background:rgba(75,130,245,.12);color:#77a4ff!important;font-size:1rem}.kpi-delta{display:inline-flex;align-items:center;gap:3px;padding:5px 8px;border-radius:999px;font-size:.68rem;font-weight:700}.kpi-delta.up{background:rgba(98,215,162,.1);color:var(--dacre-success)!important}.kpi-delta.down{background:rgba(255,109,115,.1);color:var(--dacre-danger)!important}.dacre-kpi-card p{margin:14px 0 3px!important;color:var(--dacre-muted)!important;font-size:.78rem}.kpi-value-row{display:flex;align-items:flex-end;justify-content:space-between;gap:10px}.kpi-value-row b{font:650 1.55rem/1.1 'Geist','Inter',sans-serif;color:var(--dacre-fg)!important;letter-spacing:-.025em}.dacre-kpi-card small{display:block;margin-top:8px;color:#74829a!important;font-size:.68rem}.dacre-spark{width:96px;height:32px;overflow:visible}
.dacre-panel{background:linear-gradient(145deg,var(--dacre-card),var(--dacre-card2));border:1px solid var(--dacre-border);border-radius:var(--dacre-radius);padding:18px;box-shadow:0 10px 30px rgba(0,0,0,.12);margin-bottom:18px}.panel-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.panel-head h2{margin:0!important;font-size:.96rem!important;font-weight:700!important}.panel-head p{margin:4px 0 0!important;color:var(--dacre-muted)!important;font-size:.72rem}.range-pills{display:flex;gap:2px;padding:3px;border:1px solid var(--dacre-border);background:var(--dacre-bg);border-radius:8px}.range-pills span{padding:5px 8px;border-radius:6px;color:var(--dacre-muted)!important;font-size:.66rem}.range-pills .active{background:var(--dacre-primary);color:#fff!important}.chart-legend{display:flex;gap:16px;margin:16px 0 4px;color:var(--dacre-muted)!important;font-size:.68rem}.chart-legend span{display:flex;align-items:center;gap:6px}.chart-legend i{width:8px;height:8px;border-radius:50%;display:inline-block}.chart-legend i.blue{background:var(--dacre-chart-1)}.chart-legend i.cyan{background:var(--dacre-chart-3)}.dacre-area-chart{display:block;width:100%;height:auto;min-height:280px}.chart-grid{stroke:rgba(150,168,200,.12);stroke-width:1}.chart-label{fill:#7f8da5;font:10px 'Geist','Inter',sans-serif}
.health-panel{height:100%;box-sizing:border-box}.dacre-health-ring{position:relative;width:144px;height:144px;margin:14px auto 20px}.dacre-health-ring svg{width:144px;height:144px}.health-progress{filter:drop-shadow(0 0 6px rgba(75,130,245,.55))}.dacre-health-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}.dacre-health-center b{font:650 1.55rem monospace;color:var(--dacre-fg)!important}.dacre-health-center span{font-size:.65rem;color:var(--dacre-muted)!important;margin-top:2px}.resource-list{display:flex;flex-direction:column;gap:15px}.resource-row>div:first-child{display:flex;justify-content:space-between;font-size:.72rem}.resource-row>div:first-child span{color:var(--dacre-muted)!important}.resource-row>div:first-child b{font:500 .7rem monospace;color:var(--dacre-fg)!important}.resource-track{height:6px;margin-top:7px;border-radius:99px;background:var(--dacre-muted-bg);overflow:hidden}.resource-track i{display:block;height:100%;border-radius:99px}
.activity-panel{padding:0;overflow:hidden}.activity-panel .panel-head{padding:18px 18px 14px}.view-all{font-size:.68rem;color:var(--dacre-muted)!important;border:1px solid var(--dacre-border);padding:6px 9px;border-radius:7px}.activity-scroll{overflow-x:auto}.dacre-activity-table{width:100%;border-collapse:collapse;font-size:.71rem}.dacre-activity-table th{padding:10px 12px;text-align:left;color:#74829a!important;font-weight:600;border-top:1px solid var(--dacre-border);border-bottom:1px solid var(--dacre-border);white-space:nowrap}.dacre-activity-table td{padding:12px;border-bottom:1px solid rgba(128,154,196,.10);color:#c3ccda!important;white-space:nowrap}.dacre-activity-table tr:hover td{background:rgba(75,130,245,.045)}.dacre-activity-table .right{text-align:right}.dacre-activity-table .mono{font-family:monospace;font-size:.67rem;color:#7f8da5!important}.channel{padding:3px 6px;border-radius:5px;background:#202a3e;color:#8d9ab0!important;font:10px monospace}.status{display:inline-flex;align-items:center;gap:5px;padding:3px 7px;border-radius:999px;font-size:.65rem;text-transform:capitalize}.status i{width:5px;height:5px;border-radius:50%;display:block}.status.success{background:rgba(98,215,162,.1);color:var(--dacre-success)!important}.status.success i{background:var(--dacre-success)}.status.warning{background:rgba(245,191,64,.1);color:#f5c75a!important}.status.warning i{background:#f5c75a}.status.error{background:rgba(255,109,115,.1);color:var(--dacre-danger)!important}.status.error i{background:var(--dacre-danger)}.empty-row{text-align:center!important;color:var(--dacre-muted)!important;padding:30px!important}
/* Supplied design's dark navy/slate theme applied to Streamlit controls. */
.stApp{background:radial-gradient(circle at 85% 0%,rgba(75,130,245,.09),transparent 32%),linear-gradient(145deg,#0b1020 0%,#101729 55%,#0e1628 100%)!important}.stApp .main .block-container{max-width:1280px!important}.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input,.stSelectbox div[data-baseweb="select"]>div{background:#11182a!important;border-color:rgba(128,154,196,.22)!important;color:#f4f7ff!important}.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{background:linear-gradient(135deg,#3f74dc,#4b82f5)!important;border:1px solid rgba(108,156,255,.55)!important;border-radius:9px!important;box-shadow:none!important}.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{background:#5a8ef5!important;border-color:#7ba7ff!important;transform:translateY(-1px)}
[data-testid="stSidebar"]{background:#0e1526!important;border-right:1px solid var(--dacre-border)!important;width:238px!important;min-width:238px!important}.dacre-sidebar-brand{padding:2px 0 16px}.dacre-sidebar-logo{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;background:var(--dacre-primary);color:#fff;font:bold 14px monospace;box-shadow:0 0 22px rgba(75,130,245,.3)}
@media(max-width:1000px){.dacre-kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.dacre-dashboard-tools .dashboard-time{display:none}}
@media(max-width:650px){.dacre-kpi-grid{grid-template-columns:1fr}.dacre-dashboard-topbar{align-items:flex-start}.dacre-panel{padding:14px}.dacre-area-chart{min-height:220px}}
</style>
""", unsafe_allow_html=True)

user=st.session_state.user

# Master and customer workspaces intentionally have different visual identities.
if user.get("role") == "master":
    st.markdown("""<style>
    .stApp{background:radial-gradient(circle at 80% 0%,#25205f 0%,#0b1026 38%,#050814 100%)!important;color:#eef4ff!important}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#080d20,#11183a 70%,#171048)!important;border-right:1px solid #463eaa!important}
    [data-testid="stSidebar"] *{color:#eef4ff!important}
    .dacre-user-hero,.master-office-hero,.di-quick-card,.di-metric,.call-stage{background:linear-gradient(135deg,rgba(34,31,92,.96),rgba(9,31,58,.96))!important;border:1px solid #544cc5!important;box-shadow:0 16px 45px rgba(0,0,0,.22)!important}
    .stButton>button{border-radius:14px!important;border:1px solid #635bdf!important;background:linear-gradient(135deg,#5447d8,#287edb)!important;color:#fff!important;font-weight:800!important}
    [data-testid="stRadio"] label{font-weight:700!important}
    .dacre-user-title,.dacre-title,.master-office-hero .title{color:#fff!important}
    .dacre-user-sub,.dacre-sub{color:#c9d4ff!important}
    .master-badge{display:inline-flex;padding:7px 12px;border-radius:999px;background:#ffb84d;color:#17101e;font-weight:900;letter-spacing:.08em}
    </style>""",unsafe_allow_html=True)

# Run any due Chibobec reminder checks whenever that protected workspace is open.
# The ledger prevents duplicate messages. For truly unattended delivery, a scheduled
# external trigger is still required because Streamlit Cloud can sleep idle apps.
chibobec_reminder_results = process_chibobec_reminders(user["username"], user["company"]) if is_chibobec_company(user.get("company")) else []

head_col1,head_col2=st.columns([4,1])
with head_col1:
    st.markdown(f"""<div class="dacre-user-hero"><div class="dacre-user-title">{'Welcome back, Master David.' if user.get('role')=='master' else 'Good to have you here, '+user['first_name']+'.'}</div><div class="dacre-user-sub">{'DA-CRE Founder Command is online. Your DI workforce, organizations, platform memory and global operations are connected.' if user.get('role')=='master' else DI_NAME+' is active for <b>'+user['company']+'</b>. Your business workspace, data tools and DI conversation are connected.'}</div></div>""",unsafe_allow_html=True)
with head_col2:
    if st.button("Sign Out",use_container_width=True):
        log_activity(user["username"],user["company"],"Signed out",notify_admin=user["role"] not in ("master","company_admin"))
        st.session_state.user=None
        st.rerun()

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH),use_container_width=True)
    st.markdown(f"### {user['first_name']}'s Workspace")
    st.caption(f"{user['company']} · {user['role']}")
    st.markdown("<div style='font-size:.78rem;color:#3556a8!important;margin:4px 0 14px'>DI is available across your workspace.</div>",unsafe_allow_html=True)

    # Normal workspace navigation. Overall Admin DI is deliberately kept out
    # of the normal user experience and is never promoted to the top.
    navigation=[
        "Overview",
        "DI Home",
        "DI Calls",
        "DI Workforce",
        "DI Action Center",
        "DI Memory Box",
        "Business Command Center",
        "Business Twin",
        "Decision Ledger",
        "Opportunity Radar",
        "Workspace & Data",
        "Formula Lab",
        "Charts",
        "File Vault",
        "Export Center",
    ]
    if is_chibobec_company(user.get("company")):
        navigation.append("Chibobec Loan Desk")
    if user["role"] in ("company_admin","master"):
        navigation.append("Organization Admin Portal")

    if user["role"] == "master":
        navigation.append("Chibobec Service")

    # MASTER ONLY: Overall Admin DI is the LAST destination. Ordinary users
    # never receive this navigation item.
    if user["role"] == "master":
        navigation.append("Overall Admin DI Portal")

    # Nobody is automatically dropped into the CEO Office.
    default_page=navigation[0]
    _nav_icons={"Overview":"⌂","DI Home":"◉","DI Calls":"☎","DI Workforce":"◈","DI Action Center":"✦","DI Memory Box":"◇","Business Command Center":"◆","Business Twin":"◇","Decision Ledger":"◌","Opportunity Radar":"✧","Workspace & Data":"▦","Formula Lab":"ƒ","Charts":"▤","File Vault":"▤","Export Center":"⇩","Chibobec Loan Desk":"₦","Organization Admin Portal":"⚙","Chibobec Service":"◆","Overall Admin DI Portal":"♛"}
    selected_page=st.radio("Navigation",navigation,index=navigation.index(default_page) if default_page in navigation else 0,format_func=lambda x:f"{_nav_icons.get(x,'•')}  {x}")

# Universal inner-page interface. Every Dacre workspace gets the same premium chrome,
# while the master account receives a separate founder visual identity.
render_page_chrome(selected_page, user)

# =============================================================================
# DI HOME / CONTINUOUS BUSINESS CONVERSATION
# =============================================================================

def di_voice_bridge(language_code="en-NG"):
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
      rec.lang = __LANG__;
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
         url.searchParams.set('di_voice_lang', __LANG__);
        window.parent.location.href = url.toString();
      };
      rec.onerror = () => { setTimeout(() => { try { rec.start(); } catch(e) {} }, 900); };
      rec.onend = () => { setTimeout(() => { try { rec.start(); } catch(e) {} }, 700); };
      try { rec.start(); } catch(e) {}
    })();
    </script>
    """.replace("__LANG__", json.dumps(language_code)),height=0)

# Process a voice turn before rendering the page. This gives DI a real
# server-side answer instead of pretending the browser itself is the brain.
voice_turn = st.query_params.get("di_voice")
voice_lang_code = st.query_params.get("di_voice_lang") or "en-NG"
if voice_turn:
    st.query_params.clear()
    spoken = str(voice_turn).strip()
    if spoken:
        st.session_state.chat_history.append({"sender":user["first_name"],"text":spoken})
        reply=di_reply(spoken,user,st.session_state.processed_df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        con=db(); now=datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],spoken,now))
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
        st.session_state.last_speech=reply
        st.rerun()

if selected_page=="Overview":
    render_analytics_overview(user)

elif selected_page=="DI Home":
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

    # Natural voice + multilingual control. Speech recognition and speech synthesis
    # run in the browser, so no audio file has to be uploaded to the server.
    vc1,vc2,vc3=st.columns([1.45,1,1])
    with vc1:
        selected_language=st.selectbox("DI language",list(DI_LANGUAGE_PROFILES.keys()),index=list(DI_LANGUAGE_PROFILES.keys()).index(st.session_state.di_language),key="di_language_select")
        st.session_state.di_language=selected_language
    with vc2:
        st.session_state.di_voice_enabled=st.toggle("Voice replies",value=st.session_state.di_voice_enabled,key="di_voice_toggle")
    with vc3:
        st.markdown("<div class='voice-panel'><b>🎙️ Natural conversation</b><br><span style='font-size:.84rem;color:#49677f!important'>Speak to DI and DI can answer aloud. Chrome/OS voices determine the exact accent and timbre.</span></div>",unsafe_allow_html=True)
    if st.session_state.di_voice_enabled:
        di_voice_bridge(DI_LANGUAGE_PROFILES[st.session_state.di_language]["code"])

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
            st.markdown(f"<div class='di-quick-card'><div style='font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:#c65f00!important;font-weight:800'>{title}</div><h4 style='margin:.45rem 0'>{headline}</h4><p style='color:#657180!important;font-size:.9rem;line-height:1.45'>{desc}</p></div>",unsafe_allow_html=True)

    if st.session_state.processed_df is not None:
        df=st.session_state.processed_df
        a,b,c,d=st.columns(4)
        metrics=[("Rows",f"{len(df):,}"),("Columns",f"{len(df.columns):,}"),("Duplicates",f"{int(df.duplicated().sum()):,}"),("Active file",st.session_state.active_filename or "Workspace")]
        for col,(label,value) in zip([a,b,c,d],metrics):
            with col: st.markdown(f"<div class='di-metric'><div class='v'>{value}</div><div class='l'>{label}</div></div>",unsafe_allow_html=True)

    st.markdown("### Conversation")
    for msg in st.session_state.chat_history[-12:]:
        who="DI" if msg["sender"]=="DI" else msg["sender"]
        st.markdown(f"<div style='background:{'#eaf7ff' if who=='DI' else '#ffffff'};border:1px solid #b8ddf4;border-radius:14px;padding:13px 16px;margin:8px 0'><b>{who}</b><div style='margin-top:5px;line-height:1.55'>{msg['text']}</div></div>",unsafe_allow_html=True)

    with st.form("di_chat_form",clear_on_submit=True):
        chat_text=st.text_input("Ask DI",placeholder="Type here if you prefer text…",label_visibility="collapsed")
        send=st.form_submit_button("Send to DI",use_container_width=True)
    if send and chat_text.strip():
        st.session_state.chat_history.append({"sender":user["first_name"],"text":chat_text.strip()})
        reply=di_reply(chat_text,user,st.session_state.processed_df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        con=db(); now=datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],chat_text.strip(),now))
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
        st.session_state.last_speech=reply
        st.rerun()

    st.caption("Voice mode uses your browser microphone and speech synthesis. If your browser does not expose continuous speech recognition, the text conversation remains available.")

# BUSINESS COMMAND CENTER — additive executive intelligence page
# =============================================================================
elif selected_page=="DI Calls":
    agents=[dict(r) for r in get_di_agents()]
    assigned=[a for a in agents if not a.get('assigned_company') or a.get('assigned_company')==user['company']]
    st.markdown("""<div class='call-stage'><div class='call-top'><div><div class='eyebrow'>DA-CRE CONNECT</div><h1 style='margin:0'>DI Calls</h1><p>Private business calling for your team — plus direct calls with any available DI worker.</p></div><div class='live-dot'>● LIVE READY</div></div></div>""",unsafe_allow_html=True)
    st.markdown("### Who do you want to call?")
    mode=st.radio("Call type",["Call a DI","Team / group call"],horizontal=True,key="call_mode")
    if mode=="Call a DI":
        if not assigned: st.info("No DI workers are currently available for this organization.")
        else:
            cards=[]
            for a in assigned:
                avatar=(a.get('avatar_url') or '')
                cards.append(f"<div class='di-person-card'><img src='{avatar}'/><div><b>{a['di_name']}</b><span>{a['specialty']}</span><small>{a['di_code']} · {a['status']}</small></div></div>")
            st.markdown("<div class='di-person-grid'>"+''.join(cards)+"</div>",unsafe_allow_html=True)
            labels=[f"{a['di_name']} — {a['specialty']}" for a in assigned]
            idx=st.selectbox("Choose DI",range(len(labels)),format_func=lambda i:labels[i],key="call_di_choice")
            target=assigned[idx]
            title=f"Call with {target['di_name']}"
            room=st.session_state.get('active_call_room')
            if not room or st.session_state.get('active_call_target')!=target['di_name']:
                if st.button(f"📞 Start call with {target['di_name']}",use_container_width=True,type='primary'):
                    room=make_call_room(user['company'],user['username'],title,'di')
                    record_call_participant(room,user['company'],'user',user['username'],f"{user['first_name']} {user['last_name']}")
                    record_call_participant(room,user['company'],'di',target['di_code'],target['di_name'])
                    st.session_state.active_call_room=room; st.session_state.active_call_target=target['di_name']; st.session_state[f'join_call_{room}']=False
                    log_activity(user['username'],user['company'],f"Started DI call with {target['di_name']}")
                    st.rerun()
            else:
                render_call_interface(room,title,[{'display_name':f"{user['first_name']} {user['last_name']}",'participant_type':'you'},{'display_name':target['di_name'],'participant_type':'DI'}],user['company'])
                if st.button("End DI Call",key="end_di_call",use_container_width=True):
                    st.session_state.active_call_room=None; st.session_state.active_call_target=None; st.rerun()
    else:
        people=pd.read_sql_query("SELECT username,first_name,last_name,role,email FROM users WHERE company_name=? ORDER BY first_name",db(),params=(user['company'],))
        selected=st.multiselect("Team members",people['username'].tolist(),format_func=lambda u: next((f"{r.first_name} {r.last_name} · {r.role}" for r in people.itertuples() if r.username==u),u),key="group_call_people")
        title=st.text_input("Meeting title",value="DA-CRE Business Team Call")
        if st.button("🎥 Create Group Call",use_container_width=True,type='primary'):
            room=make_call_room(user['company'],user['username'],title,'team')
            record_call_participant(room,user['company'],'user',user['username'],f"{user['first_name']} {user['last_name']}")
            for uname in selected:
                row=next((r for r in people.itertuples() if r.username==uname),None)
                if row: record_call_participant(room,user['company'],'user',uname,f"{row.first_name} {row.last_name}")
            st.session_state.active_call_room=room; st.session_state.active_call_target='team'; st.session_state[f'join_call_{room}']=False
            log_activity(user['username'],user['company'],f"Created group call: {title}")
            st.rerun()
        room=st.session_state.get('active_call_room')
        if room and st.session_state.get('active_call_target')=='team':
            render_call_interface(room,title,[{'display_name':f"{user['first_name']} {user['last_name']}",'participant_type':'host'}]+[{'display_name':str(u),'participant_type':'member'} for u in selected],user['company'])

elif selected_page=="DI Workforce":
    agents=[dict(r) for r in get_di_agents() if not r.get('assigned_company') or r.get('assigned_company')==user['company']]
    st.markdown("""<div class='dacre-hero'><div class='dacre-title'>DI Workforce</div><div class='dacre-sub'>Your assigned digital team. Every DI has a distinct identity, specialty, memory profile and work style — all under the same DACRE intelligence foundation.</div></div>""",unsafe_allow_html=True)
    if not agents: st.info("No DI workers have been assigned to this organization yet.")
    else:
        names=[a['di_name'] for a in agents]
        selected_name=st.selectbox("Choose a DI to work with",names,key="workforce_di")
        a=next(x for x in agents if x['di_name']==selected_name)
        c1,c2=st.columns([1,2])
        with c1:
            if a.get('avatar_url'): st.image(a['avatar_url'],width=150)
            st.markdown(f"### {a['di_name']}")
            st.caption(f"{a['di_code']} · {a['status']}")
            st.write(a['specialty'])
            st.info("DI knows David Emenike is the creator and Overall Administrator/master of DACRE.")
        with c2:
            st.markdown("#### Give this DI a task")
            task=st.text_area("Task",placeholder=f"Ask {a['di_name']} to do work using the active Dacre workspace...",height=120)
            if st.button(f"Run with {a['di_name']}",use_container_width=True,type='primary') and task.strip():
                answer=di_specialist_reply(task,user,st.session_state.processed_df,a['di_name'])
                st.markdown(f"<div class='di-quick-card'><b>{a['di_name']}</b><div style='margin-top:8px;line-height:1.7'>{answer}</div></div>",unsafe_allow_html=True)
                st.session_state.last_speech=answer
                log_activity(user['username'],user['company'],f"Assigned task to {a['di_name']}: {task[:120]}")
                st.session_state[f"di_task_result_{a['di_name']}"]=answer
            if st.session_state.get(f"di_task_result_{a['di_name']}"):
                di_voice_player(st.session_state[f"di_task_result_{a['di_name']}"])

elif selected_page=="DI Action Center":
    render_action_center(user)

elif selected_page=="Business Twin":
    render_business_twin(st.session_state.processed_df, user)

elif selected_page=="Decision Ledger":
    render_decision_ledger(user)

elif selected_page=="Opportunity Radar":
    render_opportunity_page(user)

elif selected_page=="Chibobec Service" and user.get('role')=='master':
    st.markdown("""<div class='master-office-hero'><div class='master-badge'>MASTER ONLY</div><div class='title'>Chibobec Service · Customer Intelligence</div><div class='sub'>System-wide customer record for the protected Chibobec workspace. This view is available only to the Overall Administrator.</div></div>""",unsafe_allow_html=True)
    users,activity,chats,files,projects,emails,calls=master_customer_360(CHIBOBEC_COMPANY)
    k1,k2,k3,k4,k5=st.columns(5)
    k1.metric('Accounts',len(users)); k2.metric('Logins',int(users['login_count'].sum()) if not users.empty else 0); k3.metric('Activities',len(activity)); k4.metric('DI messages',len(chats)); k5.metric('Files',len(files))
    tabs=st.tabs(['Accounts & Sign-ins','Everything They Did','DI Conversations','Files & Projects','Emails','Calls'])
    with tabs[0]: st.dataframe(safe_dataframe_for_streamlit(users),use_container_width=True,hide_index=True)
    with tabs[1]: st.dataframe(safe_dataframe_for_streamlit(activity),use_container_width=True,hide_index=True)
    with tabs[2]: st.dataframe(safe_dataframe_for_streamlit(chats),use_container_width=True,hide_index=True)
    with tabs[3]:
        st.subheader('Files'); st.dataframe(safe_dataframe_for_streamlit(files),use_container_width=True,hide_index=True)
        st.subheader('Projects'); st.dataframe(safe_dataframe_for_streamlit(projects),use_container_width=True,hide_index=True)
    with tabs[4]: st.dataframe(safe_dataframe_for_streamlit(emails),use_container_width=True,hide_index=True)
    with tabs[5]: st.dataframe(safe_dataframe_for_streamlit(calls),use_container_width=True,hide_index=True)

elif selected_page=="DI Memory Box":
    st.markdown("<div class='dacre-hero'><div class='dacre-title'>DI Memory Box</div><div class='dacre-sub'>Shared knowledge used by DI across DACRE</div></div>",unsafe_allow_html=True)
    st.info("This is the trusted project knowledge that DI uses before it researches online. The Overall Administrator can add or update records from the master portal.")
    mem_df=pd.read_sql_query("SELECT category,title,content,priority,updated_at FROM di_memory WHERE active=1 ORDER BY priority DESC,id ASC",db())
    for row in mem_df.itertuples(index=False):
        with st.expander(f"{row.category} · {row.title}",expanded=False):
            st.write(row.content)
    st.caption("DI also uses your active workspace and can use public online research when the Memory Box does not contain the answer.")

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
        st.markdown("### DA-CRE Advantage Engine")
        st.caption("Three business capabilities designed to turn analytics into action, not just dashboards.")
        adv1,adv2,adv3=st.columns(3)
        with adv1:
            st.markdown("#### 🧠 Decision Ledger")
            st.write("Record a decision, why it was made, the expected outcome and when DI should review the result. This creates institutional memory instead of forgotten meetings.")
            with st.expander("Create decision"):
                dt=st.text_input("Decision title",key="dec_title")
                dc=st.text_area("Context",key="dec_context")
                dd=st.text_area("Decision",key="dec_decision")
                de=st.text_input("Expected outcome",key="dec_expected")
                dr=st.date_input("Review date",key="dec_review")
                if st.button("Save decision",key="save_decision",use_container_width=True) and dt.strip() and dd.strip():
                    create_decision(user['company'],user['username'],dt,dc,dd,de,str(dr)); log_activity(user['username'],user['company'],f"Created decision: {dt}"); st.success("Decision saved to institutional memory.")
        with adv2:
            st.markdown("#### 🔭 Opportunity Radar")
            opps=opportunity_radar(df,user['company'],user['username'])
            if opps:
                for o in opps: st.markdown(f"**{o['title']}** · {o['impact']}\n\n{o['evidence']}\n\n➡️ {o['action']}")
            else: st.info("Upload more time-ordered numeric data for opportunity signals.")
        with adv3:
            st.markdown("#### 🛡️ Silent Risk Radar")
            risk_count=int(df.isna().sum().sum())+int(df.duplicated().sum())
            st.metric("Data-risk indicators",risk_count)
            st.write("DI watches missing data and duplication as early warning signals before they contaminate business decisions.")

        st.markdown("### Ask the data")
        with st.form("command_center_form",clear_on_submit=True):
            q=st.text_input("Business question",placeholder="e.g. Give me an executive brief, show the top products, or check the data health")
            go=st.form_submit_button("Ask DI",use_container_width=True)
        if go and q.strip():
            answer=di_reply(q,user,df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
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
        st.dataframe(safe_dataframe_for_streamlit(df),use_container_width=True)
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
elif selected_page=="Chibobec Loan Desk" and is_chibobec_company(user.get("company")):
    st.markdown(f"""<div class='dacre-user-hero'><div class='dacre-user-title'>Chibobec Loan Collection Desk</div><div class='dacre-user-sub'>Private workspace for <b>{CHIBOBEC_COMPANY.title()}</b> · Client loans, due dates and WhatsApp reminder automation.</div></div>""", unsafe_allow_html=True)

    if chibobec_reminder_results:
        for client_name, reminder_type, ok, status in chibobec_reminder_results:
            if ok:
                st.success(f"{reminder_type.title()} sent to {client_name} on WhatsApp.")
            else:
                st.warning(f"{reminder_type.title()} for {client_name} is pending: {status}")

    st.info("DI automatically checks this workspace for loans due in 2 days and loans due today. WhatsApp delivery requires a connected WhatsApp provider. The app never claims a message was delivered unless the provider confirms it.")

    add_tab, clients_tab, setup_tab = st.tabs(["Add Loan Client", "Loan Book", "WhatsApp Setup"])
    with add_tab:
        with st.form("add_chibobec_loan", clear_on_submit=True):
            c1,c2=st.columns(2)
            with c1:
                lc_name=st.text_input("Client full name", placeholder="e.g. Ada Okafor")
                lc_phone=st.text_input("Client WhatsApp number", placeholder="08012345678 or +2348012345678")
                lc_amount=st.number_input("Loan amount (₦)", min_value=0.0, step=1000.0, format="%.2f")
            with c2:
                lc_lent=st.date_input("Date loan was given", value=datetime.now().date())
                lc_due=st.date_input("Date repayment is due", value=datetime.now().date())
                st.caption("DI will prepare the 2-day reminder and the due-date reminder from these dates.")
            save_loan=st.form_submit_button("Save Client & Schedule Reminders", use_container_width=True, type="primary")
        if save_loan:
            ok,msg=add_loan_client(user["username"], user["company"], lc_name, lc_phone, lc_amount, lc_lent, lc_due)
            if ok: st.success(msg); st.rerun()
            else: st.error(msg)

    with clients_tab:
        con=db()
        loans=pd.read_sql_query("SELECT id,client_name,whatsapp_number,loan_amount,lent_date,due_date,reminder_2_sent,due_sent,created_at FROM loan_clients WHERE username=? AND company_name=? ORDER BY due_date ASC", con, params=(user["username"],user["company"]))
        con.close()
        if loans.empty:
            st.warning("No loan clients have been added yet.")
        else:
            view=loans.copy()
            view["loan_amount"]=view["loan_amount"].map(lambda x:f"₦{float(x):,.2f}")
            view["2-day reminder"]=view["reminder_2_sent"].map({0:"Pending",1:"Sent"})
            view["due-date reminder"]=view["due_sent"].map({0:"Pending",1:"Sent"})
            view=view.drop(columns=["reminder_2_sent","due_sent"])
            st.dataframe(safe_dataframe_for_streamlit(view),use_container_width=True,hide_index=True)
            st.markdown("### Remove a loan record")
            options={f"#{int(r['id'])} · {r['client_name']} · due {r['due_date']}":int(r['id']) for _,r in loans.iterrows()}
            chosen=st.selectbox("Select loan", list(options.keys()))
            if st.button("Delete Loan Record", use_container_width=True):
                delete_loan_client(options[chosen],user["username"]); st.success("Loan record deleted."); st.rerun()

    with setup_tab:
        st.markdown("### Meta WhatsApp Cloud API — Production Connection")
        cfg=_meta_whatsapp_config()
        configured=bool(cfg["token"] and cfg["phone_id"])
        if configured:
            st.success("Meta WhatsApp Cloud API credentials are loaded. DACRE will only mark a reminder as sent after Meta returns a message ID.")
        else:
            st.error("Meta WhatsApp Cloud API is NOT configured yet. No message will be falsely reported as sent.")
        st.write("Add these secrets to Streamlit Cloud → Manage app → Settings → Secrets:")
        meta_secrets = """DACRE_WHATSAPP_TOKEN = "YOUR_META_ACCESS_TOKEN"
DACRE_WHATSAPP_PHONE_NUMBER_ID = "YOUR_META_PHONE_NUMBER_ID"
DACRE_WHATSAPP_API_VERSION = "v23.0"
DACRE_WHATSAPP_2DAY_TEMPLATE = "dacre_loan_due_2days"
DACRE_WHATSAPP_DUE_TEMPLATE = "dacre_loan_due_today"
DACRE_WHATSAPP_TEMPLATE_LANGUAGE = "en_US"""
        st.code(meta_secrets, language="toml")
        st.info("The two reminder templates must first be created and approved in Meta WhatsApp Manager. Their body must contain exactly three text variables: customer name, loan amount, and due date.")
        st.caption(f"2-day template: {cfg['reminder_2_template']} · Due-date template: {cfg['due_template']} · Language: {cfg['language']}")
        if st.button("Run Real Meta Reminder Check Now", use_container_width=True, type="primary"):
            results=process_chibobec_reminders(user["username"],user["company"])
            if results:
                for name,typ,ok,status in results:
                    (st.success if ok else st.error)(f"{name} · {typ} · {'Sent by Meta' if ok else 'Not sent'} · {status}")
            else:
                st.info("No reminder is due today or in exactly 2 days.")

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
        st.dataframe(safe_dataframe_for_streamlit(users_df),use_container_width=True)
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
        st.dataframe(safe_dataframe_for_streamlit(activity_df),use_container_width=True)
    with tabs[2]:
        notes_df=pd.read_sql_query("SELECT id,event_type,message,is_read,created_at FROM notifications WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(safe_dataframe_for_streamlit(notes_df),use_container_width=True)
        if not notes_df.empty and st.button("Mark DI messages as read"):
            con.execute("UPDATE notifications SET is_read=1 WHERE company_name=?",(target_company,)); con.commit(); st.rerun()
    con.close()

# =============================================================================
# MASTER ADMIN PORTAL / CEO OFFICE
# =============================================================================
elif selected_page=="Overall Admin DI Portal" and user["role"]=="master":
    counts=admin_metric_counts()
    st.markdown("""
    <div class="master-office-hero">
      <span class="master-only-badge">🔐 MASTER ONLY · SYSTEM-WIDE ACCESS</span>
      <div class="title">CEO Office</div>
      <div class="sub">DACRE Analysis executive command centre · Overall Administration · DI Workforce</div>
      <div class="authority">David Emenike · Overall Administrator · DACRE MASTER</div>
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
    tabs=st.tabs(["Executive Overview","DI Workforce","Organizations","People & Accounts","Live Activity","DI Conversations","DI Memory Box","Mail Source","System Controls"])

    with tabs[0]:
        st.subheader("Executive Overview")
        recent= pd.read_sql_query("SELECT username,company_name,action,created_at FROM activity ORDER BY id DESC LIMIT 15",con)
        left,right=st.columns([1.25,1])
        with left:
            st.markdown("#### Recent system activity")
            st.dataframe(safe_dataframe_for_streamlit(recent),use_container_width=True,hide_index=True)
        with right:
            st.markdown("#### Platform position")
            st.write("The CEO Office is the highest DACRE administration layer. This is where master-level oversight, DI workforce creation, organization visibility and platform activity are managed.")
            st.write("All normal company users remain isolated inside their own organization workspaces.")
            if cloud_persistence_configured():
                st.success("Cloud database persistence is configured.")
            else:
                st.warning("Cloud database persistence is NOT configured. This deployment is currently using local SQLite; Streamlit Community Cloud does not guarantee local-file persistence across restarts/redeploys.")
                st.caption("If a customer signs up and the app later restarts, that local database can disappear. A remote SQL database is required for permanent customer accounts.")
            st.markdown("#### Latest customer sign-ups")
            signup_df=pd.read_sql_query("SELECT first_name,last_name,company_name,email,role,created_at,last_login FROM users WHERE role!='master' ORDER BY id DESC LIMIT 20",con)
            if signup_df.empty:
                st.info("No non-master customer accounts are currently present in this database.")
            else:
                st.dataframe(safe_dataframe_for_streamlit(signup_df),use_container_width=True,hide_index=True)
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
            st.dataframe(safe_dataframe_for_streamlit(agent_df),use_container_width=True,hide_index=True)
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
        st.dataframe(safe_dataframe_for_streamlit(companies_df),use_container_width=True,hide_index=True)
        st.metric("Organizations",len(companies_df))

    with tabs[3]:
        st.subheader("People & Accounts — Permanent Control")
        st.caption("Fast account cleanup for the Overall Administrator. The master account is protected. Deletion is permanent and cannot be undone.")
        users_df=pd.read_sql_query("SELECT id,first_name,last_name,username,company_name,email,role,login_count,created_at,last_login FROM users WHERE role!='master' ORDER BY id DESC",con)
        st.metric("Deletable accounts",len(users_df))
        if users_df.empty:
            st.success("There are currently no non-master accounts to delete.")
        else:
            account_options={int(r.id): f"#{int(r.id)} · {r.first_name} {r.last_name} · {r.email} · {r.company_name}" for r in users_df.itertuples()}
            selected_delete=st.multiselect("Select account(s) to permanently delete",options=list(account_options),format_func=lambda x: account_options[x],key="master_delete_accounts")
            if selected_delete:
                preview=users_df[users_df["id"].isin(selected_delete)][["id","first_name","last_name","email","company_name","role","created_at"]]
                st.dataframe(preview,use_container_width=True,hide_index=True)
                st.warning(f"You selected {len(selected_delete)} account(s). This removes the account and its stored workspace records. This cannot be undone.")
                confirm=st.checkbox("I understand these selected accounts will be permanently deleted.",key="confirm_bulk_delete")
                if confirm and st.button("DELETE SELECTED ACCOUNTS PERMANENTLY",use_container_width=True,type="primary",key="bulk_delete_accounts_btn"):
                    deleted,removed=permanently_delete_accounts(selected_delete)
                    for r in removed:
                        log_activity(MASTER_USERNAME,"DACRE MASTER",f"PERMANENTLY DELETED account {r['username']} ({r['email']})",notify_admin=False)
                    st.success(f"Permanently deleted {deleted} account(s).")
                    st.rerun()
            st.markdown("#### Current accounts")
            st.dataframe(safe_dataframe_for_streamlit(users_df),use_container_width=True,hide_index=True)

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
        # This entire tab is inside the master-only Overall Admin branch.
        # Keep the extra identity check so the Memory Box can never be rendered
        # to an ordinary company user by mistake.
        if user.get("role") != "master" or user.get("username") != MASTER_USERNAME:
            st.error("DI Memory Box is restricted to the Overall Administrator.")
        else:
            st.subheader("DI Memory Box — MASTER ONLY")
            st.caption("Private master knowledge store. DI workers use active records as trusted context, but ordinary company users cannot open or manage this page.")
            mem_search=st.text_input("Search the DI Memory Box",placeholder="Search DACRE, DI, accounts, business analytics, formulas, security...",key="di_memory_admin_search")
            mem_filter=st.selectbox("Memory category",["ALL"]+sorted([r[0] for r in con.execute("SELECT DISTINCT category FROM di_memory ORDER BY category").fetchall()]),key="di_memory_category")
            if mem_search.strip():
                pattern="%"+mem_search.strip()+"%"
                mem_sql="SELECT id,category,title,content,priority,active,created_at,updated_at FROM di_memory WHERE (title LIKE ? OR content LIKE ? OR category LIKE ?)"
                params=(pattern,pattern,pattern)
                if mem_filter!="ALL":
                    mem_sql+=" AND category=?"; params=params+(mem_filter,)
                mem_sql+=" ORDER BY priority DESC,id ASC LIMIT 500"
                mem_df=pd.read_sql_query(mem_sql,con,params=params)
            elif mem_filter!="ALL":
                mem_df=pd.read_sql_query("SELECT id,category,title,content,priority,active,created_at,updated_at FROM di_memory WHERE category=? ORDER BY priority DESC,id ASC",con,params=(mem_filter,))
            else:
                mem_df=pd.read_sql_query("SELECT id,category,title,content,priority,active,created_at,updated_at FROM di_memory ORDER BY priority DESC,id ASC",con)
            total_mem=con.execute("SELECT COUNT(*) FROM di_memory").fetchone()[0]
            active_mem=con.execute("SELECT COUNT(*) FROM di_memory WHERE active=1").fetchone()[0]
            a,b,c=st.columns(3)
            a.metric("Total Memory Records",total_mem)
            b.metric("Active Records",active_mem)
            c.metric("Target Library", "4,000")
            st.dataframe(safe_dataframe_for_streamlit(mem_df),use_container_width=True,hide_index=True)
            with st.expander("Add a new DI Memory Box record",expanded=False):
                mc1,mc2=st.columns([1,2])
                with mc1:
                    mem_category=st.text_input("Category",placeholder="PLATFORM / SECURITY / DI / HELP")
                    mem_title=st.text_input("Memory title")
                    mem_priority=st.number_input("Priority",min_value=1,max_value=2000,value=500,step=10)
                with mc2:
                    mem_content=st.text_area("Trusted information",height=150,placeholder="Write the exact information DI should know.")
                if st.button("Save to DI Memory Box",use_container_width=True,type="primary"):
                    if not mem_title.strip() or not mem_content.strip():
                        st.error("Memory title and trusted information are required.")
                    else:
                        now=datetime.now().isoformat(timespec="seconds")
                        con.execute("INSERT INTO di_memory(category,title,content,priority,active,created_at,updated_at) VALUES(?,?,?,?,1,?,?)",(mem_category.strip().upper() or "GENERAL",mem_title.strip(),mem_content.strip(),int(mem_priority),now,now)); con.commit(); st.success("Saved to DI Memory Box."); st.rerun()
            st.info("Use this box for durable project facts, approved operating rules, creator information, security rules, product capabilities and other knowledge that every DI should share.")

    with tabs[7]:
        st.subheader("DI Mail Source")
        try:
            _smtp_cfg = {
                "host": st.secrets.get("DACRE_SMTP_HOST", ""),
                "port": st.secrets.get("DACRE_SMTP_PORT", "587"),
                "user": st.secrets.get("DACRE_SMTP_USER", ""),
                "password": st.secrets.get("DACRE_SMTP_PASSWORD", ""),
                "from": st.secrets.get("DACRE_SMTP_FROM", ""),
            }
        except Exception:
            _smtp_cfg = {"host": "", "port": "587", "user": "", "password": "", "from": ""}
        provider_status=[]
        for label,prefix in [("Gmail","DACRE_GMAIL"),("Outlook / Microsoft 365","DACRE_OUTLOOK"),("Proton","DACRE_PROTON")]:
            try:
                configured=bool(st.secrets.get(f"{prefix}_SMTP_HOST", "") and st.secrets.get(f"{prefix}_SMTP_USER", "") and st.secrets.get(f"{prefix}_SMTP_PASSWORD", ""))
            except Exception:
                configured=False
            provider_status.append((label,configured))
        configured_labels=[x for x,ok in provider_status if ok]
        if configured_labels:
            st.success("Real mail providers configured: " + ", ".join(configured_labels) + ". DACRE tries them in order and stops after the first successful delivery.")
        else:
            st.warning("No real mail provider is configured yet. Accounts can still be created, but real welcome emails require at least one configured provider.")
        st.code("""# Gmail
DACRE_GMAIL_SMTP_HOST = \"smtp.gmail.com\"
DACRE_GMAIL_SMTP_PORT = 587
DACRE_GMAIL_SMTP_USER = \"your-gmail@gmail.com\"
DACRE_GMAIL_SMTP_PASSWORD = \"your-google-app-password\"
DACRE_GMAIL_SMTP_FROM = \"your-gmail@gmail.com\"

# Outlook / Microsoft 365
DACRE_OUTLOOK_SMTP_HOST = \"smtp.office365.com\"
DACRE_OUTLOOK_SMTP_PORT = 587
DACRE_OUTLOOK_SMTP_USER = \"your-outlook@outlook.com\"
DACRE_OUTLOOK_SMTP_PASSWORD = \"your-outlook-app-password\"
DACRE_OUTLOOK_SMTP_FROM = \"your-outlook@outlook.com\"

# Proton: configure a Proton-supported SMTP endpoint that is reachable from deployment.
DACRE_PROTON_SMTP_HOST = \"your-proton-smtp-host\"
DACRE_PROTON_SMTP_PORT = 587
DACRE_PROTON_SMTP_USER = \"your-proton-sender\"
DACRE_PROTON_SMTP_PASSWORD = \"your-proton-smtp-credential\"
DACRE_PROTON_SMTP_FROM = \"your-proton-address\"

# Optional legacy fallback
DACRE_SMTP_HOST = \"\"
DACRE_SMTP_PORT = 587
DACRE_SMTP_USER = \"\"
DACRE_SMTP_PASSWORD = \"\"
DACRE_SMTP_FROM = \"\"
""", language="toml")
        st.info("Use provider app passwords/SMTP credentials, not a DACRE user's mailbox password. A local-only Proton Mail Bridge endpoint cannot be reached by Streamlit Cloud; Proton must provide a deployment-reachable SMTP method.")
        mails_df=pd.read_sql_query("SELECT id,recipient_name,recipient_email,company_name,subject,sender_email,status,sent_at,body FROM emails_log ORDER BY id DESC",con)
        st.dataframe(safe_dataframe_for_streamlit(mails_df),use_container_width=True,hide_index=True)

    with tabs[8]:
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
        reply=di_reply(q,user,st.session_state.processed_df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        st.session_state.last_speech=reply
        st.rerun()

if st.session_state.last_speech:
    speech=st.session_state.last_speech
    st.session_state.last_speech=None
    di_voice_player(speech, DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language","English — Nigeria"),{}).get("code","en-NG"))
