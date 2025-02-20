import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better visuals
sns.set_theme(style="darkgrid")

API_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&date=2000:2023"