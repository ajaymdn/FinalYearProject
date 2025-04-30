# Final Year Project - ESG Prediction using 10-K Filings

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [License](#license)

## Project Overview
This project analyzes industry ESG (Environmental, Social, Governance) trends using advanced natural language processing (NLP) techniques on 10-K financial filings. It provides insights into industries such as Technology (TECH) or Oil & Gas (OIL) over the period from 2014 to 2024 by leveraging financial data and machine learning models.

## Features
- **URL Generation**: Generate URLs for 10-K filings data collection using `edgar.ipynb`.
- **Dictionary-Based Analysis**: Analyze text using predefined dictionaries in `Dictionary/dictionary-based.ipynb`.
- **Sentiment Analysis**: Perform sentiment analysis on financial texts with `FinBERT/finbert.ipynb`.
- **Topic Modeling**: Extract topics and trends using `BERTopic/bertopic.ipynb`.
- **Flexible Configuration**: Select target year range (2014-2024) and industry (TECH or OIL).

## Prerequisites
- Python 3.11.4
- Jupyter Notebook
- Git
- Required Python packages (listed in `requirements.txt`)

## Setup Instructions
1. **Clone the repository**:
    ```bash
    git clone https://github.com/ajaymdn/FinalYearProject.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd FinalYearProject
    ```
3. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the notebooks**:
    - Generate URLs for data collection:
        ```bash
        jupyter notebook edgar.ipynb
        ```
    - Perform analysis using one of the following:
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