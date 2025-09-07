

**What it has**
- Register / Login (SQLite)
- Start a mock interview (5 preset questions)
- Type your answers (no speech)
- Static, rule-based feedback (keyword match + tips)
- Result page + score
 

**What it does *not* have**
- Real AI models, voice, or external APIs
- Advanced analytics

## Quickstart  process

```bash
# 1) Create venv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Initialise the database
python init_db.py

# 4) Run the app
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project structure
```
com668_option_b/
├─ app.py
├─ init_db.py
├─ requirements.txt
├─ questions.json
├─ README.md
├─ report_template.txt
├─ static/
│  └─ style.css
└─ templates/
   ├─ layout.html
   ├─ login.html
   ├─ register.html
   ├─ dashboard.html
   ├─ interview.html
   └─ result.html
```

![alt text ](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
