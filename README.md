# DACRE Analysis — Complete Unified App

This package contains the complete DACRE Analysis application in one main
`app.py`, plus its dependency file and required static assets.

## Included
- Premium landing page
- DACRE logo as page/browser icon and PWA icon
- Get Started / Log In navigation
- Signup and persistent SQLite accounts
- Login and account-not-created handling
- Responsive dashboard
- Sidebar menu for all application areas
- Data Workspace
- Visualizations
- Dashboard Studio
- Reports
- SQL Code Space
- Power BI area
- Connections
- File Vault
- Organisation Admin
- Settings
- Internal DI routing/status
- XLSX generation
- Optional server-side Gemini integration
- PWA installation/download button

## Run
`pip install -r requirements.txt`
then
`python app.py`

Open `http://127.0.0.1:5000`.

## Server secrets
Set `DACRE_SECRET_KEY` to a strong random secret in production.
Optionally set `GOOGLE_API_KEY` for server-side Gemini generation.
Never put the Google key in frontend code.

## Phone
The landing page has a Download DACRE App button. On supported Android/Chrome
browsers it uses the PWA install prompt. On iPhone, Safari can use Add to Home
Screen. The hosted backend remains responsible for the persistent database.
