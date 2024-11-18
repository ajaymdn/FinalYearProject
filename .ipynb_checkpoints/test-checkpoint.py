# Import requests to retrive Web Urls example HTML. TXT 
import requests

# Import BeautifulSoup
from bs4 import BeautifulSoup

# import re module for REGEXes
import re

# import pandas
import pandas as pd


# Get the HTML data from the 2018 10-K from Apple
r = requests.get('https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145.txt')
raw_10k = r.text


print(raw_10k[0:1300])