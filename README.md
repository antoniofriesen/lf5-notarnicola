# lf5-notarnicola

A database management system for **Gemüse und Früchte Notarnicola**, developed as part of Lernfeld 05 at ITECH school. The system digitalizes customer and order management and includes GDPR-compliant data handling.

---

## 👥 Team

- Antonio Friesen
- Julian Brandtstaedter
- Thore Heuer

---

## 🗂️ Project Structure

```
lf5-notarnicola/
├── backend/
│   ├── cli/
│   │   ├── helpers.py        # Menu and input validation
│   │   └── main.py           # Central CLI entry point
│   ├── db/
│   │   └── db_utils.py       # Database connection utilities
│   └── models/
│       ├── customers.py      # CRUD + GDPR anonymization for customers
│       ├── orders.py         # CRUD + cancellation for orders
│       └── products.py       # CRUD + deactivation for products
├── db/
│   └── lf5.sql               # Database dump (latest)
├── frontend/                 # GUI (in development)
├── .env                      # Local environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

- Python 3.11+
- MySQL 8.0 (via Docker, XAMPP, or any local MySQL installation)

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/antoniofriesen/lf5-notarnicola.git
cd lf5-notarnicola
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the project root with your database credentials:

```
DB_HOST=<host>
DB_PORT=<port>
DB_USER=<username>
DB_PASSWORD=<password>
DB_NAME=<database_name>
```

> ⚠️ Never commit the `.env` file — it contains sensitive credentials.

### 5. Create the `.gitignore` file

Make sure your `.gitignore` includes at least:

```
.env
.venv/
__pycache__/
*.pyc
.DS_Store
.idea/
```

### 6. Start the database

Start your MySQL database using your local environment (Docker, XAMPP, or any other MySQL setup). Make sure the database is running and accessible with the credentials defined in your `.env` file.

### 7. Import the database

```bash
docker compose exec -i mysql mysql -u root -proot lf5 < db/lf5.sql
```

### 8. Run the application

```bash
python3 backend/cli/main.py
```

---

## 🗃️ Database

The database is named `lf5` and runs on port `3307` (Docker). The schema includes the following tables:

| Table | Description |
|---|---|
| `kunden` | Customer master data |
| `orte` | Postal codes and cities |
| `bestellungen` | Orders |
| `bestellpositionen` | Order positions (line items) |
| `produkte` | Products |
| `allergene` | Allergens |
| `produkt_allergene` | Product-allergen mapping |

---

## 🔒 GDPR Compliance

This system implements two GDPR requirements:

- **Art. 15 — Right of Access**: retrieve all stored data for a customer
- **Art. 17 — Right to Erasure**: anonymize customer personal data by replacing name with `N/A`

> Full deletion is not performed due to the 10-year retention obligation under §147 AO (German Tax Code).

---