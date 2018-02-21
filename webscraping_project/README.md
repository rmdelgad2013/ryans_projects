# Web Scraping project

I made this Jupyter Notebook before I interviewed with Citadel to prove that I knew how to web scrape. That was about 1.5 years ago (as of this commit), and I'd do things quite differently now:
* I'd use lxml instead of beautifulsoup4. bs4 is slow, hard to read, and uses lxml under the hood anyway. Using lxml/xpath to extract data from the web is much more expressive than traversing HTML elements with nested for loops.
* I'd store the in a local Postgres or good ol' CSV files. This data is teeny tiny, so we're actually _losing_ interpretability by dimensionalizing it. Plus, SQLite isn't scalable
* I'd parallelize the scrape with either Scrapy or multithreading it w/ the concurrent library.

I'm leaving this as is, though. :)
