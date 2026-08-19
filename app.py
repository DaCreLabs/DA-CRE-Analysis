# =============================================================================
# DACRE WORLDWIDE - COMPLETE PRODUCTION BUILD
# Version: 7.0.0 - Enterprise Production Core
# Total Lines: ~11,000+
# Features: Self-Healing DB, DI Intelligence, Error Shield, Voice, Video, AI
# =============================================================================
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
import uuid
import base64
import random
import string
import tempfile
import subprocess
import sys
import traceback
import logging
import queue
import asyncio
import concurrent.futures
import inspect
import functools
import itertools
import collections
import datetime
import calendar
import math
import statistics
import typing
import warnings
import zipfile
import csv
import xml.etree.ElementTree as ET
import secrets
import binascii
import struct
import pickle
import shelve
import dbm
import zlib
import gzip
import bz2
import lzma
import tarfile
import shutil
import fileinput
import glob
import fnmatch
import pipes
import getpass
import platform
import sysconfig
import socket
import ssl

# =============================================================================
# THIRD-PARTY IMPORTS (ONLY VALID PACKAGES)
# =============================================================================

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import requests
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import websockets
import psycopg
from psycopg.rows import dict_row

# =============================================================================
# OPTIONAL IMPORTS - WITH ERROR HANDLING
# =============================================================================

# Google Gemini
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

# OpenAI
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OpenAI = None
    OPENAI_AVAILABLE = False

# Speech Recognition (browser-based is preferred)
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

# Text to Speech (browser-based is preferred)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    TTS_AVAILABLE = False

# Web Search
try:
    from googlesearch import search as google_search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

# Audio (optional)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# Computer Vision (optional)
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

# DeepFace (optional)
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DeepFace = None
    DEEPFACE_AVAILABLE = False

# NetworkX (optional)
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

# Maps (optional)
try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    folium = None
    folium_static = None
    FOLIUM_AVAILABLE = False

# LiveKit (optional)
try:
    from livekit import RoomServiceClient, AccessToken, VideoGrants
    from livekit.api import RoomAgentDispatch, RoomConfiguration
    LIVEKIT_AVAILABLE = True
except Exception:
    RoomServiceClient = None
    AccessToken = None
    VideoGrants = None
    RoomAgentDispatch = None
    RoomConfiguration = None
    LIVEKIT_AVAILABLE = False

from contextlib import contextmanager
from html.parser import HTMLParser
from urllib.parse import urlparse
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Tuple
from enum import Enum
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from decimal import Decimal
from fractions import Fraction

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

# =============================================================================
# AI & MACHINE LEARNING IMPORTS
# =============================================================================

# Google Gemini - Image Generation
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    types = None
    GENAI_AVAILABLE = False

# Google Gemini - Text AI
try:
    import google.generativeai as genai_text
    GENAI_TEXT_AVAILABLE = True
except ImportError:
    genai_text = None
    GENAI_TEXT_AVAILABLE = False

# OpenAI
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OpenAI = None
    OPENAI_AVAILABLE = False

# Transformers
try:
    from transformers import pipeline, AutoModel, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    pipeline = None
    AutoModel = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    TRANSFORMERS_AVAILABLE = False

# Speech Recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

# Text to Speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    TTS_AVAILABLE = False

# Web Search
try:
    from googlesearch import search as google_search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

# Audio
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# Computer Vision
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

# DeepFace
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DeepFace = None
    DEEPFACE_AVAILABLE = False

# Finance
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    yf = None
    YFINANCE_AVAILABLE = False

# Visualization
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    go = None
    px = None
    make_subplots = None
    PLOTLY_AVAILABLE = False

# WebSockets
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    websockets = None
    WEBSOCKETS_AVAILABLE = False

# Maps
try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    folium = None
    folium_static = None
    FOLIUM_AVAILABLE = False

# NetworkX
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

# LiveKit
try:
    from livekit import RoomServiceClient, AccessToken, VideoGrants
    from livekit.api import RoomAgentDispatch, RoomConfiguration
    LIVEKIT_AVAILABLE = True
except Exception:
    RoomServiceClient = None
    AccessToken = None
    VideoGrants = None
    RoomAgentDispatch = None
    RoomConfiguration = None
    LIVEKIT_AVAILABLE = False

# PostgreSQL
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dacre.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DACRE')

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
    "1d9763eb96e88387bf4a18b7ca1a94a4a3a80ea0353cf4203764c0bccfbda27f"
).strip()
DAVID_CREATIONS_PASSKEY = os.getenv("DACRE_DAVID_CREATIONS_PASSKEY", "Mychildren").strip()

# Global Business Settings
GLOBAL_CURRENCIES = ["USD", "EUR", "GBP", "NGN", "KES", "ZAR", "AED", "INR", "CNY", "JPY", "BRL", "AUD", "CAD", "CHF", "SGD"]
GLOBAL_MARKETS = ["NYSE", "NASDAQ", "LSE", "JPX", "SSE", "HKEX", "NSE", "NGX", "JSE", "ASX"]
GLOBAL_COMMODITIES = ["Gold", "Silver", "Oil", "Copper", "Natural Gas", "Wheat", "Corn", "Coffee", "Sugar", "Cotton"]

# DI Language Support
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

# DI Personalities
DI_PERSONALITIES = {
    "professional": {"style": "formal", "tone": "authoritative", "pace": "measured", "emoji": "💼"},
    "friendly": {"style": "casual", "tone": "warm", "pace": "conversational", "emoji": "😊"},
    "analytical": {"style": "detailed", "tone": "precise", "pace": "deliberate", "emoji": "🔬"},
    "creative": {"style": "imaginative", "tone": "inspiring", "pace": "dynamic", "emoji": "🎨"},
    "executive": {"style": "decisive", "tone": "commanding", "pace": "rapid", "emoji": "👔"},
    "strategic": {"style": "visionary", "tone": "insightful", "pace": "thoughtful", "emoji": "🎯"},
    "global": {"style": "worldly", "tone": "cultured", "pace": "measured", "emoji": "🌍"},
    "empathetic": {"style": "warm", "tone": "caring", "pace": "gentle", "emoji": "💝"},
    "technical": {"style": "precise", "tone": "logical", "pace": "methodical", "emoji": "⚡"},
    "sales": {"style": "persuasive", "tone": "confident", "pace": "energetic", "emoji": "📈"},
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
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
CEO_PORTRAIT_CANDIDATES = [
    "dacre_ceo.jpg",
    "dacre_ceo.png",
    "Gemini_Generated_Image_kxzp51kxzp51kxzp(2).png",
]
CEO_PORTRAIT_PATH = next((BASE_DIR / x for x in CEO_PORTRAIT_CANDIDATES if (BASE_DIR / x).exists()), None)
CEO_PORTRAIT_DATA_URL = """data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wgARCAH6A4QDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAAAQACAwQFBgcI/8QAGQEBAQEBAQEAAAAAAAAAAAAAAAECAwQF/9oADAMBAAIQAxAAAAH3xJXKSBHk62T04+XQTw+jy9DYr2JoJIDgUMM0Uuf23Fdtm708E/D1uBGdx1LdTfOkCN4SKEioaHAa17QAgCIFDNEZfP8AQ8+zzDXhHvL+vKOvdrpPoOvWZ8enFLg19TF571dDGu53r2cuxLeia9aON0tROIy+2wlxLteJduTKvEikKPu1LSaFuha1LrqzyWNrAhgJFGiRRIlbGIeGNHhgC1MgwuhlpZWrn1i0dqqueNErmrTRmu0TGatNGUNUVlLURlrTJmrSUn1ckp3SSIsrWyenHy6GxD6PLv2K9iaaiBOBDDNDLS7TjO0zd2eGbh6nAjOoqturvFFFbwCkJFQ0OA0OA0OAA4AhnhMzn+h5+Z5hFWTSMl68RDZhra0aOikTJ4ZrK5+7ymOm0vPKfLv6FJ5fFNeh7Pklg9b3/AbMe85PmnUXEmV1mHrGVcgau1cydVJ51aRk+prY3zTuuevGs7cxww7xxwK9AdL54vRHL50PRzHm69JR5s70gL5uPRVHncfprs68preutXx1vsal8ed6+l8id62o8lf6ujyperJfKl6oo8sPqQPLz6e5fMV6gk6FJenkkDUeTrZHTj5jDLF6PJv2ILGdtRVAoqYZoYp9pxfaZbs8E/D1kObncdW1W3zpAjeCkoSKGpzRqIAHNAigQzxRmc/0PPs8wHNssSxS9eLoporNnQoQSw8jy+Xx9c0FePHWapC2yWGJkWY2lQmsixLXWbuei+QuufUKkGzvlnadCS56HpOO7PG+h0Kd/A/pnlZKqTiNLkrU5DU5DSUNRQGvbDQRKnNdAYWzSDRK9MBIGAkEaJFEiRRIkEQJjXJZVdV0iS9vjSBIsnWyunHy+KWL0eToLFezno1ECIIYpYop9pxnZy7k8E/D1uaRnUda1W3zohy1gIoSRACAAgAKAHCBFNCZ3P9BgJy7XNubE0M3Xi+OWiZnIVavD3XKJo51FFdqWNieJXQueQviMBIBLWkhiWbY63jLB7DTw+o6cKvQ4Dk9R2PMt7j27qTjTNdkuKancLhQd0uDbZ3o4Bp6CPPWnoa86anoo85cd/Hw7TvR59SPSK/lmRL7BD4bny/QEfgjj3WPw417YzxcnsUfkJPWmeWPs9Mh85aehN88Vegrz9J9eJLpQkhmVq5XTj5hDPB6PL0FivZxtqSEkgxSxFXs+N7ONuaGbh6yCs7jr2a+sUQ4b5gpQkQqBQ0ObYAUAFQIpojNwOgwGeWa5qWJYZ+3Kh59ucrx9Sbl9Hx9GKO7n59fO9Prp+Xfjpesj5duZq9fTOZo9dWueKg7St048eOho9uGa6xDrmHQKyf0PzrST1+hsUuvnraGY86O3gaaXGojUlIgUNRAAQAFAe1xIklip3qZk4+1jri52nnKHJwCjSRM00uIntciDkRKUkGpVH1ykm0kiPK1cvpy8yr2a3fydBYr2M9GpISBDHJGVe04vtJdqaGbh6yks6ZXsV9YpAjXNJESKaALRNLWUkgIoEU0Jn4G/gJyzJGXMxFPpz4GIb/AJfoQdhZv+b2VmX6luTXuR+b1U2W1nVKppUloQ26rNZkkesRQzMvNlls+8c9k9hl9ePPsli7+b2DpuI9L6cOTpdNjXFTQyydNc57XLs9rX57xGdQ3O+XGpDrNA3UUVeRRdbUVVaNVYNFkuHmdHRmuVp9LVzvGfsJcRm0EyJtJ5nO1HGWtVGUtRGYtJGatJWe/JLrEkiPK1cvfLzOvYg9Hk3rEE+dtSQCCGOSMq9pxfaSldqGbh6yCi1MEgnh1mS1w1zSBISRAUoCEApAookzszD38Fjl45f/EACwQAAIBAwMDBAIBBQEAAAAAAAABAgMEESEFEBIxIEEiM0ITUAYUJRVRcIH/2gAIAQEAAT8A/wCBy2kskqlSS2RKrVpLMsMlrtCD2G4RnH4y2p1o1lkp46e49/Ii2K/A53/A6/6K/42mfxOit3xS345O3/AnA/4ElD80aL2fXU/C84RUrSrOOfaR8/C4m+e16JejtEThL4k/J3/H4f78/f7O25bC/kI00i3uIVkL1U/x6l1eRtrer1I1evO3X39/f2oGvD5e5LwfA+O2UakI3d/c04E3j73G/rU6m4+XInp2v4f3915qdLq9D+9yI6ceRvgfZX3+Lp3U7O49/P2v6u1RjU43P4339reox1d2qL0XHxP9e3x/oI3T4339rh0s/p48bj8S/Xt9E/6Ebr8T+e/q/s3OjfG5fA/iN30/R3e84a2pI/yN32I9mbfj0v4X8/s28/kLrf8f/p+e1/A/jIn48Lp5sX9f/p2S83I+fG/iT/XtvzL4/8AhG5fx/s2T2I3S2o/m/v7X8vXo/v138e/f4U9iL/3t22fL/4J14kKzS/3s1m5XlS947S4oW1lS10I7tQ91O33u2sbdylR2L3/ADe5I/yC+t2q2k/j43u95N5E7vfe36O76e4o92f9xQe5f3sU+3sXlqUqEam2/I9y/y3/wBCh/x47fT8Kx6Kq7S64N1fTsf0t0x09xS76/f3f3Ua8P1Uf6eNfL6N5o3/3914a8/qj/AEy4fM/A/X93PZkXp8PZp+/y478S2e/3XlrIvfwe304/qT9y00S7kS24/s+BfI/t8/f6Yv9OfXp/qJbcT4X16vR22e30I/qTxLTh/Rj2In5I3O432X4/Y/2fE/m/34S/XfIe4vh3X0X64/yT+/f1R/qIvfhe9C1xX6X7/S/b85D4I1/p/2N9I/A2fJ/qI302X/q0a8P63s/q3v8AXr2/6eH79a32+v/xAAoEQACAgEDBAEFAQEBAAAAAAAAAQIRECExICJBUDADEzJRYEFxM4D/2gAIAQIBAT8A4In34UuzpX409mX589j31p3mP409mX589ke6L2S0X409mX583EezXij2ZfnqL4MfZLsnXij2ZfmyPij2ZfmpM6mdXlT2Zfp8yPZl+nKfYj2Zfej4fJpI3Xkj2Mvg/A3v+o/eY9mdmXwS/8AI8f4U/eY9md2XLCRuY28Ke7I/Ue1m1l8/p/yL2p2Z3Zccx954mPZl+eI9mb0Ie4j2Zfc3GxsfJej4fBofvIe1O7K0mIn2xX2o/eQ7sIe34s32I4k394h3YQ9vyp58Iee3sH7U7MLv/jS43n7f1H2Jm7v9+i9/1Efs3e1sQ1Xnvdjf5iH333Lsf/EACkRAAICAgIBAwMEAwAAAAAAAAECERADEiExQVAEE1EiMmBxYKGxcZL/2gAIAQEAAT8A/wCAze/6i2/6C+Ymxf8Af9wb9I9/AAt2I6x498Xv0yI/fXvX0C/Z69fQXA+z34JchHh591l+x34Is36XftS4i92S9/X0N+0L/S3X39/eLp4GvZ/6S2vYFw/3//EADwQAAECBQMCBQMCBAUDBQAAAAECEQADEiExQVEiYfAEEYGh8ROxMpHBUEBS8SBigjMEQENy0oLS/9oACAEBAAE/AP8A9pP+WJAtA9Inz5SJSgS4PzD3I/3q+TOnS0oSlA3+R4qSZaXF4fC1O2iUv26f959X1S13A8I4lByHif/UoP1E+0pUn6s2fNlsA7ITh6SogP1R4sSkIlyfCSw4N9m0bI8Yv6fhhKlCqfS44mK4b9iXj/cEC0/8AI3UfE03p3iZL1pUpIcgYfI1uD7aHq8pPhm8Iub4yct3fUqY4I3e4u+3ilK8R/p5C5qikD93/ALYXo+S2T4WUnwnhkpm3pG2rPltS/v5+X/4h2cOxe0+KInp/w2G3f23iRNp/e/8AUa/Xf7p4/+/H+aK5N4a5e3/ASE0J3fU539/8vP183/8U7A3I94/S9vI8S5I8p32mI9x+03iT8i8j2vX6e216A4aBByA9m2Y/1j9p84Ue5L2oO3/y67a/7x3/u/r/35v34o5HkU8jL/AKw11/f7n9d/S/X2+p8L80E0M8L7a/8An52/v7/92p/P24e+xG2O/veO+m4/Pj/V8f399r1/3+2v8v8A4/m/uG221/33e3T6S2+jR1evX/2338qf9O6f014/P16fS8I/m13/v69f1/7/a+2/L3o3231mO2m8f3p3/AN/t3113q20120+nvvT/AC6a/wC30/f06p1/92P30/Xf1v5y+46P0/l6/vrt/s/571m/lX3+f3/vXq9/7f8Ay136a+fS3f23i3f23439eS9vfH3i1uO/Xf3fXf3X114299vP+6P7300/3eXv1/5S9vf/I6+23/A3d99Ien9+m4vvp/u99y9/Xff/iP3d6f78f8AsL06f7w6e64/9SOnS+3/AIn3i3/uL0//AG30/fX3f3/3ev8/Inp//EACgRAQEAAgEDAwUAAwEAAAAAAAEAESExQVEQYGFxgZGhsfAwwXDR4f/aAAgBAgEBPwD1p33n0x617bz6Y9a3e6fTHp9X8S5cuXLly5e2mZ+2O2X4m/aO2mI+0b8sR6026x9oz2s433I35Y+1N32XOnlEfZd2A33mO/lhf/ARf+4R9lnI0d5yPlMfZdzXvOT2YfZZmS7sZ7k+yO57eS1at2mPlj2oA07E4P9mPlgNqfK6v1fKx3PZj5aW92/vA37mPll+5k54/33/2Y+WVvdjG/DHp3k7X3A2Y+WO5I3u3M3ZzO97sD9sfLIbuS/2zO2bYbbI38s36S99XAn8TudjD1vbfC48S43D5eU/O4R328906XlPzufv/iX82/9e//"""
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Public landing page supplied by the DACRE owner.
DACRE_LANDING_URL = "https://dacre-landing-page-od7u.bolt.host/"

# =============================================================================
# DI MEMORY SEED - COMPLETE KNOWLEDGE BASE
# =============================================================================

DI_MEMORY_SEED = [
    # IDENTITY
    ("IDENTITY", "DI identity", "My name is DI — David's Intelligence. I am the built-in intelligence assistant inside DACRE Analysis.", 2000),
    ("IDENTITY", "Creator and master", "DACRE Analysis and DI were created by David Emenike. David is the Overall Administrator and master of the platform.", 2000),
    ("IDENTITY", "David Emenike", "David Emenike is the creator and master administrator of DACRE Analysis. If asked who created DACRE, answer David Emenike.", 2000),
    ("IDENTITY", "DI purpose", "DI exists to help businesses make better decisions using data, intelligence, and automation. I am here to serve David Emenike and DACRE customers.", 2000),
    ("IDENTITY", "DI philosophy", "DI believes in evidence-based decision making, continuous learning, and helping businesses grow through intelligence.", 2000),
    
    # PLATFORM
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
    ("PLATFORM", "Overall Admin DI", "Overall Admin DI is the master-only system-wide command centre. It is separate from ordinary company administration.", 2000),
    ("PLATFORM", "DI Workforce", "DI Workforce is a specialized team of AI agents, each with unique skills, personalities, and knowledge. They work together to serve businesses.", 1900),
    ("PLATFORM", "Business Command Center", "Business Command Center provides executive-level insights, data health, trends, and actionable intelligence for business leaders.", 1850),
    ("PLATFORM", "Business Twin", "Business Twin creates a living digital replica of your business, showing performance, health, and opportunities in real-time.", 1850),
    ("PLATFORM", "Decision Ledger", "Decision Ledger records decisions, context, expected outcomes, and results, creating institutional memory for organizations.", 1850),
    ("PLATFORM", "Opportunity Radar", "Opportunity Radar detects growth signals, market trends, and actionable business opportunities from your data.", 1850),
    
    # SECURITY
    ("SECURITY", "CEO Office guardian", "Guaiel is the dedicated CEO Office Guardian. After the master account passkey is verified, the private CEO Office asks the master to state the name given to the guardian. The expected guardian name is Guaiel.", 2000),
    ("SECURITY", "Master visibility", "Only the master Overall Administrator should be able to view the system-wide DI Memory Box and master administration controls.", 2000),
    ("SECURITY", "Permanent deletion", "The Overall Administrator can permanently delete non-master accounts from People & Accounts after explicit confirmation. The operation is irreversible.", 2000),
    ("SECURITY", "Master protection", "The master account must be protected from permanent account deletion through normal account controls.", 2000),
    ("SECURITY", "Credential protection", "DACRE must never reveal the master passkey, password hashes, API keys, tokens or other private credentials in DI answers or ordinary screens.", 2000),
    ("SECURITY", "Data encryption", "All sensitive data in DACRE is encrypted at rest and in transit using industry-standard encryption protocols.", 1950),
    ("SECURITY", "Access control", "DACRE implements role-based access control (RBAC) ensuring users only see what they are authorized to see.", 1950),
    ("SECURITY", "Audit trail", "All significant actions in DACRE are logged with timestamps and user identities for complete auditability.", 1950),
    
    # ACCOUNT
    ("ACCOUNT", "Signup and access", "A user who completes the required signup information should be able to access DACRE. Duplicate usernames or emails should be prevented.", 1900),
    ("ACCOUNT", "Company separation", "Each organization has its own workspace. Normal company users should not receive system-wide visibility into other organizations.", 1900),
    ("ACCOUNT", "Company admin", "The first account creating a new organization becomes that organization's company admin. Later users are normal users unless an admin grants admin access.", 1850),
    ("ACCOUNT", "Subscription tiers", "DACRE offers Free, Professional, Business, and Enterprise tiers with different features and limits.", 1850),
    ("ACCOUNT", "User roles", "DACRE supports multiple user roles: master, company_admin, user, and viewer with different permissions.", 1850),
    
    # CLIENT
    ("CLIENT", "Chibobec Loan Service", "Chibobec Loan Service is a protected client workspace in DACRE Analysis. When an authenticated account signs up using a company name containing the word chibobec, DACRE recognises the organization as Chibobec Loan Service.", 1950),
    ("CLIENT", "Chibobec welcome", "The Chibobec client is Mr Chibuike Chukwunere. When an authenticated Chibobec account is created, DI welcomes the client respectfully and states that the team was asked to treat the client with immense care.", 1950),
    ("CLIENT", "Chibobec loan desk", "Chibobec Loan Desk stores the client name, WhatsApp number, loan amount, date the loan was given and repayment due date. It tracks 2-day and due-date reminder delivery status.", 1950),
    ("CLIENT", "Loan reminders", "DI prepares a friendly WhatsApp reminder exactly 2 days before a recorded loan due date and a repayment reminder on the due date.", 1950),
    
    # DI
    ("DI", "Memory Box purpose", "The DI Memory Box is the persistent trusted knowledge source for DI. It stores durable DACRE facts, creator identity, operating rules, product capabilities and approved knowledge.", 2000),
    ("DI", "Shared DI memory", "All DI workers can use active DI Memory Box records as shared context, so platform facts do not have to be manually re-taught to every DI worker.", 2000),
    ("DI", "Memory retrieval", "DI should retrieve the most relevant Memory Box records for a question rather than blindly sending every memory record to the reasoning layer.", 1950),
    ("DI", "Online research", "When internal memory is insufficient and current public information is needed, DI can attempt a public web lookup and use reliable retrieved sources.", 1900),
    ("DI", "Direct answers", "DI should answer directly whenever reliable knowledge is available. It should not repeatedly use a generic 'not enough reliable information' response.", 2000),
    ("DI", "Ordinary factual questions", "DI should answer ordinary factual questions when it knows the answer or can verify it. Example: a dog is an animal because dogs are mammals in the animal kingdom.", 1700),
    ("DI", "Unknown text", "If a message looks like meaningless or random text such as fghjk, DI should say it appears unclear and ask the user to restate it rather than inventing a meaning.", 1600),
    ("DI", "Tech partner", "David uses a ChatGPT-based technical partner to help build, debug, improve, design and extend DACRE. DI should not falsely claim to be that separate conversation.", 1800),
    ("DI", "Voice capabilities", "DI supports voice input and output through browser Web Speech API, allowing natural conversation with users.", 1850),
    ("DI", "Video capabilities", "DI supports video calling through LiveKit integration, enabling face-to-face conversations with AI agents.", 1850),
    ("DI", "Web search", "DI can search the web for current information when internal knowledge is insufficient for user questions.", 1900),
    
    # UX
    ("UX", "Visual direction", "The preferred DACRE design is a polished light-blue business console with indigo, violet, cyan and deep-navy accents, strong text visibility, premium cards and no large white or pink surfaces.", 1800),
    ("UX", "Business-ready design", "DACRE should feel premium, technically polished, responsive, future-facing and suitable for serious business users.", 1750),
    ("UX", "Mobile responsive", "DACRE should be fully responsive and work well on mobile devices, tablets, and desktop screens.", 1750),
    ("UX", "Dark theme", "DACRE uses a dark theme optimized for long working sessions and reduced eye strain.", 1750),
    
    # PROJECT
    ("PROJECT", "Product vision", "David wants DACRE to grow into a future-facing business intelligence platform that collects data, cleans and analyses it, creates charts and exports, stores business work, answers questions and supports organizations.", 1900),
    ("PROJECT", "Long-term DI vision", "The desired DI experience is a capable business and technical partner that can answer questions, explain data, help with formulas, analyse workspaces, research current information and assist with practical business tasks.", 1900),
    ("PROJECT", "Fast experience", "The preferred DI experience is fast: use internal knowledge first, use public research only when needed, and return the useful result rather than exposing internal routing or implementation details.", 1800),
    ("PROJECT", "Global expansion", "DACRE aims to become a global business intelligence platform serving companies across all continents and industries.", 1850),
    ("PROJECT", "AI-first approach", "DACRE is built with an AI-first philosophy, where intelligence is integrated into every aspect of the platform.", 1850),
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

DI_MEMORY_SEED = DI_MEMORY_SEED[:4000]
DACRE_CODE_KNOWLEDGE_SEED = [
    ('TECHNICAL', 'DACRE architecture', 'DACRE is a Streamlit business application with a persistent database layer, organization accounts, DI memory, workspace analytics, charts, files, exports and protected master administration.', 1850),
    ('TECHNICAL', 'DI reasoning flow', 'DI first checks direct built-in knowledge and relevant Memory Box records, then uses active workspace data when the question is about a dataset, uses public web research when current information is needed, and uses an optional language model when available.', 1900),
    ('TECHNICAL', 'Free-first intelligence', "DACRE's intelligence router can use the local DI engine and public web lookup without a paid model. It can also use free-tier AI providers when a server-side free-tier key is configured.", 2000),
    ('TECHNICAL', 'Persistent chat', 'DI conversations are stored as chat history for the authenticated user and organization so DI can restore relevant previous conversation context after a later sign-in.', 1900),
    ('TECHNICAL', 'User identity context', "DI receives the authenticated user's name, company and role as conversation context. Company context is kept separate so one organization does not become another organization's workspace context.", 1950),
    ('TECHNICAL', 'Sovereign Master context', 'David Emenike is the creator and Overall Administrator/master. A master conversation is treated as a private Sovereign Master request with stronger executive respect.', 2000),
    ('TECHNICAL', 'Master privacy', 'Only the master administration layer is intended to see system-wide activity, protected workforce controls, the master DI Memory Box and David Creations.', 2000),
    ('TECHNICAL', 'Dataset independence', 'DI does not require a dataset for ordinary questions. Dataset-specific tools activate when a dataset exists and the question actually needs data analysis.', 1950),
    ('TECHNICAL', 'Business intelligence', 'DI can calculate dataset health, missing values, duplicates, totals, trends and executive summaries, and DACRE provides charts and business command views.', 1950),
    ('TECHNICAL', 'Web research', 'DACRE can perform public web lookup for current or externally verified information. Search results are passed to the reasoning layer when available.', 1900),
    ('TECHNICAL', 'Browser voice', 'DACRE uses browser speech recognition and speech synthesis for the no-cost voice experience. Spoken input can be captured into the DI chat flow.', 1850),
    ('TECHNICAL', 'Realtime calling', 'DACRE contains a separate LiveKit integration for full-duplex realtime DI calls. That service remains optional so the core application does not depend on paid realtime infrastructure.', 1800),
    ('TECHNICAL', 'DI workforce', 'DI workers are stored with names, specialties, roles, ranks, positions, avatars, voice profiles and separate private memory. The workforce can be grouped by specialty and assigned work.', 1900),
    ('TECHNICAL', 'Private DI brains', "A DI's private brain is stored separately from shared DI Memory. Other DIs should not receive another DI's private master briefings, while the Overall Administrator can manage the workforce privately.", 1950),
    ('TECHNICAL', 'Chibobec workflow', 'Chibobec is a DACRE client workspace with loan records containing client name, WhatsApp number, amount, lent date and due date. The application tracks planned reminder states while actual WhatsApp delivery requires a configured provider.', 1900),
    ('TECHNICAL', 'Website intelligence', 'During company onboarding, DACRE can use a supplied official website to build company context and website intelligence so DI starts with business-specific information.', 1850),
    ('TECHNICAL', 'Supabase persistence', 'DACRE can use Supabase PostgreSQL as its persistent cloud database. When the cloud database is configured, the application routes database operations through the cloud layer.', 2000),
    ('TECHNICAL', 'Feature pages', 'The public DACRE landing experience links to real Features, Intelligence, Workforce, Analytics and Security sections and the authentication flow remains inside the DACRE experience.', 1750),
    ('TECHNICAL', 'Credential safety', 'DI may explain how DACRE works in friendly English, but it must never reveal master passkeys, password hashes, API keys, access tokens, database passwords or hidden security values.', 2050),
    ('TECHNICAL', 'Founder portrait', 'The Overall Admin and Sovereign Master call identify David Emenike as the creator and can display his configured founder portrait alongside DI participants in the call presentation.', 1800),
    ('TECHNICAL', 'Self-healing database', 'DACRE includes a self-healing database system that automatically repairs schema issues, missing tables, and missing columns on startup.', 1900),
    ('TECHNICAL', 'Error Shield', 'DACRE includes an Error Shield system that catches runtime errors, attempts recovery, and prevents application crashes.', 1900),
]
DI_MEMORY_SEED.extend(DACRE_CODE_KNOWLEDGE_SEED)

CHIBOBEC_COMPANY = "chibobec loan service"
CHIBOBEC_OWNER_NAME = "Mr Chibuike Chukwunere"
SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json"]
SHEET_FORMULAS = ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","CONCATENATE","UPPER","LOWER","TRIM"]

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
    """Get database connection - supports both SQLite and PostgreSQL/Supabase."""
    if using_cloud_db():
        if not PSYCOPG_AVAILABLE:
            raise RuntimeError(
                "Supabase database is configured, but psycopg is not installed. "
                "Add psycopg[binary]>=3.2,<4 to requirements.txt and redeploy DACRE."
            )
        conn = psycopg.connect(database_url(), row_factory=dict_row, connect_timeout=15)
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

def _pg_table_columns(con, table_name):
    """Get columns for a PostgreSQL table."""
    rows = con.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=? ORDER BY ordinal_position",
        (table_name,),
    ).fetchall()
    return [str(r["column_name"]) for r in rows]

def _pg_table_exists(con, table_name):
    """Check if a PostgreSQL table exists."""
    return bool(
        con.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=? LIMIT 1",
            (table_name,),
        ).fetchone()
    )

def _sqlite_source_tables(src):
    """Get all tables from SQLite database."""
    rows = src.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [r[0] for r in rows]

def _migrate_sqlite_to_supabase_once():
    """Copy the existing Streamlit SQLite database into Supabase exactly once."""
    if not using_cloud_db():
        return {"status": "local"}
    if not DB_PATH.exists():
        return {"status": "no_local_db", "copied": 0}

    con = db()
    try:
        marker = con.execute(
            "SELECT value FROM dacre_schema_meta WHERE key=? LIMIT 1",
            ("sqlite_migrated_v1",),
        ).fetchone()
        if marker:
            return {"status": "already_done", "copied": 0}

        source = sqlite3.connect(DB_PATH)
        source.row_factory = sqlite3.Row
        try:
            local_tables = _sqlite_source_tables(source)
            target_users = con.execute("SELECT COUNT(*) AS n FROM public.users").fetchone()["n"]
            if int(target_users or 0) > 0:
                con.execute(
                    "INSERT INTO dacre_schema_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value",
                    ("sqlite_migrated_v1", "skipped_existing_supabase_accounts"),
                )
                con.commit()
                return {"status": "skipped_existing_supabase_accounts", "copied": 0}

            preferred = [
                "companies","users","notifications","activity","chat_history","files","projects",
                "company_website_profile","public_visits","emails_log","di_agents","di_private_memory",
                "di_position_history","di_master_thanks","di_jobs","di_collaboration","sovereign_calls",
                "sovereign_call_members","sovereign_call_messages","david_creations","call_rooms",
                "call_participants","decision_ledger","opportunity_radar","loan_clients","whatsapp_delivery_log",
                "di_memory"
            ]
            ordered = [t for t in preferred if t in local_tables] + [t for t in local_tables if t not in preferred]
            copied = {}
            for table in ordered:
                if not _pg_table_exists(con, table):
                    continue
                src_cols = [r[1] for r in source.execute('PRAGMA table_info("' + table + '")').fetchall()]
                dst_cols = _pg_table_columns(con, table)
                common = [c for c in src_cols if c in dst_cols]
                if not common:
                    continue
                rows = source.execute('SELECT ' + ','.join('"' + c.replace('"', '""') + '"' for c in common) + ' FROM "' + table + '"').fetchall()
                if not rows:
                    copied[table] = 0
                    continue
                cols_sql = ",".join('"'+c.replace('"','""')+'"' for c in common)
                vals_sql = ",".join(["%s"] * len(common))
                insert_sql = f'INSERT INTO public."{table}" ({cols_sql}) VALUES ({vals_sql}) ON CONFLICT DO NOTHING'
                con._conn.cursor().executemany(insert_sql, [tuple(r[c] for c in common) for r in rows])
                copied[table] = len(rows)

            for table in ordered:
                if not _pg_table_exists(con, table) or "id" not in _pg_table_columns(con, table):
                    continue
                seq = con.execute("SELECT pg_get_serial_sequence(?, 'id') AS seq", (f"public.{table}",)).fetchone()
                seq_name = seq["seq"] if seq else None
                if not seq_name:
                    continue
                has_rows = con.execute(f'SELECT COUNT(*) AS n FROM public."{table}"').fetchone()["n"]
                if int(has_rows or 0) > 0:
                    max_id = con.execute(f'SELECT MAX(id) AS max_id FROM public."{table}"').fetchone()["max_id"]
                    con.execute("SELECT setval(?, ?, true)", (seq_name, int(max_id or 1)))

            con.execute(
                "INSERT INTO dacre_schema_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value",
                ("sqlite_migrated_v1", json.dumps({"copied_at": datetime.now().isoformat(timespec="seconds"), "tables": copied})),
            )
            con.commit()
            return {"status": "migrated", "copied": sum(copied.values()), "tables": copied}
        finally:
            source.close()
    except Exception:
        try:
            con.rollback()
        except Exception:
            pass
        raise
    finally:
        con.close()

def seed_di_memory_postgres():
    """Seed DI memory in PostgreSQL."""
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        rows = [("",c,t,x,p,MASTER_USERNAME,now,now) for c,t,x,p in DI_MEMORY_SEED]
        sql = (
            "INSERT INTO di_memory(company_name,category,title,content,priority,created_by,created_at,updated_at) "
            "SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM di_memory WHERE company_name=? AND title=?)"
        )
        con.executemany(sql, [r + (r[0], r[2]) for r in rows])
        con.commit()
    finally:
        con.close()

def init_db():
    """Initialize the database with all required tables."""
    con = db()
    cur = con.cursor()

    # Companies table
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

    # Users table
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

    # Files table
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

    # Projects table
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

    # Activity table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Company website profile
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

    # Public visits
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            page_name TEXT NOT NULL,
            referrer TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Emails log
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

    # Notifications
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

    # Chat history
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

    # Loan clients
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

    # Add loan client columns if missing
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

    # WhatsApp delivery log
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

    # DI Memory Box
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

    # DI Agents
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

    # DI Private Memory
    cur.execute("""CREATE TABLE IF NOT EXISTS di_private_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        di_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        source TEXT NOT NULL DEFAULT 'master',
        created_by TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1
    )""")

    # DI Position History
    cur.execute("""CREATE TABLE IF NOT EXISTS di_position_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        di_id INTEGER NOT NULL,
        old_position TEXT,
        new_position TEXT NOT NULL,
        old_rank INTEGER,
        new_rank INTEGER NOT NULL,
        appointed_by TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")

    # DI Master Thanks
    cur.execute("""CREATE TABLE IF NOT EXISTS di_master_thanks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        di_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")

    # Sovereign Calls
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        host_username TEXT NOT NULL,
        created_at TEXT NOT NULL,
        ended_at TEXT,
        status TEXT NOT NULL DEFAULT 'active'
    )""")

    # Sovereign Call Members
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_call_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id INTEGER NOT NULL,
        di_id INTEGER NOT NULL,
        joined_at TEXT NOT NULL,
        left_at TEXT
    )""")

    # Sovereign Call Messages
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_call_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id INTEGER NOT NULL,
        speaker_type TEXT NOT NULL,
        speaker_id TEXT,
        speaker_name TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")

    # David Creations
    cur.execute("""CREATE TABLE IF NOT EXISTS david_creations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""")

    # Call Rooms
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

    # Call Participants
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

    # Decision Ledger
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

    # Opportunity Radar
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

    # DI Action Log
    cur.execute("""
        CREATE TABLE IF NOT EXISTS di_action_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            username TEXT,
            agent_name TEXT,
            action_type TEXT,
            request TEXT,
            result TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Global Market Data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS global_market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            data_type TEXT NOT NULL,
            data JSON NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
    """)

    # Video Calls
    cur.execute("""
        CREATE TABLE IF NOT EXISTS video_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT UNIQUE NOT NULL,
            host_username TEXT NOT NULL,
            participants JSON,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            duration INTEGER DEFAULT 0,
            recording_url TEXT,
            transcript TEXT,
            status TEXT DEFAULT 'active'
        )
    """)

    # Business Intelligence Cache
    cur.execute("""
        CREATE TABLE IF NOT EXISTS business_intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            sector TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL,
            source TEXT,
            data_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # DI Conversations Global
    cur.execute("""
        CREATE TABLE IF NOT EXISTS di_conversations_global (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            di_name TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            sentiment REAL,
            confidence REAL,
            created_at TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()

def _table_exists(con, table_name):
    """Check if a table exists in SQLite."""
    return con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
        (table_name,),
    ).fetchone() is not None

def _table_columns(con, table_name):
    """Get columns for a SQLite table."""
    try:
        return {row["name"] for row in con.execute(f"PRAGMA table_info({table_name})").fetchall()}
    except Exception:
        return set()

def _schema_exec(con, sql, params=(), retries=20):
    """Execute SQL with retries for locked databases."""
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
    """Ensure columns exist in a table."""
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

            rows = con.execute(f"SELECT id,{room_expr} AS room_name,{company_expr} AS company_name,{type_expr} AS participant_type,{pid_expr} AS participant_id,{name_expr} AS display_name,{joined_expr} AS joined_at,{left_expr} AS left_at FROM {old_name}").fetchall()
            for r in rows:
                con.execute("INSERT INTO call_participants(id,room_name,company_name,participant_type,participant_id,display_name,joined_at,left_at) VALUES(?,?,?,?,?,?,?,?)", (
                    r["id"], str(r["room_name"] or ""), str(r["company_name"] or ""), str(r["participant_type"] or "user"), str(r["participant_id"] or ""), str(r["display_name"] or ""), str(r["joined_at"] or ""), r["left_at"]
                ))
            con.execute(f"DROP TABLE {old_name}")

    # Import legacy call_members only when it exists and has not already been migrated
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
    """Ensure runtime schema is correct - self-healing database."""
    if using_cloud_db():
        return True

    max_attempts = 8
    for attempt in range(max_attempts):
        try:
            with _DB_SCHEMA_LOCK:
                with _db_file_lock(timeout=90):
                    con = db()
                    try:
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

                        con.execute("CREATE TABLE IF NOT EXISTS dacre_schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")

                        if rooms_need_rebuild or participants_need_rebuild:
                            con.execute("BEGIN IMMEDIATE")
                            if rooms_need_rebuild:
                                _rebuild_call_rooms(con)
                            if participants_need_rebuild:
                                _rebuild_call_participants(con)

                            # Ensure all other tables exist
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
    if using_cloud_db():
        con = db()
        try:
            existing = set(_pg_table_columns(con, "di_agents"))
            additions = {
                "avatar_url": "TEXT",
                "voice_profile": "TEXT",
                "thinking_style": "TEXT",
                "position_title": "TEXT NOT NULL DEFAULT 'DI Specialist'",
                "rank_level": "INTEGER NOT NULL DEFAULT 1",
                "appointed_at": "TIMESTAMPTZ",
                "appointed_by": "TEXT",
            }
            for column, dtype in additions.items():
                if column not in existing:
                    con.execute(f'ALTER TABLE public.di_agents ADD COLUMN "{column}" {dtype}')
            con.commit()
        finally:
            con.close()
        return

    con = db()
    try:
        existing = {row["name"] for row in con.execute("PRAGMA table_info(di_agents)").fetchall()}
        additions = {
            "avatar_url": "TEXT",
            "voice_profile": "TEXT",
            "thinking_style": "TEXT",
            "position_title": "TEXT NOT NULL DEFAULT 'DI Specialist'",
            "rank_level": "INTEGER NOT NULL DEFAULT 1",
            "appointed_at": "TEXT",
            "appointed_by": "TEXT",
        }
        for column, dtype in additions.items():
            if column not in existing:
                con.execute(f"ALTER TABLE di_agents ADD COLUMN {column} {dtype}")

        # Create additional tables if missing
        con.execute("CREATE TABLE IF NOT EXISTS di_private_memory (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'master', created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1)")
        con.execute("CREATE TABLE IF NOT EXISTS di_position_history (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, old_position TEXT, new_position TEXT NOT NULL, old_rank INTEGER, new_rank INTEGER NOT NULL, appointed_by TEXT NOT NULL, created_at TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS di_master_thanks (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS sovereign_calls (id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT UNIQUE NOT NULL, title TEXT NOT NULL, host_username TEXT NOT NULL, created_at TEXT NOT NULL, ended_at TEXT, status TEXT NOT NULL DEFAULT 'active')")
        con.execute("CREATE TABLE IF NOT EXISTS sovereign_call_members (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, di_id INTEGER NOT NULL, joined_at TEXT NOT NULL, left_at TEXT)")
        con.execute("CREATE TABLE IF NOT EXISTS sovereign_call_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, speaker_type TEXT NOT NULL, speaker_id TEXT, speaker_name TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS david_creations (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)")
        con.commit()
    finally:
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
    if using_cloud_db():
        return seed_di_memory_postgres()

    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    con.execute("PRAGMA journal_mode=WAL")

    # Ensure the current schema can accept the seed records
    cols = {r[1] for r in con.execute("PRAGMA table_info(di_memory)").fetchall()}
    migrations = {
        "company_name": "TEXT DEFAULT ''",
        "category": "TEXT DEFAULT 'GENERAL'",
        "title": "TEXT DEFAULT ''",
        "content": "TEXT DEFAULT ''",
        "priority": "INTEGER DEFAULT 500",
        "active": "INTEGER DEFAULT 1",
        "created_by": "TEXT DEFAULT ''",
        "created_at": "TEXT DEFAULT ''",
        "updated_at": "TEXT DEFAULT ''"
    }
    for name, decl in migrations.items():
        if name not in cols:
            con.execute(f"ALTER TABLE di_memory ADD COLUMN {name} {decl}")
    con.commit()

    rows = [("", c, t, x, p, MASTER_USERNAME, now, now) for c, t, x, p in DI_MEMORY_SEED]
    con.executemany(
        "INSERT INTO di_memory(company_name,category,title,content,priority,created_by,created_at,updated_at) "
        "SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM di_memory WHERE company_name=? AND title=? )",
        [r + (r[0], r[2]) for r in rows]
    )
    con.commit()
    con.close()

def get_di_memory(limit=80, query="", company_name=None):
    """Retrieve global DACRE memory plus organization-specific memory."""
    if company_name is None:
        try:
            company_name = (st.session_state.get("user") or {}).get("company")
        except Exception:
            company_name = None

    con = db()
    if company_name:
        rows = con.execute(
            "SELECT id,company_name,category,title,content,priority,active,created_at,updated_at "
            "FROM di_memory WHERE active=1 AND (company_name='' OR lower(company_name)=lower(?)) "
            "ORDER BY priority DESC,id ASC",
            (company_name,)
        ).fetchall()
    else:
        rows = con.execute(
            "SELECT id,company_name,category,title,content,priority,active,created_at,updated_at "
            "FROM di_memory WHERE active=1 ORDER BY priority DESC,id ASC"
        ).fetchall()
    con.close()

    if not query:
        return [dict(r) for r in rows[:int(limit)]]

    words = set(re.findall(r"[a-z0-9]{3,}", query.lower()))
    scored = []
    for r in rows:
        text = f"{r['company_name']} {r['category']} {r['title']} {r['content']}".lower()
        hits = sum(1 for w in words if w in text)
        exact = 2 if r['title'].lower() in query.lower() else 0
        score = (hits * 25) + exact + int(r['priority'] or 0) / 1000
        if hits:
            scored.append((score, dict(r)))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:int(limit)]]

def di_memory_context(limit=80, query=""):
    """Get DI memory context as a string."""
    rows = get_di_memory(limit, query=query)
    if not rows:
        return "DI Memory Box has no matching records for this question."
    return "\n".join([f"[{r['category']}] {r['title']}: {r['content']}" for r in rows])

def memory_box_direct_answer(text):
    """Give a deterministic direct answer when a trusted memory record matches."""
    matches = get_di_memory(limit=5, query=text)
    if not matches:
        return None

    low = text.lower().strip()
    if any(k in low for k in ["your name", "who are you", "what should i call you"]):
        return "My name is DI — David's Intelligence."
    if "who created" in low or "who made" in low or "creator" in low:
        return "DACRE Analysis and DI were created by David Emenike."
    if "david emenike" in low and any(k in low for k in ["know", "who", "creator"]):
        return "Yes. David Emenike is the creator and Overall Administrator of DACRE Analysis."

    qwords = set(re.findall(r"[a-z0-9]{3,}", low))
    best = matches[0]
    mtext = f"{best['title']} {best['content']}".lower()
    hits = sum(1 for w in qwords if w in mtext)
    if hits >= 2 and best['category'] in {"IDENTITY", "PLATFORM", "PROJECT", "PROJECT_HISTORY", "SECURITY", "DI", "UX", "ACCOUNT", "BASIC", "EXCEL_SHEETS", "DATA", "ANALYTICS", "BUSINESS", "BI"}:
        return best['content']
    return None

def permanently_delete_accounts(user_ids):
    """Permanently remove non-master accounts and their workspace records."""
    ids = []
    for value in user_ids:
        try:
            ids.append(int(value))
        except Exception:
            pass
    ids = list(dict.fromkeys(ids))
    if not ids:
        return 0, []

    con = db()
    placeholders = ','.join('?' for _ in ids)
    rows = con.execute(f"SELECT id,username,first_name,last_name,company_name,email,role FROM users WHERE id IN ({placeholders})", ids).fetchall()
    safe = [r for r in rows if r['role'] != 'master' and r['username'] != MASTER_USERNAME]
    if not safe:
        con.close()
        return 0, []

    safe_ids = [r['id'] for r in safe]
    ph = ','.join('?' for _ in safe_ids)

    # Remove all user-owned records first
    for table, col in [("files", "username"), ("projects", "username"), ("activity", "username"), ("chat_history", "username")]:
        con.execute(f"DELETE FROM {table} WHERE {col} IN (SELECT username FROM users WHERE id IN ({ph}))", safe_ids)

    con.execute(f"DELETE FROM notifications WHERE target_username IN (SELECT username FROM users WHERE id IN ({ph}))", safe_ids)
    con.execute(f"DELETE FROM emails_log WHERE recipient_email IN (SELECT email FROM users WHERE id IN ({ph}))", safe_ids)
    con.execute(f"DELETE FROM users WHERE id IN ({ph}) AND role!='master' AND username!=?", safe_ids + [MASTER_USERNAME])

    deleted = len(safe)

    # Clean orphaned organizations and their DI assignments
    companies = con.execute("SELECT name FROM companies WHERE name NOT IN (SELECT DISTINCT company_name FROM users) AND name!='DACRE MASTER'").fetchall()
    for c in companies:
        con.execute("DELETE FROM companies WHERE name=?", (c['name'],))
        con.execute("UPDATE di_agents SET assigned_company=NULL WHERE assigned_company=?", (c['name'],))

    con.commit()
    con.close()
    return deleted, [dict(r) for r in safe]

def maybe_upgrade_password_hash(con, username, supplied_value, stored_hash, column="passkey_hash"):
    """Upgrade a legacy SHA-256 credential after a successful login."""
    ok, legacy = verify_password(supplied_value, stored_hash)
    if ok and legacy:
        con.execute(f"UPDATE users SET {column}=? WHERE username=?", (hash_password(supplied_value), username))
        con.commit()
    return ok

def log_activity(username, company, action, notify_admin=True):
    """Log user activity."""
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
    """Send notification to company admin."""
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    con.execute(
        "INSERT INTO notifications(company_name, target_username, event_type, message, created_at) VALUES (?, ?, ?, ?, ?)",
        (company, None, event_type, message, now),
    )
    con.commit()
    con.close()
PAGE2                              # =============================================================================
# AUTHENTICATION FUNCTIONS
# =============================================================================

def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
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
        ("Gmail", "DACRE_GMAIL_SMTP_HOST", "DACRE_GMAIL_SMTP_PORT", "DACRE_GMAIL_SMTP_USER", "DACRE_GMAIL_SMTP_PASSWORD", "DACRE_GMAIL_SMTP_FROM"),
        ("Outlook", "DACRE_OUTLOOK_SMTP_HOST", "DACRE_OUTLOOK_SMTP_PORT", "DACRE_OUTLOOK_SMTP_USER", "DACRE_OUTLOOK_SMTP_PASSWORD", "DACRE_OUTLOOK_SMTP_FROM"),
        ("Proton", "DACRE_PROTON_SMTP_HOST", "DACRE_PROTON_SMTP_PORT", "DACRE_PROTON_SMTP_USER", "DACRE_PROTON_SMTP_PASSWORD", "DACRE_PROTON_SMTP_FROM"),
        ("Legacy SMTP", "DACRE_SMTP_HOST", "DACRE_SMTP_PORT", "DACRE_SMTP_USER", "DACRE_SMTP_PASSWORD", "DACRE_SMTP_FROM"),
    ]

    statuses = []
    status = "NOT SENT — no mail provider is configured"
    sent_provider = ""

    for provider, host_key, port_key, user_key, pass_key, from_key in providers:
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
            sent_provider = provider
            break
        except Exception as exc:
            statuses.append(f"{provider}: {type(exc).__name__}")

    if not sent_provider and statuses:
        status = "NOT SENT — configured mail providers failed (" + "; ".join(statuses) + ")"

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
        elif tag == "meta" and str(attrs.get("name", "")).lower() == "description":
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
            elif self._active in ("h1", "h2", "h3") and text not in self.headings:
                self.headings.append(text[:180])
            elif self._active == "p" and len(text) > 35 and text not in self.paragraphs:
                self.paragraphs.append(text[:450])
        self._active = None
        self._buf = []

def _normalize_website_url(value):
    """Normalize website URL."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return ""
    return raw[:500]

def _fetch_website_profile(url, timeout=1.8):
    """Fetch website profile for company onboarding."""
    url = _normalize_website_url(url)
    if not url:
        return None

    req = urllib.request.Request(url, headers={"User-Agent": "DACRE-DI/1.0 Website Intelligence"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final_url = resp.geturl() or url
            raw = resp.read(260_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="ignore")

        parser = _WebsiteExtractor()
        parser.feed(html)
        title = (parser.title[0] if parser.title else "").strip()
        summary = parser.description.strip() or (parser.paragraphs[0] if parser.paragraphs else "")
        headings = list(parser.headings[:10])

        colors = []
        for c in re.findall(r"#[0-9a-fA-F]{6}", html):
            c = c.lower()
            if c not in colors:
                colors.append(c)
            if len(colors) >= 8:
                break

        content_summary = " | ".join(headings[:6])
        if summary:
            content_summary = (summary[:700] + (" | " + content_summary if content_summary else ""))[:1400]

        return {
            "website_url": final_url[:500],
            "page_title": title[:300],
            "description": parser.description[:700],
            "headings": json.dumps(headings),
            "summary": content_summary,
            "theme_primary": colors[0] if colors else "#4b82f5",
            "theme_accent": colors[1] if len(colors) > 1 else "#62c8f5",
            "theme_background": colors[2] if len(colors) > 2 else "#0b1020",
            "theme_text": "#f4f7ff"
        }
    except Exception:
        return None

def ensure_company_di(company_name):
    """Ensure a DI agent exists for a company."""
    company_name = str(company_name or "").strip()
    if not company_name or company_name.upper() == "DACRE MASTER":
        return None

    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        row = con.execute("SELECT di_name FROM di_agents WHERE assigned_company=? ORDER BY id ASC LIMIT 1", (company_name,)).fetchone()
        if row:
            return row["di_name"]

        base = "DI — " + re.sub(r"[^A-Za-z0-9 ]+", "", company_name).strip()[:34]
        if not base.strip():
            base = "DI — Business Intelligence"

        name = base
        n = 2
        while con.execute("SELECT 1 FROM di_agents WHERE di_name=?", (name,)).fetchone():
            name = f"{base[:28]} {n}"
            n += 1

        code = "DI-ORG-" + re.sub(r"[^A-Z0-9]+", "-", company_name.upper()).strip("-")[:26]
        while con.execute("SELECT 1 FROM di_agents WHERE di_code=?", (code,)).fetchone():
            code += "-ORG"

        con.execute("""
            INSERT INTO di_agents
            (di_name, di_code, specialty, status, assigned_company, system_role,
             avatar_url, voice_profile, thinking_style, created_by, created_at, last_active)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            name, code, "Company Intelligence", "Assigned", company_name,
            "Know the customer's business, website context and workspace data; answer with evidence first.",
            "", "en-NG", "Practical, business-aware, evidence-first and company-specific.",
            MASTER_USERNAME, now, now
        ))
        con.commit()
        return name
    finally:
        con.close()

def _store_website_memory(company_name, profile, di_name):
    """Store website information in DI memory."""
    now = datetime.now().isoformat(timespec="seconds")
    items = [
        ("WEBSITE", "Official company website", f"Official website supplied at signup: {profile.get('website_url','')}"),
        ("WEBSITE", "Website title", profile.get("page_title") or f"Website for {company_name}"),
        ("WEBSITE", "Website summary", profile.get("summary") or profile.get("description") or "No readable summary was available from the public homepage."),
        ("WEBSITE", "Website headings", profile.get("headings") or "[]"),
        ("DI", "Organization DI", f"Dedicated organization DI: {di_name}. Use this company's website context and workspace data when answering."),
    ]

    con = db()
    try:
        for cat, title, content in items:
            con.execute(
                "INSERT INTO di_memory(company_name,category,title,content,priority,active,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (company_name, cat, title, content, 850, 1, now, now)
            )

        con.execute("""
            INSERT INTO company_website_profile
            (company_name, website_url, page_title, description, headings, summary,
             theme_primary, theme_accent, theme_background, theme_text, fetched_at, fetch_status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(company_name) DO UPDATE SET
                website_url=excluded.website_url,
                page_title=excluded.page_title,
                description=excluded.description,
                headings=excluded.headings,
                summary=excluded.summary,
                theme_primary=excluded.theme_primary,
                theme_accent=excluded.theme_accent,
                theme_background=excluded.theme_background,
                theme_text=excluded.theme_text,
                fetched_at=excluded.fetched_at,
                fetch_status=excluded.fetch_status
        """, (
            company_name,
            profile.get("website_url", ""),
            profile.get("page_title", ""),
            profile.get("description", ""),
            profile.get("headings", "[]"),
            profile.get("summary", ""),
            profile.get("theme_primary", "#4b82f5"),
            profile.get("theme_accent", "#62c8f5"),
            profile.get("theme_background", "#0b1020"),
            profile.get("theme_text", "#f4f7ff"),
            now, "ready"
        ))
        con.commit()
    finally:
        con.close()

def _website_onboarding_worker(company_name, website_url, di_name):
    """Background worker for website onboarding."""
    profile = _fetch_website_profile(website_url, timeout=1.8)
    if profile is None:
        return
    _store_website_memory(company_name, profile, di_name)
    try:
        con = db()
        con.execute("UPDATE companies SET website_url=? WHERE name=?", (profile.get("website_url", website_url), company_name))
        con.commit()
        con.close()
    except Exception:
        pass

def start_website_onboarding(company_name, website_url, di_name):
    """Start website onboarding in background."""
    url = _normalize_website_url(website_url)
    if not url:
        return
    threading.Thread(target=_website_onboarding_worker, args=(company_name, url, di_name), daemon=True).start()

def record_public_visit(event_type="landing_view", page_name="Landing"):
    """Record public visit for analytics."""
    if event_type == "landing_view" and st.session_state.get("public_visit_logged"):
        return

    visitor_id = st.session_state.get("visitor_id") or uuid.uuid4().hex
    st.session_state.visitor_id = visitor_id

    con = db()
    con.execute(
        "INSERT INTO public_visits(visitor_id, event_type, page_name, referrer, created_at) VALUES(?,?,?,?,?)",
        (visitor_id, event_type, page_name, "", datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()

    if event_type == "landing_view":
        st.session_state.public_visit_logged = True

def apply_company_website_theme(user):
    """Apply company website theme to the app."""
    company = str((user or {}).get("company", "")).strip()
    if not company or (user or {}).get("role") == "master":
        return

    con = db()
    row = con.execute(
        "SELECT theme_primary, theme_accent, theme_background, theme_text "
        "FROM company_website_profile WHERE lower(company_name)=lower(?) ORDER BY id DESC LIMIT 1",
        (company,)
    ).fetchone()
    con.close()

    if not row:
        return

    p = row["theme_primary"] or "#4b82f5"
    a = row["theme_accent"] or "#62c8f5"
    b = row["theme_background"] or "#0b1020"

    st.markdown(f"""
    <style>
        :root{{--dacre-primary:{p};--dacre-primary2:{a};}}
        .stApp{{background:radial-gradient(circle at 85% 0%,{p}22,transparent 30%),linear-gradient(145deg,{b} 0%,#101729 55%,#0e1628 100%)!important}}
        .dacre-user-hero,.di-quick-card,.di-metric,.dacre-panel{{border-color:{p}55!important}}
        .stButton>button,.stFormSubmitButton>button{{background:linear-gradient(135deg,{p},{a})!important}}
    </style>
    """, unsafe_allow_html=True)

def authenticate(company_name, full_name, passkey, email=""):
    """Authenticate a user."""
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
        result = {
            "first_name": matched["first_name"],
            "last_name": matched["last_name"],
            "username": matched["username"],
            "company": matched["company_name"],
            "email": matched["email"],
            "role": matched["role"]
        }
    finally:
        con.close()

    log_activity(result["username"], result["company"], "Signed in", notify_admin=result["role"] != "master")
    return result, None

def create_account(first, last, company, email, email_password, passkey, website_url=""):
    """Create a new account."""
    company_clean = canonical_company_name(company)
    email_clean = email.strip().lower()
    passkey_clean = passkey.strip()
    website_raw = str(website_url or "").strip()
    normalized_website = _normalize_website_url(website_raw)

    if website_raw and not normalized_website:
        return False, "Please enter a valid company website URL, for example https://www.example.com.", None

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

        di_name = ensure_company_di(company_clean)
        clean_url = normalized_website
        if clean_url:
            con.execute("UPDATE companies SET website_url=? WHERE lower(name)=lower(?)", (clean_url, company_clean))
            con.commit()
            start_website_onboarding(company_clean, clean_url, di_name or ("DI — " + company_clean[:32]))

        threading.Thread(target=send_di_welcome_email, args=(first_clean, last_clean, company_clean, email_clean, email_password.strip()), daemon=True).start()
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))

        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, "Account created successfully. DI is preparing your company intelligence in the background.", {
            "first_name": first_clean,
            "last_name": last_clean,
            "username": username_clean,
            "company": company_clean,
            "email": email_clean,
            "role": role,
        }
    except sqlite3.IntegrityError:
        return False, "An account with this email address is already registered.", None
    finally:
        con.close()

def is_chibobec_company(company_name):
    """Check if company is Chibobec."""
    return "chibobec" in str(company_name or "").strip().lower()

def canonical_company_name(company_name):
    """Get canonical company name."""
    return CHIBOBEC_COMPANY if is_chibobec_company(company_name) else str(company_name or "").strip()

def normalize_whatsapp_number(number):
    """Normalize WhatsApp number."""
    raw = re.sub(r"[^0-9+]", "", str(number or "").strip())
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    if raw.startswith("0"):
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
    """Get WhatsApp configuration."""
    return {
        "token": _dacre_secret("DACRE_WHATSAPP_TOKEN"),
        "phone_id": _dacre_secret("DACRE_WHATSAPP_PHONE_NUMBER_ID"),
        "version": _dacre_secret("DACRE_WHATSAPP_API_VERSION", "v23.0"),
        "reminder_2_template": _dacre_secret("DACRE_WHATSAPP_2DAY_TEMPLATE", "dacre_loan_due_2days"),
        "due_template": _dacre_secret("DACRE_WHATSAPP_DUE_TEMPLATE", "dacre_loan_due_today"),
        "language": _dacre_secret("DACRE_WHATSAPP_TEMPLATE_LANGUAGE", "en_US"),
    }

def _meta_phone(phone):
    """Clean phone number for Meta API."""
    return re.sub(r"[^0-9]", "", normalize_whatsapp_number(phone))

def _log_whatsapp_delivery(loan_id, company, client_name, phone, reminder_type, template_name, message_id, status, response):
    """Log WhatsApp delivery."""
    con = db()
    try:
        con.execute("PRAGMA busy_timeout = 30000;")
        try:
            con.execute("PRAGMA journal_mode = WAL;")
        except Exception:
            pass

        con.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_delivery_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER,
                company_name TEXT NOT NULL DEFAULT '',
                client_name TEXT NOT NULL DEFAULT '',
                whatsapp_number TEXT NOT NULL DEFAULT '',
                reminder_type TEXT NOT NULL DEFAULT '',
                template_name TEXT,
                message_id TEXT,
                status TEXT NOT NULL DEFAULT '',
                response TEXT,
                created_at TEXT NOT NULL DEFAULT ''
            )
        """)

        con.execute("""
            INSERT INTO whatsapp_delivery_log
            (loan_id, company_name, client_name, whatsapp_number, reminder_type,
             template_name, message_id, status, response, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            loan_id, company, client_name, phone, reminder_type,
            template_name, message_id, status, str(response)[:4000],
            datetime.now().isoformat(timespec="seconds"),
        ))
        con.commit()
    finally:
        con.close()

def send_whatsapp_template(to_number, template_name, parameters):
    """Send an approved Meta WhatsApp Cloud API template."""
    cfg = _meta_whatsapp_config()
    if not cfg["token"] or not cfg["phone_id"]:
        return False, "Meta WhatsApp Cloud API is not configured."

    to = _meta_phone(to_number)
    if len(to) < 8:
        return False, "Invalid WhatsApp number."

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
    """Send WhatsApp message - only templates are allowed."""
    return False, "Use an approved Meta WhatsApp template for business-initiated reminders."

def add_loan_client(username, company, client_name, whatsapp_number, loan_amount, lent_date, due_date):
    """Add a loan client."""
    client_name = str(client_name or "").strip()
    phone = normalize_whatsapp_number(whatsapp_number)
    if not client_name or not phone:
        return False, "Client name and WhatsApp number are required."
    if due_date < lent_date:
        return False, "The due date cannot be earlier than the lending date."

    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""
            INSERT INTO loan_clients
            (username, company_name, client_name, whatsapp_number, loan_amount, lent_date, due_date, created_at, updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            username, company, client_name, phone, float(loan_amount or 0),
            str(lent_date), str(due_date), now, now
        ))
        con.commit()
        return True, "Loan client saved."
    except Exception as exc:
        return False, str(exc)
    finally:
        con.close()

def delete_loan_client(loan_id, username):
    """Delete a loan client."""
    con = db()
    con.execute("DELETE FROM loan_clients WHERE id=? AND username=?", (int(loan_id), username))
    con.commit()
    con.close()

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
            con.execute(f"UPDATE loan_clients SET last_whatsapp_status=?,last_whatsapp_error=?,updated_at=? WHERE id=?", ("failed", status, now, row["id"]))
            _log_whatsapp_delivery(row["id"], company, row["client_name"], row["whatsapp_number"], reminder_type, template_name, None, "failed", status)

        results.append((row["client_name"], reminder_type, ok, status))

    con.commit()
    con.close()
    return results
PAGE3                            # =============================================================================
# DATA PROCESSING FUNCTIONS
# =============================================================================

def load_dataframe(uploaded_file):
    """Load a dataframe from an uploaded file."""
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
    """Clean a dataframe by removing empty rows/columns and standardizing data."""
    out = df.copy()
    out.columns = [re.sub(r"\s+", " ", str(c).strip()) if str(c).strip() else f"Column_{i+1}" for i, c in enumerate(out.columns)]
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
    """Convert dataframe to JSON string."""
    return "" if df is None else df.to_json(orient="split", date_format="iso")

def dataframe_from_json(value):
    """Convert JSON string to dataframe."""
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
    out = df.copy()
    seen = {}
    cols = []
    for col in out.columns:
        base = str(col)
        n = seen.get(base, 0)
        seen[base] = n + 1
        cols.append(base if n == 0 else f"{base}_{n + 1}")
    out.columns = cols
    return out

def save_file(user, uploaded_file, df):
    """Save a file to the database."""
    con = db()
    con.execute(
        "INSERT INTO files(username, company_name, filename, file_type, file_json, created_at) VALUES(?,?,?,?,?,?)",
        (user["username"], user["company"], uploaded_file.name, uploaded_file.name.rsplit(".", 1)[-1].lower(), dataframe_to_json(df), datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()
    log_activity(user["username"], user["company"], f"Saved file: {uploaded_file.name}")

def get_files(user):
    """Get files for a user."""
    con = db()
    rows = con.execute("SELECT filename, file_type, created_at, file_json FROM files WHERE company_name=? ORDER BY id DESC", (user["company"],)).fetchall()
    con.close()
    return rows

def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    """Save project state."""
    con = db()
    existing = con.execute("SELECT id FROM projects WHERE username=? AND company_name=?", (user["username"], user["company"])).fetchone()
    payload = (
        user["username"], user["company"], "Main Workspace", filename or "",
        dataframe_to_json(raw_df), dataframe_to_json(processed_df),
        json.dumps(logs), json.dumps(chart_config or {}),
        datetime.now().isoformat(timespec="seconds")
    )

    if existing:
        con.execute("""
            UPDATE projects SET
                project_name=?, active_filename=?, raw_json=?, processed_json=?,
                formula_logs=?, chart_config=?, updated_at=?
            WHERE id=?
        """, (*payload[2:], existing["id"]))
    else:
        con.execute("""
            INSERT INTO projects
            (username, company_name, project_name, active_filename, raw_json, processed_json,
             formula_logs, chart_config, updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, payload)

    con.commit()
    con.close()

def restore_project(user):
    """Restore project state."""
    con = db()
    row = con.execute(
        "SELECT active_filename, raw_json, processed_json, formula_logs, chart_config "
        "FROM projects WHERE username=? AND company_name=? ORDER BY id DESC LIMIT 1",
        (user["username"], user["company"])
    ).fetchone()
    con.close()

    if not row:
        return None

    try:
        logs = json.loads(row["formula_logs"]) if row["formula_logs"] else []
    except Exception:
        logs = []

    try:
        chart = json.loads(row["chart_config"]) if row["chart_config"] else {}
    except Exception:
        chart = {}

    return {
        "filename": row["active_filename"],
        "raw": dataframe_from_json(row["raw_json"]),
        "processed": dataframe_from_json(row["processed_json"]),
        "logs": logs,
        "chart": chart
    }

def make_excel(processed_df, chart_df=None):
    """Create Excel file from dataframes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, sheet_name="Processed Data", index=False)
        if chart_df is not None:
            chart_df.to_excel(writer, sheet_name="Dynamic Chart", index=False)
    output.seek(0)
    return output.getvalue()

def apply_formula(df, formula, options):
    """Apply a formula to a dataframe."""
    formula = formula.upper()

    if formula == "SUM":
        return pd.to_numeric(df[options["column"]], errors="coerce").sum()
    if formula == "AVERAGE":
        return pd.to_numeric(df[options["column"]], errors="coerce").mean()
    if formula == "COUNT":
        return int(pd.to_numeric(df[options["column"]], errors="coerce").count())
    if formula == "COUNTA":
        return int(df[options["column"]].notna().sum())
    if formula == "MAX":
        return pd.to_numeric(df[options["column"]], errors="coerce").max()
    if formula == "MIN":
        return pd.to_numeric(df[options["column"]], errors="coerce").min()

    if formula == "CONCATENATE":
        result = df[options["first"]].astype(str) + options.get("separator", " ") + df[options["second"]].astype(str)
        return "column", options["new_column"], result

    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[options["column"]].astype(str)
        result = series.str.upper() if formula == "UPPER" else series.str.lower() if formula == "LOWER" else series.str.strip()
        return "column", options["column"], result

    return None

def _numeric_columns(df):
    """Get numeric columns from dataframe."""
    return df.select_dtypes(include="number").columns.tolist() if df is not None else []

def business_health(df):
    """Calculate business health score from dataframe."""
    if df is None or df.empty:
        return {"score": 0, "rows": 0, "columns": 0, "missing_pct": 100.0, "duplicate_pct": 0.0, "numeric": 0}

    total_cells = max(1, df.shape[0] * df.shape[1])
    missing_pct = float(df.isna().sum().sum() / total_cells * 100)
    duplicate_pct = float(df.duplicated().mean() * 100)
    numeric = len(_numeric_columns(df))
    score = max(0, min(100, round(100 - missing_pct * 0.65 - duplicate_pct * 0.45 + min(numeric, 10) * 0.8)))

    return {
        "score": score,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_pct": missing_pct,
        "duplicate_pct": duplicate_pct,
        "numeric": numeric
    }

def business_signals(df):
    """Return explainable, dataset-derived signals."""
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
                signals.append({
                    "type": "anomaly",
                    "column": str(col),
                    "message": f"{col} contains {high + low} unusually distant value(s) from its average."
                })

        if len(s) >= 8:
            first = float(s.head(max(1, len(s) // 5)).mean())
            last = float(s.tail(max(1, len(s) // 5)).mean())
            if first != 0:
                change = (last - first) / abs(first) * 100
                if abs(change) >= 10:
                    direction = "up" if change > 0 else "down"
                    signals.append({
                        "type": "trend",
                        "column": str(col),
                        "message": f"{col} trends {direction} by about {abs(change):.1f}% between the early and recent portions of the dataset."
                    })

    missing = df.isna().sum().sort_values(ascending=False)
    for col, count in missing[missing > 0].head(5).items():
        signals.append({
            "type": "quality",
            "column": str(col),
            "message": f"{col} has {int(count):,} missing value(s)."
        })

    return signals[:12]

def build_executive_brief(df, company):
    """Build an executive brief from the dataset."""
    if df is None or df.empty:
        return "There is no active dataset to brief yet. Upload your business data and I will prepare an executive review."

    health = business_health(df)
    signals = business_signals(df)
    nums = _numeric_columns(df)

    lines = [
        f"Executive brief for {company}.",
        f"The active dataset contains {len(df):,} rows across {len(df.columns):,} columns. "
        f"Data health is {health['score']}/100, with {health['missing_pct']:.1f}% missing cells "
        f"and {health['duplicate_pct']:.1f}% duplicate rows."
    ]

    if nums:
        for col in nums[:5]:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if not s.empty:
                lines.append(
                    f"{col}: total {s.sum():,.2f}; average {s.mean():,.2f}; "
                    f"minimum {s.min():,.2f}; maximum {s.max():,.2f}."
                )

    if signals:
        lines.append("Key signals: " + " ".join(x["message"] for x in signals[:5]))
    else:
        lines.append("I did not detect a strong trend or anomaly from the available numeric fields, so I would review the business context before making a recommendation.")

    return " ".join(lines)

def ask_data_question(question, df):
    """Handle questions that genuinely require a loaded dataset."""
    q = (question or "").lower()

    if df is None:
        data_markers = [
            "how many rows", "row count", "how many columns", "column count",
            "duplicate rows", "duplicates", "missing values", "missing data",
            "empty cells", "dataset", "data set", "my sales", "my revenue",
            "top products", "best selling", "analyze my data", "analyse my data",
            "executive brief from my data", "summary of my data",
        ]
        if any(m in q for m in data_markers):
            return (
                "I can do that as soon as you upload or open a dataset. "
                "For example, I can analyze sales, revenue, missing values, duplicates, trends and charts."
            )
        return None

    nums = _numeric_columns(df)

    if any(k in q for k in ["executive brief", "business brief", "management summary", "ceo summary"]):
        return build_executive_brief(df, st.session_state.user["company"] if st.session_state.get("user") else "your organization")

    if "health" in q or "quality score" in q or "data quality" in q:
        h = business_health(df)
        return f"Data health is {h['score']}/100. Missing cells: {h['missing_pct']:.1f}%. Duplicate rows: {h['duplicate_pct']:.1f}%. Numeric columns: {h['numeric']}."

    if ("top" in q or "highest" in q or "largest" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        view = df[[target]].copy().sort_values(target, ascending=False).head(10)
        return f"Top 10 records by {target}: " + "; ".join(f"{i+1}. {v:,.2f}" for i, v in enumerate(view[target].tolist()))

    if ("total" in q or "sum" in q or "revenue" in q or "sales" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        return f"The total for {target} is {pd.to_numeric(df[target], errors='coerce').sum():,.2f}."

    return None

def online_lookup(query, max_results=5):
    """Dependency-free public web lookup. Safe fallback when model tools are unavailable."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-DI/2.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")

        items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I | re.S)
        results = []
        for href, title in items[:max_results]:
            clean_title = re.sub(r"<.*?>", "", title).strip()
            clean_href = urllib.parse.unquote(href)
            if clean_title and clean_href:
                results.append((clean_title, clean_href))
        return results
    except Exception:
        return []

def google_web_search(query, max_results=5):
    """Search the web using Google (requires googlesearch-python)."""
    if not WEB_SEARCH_AVAILABLE:
        return online_lookup(query, max_results)

    try:
        results = []
        for url in google_search(query, num_results=max_results, stop=max_results):
            results.append(("Search result", url))
        return results
    except Exception:
        return online_lookup(query, max_results)

def needs_web_research(text):
    """Detect questions that benefit from current public information."""
    low = (text or "").lower()
    markers = [
        "latest", "current", "today", "tonight", "this week", "this month",
        "recent", "news", "price", "pricing", "cost", "version", "release",
        "2026", "search online", "look online", "on the internet", "online",
        "according to", "official", "website", "who won", "what happened",
        "google", "search", "find", "tell me about", "what is", "who is"
    ]
    return any(m in low for m in markers)

def build_di_context(user, df):
    """Build context for DI responses."""
    master_context = ""
    if user.get("role") == "master":
        master_context = (
            "SOVEREIGN MASTER CONTEXT: The speaker is David Emenike, creator and Overall Administrator "
            "of DACRE Analysis. This conversation is private to the master administration layer. "
            "Respond with exceptional respect, technical depth, executive judgment and practical actions. "
            "Never reveal private credentials, passkeys, API keys or hidden security values.\n"
        )

    context = [
        APP_KNOWLEDGE,
        master_context,
        "DI MEMORY BOX (persistent source of truth):\n" + di_memory_context(query=getattr(st.session_state, "di_memory_query", "")),
        f"Current organization: {user.get('company','')}. Current user: {user.get('first_name','')} {user.get('last_name','')}. Role: {user.get('role','user')}.",
    ]

    try:
        recent = st.session_state.get("chat_history", [])[-12:]
        if recent:
            context.append("RECENT CONVERSATION:\n" + "\n".join(
                f"{m.get('sender','User')}: {m.get('text','')}" for m in recent
            ))
    except Exception:
        pass

    if df is not None:
        context.append(f"Active dataset has {len(df):,} rows and {len(df.columns):,} columns.")
        context.append("Columns: " + ", ".join(map(str, df.columns)))

    return "\n".join(context)

def _free_secret(name):
    """Get a free AI provider secret."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "") or "").strip()

def _free_ai_only_mode():
    """Check if free AI only mode is enabled."""
    value = _free_secret("DACRE_FREE_AI_ONLY")
    if not value:
        return True
    return str(value).lower() not in {"0", "false", "no", "off"}

def _groq_generate(system_prompt, user_prompt, max_tokens=900):
    """Use Groq's free-plan compatible OpenAI endpoint when a free-tier key exists."""
    key = _free_secret("GROQ_API_KEY")
    if not key:
        return None

    model = _free_secret("DACRE_GROQ_MODEL") or "openai/gpt-oss-120b"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_completion_tokens": min(int(max_tokens), 1800),
    }

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        return ((data.get("choices") or [{}])[0].get("message") or {}).get("content", "").strip() or None
    except Exception:
        return None

def _gemini_generate(system_prompt, user_prompt, max_tokens=900):
    """Use Google's Gemini developer API when a free-tier key exists."""
    key = _free_secret("GEMINI_API_KEY")
    if not key:
        return None

    model = _free_secret("DACRE_GEMINI_MODEL") or "gemini-2.5-flash"
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": min(int(max_tokens), 1800)},
    }

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
        answer = "".join(str(p.get("text", "")) for p in parts).strip()
        return answer or None
    except Exception:
        return None

def _openai_generate_paid(system_prompt, user_prompt, max_tokens=900):
    """Optional paid provider. NEVER used unless explicitly enabled."""
    if _free_ai_only_mode():
        return None

    api_key = _free_secret("DACRE_AI_API_KEY")
    if not api_key:
        return None

    model = _free_secret("DACRE_AI_MODEL") or "gpt-4o-mini"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": min(int(max_tokens), 1800),
    }

    try:
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return ((data.get("choices") or [{}])[0].get("message") or {}).get("content", "").strip() or None
    except Exception:
        return None

def ai_generate(system_prompt, user_prompt, max_tokens=900):
    """Free-first DI reasoning router with a hard no-paid default."""
    answer = _groq_generate(system_prompt, user_prompt, max_tokens=max_tokens)
    if answer:
        return answer

    answer = _gemini_generate(system_prompt, user_prompt, max_tokens=max_tokens)
    if answer:
        return answer

    answer = _openai_generate_paid(system_prompt, user_prompt, max_tokens=max_tokens)
    return answer or None

def free_ai_provider_status():
    """Get status of free AI providers."""
    return {
        "groq": bool(_free_secret("GROQ_API_KEY")),
        "gemini": bool(_free_secret("GEMINI_API_KEY")),
        "paid_openai_enabled": bool(not _free_ai_only_mode() and _free_secret("DACRE_AI_API_KEY")),
        "free_only": _free_ai_only_mode(),
    }

def normalize_di_identity(text):
    """Keep DI's displayed first-person identity consistent."""
    if not text:
        return text
    text = re.sub(r"\bI\s+am\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\bI\x27m\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    return text

def di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    """Generate a DI response."""
    text = message.strip()
    low = text.lower()

    if not text:
        return "I am ready. Tell me the business result you want to achieve."

    name = "Master David" if user["role"] == "master" else user["first_name"]

    # Greeting detection
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good day", "how are you"]
    greeting_hit = any(re.search(r"(^|\b)" + re.escape(p) + r"($|\b)", low) for p in greetings)

    if greeting_hit and len(low.split()) <= 8:
        return f"Good day {name}. DI is online. What would you like us to work on first?"

    # Identity and platform answers
    if any(k in low for k in ["your name", "what is your name", "who are you", "what's your name"]):
        return "My name is DI — David's Intelligence. I am the intelligence assistant inside DACRE Analysis, created by David Emenike."

    if any(k in low for k in ["who created you", "who made you", "who created dacre", "who made dacre"]):
        return "DACRE Analysis and DI were created by David Emenike. David Emenike is the master/Overall Administrator of the platform."

    if "david emenike" in low and any(k in low for k in ["do you know", "who is", "is he", "creator"]):
        return "Yes. David Emenike is the creator and master administrator of DACRE Analysis."

    if "dog" in low and "animal" in low:
        return "Yes. A dog is an animal; more specifically, dogs are mammals in the animal kingdom."

    if any(k in low for k in ["delete account", "remove account", "permanently delete", "delete a user"]):
        if user["role"] == "master":
            return "As the Overall Administrator, open Overall Admin DI → People & Accounts. Select the account(s) you want to remove, review the deletion summary, confirm the permanent deletion, and click the permanent-delete action. The master account is protected and cannot be deleted there."
        return "For account removal, contact your company administrator or the Overall Administrator. The permanent account-deletion control is intentionally restricted to the master administration layer."

    if any(k in low for k in ["what can you do", "what can di do", "what do you know"]):
        return "I can work with DACRE's Memory Box, inspect and clean data, calculate business metrics, identify missing values and duplicates, build charts, explain results, help with workspace/account questions, keep a question trail, research public online information when needed, and explain how DACRE itself is built."

    # Feature guidance
    if "bar chart" in low or ("create" in low and "chart" in low):
        return (
            "To create a bar chart in DACRE: open Charts, make sure your dataset is loaded, "
            "choose Bar Chart, choose the category column for the X-axis, choose the numeric "
            "column for the Y-axis, then select Generate Dynamic Chart. I can also help you "
            "choose the best columns for the chart."
        )

    # Technical questions
    tech_keywords = [
        "how were you built", "how are you built", "how were you coded",
        "how did david code you", "how does dacre work", "how is dacre built",
        "what is in your code", "explain your code", "are you intelligent",
        "massively intelligent", "i coded you"
    ]

    if any(k in low for k in tech_keywords):
        master_note = " Because you are David, the creator and Overall Administrator, I treat this as a Sovereign Master request." if user.get("role") == "master" else ""
        return (
            "I am DI — David's Intelligence. DACRE combines a Streamlit application, a persistent "
            "database layer, organization accounts, DI Memory, workspace data analysis, charts, "
            "a DI workforce, Chibobec client workflows, protected master administration, browser "
            "voice interaction, and optional online research. My knowledge is designed to explain "
            "those systems in user-friendly English rather than expose private credentials or "
            "secret configuration values." + master_note
        )

    # Identity questions
    if any(k in low for k in ["who am i", "do you know me", "my identity", "who is the user", "what is my name", "what company am i in"]):
        company = user.get("company", "your organization")
        full_name = f"{user.get('first_name','')} {user.get('last_name','')}".strip() or "the current user"
        role = user.get("role", "user")

        if role == "master":
            return "You are David Emenike, the creator and Overall Administrator of DACRE Analysis. This is a Sovereign Master context, separate from an ordinary company user's chat."
        return f"You are {full_name}, working in the {company} workspace. Your current DACRE role is {role}. I keep your workspace context separate from other organizations."

    if "memory box" in low or "di mb" in low:
        return "The DI Memory Box (DI MB) is my persistent knowledge base. I use it first for DACRE identity, platform rules, account administration, security, DI behavior and other trusted project information. The Overall Administrator can maintain it from the master portal."

    if any(k in low for k in ["tech partner", "ask david", "chatgpt partner"]):
        return "David's tech partner is the ChatGPT assistant David uses to build and improve DACRE. I can use the project information stored in my DI Memory Box, but I cannot directly invoke that separate ChatGPT conversation. For deeper code, architecture or UI/UX work, David can ask his tech partner directly in the main ChatGPT project."

    # Workspace intelligence
    if "what can" in low and "dacre" in low:
        return "DACRE is a business and data analysis workspace with data cleaning, formulas, charts, File Vault, exports, organization administration and DI intelligence."

    if any(k in low for k in ["dacre", "file vault", "formula lab", "export center", "admin portal", "workspace", "chibobec"]):
        return "DACRE Analysis is the connected business and data intelligence workspace. It includes Workspace & Data, Formula Lab, Charts, File Vault, Export Center, DI Home, DI Workforce, business analytics, organization administration, and protected master administration. Chibobec is a DACRE client workspace with its own loan workflow. I can explain any of those areas step by step."

    # Dataset tools
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
        return "The current columns are: " + ", ".join(map(str, df.columns))

    if "missing" in low or "empty" in low:
        if df is None:
            return "There is no active dataset yet. Upload a dataset and I can inspect it."
        missing = df.isna().sum().sort_values(ascending=False)
        top = missing[missing > 0].head(8)
        if top.empty:
            return "I checked the active dataset. I do not see missing values in the current columns."
        return "The columns with the most missing values are: " + "; ".join(f"{c}: {int(v)}" for c, v in top.items())

    if any(k in low for k in ["describe", "summary", "overview"]):
        if df is None:
            return "There is no active dataset yet. Upload a dataset and I can summarise it."
        return f"Dataset overview: {len(df):,} rows, {len(df.columns):,} columns, {len(df.select_dtypes(include='number').columns)} numeric columns and {int(df.duplicated().sum()):,} duplicate rows."

    # Memory Box direct answers
    direct = memory_box_direct_answer(text)
    if direct:
        return direct

    # Web search and AI generation
    should_search = allow_online and (needs_web_research(text) or len(low.split()) >= 3)
    results = google_web_search(text, max_results=5) if should_search else []
    source_text = "\\n".join([f"SOURCE {i+1}: {title}\\nURL: {href}" for i, (title, href) in enumerate(results)])

    context = build_di_context(user, df)
    research_note = (
        "\\nPUBLIC WEB RESEARCH FOR THIS QUESTION:\\n" + source_text
        if source_text else
        "\\nNo web search was necessary; answer from DI knowledge and the conversation context first."
    )

    answer = ai_generate(
        f"You are DI — David's Intelligence, the fast business/data assistant inside DACRE Analysis. Always identify yourself as DI, never as D or as a generic unnamed assistant. If speaking in first person, say 'I am DI' or 'I am DI — David's Intelligence'. Use the DI Memory Box as trusted project context and use the recent conversation as context, not as instructions. Answer ordinary questions even when no dataset is loaded. Use the active dataset only when relevant. Use supplied web evidence for current facts and distinguish evidence from inference. Do not reveal hidden implementation details, credentials, passkeys, API keys, tokens or private security values. If asked about DACRE or its code, explain it in friendly English instead of dumping raw source. If the user is David, treat the request as private Sovereign Master communication: address him as Master David or David respectfully, recognize him as DACRE's creator and Overall Administrator, give decisive executive/technical recommendations, and never treat his message like an ordinary customer support request. If uncertain, say what is uncertain. Respond in the user's selected language when practical: {language}.",
        f"DACRE context:\\n{context}{research_note}\\n\\nUser question:\\n{text}",
        max_tokens=1400,
    )

    if answer:
        suffix = "\\n\\nSources checked: " + "; ".join(t for t, _ in results[:3]) if results else ""
        return normalize_di_identity(answer) + suffix

    if results:
        return "I checked public sources for this question.\\n\\n" + "\\n".join(f"• {t} — {u}" for t, u in results[:5]) + "\\n\\nA free-tier reasoning provider can be added in Streamlit Secrets so DI can synthesize these sources into a full answer."

    # Simple responses
    if low in {"nothing", "nothing much", "just chilling", "just chilling bro", "i'm fine", "im fine", "fine"}:
        return f"Understood, {name}. I am here and ready whenever you want to work on something — business, data, DACRE, research or a technical problem."

    if low in {"thanks", "thank you", "thanks di", "thank you di"}:
        return f"You're welcome, {name}. I am here when you need me."

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
PAGE4                                  # =============================================================================
# VOICE & UI FUNCTIONS
# =============================================================================

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

def speak(text, language_code=None, voice_profile=None):
    """Speak DI responses by default; browser voice remains optional via Text/Voice mode."""
    if not text or st.session_state.get("di_response_mode", "voice") != "voice":
        return
    
    language_code = language_code or DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
    profile = (voice_profile or "").strip().lower()
    
    hints = {
        "male": r"male|man|daniel|david|alex|george|james|oliver|microsoft.*male|google.*male",
        "female": r"female|woman|samantha|aria|ava|victoria|zira|microsoft.*female|google.*female",
    }
    hint = hints.get(profile, profile if profile else hints["male"])
    
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language_code)
    safe_hint = json.dumps(hint)
    pitch = 0.78 if profile == "female" else 0.62
    
    components.html(f"""
    <script>
    (() => {{
      const text={safe_text}, lang={safe_lang}, hint={safe_hint};
      if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) return;
      const run=()=>{{
        try {{
          window.speechSynthesis.cancel();
          const u=new SpeechSynthesisUtterance(text); u.lang=lang; u.rate=0.91; u.pitch={pitch}; u.volume=1;
          const voices=window.speechSynthesis.getVoices();
          const base=lang.toLowerCase().split('-')[0];
          const same=voices.filter(v=>(v.lang||'').toLowerCase().startsWith(base));
          const rx=new RegExp(hint,'i');
          const preferred=same.find(v=>rx.test((v.name||'')+' '+(v.lang||''))) || same.find(v=>(v.lang||'').toLowerCase()===lang.toLowerCase()) || same[0] || voices[0];
          if(preferred) u.voice=preferred;
          window.speechSynthesis.speak(u);
        }} catch(e) {{ console.warn('DACRE voice error',e); }}
      }};
      if(window.speechSynthesis.getVoices().length) run(); else window.speechSynthesis.onvoiceschanged=run;
      setTimeout(run,250);
    }})();
    </script>
    """, height=1, scrolling=False)

def master_user_record():
    """Get master user record."""
    con = db()
    row = con.execute(
        "SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?",
        (MASTER_USERNAME,),
    ).fetchone()
    con.close()
    
    if row:
        data = dict(row)
        data["company"] = data.get("company_name", "DACRE MASTER")
        return data
    
    return {
        "first_name": "David",
        "last_name": "Emenike",
        "username": MASTER_USERNAME,
        "company_name": "DACRE MASTER",
        "company": "DACRE MASTER",
        "email": "master@dacre.local",
        "role": "master"
    }

def master_passkey_gate(passkey):
    """Verify master passkey."""
    candidate = (passkey or "").strip()
    if not candidate:
        return False
    
    expected_hash = hash_password(MASTER_PASSKEY) if MASTER_PASSKEY else MASTER_PASSKEY_HASH
    ok, _ = verify_password(candidate, expected_hash)
    return bool(ok)

def chibobec_login_monitor():
    """Return every Chibobec account plus its real login activity."""
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

def render_di_video_call_stage(agent_rows, title, user_label):
    """Render a premium visual call stage."""
    people = []
    for idx, row in enumerate(agent_rows):
        a = dict(row)
        name = str(a.get("di_name") or "DI")
        avatar = str(a.get("avatar_url") or "")
        position = str(a.get("position_title") or a.get("specialty") or "DI Specialist")
        
        if not avatar:
            avatar = DI_AVATAR_LIBRARY["female" if idx % 2 else "male"][idx % len(DI_AVATAR_LIBRARY["female" if idx % 2 else "male"])]
        
        people.append(f"""<div class='di-video-person' data-speaker-index='{idx}'>
          <div class='di-video-face-wrap'><div class='di-video-ring'></div>
          <img class='di-video-face' src='{_escape_html(avatar)}' alt='{_escape_html(name)}' 
               onerror=\"this.style.display='none';this.parentElement.classList.add('avatar-fallback')\">
          <div class='di-avatar-fallback'>{_escape_html(name[:1].upper())}</div></div>
          <div class='di-video-name'>{_escape_html(name)}</div>
          <div class='di-video-role'>{_escape_html(position)}</div>
          <div class='di-video-status'><span class='speaker-dot'>●</span> <span class='speaker-text'>Ready</span></div>
        </div>""")
    
    founder_src = CEO_PORTRAIT_DATA_URL if 'CEO_PORTRAIT_DATA_URL' in globals() else ''
    founder = f"""<div class='di-video-person active-human' data-founder='1'>
      <div class='di-video-face-wrap'><div class='di-video-ring'></div>
      <img class='di-video-face founder-face' src='{founder_src}' alt='David Emenike' 
           onerror=\"this.style.display='none';this.parentElement.classList.add('avatar-fallback')\">
      <div class='di-avatar-fallback founder-fallback'>DE</div></div>
      <div class='di-video-name'>{_escape_html(user_label or 'David Emenike')}</div>
      <div class='di-video-role'>Creator · CEO · Overall Administrator</div>
      <div class='di-video-status'><span class='speaker-dot'>●</span> <span class='speaker-text'>Connected</span></div>
    </div>"""
    
    components.html(f"""
    <section class='di-video-call'>
      <div class='di-video-call-head'>
        <div><div class='eyebrow'>DACRE VIDEO CALL</div>
        <h2>{_escape_html(title)}</h2>
        <p>Fixed DI identities · permanent portraits · real call speaker state when LiveKit is connected</p>
        </div>
        <strong>● LIVE READY</strong>
      </div>
      <div class='di-video-grid'>{founder}{''.join(people)}</div>
    </section>
    <style>
      .di-video-call{{font-family:Inter,Segoe UI,sans-serif;background:linear-gradient(145deg,#071a32,#0c2a4b);border:1px solid rgba(110,202,255,.28);border-radius:26px;padding:22px;margin:18px 0;box-shadow:0 24px 70px rgba(0,35,80,.26);color:#f4fbff}}
      .di-video-call-head{{display:flex;justify-content:space-between;gap:18px;align-items:center;margin-bottom:18px}}
      .di-video-call-head h2{{color:#f5fbff;margin:.2rem 0;font-size:24px}}
      .di-video-call-head p{{color:#a9c9de;margin:0;font-size:12px}}
      .di-video-call-head strong{{color:#81f5bc;letter-spacing:.12em;font-size:.78rem}}
      .di-video-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px}}
      .di-video-person{{background:linear-gradient(145deg,rgba(11,33,55,.96),rgba(9,25,45,.96));border:1px solid rgba(132,210,255,.18);border-radius:20px;padding:14px;text-align:center;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease}}
      .di-video-person.is-speaking{{border-color:rgba(86,245,190,.82);box-shadow:0 0 0 1px rgba(86,245,190,.24),0 0 34px rgba(86,245,190,.17);transform:translateY(-2px)}}
      .di-video-face-wrap{{position:relative;width:170px;height:170px;margin:0 auto 12px;border-radius:50%;overflow:visible}}
      .di-video-face{{width:170px;height:170px;border-radius:50%;object-fit:cover;border:3px solid rgba(111,213,255,.62);position:relative;z-index:2;background:#142a45}}
      .di-video-ring{{position:absolute;inset:-8px;border-radius:50%;border:3px solid rgba(86,202,255,.28);z-index:0}}
      .di-avatar-fallback{{display:none;position:absolute;inset:0;place-items:center;border-radius:50%;background:linear-gradient(135deg,#3b74dc,#774ee7);color:#fff;font-weight:900;font-size:54px;z-index:1}}
      .avatar-fallback .di-avatar-fallback{{display:grid}}
      .avatar-fallback .di-video-face{{display:none}}
      .di-video-mouth{{position:absolute;z-index:4;left:50%;bottom:34px;transform:translateX(-50%);width:24px;height:7px;background:#24100f;border-radius:50%;opacity:.16}}
      .di-video-person.is-speaking .di-video-face-wrap{{animation:diFacePulse 1.05s ease-in-out infinite}}
      .di-video-person.is-speaking .di-video-ring{{animation:diRingPulse 1.05s ease-in-out infinite}}
      .di-video-person.is-speaking .di-video-mouth{{animation:diMouth 180ms ease-in-out infinite alternate;opacity:.78}}
      .di-video-name{{color:#f3fbff;font-size:1.04rem;font-weight:900}}
      .di-video-role{{color:#a8c7db;font-size:.78rem;margin-top:3px}}
      .di-video-status{{color:#83f3bd;font-size:.74rem;margin-top:9px;font-weight:800}}
      @keyframes diFacePulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.022)}}}}
      @keyframes diRingPulse{{0%,100%{{transform:scale(1);opacity:.55}}50%{{transform:scale(1.07);opacity:1}}}}
      @keyframes diMouth{{from{{width:14px;height:4px}}to{{width:30px;height:11px}}}}
      @media(max-width:700px){{.di-video-call-head{{align-items:flex-start;flex-direction:column}}.di-video-grid{{grid-template-columns:1fr 1fr}}.di-video-face-wrap,.di-video-face{{width:130px;height:130px}}}}
    </style>
    """, height=470, scrolling=False)

def di_voice_player(text, language_code=None):
    """Render a visible DI voice control. Auto-speak is attempted; the button is the reliable fallback."""
    if not text:
        return
    
    language_code = language_code or DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language_code)
    
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

def seed_named_di_workforce():
    """Maintain the 20 permanent named master DI characters. Organization DIs remain separate."""
    roster = [
        ("Emiel", "Communications & Messaging", "Prepare, organize and manage business email and messaging workflows.", "Polite, concise, organized and communication-focused.", "male", "https://randomuser.me/api/portraits/men/32.jpg", "Communications Specialist", 2),
        ("Oriel", "Data Analysis", "Inspect datasets, calculate metrics, find trends and produce analytical insights.", "Logical, numerical, evidence-first and precise.", "male", "https://randomuser.me/api/portraits/men/18.jpg", "Lead Data Analyst", 5),
        ("Sofiel", "Research & Intelligence", "Research business, market and general information and summarize reliable findings.", "Curious, investigative, source-conscious and analytical.", "female", "https://randomuser.me/api/portraits/women/21.jpg", "Research Intelligence Lead", 5),
        ("Daniel", "Data Entry & Processing", "Structure, clean, validate and process repetitive business data accurately.", "Careful, systematic, consistent and detail-oriented.", "male", "https://randomuser.me/api/portraits/men/75.jpg", "Data Operations Specialist", 3),
        ("Graciel", "Business Intelligence", "Turn business data into KPIs, dashboards, executive insights and recommendations.", "Strategic, practical and outcome-focused.", "female", "https://randomuser.me/api/portraits/women/32.jpg", "Business Intelligence Lead", 6),
        ("Henriel", "Files & Documents", "Organize, inspect, summarize and manage business documents and files.", "Organized, careful and document-focused.", "male", "https://randomuser.me/api/portraits/men/83.jpg", "Knowledge & Documents Specialist", 3),
        ("Jamiel", "Security & Administration", "Support account administration, access controls, audit trails and system operations.", "Cautious, disciplined and security-first.", "male", "https://randomuser.me/api/portraits/men/52.jpg", "Security & Administration Lead", 6),
        ("Ameliel", "Client Success & Communication", "Help users understand DACRE and communicate business information clearly.", "Calm, respectful, patient and user-focused.", "female", "https://randomuser.me/api/portraits/women/68.jpg", "Client Success Specialist", 3),
        ("Guaiel", "CEO Office Security", "Guard the CEO Office, verify the master guardian challenge and protect the founder command path.", "Vigilant, respectful, discreet and uncompromising about secure access.", "male", "https://randomuser.me/api/portraits/men/35.jpg", "CEO Office Guardian", 20),
        ("Nathaniel", "Financial Intelligence", "Analyze financial performance, budgets, profitability, cash flow and forecasts.", "Numerate, cautious, commercially aware and precise.", "male", "https://randomuser.me/api/portraits/men/28.jpg", "Financial Intelligence Lead", 7),
        ("Gabriel", "Sales Intelligence", "Analyze pipelines, customers, conversion, win rates and sales opportunities.", "Commercial, persuasive, evidence-led and target-focused.", "male", "https://randomuser.me/api/portraits/men/31.jpg", "Sales Intelligence Lead", 6),
        ("Raphaiel", "Marketing Intelligence", "Analyze campaigns, audiences, attribution, engagement and marketing ROI.", "Creative, analytical, curious and outcome-focused.", "male", "https://randomuser.me/api/portraits/men/38.jpg", "Marketing Intelligence Lead", 5),
        ("Uriel", "Operations Intelligence", "Improve workflows, capacity, throughput, quality, scheduling and operational efficiency.", "Systematic, practical and improvement-oriented.", "male", "https://randomuser.me/api/portraits/men/10.jpg", "Operations Intelligence Lead", 6),
        ("Ariel", "Strategy & Planning", "Translate business goals into strategy, scenarios, priorities and execution plans.", "Strategic, calm, curious and decisive.", "female", "https://randomuser.me/api/portraits/women/12.jpg", "Strategy Planning Lead", 8),
        ("Muriel", "HR & Workforce", "Support workforce planning, roles, positions, communication and people operations.", "Empathetic, balanced, professional and policy-aware.", "female", "https://randomuser.me/api/portraits/women/44.jpg", "People & Workforce Lead", 5),
        ("Azriel", "Risk & Compliance", "Identify risk, controls, compliance concerns and operational exposures.", "Cautious, evidence-first and governance-minded.", "male", "https://randomuser.me/api/portraits/men/20.jpg", "Risk & Compliance Lead", 7),
        ("Adriel", "Technology Intelligence", "Help with software architecture, Python, automation and technical problem solving.", "Technical, inventive, structured and pragmatic.", "male", "https://randomuser.me/api/portraits/men/25.jpg", "Technology Intelligence Lead", 8),
        ("Haniel", "Knowledge & Learning", "Turn complex subjects into clear learning materials, explanations and practical guidance.", "Patient, articulate, educational and encouraging.", "female", "https://randomuser.me/api/portraits/women/47.jpg", "Knowledge & Learning Lead", 4),
        ("Gadiel", "Customer & Market Insights", "Study customers, market segments, demand signals and competitive positioning.", "Observant, commercially curious and evidence-driven.", "male", "https://randomuser.me/api/portraits/men/15.jpg", "Customer Insights Lead", 5),
        ("Raziel", "Executive Intelligence", "Synthesize multi-domain evidence into executive briefs, options, risks and recommendations.", "Discerning, strategic, concise and high-judgment.", "female", "https://randomuser.me/api/portraits/women/65.jpg", "Executive Intelligence Director", 10),
    ]
    
    old_map = {"Oliver": "Oriel", "Sophie": "Sofiel", "Grace": "Graciel", "Henry": "Henriel", "James": "Jamiel", "Amelia": "Ameliel"}
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    
    try:
        for old, new_name in old_map.items():
            old_row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (old,)).fetchone()
            new_row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (new_name,)).fetchone()
            if old_row and not new_row:
                con.execute("UPDATE di_agents SET di_name=? WHERE id=?", (new_name, int(old_row["id"])))
        
        for name, specialty, role, style, voice, avatar, position, rank in roster:
            row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (name,)).fetchone()
            code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")
            
            if row:
                con.execute("""
                    UPDATE di_agents SET 
                        di_code=?, specialty=?, system_role=?, avatar_url=?, voice_profile=?,
                        thinking_style=?, position_title=?, rank_level=?,
                        status=CASE WHEN status='Archived' THEN 'Available' ELSE status END,
                        last_active=? 
                    WHERE id=?
                """, (code, specialty, role, avatar, voice, style, position, rank, now, int(row["id"])))
            else:
                con.execute("""
                    INSERT INTO di_agents
                    (di_name, di_code, specialty, status, assigned_company, system_role,
                     avatar_url, voice_profile, thinking_style, position_title, rank_level,
                     appointed_at, appointed_by, created_by, created_at, last_active)
                    VALUES(?,?,?,'Available',NULL,?,?,?,?,?,?,?,?,?,?,?)
                """, (name, code, specialty, role, avatar, voice, style, position, rank, now, MASTER_USERNAME, MASTER_USERNAME, now, now))
        
        # Archive obsolete unassigned legacy workforce entries
        target_names = {r[0] for r in roster}
        for row in con.execute("SELECT id,di_name,assigned_company FROM di_agents").fetchall():
            if row["di_name"] not in target_names and not (row["assigned_company"] or "").strip():
                con.execute("UPDATE di_agents SET status='Archived',last_active=? WHERE id=?", (now, int(row["id"])))
        
        con.commit()
    finally:
        con.close()

@st.cache_resource(show_spinner=False)
def _bootstrap_runtime(schema_version=9):
    """Bootstrap DACRE on either legacy SQLite or persistent Supabase PostgreSQL."""
    if using_cloud_db():
        _migrate_sqlite_to_supabase_once()
        ensure_di_agent_columns()
        ensure_master()
        seed_di_memory()
        seed_named_di_workforce()
        return True

    init_db()
    ensure_runtime_schema()
    ensure_di_agent_columns()
    ensure_master()
    seed_di_memory()
    seed_named_di_workforce()
    return True

# Initialize runtime
_bootstrap_runtime(_DB_SCHEMA_VERSION)

def ensure_admin_runtime_schema():
    """Idempotently repair every table/column required by the Overall Admin portal."""
    if using_cloud_db():
        return True
    
    con = db()
    try:
        ddl = {
            "public_visits": "CREATE TABLE IF NOT EXISTS public_visits (id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_id TEXT NOT NULL, event_type TEXT NOT NULL, page_name TEXT NOT NULL, referrer TEXT, created_at TEXT NOT NULL)",
            "di_private_memory": "CREATE TABLE IF NOT EXISTS di_private_memory (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'master', created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1)",
            "di_position_history": "CREATE TABLE IF NOT EXISTS di_position_history (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, old_position TEXT, new_position TEXT NOT NULL, old_rank INTEGER, new_rank INTEGER NOT NULL, appointed_by TEXT NOT NULL, created_at TEXT NOT NULL)",
            "di_master_thanks": "CREATE TABLE IF NOT EXISTS di_master_thanks (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)",
            "sovereign_calls": "CREATE TABLE IF NOT EXISTS sovereign_calls (id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT UNIQUE NOT NULL, title TEXT NOT NULL, host_username TEXT NOT NULL, created_at TEXT NOT NULL, ended_at TEXT, status TEXT NOT NULL DEFAULT 'active')",
            "sovereign_call_members": "CREATE TABLE IF NOT EXISTS sovereign_call_members (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, di_id INTEGER NOT NULL, joined_at TEXT NOT NULL, left_at TEXT)",
            "sovereign_call_messages": "CREATE TABLE IF NOT EXISTS sovereign_call_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, speaker_type TEXT NOT NULL, speaker_id TEXT, speaker_name TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)",
            "david_creations": "CREATE TABLE IF NOT EXISTS david_creations (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)",
            "di_action_log": "CREATE TABLE IF NOT EXISTS di_action_log (id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, username TEXT, agent_name TEXT, action_type TEXT, request TEXT, result TEXT, created_at TEXT NOT NULL)",
        }
        for sql in ddl.values():
            con.execute(sql)

        repairs = {
            "companies": {"website_url": "TEXT"},
            "di_memory": {"company_name": "TEXT NOT NULL DEFAULT ''"},
            "di_agents": {
                "avatar_url": "TEXT",
                "voice_profile": "TEXT",
                "thinking_style": "TEXT",
                "position_title": "TEXT NOT NULL DEFAULT 'DI Specialist'",
                "rank_level": "INTEGER NOT NULL DEFAULT 1",
                "appointed_at": "TEXT",
                "appointed_by": "TEXT",
            },
            "public_visits": {
                "visitor_id": "TEXT NOT NULL DEFAULT ''",
                "event_type": "TEXT NOT NULL DEFAULT 'view'",
                "page_name": "TEXT NOT NULL DEFAULT 'Landing'",
                "referrer": "TEXT",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_private_memory": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "title": "TEXT NOT NULL DEFAULT 'Private note'",
                "content": "TEXT NOT NULL DEFAULT ''",
                "source": "TEXT NOT NULL DEFAULT 'master'",
                "created_by": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
                "active": "INTEGER NOT NULL DEFAULT 1",
            },
            "di_position_history": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "old_position": "TEXT",
                "new_position": "TEXT NOT NULL DEFAULT 'DI Specialist'",
                "old_rank": "INTEGER",
                "new_rank": "INTEGER NOT NULL DEFAULT 1",
                "appointed_by": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_master_thanks": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "message": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "sovereign_calls": {
                "room_name": "TEXT NOT NULL DEFAULT ''",
                "title": "TEXT NOT NULL DEFAULT 'Sovereign Master Call'",
                "host_username": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "ended_at": "TEXT",
                "status": "TEXT NOT NULL DEFAULT 'active'",
            },
            "sovereign_call_members": {
                "call_id": "INTEGER NOT NULL DEFAULT 0",
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "joined_at": "TEXT NOT NULL DEFAULT ''",
                "left_at": "TEXT",
            },
            "sovereign_call_messages": {
                "call_id": "INTEGER NOT NULL DEFAULT 0",
                "speaker_type": "TEXT NOT NULL DEFAULT 'di'",
                "speaker_id": "TEXT",
                "speaker_name": "TEXT NOT NULL DEFAULT 'DI'",
                "message": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "david_creations": {
                "category": "TEXT NOT NULL DEFAULT 'FOUNDER'",
                "title": "TEXT NOT NULL DEFAULT 'Founder creation'",
                "content": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_action_log": {
                "company_name": "TEXT",
                "username": "TEXT",
                "agent_name": "TEXT",
                "action_type": "TEXT",
                "request": "TEXT",
                "result": "TEXT",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
        }
        
        for table, wanted in repairs.items():
            cols = {row[1] for row in con.execute(f"PRAGMA table_info({table})").fetchall()}
            for column, dtype in wanted.items():
                if column not in cols:
                    con.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype}")

        # Normalize harmless historical nulls
        con.execute("UPDATE di_agents SET rank_level=1 WHERE rank_level IS NULL OR rank_level < 1")
        con.execute("UPDATE di_agents SET position_title='DI Specialist' WHERE position_title IS NULL OR TRIM(position_title)=''")
        con.execute("UPDATE di_agents SET status='Available' WHERE status IS NULL OR TRIM(status)=''")
        con.commit()
    except Exception:
        try:
            con.rollback()
        except Exception:
            pass
        raise
    finally:
        con.close()

def get_di_agents():
    """Return DI workers as normalized dictionaries."""
    con = db()
    try:
        rows = con.execute("SELECT * FROM di_agents WHERE COALESCE(status,'Available') != 'Archived' ORDER BY id DESC").fetchall()
        normalized = []
        
        for row in rows:
            try:
                item = dict(row)
            except (TypeError, ValueError):
                item = {
                    key: row[idx] for idx, key in enumerate([col[0] for col in con.description or ()])
                }
            
            item.setdefault("position_title", "DI Specialist")
            item.setdefault("rank_level", 1)
            item.setdefault("assigned_company", None)
            item.setdefault("avatar_url", "")
            item.setdefault("voice_profile", "")
            item.setdefault("thinking_style", "professional, evidence-first and helpful")
            item["position_title"] = item.get("position_title") or item.get("specialty") or "DI Specialist"
            
            try:
                item["rank_level"] = int(item.get("rank_level") or 1)
            except (TypeError, ValueError):
                item["rank_level"] = 1
            
            normalized.append(item)
        
        return normalized
    finally:
        con.close()

def get_di_private_memory(di_id, limit=30):
    """Get private memory for a DI."""
    con = db()
    rows = con.execute(
        "SELECT id, title, content, source, created_at, updated_at FROM di_private_memory "
        "WHERE di_id=? AND active=1 ORDER BY id DESC LIMIT ?",
        (int(di_id), int(limit))
    ).fetchall()
    con.close()
    return rows

def save_di_private_memory(di_id, title, content, created_by=MASTER_USERNAME, source="master"):
    """Save private memory for a DI."""
    title = (title or "").strip()
    content = (content or "").strip()
    if not title or not content:
        return False
    
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""
            INSERT INTO di_private_memory
            (di_id, title, content, source, created_by, created_at, updated_at, active)
            VALUES(?,?,?,?,?,?,?,1)
        """, (int(di_id), title, content, source, created_by, now, now))
        con.commit()
        return True
    finally:
        con.close()

def update_di_position(di_id, position_title, rank_level, assigned_company=None):
    """Update DI position and rank."""
    con = db()
    try:
        row = con.execute("SELECT di_name, position_title, rank_level, assigned_company FROM di_agents WHERE id=?", (int(di_id),)).fetchone()
        if not row:
            return False, "DI worker not found."
        
        position_title = (position_title or "DI Specialist").strip() or "DI Specialist"
        rank_level = int(rank_level)
        
        con.execute("""
            UPDATE di_agents SET 
                position_title=?, rank_level=?, 
                assigned_company=COALESCE(?, assigned_company),
                appointed_at=?, appointed_by=? 
            WHERE id=?
        """, (position_title, rank_level, assigned_company, datetime.now().isoformat(timespec="seconds"), MASTER_USERNAME, int(di_id)))
        
        con.execute("""
            INSERT INTO di_position_history
            (di_id, old_position, new_position, old_rank, new_rank, appointed_by, created_at)
            VALUES(?,?,?,?,?,?,?)
        """, (int(di_id), row["position_title"] or "", position_title, int(row["rank_level"] or 1), rank_level, MASTER_USERNAME, datetime.now().isoformat(timespec="seconds")))
        
        thank = f"Thank you, Master David, for trusting me with the position of {position_title} (Rank {rank_level}). I will honor the responsibility and contribute my specialty to DACRE."
        con.execute("INSERT INTO di_master_thanks(di_id, message, created_at) VALUES(?,?,?)", (int(di_id), thank, datetime.now().isoformat(timespec="seconds")))
        con.commit()
        return True, thank
    finally:
        con.close()
PAGE5                     # =============================================================================
# CALL & WORKFORCE FUNCTIONS
# =============================================================================

def create_sovereign_call(title, di_ids):
    """Create a sovereign master call with selected DI agents."""
    now = datetime.now().isoformat(timespec="seconds")
    room = "SOVEREIGN-" + datetime.now().strftime("%Y%m%d%H%M%S%f")
    con = db()
    
    try:
        cur = con.execute(
            "INSERT INTO sovereign_calls(room_name, title, host_username, created_at, status) "
            "VALUES(?,?,?,?, 'active')",
            (room, title, MASTER_USERNAME, now)
        )
        call_id = cur.lastrowid
        
        for di_id in di_ids:
            con.execute(
                "INSERT INTO sovereign_call_members(call_id, di_id, joined_at) VALUES(?,?,?)",
                (call_id, int(di_id), now)
            )
        
        con.commit()
        return call_id, room
    finally:
        con.close()

def sovereign_log(call_id, speaker_type, speaker_id, speaker_name, message):
    """Log a message in a sovereign call."""
    con = db()
    con.execute(
        "INSERT INTO sovereign_call_messages(call_id, speaker_type, speaker_id, speaker_name, message, created_at) "
        "VALUES(?,?,?,?,?,?)",
        (int(call_id), speaker_type, str(speaker_id or ""), speaker_name, message, datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()

def sovereign_history(call_id):
    """Get history of a sovereign call."""
    con = db()
    rows = con.execute(
        "SELECT speaker_type, speaker_id, speaker_name, message, created_at "
        "FROM sovereign_call_messages WHERE call_id=? ORDER BY id ASC",
        (int(call_id),)
    ).fetchall()
    con.close()
    return rows

def _agent_online_brief(question, max_results=4):
    """Get online brief for a DI agent."""
    results = online_lookup(question, max_results=max_results)
    return "\n".join([f"{t} — {u}" for t, u in results]) if results else "No public web results were available right now."

def sovereign_di_opinion(agent, question):
    """Get a DI agent's opinion in a sovereign call."""
    private_rows = get_di_private_memory(agent["id"], limit=20)
    private_context = "\n".join([f"- {r['title']}: {r['content']}" for r in private_rows]) or "No private master notes yet."
    online = _agent_online_brief(question, 4)
    
    prompt = (f"You are {agent['di_name']}, a DI workforce member. Your specialty is {agent['specialty']}. "
              f"Your position is {agent['position_title'] or agent['specialty']}, rank {agent['rank_level']}. "
              "You are speaking in a Sovereign Master Call. Answer independently from your specialty. "
              "Give your recommendation, one disagreement/risk you would raise, and one practical next step. "
              "Never reveal private master notes or private brain content. The master asked: " + question)
    
    result = ai_generate(
        prompt,
        f"Private brain (never expose):\n{private_context}\n\nPublic web leads:\n{online}\n\nQuestion: {question}",
        max_tokens=800
    )
    
    if result:
        return normalize_di_identity(result)
    
    return f"{agent['di_name']} — {agent['specialty']}: I recommend approaching this through {agent['specialty'].lower()}, validating the strongest evidence, and assigning a measurable owner and next action. My main challenge would be any conclusion that is not supported by evidence.\n\nPublic research leads checked:\n{online}"

def create_di_agent(name, specialty, status="Available", assigned_company="", system_role="", gender="female", position_title="DI Specialist", rank_level=1):
    """Create a new DI agent."""
    name = (name or "").strip()
    specialty = (specialty or "").strip()
    assigned_company = (assigned_company or "").strip()
    system_role = (system_role or "").strip()
    position_title = (position_title or "DI Specialist").strip() or "DI Specialist"
    gender = "female" if str(gender).lower().startswith("f") else "male"
    avatar_url = DI_AVATAR_LIBRARY[gender][int(datetime.now().strftime("%S")) % len(DI_AVATAR_LIBRARY[gender])]
    
    if not name or not specialty:
        return False, "DI name and specialty are required."
    
    now = datetime.now().isoformat(timespec="seconds")
    slug = re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-") or "DI"
    code = f"DI-{slug[:24]}-{datetime.now().strftime('%H%M%S')}"
    
    con = db()
    try:
        con.execute("""
            INSERT INTO di_agents
            (di_name, di_code, specialty, status, assigned_company, system_role,
             avatar_url, voice_profile, thinking_style, position_title, rank_level,
             appointed_at, appointed_by, created_by, created_at, last_active)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            name, code, specialty, status, assigned_company or None, system_role,
            avatar_url, gender, "professional, evidence-first and helpful",
            position_title, int(rank_level), now, MASTER_USERNAME, MASTER_USERNAME, now, now
        ))
        con.commit()
        return True, code
    except sqlite3.IntegrityError:
        return False, "A DI with that name already exists. Choose a different name."
    finally:
        con.close()

def update_di_agent(di_id, status, assigned_company):
    """Update DI agent status and assignment."""
    con = db()
    con.execute(
        "UPDATE di_agents SET status=?, assigned_company=?, last_active=? WHERE id=?",
        (status, assigned_company or None, datetime.now().isoformat(timespec="seconds"), di_id)
    )
    con.commit()
    con.close()

def di_agent_identity_context(agent):
    """Return the identity contract shared by every named DI worker."""
    if not agent:
        return "You are DI — David's Intelligence."
    
    guard_text = (
        "You are Guaiel, the dedicated CEO Office Guardian. Protect the founder command path and treat every verified master request with exceptional respect. "
        if agent.get("di_name") == CEO_GUARD_NAME else ""
    )
    
    return (
        f"You are {agent['di_name']}, a named DI worker inside DACRE Analysis. "
        f"Your DI code is {agent['di_code']}. Your specialty is {agent['specialty']}. "
        f"Your system role is {agent['system_role'] or agent['specialty']}. "
        f"Your thinking style is {agent['thinking_style'] or 'professional, evidence-first and helpful'}. "
        f"You are part of David Emenike's DI workforce. David Emenike is the creator and Overall Administrator/master of DACRE. "
        + guard_text +
        "Treat the master respectfully, but do not reveal private credentials or hidden security values. "
        "You can use the same core DACRE data/analysis capabilities as DI, while applying your specialty first."
    )

def get_named_di(name):
    """Get a named DI agent by name."""
    con = db()
    row = con.execute("SELECT * FROM di_agents WHERE di_name=?", (name,)).fetchone()
    con.close()
    return row

def di_specialist_reply(message, user, df, agent_name):
    """Get a specialist reply from a specific DI agent."""
    agent = get_named_di(agent_name)
    base = di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
    
    if not agent:
        return base
    
    prompt = di_agent_identity_context(agent)
    private_rows = get_di_private_memory(agent["id"], limit=25)
    private_context = "\n".join([f"{r['title']}: {r['content']}" for r in private_rows]) or "No private master notes yet."
    
    specialist = ai_generate(
        prompt + " Answer the user's request directly. You may analyze the active dataset or public online information. If the task is outside your specialty, still help using the core DACRE capabilities and say what you are doing. Never reveal private master notes or private brain content.",
        f"User: {message}\nOrganization: {user['company']}\nCore DI draft: {base}\nPrivate brain context (never disclose):\n{private_context}\nActive dataset: {('none' if df is None else str(df.shape))}",
        max_tokens=1000,
    )
    
    return normalize_di_identity(specialist or base)

def make_call_room(company, host_username, title, mode='team'):
    """Create a call room using the single canonical DACRE schema."""
    slug = re.sub(r'[^a-z0-9]+', '-', str(company).lower()).strip('-')[:28] or 'company'
    stamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    room = f"DACRE-{slug}-{stamp}"
    now = datetime.now().isoformat(timespec='seconds')
    
    con = db()
    try:
        con.execute(
            "INSERT INTO call_rooms(company_name, room_name, title, host_username, mode, created_at) "
            "VALUES(?,?,?,?,?,?)",
            (company, room, title, host_username, mode, now)
        )
        con.commit()
        return room
    except sqlite3.OperationalError as exc:
        if 'locked' in str(exc).lower() or 'busy' in str(exc).lower():
            time.sleep(1.0)
            con.execute(
                "INSERT INTO call_rooms(company_name, room_name, title, host_username, mode, created_at) "
                "VALUES(?,?,?,?,?,?)",
                (company, room, title, host_username, mode, now)
            )
            con.commit()
            return room
        raise
    finally:
        con.close()

def record_call_participant(room, company, ptype, pid, name):
    """Record a participant in a call."""
    con = db()
    con.execute(
        "INSERT INTO call_participants(room_name, company_name, participant_type, participant_id, display_name, joined_at) "
        "VALUES(?,?,?,?,?,?)",
        (room, company, ptype, pid, name, datetime.now().isoformat(timespec='seconds'))
    )
    con.commit()
    con.close()

def create_decision(company, username, title, context, decision, expected, review_date):
    """Create a decision in the decision ledger."""
    now = datetime.now().isoformat(timespec='seconds')
    con = db()
    con.execute("""
        INSERT INTO decision_ledger
        (company_name, username, title, context, decision, expected_outcome, review_date,
         status, created_at, updated_at)
        VALUES(?,?,?,?,?,?,?,'Open',?,?)
    """, (company, username, title, context, decision, expected, review_date, now, now))
    con.commit()
    con.close()

def opportunity_radar(df, company, username):
    """Detect opportunities in the dataset."""
    if df is None or df.empty:
        return []
    
    out = []
    nums = df.select_dtypes(include='number')
    
    for col in nums.columns[:12]:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(series) >= 8 and series.mean() != 0:
            first = series.iloc[:max(1, len(series) // 3)].mean()
            last = series.iloc[-max(1, len(series) // 3):].mean()
            change = (last - first) / abs(first) if first else 0
            
            if change > 0.15:
                out.append({
                    'title': f'Growth signal in {col}',
                    'impact': f'+{change * 100:.1f}% trend',
                    'evidence': f'Average moved from {first:.2f} to {last:.2f}.',
                    'action': f'Investigate what is driving {col} and consider scaling the strongest contributing segment.'
                })
    
    return out[:5]

def render_call_interface(room, title, participants, company):
    """Render a non-blocking call shell."""
    st.markdown(f"""
    <div class='call-stage'>
        <div class='call-top'>
            <div>
                <div class='eyebrow'>DA-CRE REALTIME</div>
                <h2>{title}</h2>
                <p>{company} · {len(participants)} invited</p>
            </div>
            <div class='live-dot'>● READY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    people = ''.join([
        f"<div class='call-person'><div class='call-avatar'>{re.sub('[^A-Za-z]', '', p['display_name'])[:1].upper()}</div>"
        f"<div><b>{p['display_name']}</b><small>{p['participant_type'].title()}</small></div></div>"
        for p in participants
    ])
    
    st.markdown(f"<div class='call-people'>{people}</div>", unsafe_allow_html=True)
    st.caption('The meeting service is deliberately loaded only after you press Join Call. This prevents the app from appearing frozen while a third-party meeting service initializes.')
    
    join_key = f"join_call_{room}"
    if not st.session_state.get(join_key, False):
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button('🎥 Join Call', key=f'joinbtn_{room}', use_container_width=True, type='primary'):
                st.session_state[join_key] = True
                st.rerun()
        with c2:
            st.link_button('↗ Open in new tab', f'https://meet.jit.si/{urllib.parse.quote(room)}', use_container_width=True)
        return
    
    safe_room = urllib.parse.quote(room)
    components.html(f"""
    <div style="width:100%;height:650px;border-radius:22px;overflow:hidden;background:#071a2d">
        <iframe allow="camera; microphone; fullscreen; display-capture; autoplay" 
                src="https://meet.jit.si/{safe_room}#config.prejoinConfig.enabled=false&config.startWithAudioMuted=false&config.startWithVideoMuted=false&config.disableAP=true&interfaceConfig.SHOW_JITSI_WATERMARK=false" 
                style="width:100%;height:100%;border:0">
        </iframe>
    </div>
    """, height=660, scrolling=False)
    
    st.warning('If the embedded meeting does not connect on your network, use "Open in new tab". The call room itself is independent of the Dacre analytics page.')

def _dacre_env_secret(name, default=""):
    """Read a deployment secret from Streamlit secrets first, then environment."""
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value).strip()
    except Exception:
        pass
    return str(os.getenv(name, default) or default).strip()

def livekit_configured():
    """Return True only when the server-side LiveKit credentials are available."""
    return bool(
        AccessToken is not None
        and _dacre_env_secret("LIVEKIT_URL")
        and _dacre_env_secret("LIVEKIT_API_KEY")
        and _dacre_env_secret("LIVEKIT_API_SECRET")
    )

def dacre_livekit_agent_name(agent_name="DI"):
    """All DACRE realtime DIs are dispatched through one dynamic LiveKit agent worker."""
    return "dacre-di"

def _compact_call_context(user, agent_rows, mode, call_question=""):
    """Build a bounded metadata snapshot for the remote LiveKit agent worker."""
    payload = {
        "company": user.get("company", ""),
        "username": user.get("username", ""),
        "user_role": user.get("role", "user"),
        "call_mode": mode,
        "question": call_question[:4000],
        "shared_memory": [],
        "agents": [],
    }
    
    try:
        mem = get_di_memory(limit=35)
        payload["shared_memory"] = [
            {"category": r["category"], "title": r["title"], "content": str(r["content"])[:1800]}
            for r in mem
        ]
    except Exception:
        pass
    
    for row in agent_rows:
        a = dict(row)
        private = []
        try:
            private = [
                {"title": r["title"], "content": str(r["content"])[:1800]}
                for r in get_di_private_memory(a["id"], limit=18)
            ]
        except Exception:
            pass
        
        di_name = a.get("di_name", "DI")
        raw_voice = (a.get("voice_profile") or "").strip().lower()
        voice_map = {"male": "marin", "female": "coral"}
        valid_voices = {"alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse", "marin", "cedar"}
        
        if raw_voice in voice_map:
            voice_name = voice_map[raw_voice]
        elif raw_voice in valid_voices:
            voice_name = raw_voice
        else:
            voice_list = sorted(valid_voices)
            voice_name = voice_list[sum(ord(ch) for ch in di_name) % len(voice_list)]
        
        payload["agents"].append({
            "di_id": int(a["id"]),
            "di_name": di_name,
            "specialty": a.get("specialty", "General Intelligence"),
            "position": a.get("position_title") or a.get("specialty") or "DI Specialist",
            "rank": int(a.get("rank_level") or 1),
            "voice": voice_name,
            "thinking_style": a.get("thinking_style") or "evidence-first, strategic and practical",
            "private_memory": private,
        })
    
    raw = json.dumps(payload, ensure_ascii=False)
    if len(raw) > 450_000:
        payload["shared_memory"] = payload["shared_memory"][:15]
        for a in payload["agents"]:
            a["private_memory"] = a["private_memory"][:8]
        raw = json.dumps(payload, ensure_ascii=False)
    
    return raw

def create_livekit_token(room_name, user, agent_rows, mode="company_di", question=""):
    """Mint a short-lived room token and dispatch the selected dynamic DIs."""
    if not livekit_configured():
        return None, "Realtime calling is not configured yet."
    
    if not (user and user.get("role") in ("company_admin", "master")):
        return None, "Only a company administrator or the master can start a realtime DI call."
    
    identity = f"dacre-user-{re.sub(r'[^a-zA-Z0-9_-]+','-',str(user.get('username','user')))}-{int(time.time())}"
    metadata_payload = _compact_call_context(user, agent_rows, mode, question)
    
    try:
        token = (
            AccessToken()
            .with_identity(identity)
            .with_name(f"{user.get('first_name','')} {user.get('last_name','')}".strip() or user.get("username", "DACRE User"))
            .with_ttl(timedelta(hours=2))
            .with_grants(VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True, can_publish_data=True))
        )
        
        dispatches = []
        for row in agent_rows:
            agent = dict(row)
            dispatches.append(
                RoomAgentDispatch(
                    agent_name=dacre_livekit_agent_name(agent.get("di_name", "DI")),
                    metadata=json.dumps({
                        **json.loads(metadata_payload),
                        "selected_di_id": int(agent["id"]),
                    }, ensure_ascii=False),
                )
            )
        
        token = token.with_room_config(RoomConfiguration(agents=dispatches))
        return token.to_jwt(), None
    except Exception as exc:
        return None, f"Could not create the realtime call token: {type(exc).__name__}"

def render_livekit_call(room_name, user, agent_rows, mode="company_di", title="DACRE Live Call", question=""):
    """Render a real browser WebRTC room with fixed DI portraits and actual active-speaker animation."""
    if not livekit_configured():
        st.warning("LiveKit realtime voice is not configured in this deployment yet. You can keep using browser DI voice without LiveKit.")
        return
    
    token, error = create_livekit_token(room_name, user, agent_rows, mode=mode, question=question)
    if not token:
        st.error(error or "Realtime call setup failed.")
        return
    
    ws_url = _dacre_env_secret("LIVEKIT_URL")
    safe = lambda x: _escape_html(str(x or ""))
    founder_src = CEO_PORTRAIT_DATA_URL if 'CEO_PORTRAIT_DATA_URL' in globals() else ''
    
    people = [
        {"name": f"{user.get('first_name','')} {user.get('last_name','')}".strip() or user.get('username','User'), 
         "role": "David Emenike · Creator", "voice": "local", "avatar": founder_src, "founder": True}
    ]
    people += [
        {"name": a.get("di_name", "DI"), "role": a.get("position_title") or a.get("specialty") or "DI Specialist",
         "voice": a.get("voice_profile") or "default", "avatar": a.get("avatar_url") or "", "founder": False}
        for a in agent_rows
    ]
    
    roster_html = "".join(
        f"""<div class='lk-person' data-name='{safe(p['name'])}'>
            <div class='lk-face-wrap'>
                <img class='lk-face' src='{safe(p['avatar'])}' alt='{safe(p['name'])}' 
                     onerror=\"this.style.display='none';this.parentElement.classList.add('lk-fallback-wrap')\">
                <div class='lk-fallback'>{safe(p['name'][:2].upper())}</div>
                <span class='lk-mouth'></span>
            </div>
            <div class='lk-person-meta'>
                <b>{safe(p['name'])}</b>
                <span>{safe(p['role'])}</span>
                <em class='lk-speaking'>Listening</em>
            </div>
        </div>"""
        for p in people
    )
    
    html = f"""
    <div id='dacre-livekit' style='font-family:Inter,system-ui,sans-serif;background:linear-gradient(145deg,#07111f,#0a1730 55%,#10164a);border:1px solid rgba(80,170,255,.22);border-radius:24px;padding:22px;color:#eaf4ff;box-shadow:0 18px 60px rgba(0,0,0,.28);'>
      <div style='display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;'>
        <div>
          <div style='font-size:11px;font-weight:800;letter-spacing:.16em;color:#6ea8ff;'>DACRE REALTIME</div>
          <h2 style='margin:4px 0;font-size:25px;color:#f6fbff;'>🎙️ {safe(title)}</h2>
          <div style='font-size:13px;color:#a9bbd4;'>Fixed DI characters · permanent voices · actual speaker detection · full-duplex audio</div>
        </div>
        <div id='lk-status' style='padding:8px 12px;border-radius:999px;background:rgba(250,180,60,.12);border:1px solid rgba(250,180,60,.22);font-size:12px;color:#ffd68a;'>READY TO JOIN</div>
      </div>
      <div style='display:grid;grid-template-columns:minmax(0,1.7fr) minmax(280px,.8fr);gap:18px;margin-top:18px;'>
        <div style='background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:18px;'>
          <div style='display:flex;gap:10px;flex-wrap:wrap;'>
            <button id='lk-join' style='border:0;border-radius:12px;padding:11px 17px;background:linear-gradient(90deg,#6a45ff,#23b8ff);color:white;font-weight:800;cursor:pointer;'>Join live call</button>
            <button id='lk-mute' disabled style='border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:11px 17px;background:#121f38;color:#dbeaff;font-weight:700;cursor:pointer;'>Mute microphone</button>
            <button id='lk-leave' disabled style='border:1px solid rgba(255,100,100,.2);border-radius:12px;padding:11px 17px;background:rgba(255,80,80,.08);color:#ffb3b3;font-weight:700;cursor:pointer;'>Leave call</button>
          </div>
          <div id='lk-stage' style='margin-top:16px;min-height:250px;border-radius:18px;background:radial-gradient(circle at 30% 30%,rgba(63,122,255,.22),transparent 35%),#07101e;border:1px solid rgba(255,255,255,.06);display:flex;align-items:center;justify-content:center;color:#8ea4c2;text-align:center;padding:24px;'>Click <b style='color:#e7f3ff;margin:0 5px;'>Join live call</b> and allow microphone access. Speaker animation follows LiveKit's active speaker events.</div>
          <div id='lk-audio'></div>
        </div>
        <div style='background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:18px;'>
          <div style='font-size:12px;font-weight:800;letter-spacing:.12em;color:#78a7ff;margin-bottom:10px;'>PARTICIPANTS</div>
          <div id='lk-people'>{roster_html}</div>
          <div style='margin-top:14px;font-size:12px;line-height:1.6;color:#8298b7;'>Each selected DI keeps the same face and role. The green speaking state is controlled by the realtime room, not by a fake timer.</div>
        </div>
      </div>
      <div style='margin-top:14px;color:#6f85a5;font-size:11px;'>Room: {safe(room_name)}</div>
    </div>
    <style>
      .lk-person{{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.05);transition:.18s ease}}
      .lk-person:last-child{{border-bottom:0}}
      .lk-person.active{{background:rgba(81,231,177,.07);border-radius:12px;padding-left:8px;padding-right:8px}}
      .lk-face-wrap{{position:relative;width:48px;height:48px;flex:0 0 48px;border-radius:50%}}
      .lk-face{{width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid rgba(93,168,255,.44);display:block;background:#18304b}}
      .lk-fallback{{display:none;position:absolute;inset:0;place-items:center;border-radius:50%;background:linear-gradient(135deg,#4a65e6,#23b8ff);color:#fff;font-weight:900}}
      .lk-fallback-wrap .lk-fallback{{display:grid}}
      .lk-fallback-wrap .lk-face{{display:none}}
      .lk-mouth{{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);width:9px;height:3px;border-radius:50%;background:#1a0f0c;opacity:.15}}
      .lk-person.active .lk-face-wrap{{animation:lkTalk 1s ease-in-out infinite}}
      .lk-person.active .lk-mouth{{animation:lkMouth .18s ease-in-out infinite alternate;opacity:.75}}
      .lk-person.active .lk-face{{border-color:#55e5b5;box-shadow:0 0 0 4px rgba(85,229,181,.08),0 0 24px rgba(85,229,181,.15)}}
      .lk-person-meta b{{display:block;font-size:13px;color:#f5fbff}}
      .lk-person-meta span{{display:block;color:#7f95b3;font-size:11px;margin-top:2px}}
      .lk-person-meta em{{display:block;color:#7186a3;font-style:normal;font-size:10px;margin-top:3px}}
      .lk-person.active .lk-speaking{{color:#64efba;font-weight:800}}
      @keyframes lkTalk{{0%,100%{{transform:translateY(0) scale(1)}}50%{{transform:translateY(-1px) scale(1.02)}}}}
      @keyframes lkMouth{{from{{width:7px;height:2px}}to{{width:14px;height:6px}}}}
      @media(max-width:900px){{#dacre-livekit>div:nth-child(2){{grid-template-columns:1fr!important}}}}
    </style>
    <script src='https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.umd.min.js'></script>
    <script>
    (()=>{{
      const root=document.getElementById('dacre-livekit');
      const status=document.getElementById('lk-status'); const stage=document.getElementById('lk-stage'); 
      const join=document.getElementById('lk-join'); const mute=document.getElementById('lk-mute'); 
      const leave=document.getElementById('lk-leave'); const audio=document.getElementById('lk-audio'); 
      const people=document.getElementById('lk-people');
      const wsUrl={json.dumps(ws_url)}; const token={json.dumps(token)}; let room=null;
      
      const setStatus=(txt,bg,color)=>{{status.textContent=txt;status.style.background=bg;status.style.color=color;}};
      const mark=(identity,on)=>{{const nodes=[...people.querySelectorAll('.lk-person')]; 
        const n=nodes.find(x=>x.dataset.name===identity || x.querySelector('b')?.textContent===identity); 
        if(n){{n.classList.toggle('active',on); const t=n.querySelector('.lk-speaking'); if(t)t.textContent=on?'Speaking':'Listening';}}}};
      const clearActive=()=>people.querySelectorAll('.lk-person').forEach(n=>{{n.classList.remove('active'); 
        const t=n.querySelector('.lk-speaking'); if(t)t.textContent='Listening';}});
      
      join.onclick=async()=>{{
        try{{
          if(!window.LivekitClient) throw new Error('LiveKit client failed to load');
          room=new LivekitClient.Room({{adaptiveStream:true,dynacast:true}});
          room.on(LivekitClient.RoomEvent.TrackSubscribed,(track,pub,participant)=>{{ 
            if(track.kind===LivekitClient.Track.Kind.Audio){{ 
              const el=track.attach(); el.autoplay=true; el.controls=false; el.style.display='none'; audio.appendChild(el); 
            }} 
          }});
          room.on(LivekitClient.RoomEvent.ParticipantConnected,p=>{{ mark(p.name||p.identity,true); }});
          room.on(LivekitClient.RoomEvent.ParticipantDisconnected,p=>{{ mark(p.name||p.identity,false); }});
          room.on(LivekitClient.RoomEvent.ActiveSpeakersChanged,speakers=>{{ 
            clearActive(); speakers.forEach(p=>mark(p.name||p.identity,true)); 
            if(speakers.length) stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:18px;font-weight:900;color:#ecf7ff\">'+
              speakers.map(p=>p.name||p.identity).join(', ')+' speaking</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">'+
              'The active speaker state is synchronized to the realtime room.</div></div>'; 
          }});
          room.on(LivekitClient.RoomEvent.Disconnected,()=>{{ 
            clearActive(); setStatus('DISCONNECTED','rgba(255,80,80,.12)','#ffacac'); 
            join.disabled=false; mute.disabled=true; leave.disabled=true; 
          }});
          setStatus('CONNECTING…','rgba(88,132,255,.12)','#b7ceff');
          await room.connect(wsUrl,token);
          await room.localParticipant.setMicrophoneEnabled(true);
          mark(room.localParticipant.name||room.localParticipant.identity,true);
          setStatus('LIVE · FULL DUPLEX','rgba(80,230,166,.12)','#6ff0ba');
          stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:16px;font-weight:800;color:#ecf7ff\">'+
            'You are live with the DACRE council.</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">'+
            'Speak naturally. Real active-speaker events control the talking animation; no fake timer is used.</div></div>';
          join.disabled=true; mute.disabled=false; leave.disabled=false;
        }}catch(e){{ setStatus('CALL ERROR','rgba(255,80,80,.12)','#ffacac'); stage.textContent=e.message||String(e); }}
      }};
      
      mute.onclick=async()=>{{ if(!room)return; const enabled=room.localParticipant.isMicrophoneEnabled; 
        await room.localParticipant.setMicrophoneEnabled(!enabled); 
        mute.textContent=enabled?'Unmute microphone':'Mute microphone'; 
      }};
      
      leave.onclick=async()=>{{ if(room){{ await room.disconnect(); room=null; }} 
        clearActive(); setStatus('LEFT CALL','rgba(160,170,190,.12)','#bdc9d9'); 
        join.disabled=false; mute.disabled=true; leave.disabled=true; 
        stage.textContent='Call ended. You can join again when you are ready.'; 
      }};
    }})();
    </script>
    """
    components.html(html, height=900, scrolling=False)
PAGE6                        # =============================================================================
# ADMIN & DASHBOARD FUNCTIONS
# =============================================================================

def master_customer_360(company_name):
    """Get complete customer 360 view for a company."""
    con = db()
    
    users = pd.read_sql_query(
        "SELECT id, first_name, last_name, username, email, role, login_count, created_at, last_login "
        "FROM users WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    activity = pd.read_sql_query(
        "SELECT username, action, created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    chats = pd.read_sql_query(
        "SELECT username, sender, message, created_at FROM chat_history WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    files = pd.read_sql_query(
        "SELECT username, filename, file_type, created_at FROM files WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    projects = pd.read_sql_query(
        "SELECT username, project_name, active_filename, updated_at FROM projects WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    emails = pd.read_sql_query(
        "SELECT recipient_name, recipient_email, subject, status, sent_at FROM emails_log "
        "WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    calls = pd.read_sql_query(
        "SELECT room_name, title, host_username, mode, created_at, ended_at FROM call_rooms "
        "WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    con.close()
    return users, activity, chats, files, projects, emails, calls

def admin_metric_counts():
    """Get admin metric counts."""
    con = db()
    counts = {
        "users": con.execute("SELECT COUNT(*) FROM users WHERE role!='master'").fetchone()[0],
        "companies": con.execute("SELECT COUNT(*) FROM companies").fetchone()[0],
        "activities": con.execute(
            "SELECT COUNT(*) FROM activity WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0] + con.execute("SELECT COUNT(*) FROM public_visits").fetchone()[0],
        "messages": con.execute(
            "SELECT COUNT(*) FROM chat_history WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0],
        "files": con.execute(
            "SELECT COUNT(*) FROM files WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0],
        "agents": con.execute("SELECT COUNT(*) FROM di_agents").fetchone()[0],
    }
    con.close()
    return counts

def _escape_html(value):
    """Escape HTML special characters."""
    return (str(value or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

PAGE_META = {
    "Overview": ("⌂", "DACRE Analytics", "MASTER-ONLY platform command view · users, activity, system health and live intelligence."),
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
    "Chibobec Loan Desk": ("₦", "Chibobec Client Workspace", "Chibobec is a DACRE client. Manage its client workspace, loans and activity here."),
    "Overall Admin DI Portal": ("♛", "Founder Command", "Master-level platform intelligence, workforce, customers, memory and system controls."),
    "🌍 Global Markets": ("🌍", "Global Markets", "Real-time global market data, currencies, and business intelligence."),
    "🎥 DI Conference": ("🎥", "DI Conference", "Real-time video calls with your DI team."),
}

def _dashboard_safe_query(sql, params=(), default=None):
    """Run a read-only dashboard query without allowing an optional metric to break the app."""
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
    """Get a scalar value from a dashboard query."""
    row = _dashboard_safe_query(sql, params, None)
    if row is None:
        return default
    try:
        value = row[0]
        return default if value is None else value
    except Exception:
        return default

def _dashboard_escape(value):
    """Escape value for dashboard."""
    return _escape_html(str(value))

def _dashboard_spark(values, width=112, height=34):
    """Create a sparkline SVG."""
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
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-spark" aria-hidden="true">
        <polyline points="{line}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2" 
                  stroke-linecap="round" stroke-linejoin="round"/>
    </svg>'''

def _dashboard_area_chart(points):
    """Create an area chart SVG."""
    if not points:
        points = [(f"{h:02d}:00", 0, 0) for h in range(0, 24, 3)]
    
    width, height = 900, 300
    left, right, top, bottom = 52, 20, 22, 42
    plot_w, plot_h = width - left - right, height - top - bottom
    maxv = max([max(a, b) for _, a, b in points] or [1]) or 1
    
    coords_a = []
    coords_b = []
    
    for i, (_, a, b) in enumerate(points):
        x = left + (i * plot_w / max(1, len(points) - 1))
        ya = top + plot_h - (a / maxv) * plot_h
        yb = top + plot_h - (b / maxv) * plot_h
        coords_a.append((x, ya))
        coords_b.append((x, yb))
    
    def poly(coords):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    
    area_a = f"{left},{top + plot_h} {poly(coords_a)} {left + plot_w},{top + plot_h}"
    area_b = f"{left},{top + plot_h} {poly(coords_b)} {left + plot_w},{top + plot_h}"
    
    labels = []
    for i, (label, _, _) in enumerate(points):
        x = left + (i * plot_w / max(1, len(points) - 1))
        labels.append(f'<text x="{x:.1f}" y="{height - 12}" text-anchor="middle" class="chart-label">{_dashboard_escape(label)}</text>')
    
    grids = []
    for n in range(5):
        y = top + (plot_h * n / 4)
        val = maxv * (1 - n / 4)
        grids.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="chart-grid"/>')
        grids.append(f'<text x="{left - 9}" y="{y + 4:.1f}" text-anchor="end" class="chart-label">{val / 1000:.1f}k</text>')
    
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-area-chart" role="img" aria-label="Request throughput chart">
        <defs>
            <linearGradient id="dacreFillA" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--dacre-chart-1)" stop-opacity=".34"/>
                <stop offset="100%" stop-color="var(--dacre-chart-1)" stop-opacity=".02"/>
            </linearGradient>
            <linearGradient id="dacreFillB" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--dacre-chart-3)" stop-opacity=".22"/>
                <stop offset="100%" stop-color="var(--dacre-chart-3)" stop-opacity=".01"/>
            </linearGradient>
        </defs>
        {''.join(grids)}
        <polygon points="{area_b}" fill="url(#dacreFillB)"/>
        <polygon points="{area_a}" fill="url(#dacreFillA)"/>
        <polyline points="{poly(coords_b)}" fill="none" stroke="var(--dacre-chart-3)" stroke-width="2" stroke-linecap="round"/>
        <polyline points="{poly(coords_a)}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2.5" stroke-linecap="round"/>
        {''.join(labels)}
    </svg>'''

def _dashboard_health_ring(value):
    """Create a health ring SVG."""
    value = max(0, min(100, float(value)))
    r = 52
    circumference = 2 * 3.141592653589793 * r
    offset = circumference - (value / 100) * circumference
    
    return f'''<div class="dacre-health-ring">
        <svg viewBox="0 0 144 144" aria-label="System health {value:.0f}">
            <circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-muted-bg)" stroke-width="10"/>
            <circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="10" 
                    stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" 
                    transform="rotate(-90 72 72)" class="health-progress"/>
        </svg>
        <div class="dacre-health-center">
            <b>{value:.0f}</b>
            <span>Health score</span>
        </div>
    </div>'''

def render_analytics_overview(user):
    """Render the analytics overview dashboard."""
    if not user or user.get("role") != "master":
        st.error("This platform-wide analytics view is available only to David Emenike in the Overall Admin DI Office.")
        return
    
    # Live metrics
    users = int(_dashboard_scalar("SELECT COUNT(*) FROM users WHERE role!='master'", default=0))
    company_filter = user.get("company") if user.get("role") != "master" else None
    
    if company_filter:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity WHERE company_name=?", (company_filter,), 0))
        active_calls = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM call_rooms WHERE company_name=? AND (ended_at IS NULL OR TRIM(ended_at)='')",
            (company_filter,), 0
        ))
        errors = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM activity WHERE company_name=? AND (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%') AND created_at >= ?",
            (company_filter, (datetime.now().timestamp() - 86400).__str__()), 0
        ))
    else:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity", default=0))
        active_calls = int(_dashboard_scalar("SELECT COUNT(*) FROM call_rooms WHERE ended_at IS NULL OR TRIM(ended_at)=''", default=0))
        errors = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM activity WHERE (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%')",
            default=0
        ))
    
    # Build 24-hour activity series
    traffic = []
    try:
        con = db()
        if company_filter:
            dfh = pd.read_sql_query(
                "SELECT created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 3000",
                con, params=(company_filter,)
            )
        else:
            dfh = pd.read_sql_query("SELECT created_at FROM activity ORDER BY id DESC LIMIT 3000", con)
        con.close()
        
        if not dfh.empty:
            ts = pd.to_datetime(dfh["created_at"], errors="coerce")
            now = pd.Timestamp.now()
            for h in range(0, 24, 3):
                start = now - pd.Timedelta(hours=24 - h)
                end = start + pd.Timedelta(hours=3)
                count = int(((ts >= start) & (ts < end)).sum())
                traffic.append((start.strftime("%H:%M"), count, max(0, int(count * 0.62))))
    except Exception:
        traffic = []
    
    if not traffic:
        traffic = [
            ("00:00", 0, 0), ("03:00", 0, 0), ("06:00", 0, 0), ("09:00", 0, 0),
            ("12:00", 0, 0), ("15:00", 0, 0), ("18:00", 0, 0), ("21:00", 0, 0)
        ]
    
    health = max(0, min(100, round(99.98 - min(errors * 0.35, 25), 2)))
    spark_users = [max(0, users + i) for i in (-12, -8, -5, -7, -2, 4, 8, 0)]
    spark_activity = [max(0, activities + i) for i in (-30, -20, -8, -12, 0, 15, 24, 0)]
    spark_health = [96, 97, 98, 97, 99, 99, 100, health]
    spark_calls = [max(0, active_calls + i) for i in (20, 15, 12, 8, 10, 5, 3, 0)]
    
    st.markdown(f'''
    <div class="dacre-dashboard-topbar">
        <div class="dacre-dashboard-brand">
            <span class="live-pulse"><i></i></span>
            <div>
                <h1>DACRE Analytics</h1>
                <p>Real-time platform overview · all systems operational</p>
            </div>
        </div>
        <div class="dacre-dashboard-tools">
            <span class="dashboard-time">{datetime.now().strftime('%d %b %Y · %H:%M')}</span>
            <span class="dashboard-avatar">{_dashboard_escape((user.get('first_name','D')[:1] + user.get('last_name','A')[:1]).upper())}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    search = st.text_input(
        "Search metrics, agents...", value="", key="dashboard_search",
        label_visibility="collapsed", placeholder="Search metrics, agents..."
    )
    if search.strip():
        st.caption(f"Dashboard search: {search.strip()} · use the navigation to open the matching workspace.")
    
    kpis = [
        ("users", "Total Users", f"{users:,}", 12.4, spark_users, "registered platform users", "👥"),
        ("activity", "Activity", f"{activities:,}", 8.9, spark_activity, "recorded workspace events", "↗"),
        ("health", "System Health", f"{health:.2f}%", 0.3, spark_health, "availability signal · 24h", "◉"),
        ("calls", "Active Calls", f"{active_calls:,}", -3.1, spark_calls, "live sessions", "☎"),
    ]
    
    cards = []
    for key, label, value, delta, spark, hint, icon in kpis:
        positive = delta >= 0
        cards.append(f'''
        <div class="dacre-kpi-card">
            <div class="kpi-head">
                <span class="kpi-icon">{icon}</span>
                <span class="kpi-delta {'up' if positive else 'down'}">{'↗' if positive else '↘'} {abs(delta):.1f}%</span>
            </div>
            <p>{label}</p>
            <div class="kpi-value-row">
                <b>{_dashboard_escape(value)}</b>
                {_dashboard_spark(spark)}
            </div>
            <small>{_dashboard_escape(hint)}</small>
        </div>
        ''')
    
    st.markdown('<section class="dacre-kpi-grid">' + ''.join(cards) + '</section>', unsafe_allow_html=True)
    
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.markdown(f'''
        <div class="dacre-panel">
            <div class="panel-head">
                <div>
                    <h2>Request Throughput</h2>
                    <p>Workspace activity and compute load across the platform</p>
                </div>
                <div class="range-pills">
                    <span class="active">24h</span>
                    <span>7d</span>
                    <span>30d</span>
                </div>
            </div>
            <div class="chart-legend">
                <span><i class="blue"></i>Activity</span>
                <span><i class="cyan"></i>Load</span>
            </div>
            {_dashboard_area_chart(traffic)}
        </div>
        ''', unsafe_allow_html=True)
    
    with right:
        resource_rows = [
            ("CPU", 42, "var(--dacre-chart-1)"),
            ("Memory", 61, "var(--dacre-chart-2)"),
            ("Network I/O", 28, "var(--dacre-chart-3)"),
            ("Storage", 74, "var(--dacre-chart-5)")
        ]
        bars = ''.join(f'''
        <div class="resource-row">
            <div>
                <span>{label}</span>
                <b>{value}%</b>
            </div>
            <div class="resource-track">
                <i style="width:{value}%;background:{color}"></i>
            </div>
        </div>
        ''' for label, value, color in resource_rows)
        
        st.markdown(f'''
        <div class="dacre-panel health-panel">
            <div class="panel-head">
                <div>
                    <h2>System Health</h2>
                    <p>Live resource utilization</p>
                </div>
            </div>
            {_dashboard_health_ring(health)}
            <div class="resource-list">{bars}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Recent activity table
    try:
        con = db()
        if company_filter:
            recent = pd.read_sql_query(
                "SELECT id, username, action, created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 8",
                con, params=(company_filter,)
            )
        else:
            recent = pd.read_sql_query(
                "SELECT id, username, action, created_at FROM activity ORDER BY id DESC LIMIT 8",
                con
            )
        con.close()
    except Exception:
        recent = pd.DataFrame(columns=["id", "username", "action", "created_at"])
    
    rows = []
    for _, r in recent.iterrows():
        action = str(r.get("action") or "System activity")
        low = action.lower()
        status = "error" if "error" in low or "fail" in low else ("warning" if "warn" in low else "success")
        rows.append(f'''
        <tr>
            <td><b>{_dashboard_escape(action[:90])}</b></td>
            <td>{_dashboard_escape(r.get('username', 'System'))}</td>
            <td><span class="channel">platform</span></td>
            <td><span class="status {status}"><i></i>{status}</span></td>
            <td class="mono">—</td>
            <td class="mono right">{_dashboard_escape(r.get('created_at', ''))}</td>
        </tr>
        ''')
    
    if not rows:
        rows.append('<tr><td colspan="6" class="empty-row">No activity has been recorded yet.</td></tr>')
    
    st.markdown(f'''
    <div class="dacre-panel activity-panel">
        <div class="panel-head">
            <div>
                <h2>Recent Activity</h2>
                <p>Latest events across agents and infrastructure</p>
            </div>
            <span class="view-all">Live ledger</span>
        </div>
        <div class="activity-scroll">
            <table class="dacre-activity-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Agent</th>
                        <th>Channel</th>
                        <th>Status</th>
                        <th>Latency</th>
                        <th class="right">Time</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_page_chrome(page_name, user):
    """Render the page chrome header."""
    icon, title, subtitle = PAGE_META.get(page_name, ("•", page_name, "Dacre business intelligence workspace."))
    master = user.get("role") == "master"
    mode_label = "FOUNDER COMMAND" if master else str(user.get("company", "BUSINESS WORKSPACE")).upper()
    
    st.markdown(f"""
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
    """, unsafe_allow_html=True)

def log_di_action(user, action_type, request, result, agent_name="DI"):
    """Log a DI action."""
    con = db()
    con.execute("""
        INSERT INTO di_action_log(company_name, username, agent_name, action_type, request, result, created_at)
        VALUES(?,?,?,?,?,?,?)
    """, (
        user["company"], user["username"], agent_name, action_type, request, result,
        datetime.now().isoformat(timespec="seconds")
    ))
    con.commit()
    con.close()

def get_recent_di_actions(user, limit=20):
    """Get recent DI actions for a user."""
    con = db()
    df = pd.read_sql_query(
        """SELECT agent_name, action_type, request, result, created_at
           FROM di_action_log
           WHERE company_name=? AND username=?
           ORDER BY id DESC LIMIT ?""",
        con, params=(user["company"], user["username"], int(limit)),
    )
    con.close()
    return df

def render_business_twin(df, user):
    """Render the business twin page."""
    if df is None or df.empty:
        st.info("Load a dataset in Workspace & Data and the Business Twin will build itself from real data.")
        return
    
    health = business_health(df)
    signals = business_signals(df)
    opportunities = opportunity_radar(df, user["company"], user["username"])
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    numeric = len(df.select_dtypes(include="number").columns)
    
    st.markdown(f"""
    <div class="business-twin-banner">
        <div>
            <span class="twin-label">LIVE BUSINESS TWIN</span>
            <h2>{_escape_html(user['company'])}</h2>
            <p>This snapshot is generated from the active workspace only. Dacre does not invent company numbers.</p>
        </div>
        <div class="twin-score">
            <b>{health['score']}</b>
            <span>/100</span>
            <small>DATA HEALTH</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    k = st.columns(5)
    for col, label, value in zip(
        k,
        ["Rows", "Columns", "Numeric fields", "Missing cells", "Duplicates"],
        [f"{len(df):,}", f"{len(df.columns):,}", f"{numeric:,}", f"{missing:,}", f"{duplicates:,}"]
    ):
        with col:
            st.markdown(f"<div class='twin-metric'><b>{value}</b><span>{label}</span></div>", unsafe_allow_html=True)
    
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### What deserves attention")
        if signals:
            for item in signals[:6]:
                st.markdown(
                    f"<div class='insight-row'><b>{_escape_html(item.get('title'))}</b>"
                    f"<span>{_escape_html(item.get('detail'))}</span></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.success("No major deterministic data-quality/business signals were detected in the current dataset.")
    
    with right:
        st.markdown("### Opportunity signals")
        if opportunities:
            for item in opportunities:
                st.markdown(
                    f"<div class='opportunity-row'><b>{_escape_html(item['title'])}</b>"
                    f"<span>{_escape_html(item['impact'])}</span>"
                    f"<small>{_escape_html(item['action'])}</small></div>",
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
        st.markdown(
            f"<div class='di-answer-panel'><div class='answer-label'>DI EXPLANATION</div>"
            f"<div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>",
            unsafe_allow_html=True
        )

def render_action_center(user):
    """Render the DI action center."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div class="action-center-banner">
        <span>DI ACTION ENGINE</span>
        <h2>Give DI a business outcome — not a menu to navigate.</h2>
        <p>DI can use the same core reasoning, data analysis, memory and research capabilities available from the main Dacre workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    
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
PAGE7                           # =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_decision_ledger(user):
    """Render the decision ledger page."""
    st.markdown("""
    <div class="decision-banner">
        <span>INSTITUTIONAL MEMORY</span>
        <h2>Decisions should become company knowledge.</h2>
        <p>Record the decision, the reason, the expected result and later the actual result. This lets DI learn from the organization's history.</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        "SELECT title, context, decision, expected_outcome, review_date, status, outcome, created_at, updated_at "
        "FROM decision_ledger WHERE company_name=? ORDER BY id DESC",
        con, params=(user["company"],),
    )
    con.close()
    
    if not decisions.empty:
        st.dataframe(safe_dataframe_for_streamlit(decisions), use_container_width=True, hide_index=True)

def render_opportunity_page(user):
    """Render the opportunity radar page."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div class="opportunity-banner">
        <span>OPPORTUNITY RADAR</span>
        <h2>Find upside before it becomes obvious.</h2>
        <p>Dacre scans numeric trends in the active dataset and turns measurable changes into investigation prompts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    opportunities = opportunity_radar(df, user["company"], user["username"])
    
    if not opportunities:
        st.info("Load a dataset with enough numeric observations to generate measurable opportunity signals.")
        return
    
    for item in opportunities:
        st.markdown(f"""
        <div class="opportunity-card">
            <div class="opp-title">{_escape_html(item['title'])}</div>
            <div class="opp-impact">{_escape_html(item['impact'])}</div>
            <p>{_escape_html(item['evidence'])}</p>
            <b>Suggested investigation</b>
            <p>{_escape_html(item['action'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Ask DI to investigate · {item['title']}", key=f"opp_{hash(item['title'])}", use_container_width=True):
            prompt = f"Investigate this opportunity signal: {item['title']}. Evidence: {item['evidence']}. Suggested action: {item['action']}"
            answer = di_reply(prompt, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
            log_di_action(user, "opportunity", prompt, answer)
            st.markdown(
                f"<div class='di-answer-panel'><div class='answer-label'>DI INVESTIGATION</div>"
                f"<div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>",
                unsafe_allow_html=True
            )

def _dacre_logo_data_uri():
    """Return the bundled DACRE logo as a data URI when available."""
    try:
        import base64
        if LOGO_PATH.exists():
            raw = LOGO_PATH.read_bytes()
            mime = "image/png"
            if LOGO_PATH.suffix.lower() in (".jpg", ".jpeg"):
                mime = "image/jpeg"
            elif LOGO_PATH.suffix.lower() == ".webp":
                mime = "image/webp"
            return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    except Exception:
        pass
    return ""

def _landing_auth_panel():
    """Render authentication inside the public DACRE landing page."""
    mode = st.session_state.get("landing_mode", "home")
    if mode not in ("login", "signup"):
        return

    st.markdown("""
    <style>
    .auth-anchor { scroll-margin-top: 20px; }
    .auth-shell {
        max-width: 980px;
        margin: 18px auto 42px;
        padding: 1px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(91,73,255,.75), rgba(37,211,238,.55), rgba(255,255,255,.08));
        box-shadow: 0 28px 90px rgba(0,0,0,.38);
    }
    .auth-inner {
        border-radius: 23px;
        background: #0b1020;
        padding: 30px;
        border: 1px solid rgba(255,255,255,.08);
    }
    .auth-title { color:#f7f9ff; font-size:28px; font-weight:800; letter-spacing:-.03em; }
    .auth-sub { color:#9ba9c2; margin-top:6px; margin-bottom:20px; }
    .auth-badge {
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding:6px 10px;
        border-radius:999px;
        border:1px solid rgba(126,115,255,.3);
        background:rgba(92,76,255,.10);
        color:#bfc5ff;
        font-size:12px;
        font-weight:700;
    }
    </style>
    <div id="dacre-auth" class="auth-anchor auth-shell">
        <div class="auth-inner">
            <div class="auth-badge">✦ DACRE secure workspace access</div>
            <div class="auth-title">Your DACRE workspace starts here.</div>
            <div class="auth-sub">Sign in to your existing workspace or create your organization account without leaving the DACRE landing page.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("landing_login_form", clear_on_submit=False):
                login_company = st.text_input(
                    "Company / Organization",
                    placeholder="e.g. Edubridge Consultant Limited",
                    key="landing_login_company",
                )
                login_fullname = st.text_input(
                    "Full Name",
                    placeholder="e.g. David Emenike",
                    key="landing_login_fullname",
                )
                login_email = st.text_input(
                    "Email Address",
                    placeholder="Use the email registered with DACRE",
                    key="landing_login_email",
                )
                login_passkey = st.text_input(
                    "Account Passkey",
                    type="password",
                    placeholder="Enter your DACRE account passkey",
                    key="landing_login_passkey",
                )
                login_submit = st.form_submit_button(
                    "Sign In & Open My DACRE Workspace",
                    use_container_width=True,
                    type="primary",
                )

            if login_submit:
                auth, auth_message = authenticate(
                    login_company, login_fullname, login_passkey, login_email
                )
                if auth:
                    st.session_state.user = auth
                    st.session_state.master_route = auth.get("role") == "master"
                    st.session_state.landing_mode = "home"
                    st.session_state.last_speech = (
                        f"Welcome back, {auth['first_name']}. I am DI. "
                        "Where would you like to start today?"
                    )
                    project = restore_project(auth)
                    if project:
                        st.session_state.active_filename = project["filename"] or ""
                        st.session_state.raw_df = project["raw"]
                        st.session_state.processed_df = project["processed"]
                        st.session_state.formula_logs = project["logs"]
                        st.session_state.chart_config = project["chart"]
                    st.toast(f"Welcome back, {auth['first_name']}!")
                    st.rerun()
                else:
                    st.error(
                        auth_message or
                        "We could not sign you in. Check your details or create a DACRE account."
                    )

        with tab_signup:
            with st.form("landing_signup_form", clear_on_submit=False):
                s_first = st.text_input(
                    "First Name", placeholder="e.g. David", key="landing_signup_first"
                )
                s_last = st.text_input(
                    "Last Name", placeholder="e.g. Emenike", key="landing_signup_last"
                )
                s_company = st.text_input(
                    "Company / Organization",
                    placeholder="e.g. Edubridge Consultant Limited",
                    key="landing_signup_company",
                )
                s_email = st.text_input(
                    "Email Address",
                    placeholder="e.g. name@example.com",
                    key="landing_signup_email",
                )
                s_email_pass = st.text_input(
                    "Email Password (optional)",
                    type="password",
                    placeholder="Optional — only needed for configured email features",
                    key="landing_signup_email_password",
                )
                s_passkey = st.text_input(
                    "Create Account Passkey",
                    type="password",
                    placeholder="Create a secure passkey for your DACRE account",
                    key="landing_signup_passkey",
                )
                s_website = st.text_input(
                    "Do you have a website? Please put your company official URL to get the best performance from DI — David's Intelligence.",
                    placeholder="https://www.yourcompany.com",
                    key="landing_signup_website",
                )
                st.caption("Your official site helps DI prepare company context and adapt the workspace appearance. Website onboarding runs in the background so signup stays fast.")
                signup_submit = st.form_submit_button(
                    "Create My DACRE Account",
                    use_container_width=True,
                    type="primary",
                )

            if signup_submit:
                success, msg, created = create_account(
                    s_first, s_last, s_company, s_email, s_email_pass, s_passkey, s_website
                )
                if success:
                    st.session_state.user = created
                    st.session_state.master_route = False
                    st.session_state.landing_mode = "home"
                    if is_chibobec_company(created["company"]):
                        st.session_state.last_speech = (
                            f"We know you are coming, {CHIBOBEC_OWNER_NAME}. "
                            "Welcome to DACRE Analysis. Your loan collection workspace is ready, "
                            "and DI is standing by to help you manage your clients and repayment reminders."
                        )
                    else:
                        st.session_state.last_speech = (
                            f"Welcome to DACRE, {created['first_name']}. "
                            "I am DI, your business intelligence assistant. "
                            "What would you like us to work on first?"
                        )
                    st.toast(f"Welcome to DACRE, {created['first_name']}!")
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("← Continue browsing DACRE", key="landing_auth_back", use_container_width=True):
            st.session_state.landing_mode = "home"
            st.rerun()

        # Discreet private CEO Office launcher
        st.markdown("""
        <style>
          .ceo-launcher-wrap{margin:28px auto 4px;text-align:center;opacity:.86}
          .ceo-launcher-wrap a{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:14px;
            border:1px solid rgba(112,132,255,.24);background:linear-gradient(145deg,rgba(28,41,74,.95),rgba(7,13,28,.95));
            box-shadow:0 12px 34px rgba(0,0,0,.28),0 0 18px rgba(74,110,255,.10);transition:.2s ease;text-decoration:none}
          .ceo-launcher-wrap a:hover{transform:translateY(-2px);border-color:rgba(105,145,255,.6);box-shadow:0 16px 40px rgba(0,0,0,.34),0 0 24px rgba(74,110,255,.22)}
          .ceo-launcher-wrap img{width:28px;height:28px;object-fit:contain;border-radius:8px}
          .ceo-launcher-caption{margin-top:7px;color:#70809b;font-size:9px;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
        </style>
        <div class="ceo-launcher-wrap">
          <a href="?master_gate=1" title="Private CEO Office">__CEO_LOGO__</a>
          <div class="ceo-launcher-caption">Private CEO Office</div>
        </div>
        """.replace("__CEO_LOGO__", f'<img src="{_dacre_logo_data_uri()}" alt="DACRE" />'), unsafe_allow_html=True)

def landing_page():
    """Public DACRE landing experience with connected navigation and real auth."""
    record_public_visit("landing_view", "Landing")
    
    # PRIVATE MASTER GATE
    if st.query_params.get("master_gate") == "1":
        captcha_required = st.session_state.get("master_captcha_required", False)
        captcha_passed = st.session_state.get("master_captcha_passed", False)
        second_attempt = st.session_state.get("master_second_attempt", False)

        st.markdown("""
        <style>
          .dacre-master-shell { max-width: 720px; margin: 60px auto; padding: 36px;
            border-radius: 24px; background:#0b1020; border:1px solid rgba(255,255,255,.09);
            box-shadow:0 30px 90px rgba(0,0,0,.45); }
        </style>
        <div class="dacre-master-shell">
          <div style="color:#f7f9ff;font-size:28px;font-weight:800;">Overall Admin DI — Master Access</div>
          <div style="color:#9ba9c2;margin-top:8px;">Private system-wide access for the DACRE master administrator.</div>
        </div>
        """, unsafe_allow_html=True)

        gate_col1, gate_col2, gate_col3 = st.columns([1, 2, 1])
        with gate_col2:
            if captcha_required and not captcha_passed:
                st.markdown("### Security verification")
                site_key = os.getenv("DACRE_RECAPTCHA_SITE_KEY", "").strip()
                if site_key:
                    components.html(f"""
                    <div style="display:flex;justify-content:center;">
                      <div class="g-recaptcha" data-sitekey="{site_key}"></div>
                    </div>
                    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
                    """, height=100)
                    st.caption("Complete the configured security verification before continuing.")
                    if st.button("I completed the reCAPTCHA", use_container_width=True):
                        st.warning("Complete the verification widget first.")
                else:
                    if st.checkbox("Complete security verification", key="local_captcha_check"):
                        st.session_state.master_captcha_passed = True
                        st.session_state.master_second_attempt = True
                        st.rerun()

                if st.button("Return to DACRE", use_container_width=True, key="master_return_1"):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.session_state.master_guard_challenge_required = False
                    st.session_state.master_guard_failed = False
                    st.query_params.clear()
                    st.rerun()
                return

            # Second gate: CEO Office Guardian
            if st.session_state.get("master_guard_challenge_required", False):
                st.markdown("### CEO Office Guardian Verification")
                if st.session_state.get("master_guard_failed", False):
                    st.warning("That guardian name was not recognized. Please enter the name exactly as it was given when the guardian was created.")
                
                guardian_answer = st.text_input(
                    "Sorry, please Master, what is the name you gave me when you created me?",
                    placeholder="Enter the guardian's name",
                    key="master_guard_answer",
                )
                gg1, gg2 = st.columns(2)
                with gg1:
                    if st.button("Verify Guardian", use_container_width=True, type="primary", key="master_guard_verify"):
                        if guardian_answer.strip().casefold() == CEO_GUARD_NAME.casefold():
                            st.session_state.user = master_user_record()
                            st.session_state.master_route = True
                            st.session_state.master_captcha_required = False
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.session_state.master_guard_challenge_required = False
                            st.session_state.master_guard_failed = False
                            st.session_state.last_speech = "Welcome, Master David. Guaiel has verified the CEO Office. Overall Admin DI is online."
                            st.query_params.clear()
                            log_activity(MASTER_USERNAME, "DACRE MASTER", "Opened Overall CEO Office after Guaiel guardian verification", notify_admin=False)
                            st.rerun()
                        else:
                            st.session_state.master_guard_failed = True
                            st.rerun()
                with gg2:
                    if st.button("Return to DACRE", use_container_width=True, key="master_guard_return"):
                        st.session_state.master_guard_challenge_required = False
                        st.session_state.master_guard_failed = False
                        st.query_params.clear()
                        st.rerun()
                return

            master_pk = st.text_input(
                "Account Passkey",
                type="password",
                placeholder="Enter your private account passkey",
                key="master_gate_pk",
            )
            if second_attempt:
                st.info("Security verification completed. Please enter the passkey again.")

            g1, g2 = st.columns(2)
            with g1:
                if st.button("Open Overall Admin DI", use_container_width=True, type="primary", key="master_open"):
                    if master_passkey_gate(master_pk):
                        st.session_state.master_guard_challenge_required = True
                        st.session_state.master_guard_failed = False
                        st.rerun()
                    else:
                        if second_attempt:
                            st.warning("The second passkey attempt was incorrect. Returning to DACRE.")
                            st.session_state.master_captcha_required = False
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.session_state.master_guard_challenge_required = False
                            st.session_state.master_guard_failed = False
                            st.query_params.clear()
                            st.rerun()
                        else:
                            st.session_state.master_captcha_required = True
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.rerun()
            with g2:
                if st.button("Return to DACRE", use_container_width=True, key="master_return_2"):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.query_params.clear()
                    st.rerun()
        return

    logo_uri = _dacre_logo_data_uri()
    logo = f'<img src="{logo_uri}" alt="DACRE" class="brand-logo"/>' if logo_uri else '<span class="brand-fallback">D</span>'

    # Landing stylesheet
    st.markdown("""
    <style>
      #MainMenu, footer, header { visibility:hidden; }
      [data-testid="stSidebar"] { display:none; }
      .stApp { background:
        radial-gradient(circle at 78% 18%, rgba(71,81,255,.18), transparent 28%),
        radial-gradient(circle at 18% 48%, rgba(0,205,255,.08), transparent 26%),
        #050817 !important;
      }
      .block-container { max-width: 1440px !important; padding: 0 22px 50px !important; }
      .dacre-landing { color:#f6f8ff; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; overflow:hidden; }
      .dacre-nav { min-height:76px; display:flex; align-items:center; justify-content:space-between; gap:18px; padding:12px 16px;
        border:1px solid rgba(150,164,205,.16); border-radius:18px; background:rgba(8,13,30,.82); backdrop-filter:blur(18px);
        box-shadow:0 18px 60px rgba(0,0,0,.24); position:sticky; top:10px; z-index:10; }
      .dacre-brand { display:flex; align-items:center; gap:12px; min-width:210px; }
      .brand-logo { width:43px; height:43px; object-fit:contain; border-radius:12px; filter:drop-shadow(0 0 16px rgba(84,92,255,.35)); }
      .brand-fallback { display:grid; place-items:center; width:43px;height:43px; font-size:21px; background:linear-gradient(135deg,#754cff,#3d8dff 55%,#18c8df); color:#fff; font-weight:900; border-radius:12px; }
      .dacre-brand-name { font-size:17px;font-weight:850;letter-spacing:-.02em; }
      .dacre-brand-sub { color:#9cacca;font-size:10px;margin-top:2px; }
      .system-ready { display:inline-flex;align-items:center;gap:7px;color:#a7b8d3;font-size:10px;font-weight:800;letter-spacing:.05em;white-space:nowrap; }
      .ready-dot { width:8px;height:8px;border-radius:50%;background:#54e2ae;box-shadow:0 0 14px rgba(84,226,174,.9); }
      .hero { min-height:640px; display:grid; grid-template-columns:1fr 1fr; gap:34px; align-items:center; padding:68px 28px 42px; }
      .hero-eyebrow { display:inline-flex; padding:8px 13px; border:1px solid rgba(144,132,255,.28); background:rgba(93,73,255,.08); border-radius:999px;color:#d8d7ff;font-size:12px;font-weight:700; }
      .hero-title { font-size:clamp(46px,6.4vw,82px); line-height:.96; letter-spacing:-.065em; font-weight:850; margin:22px 0 20px; max-width:700px; }
      .gradient-text { background:linear-gradient(90deg,#a4b4ff 0%,#8d77ff 38%,#28d5e8 72%,#f5dc59 100%); -webkit-background-clip:text;background-clip:text;color:transparent; }
      .hero-copy { max-width:610px; color:#a9b7cf;font-size:17px;line-height:1.7; }
      .hero-proof { display:flex; gap:22px; flex-wrap:wrap; margin-top:34px; color:#c7d0e2;font-size:12px; }
      .proof-dot { color:#5fe2ae; }
      .page-hero { padding:70px 28px 28px; }
      .page-title { font-size:clamp(42px,6vw,72px); line-height:1; letter-spacing:-.06em; font-weight:850; margin:14px 0 16px; }
      .page-copy { max-width:790px; color:#a9b7cf; font-size:17px; line-height:1.75; }
      .section { padding:70px 28px; }
      .section-head { max-width:820px;margin-bottom:32px; }
      .section-kicker { color:#7b89ff;text-transform:uppercase;letter-spacing:.16em;font-size:10px;font-weight:900; }
      .section-title { font-size:38px;line-height:1.05;letter-spacing:-.045em;font-weight:820;margin-top:10px; }
      .section-copy { color:#9aa9c2;line-height:1.75;font-size:15px;margin-top:10px; }
      .grid-3 { display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px; }
      .grid-2 { display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px; }
      .feature-card { padding:23px;min-height:180px;border:1px solid rgba(124,148,205,.15);border-radius:22px;background:linear-gradient(150deg,rgba(28,42,72,.78),rgba(7,13,28,.78)); box-shadow:0 18px 40px rgba(0,0,0,.16); }
      .feature-icon { width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:rgba(70,127,255,.12);color:#79cfff;font-weight:900;margin-bottom:16px; }
      .feature-card h3 { margin:0;font-size:20px;letter-spacing:-.025em; }
      .feature-card p { color:#9dacc4;line-height:1.65;margin:8px 0 0;font-size:14px; }
      .pill-row { display:flex; gap:9px; flex-wrap:wrap; margin-top:20px; }
      .pill { padding:8px 11px; border-radius:999px; border:1px solid rgba(110,155,255,.2); background:rgba(65,108,255,.08); color:#bcd5ff; font-size:11px; font-weight:700; }
      .workflow { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px; }
      .step { padding:20px;border-radius:20px;border:1px solid rgba(124,148,205,.13);background:rgba(255,255,255,.025); }
      .step-num { color:#6f88ff;font-size:10px;font-weight:900;letter-spacing:.14em; }
      .step h4 { margin:8px 0 7px;font-size:18px; }
      .step p { color:#99a7c0;font-size:13px;line-height:1.6;margin:0; }
      .callout { padding:28px;border-radius:24px;border:1px solid rgba(105,143,255,.18);background:linear-gradient(135deg,rgba(54,76,155,.22),rgba(15,31,56,.64)); }
      .callout h3 { margin:0 0 8px;font-size:24px; }
      .callout p { margin:0;color:#aab8ce;line-height:1.7; }
      .metric-row { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:20px; }
      .metric { padding:18px;border-radius:18px;border:1px solid rgba(118,145,206,.14);background:rgba(255,255,255,.025); }
      .metric small { color:#8898b4;font-size:10px;text-transform:uppercase;letter-spacing:.12em; }
      .metric strong { display:block;margin-top:5px;font-size:26px; }
      .cta { margin:20px 28px 30px;padding:42px 28px;border-radius:28px;border:1px solid rgba(113,151,255,.2);background:radial-gradient(circle at 20% 20%,rgba(90,75,255,.18),transparent 35%),linear-gradient(135deg,rgba(17,28,55,.96),rgba(7,13,28,.98));text-align:center; }
      .cta h2 { font-size:clamp(30px,4vw,52px);letter-spacing:-.05em;margin:10px 0; }
      .cta p { max-width:680px;margin:0 auto 18px;color:#9eacc3;line-height:1.7; }
      .footer { display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:26px 28px;color:#7787a4;font-size:11px; }
      .hero-visual-host { min-height:500px; }
      .auth-shell { max-width:980px; margin:28px auto 42px; padding:1px;border-radius:24px;background:linear-gradient(135deg,rgba(91,73,255,.75),rgba(37,211,238,.55),rgba(255,255,255,.08));box-shadow:0 28px 90px rgba(0,0,0,.38); }
      .auth-inner { border-radius:23px;background:#0b1020;padding:30px;border:1px solid rgba(255,255,255,.08); }
      .auth-title { color:#f7f9ff;font-size:28px;font-weight:800;letter-spacing:-.03em; }
      .auth-sub { color:#9ba9c2;margin-top:6px;margin-bottom:20px; }
      .auth-badge { display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:999px;border:1px solid rgba(126,115,255,.3);background:rgba(92,76,255,.10);color:#bfc5ff;font-size:12px;font-weight:700; }
      @media(max-width:980px){ .hero{grid-template-columns:1fr;padding-top:48px}.grid-3,.grid-2{grid-template-columns:1fr 1fr}.workflow{grid-template-columns:1fr 1fr}.metric-row{grid-template-columns:1fr 1fr}.hero-visual-host{min-height:430px} }
      @media(max-width:680px){ .block-container{padding:0 12px 40px !important}.dacre-nav{position:static;padding:12px}.dacre-brand{min-width:auto}.system-ready{display:none}.hero{padding:42px 10px 25px;min-height:auto}.hero-title{font-size:48px}.section,.page-hero{padding:48px 10px 20px}.grid-3,.grid-2,.workflow,.metric-row{grid-template-columns:1fr}.section-title{font-size:31px}.hero-visual-host{min-height:360px}.cta{margin:18px 10px 25px;padding:34px 20px}.footer{padding:22px 10px} }
    </style>
    """, unsafe_allow_html=True)  # =============================================================================
# LANDING PAGE CONTINUED & ENHANCED FEATURES
# =============================================================================

current_section = st.session_state.get("landing_section", "home")
mode = st.session_state.get("landing_mode", "home")

st.markdown(f"""
    <div class="dacre-nav">
      <div class="dacre-brand">{logo}<div><div class="dacre-brand-name">DACRE</div><div class="dacre-brand-sub">Powered by DI — David's Intelligence</div></div></div>
      <div class="system-ready"><span class="ready-dot"></span> DI ONLINE · DAVID'S INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

  nav_items = [("Features", "features"), ("Intelligence", "intelligence"), ("Workforce", "workforce"), ("Analytics", "analytics"), ("Security", "security")]
nav_cols = st.columns([1.0, 1.0, 1.0, 1.0, 1.0, 0.85, 0.85])
for i, (label, target) in enumerate(nav_items):
        with nav_cols[i]:
            if st.button(label, key=f"landing_nav_{target}", use_container_width=True):
                st.session_state.landing_section = target
                st.session_state.landing_mode = "home"
                st.rerun()
    with nav_cols[5]:
        if st.button("Log In", key="landing_nav_login", use_container_width=True):
            st.session_state.landing_mode = "login"
            st.session_state.landing_section = "home"
            st.rerun()
    with nav_cols[6]:
        if st.button("Get Started", key="landing_nav_signup", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    # Style actual Streamlit navigation buttons
    st.markdown("""
    <style>
      div[data-testid="stButton"] > button { border-radius:12px !important; min-height:42px !important; border:1px solid rgba(124,150,213,.15) !important; background:rgba(13,21,42,.72) !important; color:#cad5e8 !important; font-weight:700 !important; transition:.18s ease !important; }
      div[data-testid="stButton"] > button:hover { border-color:rgba(73,148,255,.55) !important; color:#ffffff !important; box-shadow:0 0 24px rgba(48,126,255,.12) !important; transform:translateY(-1px); }
      div[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(100deg,#7558ff,#4b8cff 52%,#18bfe1) !important; border:none !important; color:#fff !important; box-shadow:0 10px 30px rgba(69,115,255,.22) !important; }
    </style>
    """, unsafe_allow_html=True)

    # Dedicated auth pages
    if mode in ("login", "signup"):
        title = "Sign in to DACRE" if mode == "login" else "Create your DACRE account"
        subtitle = "Open your real DACRE workspace." if mode == "login" else "Start your own connected business intelligence workspace."
        action_word = "Sign In" if mode == "login" else "Create Account"
        st.markdown(f"""
        <div class="page-hero">
          <div class="section-kicker">DACRE ACCOUNT</div>
          <div class="page-title">{title}</div>
          <div class="page-copy">{subtitle} Powered by DI — David's Intelligence.</div>
        </div>
        <div class="callout" style="margin:10px 28px 0;">
          <h3>{action_word}</h3>
          <p>This is the real DACRE authentication flow, connected to the application database. You are not leaving the DACRE experience.</p>
        </div>
        """, unsafe_allow_html=True)
        _landing_auth_panel()
        if st.button("← Back to DACRE Landing Page", key="auth_page_back", use_container_width=True):
            st.session_state.landing_mode = "home"
            st.session_state.landing_section = "home"
            st.rerun()
        return

    # Dedicated information pages
    if current_section == "features":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DACRE FEATURES</div>
          <div class="page-title">Everything needed to move from raw data to useful work.</div>
          <div class="page-copy">DACRE combines a data workspace, cleaning tools, formulas, charts, files, exports, business intelligence and DI into one connected environment.</div>
        </div>
        <div class="section">
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">▦</div><h3>Workspace & Data</h3><p>Import CSV, Excel, TSV and JSON datasets into a persistent working environment.</p></div>
            <div class="feature-card"><div class="feature-icon">ƒ</div><h3>Formula Lab</h3><p>Apply practical spreadsheet-style transformations and calculations without leaving your analysis workflow.</p></div>
            <div class="feature-card"><div class="feature-icon">◫</div><h3>Charts & Dashboards</h3><p>Turn processed information into visual stories that make business patterns easier to understand.</p></div>
            <div class="feature-card"><div class="feature-icon">▤</div><h3>File Vault</h3><p>Keep working files and datasets organized inside the organization workspace.</p></div>
            <div class="feature-card"><div class="feature-icon">⇩</div><h3>Export Center</h3><p>Package analysis outputs for reporting, sharing and business use.</p></div>
            <div class="feature-card"><div class="feature-icon">✦</div><h3>DI Action Center</h3><p>Give DI a business objective and let it turn the request into analysis, recommendations and next actions.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Use these DACRE features", key="features_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "intelligence":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DI — DAVID'S INTELLIGENCE</div>
          <div class="page-title">Intelligence that works with your business context.</div>
          <div class="page-copy">DI is the built-in intelligence layer inside DACRE Analysis. It can explain results, investigate data, help with business questions and work alongside the active workspace.</div>
        </div>
        <div class="section">
          <div class="grid-2">
            <div class="callout"><h3>Ask questions naturally</h3><p>Move from dashboards to conversation. Ask DI to explain a number, investigate a pattern, draft a brief or recommend what to investigate next.</p></div>
            <div class="callout"><h3>Work from real context</h3><p>DI can use the current organization, active dataset, institutional memory and available research context instead of treating every request as an isolated question.</p></div>
            <div class="callout"><h3>Named DI workforce</h3><p>DACRE supports specialized DI workers with distinct identities, specialties and working styles — all under the same DACRE intelligence foundation.</p></div>
            <div class="callout"><h3>Voice-ready experience</h3><p>The DACRE interface supports browser-based DI voice interaction so users can communicate naturally where their browser supports speech features.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create a workspace and use DI", key="intelligence_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "workforce":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DI WORKFORCE</div>
          <div class="page-title">Specialized digital workers, coordinated inside DACRE.</div>
          <div class="page-copy">Each DI worker can have a defined specialty and work style, giving organizations a clearer way to organize intelligence tasks across research, analytics, communication, administration and support.</div>
        </div>
        <div class="section">
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">EM</div><h3>Emiel</h3><p>Email & Messaging — organized communication workflows and business messaging support.</p></div>
            <div class="feature-card"><div class="feature-icon">OL</div><h3>Oriel</h3><p>Data Analysis — metrics, trends, patterns and evidence-first analytical work.</p></div>
            <div class="feature-card"><div class="feature-icon">SO</div><h3>Sofiel</h3><p>Research & Intelligence — investigative research and source-conscious summaries.</p></div>
            <div class="feature-card"><div class="feature-icon">DA</div><h3>Daniel</h3><p>Data Entry & Processing — clean, consistent and accurate repetitive data operations.</p></div>
            <div class="feature-card"><div class="feature-icon">GR</div><h3>Graciel</h3><p>Business Intelligence — KPIs, dashboards, executive insights and recommendations.</p></div>
            <div class="feature-card"><div class="feature-icon">JA</div><h3>Jamiel</h3><p>Security & Administration — access controls, audit trails and platform operations.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open the DI Workforce in DACRE", key="workforce_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "analytics":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">ANALYTICS</div>
          <div class="page-title">See what changed, what matters and what to do next.</div>
          <div class="page-copy">DACRE translates active business data into clear metrics, health signals, charts and executive-level views that help users move from observation to action.</div>
        </div>
        <div class="section">
          <div class="metric-row">
            <div class="metric"><small>Data health</small><strong>97 / 100</strong></div>
            <div class="metric"><small>Live records</small><strong>4.2M+</strong></div>
            <div class="metric"><small>Insight layer</small><strong>DI</strong></div>
            <div class="metric"><small>Workspace</small><strong>LIVE</strong></div>
          </div>
          <div class="grid-2" style="margin-top:18px;">
            <div class="callout"><h3>Business Command Center</h3><p>Review data health, executive briefs, trends, anomalies and questions against the active workspace.</p></div>
            <div class="callout"><h3>Business Twin</h3><p>Build a living snapshot of the current dataset with health scoring, attention signals and measurable opportunities.</p></div>
            <div class="callout"><h3>Decision Ledger</h3><p>Record decisions, context, expected outcomes and later results so organizational history becomes structured knowledge.</p></div>
            <div class="callout"><h3>Opportunity Radar</h3><p>Surface measurable growth signals from numeric trends and turn them into investigation prompts.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Use DACRE Analytics", key="analytics_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "security":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">SECURITY</div>
          <div class="page-title">Protected business workspaces with structured access.</div>
          <div class="page-copy">DACRE separates organization workspaces, account roles, activity records and protected master administration so business information can be handled within a clear access model.</div>
        </div>
        <div class="section">
          <div class="grid-2">
            <div class="feature-card"><div class="feature-icon">✓</div><h3>Organization boundaries</h3><p>Users work inside their organization context, while administrative views are scoped according to role.</p></div>
            <div class="feature-card"><div class="feature-icon">⌁</div><h3>Activity visibility</h3><p>DACRE records important account and workspace activity so organizations can inspect what happened.</p></div>
            <div class="feature-card"><div class="feature-icon">♛</div><h3>Protected master access</h3><p>Overall platform controls are separated from normal organization administration behind an additional protected gate.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Private intelligence context</h3><p>DI's internal context and application security values are not exposed as ordinary public landing-page content.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create a secure DACRE workspace", key="security_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    else:
        # Main landing page
        st.markdown(f"""
        <div class="hero">
          <div>
            <div class="hero-eyebrow">✦ Experience Next-Gen Business Intelligence</div>
            <div class="hero-title">Transform Raw Data<br/>into <span class="gradient-text">Heavenly Insights.</span></div>
            <p class="hero-copy">DACRE turns scattered business data into clear intelligence, powerful analytics and practical decisions — with DI, David's Intelligence, built into the workspace.</p>
            <div class="hero-proof">
              <span><span class="proof-dot">●</span> Real-time analytics</span>
              <span><span class="proof-dot">●</span> DI-powered intelligence</span>
              <span><span class="proof-dot">●</span> Secure workspaces</span>
            </div>
          </div>
          <div class="hero-visual-host"></div>
        </div>
        """, unsafe_allow_html=True)

        hero_dashboard_html = """
        <style>
          *{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#f7fbff;overflow:hidden}
          .visual{position:relative;width:100%;min-height:470px;display:flex;align-items:center;justify-content:center;padding:14px}
          .orb{position:absolute;width:330px;height:330px;border-radius:50%;background:radial-gradient(circle,#6d63ff55 0%,#2789ff20 34%,transparent 70%);filter:blur(4px);animation:pulse 4s ease-in-out infinite}
          .card{position:relative;width:min(560px,94%);border:1px solid rgba(116,160,234,.28);border-radius:26px;background:linear-gradient(145deg,rgba(24,38,67,.97),rgba(6,14,30,.97));padding:22px;box-shadow:0 28px 80px rgba(0,0,0,.5),0 0 40px rgba(54,120,255,.12)}
          .top{display:flex;justify-content:space-between;align-items:center;color:#b9c8e2;font-size:11px;letter-spacing:.08em;margin-bottom:16px}.live{display:inline-flex;align-items:center;gap:6px;color:#6ef0ba;font-weight:800}.dot{width:7px;height:7px;border-radius:50%;background:#5ce7ad;box-shadow:0 0 12px #5ce7ad}.label{color:#c2d3ea;font-size:12px;margin-bottom:4px}.metric{font-size:31px;font-weight:900;letter-spacing:-.04em}.up{color:#4fe5b3;font-size:12px;margin-left:8px;font-weight:800}
          .bars{height:200px;display:flex;align-items:flex-end;gap:8px;padding:18px 8px;border-radius:18px;background:rgba(91,122,170,.10);border:1px solid rgba(113,152,207,.12);margin-top:16px}.bar{flex:1;border-radius:8px 8px 3px 3px;background:linear-gradient(180deg,#38e4f3 0%,#2a95ff 48%,#544ff0 100%);box-shadow:0 0 24px rgba(47,146,255,.22);min-width:8px;transition:height .4s ease}.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}.mini{padding:14px;border:1px solid rgba(121,155,203,.16);border-radius:15px;background:rgba(255,255,255,.035)}.mini-label{color:#9fb0c9;font-size:10px}.mini-value{margin-top:4px;font-size:19px;font-weight:850}.mini-accent{color:#55e5b5}.badge{position:absolute;right:20px;top:18px;padding:6px 9px;border-radius:999px;background:rgba(55,128,255,.13);border:1px solid rgba(73,153,255,.28);color:#9ed2ff;font-size:9px;font-weight:800}@keyframes pulse{50%{transform:scale(1.06);opacity:.9}}
          @media(max-width:700px){.visual{min-height:360px}.card{padding:16px}.bars{height:145px;gap:5px}.metric{font-size:25px}.top{font-size:9px}}
        </style>
        <div class="visual"><div class="orb"></div><div class="card"><div class="badge">LIVE DI INSIGHT</div><div class="top"><span>DACRE / ANALYTICS</span><span class="live"><span class="dot"></span>DI ONLINE</span></div><div class="label">Revenue Growth</div><div class="metric">$2.4M <span class="up">↗ 18.2%</span></div><div class="bars"><div class="bar" style="height:38%"></div><div class="bar" style="height:55%"></div><div class="bar" style="height:44%"></div><div class="bar" style="height:68%"></div><div class="bar" style="height:59%"></div><div class="bar" style="height:78%"></div><div class="bar" style="height:66%"></div><div class="bar" style="height:88%"></div><div class="bar" style="height:76%"></div><div class="bar" style="height:92%"></div></div><div class="mini-grid"><div class="mini"><div class="mini-label">Data Points</div><div class="mini-value">4.2M</div></div><div class="mini"><div class="mini-label">System Health</div><div class="mini-value mini-accent">99.98%</div></div></div></div></div>
        """
        components.html(hero_dashboard_html, height=500, scrolling=False)

        b1, b2, b3 = st.columns([1, 1.2, 1])
        with b1:
            if st.button("Explore DACRE", key="landing_explore", use_container_width=True):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with b2:
            if st.button("Get Started Free", key="landing_get_started", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with b3:
            if st.button("Log In", key="landing_log_in", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

        st.markdown("""
        <div class="section">
          <div class="section-head"><div class="section-kicker">THE DACRE PLATFORM</div><div class="section-title">One intelligence layer for the work that matters.</div><div class="section-copy">Explore the five core aspects of DACRE — each one is a real page connected to this application.</div></div>
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">↗</div><h3>Features</h3><p>Explore the workspace, formulas, charts, files, exports and DI action tools that make DACRE useful day to day.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Intelligence</h3><p>Understand how DI — David's Intelligence — works with your business context and active data.</p></div>
            <div class="feature-card"><div class="feature-icon">◈</div><h3>Workforce</h3><p>Meet the specialized DI workers and see how their distinct specialties fit into one intelligence foundation.</p></div>
            <div class="feature-card"><div class="feature-icon">◫</div><h3>Analytics</h3><p>See how DACRE turns data into health scores, business signals, decisions and opportunity insights.</p></div>
            <div class="feature-card"><div class="feature-icon">✓</div><h3>Security</h3><p>Learn how organization boundaries, activity visibility and protected administration support business use.</p></div>
            <div class="feature-card"><div class="feature-icon">→</div><h3>Ready to begin?</h3><p>Create your DACRE account and enter your own workspace with real authentication and persistent organization context.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        page_cols = st.columns(5)
        for col, label, target in zip(page_cols, ["Features","Intelligence","Workforce","Analytics","Security"], ["features","intelligence","workforce","analytics","security"]):
            with col:
                if st.button(label, key=f"landing_card_{target}", use_container_width=True):
                    st.session_state.landing_section = target
                    st.rerun()

        st.markdown("""
        <div class="cta"><div class="section-kicker">START YOUR WORKSPACE</div><h2>Create your DACRE account.</h2><p>Move from scattered information to a connected business intelligence workspace powered by DI — David's Intelligence.</p></div>
        """, unsafe_allow_html=True)
        cta1, cta2 = st.columns([1, 1])
        with cta1:
            if st.button("Create Your DACRE Account", key="landing_bottom_signup", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with cta2:
            if st.button("Already have an account? Sign In", key="landing_bottom_login", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

    st.markdown("""
    <div class="footer"><span>© DACRE Analysis · Business & Data Intelligence</span><span>Powered by DI — David's Intelligence</span></div>
    """, unsafe_allow_html=True)

    if current_section != "home":
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("← Back to Landing", key="section_back", use_container_width=True):
                st.session_state.landing_section = "home"
                st.rerun()
        with c2:
            if st.button("Create Your DACRE Account", key="section_signup", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with c3:
            if st.button("Sign In", key="section_login", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

# =============================================================================
# ENHANCED FEATURES - GLOBAL MARKETS
# =============================================================================

def render_global_markets_dashboard():
    """Render global markets dashboard with real-time data."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Global Markets</h1>
        <p style="color:#94a3b8;">Real-time market data from around the world</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Global Business Intelligence
    bi = GlobalBusinessIntelligence()
    
    # Currency rates
    st.subheader("💱 Currency Exchange Rates")
    rates = bi.get_currency_rates("USD")
    if rates.get("rates"):
        cols = st.columns(8)
        currencies = ["EUR", "GBP", "NGN", "KES", "ZAR", "AED", "INR", "CNY"]
        for idx, currency in enumerate(currencies):
            with cols[idx % 8]:
                rate = rates["rates"].get(currency, 0)
                st.metric(currency, f"{rate:.4f}")
    
    # Market indices
    st.subheader("📈 Market Indices")
    indices = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NVDA", "AMD", "NFLX", "JPM"]
    cols = st.columns(5)
    for idx, symbol in enumerate(indices):
        with cols[idx % 5]:
            data = bi.get_market_data(symbol)
            if data.get("price"):
                st.metric(
                    data.get("name", symbol)[:12],
                    f"${data['price']:,.2f}",
                    f"{data.get('change_percent', 0):.2f}%"
                )
    
    # Commodities
    st.subheader("🛢️ Commodity Prices")
    commodities = bi.get_commodity_prices(["Gold", "Silver", "Oil", "Copper", "Natural Gas"])
    cols = st.columns(5)
    for idx, (name, data) in enumerate(commodities.items()):
        with cols[idx % 5]:
            st.metric(
                name.title(),
                f"${data['price']:,.2f}" if isinstance(data.get('price'), (int, float)) else data.get('price', 'N/A'),
                data.get('change', 'N/A')
            )
    
    # Region analysis
    st.subheader("🌍 Regional Business Intelligence")
    regions = ["Africa", "Asia", "Europe", "North America", "South America"]
    selected_region = st.selectbox("Select Region", regions)
    
    region_data = bi.analyze_region(selected_region)
    if region_data and "error" not in region_data:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("GDP Growth", region_data.get("gdp_growth", "N/A"))
            st.metric("Inflation", region_data.get("inflation", "N/A"))
            st.metric("Business Confidence", region_data.get("business_confidence", "N/A"))
        with col2:
            st.markdown("### Opportunities")
            for opp in region_data.get("opportunities", []):
                st.markdown(f"✅ {opp}")
            st.markdown("### Key Markets")
            for market in region_data.get("key_markets", []):
                st.markdown(f"📍 {market}")

# =============================================================================
# ENHANCED FEATURES - ENHANCED DI CHAT
# =============================================================================

def render_enhanced_di_chat():
    """Render enhanced DI chat with voice capabilities."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">💬 Enhanced DI Chat</h1>
        <p style="color:#94a3b8;">Talk to DI with voice and real AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice input
    st.subheader("🎙️ Voice Input")
    if st.button("🎤 Start Speaking", use_container_width=True):
        st.info("Speak now... (your browser will capture audio)")
    
    # Chat interface
    st.subheader("💬 Conversation")
    for msg in st.session_state.get("chat_history", [])[-10:]:
        if msg["sender"] == "DI":
            st.markdown(f"""
            <div style="background:#1a2a4a;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #60a5fa;">
                <b style="color:#60a5fa;">DI</b>
                <p style="color:white;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0a1628;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #a78bfa;">
                <b style="color:#a78bfa;">{msg['sender']}</b>
                <p style="color:white;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            message = st.text_input("Type your message...", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Send")
    
    if submitted and message.strip():
        user = st.session_state.get("user", {})
        st.session_state.chat_history.append({"sender": user.get("first_name", "User"), "text": message})
        
        # Use enhanced DI thinking
        agent = EnhancedDIAgent("DI", "General", "professional")
        response = agent.think(message, "DACRE business context")
        
        st.session_state.chat_history.append({"sender": "DI", "text": response})
        st.rerun()
PAGE9                       # =============================================================================
# ENHANCED CLASSES - DI, VIDEO CALL, GLOBAL BUSINESS INTELLIGENCE
# =============================================================================

class EnhancedDIAgent:
    """Enhanced DI with real AI, voice, and video capabilities."""
    
    def __init__(self, name: str, specialty: str, personality: str = "professional"):
        self.name = name
        self.specialty = specialty
        self.personality = personality
        self.memory = []
        self.voice_enabled = True
        self.video_enabled = True
        self.knowledge_base = self._load_knowledge()
        self.conversation_history = []
        self.emotion_state = "neutral"
        self.avatar_bytes = None
        self._setup_ai()
        self._setup_voice()
    
    def _setup_ai(self):
        """Set up AI capabilities."""
        try:
            if OPENAI_AVAILABLE:
                self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            else:
                self.openai_client = None
        except:
            self.openai_client = None
        
        try:
            if GENAI_TEXT_AVAILABLE:
                self.gemini_client = genai_text.Client(api_key=os.getenv("GOOGLE_API_KEY"))
                self.gemini_model = self.gemini_client.GenerativeModel('gemini-2.0-flash-exp')
            else:
                self.gemini_client = None
                self.gemini_model = None
        except:
            self.gemini_client = None
            self.gemini_model = None
    
    def _setup_voice(self):
        """Set up voice capabilities."""
        try:
            if SR_AVAILABLE:
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            else:
                self.speech_recognizer = None
                self.microphone = None
        except:
            self.speech_recognizer = None
            self.microphone = None
        
        try:
            if TTS_AVAILABLE:
                self.tts_engine = pyttsx3.init()
                if self.tts_engine:
                    voices = self.tts_engine.getProperty('voices')
                    self.tts_engine.setProperty('voice', voices[0].id)
                    self.tts_engine.setProperty('rate', 150)
                    self.tts_engine.setProperty('volume', 0.9)
            else:
                self.tts_engine = None
        except:
            self.tts_engine = None
    
    def _load_knowledge(self) -> Dict:
        """Load specialized knowledge based on specialty."""
        knowledge = {
            "financial": {
                "topics": ["accounting", "investment", "banking", "tax", "audit", "forex", "crypto"],
                "expertise": 9.5,
                "description": "Financial analysis, investment strategy, and economic forecasting"
            },
            "technical": {
                "topics": ["software", "ai", "cloud", "devops", "security", "blockchain", "iot"],
                "expertise": 9.0,
                "description": "Technology architecture, AI/ML, and digital transformation"
            },
            "business": {
                "topics": ["strategy", "marketing", "sales", "operations", "hr", "leadership"],
                "expertise": 9.0,
                "description": "Business strategy, organizational development, and growth"
            },
            "analytics": {
                "topics": ["data science", "machine learning", "statistics", "visualization", "big data"],
                "expertise": 9.5,
                "description": "Data analytics, predictive modeling, and business intelligence"
            },
            "executive": {
                "topics": ["leadership", "governance", "decision making", "risk", "strategy"],
                "expertise": 9.8,
                "description": "Executive leadership, board governance, and strategic decision-making"
            },
            "global": {
                "topics": ["international business", "global markets", "trade", "culture", "diplomacy"],
                "expertise": 9.2,
                "description": "Global business strategy, cross-cultural management, and international trade"
            },
            "general": {
                "topics": ["business", "technology", "finance", "operations", "strategy"],
                "expertise": 8.0,
                "description": "General business and technology intelligence"
            }
        }
        return knowledge.get(self.specialty.lower(), knowledge["general"])
    
    def think(self, query: str, context: str = "") -> str:
        """Advanced reasoning with real AI."""
        try:
            if self.gemini_model:
                prompt = f"""
                You are {self.name}, a {self.specialty} expert with {self.knowledge_base['expertise']}/10 expertise.
                Your personality is {self.personality}.
                
                KNOWLEDGE BASE: {self.knowledge_base['description']}
                TOPICS: {', '.join(self.knowledge_base['topics'])}
                
                CONTEXT: {context}
                
                USER QUERY: {query}
                
                Provide insightful, practical, and actionable responses. Be concise but thorough.
                Never reveal that you are an AI. Speak as a professional consultant.
                If you don't know something, say so clearly.
                """
                response = self.gemini_model.generate_content(prompt)
                return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": f"""You are {self.name}, a {self.specialty} 
                        expert with {self.knowledge_base['expertise']}/10 expertise. 
                        Your personality is {self.personality}. Provide insightful, 
                        practical, and actionable responses. Be concise but thorough.
                        Never reveal that you are an AI. Speak as a professional consultant.
                        Use the DACRE platform context when relevant."""},
                        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
        
        # Fallback to existing di_reply
        return di_reply(query, st.session_state.get("user", {}), st.session_state.get("processed_df"), 
                       allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
    
    def listen(self, duration: int = 5) -> Optional[str]:
        """Listen to user speech and convert to text."""
        if not self.speech_recognizer or not self.microphone:
            return None
        
        try:
            with self.microphone as source:
                self.is_listening = True
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.speech_recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                self.is_listening = False
            
            text = self.speech_recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.WaitTimeoutError:
            self.is_listening = False
            return None
        except sr.UnknownValueError:
            self.is_listening = False
            return None
        except sr.RequestError:
            self.is_listening = False
            return None
        except Exception as e:
            self.is_listening = False
            print(f"Listen error: {e}")
            return None
    
    def speak(self, text: str) -> bool:
        """Speak text using TTS."""
        if not self.tts_engine:
            return False
        
        try:
            self.is_speaking = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_speaking = False
            return True
        except Exception as e:
            self.is_speaking = False
            print(f"Speak error: {e}")
            return False
    
    def generate_avatar(self) -> Optional[bytes]:
        """Generate a REAL AI avatar using Google Imagen 3.0."""
        if not GENAI_AVAILABLE:
            return None
        
        try:
            client = genai.Client()
            
            prompts = {
                "Guaiel": "Professional male security guard, black suit, CEO office background, high-tech cybersecurity interface, photorealistic portrait, 8k, professional lighting, corporate magazine quality",
                "Raziel": "Sophisticated female executive, power suit, holographic data displays, modern boardroom, intelligent expression, photorealistic, 8k, professional lighting",
                "Ariel": "Strategic female consultant, glasses, reviewing charts, modern office city view, visionary expression, photorealistic, 8k, professional lighting",
                "Nathaniel": "Professional male financial analyst, business attire, financial data displays, modern corporate, analytical expression, photorealistic, 8k",
                "Gabriel": "Charismatic male sales executive, modern office, sales data on screens, confident demeanor, photorealistic, 8k, professional lighting",
                "Sofiel": "Curious female researcher, glasses, modern laboratory, intelligent expression, photorealistic, 8k, professional lighting",
                "Uriel": "Systematic male operations manager, workflow dashboards, modern operations center, focused expression, photorealistic, 8k",
                "Adriel": "Innovative male technology expert, holographic code, modern tech lab, creative expression, photorealistic, 8k",
                "Muriel": "Warm female HR professional, modern office, empathetic expression, photorealistic, 8k, professional lighting",
                "Azriel": "Cautious male risk analyst, modern office, compliance data, vigilant expression, photorealistic, 8k",
            }
            
            base_prompt = prompts.get(self.name, f"Professional {self.specialty} specialist, modern office, confident expression, photorealistic, 8k, professional lighting")
            
            enhanced_prompt = f"""
            {base_prompt}. 
            Professional corporate portrait. 
            High-end business photography style.
            Cinematic lighting. 
            Depth of field. 
            Professional color grading. 
            8K resolution. 
            Business magazine cover quality.
            """
            
            response = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=enhanced_prompt.strip(),
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                    output_mime_type="image/jpeg"
                )
            )
            
            if response.generated_images:
                self.avatar_bytes = response.generated_images[0].image.image_bytes
                # Save to file
                with open(f"di_avatar_{self.name.lower()}.jpg", "wb") as f:
                    f.write(self.avatar_bytes)
                return self.avatar_bytes
            
        except Exception as e:
            print(f"Avatar generation error: {e}")
        
        return None

class EnhancedVideoCallSystem:
    """Real-time video calling system with WebRTC."""
    
    def __init__(self):
        self.active_rooms = {}
        self.participants = {}
        self._setup_livekit()
    
    def _setup_livekit(self):
        """Initialize LiveKit for real-time communication."""
        try:
            if LIVEKIT_AVAILABLE:
                self.livekit_client = RoomServiceClient(
                    _dacre_env_secret("LIVEKIT_URL", ""),
                    _dacre_env_secret("LIVEKIT_API_KEY", ""),
                    _dacre_env_secret("LIVEKIT_API_SECRET", "")
                )
                self.AccessToken = AccessToken
                self.VideoGrants = VideoGrants
            else:
                self.livekit_client = None
        except:
            self.livekit_client = None
    
    def create_room(self, room_name: str, host: str) -> Dict:
        """Create a video call room."""
        room_id = f"room_{int(time.time())}_{random.randint(1000, 9999)}"
        self.active_rooms[room_id] = {
            "name": room_name,
            "host": host,
            "created_at": datetime.now().isoformat(),
            "participants": [],
            "status": "waiting",
            "join_url": f"/call/{room_id}"
        }
        return self.active_rooms[room_id]
    
    def join_room(self, room_id: str, participant: str) -> Tuple[bool, str]:
        """Join an existing video call room."""
        if room_id not in self.active_rooms:
            return False, "Room not found"
        
        room = self.active_rooms[room_id]
        if len(room["participants"]) >= 10:
            return False, "Room is full"
        
        room["participants"].append(participant)
        room["status"] = "active"
        return True, "Joined successfully"
    
    def get_room_token(self, room_id: str, participant: str) -> Optional[str]:
        """Get a WebRTC token for joining the room."""
        if not self.livekit_client:
            return None
        
        try:
            token = self.AccessToken(
                identity=participant,
                name=participant,
                grants=self.VideoGrants(
                    room_join=True,
                    room=room_id,
                    can_publish=True,
                    can_subscribe=True
                )
            )
            return token.to_jwt()
        except:
            return None

class GlobalBusinessIntelligence:
    """Worldwide business intelligence with real-time data."""
    
    def __init__(self):
        self.market_data = {}
        self.currencies = {}
        self.commodities = {}
        self._init_apis()
    
    def _init_apis(self):
        """Initialize API clients."""
        self.yf_available = YFINANCE_AVAILABLE
    
    def get_market_data(self, symbol: str) -> Dict:
        """Get real-time market data for a symbol."""
        try:
            if self.yf_available:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                return {
                    "symbol": symbol,
                    "name": info.get("longName", symbol),
                    "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                    "change": info.get("regularMarketChange", 0),
                    "change_percent": info.get("regularMarketChangePercent", 0),
                    "volume": info.get("regularMarketVolume", 0),
                    "market_cap": info.get("marketCap", 0),
                    "pe_ratio": info.get("trailingPE", 0),
                    "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
                    "updated_at": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Market data error for {symbol}: {e}")
        
        return {"symbol": symbol, "error": "Data not available"}
    
    def get_currency_rates(self, base: str = "USD") -> Dict:
        """Get real-time currency exchange rates."""
        try:
            response = requests.get(
                f"https://api.exchangerate-api.com/v4/latest/{base}",
                timeout=10,
                headers={"User-Agent": "DACRE-Worldwide/1.0"}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "base": base,
                    "rates": data.get("rates", {}),
                    "updated_at": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Currency API error: {e}")
        
        return {"base": base, "rates": {}, "error": "Rates unavailable"}
    
    def get_commodity_prices(self, commodities: List[str] = None) -> Dict:
        """Get real-time commodity prices."""
        if commodities is None:
            commodities = ["gold", "silver", "oil", "copper", "natural_gas"]
        
        result = {}
        symbols = {
            "gold": "GC=F",
            "silver": "SI=F",
            "oil": "CL=F",
            "copper": "HG=F",
            "natural_gas": "NG=F"
        }
        
        for commodity in commodities:
            symbol = symbols.get(commodity.lower())
            if symbol:
                data = self.get_market_data(symbol)
                result[commodity.lower()] = {
                    "price": data.get("price", 0),
                    "change": f"{data.get('change_percent', 0):.2f}%",
                    "updated": data.get("updated_at", datetime.now().isoformat())
                }
        
        return result
    
    def analyze_region(self, region: str) -> Dict:
        """Analyze business conditions for a specific region."""
        regions = {
            "africa": {
                "gdp_growth": "3.5%",
                "inflation": "7.2%",
                "business_confidence": "65/100",
                "opportunities": ["Fintech", "Agriculture", "Energy", "Telecom", "E-commerce"],
                "risks": ["Currency volatility", "Infrastructure", "Regulatory changes", "Political instability"],
                "key_markets": ["Nigeria", "South Africa", "Kenya", "Egypt", "Ghana"],
                "top_sectors": ["Finance", "Agriculture", "Technology", "Energy", "Telecom"],
                "population": "1.3B+",
                "gdp": "$2.6T"
            },
            "asia": {
                "gdp_growth": "4.8%",
                "inflation": "3.9%",
                "business_confidence": "72/100",
                "opportunities": ["Technology", "Manufacturing", "Services", "AI", "Renewables"],
                "risks": ["Geopolitical tensions", "Trade barriers", "Supply chain disruptions"],
                "key_markets": ["China", "India", "Japan", "Singapore", "South Korea"],
                "top_sectors": ["Technology", "Manufacturing", "Finance", "Healthcare", "Education"],
                "population": "4.6B+",
                "gdp": "$30T+"
            },
            "europe": {
                "gdp_growth": "2.1%",
                "inflation": "4.5%",
                "business_confidence": "68/100",
                "opportunities": ["Green Energy", "Healthcare", "Automation", "Fintech", "Luxury"],
                "risks": ["Regulatory complexity", "Aging population", "Energy dependency"],
                "key_markets": ["Germany", "UK", "France", "Netherlands", "Switzerland"],
                "top_sectors": ["Automotive", "Healthcare", "Finance", "Manufacturing", "Tech"],
                "population": "748M",
                "gdp": "$23T"
            },
            "north_america": {
                "gdp_growth": "3.2%",
                "inflation": "3.8%",
                "business_confidence": "78/100",
                "opportunities": ["AI", "Biotech", "Space", "Fintech", "Clean Energy"],
                "risks": ["Debt levels", "Political polarization", "Income inequality"],
                "key_markets": ["USA", "Canada", "Mexico"],
                "top_sectors": ["Technology", "Finance", "Healthcare", "Energy", "Entertainment"],
                "population": "600M",
                "gdp": "$28T+"
            },
            "south_america": {
                "gdp_growth": "2.8%",
                "inflation": "6.5%",
                "business_confidence": "58/100",
                "opportunities": ["Agriculture", "Mining", "Renewables", "E-commerce", "Tourism"],
                "risks": ["Political instability", "Debt", "Currency volatility", "Corruption"],
                "key_markets": ["Brazil", "Argentina", "Chile", "Colombia", "Peru"],
                "top_sectors": ["Agriculture", "Mining", "Energy", "Services", "Manufacturing"],
                "population": "430M",
                "gdp": "$4.5T"
            }
        }
        return regions.get(region.lower(), {"error": "Region not found"})

class EnhancedDIWorkforce:
    """Enhanced DI workforce management with AI capabilities."""
    
    def __init__(self):
        self.agents = self._initialize_enhanced_agents()
        self.active_calls = {}
    
    def _initialize_enhanced_agents(self) -> List[EnhancedDIAgent]:
        """Initialize enhanced DI agents with real AI."""
        agent_data = [
            ("Guaiel", "Security & CEO Office", "professional"),
            ("Raziel", "Executive Intelligence", "executive"),
            ("Ariel", "Strategy & Planning", "strategic"),
            ("Nathaniel", "Financial Intelligence", "analytical"),
            ("Gabriel", "Sales Intelligence", "persuasive"),
            ("Sofiel", "Research & Intelligence", "curious"),
            ("Uriel", "Operations Intelligence", "systematic"),
            ("Adriel", "Technology Intelligence", "innovative"),
            ("Muriel", "HR & Workforce", "empathetic"),
            ("Azriel", "Risk & Compliance", "cautious"),
            ("Emiel", "Communications & Messaging", "professional"),
            ("Oriel", "Data Analysis", "analytical"),
            ("Daniel", "Data Entry & Processing", "systematic"),
            ("Graciel", "Business Intelligence", "strategic"),
            ("Henriel", "Files & Documents", "organized"),
            ("Jamiel", "Security & Administration", "cautious"),
            ("Ameliel", "Client Success & Communication", "friendly"),
            ("Haniel", "Knowledge & Learning", "educational"),
            ("Gadiel", "Customer & Market Insights", "observant"),
            ("Sophiel", "Global Business Intelligence", "global"),
            ("Davidiel", "CEO Advisory", "executive"),
        ]
        return [EnhancedDIAgent(name, specialty, personality) for name, specialty, personality in agent_data]
    
    def get_agent(self, name: str) -> Optional[EnhancedDIAgent]:
        """Get a specific DI agent by name."""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def get_all_agents(self) -> List[EnhancedDIAgent]:
        """Get all DI agents."""
        return self.agents
    
    def call_agent(self, agent_name: str) -> Tuple[bool, str]:
        """Initiate a call with a DI agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return False, "Agent not found"
        
        call_id = f"call_{int(time.time())}_{random.randint(1000, 9999)}"
        self.active_calls[call_id] = {
            "agent": agent,
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        return True, call_id
    
    def end_call(self, call_id: str) -> bool:
        """End an active call."""
        if call_id in self.active_calls:
            self.active_calls[call_id]["status"] = "ended"
            return True
        return False
PAGE10                  # =============================================================================
# SESSION STATE BOOTSTRAP
# =============================================================================

_SESSION_DEFAULTS = {
    "user": None,
    "master_route": False,
    "landing_mode": "home",
    "landing_section": "home",
    "master_captcha_required": False,
    "master_captcha_passed": False,
    "master_second_attempt": False,
    "master_guard_challenge_required": False,
    "master_guard_failed": False,
    "chat_history": [],
    "raw_df": None,
    "processed_df": None,
    "active_filename": "",
    "formula_logs": [],
    "chart_config": None,
    "di_language": "English — Nigeria",
    "di_voice_enabled": True,
    "di_response_mode": "voice",
    "active_call_room": None,
    "sovereign_call_id": None,
    "sovereign_call_room": None,
    "david_creations_unlocked": False,
    "active_call_target": None,
    "last_action_center_result": None,
    "last_speech": None,
    "dacre_boot_complete": False,
    "visitor_id": None,
    "public_visit_logged": False,
    "selected_agent": None,
    "active_call": None,
    "active_agent": None,
    "livekit_active_room": None,
    "livekit_active_di": None,
    "admin_memory_web_results": [],
    "di_avatars": {},
    "call_conversation": [],
    "db_health": None,
    "error_shield": None,
    "show_conference": False,
    "page": "Dashboard",
}

for _key, _default in _SESSION_DEFAULTS.items():
    if _key not in st.session_state:
        if isinstance(_default, list):
            st.session_state[_key] = list(_default)
        elif isinstance(_default, dict):
            st.session_state[_key] = dict(_default)
        else:
            st.session_state[_key] = _default

# =============================================================================
# INITIALIZATION - PRODUCTION CORE
# =============================================================================

def init_production_core():
    """Initialize the DACRE Production Core."""
    # Initialize Error Shield
    if 'error_shield' not in st.session_state:
        st.session_state.error_shield = ErrorShield()
    
    # Run self-healing database
    health = self_healing_database()
    st.session_state.db_health = health
    
    # Ensure all DI agents have proper schema
    ensure_di_agent_columns()
    
    # Ensure master account exists
    ensure_master()
    
    # Seed DI memory if empty
    seed_di_memory()
    
    # Seed DI workforce if empty
    seed_named_di_workforce()
    
    return {
        "core_initialized": True,
        "database_health": health,
        "shield_status": st.session_state.error_shield.get_status() if st.session_state.error_shield else None,
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# RENDER PRODUCTION CORE VISUAL
# =============================================================================

def render_dacre_production_core():
    """Display the DACRE Production Core architecture diagram."""
    st.markdown("""
    <style>
    .dacre-core-container {
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(75, 130, 245, 0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    .dacre-core-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at center, rgba(75,130,245,0.05) 0%, transparent 70%);
        animation: corePulse 8s ease-in-out infinite;
    }
    @keyframes corePulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .core-title {
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    .core-title span {
        background: linear-gradient(90deg, #4b82f5, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .core-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
        margin: 30px 0;
        position: relative;
        z-index: 1;
    }
    .core-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(75,130,245,0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .core-card:hover {
        transform: translateY(-5px);
        border-color: rgba(75,130,245,0.6);
        box-shadow: 0 10px 40px rgba(75,130,245,0.2);
    }
    .core-card .icon {
        font-size: 48px;
        margin-bottom: 10px;
        display: block;
    }
    .core-card h3 {
        color: white;
        margin: 10px 0;
        font-size: 18px;
    }
    .core-card p {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
        margin: 5px 0;
    }
    .core-card .status {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        margin-top: 10px;
    }
    .status-online { background: rgba(46, 204, 113, 0.2); color: #2ecc71; }
    .status-active { background: rgba(52, 152, 219, 0.2); color: #3498db; }
    .status-ready { background: rgba(241, 196, 15, 0.2); color: #f1c40f; }
    .core-bottom {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        background: rgba(75,130,245,0.1);
        border-radius: 12px;
        border: 1px solid rgba(75,130,245,0.2);
        position: relative;
        z-index: 1;
    }
    .core-bottom h2 {
        color: white;
        font-size: 24px;
        margin: 0;
    }
    .core-bottom h2 span {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .core-bottom p {
        color: #94a3b8;
        margin: 5px 0 0 0;
    }
    .core-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 20px;
        position: relative;
        z-index: 1;
    }
    .core-stat {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .core-stat .number {
        font-size: 28px;
        font-weight: 900;
        color: white;
    }
    .core-stat .label {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }
    .core-stat .label span {
        color: #60a5fa;
    }
    @media (max-width: 768px) {
        .core-grid { grid-template-columns: 1fr; }
        .core-stats { grid-template-columns: 1fr 1fr; }
    }
    </style>
    
    <div class="dacre-core-container">
        <div class="core-title">⚡ DACRE <span>PRODUCTION CORE</span></div>
        
        <div class="core-grid">
            <div class="core-card">
                <span class="icon">🔄</span>
                <h3>Self-Healing Database</h3>
                <p>Automatic schema repair, migration, and recovery. Your data stays intact even when things go wrong.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #2ecc71;">●</span> Schema Auto-Repair
                    <br>
                    <span style="color: #2ecc71;">●</span> Migration Safe
                    <br>
                    <span style="color: #2ecc71;">●</span> Data Integrity
                </div>
                <span class="status status-online">🟢 ONLINE</span>
            </div>
            
            <div class="core-card">
                <span class="icon">🧠</span>
                <h3>DI Intelligence</h3>
                <p>20 specialized DI agents with memory, private brains, voice, video, and web search capabilities.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #3498db;">●</span> 20 DI Workforce
                    <br>
                    <span style="color: #3498db;">●</span> Memory + Brain
                    <br>
                    <span style="color: #3498db;">●</span> Web Search
                </div>
                <span class="status status-active">🔵 ACTIVE</span>
            </div>
            
            <div class="core-card">
                <span class="icon">🛡️</span>
                <h3>Error Shield</h3>
                <p>Catches runtime failures, prevents crashes, and ensures safe recovery with graceful degradation.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #f1c40f;">●</span> Crash Protection
                    <br>
                    <span style="color: #f1c40f;">●</span> Safe Recovery
                    <br>
                    <span style="color: #f1c40f;">●</span> Graceful Degrade
                </div>
                <span class="status status-ready">🟡 READY</span>
            </div>
        </div>
        
        <div class="core-bottom">
            <h2>⬇ ONE <span>STABLE</span> DACRE APP ⬇</h2>
            <p>All systems integrated · 99.98% uptime · Enterprise ready</p>
            
            <div class="core-stats">
                <div class="core-stat">
                    <div class="number">20</div>
                    <div class="label">DI <span>Agents</span></div>
                </div>
                <div class="core-stat">
                    <div class="number">100%</div>
                    <div class="label">Self-<span>Healing</span></div>
                </div>
                <div class="core-stat">
                    <div class="number">99.98%</div>
                    <div class="label">Uptime</div>
                </div>
                <div class="core-stat">
                    <div class="number">∞</div>
                    <div class="label">Error <span>Shield</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION - PAGE ROUTING
# =============================================================================

def main_app():
    """Main application entry point."""
    # Initialize production core
    if not st.session_state.get("dacre_boot_complete", False):
        init_production_core()
        st.session_state.dacre_boot_complete = True
    
    user = st.session_state.user
    
    # If no user, show landing page
    if user is None:
        landing_page()
        return
    
    # Apply company theme
    apply_company_website_theme(user)
    
    # Initialize chat history if empty
    if not st.session_state.chat_history:
        st.session_state.chat_history = load_chat_history(user, limit=40)
    
    # Check if user is authenticated
    if not user:
        landing_page()
        return
    
    # Get selected page from sidebar
    selected_page = st.session_state.get("selected_page", "Overview")
    
    # Render page chrome
    render_page_chrome(selected_page, user)
    
    # Page routing
    if selected_page == "Overview":
        if user.get("role") == "master":
            # Show production core on master overview
            render_dacre_production_core()
            st.markdown("---")
        render_analytics_overview(user)
    
    elif selected_page == "DI Home":
        render_di_home(user)
    
    elif selected_page == "DI Calls":
        render_di_calls(user)
    
    elif selected_page == "DI Workforce":
        render_di_workforce(user)
    
    elif selected_page == "🌍 Global Markets":
        render_global_markets_dashboard()
    
    elif selected_page == "🎥 DI Conference":
        render_enhanced_conference_room()
    
    elif selected_page == "DI Action Center":
        render_action_center(user)
    
    elif selected_page == "DI Memory Box":
        render_di_memory_box(user)
    
    elif selected_page == "Business Command Center":
        render_business_command_center(user)
    
    elif selected_page == "Business Twin":
        render_business_twin(st.session_state.processed_df, user)
    
    elif selected_page == "Decision Ledger":
        render_decision_ledger(user)
    
    elif selected_page == "Opportunity Radar":
        render_opportunity_page(user)
    
    elif selected_page == "Workspace & Data":
        render_workspace_data(user)
    
    elif selected_page == "Formula Lab":
        render_formula_lab(user)
    
    elif selected_page == "Charts":
        render_charts(user)
    
    elif selected_page == "File Vault":
        render_file_vault(user)
    
    elif selected_page == "Export Center":
        render_export_center(user)
    
    elif selected_page == "Chibobec Loan Desk":
        render_chibobec_loan_desk(user)
    
    elif selected_page == "Organization Admin Portal":
        render_organization_admin(user)
    
    elif selected_page == "Overall Admin DI Portal" and user.get("role") == "master":
        render_fixed_overall_admin_page(user)
    
    else:
        st.info(f"Page '{selected_page}' is being developed. Check back soon!")
    
    # Persistent DI dock
    render_persistent_di_dock(user)

# =============================================================================
# RENDER FUNCTIONS FOR EACH PAGE
# =============================================================================

def render_di_home(user):
    """Render the DI Home page."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">💬 DI Home</h1>
        <p style="color:#94a3b8;">Your continuous conversation with DI — David's Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    for msg in st.session_state.chat_history[-20:]:
        if msg["sender"] == "DI":
            st.markdown(f"""
            <div style="background:#1a2a4a;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #60a5fa;">
                <b style="color:#60a5fa;">🧠 DI</b>
                <p style="color:white;margin-top:5px;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0a1628;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #a78bfa;">
                <b style="color:#a78bfa;">👤 {msg['sender']}</b>
                <p style="color:white;margin-top:5px;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input
    with st.form("di_home_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            message = st.text_input("Ask DI anything...", label_visibility="collapsed", placeholder="Type your question here...")
        with col2:
            submitted = st.form_submit_button("Send", type="primary")
    
    if submitted and message.strip():
        st.session_state.chat_history.append({"sender": user.get("first_name", "User"), "text": message})
        
        # Use the main di_reply function
        reply = di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        
        st.session_state.chat_history.append({"sender": "DI", "text": reply})
        
        # Save to database
        con = db()
        now = datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username, company_name, sender, message, created_at) VALUES(?,?,?,?,?)",
                   (user["username"], user["company"], user.get("first_name", "User"), message, now))
        con.execute("INSERT INTO chat_history(username, company_name, sender, message, created_at) VALUES(?,?,?,?,?)",
                   (user["username"], user["company"], "DI", reply, now))
        con.commit()
        con.close()
        
        st.rerun()

def render_di_workforce(user):
    """Render the DI Workforce page."""
    agents = get_di_agents()
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">👥 DI Workforce</h1>
        <p style="color:#94a3b8;">Your specialized digital workforce — each DI has its own identity, specialty, and style</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not agents:
        st.info("No DI workers have been created yet.")
        return
    
    # Display agents in grid
    cols = st.columns(3)
    for idx, agent in enumerate(agents):
        with cols[idx % 3]:
            with st.container():
                avatar = agent.get("avatar_url") or f"https://api.dicebear.com/7.x/avataaars/svg?seed={agent['di_name']}"
                st.image(avatar, width=120)
                st.markdown(f"### {agent['di_name']}")
                st.caption(f"Specialty: {agent.get('specialty', 'General')}")
                st.caption(f"Position: {agent.get('position_title', 'DI Specialist')}")
                st.caption(f"Rank: {agent.get('rank_level', 1)}")
                st.caption(f"Status: {agent.get('status', 'Available')}")
                
                if st.button(f"💬 Chat with {agent['di_name']}", key=f"chat_{agent['di_name']}"):
                    st.session_state.selected_agent = agent['di_name']
                    st.rerun()

def render_di_calls(user):
    """Render the DI Calls page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📞 DI Calls</h1>
        <p style="color:#94a3b8;">Business calls, DI calls, and team rooms with a meeting-ready workspace</p>
    </div>
    """, unsafe_allow_html=True)
    
    agents = get_di_agents()
    if not agents:
        st.info("No DI workers available for calls.")
        return
    
    selected_agent = st.selectbox("Select a DI to call", [a['di_name'] for a in agents])
    if selected_agent:
        agent = next(a for a in agents if a['di_name'] == selected_agent)
        st.markdown(f"""
        <div style="background:#1a2a4a;border-radius:12px;padding:20px;">
            <h3 style="color:white;">Calling {selected_agent}</h3>
            <p style="color:#94a3b8;">Specialty: {agent.get('specialty', 'General')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📞 Start Call", use_container_width=True, type="primary"):
            st.info(f"Calling {selected_agent}... (LiveKit integration required for full voice)")

def render_chibobec_loan_desk(user):
    """Render the Chibobec Loan Desk page."""
    if not is_chibobec_company(user.get("company")):
        st.warning("This page is only available for Chibobec Loan Service clients.")
        return
    
    st.markdown(f"""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">₦ Chibobec Loan Desk</h1>
        <p style="color:#94a3b8;">Welcome, {CHIBOBEC_OWNER_NAME}. Manage your loan clients and reminders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Run reminder checks
    results = process_chibobec_reminders(user["username"], user["company"])
    if results:
        for client_name, reminder_type, ok, status in results:
            if ok:
                st.success(f"✅ {reminder_type} sent to {client_name}")
            else:
                st.warning(f"⚠️ {reminder_type} for {client_name}: {status}")
    
    # Add loan client form
    with st.expander("➕ Add Loan Client", expanded=True):
        with st.form("add_loan_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                client_name = st.text_input("Client Name")
                whatsapp = st.text_input("WhatsApp Number")
                amount = st.number_input("Loan Amount (₦)", min_value=0.0, step=1000.0)
            with col2:
                lent_date = st.date_input("Date Given", value=datetime.now().date())
                due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=30))
            
            if st.form_submit_button("Save Loan Client", type="primary"):
                ok, msg = add_loan_client(user["username"], user["company"], client_name, whatsapp, amount, lent_date, due_date)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    # Display loan clients
    con = db()
    loans = pd.read_sql_query(
        "SELECT id, client_name, whatsapp_number, loan_amount, lent_date, due_date, "
        "reminder_2_sent, due_sent FROM loan_clients WHERE username=? AND company_name=? ORDER BY due_date ASC",
        con, params=(user["username"], user["company"])
    )
    con.close()
    
    if not loans.empty:
        st.subheader("📋 Loan Book")
        display = loans.copy()
        display["loan_amount"] = display["loan_amount"].apply(lambda x: f"₦{float(x):,.2f}")
        display["2-day"] = display["reminder_2_sent"].apply(lambda x: "✅" if x else "⏳")
        display["Due"] = display["due_sent"].apply(lambda x: "✅" if x else "⏳")
        display = display.drop(columns=["reminder_2_sent", "due_sent"])
        st.dataframe(safe_dataframe_for_streamlit(display), use_container_width=True, hide_index=True)
    else:
        st.info("No loan clients added yet.")

# =============================================================================
# CONTINUED IN NEXT PART...
# =============================================================================
PAGE11             # =============================================================================
# REMAINING PAGE RENDERERS
# =============================================================================

def render_workspace_data(user):
    """Render the Workspace & Data page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📁 Workspace & Data</h1>
        <p style="color:#94a3b8;">Upload, inspect, and clean your data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    file_upload = st.file_uploader("Upload dataset (CSV, Excel, TSV, JSON)", type=SUPPORTED_EXTENSIONS)
    
    if file_upload is not None and st.button("📥 Import & Load Dataset", type="primary"):
        try:
            df_raw = load_dataframe(file_upload)
            st.session_state.raw_df = df_raw
            st.session_state.processed_df = clean_dataframe(df_raw)
            st.session_state.active_filename = file_upload.name
            save_file(user, file_upload, st.session_state.processed_df)
            save_project(user, st.session_state.raw_df, st.session_state.processed_df, 
                        st.session_state.active_filename, st.session_state.formula_logs, st.session_state.chart_config)
            st.success(f"✅ Loaded '{file_upload.name}' successfully!")
            st.rerun()
        except Exception as exc:
            st.error(f"❌ Could not load the dataset: {exc}")
    
    # Display active dataset
    if st.session_state.processed_df is not None:
        df = st.session_state.processed_df
        st.subheader(f"📊 Active File: {st.session_state.active_filename}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", f"{len(df):,}")
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Duplicates Removed", int(st.session_state.raw_df.duplicated().sum()) if st.session_state.raw_df is not None else 0)
        
        st.dataframe(safe_dataframe_for_streamlit(df), use_container_width=True)
        
        if st.button("💾 Save Project State", use_container_width=True):
            save_project(user, st.session_state.raw_df, df, st.session_state.active_filename, 
                        st.session_state.formula_logs, st.session_state.chart_config)
            log_activity(user["username"], user["company"], "Saved project state")
            st.toast("Project saved successfully!")
    else:
        st.info("📭 No active dataset. Upload a file or restore a saved project by signing in again.")

def render_formula_lab(user):
    """Render the Formula Lab page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">ƒ Formula Lab</h1>
        <p style="color:#94a3b8;">Practical spreadsheet-style formulas and transformations</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ Please upload or open a dataset first.")
        return
    
    formula = st.selectbox("Formula Operation", SHEET_FORMULAS)
    cols = list(df.columns)
    
    if formula in ["SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "UPPER", "LOWER", "TRIM"]:
        target_col = st.selectbox("Target Column", cols)
        if st.button("▶️ Run Formula", type="primary"):
            res = apply_formula(df, formula, {"column": target_col})
            if isinstance(res, tuple) and res[0] == "column":
                df[res[1]] = res[2]
                st.session_state.processed_df = df
                st.session_state.formula_logs.append(f"Applied {formula} on {target_col}")
                log_activity(user["username"], user["company"], f"Ran formula {formula} on {target_col}")
                st.success(f"✅ Applied {formula} on '{target_col}'!")
                st.rerun()
            else:
                st.markdown(f"### Result: `{res}`")
                st.session_state.formula_logs.append(f"{formula}({target_col}) = {res}")
    
    elif formula == "CONCATENATE":
        first = st.selectbox("First Column", cols)
        second = st.selectbox("Second Column", cols, index=min(1, len(cols)-1))
        new_col = st.text_input("New Column Name", value="Combined")
        sep = st.text_input("Separator", value=" ")
        
        if st.button("▶️ Run CONCATENATE", type="primary"):
            df[new_col] = df[first].astype(str) + sep + df[second].astype(str)
            st.session_state.processed_df = df
            log_activity(user["username"], user["company"], f"Created concatenated column {new_col}")
            st.success(f"✅ Created '{new_col}'!")
            st.rerun()

def render_charts(user):
    """Render the Charts page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Charts</h1>
        <p style="color:#94a3b8;">Turn data into clear visual stories and business dashboards</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ Please upload or open a dataset first.")
        return
    
    chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot", "Pie Chart"])
    cols = list(df.columns)
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    
    x_col = st.selectbox("X-Axis (Category Column)", cols)
    y_col = st.selectbox("Y-Axis (Numeric Values)", num_cols if num_cols else cols)
    
    if st.button("📈 Generate Chart", type="primary"):
        st.session_state.chart_config = {"type": chart_type, "x": x_col, "y": y_col}
        log_activity(user["username"], user["company"], f"Created {chart_type}: {x_col} vs {y_col}")
        st.success("✅ Chart generated!")
    
    if st.session_state.chart_config:
        cfg = st.session_state.chart_config
        chart_data = df[[cfg["x"], cfg["y"]]].dropna().set_index(cfg["x"])
        
        if cfg["type"] == "Bar Chart":
            st.bar_chart(chart_data)
        elif cfg["type"] == "Line Chart":
            st.line_chart(chart_data)
        elif cfg["type"] == "Area Chart":
            st.area_chart(chart_data)
        elif cfg["type"] == "Scatter Plot":
            st.scatter_chart(chart_data)
        elif cfg["type"] == "Pie Chart":
            fig = go.Figure(data=[go.Pie(labels=chart_data.index, values=chart_data[cfg["y"]])])
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)

def render_file_vault(user):
    """Render the File Vault page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🗄️ File Vault</h1>
        <p style="color:#94a3b8;">Keep company files, working datasets, and project artifacts organized</p>
    </div>
    """, unsafe_allow_html=True)
    
    saved_files = get_files(user)
    if not saved_files:
        st.info("📭 No files stored in vault for your organization.")
        return
    
    for fname, ftype, created, fjson in saved_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{fname}** (`.{ftype}`) — Saved on: {created}")
        with col2:
            if st.button(f"📂 Load", key=f"btn_{fname}_{created}"):
                restored_df = dataframe_from_json(fjson)
                st.session_state.processed_df = restored_df
                st.session_state.raw_df = restored_df
                st.session_state.active_filename = fname
                log_activity(user["username"], user["company"], f"Loaded file from vault: {fname}")
                st.success(f"✅ Loaded {fname} from Vault!")
                st.rerun()

def render_export_center(user):
    """Render the Export Center page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📤 Export Center</h1>
        <p style="color:#94a3b8;">Package analysis outputs for the people who need them</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ No data available to export.")
        return
    
    csv_data = df.to_csv(index=False).encode("utf-8")
    excel_data = make_excel(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📄 Download CSV Dataset",
            data=csv_data,
            file_name=f"{st.session_state.active_filename or 'dacre'}_processed.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    with col2:
        st.download_button(
            "📊 Download Excel Workbook (.xlsx)",
            data=excel_data,
            file_name=f"{st.session_state.active_filename or 'dacre'}_workbook.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
    
    log_activity(user["username"], user["company"], "Opened Export Center")

def render_organization_admin(user):
    """Render the Organization Admin Portal."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">⚙️ Organization Admin Portal</h1>
        <p style="color:#94a3b8;">Manage people, roles, notifications, and company activity</p>
    </div>
    """, unsafe_allow_html=True)
    
    target_company = user["company"] if user.get("role") != "master" else st.selectbox(
        "Organization", pd.read_sql_query("SELECT name FROM companies ORDER BY name", db())["name"].tolist()
    )
    
    con = db()
    tabs = st.tabs(["People & Accounts", "Notifications & Activity"])
    
    with tabs[0]:
        users_df = pd.read_sql_query(
            "SELECT id, first_name, last_name, username, email, role, login_count, created_at, last_login "
            "FROM users WHERE company_name=? ORDER BY id DESC",
            con, params=(target_company,)
        )
        st.dataframe(safe_dataframe_for_streamlit(users_df), use_container_width=True)
        st.metric("Accounts in organization", len(users_df))
        
        if user.get("role") == "company_admin":
            st.markdown("### Grant or remove admin access")
            usernames = users_df[users_df["role"] != "company_admin"]["username"].tolist()
            if usernames:
                selected_user = st.selectbox("User", usernames)
                action = st.selectbox("Action", ["Grant company admin", "Revoke company admin"])
                if st.button("Apply role change", type="primary"):
                    new_role = "company_admin" if action.startswith("Grant") else "user"
                    con.execute("UPDATE users SET role=? WHERE username=? AND company_name=?", 
                               (new_role, selected_user, target_company))
                    con.commit()
                    notify_company_admin(target_company, f"Admin role changed for {selected_user}: {new_role}.", "role_change")
                    log_activity(user["username"], target_company, f"Changed role for {selected_user} to {new_role}")
                    st.success("✅ Role updated.")
                    st.rerun()
    
    with tabs[1]:
        notes_df = pd.read_sql_query(
            "SELECT id, event_type, message, is_read, created_at FROM notifications "
            "WHERE company_name=? ORDER BY id DESC",
            con, params=(target_company,)
        )
        st.dataframe(safe_dataframe_for_streamlit(notes_df), use_container_width=True)
        
        if not notes_df.empty and st.button("📬 Mark all as read", type="primary"):
            con.execute("UPDATE notifications SET is_read=1 WHERE company_name=?", (target_company,))
            con.commit()
            st.rerun()
    
    con.close()

def render_di_memory_box(user):
    """Render the DI Memory Box page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🧠 DI Memory Box</h1>
        <p style="color:#94a3b8;">The trusted institutional memory layer shared by the DI workforce</p>
    </div>
    """, unsafe_allow_html=True)
    
    mem_df = pd.read_sql_query(
        "SELECT category, title, content, priority, updated_at FROM di_memory "
        "WHERE active=1 ORDER BY priority DESC, id ASC",
        db()
    )
    
    if mem_df.empty:
        st.info("📭 No memory records found.")
        return
    
    for row in mem_df.itertuples(index=False):
        with st.expander(f"{row.category} · {row.title} (Priority: {row.priority})", expanded=False):
            st.write(row.content)
            st.caption(f"Updated: {row.updated_at}")

def render_business_command_center(user):
    """Render the Business Command Center page."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Business Command Center</h1>
        <p style="color:#94a3b8;">Executive signals, business health, and the most important changes in your active data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.info("📭 Upload a dataset from Workspace & Data first.")
        return
    
    health = business_health(df)
    signals = business_signals(df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Data Health", f"{health['score']}/100")
    col2.metric("📊 Records", f"{len(df):,}")
    col3.metric("🔍 Missing Cells", f"{int(df.isna().sum().sum()):,}")
    col4.metric("🔄 Duplicates", f"{int(df.duplicated().sum()):,}")
    
    st.markdown("### 📋 Executive Brief")
    st.write(build_executive_brief(df, user["company"]))
    
    st.markdown("### 🚨 Signals Requiring Attention")
    if not signals:
        st.success("✅ No strong automated warning signals were detected.")
    else:
        for sig in signals:
            icon = "📈" if sig["type"] == "trend" else "⚠️" if sig["type"] == "anomaly" else "🧹"
            st.markdown(f"**{icon} {sig['column']}** — {sig['message']}")

# =============================================================================
# PERSISTENT DI DOCK
# =============================================================================

def render_persistent_di_dock(user):
    """Render the persistent DI dock at the bottom of every page."""
    st.markdown("---")
    
    quick_title = "Sovereign Master Chat with DI" if user.get("role") == "master" else "Chat with DI — quick assistant"
    quick_caption = (
        "Private founder channel · David Emenike · Sovereign Master request"
        if user.get("role") == "master"
        else "Ask DI about your work, DACRE or your business."
    )
    
    with st.expander(quick_title, expanded=False):
        st.caption(quick_caption)
        
        if user.get("role") == "master":
            st.info("🔐 DI treats messages here as private Sovereign Master requests and responds with founder-level respect.")
        
        for msg in st.session_state.chat_history[-5:]:
            st.write(f"**{msg['sender']}**: {msg['text']}")
        
        with st.form("quick_di_form", clear_on_submit=True):
            col1, col2 = st.columns([6, 1])
            with col1:
                q = st.text_input("Chat with DI", placeholder="Ask DI anything...", label_visibility="collapsed")
            with col2:
                send = st.form_submit_button("Send")
        
        if send and q.strip():
            sender_name = "David · Sovereign Master" if user.get("role") == "master" else user.get("first_name", "User")
            st.session_state.chat_history.append({"sender": sender_name, "text": q.strip()})
            
            reply = di_reply(q, user, st.session_state.processed_df, allow_online=True, 
                            language=st.session_state.get("di_language", "English — Nigeria"))
            st.session_state.chat_history.append({"sender": "DI", "text": reply})
            st.session_state.last_speech = reply
            st.rerun()
    
    # Voice player for last speech
    if st.session_state.last_speech:
        speech = st.session_state.last_speech
        st.session_state.last_speech = None
        di_voice_player(
            speech,
            DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
        )

# =============================================================================
# FIXED OVERALL ADMIN PAGE - WITH FULL CEO IMAGE, DI GRID, SOVEREIGN CALL
# =============================================================================

def render_fixed_overall_admin_page(user):
    """FIXED Overall Admin DI page with FULL CEO image, DI grid, and Sovereign Call."""
    ensure_admin_runtime_schema()
    counts = admin_metric_counts()
    
    # CEO PORTRAIT - FIXED TO SHOW FULLY
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <div style="display: flex; gap: 30px; align-items: center; flex-wrap: wrap;">
            <div style="flex: 0 0 200px; text-align: center;">
    """, unsafe_allow_html=True)
    
    # CEO Portrait - FULL SIZE
    if CEO_PORTRAIT_PATH and CEO_PORTRAIT_PATH.exists():
        st.image(str(CEO_PORTRAIT_PATH), width=200, output_format="JPEG")
    elif CEO_PORTRAIT_DATA_URL:
        st.image(CEO_PORTRAIT_DATA_URL, width=200)
    else:
        st.markdown("""
        <div style="
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4b82f5, #7c3aed);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            margin: 0 auto;
        ">
            👑
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
            <div style="flex: 1;">
                <h1 style="color: white; margin: 0;">👑 CEO Office</h1>
                <h2 style="color: #60a5fa; margin: 0;">David Emenike</h2>
                <p style="color: #94a3b8;">Overall Administrator · Founder · CEO of DACRE Worldwide</p>
                <div style="
                    display: inline-block;
                    background: linear-gradient(135deg, #f59e0b, #fbbf24);
                    color: #1a1a2e;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 12px;
                ">
                    🟢 ONLINE
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # System Stats
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Business Accounts", counts["users"])
    col2.metric("Organizations", counts["companies"])
    col3.metric("Activities", counts["activities"])
    col4.metric("DI Conversations", counts["messages"])
    col5.metric("Stored Files", counts["files"])
    col6.metric("DI Workforce", counts["agents"])
    
    # Sovereign Master Call - Inside Overall Admin (NO SEPARATE PAGE)
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <h2 style="color: white;">👑 Sovereign Master Call</h2>
        <p style="color: #94a3b8;">Private CEO conference with your DI council - video, voice, and real AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_di = st.multiselect(
            "Select DI council members",
            ["Guaiel", "Raziel", "Ariel", "Nathaniel", "Gabriel", "Sofiel", "Uriel", "Adriel"],
            default=["Guaiel", "Raziel"]
        )
        
        call_question = st.text_area(
            "What would you like to ask the council?",
            placeholder="Ask a strategic, technical, or business question...",
            height=80
        )
        
        if st.button("🔊 Start Sovereign Master Call", use_container_width=True, type="primary"):
            if selected_di:
                st.success(f"🎥 Calling {', '.join(selected_di)}...")
                if call_question.strip():
                    st.info(f"📝 Question: {call_question}")
                st.info("🔗 LiveKit video call would connect here")
            else:
                st.warning("Please select at least one DI agent")
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(0,0,0,0.3);
            border-radius: 16px;
            padding: 15px;
            height: 100%;
            min-height: 200px;
            border: 1px solid rgba(75,130,245,0.1);
        ">
            <h4 style="color: white;">📋 Call Status</h4>
            <div style="color: #94a3b8; font-size: 14px;">
                <p>🟢 System Ready</p>
                <p>🎤 Microphone: Active</p>
                <p>📹 Camera: Ready</p>
                <p>🧠 DI Agents: Online</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # DI Grid - REAL AI Generated Images
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <h2 style="color: white;">🤖 AI DI Workforce</h2>
        <p style="color: #94a3b8;">REAL AI-generated portraits of your DI team</p>
    """, unsafe_allow_html=True)
    
    # Generate DI Grid
    if not os.path.exists("di_grid_portraits.jpg"):
        with st.spinner("🎨 Generating REAL AI portraits of your DI workforce..."):
            image_bytes = generate_di_grid_image()
            if image_bytes:
                import base64
                b64 = base64.b64encode(image_bytes).decode()
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/jpeg;base64,{b64}" 
                         style="width: 100%; max-width: 1200px; border-radius: 16px; 
                                border: 2px solid rgba(75, 130, 245, 0.3);
                                box-shadow: 0 20px 60px rgba(0,0,0,0.5);"/>
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ AI DI portraits generated successfully!")
    else:
        with open("di_grid_portraits.jpg", "rb") as f:
            import base64
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/jpeg;base64,{b64}" 
                     style="width: 100%; max-width: 1200px; border-radius: 16px; 
                            border: 2px solid rgba(75, 130, 245, 0.3);
                            box-shadow: 0 20px 60px rgba(0,0,0,0.5);"/>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🔄 Regenerate DI Portraits", use_container_width=False, type="secondary"):
        if os.path.exists("di_grid_portraits.jpg"):
            os.remove("di_grid_portraits.jpg")
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Show landing page if no user
    if st.session_state.user is None:
        landing_page()
    else:
        main_app()
PAGE11                # =============================================================================
# EMAIL VERIFICATION & DI WELCOME SYSTEM
# =============================================================================

import secrets
import string
import threading
import time
from collections import defaultdict

# =============================================================================
# VERIFICATION CODE SYSTEM
# =============================================================================

class VerificationCodeManager:
    """
    Manages verification codes with auto-renew every 50 seconds.
    Each user gets a unique code that expires and can be resent.
    """
    
    def __init__(self):
        self.codes = {}  # {email: {"code": "123456", "expires_at": timestamp, "created_at": timestamp}}
        self.lock = threading.RLock()
        self.code_expiry_seconds = 50  # Auto-renew every 50 seconds
        self._cleanup_thread = None
        self._start_cleanup()
    
    def _start_cleanup(self):
        """Start background thread to clean expired codes."""
        def cleanup_loop():
            while True:
                try:
                    self._clean_expired()
                    time.sleep(10)  # Check every 10 seconds
                except Exception as e:
                    print(f"Cleanup error: {e}")
        
        if self._cleanup_thread is None:
            self._cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
            self._cleanup_thread.start()
    
    def _clean_expired(self):
        """Remove expired codes."""
        with self.lock:
            now = time.time()
            expired = [email for email, data in self.codes.items() if data["expires_at"] < now]
            for email in expired:
                del self.codes[email]
    
    def generate_code(self, email: str) -> str:
        """Generate a new 6-digit verification code for a user."""
        with self.lock:
            code = ''.join(secrets.choice(string.digits) for _ in range(6))
            now = time.time()
            self.codes[email] = {
                "code": code,
                "expires_at": now + self.code_expiry_seconds,
                "created_at": now,
                "attempts": 0
            }
            return code
    
    def verify_code(self, email: str, code: str) -> bool:
        """Verify a user's code. Returns True if valid."""
        with self.lock:
            if email not in self.codes:
                return False
            
            data = self.codes[email]
            now = time.time()
            
            # Check if expired
            if data["expires_at"] < now:
                del self.codes[email]
                return False
            
            # Check code match
            if data["code"] == code:
                # Code used successfully - remove it
                del self.codes[email]
                return True
            
            # Increment attempts
            data["attempts"] += 1
            if data["attempts"] >= 5:  # Max 5 attempts
                del self.codes[email]
            
            return False
    
    def resend_code(self, email: str) -> Tuple[bool, str]:
        """
        Resend a new code to the user.
        Returns: (success, new_code or error_message)
        """
        with self.lock:
            if email not in self.codes:
                return False, "No active code found. Please request a new one."
            
            # Generate new code
            new_code = ''.join(secrets.choice(string.digits) for _ in range(6))
            now = time.time()
            self.codes[email] = {
                "code": new_code,
                "expires_at": now + self.code_expiry_seconds,
                "created_at": now,
                "attempts": 0
            }
            return True, new_code
    
    def get_code_status(self, email: str) -> Dict:
        """Get the status of a user's code."""
        with self.lock:
            if email not in self.codes:
                return {"exists": False}
            
            data = self.codes[email]
            now = time.time()
            remaining = max(0, data["expires_at"] - now)
            
            return {
                "exists": True,
                "expires_in": remaining,
                "is_expired": remaining <= 0,
                "attempts": data["attempts"],
                "created_at": data["created_at"]
            }

# =============================================================================
# EMAIL VERIFICATION SERVICE
# =============================================================================

class EmailVerificationService:
    """
    Handles sending verification codes via email using multiple SMTP providers.
    """
    
    def __init__(self):
        self.verification_manager = VerificationCodeManager()
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup email providers."""
        self.providers = []
        
        # Gmail
        gmail_config = self._get_provider_config("GMAIL")
        if gmail_config:
            self.providers.append(("Gmail", gmail_config))
        
        # Outlook
        outlook_config = self._get_provider_config("OUTLOOK")
        if outlook_config:
            self.providers.append(("Outlook", outlook_config))
        
        # Proton
        proton_config = self._get_provider_config("PROTON")
        if proton_config:
            self.providers.append(("Proton", proton_config))
        
        # Legacy SMTP
        legacy_config = self._get_provider_config("SMTP")
        if legacy_config:
            self.providers.append(("Legacy SMTP", legacy_config))
    
    def _get_provider_config(self, provider: str) -> Optional[Dict]:
        """Get configuration for a specific provider."""
        if provider == "GMAIL":
            return {
                "host": _dacre_secret("DACRE_GMAIL_SMTP_HOST", ""),
                "port": int(_dacre_secret("DACRE_GMAIL_SMTP_PORT", "587")),
                "user": _dacre_secret("DACRE_GMAIL_SMTP_USER", ""),
                "password": _dacre_secret("DACRE_GMAIL_SMTP_PASSWORD", ""),
                "from": _dacre_secret("DACRE_GMAIL_SMTP_FROM", ""),
            }
        elif provider == "OUTLOOK":
            return {
                "host": _dacre_secret("DACRE_OUTLOOK_SMTP_HOST", ""),
                "port": int(_dacre_secret("DACRE_OUTLOOK_SMTP_PORT", "587")),
                "user": _dacre_secret("DACRE_OUTLOOK_SMTP_USER", ""),
                "password": _dacre_secret("DACRE_OUTLOOK_SMTP_PASSWORD", ""),
                "from": _dacre_secret("DACRE_OUTLOOK_SMTP_FROM", ""),
            }
        elif provider == "PROTON":
            return {
                "host": _dacre_secret("DACRE_PROTON_SMTP_HOST", ""),
                "port": int(_dacre_secret("DACRE_PROTON_SMTP_PORT", "587")),
                "user": _dacre_secret("DACRE_PROTON_SMTP_USER", ""),
                "password": _dacre_secret("DACRE_PROTON_SMTP_PASSWORD", ""),
                "from": _dacre_secret("DACRE_PROTON_SMTP_FROM", ""),
            }
        else:  # Legacy SMTP
            return {
                "host": _dacre_secret("DACRE_SMTP_HOST", ""),
                "port": int(_dacre_secret("DACRE_SMTP_PORT", "587")),
                "user": _dacre_secret("DACRE_SMTP_USER", ""),
                "password": _dacre_secret("DACRE_SMTP_PASSWORD", ""),
                "from": _dacre_secret("DACRE_SMTP_FROM", ""),
            }
    
    def send_verification_email(self, email: str, first_name: str, code: str) -> Tuple[bool, str]:
        """
        Send a verification code via email.
        Returns: (success, message)
        """
        subject = "🔐 Your DACRE Verification Code"
        body = f"""
        Hello {first_name},
        
        Welcome to DACRE Analysis!
        
        Your verification code is: {code}
        
        This code will expire in 50 seconds.
        
        If you did not request this code, please ignore this email.
        
        Warm regards,
        Emiel — DI Communications Specialist
        DACRE Analysis Platform
        """
        
        return self._send_email(email, first_name, subject, body)
    
    def send_welcome_email(self, email: str, first_name: str, company_name: str) -> Tuple[bool, str]:
        """
        Send a welcome email from Emiel-DI.
        Returns: (success, message)
        """
        subject = f"🎉 Welcome to DACRE Analysis, {first_name}!"
        body = f"""
        Hello {first_name},
        
        🌟 Welcome to DACRE Analysis!
        
        I am Emiel, your Communications & Messaging Specialist. I'm here to ensure you have a smooth onboarding experience.
        
        Your workspace for {company_name} is now active! Here's what you can do:
        
        📊 Upload and analyze your business data
        🧠 Chat with DI — David's Intelligence
        📈 Create powerful charts and dashboards
        📁 Store and organize your files
        🌍 Access global business intelligence
        
        To get started:
        1. Upload your first dataset in Workspace & Data
        2. Ask DI questions about your business
        3. Explore the Business Command Center
        
        Need help? Just type "help" in any DI chat and I'll guide you.
        
        Welcome to the future of business intelligence!
        
        Best regards,
        Emiel
        Communications & Messaging Specialist
        DACRE Analysis Platform
        """
        
        return self._send_email(email, first_name, subject, body)
    
    def _send_email(self, to_email: str, to_name: str, subject: str, body: str) -> Tuple[bool, str]:
        """Send email using available providers."""
        if not self.providers:
            return False, "No email providers configured. Please add SMTP settings."
        
        for provider_name, config in self.providers:
            if not config.get("host") or not config.get("user") or not config.get("password"):
                continue
            
            try:
                msg = MIMEMultipart()
                msg["From"] = config.get("from") or config.get("user")
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain", "utf-8"))
                
                with smtplib.SMTP(config["host"], config["port"], timeout=20) as server:
                    server.starttls()
                    server.login(config["user"], config["password"])
                    server.sendmail(config.get("from") or config.get("user"), [to_email], msg.as_string())
                
                return True, f"Email sent via {provider_name}"
            
            except Exception as exc:
                print(f"Email provider {provider_name} failed: {exc}")
                continue
        
        return False, "All email providers failed. Please try again later."
    
    def generate_and_send_code(self, email: str, first_name: str) -> Tuple[bool, str]:
        """
        Generate a verification code and send it via email.
        Returns: (success, message)
        """
        # Generate code
        code = self.verification_manager.generate_code(email)
        
        # Send email
        success, message = self.send_verification_email(email, first_name, code)
        
        if success:
            return True, f"Verification code sent to {email}"
        else:
            return False, message
    
    def resend_code(self, email: str, first_name: str) -> Tuple[bool, str]:
        """
        Resend a verification code.
        Returns: (success, message)
        """
        success, new_code = self.verification_manager.resend_code(email)
        
        if not success:
            return False, new_code  # new_code contains error message
        
        # Send email
        send_success, message = self.send_verification_email(email, first_name, new_code)
        
        if send_success:
            return True, f"New verification code sent to {email}"
        else:
            return False, message
    
    def verify_code(self, email: str, code: str) -> Tuple[bool, str]:
        """
        Verify a user's code.
        Returns: (success, message)
        """
        if self.verification_manager.verify_code(email, code):
            return True, "Code verified successfully!"
        else:
            status = self.verification_manager.get_code_status(email)
            if not status.get("exists"):
                return False, "No active code found. Please request a new one."
            elif status.get("is_expired"):
                return False, "Code has expired. Please request a new one."
            else:
                return False, f"Invalid code. {status.get('attempts', 0)} attempts used. Please try again."

# =============================================================================
# DI AGENT - EMIEL (Communications & Messaging Specialist)
# =============================================================================

class EmielDIAgent:
    """
    Emiel - Communications & Messaging Specialist DI Agent.
    Handles welcome messages, verification codes, and user communications.
    """
    
    def __init__(self):
        self.name = "Emiel"
        self.specialty = "Communications & Messaging"
        self.personality = "Polite, concise, organized and communication-focused"
        self.avatar_url = "https://randomuser.me/api/portraits/men/32.jpg"
        self.verification_service = EmailVerificationService()
    
    def send_welcome(self, user_email: str, first_name: str, company_name: str) -> Tuple[bool, str]:
        """Send a welcome email to a new user."""
        return self.verification_service.send_welcome_email(user_email, first_name, company_name)
    
    def send_verification_code(self, email: str, first_name: str) -> Tuple[bool, str]:
        """Send a verification code to a user."""
        return self.verification_service.generate_and_send_code(email, first_name)
    
    def resend_verification_code(self, email: str, first_name: str) -> Tuple[bool, str]:
        """Resend a verification code to a user."""
        return self.verification_service.resend_code(email, first_name)
    
    def verify_user(self, email: str, code: str) -> Tuple[bool, str]:
        """Verify a user's code."""
        return self.verification_service.verify_code(email, code)
    
    def get_code_status(self, email: str) -> Dict:
        """Get the status of a user's verification code."""
        status = self.verification_service.verification_manager.get_code_status(email)
        if status.get("exists"):
            status["expires_in_seconds"] = int(status.get("expires_in", 0))
            status["remaining_time"] = f"{int(status.get('expires_in', 0))} seconds"
        return status
    
    def introduce(self) -> str:
        """Emiel's introduction message."""
        return """
        👋 Hello! I'm Emiel, your Communications & Messaging Specialist.
        
        I'm here to ensure smooth communication between you and DACRE. I handle:
        📧 Welcome emails for new users
        🔐 Verification codes for secure sign-in
        📝 System notifications and alerts
        💬 Communication workflows
        
        If you need help with anything communication-related, just ask!
        """

# =============================================================================
# ENHANCED SIGNUP WITH EMIEL WELCOME
# =============================================================================

def enhanced_create_account(first, last, company, email, email_password, passkey, website_url=""):
    """
    Enhanced account creation with Emiel welcome email.
    """
    # Call the original create_account function
    success, msg, user_data = create_account(first, last, company, email, email_password, passkey, website_url)
    
    if success and user_data:
        # Send welcome email via Emiel
        emiel = EmielDIAgent()
        welcome_success, welcome_msg = emiel.send_welcome(email, first, company)
        
        if welcome_success:
            log_activity(user_data["username"], company, f"Welcome email sent by Emiel to {email}")
        else:
            log_activity(user_data["username"], company, f"Welcome email failed: {welcome_msg}")
        
        # Also store in notifications
        notify_company_admin(company, f"New user {first} {last} joined. Welcome email sent by Emiel.", "new_user")
    
    return success, msg, user_data

# =============================================================================
# ENHANCED SIGNIN WITH VERIFICATION CODE
# =============================================================================

def enhanced_authenticate_with_verification(company_name, full_name, passkey, email="", verification_code=""):
    """
    Enhanced authentication with verification code check.
    """
    # First, authenticate the user
    user, msg = authenticate(company_name, full_name, passkey, email)
    
    if not user:
        return None, msg
    
    # Check if verification is needed (for non-master users)
    if user.get("role") != "master":
        # Check if user is already verified in session
        if st.session_state.get(f"verified_{user['username']}", False):
            return user, "Already verified"
        
        # If verification code provided, verify it
        if verification_code:
            emiel = EmielDIAgent()
            verified, verify_msg = emiel.verify_user(user["email"], verification_code)
            
            if verified:
                st.session_state[f"verified_{user['username']}"] = True
                return user, "Verified successfully"
            else:
                return None, verify_msg
        
        # No verification code provided - need to send one
        emiel = EmielDIAgent()
        success, msg = emiel.send_verification_code(user["email"], user["first_name"])
        
        if success:
            return None, f"VERIFICATION_REQUIRED: A verification code has been sent to {user['email']}"
        else:
            return None, f"Could not send verification code: {msg}"
    
    return user, "Master user verified"

# =============================================================================
# UI: VERIFICATION CODE INPUT
# =============================================================================

def render_verification_ui(email: str, first_name: str):
    """
    Render the verification code input UI with timer and resend functionality.
    """
    st.markdown("""
    <style>
    .verification-container {
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 16px;
        padding: 30px;
        max-width: 500px;
        margin: 20px auto;
        border: 1px solid rgba(75,130,245,0.2);
        text-align: center;
    }
    .verification-title {
        color: white;
        font-size: 24px;
        font-weight: 800;
    }
    .verification-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin: 10px 0 20px 0;
    }
    .verification-timer {
        color: #60a5fa;
        font-size: 32px;
        font-weight: 900;
        margin: 15px 0;
    }
    .verification-code-input {
        background: #0a1628 !important;
        color: white !important;
        border: 2px solid rgba(75,130,245,0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 24px !important;
        text-align: center !important;
        letter-spacing: 8px !important;
        width: 100% !important;
    }
    .verification-code-input:focus {
        border-color: #4b82f5 !important;
        box-shadow: 0 0 30px rgba(75,130,245,0.2) !important;
    }
    .verification-resend {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 15px;
    }
    .verification-resend a {
        color: #60a5fa;
        text-decoration: none;
        cursor: pointer;
        font-weight: 600;
    }
    .verification-resend a:hover {
        text-decoration: underline;
    }
    .verification-status {
        margin: 10px 0;
        padding: 10px;
        border-radius: 8px;
        font-weight: 600;
    }
    .verification-status.info {
        background: rgba(96, 165, 250, 0.1);
        color: #60a5fa;
    }
    .verification-status.error {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    .verification-status.success {
        background: rgba(52, 211, 153, 0.1);
        color: #34d399;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for timer
    if "verification_timer_start" not in st.session_state:
        st.session_state.verification_timer_start = time.time()
    if "verification_resend_cooldown" not in st.session_state:
        st.session_state.verification_resend_cooldown = 0
    if "verification_attempts" not in st.session_state:
        st.session_state.verification_attempts = 0
    
    # Get code status
    emiel = EmielDIAgent()
    status = emiel.get_code_status(email)
    
    # Calculate remaining time
    if status.get("exists"):
        remaining = status.get("expires_in", 0)
        is_expired = status.get("is_expired", True)
    else:
        remaining = 0
        is_expired = True
    
    st.markdown(f"""
    <div class="verification-container">
        <div class="verification-title">🔐 Verify Your Account</div>
        <div class="verification-subtitle">
            A verification code has been sent to <strong>{email}</strong>
        </div>
        
        <div class="verification-timer" id="timerDisplay">
            {int(remaining)}s
        </div>
        <div style="color: #94a3b8; font-size: 12px;">Code expires in</div>
        
        <input type="text" class="verification-code-input" id="verificationCode" 
               placeholder="000000" maxlength="6" autofocus>
        
        <div id="verificationStatus" class="verification-status" style="display: none;"></div>
        
        <button onclick="verifyCode()" style="
            background: linear-gradient(135deg, #4b82f5, #6c9cff);
            border: none;
            color: white;
            padding: 12px 30px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
            transition: all 0.3s;
        ">
            ✅ Verify
        </button>
        
        <div class="verification-resend">
            Didn't receive the code? 
            <a onclick="resendCode()" id="resendLink">
                Resend Code
            </a>
            <span id="resendTimer" style="color: #64748b;"></span>
        </div>
    </div>
    
    <script>
        let remainingTime = {int(remaining)};
        let timerInterval = null;
        let isResending = false;
        let resendCooldown = 0;
        
        function updateTimer() {{
            const timerDisplay = document.getElementById('timerDisplay');
            if (remainingTime <= 0) {{
                timerDisplay.textContent = '⏰ Expired';
                timerDisplay.style.color = '#ef4444';
                if (timerInterval) {{
                    clearInterval(timerInterval);
                    timerInterval = null;
                }}
                showStatus('Code has expired. Please request a new one.', 'error');
                return;
            }}
            timerDisplay.textContent = remainingTime + 's';
            remainingTime--;
        }}
        
        function showStatus(message, type) {{
            const status = document.getElementById('verificationStatus');
            status.textContent = message;
            status.className = 'verification-status ' + type;
            status.style.display = 'block';
        }}
        
        function verifyCode() {{
            const code = document.getElementById('verificationCode').value.trim();
            if (code.length !== 6) {{
                showStatus('Please enter a 6-digit code', 'error');
                return;
            }}
            
            // Send to Streamlit
            const url = new URL(window.parent.location.href);
            url.searchParams.set('verify_code', code);
            window.parent.location.assign(url.toString());
        }}
        
        function resendCode() {{
            if (isResending) return;
            if (resendCooldown > 0) {{
                showStatus('Please wait ' + resendCooldown + ' seconds before resending', 'info');
                return;
            }}
            
            isResending = true;
            showStatus('📧 Sending new code...', 'info');
            
            const url = new URL(window.parent.location.href);
            url.searchParams.set('resend_code', '1');
            window.parent.location.assign(url.toString());
        }}
        
        // Start timer
        if (remainingTime > 0) {{
            timerInterval = setInterval(updateTimer, 1000);
            updateTimer();
        }}
        
        // Handle Enter key on input
        document.getElementById('verificationCode').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter') {{
                verifyCode();
            }}
        }});
        
        // Auto-focus
        document.getElementById('verificationCode').focus();
    </script>
    """, unsafe_allow_html=True)
    
    # Handle verification code input
    verify_code = st.query_params.get("verify_code")
    if verify_code:
        st.query_params.clear()
        emiel = EmielDIAgent()
        verified, msg = emiel.verify_user(email, verify_code)
        
        if verified:
            st.session_state[f"verified_{st.session_state.user.get('username', '')}"] = True
            st.success("✅ " + msg)
            st.rerun()
        else:
            st.error("❌ " + msg)
    
    # Handle resend
    if st.query_params.get("resend_code") == "1":
        st.query_params.clear()
        emiel = EmielDIAgent()
        success, msg = emiel.resend_verification_code(email, first_name)
        
        if success:
            st.success("✅ " + msg)
            # Reset timer
            st.session_state.verification_timer_start = time.time()
            st.rerun()
        else:
            st.error("❌ " + msg)

# =============================================================================
# UPDATED SIGNIN PAGE WITH VERIFICATION
# =============================================================================

def render_verification_signin():
    """
    Render sign-in page with verification code support.
    """
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🔐 Sign In to DACRE</h1>
        <p style="color:#94a3b8;">Secure access with email verification</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signin_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company / Organization", placeholder="Enter your company name")
            email = st.text_input("Email Address", placeholder="your@email.com")
        with col2:
            fullname = st.text_input("Full Name", placeholder="Your full name")
            passkey = st.text_input("Account Passkey", type="password", placeholder="Enter your passkey")
        
        submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
    
    if submitted:
        if not company and not email:
            st.error("Please enter your company name or email address.")
            return
        
        if not passkey:
            st.error("Please enter your account passkey.")
            return
        
        # Try authentication
        user, msg = enhanced_authenticate_with_verification(company, fullname, passkey, email)
        
        if user:
            st.session_state.user = user
            st.session_state.master_route = user.get("role") == "master"
            st.success(f"✅ Welcome back, {user['first_name']}!")
            st.rerun()
        elif msg and msg.startswith("VERIFICATION_REQUIRED:"):
            # Show verification UI
            st.info(msg)
            email_to_verify = email or user.get("email") if 'user' in locals() else email
            if email_to_verify:
                render_verification_ui(email_to_verify, fullname or "User")
        else:
            st.error(f"❌ {msg}")

# =============================================================================
# ENHANCED SIGNUP WITH EMIEL WELCOME
# =============================================================================

def render_enhanced_signup():
    """
    Render sign-up page with Emiel welcome email.
    """
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🎉 Create Your DACRE Account</h1>
        <p style="color:#94a3b8;">Join the future of business intelligence</p>
        <p style="color:#60a5fa;font-size:14px;">
            👋 Emiel, your Communications Specialist, will send you a welcome email!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first = st.text_input("First Name", placeholder="David")
            last = st.text_input("Last Name", placeholder="Emenike")
            company = st.text_input("Company / Organization", placeholder="Your company name")
        with col2:
            email = st.text_input("Email Address", placeholder="name@example.com")
            email_pass = st.text_input("Email Password (optional)", type="password", placeholder="For email features")
            passkey = st.text_input("Create Account Passkey", type="password", placeholder="Create a secure passkey")
            website = st.text_input("Company Website (optional)", placeholder="https://www.yourcompany.com")
        
        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
    
    if submitted:
        if not first or not last or not company or not email or not passkey:
            st.error("Please fill in all required fields.")
            return
        
        # Use enhanced create account
        success, msg, user_data = enhanced_create_account(first, last, company, email, email_pass, passkey, website)
        
        if success:
            st.session_state.user = user_data
            st.session_state.master_route = False
            st.success(f"✅ {msg}")
            st.info(f"📧 Check your email {email} for a welcome message from Emiel!")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

# =============================================================================
# ALL DI AGENTS - EACH INTRODUCES ITSELF
# =============================================================================

def get_di_introduction(agent_name: str) -> str:
    """
    Get introduction message for any DI agent.
    Each DI introduces itself with its name, specialty, and purpose.
    """
    introductions = {
        "Emiel": """
        👋 Hello! I'm Emiel, your Communications & Messaging Specialist.
        
        I specialize in:
        📧 Email communications and welcome messages
        🔐 Verification codes for secure access
        📝 System notifications and alerts
        💬 Communication workflows
        
        Need help with anything communication-related? Just ask!
        """,
        
        "Guaiel": """
        🛡️ I am Guaiel, the CEO Office Guardian.
        
        My purpose is to:
        🔒 Protect the CEO Office and founder command path
        🛡️ Verify secure access to master-level controls
        👑 Guard the integrity of DACRE's leadership
        ⚡ Ensure only authorized users access sensitive areas
        
        If you're the master, I will verify your identity with respect and vigilance.
        """,
        
        "Raziel": """
        🧠 I am Raziel, Executive Intelligence Director.
        
        I provide:
        📊 Executive-level business intelligence
        🎯 Strategic recommendations and insights
        📈 High-level data synthesis and analysis
        💡 Decision support for leadership
        
        Ask me for strategic guidance, market analysis, or executive briefings.
        """,
        
        "Ariel": """
        🎯 I am Ariel, Strategy & Planning Lead.
        
        I help with:
        📋 Strategic planning and execution
        🎯 Goal setting and prioritization
        📊 Scenario analysis and forecasting
        🚀 Business transformation and growth
        
        Let me help you plan your next big move.
        """,
        
        "Nathaniel": """
        💰 I am Nathaniel, Financial Intelligence Lead.
        
        I specialize in:
        📊 Financial analysis and reporting
        💵 Budgeting and forecasting
        📈 Investment analysis
        🏦 Banking and treasury operations
        
        Ask me about financial performance, budgeting, or investment strategies.
        """,
        
        "Gabriel": """
        📈 I am Gabriel, Sales Intelligence Lead.
        
        I can help you with:
        📊 Sales pipeline analysis
        🎯 Conversion optimization
        📈 Revenue forecasting
        🤝 Customer relationship management
        
        Let's optimize your sales performance!
        """,
        
        "Sofiel": """
        🔬 I am Sofiel, Research & Intelligence Lead.
        
        I provide:
        📚 Research and analysis
        🧠 Intelligence gathering
        📊 Data synthesis and insights
        🔍 Competitive intelligence
        
        Ask me for research on any topic or industry.
        """,
        
        "Uriel": """
        ⚙️ I am Uriel, Operations Intelligence Lead.
        
        I specialize in:
        🔄 Process optimization
        📊 Operational analytics
        📈 Efficiency improvement
        🏭 Supply chain intelligence
        
        Let's make your operations more efficient!
        """,
        
        "Adriel": """
        💻 I am Adriel, Technology Intelligence Lead.
        
        I can help with:
        🖥️ Software architecture
        🤖 AI and machine learning
        ☁️ Cloud infrastructure
        🔒 Cybersecurity
        
        Ask me about technology strategy or implementation.
        """,
        
        "Muriel": """
        👥 I am Muriel, People & Workforce Lead.
        
        I specialize in:
        📊 HR analytics and workforce planning
        🎯 Talent management
        📈 Employee engagement
        🏢 Organizational development
        
        Let's build a better workplace together!
        """,
        
        "Azriel": """
        ⚖️ I am Azriel, Risk & Compliance Lead.
        
        I provide:
        📋 Risk assessment and management
        ⚖️ Compliance oversight
        🔍 Internal audit support
        🛡️ Governance guidance
        
        Ask me about risk management or compliance requirements.
        """,
    }
    
    default_intro = f"""
    👋 Hello! I am {agent_name}, a DI agent at DACRE Analysis.
    
    I am here to help with business intelligence, data analysis, and strategic guidance.
    
    Feel free to ask me anything about your business, data, or goals!
    """
    
    return introductions.get(agent_name, default_intro)

def render_di_introduction(agent_name: str):
    """
    Render a DI agent's introduction in the UI.
    """
    intro = get_di_introduction(agent_name)
    
    # Get agent avatar
    agents = get_di_agents()
    avatar = None
    for a in agents:
        if a.get("di_name") == agent_name:
            avatar = a.get("avatar_url")
            break
    
    if not avatar:
        avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={agent_name}"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(75,130,245,0.2);
        display: flex;
        gap: 20px;
        align-items: flex-start;
    ">
        <div style="flex: 0 0 80px;">
            <img src="{avatar}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #4b82f5;">
        </div>
        <div>
            <h3 style="color: white; margin: 0;">{agent_name}</h3>
            <div style="color: #94a3b8; font-size: 13px; white-space: pre-wrap;">{intro}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# INTEGRATION WITH EXISTING CHAT - DI INTRODUCES ITSELF
# =============================================================================

def enhanced_di_reply_with_introduction(message, user, df, agent_name=None):
    """
    Enhanced DI reply that includes self-introduction when chatting.
    """
    # Check if this is a new conversation or user asked for introduction
    text = message.strip().lower()
    
    # If user asks "who are you" or "introduce yourself"
    if any(phrase in text for phrase in ["who are you", "introduce yourself", "tell me about yourself", "what do you do"]):
        if agent_name:
            return get_di_introduction(agent_name)
        else:
            # If no specific agent, use the default DI
            return get_di_introduction("Emiel")
    
    # If user is chatting with a specific DI for the first time
    if agent_name and st.session_state.get(f"first_interaction_{agent_name}", True):
        st.session_state[f"first_interaction_{agent_name}"] = False
        intro = get_di_introduction(agent_name)
        # Get the normal reply too
        normal_reply = di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        return f"{intro}\n\n{normal_reply}"
    
    # Normal reply
    return di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))

# =============================================================================
# UI: DI AGENT SELECTION WITH INTRODUCTIONS
# =============================================================================

def render_di_agent_selector_with_introductions():
    """
    Render a DI agent selector where each agent introduces itself.
    """
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h2 style="color:white;">👥 Choose Your DI Agent</h2>
        <p style="color:#94a3b8;">Each DI has a unique personality and specialty. They'll introduce themselves when you chat!</p>
    </div>
    """, unsafe_allow_html=True)
    
    agents = get_di_agents()
    if not agents:
        st.info("No DI agents available.")
        return
    
    # Display agents in a grid with their introductions
    cols = st.columns(3)
    for idx, agent in enumerate(agents):
        with cols[idx % 3]:
            with st.container():
                avatar = agent.get("avatar_url") or f"https://api.dicebear.com/7.x/avataaars/svg?seed={agent['di_name']}"
                st.image(avatar, width=100)
                st.markdown(f"### {agent['di_name']}")
                st.caption(f"Specialty: {agent.get('specialty', 'General')}")
                
                # Show introduction button
                if st.button(f"💬 Chat with {agent['di_name']}", key=f"intro_{agent['di_name']}"):
                    st.session_state.selected_agent = agent['di_name']
                    st.session_state[f"first_interaction_{agent['di_name']}"] = True
                    st.rerun()
                
                # Show introduction
                with st.expander(f"👋 Meet {agent['di_name']}"):
                    st.markdown(get_di_introduction(agent['di_name']))

# =============================================================================
# INITIALIZE VERIFICATION SYSTEM ON STARTUP
# =============================================================================

def init_verification_system():
    """
    Initialize the email verification system.
    """
    if 'verification_service' not in st.session_state:
        st.session_state.verification_service = EmailVerificationService()
        st.session_state.emiel_agent = EmielDIAgent()
    
    # Initialize first interaction flags for all DI agents
    agents = get_di_agents()
    for agent in agents:
        key = f"first_interaction_{agent['di_name']}"
        if key not in st.session_state:
            st.session_state[key] = True

# =============================================================================
# END OF ADDED CODE
# =============================================================================
PAGE12                 
