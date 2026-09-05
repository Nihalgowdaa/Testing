import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def generate_transactions(user_details, filename, start_date, seed, num_transactions=100):
    generator = random.Random(seed)

    # Create transaction descriptions
    descriptions = [
        "ATM Withdrawal", "Salary", "Online Shopping", "Electricity Bill",
        "Grocery Store", "Restaurant", "Mobile Recharge", "Insurance Payment",
        "Refund", "Money Transfer", "Fuel", "Subscription"
    ]
    
    # Starting balance
    balance = generator.randint(5000, 20000)
    
    # Open CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write user details at the top
        for key, value in user_details.items():
            writer.writerow([f"{key}: {value}"])
        writer.writerow([])  # Empty line
        
        # Write transaction header
        writer.writerow(["Date", "Transaction ID", "Description", "Debit", "Credit", "Balance"])
        
        # Generate transactions
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        for i in range(num_transactions):
            txn_id = f"TXN{seed:02d}{i+1:03d}"
            desc = generator.choice(descriptions)
            
            # Randomly decide debit or credit
            if desc in ["Salary", "Refund"]:
                credit = round(generator.uniform(500, 5000), 2)
                debit = ""
                balance += credit
            else:
                debit = round(generator.uniform(50, 2000), 2)
                credit = ""
                balance -= debit
            
            # Write row
            writer.writerow([
                (current_date + timedelta(days=i % 28)).strftime("%Y-%m-%d"),
                txn_id,
                desc,
                debit,
                credit,
                round(balance, 2)
            ])

users = [
    ("Aarav Sharma", "111111001", "ABC Bank", "New York"),
    ("Ananya Iyer", "111111002", "XYZ Bank", "Los Angeles"),
    ("Vivaan Patel", "111111003", "Global Bank", "Chicago"),
    ("Diya Reddy", "111111004", "Metro Bank", "Houston"),
    ("Advik Singh", "111111005", "National Bank", "Phoenix"),
    ("Myra Nair", "111111006", "United Bank", "Seattle"),
    ("Arjun Mehta", "111111007", "Capital Bank", "Boston"),
    ("Sara Khan", "111111008", "Trust Bank", "Austin"),
    ("Kabir Das", "111111009", "City Bank", "Denver"),
    ("Ishita Rao", "111111010", "First Bank", "Miami"),
    ("Reyansh Joshi", "111111011", "Sunrise Bank", "Dallas"),
    ("Aadhya Menon", "111111012", "Horizon Bank", "Atlanta"),
    ("Vihaan Kapoor", "111111013", "Pioneer Bank", "Portland"),
    ("Meera Shah", "111111014", "Summit Bank", "San Diego"),
    ("Rudra Verma", "111111015", "Evergreen Bank", "Philadelphia"),
]

output_folder = Path(__file__).resolve().parent
for index, (name, account_number, bank, branch) in enumerate(users, start=1):
    user = {
        "User Name": name,
        "Account Number": account_number,
        "Bank": bank,
        "Branch": branch,
        "IFSC": f"BANK{index:07d}",
    }
    filename = output_folder / f"records__user{index:02d}_transactions.csv"
    start_date = f"2026-{((index - 1) % 12) + 1:02d}-01"
    generate_transactions(user, filename, start_date, seed=index)

print(f"{len(users)} unique CSV files generated in {output_folder}")
