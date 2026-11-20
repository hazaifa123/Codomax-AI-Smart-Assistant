# AI-Powered Expense & Budget Assistant

**Intern:** M. Hazaifa Tahir  
**Program:** Codomax AI & Python Internship (Module 05 — Final Capstone)  

## Overview
An upgraded AI-powered version of the CLI Expense Tracker built in Module 02. It integrates **Google Gemini (`google-genai`)** for automatic expense categorization and personalized financial insights, along with a built-in rule-based fallback so it works seamlessly both online and offline.

## Key Features
- **AI Auto-Categorization:** Automatically classifies expenses (e.g., Food, Education, Transport, Utilities) from natural descriptions.
- **AI Financial Advisor:** Analyzes spending history and generates actionable budgeting tips.
- **Offline Fallback Mode:** Built-in keyword classifier and statistical analyzer ensure full functionality even without an API key.
- **Persistent JSON Storage:** Automatically saves and loads records from `smart_expenses.json`.

## Setup & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
