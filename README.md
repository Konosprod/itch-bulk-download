# itch-bulk-download

Download free games from itch.io

## Installation

- `pip install - requirements.txt`

## How to use

- Place your urls in a file called `links.txt`, one url per line
- Copy the `.env.example` file into a `.env` file
- Fill the variables.

`python src/main.py`

Enjoy !

## How to get the API_KEY

To get an API key, just go on your profile settings. You can get a key under the API Key tab.

## How to get CRSF_TOKEN

Juste check the cookies stored in your browser for itch.io. It should have a CSRF_TOKEN entry.

## TODO

- Maybe add a GUI or something
