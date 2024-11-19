import json

# Load the JSON file
with open('/mnt/data/sample.json', 'r') as file:
    data = json.load(file)

# Extract filings
recent_filings = data.get('filings', {}).get('recent', {})
forms = recent_filings.get('form', [])
accession_numbers = recent_filings.get('accessionNumber', [])

# Filter for 10-K filings
ten_k_filings = [
    {"form": form, "accessionNumber": accession}
    for form, accession in zip(forms, accession_numbers)
    if form == "10-K"
]

# Display the filtered 10-K filings
for filing in ten_k_filings:
    print(filing)

# Optionally, save to a new JSON file
with open('/mnt/data/ten_k_filings.json', 'w') as output_file:
    json.dump(ten_k_filings, output_file, indent=4)
