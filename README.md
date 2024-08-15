## Fetch data from Google Analytics using Data API

### Initialize and activate virtualenv
```bash
python3 -m venv venv
source venv/bin/activate
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

### Setup env variables
Follow [Quickstart](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries#python_1)
- Get all required values and add it to .env file.

### Running script
```bash
python index.py
```