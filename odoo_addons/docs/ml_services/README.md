Expense Seer - Adaptive Approval Engine (AAE)
============================================

This is a minimal FastAPI microservice that suggests an approval chain for an expense claim
and returns a confidence score. It's a toy implementation intended for local demos.

Files:
- main.py: FastAPI app exposing /suggest_chain
- model.py: wrapper to load/predict using a sklearn model
- train_model.py: script that trains a toy model and saves it to disk (model.joblib)
- call_approve.py: demo script showing how to call the Odoo approve endpoint when confidence > threshold
- requirements.txt: Python deps

How to run (Windows PowerShell):

1. Create a virtualenv and install deps:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Train the demo model:

```powershell
python train_model.py
```

3. Start the server:

```powershell
uvicorn main:app --reload --port 8001
```

4. Call the API (example using curl or the demo script):

```powershell
python call_approve.py
```
