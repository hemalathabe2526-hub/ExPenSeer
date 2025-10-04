```# 💰 ExPenSeer — Predict. Protect. Pay.

> **Odoo Hackathon 2025 Project Submission**  
> Smart AI-powered Expense Management Suite built on Odoo 🚀

## 🧠 Problem Statement

Companies still rely on **manual expense reimbursement systems** — slow, error-prone, and lacking transparency.  
They struggle to:
- Define and automate **approval flows**  
- Manage **multi-level approvals**  
- Ensure **fraud-proof audit trails**
- Support **flexible, rule-based** approvals

## 💡 Our Solution — *ExPenSeer*

**ExPenSeer** is an intelligent, modular **Odoo-based expense management suite** that automates every step of expense handling — from OCR-based receipt scanning to blockchain-backed audit trails.

### 🔥 Key Highlights
| Category | Innovation |
|-----------|-------------|
| 🧩 **Adaptive Approval Engine (AAE)** | ML model suggests the best approval chain & confidence score |
| 📸 **AR + OCR Receipt Capture** | Auto-fills expenses by scanning receipts; detects merchant, date & items |
| 🔗 **Blockchain Audit Trail** | Tamper-proof approval record storage on a permissioned ledger |
| ⚙️ **Business-Policy DSL** | Write human-readable rules (e.g. IF amount > 2000 THEN require CFO) |
| 💳 **Auto Reconciliation** | Matches corporate card transactions with claims automatically |
| 🌿 **Sustainability & Forecasting** | Tracks carbon impact & predicts future departmental spend |
| 🧾 **Explainable Decisions** | Shows why a claim was approved/rejected (rule or ML reason) |

## 🏗️ Architecture Overview

Employee (Mobile / Web) 
         ↓  
(AR + OCR) Odoo Backend (Expense Core) 
         ↓ 
Adaptive Approval Engine (ML microservice) 
         ↓ 
Blockchain Ledger (Audit Hash) 
         ↓ 
Finance Dashboard + Analytics + Forecast

**Tech Stack:**
- 🐍 **Backend:** Odoo 16+, Python, PostgreSQL  
- ⚛️ **Frontend:** React (Web), React Native PWA (Mobile + AR)  
- 🤖 **AI/ML:** scikit-learn, Tesseract OCR / Textract API  
- 🔗 **Blockchain:** Hyperledger Fabric / Ganache (for PoC)  
- 🧰 **Infra:** Docker, Redis (Celery/RQ Workers)

## 🧩 Core Modules

| Module | Description |
|--------|--------------|
| expense_seer_core | Core models, roles, submission, approval workflows |
| expense_seer_aae | Adaptive Approval Engine (AI rules + ML model) |
| expense_seer_ocr | OCR + AR-based receipt parsing |
| expense_seer_policy | DSL compiler for approval rules |
| expense_seer_audit | Blockchain audit hashing |
| expense_seer_reconcile | Bank/card reconciliation engine |
| expense_seer_analytics | Budget forecast + sustainability insights |

## 🧭 Demo Flow (for judges)

1. 👤 Employee scans a receipt → OCR auto-fills claim  
2. 🤖 AAE suggests optimal approval chain (with confidence)  
3. ✅ Manager approves/rejects with comments & explainability  
4. 💳 Finance dashboard shows auto-matched card feed & green score  
5. 🔗 Audit tab shows immutable blockchain hash trail

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/hemalathabe2526hub/ExPenSeer.git
cd ExPenSeer

# Run using docker-compose (Odoo + PostgreSQL + Redis)
docker-compose up -d

# Install Odoo modules
odoo -i expense_seer_core,expense_seer_aae,expense_seer_ocr

## 📂 Repository Structure

ExPenSeer/
 ├── odoo_addons/
 │   ├── expense_seer_core/
 │   ├── expense_seer_aae/
 │   ├── expense_seer_ocr/
 │   ├── expense_seer_policy/
 │   ├── expense_seer_audit/
 │   ├── expense_seer_reconcile/
 │   └── expense_seer_analytics/
 ├── ml_services/
 │   ├── aae_service/
 │   └── ocr_service/
 ├── mobile_pwa/
 ├── infra/
 │   ├── docker-compose.yml
 │   └── README.md
 ├── docs/
 │   ├── architecture.png
 │   ├── demo_script.md
 │   ├── ppt_content.md
 │   └── sample_data/
 ├── README.md
 ├── DEMO.md
 └── LICENSE

## 🧪 Sample Business Policy DSL

IF category == 'Meal' AND amount > 2000 THEN require CFO
IF percent_approvers >= 60% OR specific_approver == 'CFO' THEN approve

## 📊 Success Metrics

✅ OCR auto-fill accuracy ≥ 85%

✅ Approval chain suggestion accuracy ≥ 70%

✅ Card reconciliation match rate ≥ 80%

✅ Blockchain audit record generated for every claim```
