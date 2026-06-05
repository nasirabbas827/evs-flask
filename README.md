# evs_flask_final  
**Electronic Voting System (EVS) built with Flask and a simple blockchain implementation**

---

## Overview
`evs_flask_final` is a prototype electronic voting platform that demonstrates how blockchain concepts can be applied to secure voting processes. The application provides separate interfaces for administrators and voters, allowing:

* Management of candidates, elections, and voters  
* Secure vote casting that is recorded on a lightweight blockchain  
* Real‑time result viewing for administrators  

The project is intended for educational purposes and as a starting point for more robust, production‑ready voting solutions.

---

## Features
| ✅ | Feature |
|---|---------|
| ✔️ | **Admin panel** – login, dashboard, CRUD for candidates, elections, and voters |
| ✔️ | **Voter portal** – registration, login, profile, view candidates, cast vote |
| ✔️ | **Blockchain‑backed voting** – each vote is stored as a block with hash chaining |
| ✔️ | **Result aggregation** – admin can view live vote counts per candidate |
| ✔️ | **SQLite database** – schema defined in `Database/evs_db.sql` |
| ✔️ | **Responsive UI** – HTML templates with Bootstrap (no external assets required) |
| ✔️ | **Static assets** – candidate pictures stored under `static/candidate_pictures/` |

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | Python 3.9+, Flask |
| Data persistence | SQLite (SQL script in `Database/evs_db.sql`) |
| Blockchain logic | Custom implementation in `blockchain.py` |
| Front‑end | HTML5, CSS3 (Bootstrap), Jinja2 templating |
| Development tools | `venv`/`virtualenv`, `pip` |

---

## Installation
> **Prerequisites** – Python 3.9+ and Git installed on your machine.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/evs_flask_final.git
cd evs_flask_final

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt   # (create this file if missing, e.g. Flask)

# 4. Initialise the SQLite database
sqlite3 evs.db < Database/evs_db.sql

# 5. (Optional) Populate with sample data
#    You can run the provided `app.py` and use the admin UI to add candidates/elections.
```

> **Note:** If `requirements.txt` does not exist, install Flask directly:

```bash
pip install Flask
```

---

## Usage
### Running the application
```bash
export FLASK_APP=app.py
export FLASK_ENV=development   # optional, enables debug mode
flask run
```
The server will start at `http://127.0.0.1:5000/`.

### Access points
| URL | Description |
|-----|-------------|
| `/admin/login` | Admin authentication |
| `/admin/dashboard` | Admin dashboard – manage candidates, elections, voters, view results |
| `/register` | Voter registration |
| `/voter/login` | Voter authentication |
| `/voter/dashboard` | Voter dashboard – view candidates and cast vote |

### Basic workflow
1. **Admin** logs in → creates an election → adds candidates (upload pictures via the UI).  
2. **Voter** registers → logs in → selects the active election → casts a vote.  
3. Each vote triggers `blockchain.add_block()` in `blockchain.py`, creating an immutable record.  
4. **Admin** can view live results on the *Admin View Results* page.

### Configuration
If you need