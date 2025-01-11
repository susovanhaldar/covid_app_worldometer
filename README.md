## COVID-19 Data Extraction and Analysis
### Project Overview
This project crawls the [Worldometer website](https://www.worldometers.info/coronavirus/) to extract COVID-19 related data, including total cases, active cases, total deaths, total recovered, total tests, and more. The extracted data is then analyzed to provide insights into the pandemic's progression.

### Features
* Crawls Worldometer website to collect COVID-19 data for the world, continents, and countries
* Extracts key metrics, including:
    - Total cases, active cases, total deaths, total recovered, total tests
    - Death per million, test per million, new cases, new deaths, new recovered
* Calculates inferred metrics, including:
    - Change in active cases (%)
    - Change in daily deaths (%)
    - Change in new recovered (%)
    - Change in new cases (%)
* Provides a GUI-based program to present output to the user
* Allows users to query for a country closest to a given country based on percentage changes in the above metrics
### Technical Details
* Built using Python with the following libraries:
    - ply for building a context-free grammar to parse the website's HTML structure
    - tkinter for creating a GUI-based program
* Crawls the Worldometer website using a custom-built web crawler
### Getting Started
1. Clone the repository using `git clone`
2. Install the required libraries using `pip install -r requirements.txt`
3. Run the program using `python run.py`
### Example Use Cases
* Extract COVID-19 data for a specific country or continent
* Analyze the change in active cases or daily deaths over time
* Find the country closest to a given country based on percentage changes in COVID-19 metrics
### Disclaimer
> **Important Note:** Worldometer has stopped maintaining COVID-19 related data on their website. As a result, the data used in this project is outdated and may not reflect the current COVID-19 situation. This project is intended for educational and research purposes only, and should not be used for making decisions or taking actions related to COVID-19.
### Contributing
Contributions are welcome! If you'd like to report a bug or suggest a new feature, please open an issue on this repository.