# README: Books to Scrape Data Extraction Project

## Project Overview

This project involves a Python-based web scraping tool designed to extract detailed information about books from the "Books to Scrape" website. It captures data such as book titles, categories, ratings, prices, and image URLs. The tool is capable of scraping data from individual books, entire categories, and even the entire website.

## Project Structure

The project is divided into several Python scripts, each handling different aspects of the scraping process:

1. s_phase_1.py: Contains functions for extracting, transforming, and loading (ETL) data for individual books.

2. s_phase_2.py: Extends s_phase_1 functionalities to handle books from a specific category.

3. s_phase_3.py: The main driver script (this file) that utilizes the functions from s_phase_1.py and s_phase_2.py to extract data from all categories available on the website.

## Installation

Before running the scripts, ensure you have Python installed on your machine.
Additionally, open a terminal or command prompt and navigate to the directory where the requirements.txt file is located. Then, run the following command to install the required packages:

    ```bash
       pip install -r requirements.txt

## Usage

To run the main script and scrape data from the entire website, execute the following command in your terminal:

    ```bash
    python s_phase_3.py

This will scrape data from each category and save it in separate CSV files named after the category.

## Features

. Extracts book details including title, category, rating, price, availability, and image URL.
. Handles pagination to scrape data from categories spanning multiple pages.
. Dynamically creates directories for storing book images.
. Writes scraped data into CSV files for easy analysis and storage.

## Error Handling

The scripts include basic error handling for scenarios like missing data fields or failed image downloads. However, for robust production use, further enhancement in error handling is recommended.

## Limitations

. The current implementation processes requests sequentially, which could be slow for large datasets. Parallel processing could be implemented for performance improvement.
. The script does not have advanced error recovery mechanisms, which might be necessary for handling network issues or website structure changes.

## Disclaimer

This project is intended for educational purposes only. Web scraping should be done responsibly and in compliance with the website's terms of service or use policy. It's important to check robots.txt of the website and ensure your scraping activity is allowed.

## Contribution

Contributions to this project are welcome. Please ensure you follow good coding practices and thoroughly test any new features before submitting a pull request.

