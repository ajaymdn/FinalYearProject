from sec_edgar_api import EdgarClient
import json
import os

# Apple CIK: 0000320193
# Microsoft CIK: 0000789019
# Amazon CIK: 0001018724
# Google CIK: 0001652044

def get_filings(cik):
    edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")

    data = edgar.get_submissions(cik)
    company = data.get('tickers', [])[0]
    
    recent_filings = data.get('filings', {}).get('recent', {})
    forms = recent_filings.get('form', [])
    accession_numbers = recent_filings.get('accessionNumber', [])

    ten_k_filings = [
        {"accessionNumber": accession}
        for form, accession in zip(forms, accession_numbers)
        if form == "10-K"
    ]

    formatted_urls = []

    for filing in ten_k_filings:
        accession_number = filing.get("accessionNumber", "")
        if accession_number:
            cik = accession_number.split("-")[0].lstrip("0")
            formatted_accession = accession_number.replace("-", "")
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{formatted_accession}/{accession_number}.txt"
            formatted_urls.append({"accessionNumber": accession_number, "url": url})
    
    output_file_path = f'./10K-URL/{company}.json'
    with open(output_file_path, 'w') as output_file:
        json.dump(formatted_urls, output_file, indent=4)

get_filings("0000320193")