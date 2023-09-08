# Azure Cost Reporting

A web app to help you monitor your Azure cost.

# Requirements

- Python 3.11

# Running locally

```sh
# Create your virtual environment
python -m venv .venv
source .venv/bin/activate # or venv\Scripts\Activate.ps1 for PowerShell/Windows
pip -r requirements.txt

# Generate architecture diagram
cd docs/
python architecture.py
```