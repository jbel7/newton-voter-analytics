# Newton Voter Analytics

A Django web app for exploring voter registration data for Newton, Massachusetts: 58,759 registered voters. Filter by party, birth year, voter score and which elections someone voted in, open any voter's details, or see the same slice of the electorate as interactive charts.

## How it's built

- Django with a single app, `voter_analytics`: a `Voter` model, a filterable paginated list view, a detail view and a graphs view.
- Charts are rendered server-side with Plotly and made interactive in the browser.
- SQLite database, loaded from the city's voter CSV with a management command.
- Plain HTML templates and CSS, with no front-end framework.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=true
python manage.py migrate
python manage.py load_voters path/to/newton_voters.csv
python manage.py runserver
```

Then open http://localhost:8000. The voter CSV isn't included in this repo. For anything other than local development, set the variables in `.env.example`.

## Author

Jed Belsany · [github.com/jbel7](https://github.com/jbel7)
