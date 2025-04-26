# Individual Project (IP)

Final Year Project - ESG Prediction using 10-K Filings

## Project Overview
This project is focused on analyzing industry ESG trends and generating insights using advanced natural language processing techniques on financial texts. It aims to provide a comprehensive analysis of industries such as TECH or OIL over a target year range (2014 to 2024) by leveraging financial data and machine learning models.

## Features
- Generate URLs for data collection using `edgar.ipynb`.
- Perform dictionary-based analysis using `Dictionary/dictionary-based.ipynb`.
- Conduct sentiment analysis with `FinBERT/finbert.ipynb`.
- Extract topics and trends using `BERTopic/bertopic.ipynb`.
- Flexible configuration for target year range (2014–2024) and industry selection (TECH or OIL).

## Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the project:
    - Generate URLs:
        ```bash
        jupyter notebook edgar.ipynb
        ```
    - Perform analysis using one of the following notebooks:
        - Dictionary-based analysis:
            ```bash
            jupyter notebook Dictionary/dictionary-based.ipynb
            ```
        - Sentiment analysis with FinBERT:
            ```bash
            jupyter notebook FinBERT/finbert.ipynb
            ```
        - Topic modeling with BERTopic:
            ```bash
            jupyter notebook BERTopic/bertopic.ipynb
            ```