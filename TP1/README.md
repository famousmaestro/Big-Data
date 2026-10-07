Author : Abderrazzak Karoui
Colab link :https://colab.research.google.com/drive/1j7O1ANhuDM6tTnLHjJBYx67VuZwA-3KM?usp=sharing
# Books to Scrape - Web Scraper

This repository contains a Python-based web scraper that extracts book details from the [Books to Scrape](https://books.toscrape.com/) sandbox website. It gathers information from all 50 pages of the website and saves the consolidated data into a structured CSV file.

## 🚀 Features
- **Multi-page Scraping**: Iterates through all 50 pages of the website.
- **Data Extraction**: Extracts essential book details:
  - Book Title
  - Price
  - Availability (Stock Status)
  - Star Rating
  - Direct Product Link
- **Data Processing**: Compiles the scraped data into a Pandas DataFrame for data profiling (checking for nulls and duplicate rows).
- **Export**: Generates and downloads a clean `books.csv` file.

## 🛠️ Tech Stack & Libraries
- **Python 3**
- **Requests**: For sending HTTP requests to the target website.
- **BeautifulSoup4**: For parsing and navigating HTML documents.
- **Pandas**: For structured data handling, cleaning, and exporting to CSV.
- **Urllib**: For resolving relative product URLs.

## 📋 Project Structure
1. **Libraries Import**: Setting up the runtime environment.
2. **Connection Check**: Verifying that the target website is accessible.
3. **Prototyping**: Parsing the first book to map out HTML elements.
4. **Data Harvesting**: Performing the complete loop across 50 pages (1000 books in total).
5. **Data Analysis**: Loading the collected dataset into Pandas to inspect overall quality.
6. **Export**: Saving and downloading `books.csv`.

## ⚙️ How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/books-to-scrape-scraper.git
   cd books-to-scrape-scraper
   ```
2. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```
3. Run the notebook or script to collect your dataset.
