# Module 3: Databases & SQL — Starter Kit

## Quick Setup

### Option A: Clone with Git
```bash
git clone <repo-url>
cd module-03-databases-sql
```

### Option B: Download ZIP (no Git required)
1. Go to this repo on GitHub
2. Click the green **Code** button → **Download ZIP**
3. Unzip and open the folder

---

### Shared steps (both options)

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start working:** Open any exercise folder and edit `starter.py`.

---

## Exercises

| # | Exercise | Folder | Packages Used |
|---|----------|--------|---------------|
| 1 | Build Your Own Database | `exercises/music-db/` | sqlite3 (built-in) |
| 2 | The Constraint Tester | `exercises/constraint-tester/` | sqlite3 (built-in) |
| 3 | Student Roster CRUD | `exercises/student-roster-crud/` | sqlite3 (built-in) |
| 4 | The Interactive CRUD App | `exercises/interactive-crud/` | sqlite3 (built-in) |
| 5 | The Product Finder | `exercises/product-finder/` | sqlite3 (built-in) |
| 6 | Employee Directory Joins | `exercises/employee-joins/` | sqlite3 (built-in) |
| 7 | The Self-Join | `exercises/self-join/` | sqlite3 (built-in) |
| 8 | Library Analytics | `exercises/library-analytics/` | sqlite3 (built-in) |
| 9 | Product Catalog Models | `exercises/product-catalog-models/` | sqlalchemy |
| 10 | The Model Inspector | `exercises/model-inspector/` | sqlalchemy |
| 11 | Contact Manager | `exercises/contact-manager/` | sqlalchemy |
| 12 | School Enrollment System | `exercises/school-enrollment/` | sqlalchemy |
| 13 | Cascade Deletes | `exercises/cascade-deletes/` | sqlalchemy |
| 14 | The Translation Challenge | `exercises/translation-challenge/` | sqlite3 + pandas |

**Note:** Exercises 1–8 use Python's built-in `sqlite3` — no virtual environment needed for those. Exercises 9–13 require SQLAlchemy, and Exercise 14 requires pandas. Activate your virtual environment before running those.

## Module Project

The project starter is in `project/starter/`. See the course platform for full requirements.

## Solutions

Solutions are in `solutions/`. **Try each exercise yourself first!**

## Need Help?

- Re-read the lesson's Concept and Guided Example sections
- Check the course discussion board
- Ask during office hours
