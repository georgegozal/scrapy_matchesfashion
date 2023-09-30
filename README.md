# scrapy_matchesfashion

Scrapy spider for scraping women's and men's shoes data from the MatchesFashion website.

## Overview

This Scrapy spider allows you to scrape shoe data, including product details and prices, from the MatchesFashion website. The spider is designed to scrape both women's and men's shoe categories.

## Usage

1. Clone the repository to your local machine:

       git clone https://github.com/georgegozal/scrapy_matchesfashion.git

2. Navigate to the project directory

       cd scrapy_matchesfashion
3. Install the required dependencies:

        pip install -r requirements.txt
    

4. Run the code

        scrapy crawl shoes -O shoes.csv
