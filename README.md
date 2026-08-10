# DACRE Analysis — Secure Upgraded Starter

DACRE Analysis is a Streamlit data workspace powered by DI — David's Intelligence.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Place `logo.png` beside `app.py` to enable the DACRE logo/favicon.

## Master security setup

The Master passkey is **not embedded as a fallback in source code**.
Set it before launching the app.

### Environment variable

Linux/macOS:

```bash
export DACRE_MASTER_PASSKEY='your-long-master-secret'
streamlit run app.py
```

Windows PowerShell:

```powershell
$env:DACRE_MASTER_PASSKEY='your-long-master-secret'
streamlit run app.py
```

### Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
DACRE_MASTER_PASSKEY = "your-long-master-secret"
```

Do **not** commit that file to GitHub.

## Important authentication change

Passwords and passkeys now use salted PBKDF2-HMAC-SHA256 rather than plain SHA-256.
Legacy SHA-256 records are accepted once and automatically upgraded after a successful login.

New account passwords must be at least 10 characters and contain:
- uppercase letter
- lowercase letter
- number

The Master portal does not expose plaintext passwords. It provides credential reset instead.

## Main modules

- Persistent SQLite authentication and company tenancy
- Company Admin user management
- File Vault with role-aware file visibility
- Automatic project restore
- Data cleaning and profiling
- Editable workflow grid
- Formula Lab
- Read-only SQL Lab
- ADD DYNAMICS charts
- Chart attachment configuration
- Excel export with embedded OpenPyXL chart
- Data health / missing-value insights
- Dynamic Presentation Engine
- DI command dock and browser voice synthesis
- Master DI audit portal and credential reset
- Failed-login temporary lockout
- Upload deduplication during Streamlit reruns

## Database

The SQLite database is created automatically as `dacre_platform.db`.
It is intentionally local to the deployment directory for this starter build.
For production deployment, use secure backups, encrypted storage, HTTPS, and a managed database when the platform grows.
