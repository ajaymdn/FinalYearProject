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
    filing_dates = recent_filings.get('filingDate', [])

    ten_k_filings = [
        {"accessionNumber": accession, "filingDate": filing_date}
        for form, accession, filing_date  in zip(forms, accession_numbers, filing_dates)
        if form == "10-K"
    ]

    formatted_urls = []

    for filing in ten_k_filings:
        accession_number = filing.get("accessionNumber", "")
        filing_date = filing.get("filingDate", "")

        if accession_number and filing_date:
            year = filing_date[:4]  # Extract the year from the filing date
            cik_number = accession_number.split("-")[0].lstrip("0")
            formatted_accession = accession_number.replace("-", "")
            url = f"https://www.sec.gov/Archives/edgar/data/{cik_number}/{formatted_accession}/{accession_number}.txt"
            formatted_urls.append({
                "accessionNumber": accession_number, 
                "url": url, 
                "filingYear": year  # Add the year to the output
            })
    
    output_file_path = f'./Edgar/All_10K_Filings_{company}.json'
    with open(output_file_path, 'w') as output_file:
        json.dump(formatted_urls, output_file, indent=4)

get_filings("0000034088")