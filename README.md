\# Realisieren Technologies - Web Scraping \& Data Consolidation



\## 1. Project Overview



This project implements a Python-based web scraping and data consolidation pipeline.



The project scrapes data from two practice websites:



\- Books to Scrape

\- Quotes to Scrape



The pipeline performs:



Extract → Clean → Validate → Deduplicate → Consolidate → Export



The final consolidated dataset is stored as a CSV file and execution metrics are stored as a JSON report.



\---



\## 2. Sources



\### Books to Scrape



URL:



https://books.toscrape.com/



The scraper collects:



\- Book title

\- Price

\- Rating

\- Book URL



\### Quotes to Scrape



URL:



https://quotes.toscrape.com/



The scraper collects:



\- Quote text

\- Author

\- Tags

\- Author URL



Both websites are practice websites intended for scraping exercises.



\---



\## 3. Technologies Used



\- Python 3.12

\- Requests

\- BeautifulSoup

\- lxml

\- CSV

\- JSON

\- Logging

\- Pytest



\---



\## 4. Project Structure



```text

scraping\_assignment/

│

├── scrapers/

│   ├── \_\_init\_\_.py

│   ├── base\_scraper.py

│   ├── books\_scraper.py

│   └── quotes\_scraper.py

│

├── processing/

│   ├── \_\_init\_\_.py

│   ├── cleaning.py

│   ├── validation.py

│   └── deduplication.py

│

├── tests/

│   ├── test\_cleaning.py

│   ├── test\_validation.py

│   └── test\_deduplication.py

│

├── output/

│   ├── final\_dataset.csv

│   └── summary\_report.json

│

├── logs/

│   └── scraper.log

│

├── main.py

├── requirements.txt

├── README.md

└── AI\_USAGE.md

