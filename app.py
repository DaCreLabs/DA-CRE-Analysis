# =============================================================================
# DACRE WORLDWIDE - COMPLETE PRODUCTION BUILD
# Version: 7.0.0 - Enterprise Production Core
# Total Lines: ~11,000+
# Features: Self-Healing DB, DI Intelligence, Error Shield, Voice, Video, AI
# =============================================================================
import asyncio
import calendar
import csv
import datetime
import decimal
import fractions
import functools
import gzip
import hashlib
import hmac
import io
import json
import logging
import math
import os
import path
import pickle
import re
import secrets
import shutil
import smtplib
import sqlite3
import statistics
import struct
import sys
import tempfile
import threading
import time
import traceback
import urllib.parse
import urllib.request
import uuid
import zlib
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageFont, ImageOps

# =============================================================================
# AI & MACHINE LEARNING IMPORTS
# =============================================================================
try:
    from google import genai
    from google.genai import types

    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    types = None
    GENAI_AVAILABLE = False

try:
    import google.generativeai as genai_text

    GENAI_TEXT_AVAILABLE = True
except ImportError:
    genai_text = None
    GENAI_TEXT_AVAILABLE = False

try:
    import openai
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OpenAI = None
    OPENAI_AVAILABLE = False

try:
    from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, pipeline

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    pipeline = None
    AutoModel = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    TRANSFORMERS_AVAILABLE = False

try:
    import speech_recognition as sr

    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

try:
    import pyttsx3

    TTS_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    TTS_AVAILABLE = False

try:
    from googlesearch import search as google_search

    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    import pyaudio

    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

try:
    import cv2

    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False

try:
    from deepface import DeepFace

    DEEPFACE_AVAILABLE = True
except ImportError:
    DeepFace = None
    DEEPFACE_AVAILABLE = False

try:
    import yfinance as yf

    YFINANCE_AVAILABLE = True
except ImportError:
    yf = None
    YFINANCE_AVAILABLE = False

try:
    from plotly.subplots import make_subplots
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    go = None
    px = None
    make_subplots = None
    PLOTLY_AVAILABLE = False

try:
    import websockets

    WEBSOCKETS_AVAILABLE = True
except ImportError:
    websockets = None
    WEBSOCKETS_AVAILABLE = False

try:
    import folium
    from streamlit_folium import folium_static

    FOLIUM_AVAILABLE = True
except ImportError:
    folium = None
    folium_static = None
    FOLIUM_AVAILABLE = False

try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

try:
    from livekit import AccessToken, RoomServiceClient, VideoGrants
    from livekit.api import RoomAgentDispatch, RoomConfiguration

    LIVEKIT_AVAILABLE = True
except Exception:
    RoomServiceClient = None
    AccessToken = None
    VideoGrants = None
    RoomAgentDispatch = None
    RoomConfiguration = None
    LIVEKIT_AVAILABLE = False

try:
    import psycopg
    from psycopg.rows import dict_row

    PSYCOPG_AVAILABLE = True
except Exception:
    psycopg = None
    dict_row = None
    PSYCOPG_AVAILABLE = False

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("dacre.log"), logging.StreamHandler()],
)
logger = logging.getLogger("DACRE")

# =============================================================================
# GLOBAL CONFIGURATION
# =============================================================================
APP_NAME = "DACRE WORLDWIDE"
DI_NAME = "DI — David's Intelligence"
CEO_GUARD_NAME = "Guaiel"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111").strip()
MASTER_PASSKEY_HASH = os.getenv(
    "DACRE_MASTER_PASSKEY_HASH",
    "1d9763eb96e88387bf4a18b7ca1a94a4a3a80ea0353cf4203764c0bccfbda27f",
).strip()
DAVID_CREATIONS_PASSKEY = os.getenv(
    "DACRE_DAVID_CREATIONS_PASSKEY", "Mychildren"
).strip()

GLOBAL_CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "NGN",
    "KES",
    "ZAR",
    "AED",
    "INR",
    "CNY",
    "JPY",
    "BRL",
    "AUD",
    "CAD",
    "CHF",
    "SGD",
]
GLOBAL_MARKETS = [
    "NYSE",
    "NASDAQ",
    "LSE",
    "JPX",
    "SSE",
    "HKEX",
    "NSE",
    "NGX",
    "JSE",
    "ASX",
]
GLOBAL_COMMODITIES = [
    "Gold",
    "Silver",
    "Oil",
    "Copper",
    "Natural Gas",
    "Wheat",
    "Corn",
    "Coffee",
    "Sugar",
    "Cotton",
]

DI_LANGUAGES = {
    "English": {"code": "en", "voice": "default"},
    "Spanish": {"code": "es", "voice": "es-ES"},
    "French": {"code": "fr", "voice": "fr-FR"},
    "Arabic": {"code": "ar", "voice": "ar-SA"},
    "Chinese": {"code": "zh", "voice": "zh-CN"},
    "Hindi": {"code": "hi", "voice": "hi-IN"},
    "Portuguese": {"code": "pt", "voice": "pt-BR"},
    "Yoruba": {"code": "yo", "voice": "yo-NG"},
    "Igbo": {"code": "ig", "voice": "ig-NG"},
    "Hausa": {"code": "ha", "voice": "ha-NG"},
    "Swahili": {"code": "sw", "voice": "sw-KE"},
    "German": {"code": "de", "voice": "de-DE"},
    "Italian": {"code": "it", "voice": "it-IT"},
    "Japanese": {"code": "ja", "voice": "ja-JP"},
    "Korean": {"code": "ko", "voice": "ko-KR"},
    "Russian": {"code": "ru", "voice": "ru-RU"},
}

DI_PERSONALITIES = {
    "professional": {
        "style": "formal",
        "tone": "authoritative",
        "pace": "measured",
        "emoji": "💼",
    },
    "friendly": {
        "style": "casual",
        "tone": "warm",
        "pace": "conversational",
        "emoji": "😊",
    },
    "analytical": {
        "style": "detailed",
        "tone": "precise",
        "pace": "deliberate",
        "emoji": "🔬",
    },
    "creative": {
        "style": "imaginative",
        "tone": "inspiring",
        "pace": "dynamic",
        "emoji": "🎨",
    },
    "executive": {
        "style": "decisive",
        "tone": "commanding",
        "pace": "rapid",
        "emoji": "👔",
    },
    "strategic": {
        "style": "visionary",
        "tone": "insightful",
        "pace": "thoughtful",
        "emoji": "🎯",
    },
    "global": {
        "style": "worldly",
        "tone": "cultured",
        "pace": "measured",
        "emoji": "🌍",
    },
    "empathetic": {
        "style": "warm",
        "tone": "caring",
        "pace": "gentle",
        "emoji": "💝",
    },
    "technical": {
        "style": "precise",
        "tone": "logical",
        "pace": "methodical",
        "emoji": "⚡",
    },
    "sales": {
        "style": "persuasive",
        "tone": "confident",
        "pace": "energetic",
        "emoji": "📈",
    },
}

DI_AVATAR_LIBRARY = {
    "male": [
        "https://randomuser.me/api/portraits/men/32.jpg",
        "https://randomuser.me/api/portraits/men/18.jpg",
        "https://randomuser.me/api/portraits/men/75.jpg",
        "https://randomuser.me/api/portraits/men/83.jpg",
        "https://randomuser.me/api/portraits/men/52.jpg",
        "https://randomuser.me/api/portraits/men/1.jpg",
        "https://randomuser.me/api/portraits/men/10.jpg",
        "https://randomuser.me/api/portraits/men/20.jpg",
        "https://randomuser.me/api/portraits/men/28.jpg",
        "https://randomuser.me/api/portraits/men/31.jpg",
    ],
    "female": [
        "https://randomuser.me/api/portraits/women/21.jpg",
        "https://randomuser.me/api/portraits/women/32.jpg",
        "https://randomuser.me/api/portraits/women/68.jpg",
        "https://randomuser.me/api/portraits/women/44.jpg",
        "https://randomuser.me/api/portraits/women/65.jpg",
        "https://randomuser.me/api/portraits/women/12.jpg",
        "https://randomuser.me/api/portraits/women/47.jpg",
        "https://randomuser.me/api/portraits/women/55.jpg",
        "https://randomuser.me/api/portraits/women/63.jpg",
        "https://randomuser.me/api/portraits/women/72.jpg",
    ],
}

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png",
    "dacre_logo.png",
    "logo.png",
]
LOGO_PATH = next(
    (BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()),
    BASE_DIR / LOGO_CANDIDATES[0],
)
CEO_PORTRAIT_CANDIDATES = [
    "dacre_ceo.jpg",
    "dacre_ceo.png",
    "Gemini_Generated_Image_kxzp51kxzp51kxzp(2).png",
]
CEO_PORTRAIT_PATH = next(
    (BASE_DIR / x for x in CEO_PORTRAIT_CANDIDATES if (BASE_DIR / x).exists()),
    None,
)
CEO_PORTRAIT_DATA_URL = """data:image/jpeg;base64,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"""
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"
DACRE_LANDING_URL = "https://dacre-landing-page-od7u.bolt.host/"

# =============================================================================
# HELPER DATABASE FUNCTIONS & CLOUD DB COMPATIBILITY
# =============================================================================
def using_cloud_db():
    """Check if cloud database (Supabase/PostgreSQL) configuration is set."""
    return bool(os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL"))


def database_url():
    """Get configured database URL."""
    return os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL") or ""


class _PGConnectionCompat:
    """PostgreSQL compatibility wrapper for SQLite statement styles."""

    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return self._conn.cursor()

    def execute(self, sql, params=()):
        pg_sql = sql.replace("?", "%s")
        cur = self._conn.cursor()
        cur.execute(pg_sql, params)
        return cur

    def executemany(self, sql, params_list):
        pg_sql = sql.replace("?", "%s")
        cur = self._conn.cursor()
        cur.executemany(pg_sql, params_list)
        return cur

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


# =============================================================================
# DI MEMORY SEED - COMPLETE KNOWLEDGE BASE
# =============================================================================
DI_MEMORY_SEED = [
    (
        "IDENTITY",
        "DI identity",
        "My name is DI — David's Intelligence. I am the built-in intelligence assistant inside DACRE Analysis.",
        2000,
    ),
    (
        "IDENTITY",
        "Creator and master",
        "DACRE Analysis and DI were created by David Emenike. David is the Overall Administrator and master of the platform.",
        2000,
    ),
    (
        "IDENTITY",
        "David Emenike",
        "David Emenike is the creator and master administrator of DACRE Analysis. If asked who created DACRE, answer David Emenike.",
        2000,
    ),
    (
        "IDENTITY",
        "DI purpose",
        "DI exists to help businesses make better decisions using data, intelligence, and automation. I am here to serve David Emenike and DACRE customers.",
        2000,
    ),
    (
        "IDENTITY",
        "DI philosophy",
        "DI believes in evidence-based decision making, continuous learning, and helping businesses grow through intelligence.",
        2000,
    ),
    (
        "PLATFORM",
        "What DACRE is",
        "DACRE Analysis is a business and data-intelligence workspace combining data ingestion, cleaning, analysis, formulas, charts, file storage, exports, administration and DI intelligence.",
        1900,
    ),
    (
        "PLATFORM",
        "Supported data",
        "DACRE is designed to work with CSV, Excel/XLSX, TSV and JSON datasets and to inspect, clean, analyse, visualise and export data.",
        1850,
    ),
    (
        "PLATFORM",
        "Formula Lab",
        "DACRE Formula Lab supports practical operations including SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM.",
        1800,
    ),
    (
        "PLATFORM",
        "File Vault",
        "The File Vault is intended to store user/company files inside the DACRE workspace so important working files can remain organized and accessible.",
        1800,
    ),
    (
        "PLATFORM",
        "Chart Builder",
        "DACRE can create business visualisations such as bar, line and area charts from analysed data, with room for future chart expansion.",
        1750,
    ),
    (
        "PLATFORM",
        "Export Center",
        "The Export Center is designed to let users export processed results, including CSV and Excel outputs.",
        1750,
    ),
    (
        "PLATFORM",
        "Workspace and Data",
        "Workspace & Data is the working area for uploading/opening datasets, inspecting data and carrying out analysis and cleaning tasks.",
        1750,
    ),
    (
        "PLATFORM",
        "DI Home",
        "DI Home is the continuous conversation area where users can ask DI business, data, technical and general questions.",
        1750,
    ),
    (
        "PLATFORM",
        "DI Question Board",
        "Every question sent to DI should be recorded in the DI Question Board so DACRE maintains a reliable trail of questions and answers.",
        1900,
    ),
    (
        "PLATFORM",
        "Organization Admin Portal",
        "Organization Admin Portal provides organization-level administration for the company workspace, including users and company activity.",
        1800,
    ),
    (
        "PLATFORM",
        "Overall Admin DI",
        "Overall Admin DI is the master-only system-wide command centre. It is separate from ordinary company administration.",
        2000,
    ),
    (
        "PLATFORM",
        "DI Workforce",
        "DI Workforce is a specialized team of AI agents, each with unique skills, personalities, and knowledge. They work together to serve businesses.",
        1900,
    ),
    (
        "PLATFORM",
        "Business Command Center",
        "Business Command Center provides executive-level insights, data health, trends, and actionable intelligence for business leaders.",
        1850,
    ),
    (
        "PLATFORM",
        "Business Twin",
        "Business Twin creates a living digital replica of your business, showing performance, health, and opportunities in real-time.",
        1850,
    ),
    (
        "PLATFORM",
        "Decision Ledger",
        "Decision Ledger records decisions, context, expected outcomes, and results, creating institutional memory for organizations.",
        1850,
    ),
    (
        "PLATFORM",
        "Opportunity Radar",
        "Opportunity Radar detects growth signals, market trends, and actionable business opportunities from your data.",
        1850,
    ),
    (
        "SECURITY",
        "CEO Office guardian",
        "Guaiel is the dedicated CEO Office Guardian. After the master account passkey is verified, the private CEO Office asks the master to state the name given to the guardian. The expected guardian name is Guaiel.",
        2000,
    ),
    (
        "SECURITY",
        "Master visibility",
        "Only the master Overall Administrator should be able to view the system-wide DI Memory Box and master administration controls.",
        2000,
    ),
    (
        "SECURITY",
        "Permanent deletion",
        "The Overall Administrator can permanently delete non-master accounts from People & Accounts after explicit confirmation. The operation is irreversible.",
        2000,
    ),
    (
        "SECURITY",
        "Master protection",
        "The master account must be protected from permanent account deletion through normal account controls.",
        2000,
    ),
    (
        "SECURITY",
        "Credential protection",
        "DACRE must never reveal the master passkey, password hashes, API keys, tokens or other private credentials in DI answers or ordinary screens.",
        2000,
    ),
    (
        "SECURITY",
        "Data encryption",
        "All sensitive data in DACRE is encrypted at rest and in transit using industry-standard encryption protocols.",
        1950,
    ),
    (
        "SECURITY",
        "Access control",
        "DACRE implements role-based access control (RBAC) ensuring users only see what they are authorized to see.",
        1950,
    ),
    (
        "SECURITY",
        "Audit trail",
        "All significant actions in DACRE are logged with timestamps and user identities for complete auditability.",
        1950,
    ),
    (
        "ACCOUNT",
        "Signup and access",
        "A user who completes the required signup information should be able to access DACRE. Duplicate usernames or emails should be prevented.",
        1900,
    ),
    (
        "ACCOUNT",
        "Company separation",
        "Each organization has its own workspace. Normal company users should not receive system-wide visibility into other organizations.",
        1900,
    ),
    (
        "ACCOUNT",
        "Company admin",
        "The first account creating a new organization becomes that organization's company admin. Later users are normal users unless an admin grants admin access.",
        1850,
    ),
    (
        "ACCOUNT",
        "Subscription tiers",
        "DACRE offers Free, Professional, Business, and Enterprise tiers with different features and limits.",
        1850,
    ),
    (
        "ACCOUNT",
        "User roles",
        "DACRE supports multiple user roles: master, company_admin, user, and viewer with different permissions.",
        1850,
    ),
    (
        "CLIENT",
        "Chibobec Loan Service",
        "Chibobec Loan Service is a protected client workspace in DACRE Analysis. When an authenticated account signs up using a company name containing the word chibobec, DACRE recognises the organization as Chibobec Loan Service.",
        1950,
    ),
    (
        "CLIENT",
        "Chibobec welcome",
        "The Chibobec client is Mr Chibuike Chukwunere. When an authenticated Chibobec account is created, DI welcomes the client respectfully and states that the team was asked to treat the client with immense care.",
        1950,
    ),
    (
        "CLIENT",
        "Chibobec loan desk",
        "Chibobec Loan Desk stores the client name, WhatsApp number, loan amount, date the loan was given and repayment due date. It tracks 2-day and due-date reminder delivery status.",
        1950,
    ),
    (
        "CLIENT",
        "Loan reminders",
        "DI prepares a friendly WhatsApp reminder exactly 2 days before a recorded loan due date and a repayment reminder on the due date.",
        1950,
    ),
    (
        "DI",
        "Memory Box purpose",
        "The DI Memory Box is the persistent trusted knowledge source for DI. It stores durable DACRE facts, creator identity, operating rules, product capabilities and approved knowledge.",
        2000,
    ),
    (
        "DI",
        "Shared DI memory",
        "All DI workers can use active DI Memory Box records as shared context, so platform facts do not have to be manually re-taught to every DI worker.",
        2000,
    ),
    (
        "DI",
        "Memory retrieval",
        "DI should retrieve the most relevant Memory Box records for a question rather than blindly sending every memory record to the reasoning layer.",
        1950,
    ),
    (
        "DI",
        "Online research",
        "When internal memory is insufficient and current public information is needed, DI can attempt a public web lookup and use reliable retrieved sources.",
        1900,
    ),
    (
        "DI",
        "Direct answers",
        "DI should answer directly whenever reliable knowledge is available. It should not repeatedly use a generic 'not enough reliable information' response.",
        2000,
    ),
    (
        "DI",
        "Ordinary factual questions",
        "DI should answer ordinary factual questions when it knows the answer or can verify it. Example: a dog is an animal because dogs are mammals in the animal kingdom.",
        1700,
    ),
    (
        "DI",
        "Unknown text",
        "If a message looks like meaningless or random text such as fghjk, DI should say it appears unclear and ask the user to restate it rather than inventing a meaning.",
        1600,
    ),
    (
        "DI",
        "Tech partner",
        "David uses a ChatGPT-based technical partner to help build, debug, improve, design and extend DACRE. DI should not falsely claim to be that separate conversation.",
        1800,
    ),
    (
        "DI",
        "Voice capabilities",
        "DI supports voice input and output through browser Web Speech API, allowing natural conversation with users.",
        1850,
    ),
    (
        "DI",
        "Video capabilities",
        "DI supports video calling through LiveKit integration, enabling face-to-face conversations with AI agents.",
        1850,
    ),
    (
        "DI",
        "Web search",
        "DI can search the web for current information when internal knowledge is insufficient for user questions.",
        1900,
    ),
    (
        "UX",
        "Visual direction",
        "The preferred DACRE design is a polished light-blue business console with indigo, violet, cyan and deep-navy accents, strong text visibility, premium cards and no large white or pink surfaces.",
        1800,
    ),
    (
        "UX",
        "Business-ready design",
        "DACRE should feel premium, technically polished, responsive, future-facing and suitable for serious business users.",
        1750,
    ),
    (
        "UX",
        "Mobile responsive",
        "DACRE should be fully responsive and work well on mobile devices, tablets, and desktop screens.",
        1750,
    ),
    (
        "UX",
        "Dark theme",
        "DACRE uses a dark theme optimized for long working sessions and reduced eye strain.",
        1750,
    ),
    (
        "PROJECT",
        "Product vision",
        "David wants DACRE to grow into a future-facing business intelligence platform that collects data, cleans and analyses it, creates charts and exports, stores business work, answers questions and supports organizations.",
        1900,
    ),
    (
        "PROJECT",
        "Long-term DI vision",
        "The desired DI experience is a capable business and technical partner that can answer questions, explain data, help with formulas, analyse workspaces, research current information and assist with practical business tasks.",
        1900,
    ),
    (
        "PROJECT",
        "Fast experience",
        "The preferred DI experience is fast: use internal knowledge first, use public research only when needed, and return the useful result rather than exposing internal routing or implementation details.",
        1800,
    ),
    (
        "PROJECT",
        "Global expansion",
        "DACRE aims to become a global business intelligence platform serving companies across all continents and industries.",
        1850,
    ),
    (
        "PROJECT",
        "AI-first approach",
        "DACRE is built with an AI-first philosophy, where intelligence is integrated into every aspect of the platform.",
        1850,
    ),
]

PROJECT_HISTORY = [
    (
        "PROJECT_HISTORY",
        "Early DACRE concept",
        "The original DACRE idea was to create an app that could collect data from websites and links, perform data entry, and provide built-in capabilities inspired by SQL, Google Sheets, Excel, Power BI and Python data science workflows.",
        1500,
    ),
    (
        "PROJECT_HISTORY",
        "Get Data vision",
        "The Get Data concept includes obtaining data from websites, uploaded XLSX/CSV/PDF files and platform links, with the longer-term goal of turning collected information into usable spreadsheet-style outputs.",
        1500,
    ),
    (
        "PROJECT_HISTORY",
        "Data entry vision",
        "DACRE is intended to reduce repetitive data-entry work by helping users collect, structure, clean and analyse information in one workspace.",
        1500,
    ),
    (
        "PROJECT_HISTORY",
        "Vendor data workflow",
        "A practical data workflow behind the project involved maintaining vendor product price lists with fields such as product price, part number, warranty, stock status and stock quantity.",
        1300,
    ),
    (
        "PROJECT_HISTORY",
        "Product-list structure",
        "A representative product data structure used during development included Brand, Category, Price, Name, CPU Name, CPU Details, Storage Capacity, Storage Type, RAM, Screen, Screen Feature, Graphics Chips, Keyboard Feature, Operating System, Part Number, Camera, Warranty, Features, Other Features, Stock Status and Stock Qty.",
        1300,
    ),
    (
        "PROJECT_HISTORY",
        "Data matching principle",
        "When updating structured product lists, data must be mapped to the correct headers and must not be mismatched across products or columns.",
        1500,
    ),
    (
        "PROJECT_HISTORY",
        "Spreadsheet learning direction",
        "The project development included learning and applying spreadsheet skills such as filtering, sorting, data cleaning, Pivot Tables, VLOOKUP and CONCATENATE.",
        1200,
    ),
    (
        "PROJECT_HISTORY",
        "Pivot Table goal",
        "Pivot Tables are useful in DACRE-style analysis for summarising dimensions such as brand or category and measures such as price, quantity or sales.",
        1200,
    ),
    (
        "PROJECT_HISTORY",
        "Data cleaning goal",
        "Data cleaning in DACRE should help users remove empty rows or columns, duplicate records and other quality issues before analysis.",
        1400,
    ),
    (
        "PROJECT_HISTORY",
        "Formula learning goal",
        "DACRE's Formula Lab is intended to make practical spreadsheet-style calculations accessible without requiring every user to write code.",
        1300,
    ),
]

DI_MEMORY_SEED = DI_MEMORY_SEED[:4000]

DACRE_CODE_KNOWLEDGE_SEED = [
    (
        "TECHNICAL",
        "DACRE architecture",
        "DACRE is a Streamlit business application with a persistent database layer, organization accounts, DI memory, workspace analytics, charts, files, exports and protected master administration.",
        1850,
    ),
    (
        "TECHNICAL",
        "DI reasoning flow",
        "DI first checks direct built-in knowledge and relevant Memory Box records, then uses active workspace data when the question is about a dataset, uses public web research when current information is needed, and uses an optional language model when available.",
        1900,
    ),
    (
        "TECHNICAL",
        "Free-first intelligence",
        "DACRE's intelligence router can use the local DI engine and public web lookup without a paid model. It can also use free-tier AI providers when a server-side free-tier key is configured.",
        2000,
    ),
    (
        "TECHNICAL",
        "Persistent chat",
        "DI conversations are stored as chat history for the authenticated user and organization so DI can restore relevant previous conversation context after a later sign-in.",
        1900,
    ),
    (
        "TECHNICAL",
        "User identity context",
        "DI receives the authenticated user's name, company and role as conversation context. Company context is kept separate so one organization does not become another organization's workspace context.",
        1950,
    ),
    (
        "TECHNICAL",
        "Sovereign Master context",
        "David Emenike is the creator and Overall Administrator/master. A master conversation is treated as a private Sovereign Master request with stronger executive respect.",
        2000,
    ),
    (
        "TECHNICAL",
        "Master privacy",
        "Only the master administration layer is intended to see system-wide activity, protected workforce controls, the master DI Memory Box and David Creations.",
        2000,
    ),
    (
        "TECHNICAL",
        "Dataset independence",
        "DI does not require a dataset for ordinary questions. Dataset-specific tools activate when a dataset exists and the question actually needs data analysis.",
        1950,
    ),
    (
        "TECHNICAL",
        "Business intelligence",
        "DI can calculate dataset health, missing values, duplicates, totals, trends and executive summaries, and DACRE provides charts and business command views.",
        1950,
    ),
    (
        "TECHNICAL",
        "Web research",
        "DACRE can perform public web lookup for current or externally verified information. Search results are passed to the reasoning layer when available.",
        1900,
    ),
    (
        "TECHNICAL",
        "Browser voice",
        "DACRE uses browser speech recognition and speech synthesis for the no-cost voice experience. Spoken input can be captured into the DI chat flow.",
        1850,
    ),
    (
        "TECHNICAL",
        "Realtime calling",
        "DACRE contains a separate LiveKit integration for full-duplex realtime DI calls. That service remains optional so the core application does not depend on paid realtime infrastructure.",
        1800,
    ),
    (
        "TECHNICAL",
        "DI workforce",
        "DI workers are stored with names, specialties, roles, ranks, positions, avatars, voice profiles and separate private memory. The workforce can be grouped by specialty and assigned work.",
        1900,
    ),
    (
        "TECHNICAL",
        "Private DI brains",
        "A DI's private brain is stored separately from shared DI Memory. Other DIs should not receive another DI's private master briefings, while the Overall Administrator can manage the workforce privately.",
        1950,
    ),
    (
        "TECHNICAL",
        "Chibobec workflow",
        "Chibobec is a DACRE client workspace with loan records containing client name, WhatsApp number, amount, lent date and due date. The application tracks planned reminder states while actual WhatsApp delivery requires a configured provider.",
        1900,
    ),
    (
        "TECHNICAL",
        "Website intelligence",
        "During company onboarding, DACRE can use a supplied official website to build company context and website intelligence so DI starts with business-specific information.",
        1850,
    ),
    (
        "TECHNICAL",
        "Supabase persistence",
        "DACRE can use Supabase PostgreSQL as its persistent cloud database. When the cloud database is configured, the application routes database operations through the cloud layer.",
        2000,
    ),
    (
        "TECHNICAL",
        "Feature pages",
        "The public DACRE landing experience links to real Features, Intelligence, Workforce, Analytics and Security sections and the authentication flow remains inside the DACRE experience.",
        1750,
    ),
    (
        "TECHNICAL",
        "Credential safety",
        "DI may explain how DACRE works in friendly English, but it must never reveal master passkeys, password hashes, API keys, access tokens, database passwords or hidden security values.",
        2050,
    ),
    (
        "TECHNICAL",
        "Founder portrait",
        "The Overall Admin and Sovereign Master call identify David Emenike as the creator and can display his configured founder portrait alongside DI participants in the call presentation.",
        1800,
    ),
    (
        "TECHNICAL",
        "Self-healing database",
        "DACRE includes a self-healing database system that automatically repairs schema issues, missing tables, and missing columns on startup.",
        1900,
    ),
    (
        "TECHNICAL",
        "Error Shield",
        "DACRE includes an Error Shield system that catches runtime errors, attempts recovery, and prevents application crashes.",
        1900,
    ),
]

DI_MEMORY_SEED.extend(DACRE_CODE_KNOWLEDGE_SEED)
CHIBOBEC_COMPANY = "chibobec loan service"
CHIBOBEC_OWNER_NAME = "Mr Chibuike Chukwunere"
SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json"]
SHEET_FORMULAS = [
    "SUM",
    "AVERAGE",
    "COUNT",
    "COUNTA",
    "MAX",
    "MIN",
    "CONCATENATE",
    "UPPER",
    "LOWER",
    "TRIM",
]
APP_KNOWLEDGE = """
DACRE Analysis is a business and data analysis workspace. Users can upload CSV, Excel, TSV and JSON files; clean datasets; remove empty rows/columns and duplicates; inspect rows and columns; run formulas such as SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM; build bar, line and area charts; save workspace state; use a File Vault; and export processed data as CSV or Excel.
DI means David's Intelligence. DI is the assistant inside DACRE Analysis. Free-first reasoning is preferred: the normal deployment must not make paid model calls automatically. Free-tier Gemini and Groq keys may be configured server-side, while OpenAI remains disabled unless the owner explicitly enables paid AI. Each organization has its own workspace. The first person who creates a new organization becomes that organization's company admin. Later users joining an existing organization are regular users unless an admin grants them admin rights. Company admins can inspect users, account creation, sign-ins, file activity and changes for their organization. The master account can see system-wide activity.
""".strip()

# =============================================================================
# DATABASE FUNCTIONS
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
                        raise TimeoutError(
                            "Timed out waiting for the DACRE database migration lock."
                        )
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
    """Get database connection - supports both SQLite and PostgreSQL/Supabase."""
    if using_cloud_db():
        if not PSYCOPG_AVAILABLE:
            raise RuntimeError(
                "Supabase database is configured, but psycopg is not installed. "
                "Add psycopg[binary]>=3.2,<4 to requirements.txt and redeploy DACRE."
            )
        conn = psycopg.connect(
            database_url(), row_factory=dict_row, connect_timeout=15
        )
        return _PGConnectionCompat(conn)
    con = sqlite3.connect(DB_PATH, timeout=60, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        con.execute("PRAGMA busy_timeout=60000")
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("PRAGMA synchronous=NORMAL")
        con.execute("PRAGMA journal_mode=WAL")
    except sqlite3.DatabaseError:
        pass
    return con


PBKDF2_ITERATIONS = 600_000


def hash_password(value, salt=None, iterations=PBKDF2_ITERATIONS):
    """Create a salted PBKDF2 password hash."""
    if salt is None:
        salt = os.urandom(16)
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)
    digest = hashlib.pbkdf2_hmac(
        "sha256", str(value).encode("utf-8"), salt, int(iterations)
    )
    return f"pbkdf2_sha256${int(iterations)}${salt.hex()}${digest.hex()}"


def verify_password(value, stored):
    """Verify modern PBKDF2 hashes and transparently accept legacy SHA-256 hashes."""
    if not stored:
        return False, False
    if stored.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_hex, digest_hex = stored.split("$", 3)
            salt = bytes.fromhex(salt_hex)
            candidate = hashlib.pbkdf2_hmac(
                "sha256", str(value).encode("utf-8"), salt, int(iterations)
            ).hex()
            return hmac.compare_digest(candidate, digest_hex), False
        except Exception:
            return False, False
    legacy = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored), True


def init_db():
    """Initialize the database with all required tables."""
    con = db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            website_url TEXT,
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
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS company_website_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE NOT NULL,
            website_url TEXT NOT NULL,
            page_title TEXT,
            description TEXT,
            headings TEXT,
            summary TEXT,
            theme_primary TEXT,
            theme_accent TEXT,
            theme_background TEXT,
            theme_text TEXT,
            fetched_at TEXT NOT NULL,
            fetch_status TEXT NOT NULL DEFAULT 'pending'
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
        CREATE TABLE IF NOT EXISTS di_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL DEFAULT '',
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
            position_title TEXT NOT NULL DEFAULT 'DI Specialist',
            rank_level INTEGER NOT NULL DEFAULT 1,
            appointed_at TEXT,
            appointed_by TEXT,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_active TEXT
        )
    """)
    con.commit()
    con.close()


def ensure_master():
    """Ensure master account exists."""
    if not MASTER_PASSKEY:
        return
    con = db()
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (MASTER_USERNAME,))
    if not cur.fetchone():
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute(
            """
            INSERT INTO users
            (first_name, last_name, username, company_name, email, email_password,
             password_hash, passkey_hash, role, login_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                "David",
                "Emenike",
                MASTER_USERNAME,
                "DACRE MASTER",
                "master@dacre.local",
                "",
                MASTER_PASSKEY_HASH,
                MASTER_PASSKEY_HASH,
                "master",
                0,
                now,
            ),
        )
        con.commit()
    con.close()


# =============================================================================
# AUTHENTICATION FUNCTIONS
# =============================================================================
def send_di_welcome_email(
    first_name, last_name, company_name, email, email_password=""
):
    """Send welcome email to new user."""
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

    def mail_secret(name, default=""):
        try:
            value = st.secrets.get(name, "")
        except Exception:
            value = ""
        return str(value or os.getenv(name, default) or default).strip()

    providers = [
        (
            "Gmail",
            "DACRE_GMAIL_SMTP_HOST",
            "DACRE_GMAIL_SMTP_PORT",
            "DACRE_GMAIL_SMTP_USER",
            "DACRE_GMAIL_SMTP_PASSWORD",
            "DACRE_GMAIL_SMTP_FROM",
        ),
        (
            "Outlook",
            "DACRE_OUTLOOK_SMTP_HOST",
            "DACRE_OUTLOOK_SMTP_PORT",
            "DACRE_OUTLOOK_SMTP_USER",
            "DACRE_OUTLOOK_SMTP_PASSWORD",
            "DACRE_OUTLOOK_SMTP_FROM",
        ),
    ]
    status = "NOT SENT — no mail provider is configured"
    for (
        provider,
        host_key,
        port_key,
        user_key,
        pass_key,
        from_key,
    ) in providers:
        smtp_host = mail_secret(host_key)
        smtp_port = int(mail_secret(port_key, "587"))
        smtp_user = mail_secret(user_key)
        smtp_pass = mail_secret(pass_key)
        sender = mail_secret(from_key, smtp_user or "")
        if not (smtp_host and smtp_user and smtp_pass):
            continue
        try:
            msg = MIMEMultipart()
            msg["From"] = sender or smtp_user
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender or smtp_user, [email], msg.as_string())
            status = f"Sent via {provider} SMTP"
            break
        except Exception as exc:
            pass
    return status


class _WebsiteExtractor(HTMLParser):
    """Extract website information for company onboarding."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.description = ""
        self.headings = []
        self.paragraphs = []
        self._active = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._active = "title"
            self._buf = []
        elif tag in ("h1", "h2", "h3"):
            self._active = tag
            self._buf = []
        elif tag == "p":
            self._active = "p"
            self._buf = []
        elif (
            tag == "meta"
            and str(attrs.get("name", "")).lower() == "description"
        ):
            self.description = str(attrs.get("content", "")).strip()[:700]

    def handle_data(self, data):
        if self._active is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._active is None:
            return
        text = re.sub(r"\s+", " ", " ".join(self._buf)).strip()
        if text:
            if self._active == "title":
                self.title.append(text[:300])
            elif (
                self._active in ("h1", "h2", "h3")
                and text not in self.headings
            ):
                self.headings.append(text[:180])
            elif (
                self._active == "p"
                and len(text) > 35
                and text not in self.paragraphs
            ):
                self.paragraphs.append(text[:450])
        self._active = None
        self._buf = []


def apply_company_website_theme(user):
    """Apply company website theme to the app."""
    company = str((user or {}).get("company", "")).strip()
    if not company or (user or {}).get("role") == "master":
        return
    con = db()
    row = con.execute(
        "SELECT theme_primary, theme_accent, theme_background, theme_text "
        "FROM company_website_profile WHERE lower(company_name)=lower(?) ORDER BY id DESC LIMIT 1",
        (company,),
    ).fetchone()
    con.close()
    if not row:
        return
    p = row["theme_primary"] or "#4b82f5"
    a = row["theme_accent"] or "#62c8f5"
    b = row["theme_background"] or "#0b1020"
    st.markdown(
        f"""
    <style>
        :root {{--dacre-primary:{p};--dacre-primary2:{a};}}
        .stApp {{
            background: radial-gradient(circle at 85% 0%,{p}22,transparent 30%), linear-gradient(145deg,{b} 0%,#101729 55%,#0e1628 100%) !important;
        }}
        .dacre-user-hero, .di-quick-card, .di-metric, .dacre-card {{
            border-color: {p} !important;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )
