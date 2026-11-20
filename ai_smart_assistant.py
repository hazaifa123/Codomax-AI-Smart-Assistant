import os
import json
from datetime import datetime

# Optional: Uses Google Gemini API if GEMINI_API_KEY is set, otherwise runs built-in smart heuristic mode
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

DATA_FILE = "smart_expenses.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(records):
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=4)


def auto_categorize(title):
    """Smart keyword-based fallback classifier when offline."""
    t = title.lower()
    if any(w in t for w in ["lunch", "dinner", "tea", "coffee", "food", "burger", "biryani"]):
        return "Food"
    if any(w in t for w in ["book", "course", "pen", "print", "tuition", "university", "lab"]):
        return "Education"
    if any(w in t for w in ["uber", "indrive", "bus", "fuel", "petrol", "ticket", "ride"]):
        return "Transport"
    if any(w in t for w in ["internet", "wifi", "mobile", "bill", "electricity", "recharge"]):
        return "Utilities"
    return "General"


def add_smart_expense(records):
    print("\n--- Add Expense (AI Auto-Categorization) ---")
    title = input("Enter expense description: ").strip()
    try:
        amount = float(input("Enter amount (PKR): "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    category = auto_categorize(title)
    api_key = os.getenv("GEMINI_API_KEY")

    if GEMINI_AVAILABLE and api_key:
        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"Classify this expense into a single one-word category "
                f"(Food, Education, Transport, Utilities, Entertainment, or General): '{title}'"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            ai_cat = response.text.strip().split()[0].strip(".,")
            if ai_cat:
                category = ai_cat.capitalize()
        except Exception:
            pass  # Fallback to local smart classifier

    record = {
        "id": len(records) + 1,
        "title": title,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    records.append(record)
    save_data(records)
    print(f"Added: '{title}' | Category: [{category}] | Amount: PKR {amount:.2f}")


def get_ai_financial_advice(records):
    print("\n--- AI Spending Insights & Advice ---")
    if not records:
        print("No expenses recorded yet. Add some expenses first!")
        return

    total = sum(r["amount"] for r in records)
    summary_lines = [f"- {r['title']} ({r['category']}): PKR {r['amount']}" for r in records]
    summary_text = "\n".join(summary_lines)

    api_key = os.getenv("GEMINI_API_KEY")
    if GEMINI_AVAILABLE and api_key:
        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"Analyze these student expenses (Total: PKR {total:.2f}) and give 3 short, "
                f"practical money-saving tips:\n{summary_text}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            print(response.text)
            return
        except Exception as e:
            print(f"[AI API unavailable, switching to local analyzer: {e}]\n")

    # Local Smart Analysis Fallback
    cat_totals = {}
    for r in records:
        cat_totals[r["category"]] = cat_totals.get(r["category"], 0) + r["amount"]

    top_cat = max(cat_totals, key=cat_totals.get)
    top_pct = (cat_totals[top_cat] / total) * 100

    print(f"Total Spending: PKR {total:.2f}")
    print(f"Highest Spending Category: {top_cat} (PKR {cat_totals[top_cat]:.2f} / {top_pct:.1f}%)")
    print("\nSmart Recommendations:")
    print(f"1. Your top expense area is '{top_cat}'. Setting a weekly cap here can save 15-20%.")
    print("2. Track small daily purchases—they often add up to over 30% of monthly budgets.")
    print("3. Follow the 50/30/20 rule: 50% needs, 30% wants, and 20% savings.")


def view_all(records):
    print("\n--- Recorded Expenses ---")
    if not records:
        print("No records found.")
        return
    for r in records:
        print(f"[{r['id']}] {r['date']} | {r['category']:<12} | {r['title']:<20} | PKR {r['amount']:.2f}")


def main():
    records = load_data()
    while True:
        print("\n==========================================")
        print("   AI-POWERED EXPENSE & BUDGET ASSISTANT  ")
        print("==========================================")
        print("1. Add Expense (AI Auto-Categorize)")
        print("2. View All Expenses")
        print("3. Get AI Spending Insights & Advice")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()
        if choice == "1":
            add_smart_expense(records)
        elif choice == "2":
            view_all(records)
        elif choice == "3":
            get_ai_financial_advice(records)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
