"""Create an HTML spending report from transaction CSV files in this folder.

The report looks first for files named ``records__*.csv``.  If none are
present, it uses the existing ``records*.csv`` naming convention as a helpful
fallback (for example, recordsuser1_transactions.csv).
"""

from __future__ import annotations

import csv
import html
from collections import defaultdict
from datetime import datetime
from pathlib import Path


OUTPUT_FILE = "spending_report.html"


def money(value: str) -> float:
    """Convert a CSV currency value to a number; blanks become zero."""
    return float((value or "0").replace(",", "").replace("$", "").strip() or 0)


def report_files(folder: Path) -> list[Path]:
    files = sorted(folder.glob("records__*.csv"))
    return files or sorted(folder.glob("records*.csv"))


def read_account(csv_file: Path) -> tuple[dict[str, str], dict[str, float], float]:
    details: dict[str, str] = {}
    monthly_spending: dict[str, float] = defaultdict(float)
    available_balance = 0.0

    with csv_file.open(newline="", encoding="utf-8-sig") as file:
        rows = list(csv.reader(file))

    header_index = next(
        (i for i, row in enumerate(rows) if row and row[0].strip().lower() == "date"),
        None,
    )
    if header_index is None:
        raise ValueError("No transaction header beginning with 'Date' was found")

    for row in rows[:header_index]:
        if row and ":" in row[0]:
            key, value = row[0].split(":", 1)
            details[key.strip()] = value.strip()

    headers = [heading.strip() for heading in rows[header_index]]
    for values in rows[header_index + 1 :]:
        row = dict(zip(headers, values))
        try:
            date = datetime.strptime(row["Date"].strip(), "%Y-%m-%d")
        except (KeyError, ValueError, AttributeError):
            continue
        monthly_spending[date.strftime("%B %Y")] += money(row.get("Debit", ""))
        if row.get("Balance", "").strip():
            available_balance = money(row["Balance"])

    return details, monthly_spending, available_balance


def create_report(folder: Path) -> Path:
    accounts = []
    for csv_file in report_files(folder):
        try:
            accounts.append((csv_file.name, *read_account(csv_file)))
        except (OSError, ValueError, csv.Error) as error:
            print(f"Skipping {csv_file.name}: {error}")

    cards = []
    for filename, details, spending, balance in accounts:
        person = html.escape(details.get("User Name", filename))
        detail_rows = "".join(
            f"<tr><th>{html.escape(key)}</th><td>{html.escape(value)}</td></tr>"
            for key, value in details.items()
        )
        month_rows = "".join(
            f"<tr><td>{html.escape(month)}</td><td>₹{amount:,.2f}</td></tr>"
            for month, amount in spending.items()
        ) or "<tr><td colspan='2'>No debit transactions</td></tr>"
        cards.append(f"""
        <section class='card'>
          <h2>{person}</h2><p class='file'>{html.escape(filename)}</p>
          <p class='balance'>Available balance: ₹{balance:,.2f}</p>
          <h3>Person details</h3><table>{detail_rows}</table>
          <h3>Monthly spending</h3><table><tr><th>Month</th><th>Spent</th></tr>{month_rows}</table>
        </section>""")

    body = "\n".join(cards) or "<p>No matching transaction CSV files were found.</p>"
    page = f"""<!doctype html><html><head><meta charset='utf-8'>
    <title>Spending report</title><style>
    body{{font:16px Arial,sans-serif;background:#f5f7fb;margin:2rem;color:#172033}}
    .card{{background:white;border-radius:10px;padding:1.5rem;margin:1rem 0;max-width:760px;box-shadow:0 2px 8px #dbe1ee}}
    h1,h2,h3{{margin-bottom:.4rem}} .file{{color:#667085}} .balance{{font-size:1.2rem;font-weight:bold;color:#087443}}
    table{{border-collapse:collapse;width:100%;margin-bottom:1.25rem}} th,td{{padding:.55rem;border-bottom:1px solid #e5e7eb;text-align:left}}
    </style></head><body><h1>Monthly Spending Report</h1>{body}</body></html>"""
    output = folder / OUTPUT_FILE
    output.write_text(page, encoding="utf-8")
    return output


if __name__ == "__main__":
    output = create_report(Path.cwd())
    print(f"Report created: {output}")
