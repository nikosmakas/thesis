# UniLabs

Μελέτη, σχεδίαση και υλοποίηση διαδικτυακής εφαρμογής για τη διαχείριση εργαστηρίων και εγγραφών φοιτητών.

## Δομή Project

```
unilabs/
│
├── app/
│   ├── app.py              # Κύριο Flask app (όλα τα routes εδώ)
│   ├── models.py            # Όλα τα SQLAlchemy models
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── templates/
│   │   ├── dashboard.html
│   │   └── login.html
│   └── data/
│       ├── data_labregister.sql
│       └── labregister.sqlite
│
├── requirements.txt
├── README.md
└── sqlite3.exe
```

## Οδηγίες Εκκίνησης

1. **Εγκατάσταση εξαρτήσεων**
   ```bash
   pip install -r requirements.txt
   ```
2. **Αρχικοποίηση βάσης (προαιρετικά)**
   - Τρέξε το Flask app και επισκέψου το `/init-db` για να δημιουργηθούν τα tables και να εισαχθούν τα δεδομένα.
3. **Εκκίνηση εφαρμογής**
   ```bash
   cd app
   python app.py
   ```
4. **Login**
   - Χρησιμοποίησε AM και password από τα demo δεδομένα (π.χ. 12345/12345).

## Περιγραφή
- Όλα τα routes βρίσκονται στο `app/app.py`.
- Όλα τα models στο `app/models.py`.
- Templates και static αρχεία στους αντίστοιχους φακέλους.
- Τα δεδομένα (SQL dump, SQLite db) στον φάκελο `app/data/`.

## GitHub Repository
[https://github.com/nikosmakas/thesis](https://github.com/nikosmakas/thesis)

---
Για ερωτήσεις ή βελτιώσεις, επικοινώνησε με τον δημιουργό του repository. 