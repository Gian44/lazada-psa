# Lazada PSA

**Lazada PSA** is a Python-based application designed to scrape product prices from Lazada, providing users with up-to-date pricing information for various products.

---

## Features

* **Price Scraping**: Automatically fetches product prices from Lazada.
* **Database Storage**: Stores scraped data in a local SQLite database (`lazada_products.db`) for easy access and analysis.
* **Configurable Settings**: Customize scraping parameters through the `config.py` file.
* **Modular Design**: Organized codebase with separate modules for scraping logic, database interactions, and Lazada-specific functions.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Gian44/lazada-psa.git
   cd lazada-psa
   ```



2. **Install Dependencies**:

   Ensure you have Python 3 installed. Then, install required packages:

   ```bash
   pip install -r requirements.txt
   ```

   After installing the requirements, run

    ```bash
   playwright install
   ```


---

## Usage

1. **Configure Settings**:

   Edit the `config.py` file to set your desired parameters, such as cookie file and db name.

2. **Run the Scraper**:

   Execute the scraper script:

   ```bash
   python lazada.py
   ```



The script will fetch product data from Lazada and store it in your `.db` file.

---

## Files Overview

* `lazada_scraper.py`: Contains functions specific to interacting with Lazada's website.
* `lazada.py`: Main script to initiate the scraping process.
* `database.py`: Handles database connections and operations.
* `config.py`: User-configurable settings for the scraper.
* `lazada_products.db`: SQLite database storing scraped product information. (You can change the name of your database)

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

*Note: This project is for educational and personal use. Ensure compliance with Lazada's terms of service when using this scraper.*

---
