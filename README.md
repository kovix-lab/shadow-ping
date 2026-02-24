# Shadow-Ping

**Shadow-Ping** is a custom, privacy-focused desktop application built for native Linux environments. It acts as a secure network tracing tool, allowing users to safely investigate suspicious IP addresses and raw phishing URLs without executing malicious redirects in a standard browser.

### Features

- **URL Scrubbing:** Automatically strips complex URLs down to their core domain for safe querying.
- **Geolocation Tracking:** Bypasses routing to ping open-source databases for physical server locations.
- **Visual Mapping:** Automatically generates exact coordinate pins for instant visual verification.
- **Custom UI:** Built with PyQt6, featuring a custom dark-mode aesthetic.

### Installation

1. Clone the repository:
   `git clone https://github.com/kovix-lab/shadow-ping.git`
2. Move into the directory:
   `cd shadow-ping`
3. Create an isolated virtual environment:
   `python -m venv venv`
4. Activate the environment:
   `source venv/bin/activate`
5. Install the required dependencies:
   `pip install -r requirements.txt`

### Usage

Run the application via the terminal:
`python main.py`
