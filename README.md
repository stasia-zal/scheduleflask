
# UEK Schedule Exporter

A clean, web-based tool designed to fetch, parse, and export student class schedules and lecturer timetables from the Cracow University of Economics (UEK) system. Users can download their schedules directly as **iCalendar (.ics)** files for Google Calendar/Apple Calendar or **Excel (.csv)** files.

---

## 👤 Credits & Authorship

* **Core Application:** Developed entirely by **Anastasiia Zaluzhna** using a bit of AI assistance (including the generation of this documentation).
* **JavaScript Exception:** A tiny snippet of JavaScript on the frontend handles mapping full professor names to their respective backend database IDs without disrupting user input.
* **Core Scraper Module:** The `schedule_uek_web_excel` dependency folder was also created entirely by me, originally hosted/published from another repository on a separate GitHub account.

---

## ⚙️ How the Application Works

The system is split into three main parts: data scraping/preparation, the backend controller, and the user interface.

### 1. Data Preparation (`group_to_code.py`)

Before running the web app, `group_to_code.py` acts as a dedicated web scraper. It crawls the university's directories to extract lecturer names and matching internal schedule database IDs, compiling them into a structured, optimized local dictionary file (`dic.json`). It handles complex text formats, ensuring hidden `UTF-8 BOM` signatures are safely parsed.

### 2. The Backend Controller (Flask Web App)

The web server is built using **Flask**. Here is how the server handles requests:

* **The Home Page (`/`)**: When a user loads the page, Flask opens `dic.json` on the server using `utf-8-sig` encoding (to strip out hidden Windows BOM marks). It injects the entire dictionary array directly into the HTML template via Jinja2 before sending it to the client. This means **zero client-side API calls** are needed to populate the search bar.
* **The Exporter API (`/api/get-schedule`)**: When the download form is submitted, Flask captures the query type (student vs. lecturer) and format (`.ics` vs `.csv`). It hands the parsed ID over to the scraper module, processes the calendar streams dynamically using an in-memory `io.BytesIO` buffer, and serves the file directly to the user as a secure attachment without clogging up server disk space.

### 3. Intelligent Form Autocomplete

The input bar accepts multiple input types seamlessly:

* **Student Group Codes:** Users can type text strings like `KrAIs-1011`.
* **Lecturer Names:** Users can begin typing a name (e.g., `Abegglen Christian...`). The UI displays the full name elegantly, while a tiny script silently swaps the form payload behind the scenes to send the lecturer's matching numeric link ID (e.g., `49482`) to the backend.

---

## 🛠️ Project Structure

```text
├── app.py                         # Main Flask application and routing
├── group_to_code.py               # Web scraper that compiles dic.json
├── dic.json                       # The generated lecturer/ID dictionary index
├── templates/
│   └── index.html                 # Frontend user interface
└── schedule_uek_web_excel/        # Core business logic module (imported from my other repo)
    ├── tracker.py                 # Contains scrape_data, save_as_icalendar, save_as_csv
    └── ...                        

```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Make sure you have Python installed on your machine. Install the required dependencies (such as Flask and any libraries required by your scraping module, like `requests` or `beautifulsoup4`):

```bash
pip install flask requests beautifulsoup4

```

### 2. Generate the Dictionary Index

If you need to refresh or create the lecturer database, run the scraper script first:

```bash
python group_to_code.py

```

### 3. Launch the Web App

Run the Flask server locally:

```bash
python app.py

```

Open your web browser and navigate to `http://127.0.0.1:5000/`. Type a group code or professor's name, choose your format, and click download!
