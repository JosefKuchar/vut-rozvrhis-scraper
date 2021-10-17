# 📅 VUT Rozvrhy IS Scraper

Scraper for VUT Rozvrhy IS - https://minerva3.fit.vutbr.cz/rozvrhis/

Generates iCalendar file (Google calendar, macOS calendar, ...)

Pre-converted iCalendar files are in `dist` directory

## Instalation

`pip install -r requirements.txt`

## Usage

```
usage: scraper.py [-h] URL OUT_FILE

VUT Rozvrhy IS Scraper

positional arguments:
  URL         Url, e.g.: https://minerva3.fit.vutbr.cz/rozvrhis/ZS2021/zkousky/1BIT
  OUT_FILE    Output filename, e.g.: calendar.ics

optional arguments:
  -h, --help  show this help message and exit
```
