# Group Expense Splitter API - Chirag Sreedhara

A backend API for managing shared expenses between users. Built with FastAPI, MySQL, AWS RDS, Python, and SQL, it supports group expenses, individual paybacks, and tracks optimized balances so users always know who owes what.


## API endpoints:

### Users
- `POST /users`: Create a user

### Groups
- `POST /groups`: Create a group
- `POST /groups/{group_id}/add-member`: Add a user to a group

### Expenses
- `POST /expenses`: Create a new expense (group or 1:1)
- `GET /expenses`: View all expenses

### Balances
- `GET /groups/{group_id}/balances`: Get optimized(net) balances in a group

---

## Ex. Expense 

```json
{
  "group_id": 2,
  "payer_id": 1,
  "amount": 60.0,
  "description": "Trip to ATL Zoo",
  "recipient_ids": [2, 3]
}
```

---

## To run:

1. Fill in `.env` with DB credentials
2. Run `python init_db.py`
3. Start server with `uvicorn main:app --reload`

---
