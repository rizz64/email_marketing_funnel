# Email Marketing Automation Funnel

A complete, working Email Marketing Automation dashboard built with **Python (Flask)** + **SQLAlchemy** (SQLite by default, MySQL ready) that closely matches the provided UI screenshot.

## Features

- **Dashboard** with three main cards matching the design:
  1. **Email Campaign** – Special Offer preview + Shop Now CTA
  2. **Automation Workflow** – Templates → Wait decision → Send offer
  3. **Email Performance** – Open Rate gauge, Click/Unsubscribe rates, Subscriber growth chart
- Fully clickable UI – every button and link works
- Campaign creation, sending & tracking
- Email Templates (Welcome, Newsletter, Special Offer)
- Automation Workflows (toggle active/inactive)
- Subscriber management (add, list, unsubscribe)
- **Uncodemy course links** integrated as the Special Offer CTAs:
  - [Digital Marketing Course – Noida](https://uncodemy.com/course/digital-marketing-training-course-in-noida)
  - [Digital Marketing Course – Delhi](https://uncodemy.com/course/digital-marketing-training-course-in-delhi)

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3 + Flask                    |
| ORM / DB  | SQLAlchemy + SQLite (default)       |
| MySQL     | Supported via `DATABASE_URL` env    |
| Frontend  | HTML5 + CSS3 + Vanilla JS            |
| UI        | Custom responsive design matching the screenshot |

## Quick Start

```bash
# 1. Go into project folder
cd email_marketing_funnel

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app (auto-creates DB + seeds sample data)
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

### Using MySQL instead of SQLite

1. Create a MySQL database:
   ```sql
   CREATE DATABASE email_marketing CHARACTER SET utf8mb4;
   ```

2. Set environment variable (or create `.env`):
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/email_marketing
   ```

3. Run `python app.py` – tables will be created automatically.

## Project Structure

```
email_marketing_funnel/
├── app.py                 # Main Flask application + routes
├── config.py              # Configuration
├── models.py              # SQLAlchemy models
├── requirements.txt
├── README.md
├── static/
│   ├── css/style.css      # Full UI styles matching screenshot
│   └── js/app.js
└── templates/
    ├── base.html
    ├── dashboard.html     # Main 3-card UI
    ├── shop_now.html      # Offer landing with both Uncodemy links
    ├── campaign_detail.html
    ├── create_campaign.html
    ├── templates.html
    ├── template_detail.html
    ├── create_template.html
    ├── workflows.html
    ├── subscribers.html
    └── add_subscriber.html
```

## Sample Data

On first run the app seeds:
- 40+ sample subscribers
- 3 email templates (Welcome, Newsletter, Special Offer)
- 1 active Special Offer campaign
- 1 automation workflow (Welcome → Wait → Offer)
- 7 days of performance logs for the chart

## All Working Clicks

| Element                    | Action                                      |
|----------------------------|---------------------------------------------|
| Shop Now button            | Opens offer landing with both course links  |
| Send offer (workflow)      | Same offer landing                          |
| View Details               | Campaign performance & email preview        |
| Send Campaign              | Marks campaign sent & creates send records  |
| Template boxes             | Opens template detail                       |
| Manage Workflows           | List + toggle active/inactive               |
| + New Campaign             | Create form (with Uncodemy URLs pre-filled) |
| Templates / Workflows / Subscribers nav | Full CRUD-style pages              |
| Enroll Noida / Delhi       | External links to Uncodemy courses          |

Enjoy the project!
