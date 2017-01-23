# LDS Calendar Filler

Fill in calendar with appointments

## Setup

1. Clone repository
2. Generate virtualenvironment (Using python 3.5+)
3. Install requirements `pip install -r requirements.txt`
4. Generate `config.json` (see below)
5. Generate `client_secret.json` (see [Google Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python))
6. Run using `birthday_filler` with a numeric month as the default parameter


### config.json

The file should be formatted as follows:

```
{
  "google": {
    "calendar_id": "{google_calendar_id}"
  },
  "lds": {
    "username": "{lds account username}",
    "password": "{lds account password}"
  }
}
```