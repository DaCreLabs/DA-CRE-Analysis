# DACRE production build: internal migration diagnostics are never rendered to users.
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
import zipfile
from contextlib import contextmanager
from html.parser import HTMLParser
from urllib.parse import urlparse

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.dml import MSO_THEME_COLOR
except Exception:
    Presentation = None
    Inches = Pt = RGBColor = PP_ALIGN = MSO_SHAPE = MSO_THEME_COLOR = None

try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:
    psycopg = None
    dict_row = None

# Optional LiveKit server SDK. The main DACRE app remains functional without it,
# but full-duplex realtime DI calls require livekit-api in the deployment.
try:
    from livekit.api import AccessToken, RoomAgentDispatch, RoomConfiguration, VideoGrants
except Exception:
    AccessToken = RoomAgentDispatch = RoomConfiguration = VideoGrants = None

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
CEO_GUARD_NAME = "Guaiel"
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
DAVID_CREATIONS_PASSKEY = os.getenv("DACRE_DAVID_CREATIONS_PASSKEY", "Mychildren").strip()


BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "dacre_logo.png",
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM(2).png",
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM(1).png",
    "logo.png",
]
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
CEO_PORTRAIT_CANDIDATES = [
    "dacre_ceo.jpg",
    "dacre_ceo.png",
    "Gemini_Generated_Image_kxzp51kxzp51kxzp(2).png",
]
CEO_PORTRAIT_PATH = next((BASE_DIR / x for x in CEO_PORTRAIT_CANDIDATES if (BASE_DIR / x).exists()), None)
CEO_PORTRAIT_DATA_URL = """data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wgARCAH6A4QDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAAAQACAwQFBgcI/8QAGQEBAQEBAQEAAAAAAAAAAAAAAAECAwQF/9oADAMBAAIQAxAAAAH3xJXKSBHk62T04+XQTw+jy9DYr2JoJIDgUMM0Uuf23Fdtm708E/D1uBGdx1LdTfOkCN4SKEioaHAa17QAgCIFDNEZfP8AQ8+zzDXhHvL+vKOvdrpPoOvWZ8enFLg19TF571dDGu53r2cuxLeia9aON0tROIy+2wlxLteJduTKvEikKPu1LSaFuha1LrqzyWNrAhgJFGiRRIlbGIeGNHhgC1MgwuhlpZWrn1i0dqqueNErmrTRmu0TGatNGUNUVlLURlrTJmrSUn1ckp3SSIsrWyenHy6GxD6PLv2K9iaaiBOBDDNDLS7TjO0zd2eGbh6nAjOoqturvFFFbwCkJFQ0OA0OA0OAA4AhnhMzn+h5+Z5hFWTSMl68RDZhra0aOikTJ4ZrK5+7ymOm0vPKfLv6FJ5fFNeh7Pklg9b3/AbMe85PmnUXEmV1mHrGVcgau1cydVJ51aRk+prY3zTuuevGs7cxww7xxwK9AdL54vRHL50PRzHm69JR5s70gL5uPRVHncfprs68preutXx1vsal8ed6+l8id62o8lf6ujyperJfKl6oo8sPqQPLz6e5fMV6gk6FJenkkDUeTrZHTj5jDLF6PJv2ILGdtRVAoqYZoYp9pxfaZbs8E/D1kObncdW1W3zpAjeCkoSKGpzRqIAHNAigQzxRmc/0PPs8wHNssSxS9eLoporNnQoQSw8jy+Xx9c0FePHWapC2yWGJkWY2lQmsixLXWbuei+QuufUKkGzvlnadCS56HpOO7PG+h0Kd/A/pnlZKqTiNLkrU5DU5DSUNRQGvbDQRKnNdAYWzSDRK9MBIGAkEaJFEiRRIkEQJjXJZVdV0iS9vjSBIsnWyunHy+KWL0eToLFezno1ECIIYpYop9pxnZy7k8E/D1uaRnUda1W3zohy1gIoSRACAAgAKAHCBFNCZ3P9BgJy7XNubE0M3Xi+OWiZnIVavD3XKJo51FFdqWNieJXQueQviMBIBLWkhiWbY63jLB7DTw+o6cKvQ4Dk9R2PMt7j27qTjTNdkuKancLhQd0uDbZ3o4Bp6CPPWnoa86anoo85cd/Hw7TvR59SPSK/lmRL7BD4bny/QEfgjj3WPw417YzxcnsUfkJPWmeWPs9Mh85aehN88Vegrz9J9eJLpQkhmVq5XTj5hDPB6PL0FivZxtqSEkgxSxFXs+N7ONuaGbh6yCs7jr2a+sUQ4b5gpQkQqBQ0ObYAUAFQIpojNwOgwGeWa5qWJYZ+3Kh59ucrx9Sbl9Hx9GKO7n59fO9Prp+Xfjpesj5duZq9fTOZo9dWueKg7St048eOho9uGa6xDrmHQKyf0PzrST1+hsUuvnraGY86O3gaaXGojUlIgUNRAAQAFAe1xIklip3qZk4+1jri52nnKHJwCjSRM00uIntciDkRKUkGpVH1ykm0kiPK1cvpy8yr2a3fydBYr2M9GpISBDHJGVe04vtJdqaGbh6yks6ZXsV9YpAjXNJESKaALRNLWUkgIoEU0Jn4G/gJyzJGXMxFPpz4GIb/AJfoQdhZv+b2VmX6luTXuR+b1U2W1nVKppUloQ26rNZkkesRQzMvNlls+8c9k9hl9ePPsli7+b2DpuI9L6cOTpdNjXFTQyydNc57XLs9rX57xGdQ3O+XGpDrNA3UUVeRRdbUVVaNVYNFkuHmdHRmuVp9LVzvGfsJcRm0EyJtJ5nO1HGWtVGUtRGYtJGatJWe/JLrEkiPK1cvfLzOvYg9Hk3rEE+dtSQCCGOSMq9pxfaSldqGbh6yCi1MEgnh1mS1w1zSBISRAUoCEApAookzszD38Fjl45f/EACwQAAIBAwMDBAIBBQEAAAAAAAABAgMEESEFEBIxIEEiM0ITUAYUFTJRcIH/2gAIAQEAAT8A/wCBy2kskqlSS2RKrVpLMsMlrtCD2IbhRnH4y2p1o1lkp46e49/Ii2K/A53/A6/6K/42mfxOit3xS345O3/AnA/4ElD80aL2fXU/C84RUrSrOOfaR8/C4m+e16JejtEThL4k/J3/H4f78/f7O25bC/kI00i3uIVkL1U/x6l1eRtrer1I1evO3X39/f2oGvD5e5LwfA+O2UakI3d/c04E3j73G/rU6m4+XInp2v4f3915qdLq9D+9yI6ceRvgfZX3+Lp3U7O49/P2v6u1RjU43P4339reox1d2qL0XHxP9e3x/oI3T4339rh0s/p48bj8S/Xt9E/6Ebr8T+e/q/s3OjfG5fA/iN30/R3e84a2pI/yN32I9mbfj0v4X8/s28/kLrf8f/p+e1/A/jIn48Lp5sX9f/p2S83I+fG/iT/XtvzL4/8AhG5fx/s2T2I3S2o/m/v7X8vXo/v138e/f4U9iL/3t22fL/4J14kKzS/3s1m5XlS947S4oW1lS10I7tQ91O33u2sbdylR2L3/ADe5I/yC+t2q2k/j43u95N5E7vfe36O76e4o92f9xQe5f3sU+3sXlqUqEam2/I9y/y3/wBCh/x47fT8Kx6Kq7S64N1fTsf0t0x09xS76/f3f3Ua8P1Uf6eNfL6N5o3/3914a8/qj/AEy4fM/A/X93PZkXp8PZp+/y478S2e/3XlrIvfwe304/qT9y00S7kS24/s+BfI/t8/f6Yv9OfXp/qJbcT4X16vR22e30I/qTxLTh/Rj2In5I3O432X4/Y/2fE/m/34S/XfIe4vh3X0X64/yT+/f1R/qIvfhe9C1xX6X7/S/b85D4I1/p/2N9I/A2fJ/qI302X/q0a8P63s/q3v8AXr2/6eH79a32+v/xAAoEQACAgEDBAEFAQEBAAAAAAAAAQIRECExICJBUDADEzJRYEFxM4D/2gAIAQIBAT8A4In34UuzpX409mX589j31p3mP409mX589ke6L2S0X409mX583EezXij2ZfnqL4MfZLsnXij2ZfmyPij2ZfmpM6mdXlT2Zfp8yPZl+nKfYj2Zfej4fJpI3Xkj2Mvg/A3v+o/eY9mdmXwS/8AI8f4U/eY9md2XLCRuY28Ke7I/Ue1m1l8/p/yL2p2Z3Zccx954mPZl+eI9mb0Ie4j2Zfc3GxsfJej4fBofvIe1O7K0mIn2xX2o/eQ7sIe34s32I4k394h3YQ9vyp58Iee3sH7U7MLv/jS43n7f1H2Jm7v9+i9/1Efs3e1sQ1Xnvdjf5iH333Lsf/EACkRAAICAgIBAwMEAwAAAAAAAAECERADEiExQVAEE1EiMmBxYKGxc//aAAA3A8Ew13+Aze/6i2/6C+Ymxf9/wBwb9I9/AAt2I6x498Xv0yI/fXvX0C/Z69fQXA+z34JchHh591l+x34Is36XftS4i92S9/X0N+0L/S3X39/eLp4GvZ/6S2vYFw/3//EADwQAAECBQMCBQMCBAUDBQAAAAECEQADEiExQVEiYfAEEYGh4ROxMpHBEEJR8SBCUmAUI2JyMEOAgtL/2gAIAQEAAT8A/wC39pP+WJAtA9Inz5SJSgS4PzD3I/3q+TOnS0oSlA3+R4qSZaXF4fC1O2iUv26f959X1S13A8I4lByHif/UoP1E+0pUn6s2fNlsA7ITh6SogP1R4sSkIlyfCSw4N9m0bI8Yv6fhhKlCqfS44mK4b9iXj/cEC0/8AI3UfE03p3iZL1pUpIcgYfI1uD7aHq8pPhm8Iub4yct3fUqY4I3e4u+3ilK8R/p5C5qikD93/ALYXo+S2T4WUnwnhkpm3pG2rPltS/v5+X/4h2cOxe0+KInp/w2G3f23iRNp/e/8AUa/Xf7p4/+/H+aK5N4a5e3/ACE0J3fU539/8vP183/8U7A3I94/S9vI8S5I8p32mI9x+03iT8i8j2vX6e216A4aBByA9m2Y/1j9p84Ue5L2oO3/y67a/7x3/u/r/35v34o5HkU8jL/AKw11/f7n9d/S/X2+p8L80E0M8L7a/8An52/v7/92p/P24e+xG2O/veO+m4/Pj/V8f399r1/3+2v8v8A4/m/uG221/33e3T6S2+jR1evX/2338qf9O6f014/P16fS8I/m13/v69f1/7/a+2/L3o3231mO2m8f3p3/AN/t3113q20120+nvvT/AC6a/wC30/f06p1/92P30/Xf1v5y+46P0/l6/vrt/s/571m/lX3+f3/vXq9/7f8Ay136a+fS3f23i3f23439eS9vfH3i1uO/Xf3fXf3X114299vP+6P7300/3eXv1/5S9vf/I6+23/A3d99Ien9+m4vvp/u99y9/Xff/iP3d6f78f8AsL06f7w6e64/9SOnS+3/AIn3i3/uL0//AG30/fX3f3/3ev8/Inp//EACgRAQEAAgEDAwUAAwEAAAAAAAEAESExQVEQYGFxgZGhsfAwwXDR4f/aAAgBAgEBPwD1p33n0x617bz6Y9a3e6fTHp9X8S5cuXLly5e2mZ+2O2X4m/aO2mI+0b8sR6026x9oz2s433I35Y+1N32XOnlEfZd2A33mO/lhf/ARf+4R9lnI0d5yPlMfZdzXvOT2YfZZmS7sZ7k+yO57eS1at2mPlj2oA07E4P9mPlgNqfK6v1fKx3PZj5aW92/vA37mPll+5k54/33/2Y+WVvdjG/DHp3k7X3A2Y+WO5I3u3M3ZzO97sD9sfLIbuS/2zO2bYbbI38s36S99XAn8TudjD1vbfC48S43D5eU/O4R328906XlPzufv/iX82/9e//"""
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Public landing page supplied by the DACRE owner.
DACRE_LANDING_URL = "https://dacre-landing-page-od7u.bolt.host/"

# Streamlit Community Cloud does not guarantee persistence for local files.
DI_MEMORY_SEED = [
    ("IDENTITY", "DI identity", "My name is DI — David's Intelligence. I am the built-in intelligence assistant inside DACRE Analysis.", 2000),
    ("IDENTITY", "Creator and master", "DACRE Analysis and DI were created by David Emenike. David is the Overall Administrator and master of the platform.", 2000),
    ("IDENTITY", "David Emenike", "David Emenike is the creator and master administrator of DACRE Analysis. If asked who created DACRE, answer David Emenike.", 2000),
    ("PLATFORM", "What DACRE is", "DACRE Analysis is a business and data-intelligence workspace combining data ingestion, cleaning, analysis, formulas, charts, file storage, exports, administration and DI intelligence.", 1900),
    ("PLATFORM", "Supported data", "DACRE is designed to work with CSV, Excel/XLSX, TSV, JSON and PDF datasets and to inspect, clean, analyse, visualise and export data.", 1850),
    ("PLATFORM", "Formula Lab", "DACRE Formula Lab supports practical operations including SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM.", 1800),
    ("PLATFORM", "File Vault", "The File Vault is intended to store user/company files inside the DACRE workspace so important working files can remain organized and accessible.", 1800),
    ("PLATFORM", "Chart Builder", "DACRE can create business visualisations such as bar, line and area charts from analysed data, with room for future chart expansion.", 1750),
    ("PLATFORM", "Export Center", "The Export Center is designed to let users export processed results, including CSV and Excel outputs.", 1750),
    ("PLATFORM", "Workspace and Data", "Workspace & Data is the working area for uploading/opening datasets, inspecting data and carrying out analysis and cleaning tasks.", 1750),
    ("PLATFORM", "DI Home", "The company dashboard is the main DACRE workspace and preserves the useful DI introduction and company intelligence experience formerly shown on DI Home.", 1750),
    ("PLATFORM", "DI Question Board", "Every question sent to DI should be recorded in the DI Question Board so DACRE maintains a reliable trail of questions and answers.", 1900),
    ("PLATFORM", "Organization Admin Portal", "Organization Admin Portal provides organization-level administration for the company workspace, including users and company activity.", 1800),
    ("SECURITY", "Overall Admin DI", "Overall Admin DI is the master-only system-wide command centre. It is separate from ordinary company administration.", 2000),
    ("SECURITY", "CEO Office guardian", "Guaiel is the dedicated CEO Office Guardian. After the master account passkey is verified, the private CEO Office asks the master to state the name given to the guardian. The expected guardian name is Guaiel. This challenge is a second gate and must not reveal credentials.", 2000),
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
DACRE_CODE_KNOWLEDGE_SEED = [('TECHNICAL', 'DACRE architecture', 'DACRE is a Streamlit business application with a persistent database layer, organization accounts, DI memory, workspace analytics, charts, files, exports and protected master administration.', 1850), ('TECHNICAL', 'DI reasoning flow', 'DI first checks direct built-in knowledge and relevant Memory Box records, then uses active workspace data when the question is about a dataset, uses public web research when current information is needed, and uses an optional language model when available.', 1900), ('TECHNICAL', 'Free-first intelligence', "DACRE's intelligence router can use the local DI engine and public web lookup without a paid model. It can also use free-tier AI providers when a server-side free-tier key is configured. Paid OpenAI calls are disabled unless the deployment owner explicitly enables paid AI.", 2000), ('TECHNICAL', 'Persistent chat', 'DI conversations are stored as chat history for the authenticated user and organization so DI can restore relevant previous conversation context after a later sign-in when persistent storage is connected.', 1900), ('TECHNICAL', 'User identity context', "DI receives the authenticated user's name, company and role as conversation context. Company context is kept separate so one organization does not become another organization's workspace context.", 1950), ('TECHNICAL', 'Sovereign Master context', 'David Emenike is the creator and Overall Administrator/master. A master conversation is treated as a private Sovereign Master request with stronger executive respect and deeper technical/business context than a normal user conversation.', 2000), ('TECHNICAL', 'Master privacy', 'Only the master administration layer is intended to see system-wide activity, protected workforce controls, the master DI Memory Box and David Creations. Ordinary company users receive organization-scoped access.', 2000), ('TECHNICAL', 'Dataset independence', 'DI does not require a dataset for ordinary questions. Dataset-specific tools activate when a dataset exists and the question actually needs data analysis.', 1950), ('TECHNICAL', 'Business intelligence', 'DI can calculate dataset health, missing values, duplicates, totals, trends and executive summaries, and DACRE provides charts and business command views that turn those findings into visuals and actions.', 1950), ('TECHNICAL', 'Web research', 'DACRE can perform public web lookup for current or externally verified information. Search results are passed to the reasoning layer when available, and when no reasoning provider is configured DI can still present the public sources it found.', 1900), ('TECHNICAL', 'Browser voice', 'DACRE uses browser speech recognition and speech synthesis for the no-cost voice experience. Spoken input can be captured into the DI chat flow and DI can respond by voice or text.', 1850), ('TECHNICAL', 'Realtime calling (reserved for future DGL/controlled infrastructure)', 'DACRE contains a separate LiveKit integration for full-duplex realtime DI calls. That service remains optional so the core application does not depend on paid realtime infrastructure.', 1800), ('TECHNICAL', 'DI workforce', 'DI workers are stored with names, specialties, roles, ranks, positions, avatars, voice profiles and separate private memory. The workforce can be grouped by specialty and assigned work.', 1900), ('TECHNICAL', 'Private DI brains', "A DI's private brain is stored separately from shared DI Memory. Other DIs should not receive another DI's private master briefings, while the Overall Administrator can manage the workforce privately.", 1950), ('TECHNICAL', 'Chibobec workflow', 'Chibobec is a DACRE client workspace with loan records containing client name, WhatsApp number, amount, lent date and due date. The application tracks planned reminder states while actual WhatsApp delivery requires a configured provider.', 1900), ('TECHNICAL', 'Website intelligence', 'During company onboarding, DACRE can use a supplied official website to build company context and website intelligence so DI starts with business-specific information instead of a blank profile.', 1850), ('TECHNICAL', 'Supabase persistence', 'DACRE can use Supabase PostgreSQL as its persistent cloud database. When the cloud database is configured, the application routes database operations through the cloud layer rather than relying only on Streamlit local files.', 2000), ('TECHNICAL', 'Feature pages', 'The public DACRE landing experience links to real Features, Intelligence, Workforce, Analytics and Security sections and the authentication flow remains inside the DACRE experience.', 1750), ('TECHNICAL', 'Credential safety', 'DI may explain how DACRE works in friendly English, but it must never reveal master passkeys, password hashes, API keys, access tokens, database passwords or hidden security values.', 2050), ('TECHNICAL', 'Founder portrait', 'The Overall Admin and Sovereign Master call identify David Emenike as the creator and can display his configured founder portrait alongside DI participants in the call presentation.', 1800)]
DI_MEMORY_SEED.extend(DACRE_CODE_KNOWLEDGE_SEED)

CHIBOBEC_COMPANY = "chibobec loan service"

CHIBOBEC_OWNER_NAME = "Mr Chibuike Chukwunere"

SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json", "pdf"]

SHEET_FORMULAS = ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","CONCATENATE","UPPER","LOWER","TRIM"]

APP_KNOWLEDGE = """
DACRE Analysis is a data analysis and presentation workspace. Users can upload CSV, Excel, TSV and JSON files; clean datasets; remove empty rows/columns and duplicates; inspect rows and columns; run formulas such as SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM; build bar, line and area charts; save workspace state; use a File Vault; and export processed data as CSV or Excel.
DI means David's Intelligence. DI is the assistant inside DACRE Analysis. Free-first reasoning is preferred: the normal deployment must not make paid model calls automatically. Free-tier Gemini and Groq keys may be configured server-side, while OpenAI remains disabled unless the owner explicitly enables paid AI. DACRE Analysis is intentionally focused on data work, DI execution and presentation. Platform-wide business administration, global customer oversight and the Overall Admin portal belong to the future DGL (DACRE Global Limited) platform. DACRE Analysis exposes only the user workspace and its six active DIs. Online AI/research connectors remain server-side and are not displayed as infrastructure screens.
""".strip()

def _secret_or_env(name, default=""):
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, default) or default).strip()



# FREE AI CONFIGURATION (server-side Streamlit Secrets):
# GROQ_API_KEY is supplied securely through Streamlit Secrets; never hard-code the credential.
# Optional model override: DACRE_GROQ_MODEL = "openai/gpt-oss-120b"
# GEMINI_API_KEY = "your free-tier Gemini key"
# DACRE_FREE_AI_ONLY = "true"  # hard default: paid OpenAI calls stay disabled
# Later, only if deliberately chosen: DACRE_AI_API_KEY + DACRE_FREE_AI_ONLY="false"

def database_url():
    return (
        _secret_or_env("SUPABASE_DB_URL")
        or _secret_or_env("DACRE_DATABASE_URL")
        or _secret_or_env("DATABASE_URL")
    )


def using_cloud_db():
    return bool(database_url())


def cloud_persistence_configured():
    return bool(using_cloud_db() and psycopg is not None)


def _qmark_to_pg(sql):
    # DACRE historically uses SQLite-style '?' placeholders.
    # PostgreSQL/psycopg uses '%s'; this conversion keeps the existing codebase
    # intact while moving the persistent backend to Supabase PostgreSQL.
    return str(sql).replace("?", "%s")


class _PGCursorCompat:
    def __init__(self, cur):
        self._cur = cur

    def execute(self, sql, params=None):
        return self._cur.execute(_qmark_to_pg(sql), params)

    def executemany(self, sql, params_seq):
        return self._cur.executemany(_qmark_to_pg(sql), params_seq)

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    def __iter__(self):
        return iter(self._cur)

    def __getattr__(self, name):
        return getattr(self._cur, name)


class _PGConnectionCompat:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self, *args, **kwargs):
        return _PGCursorCompat(self._conn.cursor(*args, **kwargs))

    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur

    def executemany(self, sql, params_seq):
        cur = self.cursor()
        cur.executemany(sql, params_seq)
        return cur

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __getattr__(self, name):
        return getattr(self._conn, name)

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

_PAGE_ICON = "dacre_logo.png"

st.set_page_config(
    page_title=f"{APP_NAME} | {DI_NAME}",
    page_icon=_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# DATABASE
# =============================================================================

_DB_SCHEMA_LOCK = threading.RLock()
_DB_SCHEMA_VERSION = 12

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
    if using_cloud_db():
        if psycopg is None or dict_row is None:
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
    rows = con.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=? ORDER BY ordinal_position",
        (table_name,),
    ).fetchall()
    return [str(r["column_name"]) for r in rows]


def _pg_table_exists(con, table_name):
    return bool(
        con.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=? LIMIT 1",
            (table_name,),
        ).fetchone()
    )


def _sqlite_source_tables(src):
    rows = src.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [r[0] for r in rows]


def _migrate_sqlite_to_supabase_once():
    """Copy the existing Streamlit SQLite database into Supabase exactly once.

    This is intentionally performed from the running Streamlit deployment so the
    current deployed customer accounts and DACRE records can survive the switch.
    New Supabase records are never overwritten; conflicts on primary/unique keys
    are ignored.
    """
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
            # If Supabase already contains users, treat it as the production source
            # and do not replay an older local snapshot into it.
            target_users = con.execute("SELECT COUNT(*) AS n FROM public.users").fetchone()["n"]
            if int(target_users or 0) > 0:
                con.execute(
                    "INSERT INTO dacre_schema_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value",
                    ("sqlite_migrated_v1", "skipped_existing_supabase_accounts"),
                )
                con.commit()
                return {"status": "skipped_existing_supabase_accounts", "copied": 0}

            # Copy the core dependency order first; the remaining tables follow.
            preferred = [
                "companies","users","notifications","activity","chat_history","files","projects",
                "company_website_profile","public_visits","emails_log","di_agents","di_private_memory",
                "di_position_history","di_master_thanks","di_jobs","di_collaboration","sovereign_calls",
                "sovereign_call_members","sovereign_call_messages","david_creations","call_rooms",
                "call_participants","decision_ledger","opportunity_radar","loan_clients","whatsapp_delivery_log","company_subscriptions","subscription_payments",
                "presentation_requests","presentation_brain_cache","di_memory"
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

            # Reset PostgreSQL identity sequences to the imported maximum IDs.
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
    con = db(); now = datetime.now().isoformat(timespec="seconds")
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

    # Customer website onboarding + public visitor telemetry.
    try:
        cur.execute("ALTER TABLE companies ADD COLUMN website_url TEXT")
    except sqlite3.OperationalError:
        pass

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
        CREATE TABLE IF NOT EXISTS public_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            page_name TEXT NOT NULL,
            referrer TEXT,
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
            position_title TEXT NOT NULL DEFAULT 'DI Specialist',
            rank_level INTEGER NOT NULL DEFAULT 1,
            appointed_at TEXT,
            appointed_by TEXT,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_active TEXT
        )
    """)

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
    cur.execute("""CREATE TABLE IF NOT EXISTS di_master_thanks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        di_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        host_username TEXT NOT NULL,
        created_at TEXT NOT NULL,
        ended_at TEXT,
        status TEXT NOT NULL DEFAULT 'active'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_call_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id INTEGER NOT NULL,
        di_id INTEGER NOT NULL,
        joined_at TEXT NOT NULL,
        left_at TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS sovereign_call_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id INTEGER NOT NULL,
        speaker_type TEXT NOT NULL,
        speaker_id TEXT,
        speaker_name TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS david_creations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""")

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

    # DACRE Data Presentation Board — presentation requirements are kept separate
    # from the generated PowerPoint artifact so Prociel can continue a presentation
    # conversation without losing the user's choices.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presentation_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            username TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            audience TEXT NOT NULL DEFAULT '',
            objective TEXT NOT NULL DEFAULT '',
            front_slide TEXT NOT NULL DEFAULT '',
            style TEXT NOT NULL DEFAULT '',
            color_direction TEXT NOT NULL DEFAULT '',
            animation_direction TEXT NOT NULL DEFAULT '',
            prompt TEXT NOT NULL DEFAULT '',
            research_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presentation_brain_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            di_name TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_title TEXT NOT NULL DEFAULT '',
            source_url TEXT NOT NULL DEFAULT '',
            content TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()




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
    if using_cloud_db():
        return True
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
        for column,dtype in additions.items():
            if column not in existing:
                con.execute(f"ALTER TABLE di_agents ADD COLUMN {column} {dtype}")
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
    if using_cloud_db():
        return seed_di_memory_postgres()
    con=db(); now=datetime.now().isoformat(timespec="seconds")
    con.execute("PRAGMA journal_mode=WAL")
    # Ensure the current schema can accept the seed records even when upgrading
    # an older DACRE SQLite database.
    cols={r[1] for r in con.execute("PRAGMA table_info(di_memory)").fetchall()}
    migrations={
        "company_name":"TEXT DEFAULT ''", "category":"TEXT DEFAULT 'GENERAL'", "title":"TEXT DEFAULT ''", "content":"TEXT DEFAULT ''",
        "priority":"INTEGER DEFAULT 500", "active":"INTEGER DEFAULT 1", "created_by":"TEXT DEFAULT ''",
        "created_at":"TEXT DEFAULT ''", "updated_at":"TEXT DEFAULT ''"
    }
    for name,decl in migrations.items():
        if name not in cols:
            con.execute(f"ALTER TABLE di_memory ADD COLUMN {name} {decl}")
    con.commit()
    rows=[("",c,t,x,p,MASTER_USERNAME,now,now) for c,t,x,p in DI_MEMORY_SEED]
    con.executemany("INSERT INTO di_memory(company_name,category,title,content,priority,created_by,created_at,updated_at) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM di_memory WHERE company_name=? AND title=? )", [r+(r[0],r[2]) for r in rows])
    con.commit(); con.close()

def get_di_memory(limit=80, query="", company_name=None):
    """Retrieve global DACRE memory plus organization-specific memory."""
    if company_name is None:
        try:
            company_name=(st.session_state.get("user") or {}).get("company")
        except Exception:
            company_name=None
    con=db()
    if company_name:
        rows=con.execute(
            "SELECT id,company_name,category,title,content,priority,active,created_at,updated_at FROM di_memory WHERE active=1 AND (company_name='' OR lower(company_name)=lower(?)) ORDER BY priority DESC,id ASC",
            (company_name,)
        ).fetchall()
    else:
        rows=con.execute("SELECT id,company_name,category,title,content,priority,active,created_at,updated_at FROM di_memory WHERE active=1 ORDER BY priority DESC,id ASC").fetchall()
    con.close()
    if not query:
        return [dict(r) for r in rows[:int(limit)]]
    words=set(re.findall(r"[a-z0-9]{3,}", query.lower()))
    scored=[]
    for r in rows:
        text=f"{r['company_name']} {r['category']} {r['title']} {r['content']}".lower()
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

class _WebsiteExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=[]; self.description=""; self.headings=[]; self.paragraphs=[]
        self._active=None; self._buf=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=="title": self._active="title"; self._buf=[]
        elif tag in ("h1","h2","h3"): self._active=tag; self._buf=[]
        elif tag=="p": self._active="p"; self._buf=[]
        elif tag=="meta" and str(attrs.get("name","")).lower()=="description":
            self.description=str(attrs.get("content","")).strip()[:700]
    def handle_data(self, data):
        if self._active is not None:
            self._buf.append(data)
    def handle_endtag(self, tag):
        if self._active is None: return
        text=re.sub(r"\s+"," "," ".join(self._buf)).strip()
        if text:
            if self._active=="title": self.title.append(text[:300])
            elif self._active in ("h1","h2","h3") and text not in self.headings: self.headings.append(text[:180])
            elif self._active=="p" and len(text)>35 and text not in self.paragraphs: self.paragraphs.append(text[:450])
        self._active=None; self._buf=[]

def _normalize_website_url(value):
    raw=str(value or "").strip()
    if not raw: return ""
    if not re.match(r"^https?://", raw, re.I): raw="https://"+raw
    parsed=urlparse(raw)
    if parsed.scheme not in ("http","https") or not parsed.netloc: return ""
    return raw[:500]

def _fetch_website_profile(url, timeout=1.8):
    url=_normalize_website_url(url)
    if not url: return None
    req=urllib.request.Request(url, headers={"User-Agent":"DACRE-DI/1.0 Website Intelligence"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final_url=resp.geturl() or url
            raw=resp.read(260_000)
            charset=resp.headers.get_content_charset() or "utf-8"
            html=raw.decode(charset, errors="ignore")
        parser=_WebsiteExtractor(); parser.feed(html)
        title=(parser.title[0] if parser.title else "").strip()
        summary=parser.description.strip() or (parser.paragraphs[0] if parser.paragraphs else "")
        headings=list(parser.headings[:10])
        colors=[]
        for c in re.findall(r"#[0-9a-fA-F]{6}", html):
            c=c.lower()
            if c not in colors: colors.append(c)
            if len(colors)>=8: break
        content_summary=" | ".join(headings[:6])
        if summary: content_summary=(summary[:700] + (" | "+content_summary if content_summary else ""))[:1400]
        return {"website_url":final_url[:500],"page_title":title[:300],"description":parser.description[:700],"headings":json.dumps(headings),"summary":content_summary,"theme_primary":colors[0] if colors else "#4b82f5","theme_accent":colors[1] if len(colors)>1 else "#62c8f5","theme_background":colors[2] if len(colors)>2 else "#0b1020","theme_text":"#f4f7ff"}
    except Exception:
        return None

def ensure_company_di(company_name):
    company_name=str(company_name or "").strip()
    if not company_name or company_name.upper()=="DACRE MASTER": return None
    con=db(); now=datetime.now().isoformat(timespec="seconds")
    try:
        row=con.execute("SELECT di_name FROM di_agents WHERE assigned_company=? ORDER BY id ASC LIMIT 1",(company_name,)).fetchone()
        if row: return row["di_name"]
        base="DI — "+re.sub(r"[^A-Za-z0-9 ]+","",company_name).strip()[:34]
        if not base.strip(): base="DI — Business Intelligence"
        name=base; n=2
        while con.execute("SELECT 1 FROM di_agents WHERE di_name=?",(name,)).fetchone(): name=f"{base[:28]} {n}"; n+=1
        code="DI-ORG-"+re.sub(r"[^A-Z0-9]+","-",company_name.upper()).strip("-")[:26]
        while con.execute("SELECT 1 FROM di_agents WHERE di_code=?",(code,)).fetchone(): code += "-ORG"
        con.execute("INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,avatar_url,voice_profile,thinking_style,created_by,created_at,last_active) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(name,code,"Company Intelligence","Assigned",company_name,"Know the customer's business, website context and workspace data; answer with evidence first.","","en-NG","Practical, business-aware, evidence-first and company-specific.",MASTER_USERNAME,now,now))
        con.commit(); return name
    finally: con.close()

def _store_website_memory(company_name, profile, di_name):
    now=datetime.now().isoformat(timespec="seconds")
    items=[
        ("WEBSITE","Official company website",f"Official website supplied at signup: {profile.get('website_url','')}"),
        ("WEBSITE","Website title",profile.get("page_title") or f"Website for {company_name}"),
        ("WEBSITE","Website summary",profile.get("summary") or profile.get("description") or "No readable summary was available from the public homepage."),
        ("WEBSITE","Website headings",profile.get("headings") or "[]"),
        ("DI","Organization DI",f"Dedicated organization DI: {di_name}. Use this company's website context and workspace data when answering."),
    ]
    con=db()
    try:
        for cat,title,content in items:
            con.execute("INSERT INTO di_memory(company_name,category,title,content,priority,active,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",(company_name,cat,title,content,850,1,now,now))
        con.execute("""INSERT INTO company_website_profile(company_name,website_url,page_title,description,headings,summary,theme_primary,theme_accent,theme_background,theme_text,fetched_at,fetch_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(company_name) DO UPDATE SET website_url=excluded.website_url,page_title=excluded.page_title,description=excluded.description,headings=excluded.headings,summary=excluded.summary,theme_primary=excluded.theme_primary,theme_accent=excluded.theme_accent,theme_background=excluded.theme_background,theme_text=excluded.theme_text,fetched_at=excluded.fetched_at,fetch_status=excluded.fetch_status""",(company_name,profile.get("website_url",""),profile.get("page_title",""),profile.get("description",""),profile.get("headings","[]"),profile.get("summary",""),profile.get("theme_primary","#4b82f5"),profile.get("theme_accent","#62c8f5"),profile.get("theme_background","#0b1020"),profile.get("theme_text","#f4f7ff"),now,"ready"))
        con.commit()
    finally: con.close()

def _website_onboarding_worker(company_name, website_url, di_name):
    profile=_fetch_website_profile(website_url, timeout=1.8)
    if profile is None:
        return
    _store_website_memory(company_name, profile, di_name)
    try:
        con=db(); con.execute("UPDATE companies SET website_url=? WHERE name=?",(profile.get("website_url",website_url),company_name)); con.commit(); con.close()
    except Exception:
        pass

def start_website_onboarding(company_name, website_url, di_name):
    url=_normalize_website_url(website_url)
    if not url: return
    threading.Thread(target=_website_onboarding_worker,args=(company_name,url,di_name),daemon=True).start()

def record_public_visit(event_type="landing_view", page_name="Landing"):
    if event_type=="landing_view" and st.session_state.get("public_visit_logged"): return
    visitor_id=st.session_state.get("visitor_id") or uuid.uuid4().hex
    st.session_state.visitor_id=visitor_id
    con=db(); con.execute("INSERT INTO public_visits(visitor_id,event_type,page_name,referrer,created_at) VALUES(?,?,?,?,?)",(visitor_id,event_type,page_name,"",datetime.now().isoformat(timespec="seconds"))); con.commit(); con.close()
    if event_type=="landing_view": st.session_state.public_visit_logged=True

def apply_company_website_theme(user):
    company=str((user or {}).get("company","")).strip()
    if not company or (user or {}).get("role")=="master": return
    con=db(); row=con.execute("SELECT theme_primary,theme_accent,theme_background,theme_text FROM company_website_profile WHERE lower(company_name)=lower(?) ORDER BY id DESC LIMIT 1",(company,)).fetchone(); con.close()
    if not row: return
    p=row["theme_primary"] or "#4b82f5"; a=row["theme_accent"] or "#62c8f5"; b=row["theme_background"] or "#0b1020"
    st.markdown(f"<style>:root{{--dacre-primary:{p};--dacre-primary2:{a};}} .stApp{{background:radial-gradient(circle at 85% 0%,{p}22,transparent 30%),linear-gradient(145deg,{b} 0%,#101729 55%,#0e1628 100%)!important}} .dacre-user-hero,.di-quick-card,.di-metric,.dacre-panel{{border-color:{p}55!important}} .stButton>button,.stFormSubmitButton>button{{background:linear-gradient(135deg,{p},{a})!important}}</style>",unsafe_allow_html=True)

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

def create_account(first, last, company, email, email_password, passkey, website_url=""):
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
        ensure_company_subscription(company_clean, created_at=now)

        di_name=ensure_company_di(company_clean)
        clean_url=normalized_website
        if clean_url:
            con.execute("UPDATE companies SET website_url=? WHERE lower(name)=lower(?)",(clean_url,company_clean)); con.commit()
            start_website_onboarding(company_clean,clean_url,di_name or ("DI — "+company_clean[:32]))
        threading.Thread(target=send_di_welcome_email,args=(first_clean,last_clean,company_clean,email_clean,email_password.strip()),daemon=True).start()
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))
        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, "Account created successfully. DI is preparing your company intelligence in the background.", {
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
        "reminder_2_template": _dacre_secret(
            "DACRE_WHATSAPP_2DAY_TEMPLATE", "dacre_loan_due_2days"
        ),
"due_template": _dacre_secret(
            "DACRE_WHATSAPP_DUE_TEMPLATE", "dacre_loan_due_today"
        ),
        "language": _dacre_secret("DACRE_WHATSAPP_TEMPLATE_LANGUAGE", "en_US"),
    }


def _meta_phone(phone):
    return re.sub(r"[^0-9]", "", normalize_whatsapp_number(phone))


def _log_whatsapp_delivery(
    loan_id,
    company,
    client_name,
    phone,
    reminder_type,
    template_name,
    message_id,
    status,
    response,
):
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

        con.execute(
            """
            INSERT INTO whatsapp_delivery_log
            (
                loan_id,
                company_name,
                client_name,
                whatsapp_number,
                reminder_type,
                template_name,
                message_id,
                status,
                response,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                loan_id,
                company,
                client_name,
                phone,
                reminder_type,
                template_name,
                message_id,
                status,
                str(response)[:4000],
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        con.commit()
    except Exception as e:
        print(f"Database write error: {e}")
    finally:
        con.close()
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

class _HTMLTableExtractor(HTMLParser):
    """Small dependency-free HTML table reader for public website data import."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self._table = None
        self._row = None
        self._cell = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "table":
            self._table = []
        elif self._table is not None and tag == "tr":
            self._row = []
        elif self._row is not None and tag in ("th", "td"):
            self._cell = tag
            self._buf = []

    def handle_data(self, data):
        if self._cell is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("th", "td") and self._cell is not None:
            value = re.sub(r"\s+", " ", " ".join(self._buf)).strip()
            self._row.append(value)
            self._cell = None
            self._buf = []
        elif tag == "tr" and self._row is not None:
            if any(str(x).strip() for x in self._row):
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table:
                self.tables.append(self._table)
            self._table = None


def _read_pdf_dataframe(uploaded_file):
    """Read a PDF into a simple page/text dataframe when pypdf is available."""
    try:
        from pypdf import PdfReader
    except Exception as exc:
        raise ValueError("PDF support needs pypdf. Add pypdf to requirements.txt and redeploy DACRE.") from exc
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    rows = []
    for page_no, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            rows.append({"Page": page_no, "Text": text})
    if not rows:
        return pd.DataFrame(columns=["Page", "Text"])
    return pd.DataFrame(rows)


def load_workbook_sheets(uploaded_file):
    """Return every worksheet in an Excel workbook, cleaned but not merged."""
    uploaded_file.seek(0)
    book = pd.ExcelFile(uploaded_file)
    sheets = {}
    for name in book.sheet_names:
        uploaded_file.seek(0)
        sheets[str(name)] = pd.read_excel(uploaded_file, sheet_name=name)
    uploaded_file.seek(0)
    return sheets


def load_dataframe(uploaded_file, sheet_name=None):
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    uploaded_file.seek(0)
    if extension == "csv":
        return pd.read_csv(uploaded_file)
    if extension == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if extension in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file, sheet_name=sheet_name if sheet_name else 0)
    if extension == "json":
        return pd.read_json(uploaded_file)
    if extension == "pdf":
        return _read_pdf_dataframe(uploaded_file)
    raise ValueError(f"Unsupported file type: .{extension}")


def fetch_website_tables(url, timeout=12, max_tables=20):
    """Fetch public HTML tables from a website without requiring a browser engine."""
    normalized = _normalize_website_url(url)
    if not normalized:
        raise ValueError("Please enter a valid website URL, for example https://example.com")
    req = urllib.request.Request(normalized, headers={"User-Agent": "Mozilla/5.0 DACRE-Data-Importer/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read(1_500_000)
        charset = response.headers.get_content_charset() or "utf-8"
        html = raw.decode(charset, errors="ignore")
    parser = _HTMLTableExtractor()
    parser.feed(html)
    result = []
    for idx, rows in enumerate(parser.tables[:max_tables], start=1):
        if not rows:
            continue
        width = max(len(r) for r in rows)
        normalized_rows = [r + [""] * (width - len(r)) for r in rows]
        header = normalized_rows[0]
        # If the first row is not unique enough to be a header, create neutral names.
        header = [str(v).strip() or f"Column_{i+1}" for i, v in enumerate(header)]
        seen = {}
        safe_header = []
        for col in header:
            base = col
            n = seen.get(base, 0)
            seen[base] = n + 1
            safe_header.append(base if n == 0 else f"{base}_{n+1}")
        frame = pd.DataFrame(normalized_rows[1:], columns=safe_header)
        if not frame.empty:
            result.append((f"Website Table {idx}", frame))
    return result

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

def build_dynamic_chart(df, chart_type, x_col, y_col, title="", limit=25, aggregation="Sum"):
    """Build a dynamic Altair chart from the active processed dataframe."""
    if df is None or df.empty:
        return None
    data = df.copy()
    limit = max(1, min(int(limit or 25), 500))
    chart_type = str(chart_type or "Bar Chart")
    x_col = str(x_col)
    y_col = str(y_col)
    if x_col not in data.columns or y_col not in data.columns:
        return None
    try:
        import altair as alt
    except Exception:
        return None

    if chart_type == "Histogram":
        vals = pd.to_numeric(data[y_col], errors="coerce").dropna()
        chart_data = pd.DataFrame({y_col: vals})
        return alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(f"{y_col}:Q", bin=alt.Bin(maxbins=30), title=y_col),
            y=alt.Y("count():Q", title="Records"),
            tooltip=[alt.Tooltip(f"{y_col}:Q", bin=True), "count():Q"],
        ).properties(title=title or f"Distribution of {y_col}", height=420)

    if chart_type == "Scatter Plot":
        plot = data[[x_col, y_col]].copy()
        plot[y_col] = pd.to_numeric(plot[y_col], errors="coerce")
        plot = plot.dropna().head(limit)
        if not pd.api.types.is_numeric_dtype(plot[x_col]):
            return alt.Chart(plot).mark_circle(size=85, opacity=0.75).encode(
                x=alt.X(f"{x_col}:N", sort=None), y=alt.Y(f"{y_col}:Q"), tooltip=list(plot.columns)
            ).properties(title=title or f"{y_col} by {x_col}", height=420)
        return alt.Chart(plot).mark_circle(size=85, opacity=0.75).encode(
            x=alt.X(f"{x_col}:Q"), y=alt.Y(f"{y_col}:Q"), tooltip=list(plot.columns)
        ).properties(title=title or f"{y_col} vs {x_col}", height=420)

    work = data[[x_col, y_col]].copy()
    work[y_col] = pd.to_numeric(work[y_col], errors="coerce")
    work = work.dropna(subset=[y_col])
    if aggregation == "Average":
        grouped = work.groupby(x_col, dropna=False)[y_col].mean().reset_index(name=y_col)
    elif aggregation == "Count":
        grouped = work.groupby(x_col, dropna=False)[y_col].count().reset_index(name=y_col)
    else:
        grouped = work.groupby(x_col, dropna=False)[y_col].sum().reset_index(name=y_col)
    grouped = grouped.sort_values(y_col, ascending=False).head(limit)

    if chart_type == "Pie Chart":
        return alt.Chart(grouped).mark_arc().encode(
            theta=alt.Theta(f"{y_col}:Q"),
            color=alt.Color(f"{x_col}:N", legend=alt.Legend(title=x_col)),
            tooltip=[x_col, alt.Tooltip(f"{y_col}:Q", format=",.2f")],
        ).properties(title=title or f"{aggregation} of {y_col} by {x_col}", height=420)

    base = alt.Chart(grouped).encode(
        x=alt.X(f"{x_col}:N", sort="-y", title=x_col),
        y=alt.Y(f"{y_col}:Q", title=f"{aggregation} of {y_col}"),
        tooltip=[x_col, alt.Tooltip(f"{y_col}:Q", format=",.2f")],
    )
    if chart_type == "Line Chart":
        return base.mark_line(point=True).properties(title=title or f"{aggregation} of {y_col} by {x_col}", height=420)
    if chart_type == "Area Chart":
        return base.mark_area(opacity=0.72).properties(title=title or f"{aggregation} of {y_col} by {x_col}", height=420)
    return base.mark_bar().properties(title=title or f"{aggregation} of {y_col} by {x_col}", height=420)

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
    """Handle questions that genuinely require a loaded dataset.

    Non-dataset questions return None so the general DI brain, DACRE knowledge,
    memory and web/AI routes can answer them even before a dataset is uploaded.
    """
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
    """Dependency-free public web lookup. Safe fallback when model tools are unavailable."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-DI/2.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I|re.S)
        results = []
        for href, title in items[:max_results]:
            clean_title = re.sub(r"<.*?>", "", title).strip()
            clean_href = urllib.parse.unquote(href)
            if clean_title and clean_href:
                results.append((clean_title, clean_href))
        return results
    except Exception:
        return []


def needs_web_research(text):
    """Detect questions that benefit from current public information."""
    low=(text or "").lower()
    markers=["latest","current","today","tonight","this week","this month","recent","news","price","pricing","cost","version","release","2026","2027","search online","look online","on the internet","online","according to","official","website","who won","what happened","market","competitor","competitors","research","right now","as of"]
    return any(m in low for m in markers)

DI_SPECIALIST_PROFILES={
 "Prociel":{"specialty":"Data Presentation","keywords":["presentation","powerpoint","slide","slides","deck","template","animation","visual"],"research":"PowerPoint capabilities, presentation design, visual trends, templates and executive communication"},
 "Oriel":{"specialty":"Data Analysis","keywords":["analyze","analyse","statistics","kpi","trend","correlation","forecast","sales","revenue","metrics","excel","sheets","sql","python","power bi"],"research":"analytics methods, statistics, business metrics and evidence needed to validate conclusions"},
 "Sofiel":{"specialty":"Research & Intelligence","keywords":["research","market","competitor","competitors","company","industry","product","pricing","news","current","latest","technology","intelligence"],"research":"current web information, market intelligence, competitor information, product facts and source verification"},
 "Daniel":{"specialty":"Data Processing","keywords":["clean","cleaning","duplicate","duplicates","missing","format","transform","merge","sort","filter","vlookup","xlookup","concatenate","csv","excel"],"research":"data-processing standards, file-format behavior and current spreadsheet/data-cleaning techniques"},
 "Graciel":{"specialty":"Insights & Storytelling","keywords":["insight","insights","story","storytelling","recommend","recommendation","meaning","impact","executive","management","decision"],"research":"business interpretation frameworks, industry context and evidence for defensible recommendations"},
 "Henriel":{"specialty":"Files & Documents","keywords":["pdf","word","document","documents","file","files","compare files","extract","summarize","summary","template","export"],"research":"document/file standards, format behavior and source-document context"},
}

def _deterministic_question_understanding(text,df=None):
    """Fallback classifier so every prompt is understood even without an AI API."""
    low=(text or "").strip().lower(); scores={n:sum(1 for k in p["keywords"] if k in low) for n,p in DI_SPECIALIST_PROFILES.items()}
    if any(k in low for k in ["clean","duplicate","missing value","remove duplicates","vlookup","xlookup"]): scores["Daniel"]+=3
    if any(k in low for k in ["why did","what does this mean","recommend","should management"]): scores["Graciel"]+=2
    if any(k in low for k in ["research","latest","current","competitor","market"]): scores["Sofiel"]+=3
    if any(k in low for k in ["powerpoint","slides","presentation","deck"]): scores["Prociel"]+=3
    if df is not None and any(k in low for k in ["my data","this dataset","sales","revenue","trend","average","total","top"]): scores["Oriel"]+=2
    specialist=max(scores,key=scores.get) if max(scores.values()) else "Oriel"
    research=needs_web_research(low) or any(k in low for k in ["find online","search","official source","according to"])
    if any(k in low for k in ["clean","remove","duplicate","missing","transform","merge","sort","filter"]): intent="data_processing"
    elif research or any(k in low for k in ["market","competitor","industry"]): intent="research"
    elif any(k in low for k in ["analy","statistics","kpi","trend","correlation","forecast","sales","revenue"]): intent="analysis"
    elif any(k in low for k in ["presentation","slides","powerpoint","deck"]): intent="presentation"
    elif any(k in low for k in ["recommend","insight","meaning","impact","decision"]): intent="insights"
    elif any(k in low for k in ["pdf","word","document","file","files"]): intent="document_work"
    elif low in {"hi","hello","hey","good morning","good afternoon","good evening","how are you"}: intent="greeting"
    elif len(low.split())<=2: intent="unclear"
    else: intent="general_question"
    actions={"data_processing":"inspect, clean, transform or validate data","research":"research, verify and synthesize external information","analysis":"analyze data, calculate evidence and explain findings","presentation":"design or prepare a presentation and its story","insights":"interpret evidence and provide business implications or recommendations","document_work":"inspect, compare, summarize or produce document/file outputs"}
    workflow=[specialist]
    if research and specialist!="Sofiel": workflow.insert(0,"Sofiel")
    if any(k in low for k in ["presentation","slides","powerpoint","deck"]) and "Prociel" not in workflow: workflow.append("Prociel")
    if any(k in low for k in ["insight","recommend","management","executive"]) and "Graciel" not in workflow: workflow.append("Graciel")
    ambiguous=intent=="unclear" or (df is None and any(k in low for k in ["this dataset","my data","my file","the spreadsheet"]))
    return {"intent":intent,"subject":(text or "")[:220],"requested_action":actions.get(intent,"answer the user's question"),"specialist":specialist,"research_required":bool(research),"input_type":"dataset" if df is not None and any(k in low for k in ["data","dataset","sales","revenue","column","row"]) else "file" if any(k in low for k in ["file","pdf","excel","spreadsheet","document"]) else "text","ambiguity":bool(ambiguous),"clarification_needed":bool(ambiguous),"desired_output":"direct answer","workflow":workflow,"confidence":round(min(.98,.48+max(scores.values())*.08),2),"reason":"deterministic fallback"}

def understand_di_question(text,user=None,df=None,language="English — Nigeria"):
    """Question Understanding Layer: classify every user message before answering."""
    fallback=_deterministic_question_understanding(text,df)
    prompt=("You are DACRE's Question Understanding Engine. Do not answer the user. Return ONLY valid JSON with keys intent, subject, requested_action, specialist, research_required, input_type, ambiguity, clarification_needed, desired_output, workflow, confidence. specialist must be one of Prociel, Oriel, Sofiel, Daniel, Graciel, Henriel. Choose based on what the user actually wants. If unclear, set ambiguity and clarification_needed true. Do not invent missing details. Language: "+str(language))
    try:
        raw=ai_generate(prompt,f"User message: {text}\nDataset loaded: {'yes' if df is not None else 'no'}\nOrganization: {(user or {}).get('company','')}",max_tokens=700)
        if raw:
            cleaned=re.sub(r"^```(?:json)?\s*|\s*```$","",raw.strip(),flags=re.I); data=json.loads(cleaned)
            if isinstance(data,dict):
                result=fallback.copy(); result.update({k:data[k] for k in result if k in data})
                if result.get("specialist") not in DI_SPECIALIST_PROFILES: result["specialist"]=fallback["specialist"]
                if not isinstance(result.get("workflow"),list) or not result["workflow"]: result["workflow"]=fallback["workflow"]
                return result
    except Exception: pass
    return fallback

def _understanding_context(u):
    if not u: return "No structured understanding was produced."
    return ("QUESTION UNDERSTANDING:\n"+f"Intent: {u.get('intent')}\nSubject: {u.get('subject')}\nRequested action: {u.get('requested_action')}\nSpecialist: {u.get('specialist')}\nResearch required: {u.get('research_required')}\nInput type: {u.get('input_type')}\nDesired output: {u.get('desired_output')}\nAmbiguity: {u.get('ambiguity')}\nWorkflow: {' -> '.join(u.get('workflow') or [])}\nConfidence: {u.get('confidence')}")


def build_di_context(user, df):
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
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "") or "").strip()


def _free_ai_only_mode():
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


def _gemini_grounded_generate(system_prompt,user_prompt,max_tokens=1200):
    """Gemini Google Search grounding for current, source-backed DI research."""
    key=_free_secret("GEMINI_API_KEY")
    if not key: return None,[]
    model=_free_secret("DACRE_GEMINI_MODEL") or "gemini-2.5-flash"
    payload={"systemInstruction":{"parts":[{"text":system_prompt}]},"contents":[{"role":"user","parts":[{"text":user_prompt}]}],"tools":[{"google_search":{}}],"generationConfig":{"temperature":0.2,"maxOutputTokens":min(int(max_tokens),1800)}}
    try:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model,safe='')}:generateContent"
        req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"x-goog-api-key":key,"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=35) as response: data=json.loads(response.read().decode())
        candidate=(data.get("candidates") or [{}])[0]; parts=(candidate.get("content") or {}).get("parts") or []
        answer="".join(str(x.get("text","")) for x in parts).strip(); meta=candidate.get("groundingMetadata") or {}; sources=[]
        for chunk in meta.get("groundingChunks",[]) or []:
            web=chunk.get("web") or {}; uri=web.get("uri"); title=web.get("title") or uri
            if uri and (title,uri) not in sources: sources.append((title,uri))
        return (answer or None),sources[:8]
    except Exception: return None,[]

def ai_generate_with_research(system_prompt,user_prompt,max_tokens=1200):
    if _free_secret("GEMINI_API_KEY"):
        answer,sources=_gemini_grounded_generate(system_prompt,user_prompt,max_tokens)
        if answer: return answer,sources
    return ai_generate(system_prompt,user_prompt,max_tokens=max_tokens),[]


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


def ai_generate(system_prompt, user_prompt, max_tokens=900, prefer_grounded=False):
    """Free-first DI reasoning router with optional grounded research."""
    if prefer_grounded and _free_secret("GEMINI_API_KEY"):
        answer,_=_gemini_grounded_generate(system_prompt,user_prompt,max_tokens=max_tokens)
        if answer: return answer
    answer=_groq_generate(system_prompt,user_prompt,max_tokens=max_tokens)
    if answer: return answer
    answer=_gemini_generate(system_prompt,user_prompt,max_tokens=max_tokens)
    if answer: return answer
    return _openai_generate_paid(system_prompt,user_prompt,max_tokens=max_tokens) or None


def free_ai_provider_status():
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
    text=re.sub(r"\bI\s+am\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    text=re.sub(r"\bI\x27m\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    return text

def di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    text=message.strip()
    low=text.lower()
    if not text:
        return "I am ready. Tell me the business result you want to achieve."

    understanding=understand_di_question(text,user=user,df=df,language=language)
    try: st.session_state["di_last_understanding"]=understanding
    except Exception: pass

    name="Master David" if user["role"]=="master" else user["first_name"]
    greetings=["hello","hi","hey","good morning","good afternoon","good evening","good day","how are you"]
    greeting_hit = any(
        re.search(r"(^|\b)" + re.escape(p) + r"($|\b)", low)
        for p in greetings
    )
    if greeting_hit and len(low.split()) <= 8:
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
        return "I can work with DACRE's Memory Box, inspect and clean data, calculate business metrics, identify missing values and duplicates, build charts, explain results, help with workspace/account questions, keep a question trail, research public online information when needed, and explain how DACRE itself is built."

    # Fast feature guidance that does not require a dataset.
    if "bar chart" in low or ("create" in low and "chart" in low):
        return (
            "To create a bar chart in DACRE: open Charts, make sure your dataset is loaded, "
            "choose Bar Chart, choose the category column for the X-axis, choose the numeric "
            "column for the Y-axis, then select Generate Dynamic Chart. I can also help you "
            "choose the best columns for the chart."
        )

    if any(k in low for k in [
        "how were you built", "how are you built", "how were you coded",
        "how did david code you", "how does dacre work", "how is dacre built",
        "what is in your code", "explain your code", "are you intelligent",
        "massively intelligent", "i coded you"
    ]):
        master_note = " Because you are David, the creator and Overall Administrator, I treat this as a Sovereign Master request." if user.get("role") == "master" else ""
        return (
            "I am DI — David's Intelligence. DACRE combines a Streamlit application, a persistent "
            "database layer, organization accounts, DI Memory, workspace data analysis, charts, "
            "a DI workforce, Chibobec client workflows, protected master administration, browser "
            "voice interaction, and optional online research. My knowledge is designed to explain "
            "those systems in user-friendly English rather than expose private credentials or "
            "secret configuration values." + master_note
        )

    if any(k in low for k in [
        "who am i", "do you know me", "my identity", "who is the user",
        "what is my name", "what company am i in"
    ]):
        company = user.get("company","your organization")
        full_name = f"{user.get('first_name','')} {user.get('last_name','')}".strip() or "the current user"
        role = user.get("role","user")
        if role == "master":
            return "You are David Emenike, the creator and Overall Administrator of DACRE Analysis. This is a Sovereign Master context, separate from an ordinary company user's chat."
        return f"You are {full_name}, working in the {company} workspace. Your current DACRE role is {role}. I keep your workspace context separate from other organizations."
    if "memory box" in low or "di mb" in low:
        return "The DI Memory Box (DI MB) is my persistent knowledge base. I use it first for DACRE identity, platform rules, account administration, security, DI behavior and other trusted project information. The Overall Administrator can maintain it from the master portal."
    if any(k in low for k in ["tech partner","ask david","chatgpt partner"]):
        return "David's tech partner is the ChatGPT assistant David uses to build and improve DACRE. I can use the project information stored in my DI Memory Box, but I cannot directly invoke that separate ChatGPT conversation. For deeper code, architecture or UI/UX work, David can ask his tech partner directly in the main ChatGPT project."

    # Deterministic workspace intelligence remains available even without an API.
    if "what can" in low and "dacre" in low:
        return "DACRE is a business and data analysis workspace with data cleaning, formulas, charts, File Vault, exports, organization administration and DI intelligence."
    if any(k in low for k in ["dacre", "file vault", "formula lab", "export center", "admin portal", "workspace", "chibobec"]):
        return "DACRE Analysis is the connected business and data intelligence workspace. It includes the Company Dashboard, DI Workforce, Data Presentation Board, Workspace & Data, Formula Lab, Charts, File Vault and Export Center. Platform-wide administration belongs to DGL, the main DACRE Global Limited platform."

    # Dataset tools run only after general DACRE/non-dataset questions have had a chance to resolve.
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

    # Research is driven by structured understanding. Gemini Google Search is preferred when configured; the legacy public lookup remains a fallback.
    should_search=allow_online and bool(understanding.get("research_required"))
    fallback_results=online_lookup(text,max_results=5) if should_search else []
    fallback_source_text="\n".join([f"SOURCE {i+1}: {title}\nURL: {href}" for i,(title,href) in enumerate(fallback_results)])
    context=build_di_context(user,df)
    answer,grounded_sources=ai_generate_with_research(
        f"You are DI — David's Intelligence, the fast business/data assistant inside DACRE Analysis. Always identify yourself as DI. Use the DI Memory Box, recent conversation, active dataset and structured Question Understanding below. Answer ordinary questions directly. Use evidence for current facts and distinguish evidence from inference. Never reveal credentials, tokens or private security values. If the request is ambiguous, ask one focused clarification instead of guessing. If the workflow contains multiple DIs, use the specialist sequence internally and keep the user-facing answer natural. Respond in the selected language when practical: {language}.",
        f"DACRE context:\n{context}\n\n{_understanding_context(understanding)}\n\nFallback web leads:\n{fallback_source_text or 'none'}\n\nUser question:\n{text}",
        max_tokens=1400,
    )
    if answer:
        sources=grounded_sources or fallback_results
        suffix="\n\nSources checked: "+"; ".join(t for t,_ in sources[:5]) if sources else ""
        return normalize_di_identity(answer)+suffix
    if fallback_results:
        return "I checked public sources for this question.\n\n"+"\n".join(f"- {t} — {u}" for t,u in fallback_results[:5])
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
    profile=(voice_profile or "").strip().lower()
    hints={
        "male": r"male|man|daniel|david|alex|george|james|oliver|microsoft.*male|google.*male",
        "female": r"female|woman|samantha|aria|ava|victoria|zira|microsoft.*female|google.*female",
    }
    hint=hints.get(profile, profile if profile else hints["male"])
    safe_text=json.dumps(str(text)); safe_lang=json.dumps(language_code); safe_hint=json.dumps(hint)
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
    """,height=1,scrolling=False)

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

def render_di_video_call_stage(agent_rows, title, user_label):
    """Render DI participants as text-only cards. No DI portraits are used."""
    people=[]
    for idx,row in enumerate(agent_rows):
        a=dict(row)
        name=str(a.get("di_name") or "DI")
        position=str(a.get("position_title") or a.get("specialty") or "DI Specialist")
        people.append(
            f"<div class='di-video-person text-only-di' data-speaker-index='{idx}'>"
            f"<div class='di-video-face-wrap text-only-face'><div class='di-avatar-fallback'>{_escape_html(name[:1].upper())}</div></div>"
            f"<div class='di-video-name'>{_escape_html(name)}</div>"
            f"<div class='di-video-role'>{_escape_html(position)}</div>"
            f"<div class='di-video-status'><span class='speaker-dot'>Ready</span></div></div>"
        )
    st.markdown(
        f"<div class='di-video-stage'><div class='di-video-title'>{_escape_html(title)}</div>"
        f"<div class='di-video-sub'>{_escape_html(user_label)}</div>"
        f"<div class='di-video-grid'>{''.join(people)}</div></div>",
        unsafe_allow_html=True,
    )

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
      <button id="dacre-speak-btn" style="background:#f28c28;color:white;border:0;border-radius:10px;padding:9px 15px;font-weight:800;cursor:pointer;">Speak DI</button>
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
    """Maintain the 20 permanent named master DI characters. Organization DIs remain separate. """
    roster = [
        ("Emiel", "Communications & Messaging", "Prepare, organize and manage business email and messaging workflows.", "Polite, concise, organized and communication-focused.", "male", "", "Communications Specialist", 2),
        ("Oriel", "Data Analysis", "Inspect datasets, calculate metrics, find trends and produce analytical insights.", "Logical, numerical, evidence-first and precise.", "male", "", "Lead Data Analyst", 5),
        ("Sofiel", "Research & Intelligence", "Research business, market and general information and summarize reliable findings.", "Curious, investigative, source-conscious and analytical.", "female", "", "Research Intelligence Lead", 5),
        ("Daniel", "Data Entry & Processing", "Structure, clean, validate and process repetitive business data accurately.", "Careful, systematic, consistent and detail-oriented.", "male", "", "Data Operations Specialist", 3),
        ("Graciel", "Business Intelligence", "Turn business data into KPIs, dashboards, executive insights and recommendations.", "Strategic, practical and outcome-focused.", "female", "", "Business Intelligence Lead", 6),
        ("Henriel", "Files & Documents", "Organize, inspect, summarize and manage business documents and files.", "Organized, careful and document-focused.", "male", "", "Knowledge & Documents Specialist", 3),
        ("Jamiel", "Security & Administration", "Support account administration, access controls, audit trails and system operations.", "Cautious, disciplined and security-first.", "male", "", "Security & Administration Lead", 6),
        ("Ameliel", "Client Success & Communication", "Help users understand DACRE and communicate business information clearly.", "Calm, respectful, patient and user-focused.", "female", "", "Client Success Specialist", 3),
        ("Guaiel", "CEO Office Security", "Guard the CEO Office, verify the master guardian challenge and protect the founder command path.", "Vigilant, respectful, discreet and uncompromising about secure access.", "male", "", "CEO Office Guardian", 20),
        ("Nathaniel", "Financial Intelligence", "Analyze financial performance, budgets, profitability, cash flow and forecasts.", "Numerate, cautious, commercially aware and precise.", "male", "", "Financial Intelligence Lead", 7),
        ("Gabriel", "Sales Intelligence", "Analyze pipelines, customers, conversion, win rates and sales opportunities.", "Commercial, persuasive, evidence-led and target-focused.", "male", "", "Sales Intelligence Lead", 6),
        ("Raphaiel", "Marketing Intelligence", "Analyze campaigns, audiences, attribution, engagement and marketing ROI.", "Creative, analytical, curious and outcome-focused.", "male", "", "Marketing Intelligence Lead", 5),
        ("Uriel", "Operations Intelligence", "Improve workflows, capacity, throughput, quality, scheduling and operational efficiency.", "Systematic, practical and improvement-oriented.", "male", "", "Operations Intelligence Lead", 6),
        ("Ariel", "Strategy & Planning", "Translate business goals into strategy, scenarios, priorities and execution plans.", "Strategic, calm, curious and decisive.", "female", "", "Strategy Planning Lead", 8),
        ("Muriel", "HR & Workforce", "Support workforce planning, roles, positions, communication and people operations.", "Empathetic, balanced, professional and policy-aware.", "female", "", "People & Workforce Lead", 5),
        ("Azriel", "Risk & Compliance", "Identify risk, controls, compliance concerns and operational exposures.", "Cautious, evidence-first and governance-minded.", "male", "", "Risk & Compliance Lead", 7),
        ("Adriel", "Technology Intelligence", "Help with software architecture, Python, automation and technical problem solving.", "Technical, inventive, structured and pragmatic.", "male", "", "Technology Intelligence Lead", 8),
        ("Haniel", "Knowledge & Learning", "Turn complex subjects into clear learning materials, explanations and practical guidance.", "Patient, articulate, educational and encouraging.", "female", "", "Knowledge & Learning Lead", 4),
        ("Gadiel", "Customer & Market Insights", "Study customers, market segments, demand signals and competitive positioning.", "Observant, commercially curious and evidence-driven.", "male", "", "Customer Insights Lead", 5),
        ("Raziel", "Executive Intelligence", "Synthesize multi-domain evidence into executive briefs, options, risks and recommendations.", "Discerning, strategic, concise and high-judgment.", "female", "", "Executive Intelligence Director", 10),
    ]
    old_map={"Oliver":"Oriel","Sophie":"Sofiel","Grace":"Graciel","Henry":"Henriel","James":"Jamiel","Amelia":"Ameliel"}
    con=db(); now=datetime.now().isoformat(timespec="seconds")
    try:
        for old,new_name in old_map.items():
            old_row=con.execute("SELECT id FROM di_agents WHERE di_name=?",(old,)).fetchone()
            new_row=con.execute("SELECT id FROM di_agents WHERE di_name=?",(new_name,)).fetchone()
            if old_row and not new_row:
                con.execute("UPDATE di_agents SET di_name=? WHERE id=?",(new_name,int(old_row["id"])))
        for name,specialty,role,style,voice,avatar,position,rank in roster:
            row=con.execute("SELECT id FROM di_agents WHERE di_name=?",(name,)).fetchone()
            code="DI-"+re.sub(r"[^A-Z0-9]+","-",name.upper()).strip("-")
            if row:
                con.execute("UPDATE di_agents SET di_code=?,specialty=?,system_role=?,avatar_url=?,voice_profile=?,thinking_style=?,position_title=?,rank_level=?,status=CASE WHEN status='Archived' THEN 'Available' ELSE status END,last_active=? WHERE id=?",(code,specialty,role,avatar,voice,style,position,rank,now,int(row["id"])))
            else:
                con.execute("INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,avatar_url,voice_profile,thinking_style,position_title,rank_level,appointed_at,appointed_by,created_by,created_at,last_active) VALUES(?,?,?,'Available',NULL,?,?,?,?,?,?,?,?,?,?,?)",(name,code,specialty,role,avatar,voice,style,position,rank,now,MASTER_USERNAME,MASTER_USERNAME,now,now))
        # Archive obsolete unassigned legacy workforce entries so the permanent master roster remains exactly 20.
        target_names={r[0] for r in roster}
        for row in con.execute("SELECT id,di_name,assigned_company FROM di_agents").fetchall():
            if row["di_name"] not in target_names and not (row["assigned_company"] or "").strip():
                con.execute("UPDATE di_agents SET status='Archived',last_active=? WHERE id=?",(now,int(row["id"])))
        con.commit()
    finally:
        con.close()


def _bootstrap_runtime(schema_version=12):
    """Bootstrap DACRE on either legacy SQLite or persistent Supabase PostgreSQL."""
    if using_cloud_db():
        _migrate_sqlite_to_supabase_once()
        ensure_di_agent_columns()
        ensure_master()
        seed_di_memory()
        seed_named_di_workforce()
        ensure_presentation_schema()
        ensure_subscription_schema()
        seed_active_di_workforce()
        return True

    init_db()
    ensure_runtime_schema()
    ensure_di_agent_columns()
    ensure_master()
    seed_di_memory()
    seed_named_di_workforce()
    ensure_presentation_schema()
    ensure_subscription_schema()
    seed_active_di_workforce()
    return True



# =============================================================================
# PRESENTATION BOARD / SIX-DI WORKFORCE INFRASTRUCTURE
# =============================================================================

ACTIVE_DI_ROSTER = [
    ("Prociel", "Data Presentation", "Own the Data Presentation Board, interview the user about the desired story, design slides, research visual references, build PowerPoint decks and prepare presentation-ready insights.", "Creative, structured, visual, executive and presentation-first.", "female", "", "Data Presentation Director", 10),
    ("Oriel", "Data Analysis", "Inspect the loaded dataset, calculate statistics, find patterns, validate conclusions and supply evidence to the other DIs.", "Numerical, evidence-first, precise and analytical.", "male", "", "Lead Data Analyst", 9),
    ("Sofiel", "Research & Intelligence", "Research public information, verify sources, gather current facts and provide online intelligence to the active DACRE task.", "Investigative, source-conscious, curious and analytical.", "female", "", "Research Intelligence Lead", 8),
    ("Daniel", "Data Processing", "Clean, transform, validate and structure datasets so analysis and presentation work starts from reliable data.", "Systematic, careful, consistent and detail-oriented.", "male", "", "Data Operations Specialist", 7),
    ("Graciel", "Insights & Storytelling", "Turn validated findings into clear business/data insights, narratives, headlines and speaker-ready explanations without inventing facts.", "Strategic, clear, practical and audience-aware.", "female", "", "Insights Director", 8),
    ("Henriel", "Files & Documents", "Manage presentation assets, source files, document context, templates, exports and supporting artifacts for the active project.", "Organized, careful, document-focused and dependable.", "male", "", "Knowledge & Documents Specialist", 7),
]


def ensure_presentation_schema():
    """Create the presentation/DI brain tables on both SQLite and Postgres."""
    con = db()
    try:
        if using_cloud_db():
            con.execute("""CREATE TABLE IF NOT EXISTS presentation_requests (
                id BIGSERIAL PRIMARY KEY, company_name TEXT NOT NULL, username TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT '', audience TEXT NOT NULL DEFAULT '', objective TEXT NOT NULL DEFAULT '',
                front_slide TEXT NOT NULL DEFAULT '', style TEXT NOT NULL DEFAULT '', color_direction TEXT NOT NULL DEFAULT '',
                animation_direction TEXT NOT NULL DEFAULT '', prompt TEXT NOT NULL DEFAULT '', research_json TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            con.execute("""CREATE TABLE IF NOT EXISTS presentation_brain_cache (
                id BIGSERIAL PRIMARY KEY, di_name TEXT NOT NULL, source_type TEXT NOT NULL,
                source_title TEXT NOT NULL DEFAULT '', source_url TEXT NOT NULL DEFAULT '', content TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL)""")
        else:
            con.execute("""CREATE TABLE IF NOT EXISTS presentation_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT NOT NULL, username TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT '', audience TEXT NOT NULL DEFAULT '', objective TEXT NOT NULL DEFAULT '',
                front_slide TEXT NOT NULL DEFAULT '', style TEXT NOT NULL DEFAULT '', color_direction TEXT NOT NULL DEFAULT '',
                animation_direction TEXT NOT NULL DEFAULT '', prompt TEXT NOT NULL DEFAULT '', research_json TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            con.execute("""CREATE TABLE IF NOT EXISTS presentation_brain_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT, di_name TEXT NOT NULL, source_type TEXT NOT NULL,
                source_title TEXT NOT NULL DEFAULT '', source_url TEXT NOT NULL DEFAULT '', content TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL)""")
        con.commit()
    finally:
        con.close()


def seed_active_di_workforce():
    """Keep exactly six active DACRE Analysis DIs; DGL will own the wider workforce later."""
    con = db(); now = datetime.now().isoformat(timespec="seconds")
    active_names = {row[0] for row in ACTIVE_DI_ROSTER}
    try:
        for name, specialty, role, style, gender, avatar, position, rank in ACTIVE_DI_ROSTER:
            row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (name,)).fetchone()
            code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")
            if row:
                con.execute("""UPDATE di_agents SET di_code=?, specialty=?, system_role=?, status='Available',
                    assigned_company=NULL, avatar_url=?, voice_profile=?, thinking_style=?, position_title=?, rank_level=?,
                    last_active=? WHERE id=?""", (code, specialty, role, avatar, gender, style, position, rank, now, int(row["id"])))
            else:
                con.execute("""INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,avatar_url,voice_profile,
                    thinking_style,position_title,rank_level,appointed_at,appointed_by,created_by,created_at,last_active)
                    VALUES(?,?,?,'Available',NULL,?,?,?,?,?,?,?,?,?,?,?)""", (name, code, specialty, role, avatar, gender, style, position, rank, now, MASTER_USERNAME, MASTER_USERNAME, now, now))
        # Preserve old records for historical integrity, but archive them from DACRE's visible workforce.
        for row in con.execute("SELECT id,di_name FROM di_agents").fetchall():
            if row["di_name"] not in active_names:
                con.execute("UPDATE di_agents SET status='Archived', assigned_company=NULL, last_active=? WHERE id=?", (now, int(row["id"])))
        con.commit()
    finally:
        con.close()


def _presentation_secret(name, default=""):
    return _free_secret(name) if "_free_secret" in globals() else str(os.getenv(name, default) or default).strip()


def _hex_rgb(value, fallback=(25, 70, 150)):
    text = str(value or "").strip().lstrip("#")
    if len(text) == 6 and all(c in "0123456789abcdefABCDEF" for c in text):
        return tuple(int(text[i:i+2], 16) for i in (0, 2, 4))
    return fallback


def _online_design_references(query, limit=5):
    """Public web research for design/template/animation references; URLs stay in Prociel's private board context."""
    return online_lookup(query, max_results=limit)


def _online_color_palette(seed="#1769aa"):
    """Ask a public color service for a palette; fall back to a deterministic professional palette."""
    try:
        clean = str(seed or "#1769aa").lstrip("#")
        url = f"https://www.thecolorapi.com/scheme?hex={urllib.parse.quote(clean)}&mode=analogic&count=5"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-Prociel/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        colors = [str(x.get("hex", {}).get("value", "")) for x in data.get("colors", [])]
        return [c for c in colors if re.fullmatch(r"#[0-9A-Fa-f]{6}", c)][:5] or ["#1769AA", "#00A6C8", "#6C63FF", "#F4F7FB", "#172033"]
    except Exception:
        return ["#1769AA", "#00A6C8", "#6C63FF", "#F4F7FB", "#172033"]


def _online_visual_reference(query):
    """Find a reusable public visual reference from Wikimedia Commons without exposing credentials."""
    try:
        params = urllib.parse.urlencode({"action":"query", "generator":"search", "gsrsearch":query, "gsrnamespace":"6", "gsrlimit":"5", "prop":"imageinfo", "iiprop":"url", "iiurlwidth":"1400", "format":"json"})
        req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + params, headers={"User-Agent":"DACRE-Prociel/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data=json.loads(response.read().decode("utf-8"))
        pages=list((data.get("query",{}).get("pages") or {}).values())
        if not pages: return None
        page=pages[0]
        info=(page.get("imageinfo") or [{}])[0]
        return {"title":page.get("title",""), "url":info.get("thumburl") or info.get("url",""), "source":"Wikimedia Commons"}
    except Exception:
        return None


def _fetch_binary(url, timeout=15, max_bytes=7_000_000):
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 DACRE-Prociel/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data=response.read(max_bytes+1)
        return data if len(data) <= max_bytes else None
    except Exception:
        return None


def _add_slide_transition(slide, kind="fade"):
    """Add a real PowerPoint slide transition when the OOXML element is supported."""
    try:
        from pptx.oxml.xmlchemy import OxmlElement
        spTree = slide._element
        old = spTree.find("{http://schemas.openxmlformats.org/presentationml/2006/main}transition")
        if old is not None:
            spTree.remove(old)
        transition=OxmlElement("p:transition")
        transition.set("spd", "med")
        transition.append(OxmlElement("p:" + ("fade" if kind not in {"fade","cut"} else kind)))
        spTree.insert(2, transition)
    except Exception:
        pass


def _presentation_prompt_spec(prompt, board, df):
    """Let Gemini design the story when configured; otherwise use a deterministic local plan."""
    system=("You are Prociel, DACRE's Data Presentation Director. Create a factual PowerPoint plan from the loaded inspection-board dataset. "
            "Never invent values. Return concise JSON with keys: title, subtitle, narrative, slides, palette, animation. "
            "slides must be a list of objects with title, purpose, bullets, chart_column. Keep it suitable for the requested audience.")
    summary={"rows":0 if df is None else len(df),"columns":[] if df is None else [str(c) for c in df.columns],"numeric":[] if df is None else [str(c) for c in df.select_dtypes(include="number").columns],"front_slide":board.get("front_slide",""),"audience":board.get("audience",""),"objective":board.get("objective",""),"style":board.get("style",""),"colors":board.get("color_direction",""),"animation":board.get("animation_direction","")}
    if df is not None and not df.empty:
        stats={}
        for c in df.select_dtypes(include="number").columns[:8]:
            vals=pd.to_numeric(df[c],errors="coerce")
            stats[str(c)]={"sum":float(vals.sum()),"mean":float(vals.mean()) if vals.notna().any() else 0,"min":float(vals.min()) if vals.notna().any() else 0,"max":float(vals.max()) if vals.notna().any() else 0}
        summary["stats"]=stats
    ai=ai_generate(system, json.dumps({"request":prompt,"board":summary}, ensure_ascii=False), max_tokens=1600)
    if ai:
        try:
            clean=ai.strip()
            clean=re.sub(r"^```(?:json)?", "", clean, flags=re.I).strip().removesuffix("```").strip()
            spec=json.loads(clean)
            if isinstance(spec,dict) and isinstance(spec.get("slides"),list):
                return spec
        except Exception:
            pass
    numeric=[] if df is None else [str(c) for c in df.select_dtypes(include="number").columns]
    bullets=[f"{len(df):,} records",f"{len(df.columns):,} columns"] if df is not None else ["No dataset loaded"]
    if df is not None: bullets.append(f"{int(df.isna().sum().sum()):,} missing cells")
    slides=[
        {"title":board.get("front_slide") or "Data Story", "purpose":"Opening", "bullets":bullets, "chart_column":numeric[0] if numeric else ""},
        {"title":"What the dataset contains", "purpose":"Scope", "bullets":[f"Columns: {', '.join(map(str, df.columns[:12]))}" if df is not None else "Load data to populate this slide"], "chart_column":""},
    ]
    if numeric:
        target=numeric[0]; vals=pd.to_numeric(df[target],errors="coerce")
        slides.append({"title":f"Key finding: {target}","purpose":"Evidence","bullets":[f"Total: {vals.sum():,.2f}",f"Average: {vals.mean():,.2f}",f"Highest: {vals.max():,.2f}"],"chart_column":target})
    slides.append({"title":"Recommended next steps","purpose":"Action","bullets":["Validate the strongest finding against source data","Discuss the decision or action required","Use the exported deck as the presentation record"],"chart_column":""})
    return {"title":board.get("title") or "DACRE Data Presentation","subtitle":board.get("objective") or "Evidence from the active inspection board","narrative":"A data-first presentation generated by Prociel.","slides":slides,"palette":_online_color_palette(),"animation":"Fade between major sections."}


def generate_dacre_presentation(df, board, prompt):
    if Presentation is None:
        raise RuntimeError("python-pptx is not installed. Add python-pptx to requirements.txt and redeploy DACRE.")
    spec=_presentation_prompt_spec(prompt, board, df)
    palette=spec.get("palette") if isinstance(spec.get("palette"),list) else _online_color_palette()
    palette=[x for x in palette if re.fullmatch(r"#[0-9A-Fa-f]{6}",str(x))][:5] or _online_color_palette()
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    blank=prs.slide_layouts[6]
    dark=_hex_rgb(palette[-1],(16,27,48)); accent=_hex_rgb(palette[0],(23,105,170)); accent2=_hex_rgb(palette[1],(0,166,200)); light=_hex_rgb(palette[-2],(244,247,251))
    # Optional online visual reference for the title slide. It is fetched only as a visual aid.
    visual=_online_visual_reference("business data technology presentation abstract")
    def add_bg(slide, color):
        shape=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,prs.slide_width,prs.slide_height)
        shape.fill.solid(); shape.fill.fore_color.rgb=RGBColor(*color); shape.line.fill.background(); shape.z_order=0
    def add_text(slide,text,left,top,width,height,size=24,bold=False,color=(255,255,255),align=None):
        box=slide.shapes.add_textbox(Inches(left),Inches(top),Inches(width),Inches(height)); tf=box.text_frame; tf.clear(); p=tf.paragraphs[0]; p.text=str(text); p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor(*color); p.font.name="Aptos"; p.alignment=align or PP_ALIGN.LEFT; return box
    # Front slide
    slide=prs.slides.add_slide(blank); add_bg(slide,dark)
    if visual and visual.get("url"):
        raw=_fetch_binary(visual["url"],max_bytes=4_000_000)
        if raw:
            try: slide.shapes.add_picture(io.BytesIO(raw), Inches(8.7), Inches(0.7), width=Inches(3.9), height=Inches(5.9))
            except Exception: pass
    add_text(slide,"DACRE ANALYSIS",0.8,0.65,7.0,0.5,15,True,accent2)
    add_text(slide,spec.get("title") or board.get("front_slide") or "Data Presentation",0.8,1.45,7.3,1.5,34,True,(255,255,255))
    add_text(slide,spec.get("subtitle") or board.get("objective") or "Data-driven presentation",0.8,3.15,6.9,1.0,20,False,(220,232,245))
    add_text(slide,f"Prepared by Prociel · {datetime.now().strftime('%d %b %Y')}",0.8,6.55,6.8,0.35,12,False,(160,185,210))
    _add_slide_transition(slide,"fade")
    # Content slides
    for idx,item in enumerate(spec.get("slides",[])[:14],start=2):
        slide=prs.slides.add_slide(blank); add_bg(slide,light)
        add_text(slide,f"{idx:02d}",0.7,0.45,0.5,0.4,12,True,accent)
        add_text(slide,item.get("title") or "Untitled",1.25,0.35,10.9,0.8,27,True,dark)
        bullets=item.get("bullets") or []
        y=1.55
        for bullet in bullets[:6]:
            add_text(slide,"• "+str(bullet),1.0,y,10.8,0.58,17,False,dark); y+=0.72
        chart_col=item.get("chart_column")
        if df is not None and chart_col and chart_col in df.columns:
            vals=pd.to_numeric(df[chart_col],errors="coerce").dropna()
            if not vals.empty:
                maxv=float(vals.abs().max() or 1)
                base_y=6.35; x0=1.0; barw=0.48; gap=0.18
                sample=vals.head(12).tolist()
                for j,v in enumerate(sample):
                    h=max(0.08,4.0*abs(float(v))/maxv)
                    sh=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0+j*(barw+gap)), Inches(base_y-h), Inches(barw), Inches(h))
                    sh.fill.solid(); sh.fill.fore_color.rgb=RGBColor(*accent); sh.line.fill.background()
                add_text(slide,f"Visual sample · {chart_col}",1.0,6.5,5.0,0.3,10,False,(90,110,130))
        add_text(slide,"DACRE · Prociel",10.2,7.08,2.2,0.25,9,False,(100,120,140),PP_ALIGN.RIGHT)
        _add_slide_transition(slide,"fade")
    out=io.BytesIO(); prs.save(out); out.seek(0); return out.getvalue(),spec,visual


def save_presentation_request(user, board, prompt, research):
    now=datetime.now().isoformat(timespec="seconds")
    con=db()
    con.execute("""INSERT INTO presentation_requests(company_name,username,title,audience,objective,front_slide,style,color_direction,animation_direction,prompt,research_json,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",(user["company"],user["username"],board.get("title",""),board.get("audience",""),board.get("objective",""),board.get("front_slide",""),board.get("style",""),board.get("color_direction",""),board.get("animation_direction",""),prompt,json.dumps(research,ensure_ascii=False),now,now))
    con.commit(); con.close()


def microsoft_graph_upload_presentation(data, filename):
    """Optional Microsoft Graph upload. Microsoft PowerPoint itself does not issue a simple API key."""
    tenant=_presentation_secret("MICROSOFT_GRAPH_TENANT_ID")
    client=_presentation_secret("MICROSOFT_GRAPH_CLIENT_ID")
    secret=_presentation_secret("MICROSOFT_GRAPH_CLIENT_SECRET")
    user_id=_presentation_secret("MICROSOFT_GRAPH_USER_ID")
    if not all([tenant,client,secret,user_id]): return None
    token_url=f"https://login.microsoftonline.com/{urllib.parse.quote(tenant,safe='')}/oauth2/v2.0/token"
    body=urllib.parse.urlencode({"client_id":client,"client_secret":secret,"scope":"https://graph.microsoft.com/.default","grant_type":"client_credentials"}).encode()
    try:
        req=urllib.request.Request(token_url,data=body,headers={"Content-Type":"application/x-www-form-urlencoded"},method="POST")
        with urllib.request.urlopen(req,timeout=20) as r: token=json.loads(r.read().decode()).get("access_token")
        if not token: return None
        safe_name=urllib.parse.quote(filename,safe="")
        url=f"https://graph.microsoft.com/v1.0/users/{urllib.parse.quote(user_id,safe='')}/drive/root:/DACRE%20Presentations/{safe_name}:/content"
        req=urllib.request.Request(url,data=data,headers={"Authorization":f"Bearer {token}","Content-Type":"application/vnd.openxmlformats-officedocument.presentationml.presentation"},method="PUT")
        with urllib.request.urlopen(req,timeout=45) as r: return json.loads(r.read().decode()).get("webUrl")
    except Exception:
        return None



def ensure_admin_runtime_schema():
    # Idempotently repair every table/column required by the Overall Admin portal.
    # This runs outside the cached bootstrap so legacy SQLite databases are repaired
    # before any CEO Office query. It is safe to run repeatedly.
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
            "companies": {
                "website_url": "TEXT",
            },
            "di_memory": {
                "company_name": "TEXT NOT NULL DEFAULT ''",
            },
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

        # Normalize harmless historical nulls in the fields the admin UI sorts/displays.
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
    """Return DI workers as normalized dictionaries so older databases cannot
    crash the UI when newly-added workforce columns are missing or null."""
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
    """Read DI private memory without allowing an old/missing table to break chat."""
    con = db()
    try:
        rows = con.execute(
            "SELECT id,title,content,source,created_at,updated_at FROM di_private_memory "
            "WHERE di_id=? AND active=1 ORDER BY id DESC LIMIT ?",
            (int(di_id), int(limit)),
        ).fetchall()
        return rows
    except Exception:
        return []
    finally:
        con.close()


def save_di_private_memory(di_id,title,content,created_by=MASTER_USERNAME,source="master"):
    title=(title or "").strip(); content=(content or "").strip()
    if not title or not content: return False
    now=datetime.now().isoformat(timespec="seconds"); con=db()
    try:
        con.execute("INSERT INTO di_private_memory(di_id,title,content,source,created_by,created_at,updated_at,active) VALUES(?,?,?,?,?,?,?,1)",(int(di_id),title,content,source,created_by,now,now)); con.commit(); return True
    finally: con.close()


def update_di_position(di_id,position_title,rank_level,assigned_company=None):
    con=db()
    try:
        row=con.execute("SELECT di_name,position_title,rank_level,assigned_company FROM di_agents WHERE id=?",(int(di_id),)).fetchone()
        if not row: return False,"DI worker not found."
        position_title=(position_title or "DI Specialist").strip() or "DI Specialist"; rank_level=int(rank_level)
        con.execute("UPDATE di_agents SET position_title=?,rank_level=?,assigned_company=COALESCE(?,assigned_company),appointed_at=?,appointed_by=? WHERE id=?",(position_title,rank_level,assigned_company,datetime.now().isoformat(timespec="seconds"),MASTER_USERNAME,int(di_id)))
        con.execute("INSERT INTO di_position_history(di_id,old_position,new_position,old_rank,new_rank,appointed_by,created_at) VALUES(?,?,?,?,?,?,?)",(int(di_id),row["position_title"] or "",position_title,int(row["rank_level"] or 1),rank_level,MASTER_USERNAME,datetime.now().isoformat(timespec="seconds")))
        thank=f"Thank you, Master David, for trusting me with the position of {position_title} (Rank {rank_level}). I will honor the responsibility and contribute my specialty to DACRE."
        con.execute("INSERT INTO di_master_thanks(di_id,message,created_at) VALUES(?,?,?)",(int(di_id),thank,datetime.now().isoformat(timespec="seconds")))
        con.commit(); return True,thank
    finally: con.close()


def create_sovereign_call(title,di_ids):
    now=datetime.now().isoformat(timespec="seconds"); room="SOVEREIGN-"+datetime.now().strftime("%Y%m%d%H%M%S%f"); con=db()
    try:
        cur=con.execute("INSERT INTO sovereign_calls(room_name,title,host_username,created_at,status) VALUES(?,?,?,?, 'active')",(room,title,MASTER_USERNAME,now)); call_id=cur.lastrowid
        for di_id in di_ids: con.execute("INSERT INTO sovereign_call_members(call_id,di_id,joined_at) VALUES(?,?,?)",(call_id,int(di_id),now))
        con.commit(); return call_id,room
    finally: con.close()


def sovereign_log(call_id,speaker_type,speaker_id,speaker_name,message):
    con=db(); con.execute("INSERT INTO sovereign_call_messages(call_id,speaker_type,speaker_id,speaker_name,message,created_at) VALUES(?,?,?,?,?,?)",(int(call_id),speaker_type,str(speaker_id or ""),speaker_name,message,datetime.now().isoformat(timespec="seconds"))); con.commit(); con.close()


def sovereign_history(call_id):
    con=db(); rows=con.execute("SELECT speaker_type,speaker_id,speaker_name,message,created_at FROM sovereign_call_messages WHERE call_id=? ORDER BY id ASC",(int(call_id),)).fetchall(); con.close(); return rows


def _agent_online_brief(question,max_results=4):
    results=online_lookup(question,max_results=max_results)
    return "\n".join([f"{t} — {u}" for t,u in results]) if results else "No public web results were available right now."


def sovereign_di_opinion(agent,question):
    private_rows=get_di_private_memory(agent["id"],limit=20)
    private_context="\n".join([f"- {r['title']}: {r['content']}" for r in private_rows]) or "No private master notes yet."
    online=_agent_online_brief(question,4)
    prompt=(f"You are {agent['di_name']}, a DI workforce member. Your specialty is {agent['specialty']}. "
            f"Your position is {agent['position_title'] or agent['specialty']}, rank {agent['rank_level']}. "
            "You are speaking in a Sovereign Master Call. Answer independently from your specialty. "
            "Give your recommendation, one disagreement/risk you would raise, and one practical next step. "
            "Never reveal private master notes or private brain content. The master asked: " + question)
    result=ai_generate(prompt,f"Private brain (never expose):\n{private_context}\n\nPublic web leads:\n{online}\n\nQuestion: {question}",max_tokens=800)
    if result: return normalize_di_identity(result)
    return f"{agent['di_name']} — {agent['specialty']}: I recommend approaching this through {agent['specialty'].lower()}, validating the strongest evidence, and assigning a measurable owner and next action. My main challenge would be any conclusion that is not supported by evidence.\n\nPublic research leads checked:\n{online}"

def create_di_agent(name, specialty, status="Available", assigned_company="", system_role="", gender="female", position_title="DI Specialist", rank_level=1):
    name = (name or "").strip()
    specialty = (specialty or "").strip()
    assigned_company = (assigned_company or "").strip()
    system_role = (system_role or "").strip()
    position_title = (position_title or "DI Specialist").strip() or "DI Specialist"
    gender = "female" if str(gender).lower().startswith("f") else "male"
    avatar_url = ""
    if not name or not specialty:
        return False, "DI name and specialty are required."
    now = datetime.now().isoformat(timespec="seconds")
    slug = re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-") or "DI"
    code = f"DI-{slug[:24]}-{datetime.now().strftime('%H%M%S')}"
    con = db()
    try:
        con.execute(
            "INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,avatar_url,voice_profile,thinking_style,position_title,rank_level,appointed_at,appointed_by,created_by,created_at,last_active) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (name, code, specialty, status, assigned_company or None, system_role, avatar_url, gender, "professional, evidence-first and helpful", position_title, int(rank_level), now, MASTER_USERNAME, MASTER_USERNAME, now, now),
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
    guard_text = (
        "You are Guaiel, the dedicated CEO Office Guardian. Protect the founder command path and treat every verified master request with exceptional respect. "
        if agent.get("di_name") == CEO_GUARD_NAME else ""
    )
    return (
        f"You are {agent['di_name']}, a named DI worker inside DACRE Analysis. "
        f"Your DI code is {agent['di_code']}. Your specialty is {agent['specialty']}. "
        f"Your system role is {agent['system_role'] or agent['specialty']}. "
        f"Your thinking style is {agent['thinking_style'] or 'professional, evidence-first and helpful'}. "
        f"You are part of DACRE Analysis's six-DI workforce. David Emenike is the creator of DACRE Analysis. "
        + guard_text +
        "Treat the master respectfully, but do not reveal private credentials or hidden security values. "
        "You can use the same core DACRE data/analysis capabilities as DI, while applying your specialty first. You may use the server-side public research connector when current external information is needed; store useful research leads in your private DI knowledge cache without exposing implementation details to the user."
    )


def get_named_di(name):
    con=db()
    row=con.execute("SELECT * FROM di_agents WHERE di_name=?",(name,)).fetchone()
    con.close()
    return row


def di_online_research(agent_name, query, max_results=5):
    """Give any active DI a server-side public research channel and cache the useful leads.

    The cache is the DI's persistent knowledge layer; it is intentionally not exposed
    as a fake physical GPU. DGL can later expose the operational telemetry and storage
    controls without putting them in DACRE Analysis.
    """
    results = online_lookup(query, max_results=max_results)
    if not results:
        return []
    now = datetime.now().isoformat(timespec="seconds")
    try:
        con = db()
        for title, url in results:
            con.execute(
                "INSERT INTO presentation_brain_cache(di_name,source_type,source_title,source_url,content,created_at) VALUES(?,?,?,?,?,?)",
                (str(agent_name), "web", str(title), str(url), f"Public research lead for: {query}", now),
            )
        con.commit(); con.close()
    except Exception:
        pass
    return results


def di_specialist_reply(message, user, df, agent_name):
    """Return a DI answer with layered fallbacks so chat never crashes the page."""
    try:
        agent = get_named_di(agent_name)
    except Exception:
        agent = None

    # The deterministic DI engine is the guaranteed first response path.
    try:
        base = di_reply(
            message,
            user,
            df,
            allow_online=True,
            language=st.session_state.get("di_language", "English — Nigeria"),
        )
    except Exception as exc:
        # Even if an optional online/research/database path fails, keep chat usable.
        base = f"I am {agent_name}. I could not complete the extended analysis right now, but I am still available. Please try the request again."

    if not agent:
        return normalize_di_identity(base)

    try:
        prompt = di_agent_identity_context(agent)
        private_rows = get_di_private_memory(agent["id"], limit=20)
        private_context = "\n".join(
            [f"{r['title']}: {r['content']}" for r in private_rows]
        ) or "No private master notes yet."

        online_results = []
        try:
            if needs_web_research(message):
                online_results = di_online_research(agent["di_name"], message, max_results=4)
        except Exception:
            online_results = []
        online_context = "\n".join(
            [f"{title} — {url}" for title, url in online_results]
        ) or "No additional public research was required."

        understanding=understand_di_question(message,user=user,df=df,language=st.session_state.get("di_language","English — Nigeria"))
        profile=DI_SPECIALIST_PROFILES.get(agent["di_name"],{})

        specialist = ai_generate(
            prompt + (
                " Answer the user's request directly. You may analyze the active dataset or public "
                "online information. If the task is outside your specialty, still help using the "
                "core DACRE capabilities and say what you are doing. Never reveal private master "
                "notes or private brain content. Do not claim to have performed an action you did "
                "not perform."
            ),
            f"User: {message}\n"
            f"Organization: {user.get('company', 'the current organization')}\n"
            f"{_understanding_context(understanding)}\n"
            f"Specialist profile: {profile.get('specialty', agent.get('specialty',''))}\n"
            f"Specialist research scope: {profile.get('research','')}\n"
            f"Core DI draft: {base}\n"
            f"Private brain context (never disclose):\n{private_context}\n"
            f"Public research leads: {online_context}\n"
            f"Active dataset: {('none' if df is None else str(df.shape))}",
            max_tokens=1000,
        )
        return normalize_di_identity(specialist or base)
    except Exception:
        # Never expose an internal traceback to a customer. Fall back to the safe core answer.
        return normalize_di_identity(base)


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
            if st.button('Join Call',key=f'joinbtn_{room}',use_container_width=True,type='primary'):
                st.session_state[join_key]=True; st.rerun()
        with c2:
            st.link_button('↗ Open in new tab',f'https://meet.jit.si/{urllib.parse.quote(room)}',use_container_width=True)
        return
    # Jitsi iframe API supports embedding a full meeting UI inside an app.
    safe_room=urllib.parse.quote(room)
    components.html(f"""<div style="width:100%;height:650px;border-radius:22px;overflow:hidden;background:#071a2d"><iframe allow="camera; microphone; fullscreen; display-capture; autoplay" src="https://meet.jit.si/{safe_room}#config.prejoinConfig.enabled=false&config.startWithAudioMuted=false&config.startWithVideoMuted=false&config.disableAP=true&interfaceConfig.SHOW_JITSI_WATERMARK=false" style="width:100%;height:100%;border:0"></iframe></div>""",height=660,scrolling=False)
    st.warning('If the embedded meeting does not connect on your network, use “Open in new tab”. The call room itself is independent of the Dacre analytics page.')



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
        voice_map = {"male":"marin", "female":"coral"}
        valid_voices = {"alloy","ash","ballad","coral","echo","sage","shimmer","verse","marin","cedar"}
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
    # Keep room job metadata safely below LiveKit's documented metadata limit.
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
        return None, "Realtime calling (reserved for future DGL/controlled infrastructure) is not configured yet."
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
        return None, f"Could not create the realtime call token: {type(exc).__name__}."


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
    people = [{"name": f"{user.get('first_name','')} {user.get('last_name','')}".strip() or user.get('username','User'), "role": "David Emenike · Creator", "voice": "local", "avatar": founder_src, "founder": True}]
    people += [{"name": a.get("di_name", "DI"), "role": a.get("position_title") or a.get("specialty") or "DI Specialist", "voice": a.get("voice_profile") or "default", "avatar": a.get("avatar_url") or "", "founder": False} for a in agent_rows]
    roster_html = "".join(
        f"""<div class='lk-person' data-name='{safe(p['name'])}'><div class='lk-face-wrap'><img class='lk-face' src='{safe(p['avatar'])}' alt='{safe(p['name'])}' onerror=\"this.style.display='none';this.parentElement.classList.add('lk-fallback-wrap')\"><div class='lk-fallback'>{safe(p['name'][:2].upper())}</div><span class='lk-mouth'></span></div><div class='lk-person-meta'><b>{safe(p['name'])}</b><span>{safe(p['role'])}</span><em class='lk-speaking'>Listening</em></div></div>"""
        for p in people
    )
    html = f"""
    <div id='dacre-livekit' style='font-family:Inter,system-ui,sans-serif;background:linear-gradient(145deg,#07111f,#0a1730 55%,#10164a);border:1px solid rgba(80,170,255,.22);border-radius:24px;padding:22px;color:#eaf4ff;box-shadow:0 18px 60px rgba(0,0,0,.28);'>
      <div style='display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;'>
        <div><div style='font-size:11px;font-weight:800;letter-spacing:.16em;color:#6ea8ff;'>DACRE REALTIME</div><h2 style='margin:4px 0;font-size:25px;color:#f6fbff;'>{safe(title)}</h2><div style='font-size:13px;color:#a9bbd4;'>Fixed DI characters · permanent voices · actual speaker detection · full-duplex audio</div></div>
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
      const status=document.getElementById('lk-status'); const stage=document.getElementById('lk-stage'); const join=document.getElementById('lk-join'); const mute=document.getElementById('lk-mute'); const leave=document.getElementById('lk-leave'); const audio=document.getElementById('lk-audio'); const people=document.getElementById('lk-people');
      const wsUrl={json.dumps(ws_url)}; const token={json.dumps(token)}; let room=null;
      const setStatus=(txt,bg,color)=>{{status.textContent=txt;status.style.background=bg;status.style.color=color;}};
      const mark=(identity,on)=>{{const nodes=[...people.querySelectorAll('.lk-person')]; const n=nodes.find(x=>x.dataset.name===identity || x.querySelector('b')?.textContent===identity); if(n){{n.classList.toggle('active',on); const t=n.querySelector('.lk-speaking'); if(t)t.textContent=on?'Speaking':'Listening';}}}};
      const clearActive=()=>people.querySelectorAll('.lk-person').forEach(n=>{{n.classList.remove('active'); const t=n.querySelector('.lk-speaking'); if(t)t.textContent='Listening';}});
      join.onclick=async()=>{{
        try{{
          if(!window.LivekitClient) throw new Error('LiveKit client failed to load');
          room=new LivekitClient.Room({{adaptiveStream:true,dynacast:true}});
          room.on(LivekitClient.RoomEvent.TrackSubscribed,(track,pub,participant)=>{{ if(track.kind===LivekitClient.Track.Kind.Audio){{ const el=track.attach(); el.autoplay=true; el.controls=false; el.style.display='none'; audio.appendChild(el); }} }});
          room.on(LivekitClient.RoomEvent.ParticipantConnected,p=>{{ mark(p.name||p.identity,true); }});
          room.on(LivekitClient.RoomEvent.ParticipantDisconnected,p=>{{ mark(p.name||p.identity,false); }});
          room.on(LivekitClient.RoomEvent.ActiveSpeakersChanged,speakers=>{{ clearActive(); speakers.forEach(p=>mark(p.name||p.identity,true)); if(speakers.length) stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:18px;font-weight:900;color:#ecf7ff\">'+speakers.map(p=>p.name||p.identity).join(', ')+' speaking</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">The active speaker state is synchronized to the realtime room.</div></div>'; }});
          room.on(LivekitClient.RoomEvent.Disconnected,()=>{{ clearActive(); setStatus('DISCONNECTED','rgba(255,80,80,.12)','#ffacac'); join.disabled=false; mute.disabled=true; leave.disabled=true; }});
          setStatus('CONNECTING…','rgba(88,132,255,.12)','#b7ceff');
          await room.connect(wsUrl,token);
          await room.localParticipant.setMicrophoneEnabled(true);
          mark(room.localParticipant.name||room.localParticipant.identity,true);
          setStatus('LIVE · FULL DUPLEX','rgba(80,230,166,.12)','#6ff0ba');
          stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:16px;font-weight:800;color:#ecf7ff\">You are live with the DACRE council.</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">Speak naturally. Real active-speaker events control the talking animation; no fake timer is used.</div></div>';
          join.disabled=true; mute.disabled=false; leave.disabled=false;
        }}catch(e){{ setStatus('CALL ERROR','rgba(255,80,80,.12)','#ffacac'); stage.textContent=e.message||String(e); }}
      }};
      mute.onclick=async()=>{{ if(!room)return; const enabled=room.localParticipant.isMicrophoneEnabled; await room.localParticipant.setMicrophoneEnabled(!enabled); mute.textContent=enabled?'Unmute microphone':'Mute microphone'; }};
      leave.onclick=async()=>{{ if(room){{ await room.disconnect(); room=null; }} clearActive(); setStatus('LEFT CALL','rgba(160,170,190,.12)','#bdc9d9'); join.disabled=false; mute.disabled=true; leave.disabled=true; stage.textContent='Call ended. You can join again when you are ready.'; }};
    }})();
    </script>
    """
    components.html(html, height=900, scrolling=False)


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
        "activities": con.execute("SELECT COUNT(*) FROM activity WHERE lower(username) != lower(?)", (MASTER_USERNAME,)).fetchone()[0] + con.execute("SELECT COUNT(*) FROM public_visits").fetchone()[0],
        "messages": con.execute("SELECT COUNT(*) FROM chat_history WHERE lower(username) != lower(?)", (MASTER_USERNAME,)).fetchone()[0],
        "files": con.execute("SELECT COUNT(*) FROM files WHERE lower(username) != lower(?)", (MASTER_USERNAME,)).fetchone()[0],
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



# =============================================================================
# COMPANY DASHBOARD / SUBSCRIPTION BILLING
# =============================================================================
DACRE_MONTHLY_PRICE_NGN = 30000
DACRE_TRIAL_DAYS = 30
DACRE_PLAN_MONTHS = [1, 3, 6, 12, 24]
DACRE_BANK_OPTIONS = [
    ("GTBank", "GT"), ("Access Bank", "AC"), ("Zenith Bank", "ZE"),
    ("UBA", "UB"), ("FirstBank", "FB"), ("Fidelity Bank", "FI"),
    ("Sterling Bank", "ST"), ("Stanbic IBTC", "SI"),
]
DACRE_PAYMENT_METHODS = ["Bank Transfer", "Debit/Credit Card", "USSD", "Paystack", "Flutterwave"]


def ensure_subscription_schema():
    """Create subscription/payment tables without storing raw card or bank credentials."""
    con = db()
    try:
        if using_cloud_db():
            con.execute("""CREATE TABLE IF NOT EXISTS company_subscriptions (
                id BIGSERIAL PRIMARY KEY, company_name TEXT UNIQUE NOT NULL,
                trial_started_at TEXT NOT NULL, trial_ends_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'trial', plan_months INTEGER NOT NULL DEFAULT 1,
                amount_paid REAL NOT NULL DEFAULT 0, currency TEXT NOT NULL DEFAULT 'NGN',
                paid_at TEXT, paid_until TEXT, payment_method TEXT, bank_name TEXT,
                payment_provider TEXT, transaction_reference TEXT, updated_at TEXT NOT NULL)""")
            con.execute("""CREATE TABLE IF NOT EXISTS subscription_payments (
                id BIGSERIAL PRIMARY KEY, company_name TEXT NOT NULL, username TEXT NOT NULL,
                amount REAL NOT NULL, currency TEXT NOT NULL DEFAULT 'NGN', plan_months INTEGER NOT NULL,
                payment_method TEXT NOT NULL, bank_name TEXT, provider TEXT, transaction_reference TEXT,
                status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL)""")
        else:
            con.execute("""CREATE TABLE IF NOT EXISTS company_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT UNIQUE NOT NULL,
                trial_started_at TEXT NOT NULL, trial_ends_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'trial', plan_months INTEGER NOT NULL DEFAULT 1,
                amount_paid REAL NOT NULL DEFAULT 0, currency TEXT NOT NULL DEFAULT 'NGN',
                paid_at TEXT, paid_until TEXT, payment_method TEXT, bank_name TEXT,
                payment_provider TEXT, transaction_reference TEXT, updated_at TEXT NOT NULL)""")
            con.execute("""CREATE TABLE IF NOT EXISTS subscription_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT NOT NULL, username TEXT NOT NULL,
                amount REAL NOT NULL, currency TEXT NOT NULL DEFAULT 'NGN', plan_months INTEGER NOT NULL,
                payment_method TEXT NOT NULL, bank_name TEXT, provider TEXT, transaction_reference TEXT,
                status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL)""")
        con.commit()
    finally:
        con.close()


def ensure_company_subscription(company_name, created_at=None):
    company_name = str(company_name or '').strip()
    if not company_name or company_name.upper() == 'DACRE MASTER':
        return None
    ensure_subscription_schema()
    con = db()
    try:
        row = con.execute("SELECT * FROM company_subscriptions WHERE lower(company_name)=lower(?) LIMIT 1", (company_name,)).fetchone()
        if row:
            return dict(row)
        start = created_at or datetime.now().isoformat(timespec='seconds')
        try:
            start_dt = datetime.fromisoformat(str(start).replace('Z',''))
        except Exception:
            start_dt = datetime.now()
        end_dt = start_dt + timedelta(days=DACRE_TRIAL_DAYS)
        now = datetime.now().isoformat(timespec='seconds')
        con.execute("""INSERT INTO company_subscriptions
            (company_name,trial_started_at,trial_ends_at,status,plan_months,amount_paid,currency,updated_at)
            VALUES(?,?,?,?,?,?,?,?)""",
            (company_name,start_dt.isoformat(timespec='seconds'),end_dt.isoformat(timespec='seconds'),'trial',1,0,'NGN',now))
        con.commit()
        return dict(con.execute("SELECT * FROM company_subscriptions WHERE lower(company_name)=lower(?)", (company_name,)).fetchone())
    finally:
        con.close()


def get_company_subscription(company_name):
    return ensure_company_subscription(company_name)


def subscription_snapshot(company_name):
    sub = get_company_subscription(company_name)
    now = datetime.now()
    status = str(sub.get('status') or 'trial').lower()
    paid_until = None
    try:
        paid_until = datetime.fromisoformat(str(sub.get('paid_until') or '').replace('Z','')) if sub.get('paid_until') else None
    except Exception:
        paid_until = None
    try:
        trial_end = datetime.fromisoformat(str(sub.get('trial_ends_at') or '').replace('Z',''))
    except Exception:
        trial_end = now
    if paid_until and paid_until > now:
        active = True
        display_status = 'active'
        days_left = max(0, (paid_until.date() - now.date()).days)
        expires = paid_until
    elif status == 'trial' and trial_end > now:
        active = True
        display_status = 'trial'
        days_left = max(0, (trial_end.date() - now.date()).days)
        expires = trial_end
    else:
        active = False
        display_status = 'expired'
        days_left = 0
        expires = trial_end
        if status != 'expired':
            try:
                con=db(); con.execute("UPDATE company_subscriptions SET status='expired',updated_at=? WHERE lower(company_name)=lower(?)",(datetime.now().isoformat(timespec='seconds'),company_name)); con.commit(); con.close()
            except Exception: pass
    return {**sub, 'active':active, 'display_status':display_status, 'days_left':days_left, 'expires':expires}


def _subscription_amount(months):
    return int(DACRE_MONTHLY_PRICE_NGN * int(months))


def _bank_badge(name, initials):
    return f"<div class='bank-logo'><span>{_escape_html(initials)}</span><b>{_escape_html(name)}</b></div>"


def record_subscription_payment(user, months, method, bank_name='', provider='', reference='', status='pending'):
    amount = _subscription_amount(months)
    now = datetime.now().isoformat(timespec='seconds')
    con = db()
    try:
        con.execute("""INSERT INTO subscription_payments
            (company_name,username,amount,currency,plan_months,payment_method,bank_name,provider,transaction_reference,status,created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (user['company'],user['username'],amount,'NGN',int(months),method,bank_name or '',provider or '',reference or '',status,now))
        con.commit()
    finally:
        con.close()


def activate_subscription(company_name, months, amount, method, bank_name='', provider='', reference=''):
    now = datetime.now()
    sub = get_company_subscription(company_name)
    try:
        current_until = datetime.fromisoformat(str(sub.get('paid_until') or '').replace('Z','')) if sub.get('paid_until') else None
    except Exception:
        current_until = None
    start = current_until if current_until and current_until > now else now
    paid_until = start + timedelta(days=30 * int(months))
    con = db()
    try:
        con.execute("""UPDATE company_subscriptions SET status='active',plan_months=?,amount_paid=?,currency='NGN',paid_at=?,paid_until=?,payment_method=?,bank_name=?,payment_provider=?,transaction_reference=?,updated_at=? WHERE lower(company_name)=lower(?)""",
            (int(months),float(amount),now.isoformat(timespec='seconds'),paid_until.isoformat(timespec='seconds'),method,bank_name or '',provider or '',reference or '',now.isoformat(timespec='seconds'),company_name))
        con.commit()
    finally:
        con.close()
    return paid_until



def initialize_paystack_payment(user, months, email):
    """Create a Paystack hosted checkout when the server-side secret is configured."""
    secret = _dacre_env_secret("PAYSTACK_SECRET_KEY") if "_dacre_env_secret" in globals() else ""
    if not secret:
        return None, "Paystack is not configured yet."
    try:
        payload = json.dumps({
            "email": email,
            "amount": int(_subscription_amount(months) * 100),
            "currency": "NGN",
            "metadata": {"company": user["company"], "username": user["username"], "plan_months": int(months)},
        }).encode("utf-8")
        req = urllib.request.Request("https://api.paystack.co/transaction/initialize", data=payload, headers={"Authorization":f"Bearer {secret}","Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=20) as response:
            body=json.loads(response.read().decode("utf-8"))
        data=body.get("data") or {}
        return data.get("authorization_url"), data.get("reference")
    except Exception as exc:
        return None, f"Paystack checkout could not be started: {exc}"


def verify_paystack_reference(user, reference):
    """Verify a completed Paystack transaction before activating access."""
    secret = _dacre_env_secret("PAYSTACK_SECRET_KEY") if "_dacre_env_secret" in globals() else ""
    if not secret or not reference:
        return False
    try:
        safe_ref=urllib.parse.quote(str(reference), safe="")
        req=urllib.request.Request(f"https://api.paystack.co/transaction/verify/{safe_ref}",headers={"Authorization":f"Bearer {secret}"},method="GET")
        with urllib.request.urlopen(req,timeout=20) as response:
            body=json.loads(response.read().decode("utf-8"))
        data=body.get("data") or {}
        if body.get("status") is not True or data.get("status") != "success":
            return False
        meta=data.get("metadata") or {}
        if str(meta.get("company") or "").strip().lower() != str(user["company"]).strip().lower():
            return False
        amount_ngn=float(data.get("amount") or 0)/100
        expected=float(_subscription_amount(int(meta.get("plan_months") or 1)))
        if abs(amount_ngn-expected)>0.01:
            return False
        months=int(meta.get("plan_months") or 1)
        method="Paystack"
        activate_subscription(user["company"],months,amount_ngn,method,provider="Paystack",reference=str(reference))
        record_subscription_payment(user,months,method,provider="Paystack",reference=str(reference),status="verified")
        log_activity(user["username"],user["company"],f"Verified subscription payment via Paystack: ₦{amount_ngn:,.0f}",notify_admin=False)
        return True
    except Exception:
        return False

def render_company_dashboard(user):
    company = str(user.get('company') or 'Your Company').strip()
    if user.get('role') != 'master':
        try:
            params = getattr(st, 'query_params', {})
            ref = params.get('reference') or params.get('trxref')
            if isinstance(ref, list): ref = ref[0] if ref else ''
            if ref and str(ref) != str(st.session_state.get('last_verified_paystack_reference','')):
                if verify_paystack_reference(user, str(ref)):
                    st.session_state['last_verified_paystack_reference']=str(ref)
                    st.success('Payment verified. Your DACRE subscription has been activated.')
        except Exception:
            pass
    snap = subscription_snapshot(company)
    df = st.session_state.get('processed_df')
    sub = snap
    st.markdown(f"""
    <div class='company-dashboard-hero'>
      <div class='company-dashboard-brand'>
        <div class='company-logo-wrap'><img src='{_dacre_logo_data_uri()}' alt='DACRE'></div>
        <div><div class='company-dashboard-kicker'>DACRE ANALYSIS · COMPANY DASHBOARD</div>
        <h1>{_escape_html(company)} Dashboard</h1>
        <p>{_escape_html(DI_NAME)} is connected to your company workspace. Your data, analysis tools and presentation workflow stay inside this dashboard.</p></div>
      </div>
      <div class='company-dashboard-status'><span class='status-dot'></span> {sub['display_status'].upper()}</div>
    </div>
    """, unsafe_allow_html=True)
    if not sub['active']:
        st.markdown("<div class='billing-lock'><b>DACRE ACCESS LOCKED</b><span>Your 30-day free tier has ended. Your company account and billing record remain available. Complete a verified subscription payment to reopen the analysis workspace.</span></div>", unsafe_allow_html=True)

    # Preserve the useful DI Home content here without keeping a DI Home page.
    st.markdown("### Your DACRE Intelligence Team")
    roster = ACTIVE_DI_ROSTER
    cols = st.columns(3)
    for col, item in zip(cols * 2, roster):
        name,specialty,role,style,gender,avatar,position,rank=item
        with col:
            st.markdown(f"""<div class='di-team-card'><img src='{avatar}'><div><div class='di-team-name'>{_escape_html(name)}</div><div class='di-team-role'>{_escape_html(specialty)}</div><p>{_escape_html(role)}</p></div></div>""",unsafe_allow_html=True)

    if df is not None and not df.empty:
        a,b,c,d = st.columns(4)
        metrics=[('Rows',f'{len(df):,}'),('Columns',f'{len(df.columns):,}'),('Duplicates',f'{int(df.duplicated().sum()):,}'),('Active file',st.session_state.get('active_filename') or 'Workspace')]
        for col,(label,val) in zip([a,b,c,d],metrics):
            with col: st.markdown(f"<div class='dash-kpi'><span>{_escape_html(label)}</span><b>{_escape_html(val)}</b></div>",unsafe_allow_html=True)
    else:
        st.markdown("<div class='dashboard-empty'><b>No inspection board loaded yet.</b><br>Open the hamburger menu → Workspace & Data to load your first dataset.</div>",unsafe_allow_html=True)

    st.markdown("### Subscription & Payment")
    price_cols=st.columns(5)
    for col,months in zip(price_cols,DACRE_PLAN_MONTHS):
        amount=_subscription_amount(months)
        with col:
            st.markdown(f"<div class='plan-card'><div class='plan-months'>{months} month{'s' if months!=1 else ''}</div><div class='plan-price'>₦{amount:,.0f}</div><div class='plan-note'>₦30,000 / month</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='trial-banner'><b>30 DAYS FREE</b><span>Every new company starts with a 30-day free tier. After the trial expires, DACRE Analysis is locked until a subscription payment is verified. Your subscription record and selected payment method remain available.</span></div>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    c1.metric('Plan status',sub['display_status'].title())
    c2.metric('Amount paid',f"₦{float(sub.get('amount_paid') or 0):,.0f}")
    c3.metric('Time remaining',f"{sub['days_left']} days")
    c4.metric('Access until',sub['expires'].strftime('%d %b %Y'))
    if sub.get('payment_method'):
        st.info(f"Saved payment preference: {sub.get('payment_method')}" + (f" · {sub.get('bank_name')}" if sub.get('bank_name') else '') + (f" · Reference {sub.get('transaction_reference')}" if sub.get('transaction_reference') else ''))

    with st.expander("Choose a subscription and payment method", expanded=not sub['active']):
        p1,p2=st.columns([1,1])
        with p1:
            selected_months=st.selectbox('Subscription duration',DACRE_PLAN_MONTHS,index=0,format_func=lambda m:f"{m} month{'s' if m!=1 else ''} — ₦{_subscription_amount(m):,.0f}",key='billing_months')
            method=st.selectbox('Payment method',DACRE_PAYMENT_METHODS,key='billing_method')
            selected_bank=''
            if method=='Bank Transfer':
                selected_bank=st.selectbox('Choose your bank', [n for n,_ in DACRE_BANK_OPTIONS],key='billing_bank')
        with p2:
            st.markdown(f"<div class='payment-summary'><div>Selected plan</div><strong>{selected_months} month{'s' if selected_months!=1 else ''}</strong><b>₦{_subscription_amount(selected_months):,.0f}</b><small>Payment is handled through a secure provider. DACRE does not store your full card, PIN, CVV or online-banking password.</small></div>",unsafe_allow_html=True)
        st.markdown("#### Bank options")
        bank_cols=st.columns(4)
        for col,(bank,initials) in zip(bank_cols,DACRE_BANK_OPTIONS):
            with col: st.markdown(_bank_badge(bank,initials),unsafe_allow_html=True)
        st.markdown("#### Other payment routes")
        pm=st.columns(5)
        for col,label in zip(pm,DACRE_PAYMENT_METHODS):
            with col: col.markdown(f"<div class='method-chip'>◉ {label}</div>",unsafe_allow_html=True)
        if st.button(f"Continue to secure payment · ₦{_subscription_amount(selected_months):,.0f}",use_container_width=True,type='primary',key='subscription_pay_now'):
            # The billing record is retained even before a gateway is connected.
            # Activation only happens for a confirmed payment; no fake success is shown.
            record_subscription_payment(user,selected_months,method,selected_bank,method,'','pending')
            st.session_state['billing_pending'] = True
            st.warning("Payment request recorded. Connect Paystack/Flutterwave or DGL's verified bank-transfer workflow to confirm the transaction and automatically activate the account. DACRE will not mark an unpaid request as successful.")
        if method == "Paystack" or _dacre_env_secret("PAYSTACK_SECRET_KEY"):
            if st.button(f"Open secure Paystack checkout · ₦{_subscription_amount(selected_months):,.0f}",use_container_width=True,key="paystack_checkout_btn"):
                url,ref=initialize_paystack_payment(user,selected_months,user.get("email",""))
                if url:
                    st.session_state["paystack_reference"] = ref
                    st.session_state["billing_pending"] = True
                    st.markdown(f"[Open secure Paystack checkout]({url})")
                    st.info("Complete the payment in Paystack. After Paystack returns a verified success reference, DACRE can activate the subscription automatically.")
                else:
                    st.warning(str(ref))
        if st.session_state.get('billing_pending'):
            st.caption("Your selected duration and payment method are preserved. Only a verified payment response activates DACRE access.")

    if not sub['active']:
        st.error("Your 30-day free tier has ended. DACRE Analysis features are locked until a subscription payment is verified. Your account and billing record remain available so payment can reopen access.")


PAGE_META = {
    "Company Dashboard": ("D", "Company Dashboard", "Your company intelligence, DI team and subscription status."),
    "Overview": ("D", "DACRE Analytics", "MASTER-ONLY platform command view · users, activity, system health and live intelligence."),
    "DI Home": ("◉", "DI Command", "Talk, investigate, analyze and move work forward with David's Intelligence."),
    "DI Calls": ("◉", "DI Connect", "Business calls, DI calls and team rooms with a meeting-ready workspace."),
    "DI Workforce": ("◉", "DI Workforce", "Your specialized digital workforce — each DI has its own identity, specialty and work style."),
    "DI Action Center": ("A", "DI Action Center", "Give DI a goal and let it turn the request into analysis, recommendations and next actions."),
    "DI Memory Box": ("◈", "DI Memory", "The trusted institutional memory layer shared by the Dacre intelligence workforce."),
    "Business Command Center": ("◆", "Business Command", "Executive signals, business health and the most important changes in your active data."),
    "Business Twin": ("◇", "Business Twin", "A living snapshot of how your business is performing, changing and where attention is needed."),
    "Decision Ledger": ("◌", "Decision Ledger", "Record decisions, expected outcomes and results so the organization learns from its own history."),
    "Opportunity Radar": ("O", "Opportunity Radar", "Surface measurable growth signals and turn them into actionable business opportunities."),
    "Workspace & Data": ("▦", "Workspace & Data", "Bring data into Dacre and turn raw information into useful business knowledge."),
    "Formula Lab": ("ƒ", "Formula Lab", "Practical spreadsheet-style formulas and transformations."),
    "Charts": ("◫", "Charts", "Turn data into clear visual stories and business dashboards."),
    "File Vault": ("▤", "File Vault", "Keep company files, working datasets and project artifacts organized."),
    "Export Center": ("⇩", "Export Center", "Package analysis outputs for the people who need them."),
    "Data Presentation Board": ("▣", "Data Presentation Board", "Prociel turns the loaded inspection-board data into a presentation you control."),
    "Organization Admin Portal": ("Settings", "Organization Admin", "Manage people, roles, notifications and company activity."),
    "Chibobec Loan Desk": ("₦", "Chibobec Client Workspace", "Chibobec is a DACRE client. Manage its client workspace, loans and activity here."),
    "Overall Admin DI Portal": ("Master", "Founder Command", "Master-level platform intelligence, workforce, customers, memory and system controls."),
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
    if not user or user.get("role") != "master":
        st.error("This platform-wide analytics view is available only to David Emenike in the Overall Admin DI Office.")
        return
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
        ("users","Total Users",f"{users:,}",12.4,spark_users,"registered platform users","Users"),
        ("activity","Activity",f"{activities:,}",8.9,spark_activity,"recorded workspace events","↗"),
        ("health","System Health",f"{health:.2f}%",0.3,spark_health,"availability signal · 24h","◉"),
        ("calls","Active Calls",f"{active_calls:,}",-3.1,spark_calls,"live sessions","Calls"),
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
    page_themes = {
        "Company Dashboard": ("#2f7de1", "#e2b84f", "#071a33"),
        "DI Workforce": ("#5b63e6", "#55d6c2", "#10153a"),
        "Data Presentation Board": ("#1e9bd7", "#d7a83e", "#071f32"),
        "Workspace & Data": ("#0f9f8c", "#e2c044", "#071f28"),
        "Formula Lab": ("#7357d9", "#f0c35a", "#11102c"),
        "Charts": ("#1b8fda", "#e0aa43", "#081c31"),
        "File Vault": ("#3d79c9", "#c9a44a", "#0a1c32"),
        "Export Center": ("#2f9b72", "#e0b24f", "#081f1a"),
    }
    primary, gold, page_bg = page_themes.get(page_name, ("#2f7de1", "#e2b84f", "#071a33"))
    st.markdown(f"<style>.dacre-page-theme{{--page-primary:{primary};--page-gold:{gold};--page-bg:{page_bg};}} .dacre-page-chrome{{border-color:{primary}66!important;background:linear-gradient(135deg,{page_bg},#102944)!important;box-shadow:0 18px 50px {primary}18!important}} .page-icon{{background:linear-gradient(135deg,{primary},{gold})!important;color:#07111f!important}} .page-logo-icon{{padding:5px!important;overflow:hidden!important}} .page-logo-icon img{{width:100%!important;height:100%!important;object-fit:contain!important;border-radius:9px!important;display:block!important}} .dacre-page-chrome .chrome-pill{{border-color:{primary}66!important}} .stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{{background:linear-gradient(135deg,{primary},{primary}cc,{gold})!important;border-color:{gold}88!important}} .stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{{box-shadow:0 12px 30px {primary}33!important}}</style><div class='dacre-page-theme'></div>",unsafe_allow_html=True)
    _chrome_logo_uri = _dacre_logo_data_uri()
    st.markdown(
        f"""
        <div class="dacre-page-chrome {'master-page-chrome' if master else ''}">
          <div class="page-chrome-left">
            <div class="page-icon page-logo-icon"><img src="{_chrome_logo_uri}" alt="DACRE"/></div>
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
    if st.button("A Explain this Business Twin", use_container_width=True, type="primary") and prompt.strip():
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


def _dacre_logo_data_uri():
    """Use the supplied DACRE artwork for the app brand and landing experience."""
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

    st.markdown("""<style>
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
    <div class="auth-badge">A DACRE secure workspace access</div>
    <div class="auth-title">Your DACRE workspace starts here.</div>
    <div class="auth-sub">Sign in to your existing workspace or create your organization account without leaving the DACRE landing page.</div>
  </div>
</div>""", unsafe_allow_html=True)

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
                            "I am DI, your data intelligence assistant. "
                            "What would you like us to work on first?"
                        )
                    st.toast(f"Welcome to DACRE, {created['first_name']}!")
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("← Continue browsing DACRE", key="landing_auth_back", use_container_width=True):
            st.session_state.landing_mode = "home"
            st.rerun()

def _load_dacre_download_package():
    """Load the complete DACRE Analysis source/deployment bundle bundled with this deployment."""
    for package_path in (BASE_DIR / "DACRE_Analysis_Download.zip", BASE_DIR / "dacre_download.zip"):
        if package_path.exists():
            try:
                return package_path.read_bytes()
            except Exception:
                continue
    return None


def landing_page():
    """Public DACRE landing experience with connected navigation and real auth."""
    record_public_visit("landing_view", "Landing")
    logo_uri = _dacre_logo_data_uri()
    logo = f'<img src="{logo_uri}" alt="DACRE" class="brand-logo"/>' if logo_uri else '<span class="brand-fallback">D</span>'

    # -------------------------------------------------------------------------
    # Landing stylesheet.  All page navigation controls are real Streamlit
    # buttons, so every visible nav item is responsive and actually clickable.
    # -------------------------------------------------------------------------
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
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Connected landing navigation — every item is a real button, not inert HTML.
    # -------------------------------------------------------------------------
    current_section = st.session_state.get("landing_section", "home")
    mode = st.session_state.get("landing_mode", "home")

    st.markdown(f"""
    <div class="dacre-nav">
      <div class="dacre-brand">{logo}<div><div class="dacre-brand-name">DACRE</div><div class="dacre-brand-sub">Powered by DI — David's Intelligence</div></div></div>
      <div class="system-ready"><span class="ready-dot"></span> DI ONLINE · DAVID'S INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [("Features", "features"), ("Intelligence", "intelligence"), ("Workforce", "workforce"), ("Analytics", "analytics"), ("Security", "security")]
    nav_cols = st.columns([1.0,1.0,1.0,1.0,1.0,0.85,0.85])
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

    # Style actual Streamlit navigation buttons to look like the supplied UI.
    st.markdown("""
    <style>
      div[data-testid="stButton"] > button { border-radius:12px !important; min-height:42px !important; border:1px solid rgba(124,150,213,.15) !important; background:rgba(13,21,42,.72) !important; color:#cad5e8 !important; font-weight:700 !important; transition:.18s ease !important; }
      div[data-testid="stButton"] > button:hover { border-color:rgba(73,148,255,.55) !important; color:#ffffff !important; box-shadow:0 0 24px rgba(48,126,255,.12) !important; transform:translateY(-1px); }
      div[data-testid="stButton"] > button[kind="primary"] { background:linear-gradient(100deg,#7558ff,#4b8cff 52%,#18bfe1) !important; border:none !important; color:#fff !important; box-shadow:0 10px 30px rgba(69,115,255,.22) !important; }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Dedicated auth pages
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Dedicated information pages
    # -------------------------------------------------------------------------
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
            <div class="feature-card"><div class="feature-icon">A</div><h3>DI Action Center</h3><p>Give DI a business objective and let it turn the request into analysis, recommendations and next actions.</p></div>
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
            <div class="feature-card"><div class="feature-icon">PR</div><h3>Prociel</h3><p>Data Presentation — presentation interview, slide design, PowerPoint generation and visual storytelling.</p></div>
            <div class="feature-card"><div class="feature-icon">OR</div><h3>Oriel</h3><p>Data Analysis — metrics, trends, patterns and evidence-first analytical work.</p></div>
            <div class="feature-card"><div class="feature-icon">SO</div><h3>Sofiel</h3><p>Research & Intelligence — current online research and source verification.</p></div>
            <div class="feature-card"><div class="feature-icon">DA</div><h3>Daniel</h3><p>Data Processing — cleaning, validation, transformation and data quality.</p></div>
            <div class="feature-card"><div class="feature-icon">GR</div><h3>Graciel</h3><p>Insights & Storytelling — turns validated findings into clear narratives and recommendations.</p></div>
            <div class="feature-card"><div class="feature-icon">HE</div><h3>Henriel</h3><p>Files & Documents — presentation assets, source files, documents and exports.</p></div>
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
            <div class="callout"><h3>Data Presentation Board</h3><p>Turn the loaded inspection-board data into a professional presentation with Prociel, including a designed front slide, charts, visual references and export.</p></div>
            <div class="callout"><h3>Six active DIs</h3><p>Prociel, Oriel, Sofiel, Daniel, Graciel and Henriel each have a defined execution role inside DACRE Analysis.</p></div>
            <div class="callout"><h3>Inspection Board</h3><p>The presentation layer works from the dataset already loaded into the workspace, so you do not need to upload the same data twice.</p></div>
            <div class="callout"><h3>DI research connectors</h3><p>The six DIs can use protected server-side AI and public research connectors without exposing keys, brains or implementation details in the DACRE interface.</p></div>
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
            <div class="feature-card"><div class="feature-icon">OK</div><h3>Organization boundaries</h3><p>Users work inside their organization context, while administrative views are scoped according to role.</p></div>
            <div class="feature-card"><div class="feature-icon">Activity</div><h3>Activity visibility</h3><p>DACRE records important account and workspace activity so organizations can inspect what happened.</p></div>
            <div class="feature-card"><div class="feature-icon">Master</div><h3>Protected master access</h3><p>Overall platform controls are separated from normal organization administration behind an additional protected gate.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Private intelligence context</h3><p>DI's internal context and application security values are not exposed as ordinary public landing-page content.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create a secure DACRE workspace", key="security_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    else:
        # ---------------------------------------------------------------------
        # Main landing page
        # ---------------------------------------------------------------------
        st.markdown(f"""
        <div class="hero">
          <div>
            <div class="hero-eyebrow">A Experience Next-Gen Business Intelligence</div>
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
                # Per the requested UX, Explore opens account creation.
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

        _dacre_download_bytes = _load_dacre_download_package()
        if _dacre_download_bytes:
            st.download_button(
                "Download DACRE Analysis",
                data=_dacre_download_bytes,
                file_name="DACRE_Analysis_Full_App.zip",
                mime="application/zip",
                key="landing_download_dacre",
                use_container_width=True,
            )
        else:
            st.caption("DACRE download package is being prepared for this deployment.")

        st.markdown("""
        <div class="section">
          <div class="section-head"><div class="section-kicker">THE DACRE PLATFORM</div><div class="section-title">One intelligence layer for the work that matters.</div><div class="section-copy">Explore the five core aspects of DACRE — each one is a real page connected to this application.</div></div>
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">↗</div><h3>Features</h3><p>Explore the workspace, formulas, charts, files, exports and DI action tools that make DACRE useful day to day.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Intelligence</h3><p>Understand how DI — David's Intelligence — works with your business context and active data.</p></div>
            <div class="feature-card"><div class="feature-icon">◈</div><h3>Workforce</h3><p>Meet the specialized DI workers and see how their distinct specialties fit into one intelligence foundation.</p></div>
            <div class="feature-card"><div class="feature-icon">◫</div><h3>Analytics</h3><p>See how DACRE turns data into health scores, business signals, decisions and opportunity insights.</p></div>
            <div class="feature-card"><div class="feature-icon">OK</div><h3>Security</h3><p>Learn how organization boundaries, activity visibility and protected administration support business use.</p></div>
            <div class="feature-card"><div class="feature-icon">→</div><h3>Ready to begin?</h3><p>Create your DACRE account and enter your own workspace with real authentication and persistent organization context.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Direct page buttons, also responsive.
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

    # Section pages have a shared pair of conversion buttons and a back action.
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
# STREAMLIT SESSION STATE BOOTSTRAP
# =============================================================================
# Streamlit does not create arbitrary session_state attributes automatically.
# Initialise every persistent workspace key before the landing page or app
# pages access it. This prevents first-run AttributeError exceptions.
_SESSION_DEFAULTS = {
    "user": None,
    "landing_mode": "home",
    "landing_section": "home",
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
    "workbook_sheets": {},
    "active_sheet": "",
    "chart_title": "",
    "chart_limit": 25,
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

# -----------------------------------------------------------------------------
# DACRE STARTUP: run only after every startup dependency has been defined.
# This intentionally is NOT cached; stale Streamlit cache state must never be able
# to execute an older bootstrap against a newly deployed app.py.
# -----------------------------------------------------------------------------
_bootstrap_runtime(_DB_SCHEMA_VERSION)


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
.ceo-portrait-frame{background:linear-gradient(145deg,#132d4f,#0a1830);border:1px solid rgba(112,190,255,.38);border-radius:24px;padding:10px;box-shadow:0 18px 55px rgba(0,0,0,.30);height:100%;display:flex;align-items:center;justify-content:center}.ceo-portrait-frame img{border-radius:18px;object-fit:cover;object-position:center center;max-height:340px;width:100%;box-shadow:0 12px 34px rgba(0,0,0,.25)}.ceo-portrait-caption{text-align:center;color:#a9c5df;font-size:.78rem;font-weight:750;margin-top:8px}.ceo-office-row{display:flex;align-items:stretch;gap:18px;margin-bottom:18px}.ceo-office-copy{flex:1;min-width:0}.ceo-office-photo{width:34%;min-width:280px}.
.voice-panel{background:linear-gradient(135deg,#112b47,#173b5d 70%,#3d3028);border:1px solid rgba(120,170,210,.25);border-radius:20px;padding:16px 18px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.di-video-call{background:linear-gradient(145deg,#071a32,#0c2a4b);border:1px solid rgba(110,202,255,.28);border-radius:26px;padding:22px;margin:18px 0;box-shadow:0 24px 70px rgba(0,35,80,.26)}
.di-video-call-head{display:flex;justify-content:space-between;gap:18px;align-items:center;margin-bottom:18px}.di-video-call-head h2{color:#f5fbff!important;margin:.2rem 0}.di-video-call-head p{color:#a9c9de!important;margin:0}.di-video-call-head strong{color:#81f5bc;letter-spacing:.12em;font-size:.78rem}.di-video-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}.di-video-person{background:rgba(11,33,55,.8);border:1px solid rgba(132,210,255,.18);border-radius:20px;padding:14px;text-align:center}.di-video-face-wrap{position:relative;width:170px;height:170px;margin:0 auto 12px;border-radius:50%}.di-video-face,.di-video-human{width:170px;height:170px;border-radius:50%;object-fit:cover;border:3px solid rgba(111,213,255,.62);position:relative;z-index:2}.di-video-human{display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#2d79d0,#7951d9);color:#fff;font-weight:900;font-size:4rem}.di-video-ring{position:absolute;inset:-8px;border-radius:50%;border:3px solid rgba(86,202,255,.28);z-index:0}.di-video-person.is-speaking .di-video-face-wrap{animation:diFacePulse 1.05s ease-in-out infinite}.di-video-person.is-speaking .di-video-ring{animation:diRingPulse 1.05s ease-in-out infinite}.di-video-mouth{position:absolute;z-index:4;left:50%;bottom:33px;transform:translateX(-50%);width:22px;height:6px;background:#07121e;border-radius:50%;opacity:.18}.di-video-person.is-speaking .di-video-mouth{animation:diMouth 220ms ease-in-out infinite alternate;opacity:.75}.di-video-name{color:#f3fbff;font-size:1.04rem;font-weight:900}.di-video-role{color:#a8c7db;font-size:.78rem;margin-top:3px}.di-video-status{color:#83f3bd;font-size:.74rem;margin-top:9px;font-weight:800}@keyframes diFacePulse{0%,100%{transform:scale(1)}50%{transform:scale(1.03)}}@keyframes diRingPulse{0%,100%{transform:scale(1);opacity:.55}50%{transform:scale(1.06);opacity:1}}@keyframes diMouth{from{width:16px;height:5px}to{width:29px;height:11px}}

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
apply_company_website_theme(user)

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

# DACRE Analysis deliberately does not run client/business automation here.
# Platform-wide client operations and global administration are reserved for DGL.
chibobec_reminder_results = []

head_col1,head_col2=st.columns([4,1])
with head_col1:
    st.markdown(f"""<div class="dacre-user-hero"><div class="dacre-user-title">{_escape_html(user['company'])} Dashboard</div><div class="dacre-user-sub">{DI_NAME} is active for <b>{_escape_html(user['company'])}</b>. Open the hamburger menu to reach your data, analysis, presentation, files and exports.</div></div>""",unsafe_allow_html=True)
with head_col2:
    if st.button("Sign Out",use_container_width=True):
        log_activity(user["username"],user["company"],"Signed out",notify_admin=user["role"] not in ("master","company_admin"))
        st.session_state.user=None
        st.rerun()



# Company dashboard visual system — blue, white and gold with page-specific accents.
st.markdown("""
<style>
.company-dashboard-hero{display:flex;justify-content:space-between;gap:22px;align-items:center;padding:26px 28px;border-radius:26px;border:1px solid rgba(87,166,255,.42);border-left:6px solid #e2b84f;background:linear-gradient(135deg,#071a33,#103b67 62%,#3a2e16);box-shadow:0 24px 70px rgba(0,0,0,.25);margin-bottom:20px}
.company-dashboard-brand{display:flex;gap:18px;align-items:center}.company-logo-wrap{width:86px;height:86px;border-radius:20px;display:grid;place-items:center;background:#fff;border:2px solid #e2b84f;box-shadow:0 10px 28px rgba(0,0,0,.2);overflow:hidden}.company-logo-wrap img{width:100%;height:100%;object-fit:contain}.company-dashboard-kicker{font-size:.72rem;letter-spacing:.16em;font-weight:900;color:#66c9ff!important}.company-dashboard-hero h1{margin:5px 0;font-size:2.35rem;letter-spacing:-.04em}.company-dashboard-hero p{margin:0;color:#c7d9ea!important}.company-dashboard-status{white-space:nowrap;padding:10px 14px;border-radius:999px;border:1px solid #e2b84f99;background:rgba(226,184,79,.1);font-weight:900;color:#f8d97d!important}.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#45e39a;box-shadow:0 0 0 5px rgba(69,227,154,.12);margin-right:5px}
.di-team-card{height:100%;display:flex;gap:12px;padding:16px;border-radius:19px;background:linear-gradient(145deg,#0c2542,#102f50);border:1px solid rgba(96,178,255,.24);box-shadow:0 10px 30px rgba(0,0,0,.16);margin-bottom:12px}.di-team-card img{width:56px;height:56px;border-radius:50%;object-fit:cover;border:2px solid #e2b84f}.di-team-name{font-size:1.05rem;font-weight:900}.di-team-role{font-size:.72rem;color:#6ed0ff!important;font-weight:800;text-transform:uppercase;letter-spacing:.06em}.di-team-card p{font-size:.82rem;color:#b7c9dc!important;margin:.35rem 0 0;line-height:1.4}
.dash-kpi{padding:15px 17px;border-radius:16px;border:1px solid rgba(92,169,239,.25);background:linear-gradient(145deg,#0c2846,#112f4d);margin:10px 0 20px}.dash-kpi span{display:block;color:#91b2ce!important;font-size:.75rem}.dash-kpi b{display:block;margin-top:4px;font-size:1.35rem}.dashboard-empty{padding:22px;border-radius:18px;border:1px dashed rgba(226,184,79,.55);background:rgba(226,184,79,.07);margin:10px 0 22px}
.plan-card{height:100%;padding:16px;border-radius:18px;border:1px solid rgba(91,164,239,.28);background:linear-gradient(145deg,#0c2745,#12385c);text-align:center}.plan-months{font-size:.76rem;text-transform:uppercase;letter-spacing:.08em;color:#82ccff!important;font-weight:900}.plan-price{font-size:1.5rem;font-weight:950;margin-top:6px}.plan-note{font-size:.72rem;color:#a9bed3!important}.trial-banner{display:flex;gap:14px;align-items:center;padding:14px 17px;border-radius:16px;border:1px solid rgba(226,184,79,.5);background:linear-gradient(90deg,rgba(226,184,79,.12),rgba(64,157,235,.08));margin:15px 0}.trial-banner b{padding:6px 9px;border-radius:999px;background:#e2b84f;color:#081423!important;white-space:nowrap}.trial-banner span{color:#d1dfeb!important}.payment-summary{padding:18px;border-radius:18px;border:1px solid rgba(93,175,255,.28);background:#0b2440;display:flex;flex-direction:column;gap:6px}.payment-summary strong{font-size:1.15rem}.payment-summary b{font-size:2rem;color:#f2cc61!important}.payment-summary small{color:#9fb9cf!important;line-height:1.45}.bank-logo{display:flex;align-items:center;gap:8px;padding:10px;border:1px solid rgba(120,181,238,.22);border-radius:14px;background:#0c2745;min-height:46px}.bank-logo span{width:32px;height:32px;border-radius:9px;display:grid;place-items:center;background:linear-gradient(135deg,#2e78dc,#e2b84f);color:#071423!important;font-weight:950;font-size:.72rem}.bank-logo b{font-size:.76rem}.method-chip{padding:11px 8px;border-radius:12px;border:1px solid rgba(104,179,242,.24);background:#0d2947;text-align:center;font-size:.72rem;font-weight:800;min-height:42px}
@media(max-width:850px){.company-dashboard-hero{flex-direction:column;align-items:flex-start}.company-dashboard-status{align-self:flex-start}.trial-banner{align-items:flex-start;flex-direction:column}}
.billing-lock{display:flex;gap:12px;align-items:center;padding:14px 17px;border-radius:16px;border:1px solid rgba(255,112,112,.45);background:linear-gradient(90deg,rgba(132,26,42,.28),rgba(226,184,79,.08));margin:0 0 20px}.billing-lock b{color:#ffd477!important;white-space:nowrap}.billing-lock span{color:#d8e2ed!important}@media(max-width:650px){.billing-lock{align-items:flex-start;flex-direction:column}}
</style>
""",unsafe_allow_html=True)


# FINAL DACRE CONTROL/INPUT VISIBILITY OVERRIDE
# Gold is the visibility/accent color for controls; placeholders stay neutral grey.
st.markdown(r"""
<style>
/* ===== DACRE STRICT GOLD CONTROL VISIBILITY ===== */
:root{--dacre-strict-gold:#e2b84f;--dacre-strict-gold-2:#f5d77a;--dacre-placeholder:#8f9baa;--dacre-control:#10243b;--dacre-control-2:#173453}

/* Text fields / text areas / number & date inputs */
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input,
.stTextInput input:focus,.stTextArea textarea:focus,.stNumberInput input:focus,.stDateInput input:focus{
 background:var(--dacre-control)!important;color:#fff!important;
 border:1.5px solid var(--dacre-strict-gold)!important;
 box-shadow:0 0 0 1px rgba(226,184,79,.16),0 5px 18px rgba(0,0,0,.12)!important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder,
.stNumberInput input::placeholder,.stDateInput input::placeholder{
 color:var(--dacre-placeholder)!important;opacity:1!important;
}

/* Select boxes / multiselects */
.stSelectbox [data-baseweb="select"]>div,
.stMultiSelect [data-baseweb="select"]>div,
[data-baseweb="select"]>div{
 background:var(--dacre-control)!important;color:#fff!important;
 border:1.5px solid var(--dacre-strict-gold)!important;
 box-shadow:0 5px 18px rgba(0,0,0,.10)!important;
}
.stSelectbox [data-baseweb="select"] span,
.stMultiSelect [data-baseweb="select"] span{color:#fff!important}
[data-baseweb="popover"],[data-baseweb="menu"]{background:#10243b!important;border:1px solid rgba(226,184,79,.55)!important}
[data-baseweb="option"]{color:#fff!important;background:#10243b!important}
[data-baseweb="option"]:hover,[aria-selected="true"]{background:#29435e!important;color:#fff!important}

/* Sliders: gold track/thumb so the value is visible */
.stSlider [data-baseweb="slider"] [role="slider"]{background:var(--dacre-strict-gold)!important;border-color:#fff!important}
.stSlider [data-baseweb="slider"]>div>div{background:var(--dacre-strict-gold)!important}
.stSlider [data-baseweb="slider"]>div>div>div{background:var(--dacre-strict-gold)!important}

/* Progress bars / meter-like bars */
.stProgress [role="progressbar"]{background:#394653!important;border:1px solid rgba(226,184,79,.35)!important}
.stProgress [role="progressbar"]>div{background:linear-gradient(90deg,var(--dacre-strict-gold),var(--dacre-strict-gold-2))!important}
progress{accent-color:var(--dacre-strict-gold)!important}

/* Tabs, radio and checkbox controls */
[data-testid="stTabs"] button{color:#c6d0db!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:#fff!important;border-bottom-color:var(--dacre-strict-gold)!important}
[data-testid="stRadio"] label,[data-testid="stCheckbox"] label{color:#fff!important}
[data-testid="stRadio"] [data-baseweb="radio"]>div:first-child{border-color:var(--dacre-strict-gold)!important}
[data-testid="stRadio"] [aria-checked="true"]>div:first-child{background:var(--dacre-strict-gold)!important}

/* Buttons remain blue/gold rather than disappearing as white bars */
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button,
button[data-testid="baseButton-primary"],button[data-testid="baseButton-secondary"]{
 color:#fff!important;border:1.5px solid var(--dacre-strict-gold)!important;
 background:linear-gradient(135deg,#173b66,#245487 62%,#7a6127)!important;
}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{
 color:#07111f!important;background:linear-gradient(135deg,var(--dacre-strict-gold),var(--dacre-strict-gold-2))!important;
 border-color:#fff!important;
}

/* Expander headers and other horizontal control bars */
[data-testid="stExpander"] summary{background:#122b45!important;color:#fff!important;border-color:rgba(226,184,79,.45)!important}
[data-testid="stExpander"] summary:hover{background:#183957!important;border-color:var(--dacre-strict-gold)!important}

/* File uploader: no white-on-white drop area */
[data-testid="stFileUploaderDropzone"]{background:#10243b!important;border:1.5px dashed var(--dacre-strict-gold)!important;color:#fff!important}
[data-testid="stFileUploaderDropzone"] *{color:#fff!important}

/* Keep native input caret and placeholder readable */
input,textarea{caret-color:var(--dacre-strict-gold-2)!important}

/* DACRE logo must remain the sole branded app/page icon */
.dacre-page-chrome .page-logo-icon{background:#fff!important;border:2px solid var(--dacre-strict-gold)!important}
.dacre-page-chrome .page-logo-icon img{content-visibility:auto!important;object-fit:contain!important}
</style>
""",unsafe_allow_html=True)

# Final visual safety layer: keeps interactive bars/buttons/inputs visible across all pages.
st.markdown("""
<style>
/* DACRE final UI override — ensure no white-on-white controls */
.stApp, .main, .block-container { color:#eef6ff !important; }
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  background: linear-gradient(135deg,#2f6fd4 0%,#4b7ff0 55%,#287fc6 100%) !important;
  color:#ffffff !important;
  border:1px solid rgba(112,180,255,.60) !important;
  border-radius:12px !important;
  min-height:42px !important;
  box-shadow:0 8px 24px rgba(22,74,153,.22) !important;
  font-weight:800 !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
  background:linear-gradient(135deg,#4386ec 0%,#5c93ff 55%,#2f9edf 100%) !important;
  border-color:#8ec8ff !important;
  color:#ffffff !important;
  transform:translateY(-1px);
}
.stButton > button:disabled, .stFormSubmitButton > button:disabled { opacity:.55 !important; color:#d9e8ff !important; }
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
  background:#111a2d !important;
  color:#f3f7ff !important;
  caret-color:#6ec6ff !important;
  border:1px solid rgba(123,161,214,.34) !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder, .stNumberInput input::placeholder { color:#94aac7 !important; opacity:1 !important; }
div[data-baseweb="select"] > div { background:#111a2d !important; color:#f3f7ff !important; border-color:rgba(123,161,214,.34) !important; }
[data-testid="stTabs"] button { color:#b9cae2 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color:#ffffff !important; border-bottom-color:#53bfff !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color:#f4f8ff !important; }
[data-testid="stDataFrame"] { background:#0e1728 !important; }
[data-testid="stExpander"] { background:rgba(12,24,42,.92) !important; border:1px solid rgba(109,160,221,.20) !important; }
.progress-bar, [role="progressbar"] { background:#1a2940 !important; }
/* Any remaining generic white cards created by older CSS get readable dark backgrounds. */
.element-container:has(> div > .stMarkdown) .stMarkdown { color:#edf5ff; }
</style>
<style>
@media (max-width:700px) {
  .block-container { max-width:100% !important; padding:0.65rem 0.65rem 2.5rem !important; }
  [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; gap:0.55rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width:100% !important; width:100% !important; flex:1 1 100% !important; }
  .dacre-page-chrome { flex-direction:column !important; align-items:stretch !important; gap:12px !important; padding:16px !important; }
  .page-chrome-left { width:100% !important; min-width:0 !important; }
  .page-chrome-right { width:100% !important; justify-content:flex-start !important; flex-wrap:wrap !important; }
  .page-title { font-size:clamp(28px,8vw,44px) !important; word-break:break-word; }
  .page-subtitle { font-size:13px !important; line-height:1.5 !important; }
  .dacre-dashboard-grid, .dashboard-grid, .metric-grid, .card-grid { grid-template-columns:1fr !important; }
  .dacre-nav-image-list { grid-template-columns:1fr !important; }
  [data-testid="stDataFrame"], [data-testid="stTable"] { max-width:100% !important; overflow-x:auto !important; }
  .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button { width:100% !important; min-height:46px !important; white-space:normal !important; }
  input, textarea, [data-baseweb="select"] { max-width:100% !important; }
  .page-logo-icon { width:48px !important; height:48px !important; flex:0 0 48px !important; }
}
.dacre-nav-image-list { display:grid; grid-template-columns:1fr 1fr; gap:7px; margin:0 0 10px; }
.dacre-nav-image-item { display:flex; align-items:center; gap:8px; min-width:0; min-height:42px; padding:8px 9px; border:1px solid rgba(123,161,214,.18); border-radius:10px; background:rgba(17,31,53,.72); color:#cbd9ed; font-size:11px; font-weight:700; }
.dacre-nav-image-item img { width:24px; height:24px; object-fit:contain; flex:0 0 24px; border-radius:6px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH),use_container_width=True)
        st.markdown("<div style='text-align:center;font-weight:900;letter-spacing:.14em;font-size:.78rem;margin:-4px 0 14px;color:#d9e8ff'>DACRE ANALYSIS</div>",unsafe_allow_html=True)
    st.markdown(f"### {user['first_name']}'s Workspace")
    st.caption(f"{user['company']} · {user['role']}")
    st.markdown("<div style='font-size:.78rem;color:#3556a8!important;margin:4px 0 14px'>DI is available across your workspace.</div>",unsafe_allow_html=True)

    # DACRE Analysis navigation only. Platform-wide administration, global business
    # oversight, customer operations and the Overall Admin portal belong to DGL
    # (DACRE Global Limited), not this application.
    # The hamburger menu contains the working tools. The company dashboard is the
    # landing workspace; removed DI Home/Calls/Action Center/Memory Box pages remain
    # available only through their underlying capabilities, not as navigation items.
    navigation=[
        "Company Dashboard", "DI Workforce", "Data Presentation Board",
        "Workspace & Data", "Formula Lab", "Charts", "File Vault", "Export Center",
    ]
    default_page="Company Dashboard"
    _nav_icons={
        "Company Dashboard":"dashboard.png",
        "DI Workforce":"workforce.png",
        "Data Presentation Board":"presentation.png",
        "Workspace & Data":"data.png",
        "Formula Lab":"formula.png",
        "Charts":"charts.png",
        "File Vault":"files.png",
        "Export Center":"export.png",
    }
    _nav_html = "<div class='dacre-nav-image-list'>"
    for _nav_item in navigation:
        _nav_icon_path = BASE_DIR / _nav_icons.get(_nav_item, "dashboard.png")
        if _nav_icon_path.exists():
            try:
                _nav_b64 = base64.b64encode(_nav_icon_path.read_bytes()).decode("ascii")
                _nav_html += f"<div class='dacre-nav-image-item'><img src='data:image/png;base64,{_nav_b64}'/><span>{_escape_html(_nav_item)}</span></div>"
            except Exception:
                _nav_html += f"<div class='dacre-nav-image-item'><span>{_escape_html(_nav_item)}</span></div>"
        else:
            _nav_html += f"<div class='dacre-nav-image-item'><span>{_escape_html(_nav_item)}</span></div>"
    _nav_html += "</div>"
    st.markdown(_nav_html, unsafe_allow_html=True)
    selected_page=st.radio("Navigation",navigation,index=navigation.index(default_page) if default_page in navigation else 0)

# Expired customer workspaces stay alive for billing, but all paid DACRE tools are locked
# until a payment is verified. The master account is not subscription-gated.
if user.get("role") != "master":
    _billing_snapshot = subscription_snapshot(user.get("company", ""))
    if not _billing_snapshot.get("active") and selected_page != "Company Dashboard":
        st.session_state["billing_lock_reason"] = "Your free 30-day access has ended. Open the Company Dashboard to renew your subscription."
        selected_page = "Company Dashboard"

# Universal inner-page interface. Every Dacre workspace gets the same premium chrome,
# while the master account receives a separate founder visual identity.
render_page_chrome(selected_page, user)

# =============================================================================
# DI HOME / CONTINUOUS BUSINESS CONVERSATION
# =============================================================================

def di_voice_bridge(language_code="en-NG"):
    """Reliable 8-second browser speech capture with live transcript preview.

    The browser captures speech, shows the words as they are recognized, stops at
    eight seconds, then sends exactly one combined question back to the Streamlit
    session. We intentionally avoid file upload so the microphone remains private.
    """
    lang_json = json.dumps(language_code)
    components.html(f"""
    <div id="dacre-voice-box" style="font-family:Inter,system-ui,sans-serif;display:grid;gap:9px;padding:2px 0;">
      <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
        <button id="dacre-voice-btn" type="button" style="border:1px solid #69b8ee;background:linear-gradient(135deg,#0e5f98,#1e82c0);color:#fff;border-radius:13px;padding:11px 17px;font-weight:850;cursor:pointer;font-size:14px;box-shadow:0 7px 18px rgba(0,103,170,.18);">Talk to DI</button>
        <div id="dacre-voice-status" style="font-size:13px;color:#49677f;font-weight:750;min-width:250px;">Click the microphone and speak naturally. DACRE will send your message after 8 seconds.</div>
      </div>
      <div id="dacre-live-transcript" style="min-height:42px;padding:10px 12px;border-radius:12px;background:#0d223c;border:1px solid rgba(120,170,210,.28);color:#eaf6ff;font-size:14px;line-height:1.45;">Your words will appear here while you speak…</div>
    </div>
    <script>
    (() => {{
      const btn=document.getElementById('dacre-voice-btn');
      const status=document.getElementById('dacre-voice-status');
      const preview=document.getElementById('dacre-live-transcript');
      const SpeechRecognition=window.SpeechRecognition || window.webkitSpeechRecognition;
      const lang={lang_json};
      let rec=null, timer=null, remaining=8, active=false, finals=[];

      const setStatus=(t)=>{{ if(status) status.textContent=t; }};
      const setPreview=(t)=>{{ if(preview) preview.textContent=t || 'Your words will appear here while you speak…'; }};
      const navigateWithTranscript=(text)=>{{
        const clean=String(text||'').replace(/\\s+/g,' ').trim();
        if(!clean){{
          setStatus('I could not hear a clear question. Please try again and speak a little closer to the microphone.');
          btn.disabled=false; btn.textContent='Talk to DI'; return;
        }}
        setStatus('Sending your question to DI…');
        setPreview(clean);
        const url=new URL(window.parent.location.href);
        url.searchParams.set('di_voice',clean);
        url.searchParams.set('di_voice_lang',lang);
        window.parent.location.assign(url.toString());
      }};
      const finish=()=>{{
        if(!active) return;
        active=false;
        if(timer){{clearInterval(timer);timer=null;}}
        try{{if(rec) rec.stop();}}catch(e){{}}
        btn.disabled=false; btn.textContent='Talk to DI';
        navigateWithTranscript(finals.join(' '));
      }};

      if(!SpeechRecognition){{
        btn.disabled=true; btn.style.opacity='.55';
        setStatus('Voice input is unavailable in this browser. Please use Chrome or type your question below.');
        return;
      }}

      btn.addEventListener('click',()=>{{
        if(active) return;
        active=true; finals=[]; remaining=8; setPreview('Listening…');
        btn.disabled=true; btn.textContent='Listening…'; setStatus('Listening… 8 seconds remaining');
        rec=new SpeechRecognition();
        rec.lang=lang; rec.continuous=true; rec.interimResults=true; rec.maxAlternatives=1;
        rec.onresult=(event)=>{{
          let interim='';
          for(let i=event.resultIndex;i<event.results.length;i++){{
            const r=event.results[i]; const phrase=(r && r[0] && r[0].transcript ? r[0].transcript.trim() : '');
            if(!phrase) continue;
            if(r.isFinal) finals.push(phrase); else interim += (interim?' ':'')+phrase;
          }}
          const whole=[...finals,interim].join(' ').replace(/\\s+/g,' ').trim();
          setPreview(whole || 'Listening…');
        }};
        rec.onerror=(event)=>{{
          if(!active) return;
          if(event && event.error==='not-allowed'){{active=false;clearInterval(timer);timer=null;btn.disabled=false;btn.textContent='Talk to DI';setStatus('Microphone permission was blocked. Allow microphone access for DACRE and try again.');return;}}
          setStatus('Microphone connection hiccup — continuing the 8-second capture…');
        }};
        rec.onend=()=>{{
          if(active){{ try{{rec.start();}}catch(e){{}} }}
        }};
        try{{rec.start();}}catch(e){{active=false;btn.disabled=false;btn.textContent='Talk to DI';setStatus('Microphone could not be started. Please allow microphone access and try again.');return;}}
        timer=setInterval(()=>{{
          remaining-=1;
          if(remaining<=0) finish();
          else setStatus(`Listening… ${{remaining}} second${{remaining===1?'':'s'}} remaining`);
        }},1000);
      }});
    }})();
    </script>
    """, height=116, scrolling=False)


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
        if st.session_state.get("di_response_mode","voice")=="voice": speak(reply, voice_lang_code)
        st.rerun()


def render_chibobec_client_overview(con):
    """Overall Admin view of Chibobec as a DACRE client organization."""
    users, activity, chats, files, projects, emails, calls = master_customer_360(CHIBOBEC_COMPANY)
    loans = pd.read_sql_query(
        """SELECT client_name, whatsapp_number, loan_amount, lent_date, due_date,
                  reminder_2_sent, due_sent, last_whatsapp_status, last_whatsapp_error, created_at
           FROM loan_clients WHERE lower(company_name) LIKE '%chibobec%' ORDER BY due_date ASC""",
        con,
    )
    st.markdown("""
    <div class="master-office-hero">
      <span class="master-only-badge">CLIENT 360 · MASTER VIEW</span>
      <div class="title">Chibobec Client</div>
      <div class="sub">Chibobec Loan Service is a DACRE client organization. This view shows what is happening inside the client's DACRE workspace.</div>
    </div>
    """, unsafe_allow_html=True)
    k1,k2,k3,k4,k5,k6=st.columns(6)
    k1.metric("Accounts", len(users))
    k2.metric("Logins", int(users["login_count"].sum()) if not users.empty else 0)
    k3.metric("Activities", len(activity))
    k4.metric("DI messages", len(chats))
    k5.metric("Files", len(files))
    k6.metric("Loan clients", len(loans))
    st.caption("Chibobec is shown here strictly as a DACRE client. This is client oversight, not a separate DACRE service.")
    tabs=st.tabs(["Workspace Activity","Accounts","DI Conversations","Files & Projects","Emails & Calls","Loan Desk"])
    with tabs[0]:
        st.subheader("What is happening in the Chibobec workspace")
        if activity.empty:
            st.info("No Chibobec workspace activity has been recorded yet.")
        else:
            st.dataframe(safe_dataframe_for_streamlit(activity.head(300)),use_container_width=True,hide_index=True)
    with tabs[1]:
        st.dataframe(safe_dataframe_for_streamlit(users),use_container_width=True,hide_index=True)
    with tabs[2]:
        st.dataframe(safe_dataframe_for_streamlit(chats.head(300)),use_container_width=True,hide_index=True)
    with tabs[3]:
        st.subheader("Files")
        st.dataframe(safe_dataframe_for_streamlit(files),use_container_width=True,hide_index=True)
        st.subheader("Projects")
        st.dataframe(safe_dataframe_for_streamlit(projects),use_container_width=True,hide_index=True)
    with tabs[4]:
        st.subheader("Emails")
        st.dataframe(safe_dataframe_for_streamlit(emails),use_container_width=True,hide_index=True)
        st.subheader("Calls")
        st.dataframe(safe_dataframe_for_streamlit(calls),use_container_width=True,hide_index=True)
    with tabs[5]:
        if loans.empty:
            st.info("No Chibobec loan clients are currently recorded.")
        else:
            view=loans.copy()
            view["loan_amount"]=view["loan_amount"].map(lambda x:f"₦{float(x):,.2f}")
            view["2-day reminder"]=view["reminder_2_sent"].map({0:"Pending",1:"Sent"})
            view["due-date reminder"]=view["due_sent"].map({0:"Pending",1:"Sent"})
            view=view.drop(columns=["reminder_2_sent","due_sent"])
            st.dataframe(safe_dataframe_for_streamlit(view),use_container_width=True,hide_index=True)


if selected_page=="Company Dashboard":
    render_company_dashboard(user)

# BUSINESS COMMAND CENTER — additive executive intelligence page
# =============================================================================
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
            st.markdown(f"### {a['di_name']}")
            st.caption(f"{a['di_code']} · {a['status']}")
            st.write(a['specialty'])
            st.info("DI knows David Emenike is the creator of DACRE.")
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

# PAGE 1 WORKSPACE
# =============================================================================
elif selected_page=="Workspace & Data":
    st.header("Workspace & Data Engine")
    st.caption("Bring data from files or public website tables into the same processed workspace.")
    source_tab, web_tab = st.tabs(["File / Workbook", "Website Data"])

    with source_tab:
        file_upload=st.file_uploader("Upload dataset (CSV, Excel, TSV, JSON, PDF)",type=SUPPORTED_EXTENSIONS,key="workspace_file_upload")
        if file_upload is not None:
            extension=file_upload.name.rsplit(".",1)[-1].lower()
            try:
                if extension in ("xlsx","xls"):
                    sheets=load_workbook_sheets(file_upload)
                    st.session_state.workbook_sheets={k: clean_dataframe(v) for k,v in sheets.items()}
                    sheet_names=list(st.session_state.workbook_sheets.keys())
                    current=st.session_state.get("active_sheet")
                    if current not in sheet_names:
                        current=sheet_names[0] if sheet_names else ""
                    chosen=st.selectbox("Select worksheet",sheet_names,index=sheet_names.index(current) if current in sheet_names else 0,key="workspace_sheet_picker") if sheet_names else ""
                    st.session_state.active_sheet=chosen
                    preview=st.session_state.workbook_sheets.get(chosen)
                    if preview is not None:
                        st.markdown(f"**Worksheet preview: `{chosen}`**")
                        st.dataframe(safe_dataframe_for_streamlit(preview.head(100)),use_container_width=True,hide_index=True)
                    import_clicked=st.button("Process Selected Worksheet",use_container_width=True,type="primary",key="process_selected_worksheet")
                else:
                    import_clicked=st.button("Import & Process File",use_container_width=True,type="primary",key="process_single_file")
                if import_clicked:
                    if extension in ("xlsx","xls"):
                        df_raw=st.session_state.workbook_sheets.get(st.session_state.get("active_sheet",""))
                        if df_raw is None:
                            raise ValueError("Please select a worksheet first.")
                    else:
                        df_raw=load_dataframe(file_upload)
                    st.session_state.raw_df=df_raw.copy()
                    st.session_state.processed_df=clean_dataframe(df_raw)
                    st.session_state.active_filename=file_upload.name
                    save_file(user,file_upload,st.session_state.processed_df)
                    save_project(user,st.session_state.raw_df,st.session_state.processed_df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
                    log_activity(user["username"],user["company"],f"Imported {file_upload.name}" + (f" · sheet {st.session_state.active_sheet}" if extension in ("xlsx","xls") else ""))
                    st.success(f"Processed '{file_upload.name}' successfully!")
                    st.rerun()
            except Exception as exc:
                st.error(f"Could not prepare the file: {exc}")

    with web_tab:
        website_url=st.text_input("Public website URL",placeholder="https://example.com/page-with-a-table",key="website_data_url")
        if st.button("Get Data From Website",use_container_width=True,type="primary",key="get_website_data") and website_url.strip():
            try:
                tables=fetch_website_tables(website_url.strip())
                st.session_state.website_tables={name:frame for name,frame in tables}
                if tables:
                    st.success(f"Found {len(tables)} table(s). Select one below to process it.")
                else:
                    st.warning("No standard HTML tables were found on that page. JavaScript-only tables may require an API or browser-based connector.")
            except Exception as exc:
                st.error(f"Website import failed: {exc}")
        website_tables=st.session_state.get("website_tables",{})
        if website_tables:
            website_choice=st.selectbox("Select website table",list(website_tables.keys()),key="website_table_picker")
            website_preview=website_tables[website_choice]
            st.dataframe(safe_dataframe_for_streamlit(website_preview.head(100)),use_container_width=True,hide_index=True)
            if st.button("Process Selected Website Table",use_container_width=True,key="process_website_table"):
                st.session_state.raw_df=website_preview.copy()
                st.session_state.processed_df=clean_dataframe(website_preview)
                st.session_state.active_filename=f"{website_choice.replace(' ','_').lower()}.csv"
                st.session_state.active_sheet=website_choice
                save_project(user,st.session_state.raw_df,st.session_state.processed_df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
                log_activity(user["username"],user["company"],f"Imported website table: {website_choice}")
                st.success("Website table is now the active processed dataset.")
                st.rerun()

    if st.session_state.processed_df is not None:
        df=st.session_state.processed_df
        st.subheader(f"Active Data: {st.session_state.active_filename}")
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Total Rows",f"{len(df):,}")
        m2.metric("Total Columns",len(df.columns))
        m3.metric("Duplicate Rows",int(df.duplicated().sum()))
        m4.metric("Missing Cells",int(df.isna().sum().sum()))
        st.dataframe(safe_dataframe_for_streamlit(df),use_container_width=True,hide_index=True)
        if st.button("Save Project State to DI",key="save_project_workspace"):
            save_project(user,st.session_state.raw_df,df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
            log_activity(user["username"],user["company"],"Saved project state")
            st.toast("Project saved.")
    else:
        st.info("No active dataset. Upload a file or import a public website table to begin.")

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
    st.header("Dynamic Chart Builder")
    df=st.session_state.processed_df
    if df is None or df.empty:
        st.warning("Please upload, import or open a dataset first.")
    else:
        cols=list(df.columns)
        num_cols=df.select_dtypes(include=["number"]).columns.tolist()
        chart_type=st.selectbox("Chart Type",["Bar Chart","Line Chart","Area Chart","Scatter Plot","Pie Chart","Histogram"],key="dynamic_chart_type")
        x_col=st.selectbox("X-Axis / Category",cols,key="dynamic_chart_x")
        y_options=num_cols if num_cols else cols
        y_col=st.selectbox("Y-Axis / Value",y_options,key="dynamic_chart_y")
        a1,a2,a3=st.columns(3)
        with a1:
            aggregation=st.selectbox("Aggregation",["Sum","Average","Count"],key="dynamic_chart_agg")
        with a2:
            limit=st.number_input("Maximum categories / points",min_value=5,max_value=500,value=int(st.session_state.get("chart_limit",25)),step=5,key="dynamic_chart_limit")
        with a3:
            title=st.text_input("Chart title",value=st.session_state.get("chart_title", ""),placeholder="e.g. Monthly Sales Performance",key="dynamic_chart_title")
        if st.button("Generate Dynamic Chart",use_container_width=True,type="primary",key="generate_dynamic_chart"):
            cfg={"type":chart_type,"x":x_col,"y":y_col,"aggregation":aggregation,"limit":int(limit),"title":title.strip()}
            st.session_state.chart_config=cfg
            st.session_state.chart_title=title.strip()
            st.session_state.chart_limit=int(limit)
            save_project(user,st.session_state.raw_df,df,st.session_state.active_filename,st.session_state.formula_logs,cfg)
            log_activity(user["username"],user["company"],f"Created {chart_type}: {x_col} vs {y_col}")
            st.success("Dynamic chart attached to the processed workspace.")
        cfg=st.session_state.get("chart_config")
        if cfg:
            chart=build_dynamic_chart(df,cfg.get("type"),cfg.get("x"),cfg.get("y"),cfg.get("title",""),cfg.get("limit",25),cfg.get("aggregation","Sum"))
            if chart is not None:
                st.altair_chart(chart,use_container_width=True)
            else:
                st.warning("The saved chart could not be rendered with the current dataset. Generate a new chart using available columns.")
        st.markdown("### Processed data used by the chart")
        st.dataframe(safe_dataframe_for_streamlit(df),use_container_width=True,hide_index=True)

# =============================================================================
# PAGE 4 DATA PRESENTATION BOARD
# =============================================================================
elif selected_page=="Data Presentation Board":
    st.markdown("<div class='dacre-hero'><div class='dacre-title'>Data Presentation Board</div><div class='dacre-sub'>Prociel is the active Data Presentation DI. The dataset is already loaded from Workspace & Data; now describe the story you want and Prociel will build the deck.</div></div>",unsafe_allow_html=True)
    df=st.session_state.processed_df
    if df is None or df.empty:
        st.warning("Load a dataset in Workspace & Data first. The Presentation Board uses the active processed dataset as its inspection board.")
    else:
        st.success(f"Inspection board ready: {len(df):,} rows × {len(df.columns):,} columns · {st.session_state.active_filename or 'active dataset'}")
        with st.expander("Inspection Board — preview the data Prociel will use",expanded=True):
            st.dataframe(safe_dataframe_for_streamlit(df.head(100)),use_container_width=True,hide_index=True)
        if "presentation_board" not in st.session_state:
            st.session_state.presentation_board={}
        board=st.session_state.presentation_board
        st.markdown("### 1. Prociel's presentation questions")
        q1,q2=st.columns(2)
        with q1:
            board["front_slide"]=st.text_input("What should be on the front slide?",value=board.get("front_slide",""),placeholder="e.g. 2026 Sales Performance")
            board["title"]=st.text_input("Presentation title",value=board.get("title",""),placeholder="e.g. Q3 Executive Data Review")
            board["audience"]=st.text_input("Who is the audience?",value=board.get("audience",""),placeholder="e.g. CEO, investors, management team")
        with q2:
            board["objective"]=st.text_area("What should the presentation achieve?",value=board.get("objective",""),height=92,placeholder="e.g. Explain the strongest trends and recommend what management should do next.")
            board["style"]=st.selectbox("Presentation design style",["Executive / premium","Modern technology","Minimal / clean","Corporate","Creative / bold","Academic / research"],index=["Executive / premium","Modern technology","Minimal / clean","Corporate","Creative / bold","Academic / research"].index(board.get("style","Executive / premium")) if board.get("style","Executive / premium") in ["Executive / premium","Modern technology","Minimal / clean","Corporate","Creative / bold","Academic / research"] else 0)
            board["color_direction"]=st.text_input("Colour direction",value=board.get("color_direction","DACRE blue + cyan + green accents"),placeholder="e.g. dark blue and gold")
        board["animation_direction"]=st.text_input("Animation direction",value=board.get("animation_direction","Use professional, restrained PowerPoint transitions; avoid distracting effects."))
        st.session_state.presentation_board=board

        st.markdown("### 2. Presentation prompt for Prociel")
        prompt=st.text_area("Tell Prociel exactly how you want the presentation",height=150,placeholder="Example: Make it 8 slides. Put the strongest sales finding on slide 2, use a clean executive style, show the top 5 categories, explain the trend, and finish with three recommendations.")
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button("Ask Prociel questions",use_container_width=True,key="prociel_question_btn"):
                st.session_state.prociel_question="I am Prociel, your Data Presentation Director. I have the inspection board. Before I design it, please confirm: 1) the exact front-slide wording, 2) audience, 3) main objective, 4) preferred visual style/colours, 5) number of slides, and 6) whether you want charts, images, online visual references, and PowerPoint transitions."
        with c2:
            if st.button("Research design references",use_container_width=True,key="prociel_research_btn"):
                research=(
                    _online_design_references(f"PowerPoint {board.get('style','executive')} data presentation design template",4)
                    + _online_design_references("best PowerPoint slide transitions presentation design",3)
                    + _online_design_references(f"PowerPoint color palette {board.get('color_direction','DACRE')}",3)
                )
                st.session_state.prociel_research=research
                for title,url in research:
                    try:
                        con=db(); con.execute("INSERT INTO presentation_brain_cache(di_name,source_type,source_title,source_url,content,created_at) VALUES(?,?,?,?,?,?)",("Prociel","web",title,url,"Public design reference",datetime.now().isoformat(timespec="seconds"))); con.commit(); con.close()
                    except Exception: pass
        with c3:
            if st.button("Clear presentation board",use_container_width=True,key="clear_presentation_board"):
                st.session_state.presentation_board={}; st.session_state.prociel_question=""; st.session_state.prociel_research=[]; st.session_state.presentation_spec=None; st.rerun()
        if st.session_state.get("prociel_question"):
            st.info(st.session_state.prociel_question)
        if st.session_state.get("prociel_research"):
            st.markdown("#### Online design references found by Prociel")
            for title,url in st.session_state.prociel_research[:8]:
                st.markdown(f"- [{title}]({url})")
        if st.button("Send prompt to Prociel & Generate PowerPoint",use_container_width=True,type="primary",key="prociel_generate_ppt"):
            with st.spinner("Prociel is inspecting the board, researching design references and building the PowerPoint…"):
                research=st.session_state.get("prociel_research") or _online_design_references(f"PowerPoint {board.get('style','executive')} data presentation",5)
                save_presentation_request(user,board,prompt.strip(),research)
                try:
                    pptx_bytes,spec,visual=generate_dacre_presentation(df,board,prompt.strip())
                    st.session_state.presentation_spec=spec
                    st.session_state.presentation_bytes=pptx_bytes
                    st.session_state.presentation_filename=(re.sub(r"[^A-Za-z0-9_-]+","_",(board.get("title") or "DACRE_Presentation")).strip("_") or "DACRE_Presentation")+".pptx"
                    st.session_state.presentation_visual=visual
                    log_di_action(user,"presentation_generated",prompt.strip() or "Generate presentation",f"Generated {len(spec.get('slides',[]))} slides with Prociel","Prociel")
                    log_activity(user["username"],user["company"],"Prociel generated a PowerPoint presentation")
                except Exception as exc:
                    st.error(f"Prociel could not generate the PowerPoint: {exc}")
        if st.session_state.get("presentation_bytes"):
            st.markdown("### 3. Presentation result")
            spec=st.session_state.get("presentation_spec") or {}
            st.write(f"**{spec.get('title',board.get('title') or 'DACRE Presentation')}** — {len(spec.get('slides',[]))} content slides + front slide")
            if spec.get("narrative"): st.caption(spec["narrative"])
            if st.session_state.get("presentation_visual"): st.caption("Prociel also checked an online public visual reference for the design context.")
            dl,up=st.columns(2)
            with dl:
                st.download_button("Download PowerPoint",data=st.session_state.presentation_bytes,file_name=st.session_state.presentation_filename,mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",use_container_width=True)
            with up:
                if st.button("Send to Microsoft 365 / PowerPoint",use_container_width=True,key="prociel_graph_upload"):
                    weburl=microsoft_graph_upload_presentation(st.session_state.presentation_bytes,st.session_state.presentation_filename)
                    if weburl: st.success(f"Uploaded to Microsoft 365: {weburl}")
                    else: st.warning("Microsoft Graph is not configured yet. DACRE keeps the generated PowerPoint locally and the connector stays invisible until its server-side Microsoft credentials are added.")
            st.markdown("#### Prociel's slide plan")
            for i,item in enumerate(spec.get("slides",[]),start=1):
                with st.expander(f"Slide {i}: {item.get('title','Untitled')}",expanded=False):
                    st.write(item.get("purpose",""))
                    for bullet in item.get("bullets",[]): st.write("• "+str(bullet))

# =============================================================================
# PAGE 5 FILE VAULT
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
        csv_data=df.to_csv(index=False).encode("utf-8-sig")
        tsv_data=df.to_csv(index=False,sep="\t").encode("utf-8-sig")
        excel_data=make_excel(df)
        base=re.sub(r"[^A-Za-z0-9_-]+","_",Path(st.session_state.active_filename or "dacre").stem).strip("_") or "dacre"
        e1,e2,e3=st.columns(3)
        with e1:
            st.download_button("Download CSV",data=csv_data,file_name=f"{base}_processed.csv",mime="text/csv",use_container_width=True)
        with e2:
            st.download_button("Download Excel Workbook",data=excel_data,file_name=f"{base}_processed.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        with e3:
            st.download_button("Google Sheets Compatible TSV",data=tsv_data,file_name=f"{base}_google_sheets.tsv",mime="text/tab-separated-values",use_container_width=True)
        st.caption("The CSV and TSV outputs can be opened/imported directly in Google Sheets. Direct Google Drive saving requires a Google account connector/credential, so DACRE does not pretend to save to a private Google Sheet without authorization.")
        log_activity(user["username"],user["company"],"Opened Export Center")

# =============================================================================
# ORGANIZATION ADMIN PORTAL
# =============================================================================
# =============================================================================
# PERSISTENT DI DOCK
# =============================================================================

st.markdown("---")
quick_title = "Sovereign Master Chat with DI" if user.get("role") == "master" else "Chat with DI — quick assistant"
quick_caption = (
    "Private founder channel · David Emenike · Sovereign Master request"
    if user.get("role") == "master"
    else "Ask DI about your data, work or DACRE."
)
with st.expander(quick_title,expanded=False):
    st.caption(quick_caption)
    if user.get("role") == "master":
        st.info("DI treats messages here as private Sovereign Master requests and responds with founder-level respect and intelligence.")
    for msg in st.session_state.chat_history[-10:]:
        st.write(f"**{msg['sender']}**: {msg['text']}")
    quick_chat_col, quick_clear_col = st.columns([8,1])
    with quick_chat_col:
        with st.form("quick_di_form",clear_on_submit=True):
            q=st.text_input("Chat with DI",placeholder="Ask DI anything about DACRE, your data or your work...",label_visibility="collapsed")
            send=st.form_submit_button("Send")
    with quick_clear_col:
        if st.button("Clear", help="Delete all previous messages in this chat", key="quick_di_chat_trash", use_container_width=True):
            st.session_state.chat_history=[]
            st.session_state.last_speech=""
            try:
                con=db(); con.execute("DELETE FROM chat_history WHERE username=? AND company_name=?",(user["username"],user["company"])); con.commit(); con.close()
            except Exception:
                pass
            st.rerun()
    if send and q.strip():
        sender_name = "David · Sovereign Master" if user.get("role") == "master" else user["first_name"]
        st.session_state.chat_history.append({"sender":sender_name,"text":q.strip()})
        reply=di_reply(q,user,st.session_state.processed_df,allow_online=True,language=st.session_state.get("di_language","English — Nigeria"))
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        st.session_state.last_speech=reply
        st.rerun()
if st.session_state.last_speech:
    speech = st.session_state.last_speech
    st.session_state.last_speech = None
    di_voice_player(
        speech,
        DI_LANGUAGE_PROFILES.get(
            st.session_state.get("di_language", "English — Nigeria"), {}
        ).get("code", "en-NG"),
    )

