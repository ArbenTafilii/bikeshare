# Bikeshare Data Analysis

## Overview
This project explores US bike share data from three cities — **Chicago**, **New York City**, and **Washington** — using Python and pandas. The script runs interactively in the terminal, allowing the user to filter data by city, month, and day, and then displays descriptive statistics.

## Files
- `bikeshare.py` — main Python script
- `README.md` — this file
- `.gitignore` — excludes data files from the repository

> Note: The CSV data files (`chicago.csv`, `new_york_city.csv`, `washington.csv`) are not included in this repository. They can be downloaded from Udacity's course resources.

## How to Run

1. Make sure Python 3 and pandas are installed.
2. Place the three CSV data files in the same folder as `bikeshare.py`.
3. Run the script from the terminal:

```
python bikeshare.py
```

4. Follow the prompts to choose a city, month, and day filter.

## Features
- Filter data by city, month, and day of the week
- Displays the most frequent times of travel
- Shows the most popular stations and trips
- Calculates total and average trip duration
- Shows user statistics (type, gender, birth year where available)
- Option to view raw data 5 rows at a time

## Dataset
The data covers the first six months of 2017 for three cities:

| City | Gender Data | Birth Year Data |
|------|-------------|-----------------|
| Chicago | Yes | Yes |
| New York City | Yes | Yes |
| Washington | No | No |

## Software Requirements
- Python 3
- pandas
- numpy
