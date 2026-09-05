# Testing

## Spending report

This project generates an HTML monthly spending report from transaction CSV
files. It discovers files named `records__*.csv` first and falls back to the
older `records*.csv` naming convention when needed.

For each account, `spending_report.py`:

- Reads account details and transaction data from CSV files.
- Calculates spending totals grouped by month from debit transactions.
- Displays the latest available balance.
- Escapes imported values before inserting them into the generated HTML.
- Skips invalid CSV files with a clear error message instead of stopping the
  entire report.

Run it with:

```powershell
python spending_report.py
```

The generated report is saved as `spending_report.html`. Transaction CSV files
are intentionally ignored by Git because they contain generated account data.
