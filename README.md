# Doable — A Personal Task Manager Built on the Eisenhower Matrix
#### Video Demo: https://youtu.be/zrcIqScWVto
#### Description:

Doable is a personal, multi-user to-do list web application built with Flask, Flask-SQLAlchemy, and SQLite on the back end, and server-rendered Jinja templates styled with hand-written CSS (plus a light touch of Bootstrap for responsiveness) on the front end. Unlike a plain to-do list, every task a user creates must be filed under one of the four categories of the **Eisenhower Decision Matrix** — *Do*, *Schedule*, *Delegate*, or *Eliminate* — which forces the user to think about a task's real priority instead of just dumping it on an undifferentiated list. Each user has their own account, their own daily task board, a full searchable history of everything they have ever added, and a small progress bar that shows how much of today's work is already done.

## Features

- Account creation and login (hashed passwords, "remember me" sessions)
- Adding a new task with free-text content and an optional note
- Categorizing every task under one of the four Eisenhower actions
- Setting a deadline (time) for the task
- Marking a task as done/undone with a single click
- Editing an existing task (content, note, action, and deadline)
- Deleting a task (soft delete — it disappears from the daily board but stays in History)
- A progress bar showing how many of today's (non-deleted) tasks are completed
- A History page listing every task ever created, filterable by keyword and by date
- A responsive layout that adapts the sidebar navigation and the data tables to phone-sized screens

## Pages

- **sign_in** — registration form (full name, email, password, confirm password) with server-side validation (name length, email format via regex, password length, matching confirmation) and duplicate-email protection.
- **login** — authenticates an existing user against the hashed password stored in the database.
- **Home** — shows *today's* tasks only, ordered by status, action, deadline, and creation time, with inline check/edit/delete controls and the progress bar.
- **Editor** — a single form used both to create a brand-new task and to edit an existing one.
- **History** — every task the user has ever created (including deleted ones), with a search bar to filter by task content and/or creation date.

## Database Design

The app uses three tables:

- **users** — `id`, `full_name`, `email` (unique), `password` (hashed)
- **actions** — `id`, `name` — seeded once at startup with the four fixed Eisenhower categories: Do, Schedule, Delegate, Eliminate
- **tasks** — `id`, `user_id` (FK → users), `action_id` (FK → actions), `content`, `note`, `status` (boolean), `deadline` (time), `created_at` (datetime), `is_deleted` (boolean)

There is a one-to-many relationship between `users` and `tasks` (one user can have many tasks) and a one-to-many relationship between `actions` and `tasks` (one action category can be applied to many tasks). Deleting a task never removes its row from the database — it only flips `is_deleted` to `True` — which is what allows the History page to keep a permanent, honest record of everything the user has ever done, while the Home page stays focused on what's still relevant today.

## File-by-file Breakdown

- **app.py** — application entry point. Configures the secret key, the SQLite database URI, and the 7-day "remember me" cookie; creates the database tables; seeds the four actions; registers the `views` and `auth` blueprints; and wires up Flask-Login's `LoginManager` and `user_loader`.
- **models.py** — the three SQLAlchemy models described above (`User` also mixes in `UserMixin` so Flask-Login can manage its sessions).
- **seed.py** — a small helper, `fill_action()`, that inserts the four Eisenhower categories into the `actions` table the first time the app runs, and is a no-op on every run after that.
- **auth.py** — the `auth` blueprint: `/sign_in` (registration, with field-by-field validation and a hashed password via Werkzeug), `/login` (credential check), and `/logout`.
- **views.py** — the `views` blueprint, which holds all of the task-management logic: `/` (Home), `/add` and `/edit` (both rendered by the same `edit.html` template), `/check` (toggle done/undone), `/delete` (soft delete), `/history`, `/search`, and a small `/back` redirect used by the History page's close button.
- **templates/base.html** — the shared layout: loads Bootstrap, Google Fonts, Font Awesome, and the page's own CSS; renders the flashed-message banner; and switches between a horizontal top nav (for guests, on the login/sign-in pages) and a vertical sidebar nav (for logged-in users, on Home/Editor/History).
- **templates/login.html, sign_in.html, home.html, edit.html, history.html** — the five page templates described above.
- **static/css/styles.css** — global resets and the CSS custom properties (color palette, font sizes) shared by every page.
- **static/css/layout1.css / layout2.css** — the two navigation layouts (horizontal header vs. sidebar), each with a `@media` block that reflows the navigation on small screens.
- **static/css/auth.css, edit.css, home.css, history.css** — per-page styling, each with its own responsive `@media` rules — for example, the Home and History tables hide their least essential columns (note, created-at) and switch from a fixed to an automatic table layout on narrow screens so the task's name, status, and its edit/delete buttons stay visible together instead of requiring long horizontal scrolling.
- **static/js/script.js** — auto-hides the flashed-message banner five seconds after the page loads.

## Notable Design Decisions

- **Soft delete instead of a separate history table.** A deleted task only has its `is_deleted` flag flipped to `True`; it is never actually removed from the `tasks` table, and no second "history" table exists alongside it. Keeping one single source of truth avoids duplicating task data across two tables and the extra complexity (syncing, extra writes, extra joins) that a separate history table would have introduced — the Home page simply filters `is_deleted == False`, while the History page queries the same table without that filter.
- **One shared template, two routes, and two request cases inside the edit route.** `edit.html` is reused for both creating and editing a task instead of duplicating the form markup twice. The `/add` and `/edit` routes stay logically separate (`/add` only ever inserts a new task), but `/edit` itself has to distinguish between two different incoming POST requests: the first is the click that only carries a `task_id` and is used to fetch that task's existing data so the form can be pre-filled; the second is the actual form submission with the edited fields, which is what triggers the update in the database.
- **A lookup table for actions instead of a hardcoded list or enum.** Storing Do/Schedule/Delegate/Eliminate as rows in an `actions` table keeps the categorization data-driven.
- **Two blueprints, one responsibility each.** `auth` only knows about accounts and sessions; `views` only knows about tasks — keeping each file focused.

## Getting Started Locally

```
pip install flask flask_sqlalchemy flask_login
python app.py
```

The SQLite database (`app.db`) and the four seeded actions are created automatically on first run.

## AI Assistance

In keeping with CS50's Academic Honesty policy, AI tools were used as helpers, not as a substitute for the work: **Gemini** was used to get explanations of intermediate Flask concepts (blueprints, Flask-SQLAlchemy, Flask-Login authentication flows) and to help spot potential bugs while the core logic was being written. **Claude** was used after the application's logic and design were already finished, specifically to make the existing pages responsive on mobile screens — adding targeted CSS `@media` queries, a couple of Bootstrap utility wrappers (`table-responsive`), and small layout fixes — without altering the app's Python logic, HTML structure, or original visual design. Claude was also used to draft this README.
