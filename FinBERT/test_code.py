from transformers import BertForSequenceClassification, BertTokenizer, pipeline
import json
import os
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')

# Initialize FinBERT-ESG model (CUDA-enabled)
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-esg', num_labels=4)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-esg')
nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer, truncation=True, max_length=512, device=0)

# Placeholder for converttotext (extracts sentences from filing URL)
def converttotext(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Sample Company <admin@sample.com>"})
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        sentences = nltk.sent_tokenize(text)
        return sentences
    except Exception as e:
        raise Exception(f"Failed to convert URL {url}: {e}")

# Placeholder for calculate_average_and_std_esg (computes ESG scores)
def calculate_average_and_std_esg(sentences, nlp, batch_size=32):
    try:
        # Batch sentences for efficient GPU inference
        scores = {'environment': [], 'social': [], 'governance': []}
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            results = nlp(batch, padding=True, truncation=True, max_length=512)
            for res in results:
                label = res['label'].lower()
                score = res['score'] if 'positive' in label else -res['score']  # Adjust for sentiment
                if 'environment' in label:
                    scores['environment'].append(score)
                elif 'social' in label:
                    scores['social'].append(score)
                elif 'governance' in label:
                    scores['governance'].append(score)

        # Compute averages and stds
        result = {
            'environment_score_avg': np.mean(scores['environment']) if scores['environment'] else 0,
            'social_score_avg': np.mean(scores['social']) if scores['social'] else 0,
            'governance_score_avg': np.mean(scores['governance']) if scores['governance'] else 0,
            # 'environment_score_std': np.std(scores['environment'], ddof=1) if len(scores['environment']) > 1 else 0,
            # 'social_score_std': np.std(scores['social'], ddof=1) if len(scores['social']) > 1 else 0,
            # 'governance_score_std': np.std(scores['governance'], ddof=1) if len(scores['governance']) > 1 else 0
        }
        return result
    except Exception as e:
        raise Exception(f"Error in ESG calculation: {e}")

def process_company(company, target_year, nlp):
    """Process a single company’s filing, returning results or None on error."""
    try:
        sentences = converttotext(company['url'])
        print(f"Company: {company['company']}, Sentence count: {len(sentences)}")

        if len(sentences) > 200:
            scores = calculate_average_and_std_esg(sentences, nlp)
            company['environment_score_avg'] = scores['environment_score_avg']
            company['social_score_avg'] = scores['social_score_avg']
            company['governance_score_avg'] = scores['governance_score_avg']
            return company
        return None
    except Exception as e:
        print(f"Error processing {company['company']}: {e}")
        return None

def process_year(target_year, industry, nlp):
    """Process all companies for a given year, parallelizing company processing."""
    print(f"Processing year: {target_year}")
    try:
        file_path = f"Edgar/10K_URL_{industry}/All_10K_Filings_{target_year}.json"
        if not os.path.exists(file_path):
            print(f"File not found for {target_year}")
            return [], 0, 0, 0, 0, 0, 0

        with open(file_path, "r") as read_file:
            companies = json.load(read_file)

        valid_companies = []
        max_workers = 4  # Adjust based on CPU cores and GPU memory

        # Parallelize company processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_company = {executor.submit(process_company, company, target_year, nlp): company for company in companies}
            for future in tqdm(as_completed(future_to_company), total=len(companies), desc=f"Companies in {target_year}"):
                result = future.result()
                if result:
                    valid_companies.append(result)

        final_companies = [company['company'] for company in valid_companies]
        print(f"Companies processed: {final_companies}")

        if valid_companies:
            environment_avg_list = [company['environment_score_avg'] for company in valid_companies]
            social_avg_list = [company['social_score_avg'] for company in valid_companies]
            governance_avg_list = [company['governance_score_avg'] for company in valid_companies]

            return (
                valid_companies,
                np.mean(environment_avg_list) if environment_avg_list else 0,
                np.std(environment_avg_list, ddof=1) if len(environment_avg_list) > 1 else 0,
                np.mean(social_avg_list) if social_avg_list else 0,
                np.std(social_avg_list, ddof=1) if len(social_avg_list) > 1 else 0,
                np.mean(governance_avg_list) if governance_avg_list else 0,
                np.std(governance_avg_list, ddof=1) if len(governance_avg_list) > 1 else 0
            )
        return [], 0, 0, 0, 0, 0, 0

    except Exception as e:
        print(f"Error processing year {target_year}: {e}")
        return [], 0, 0, 0, 0, 0, 0

# Main execution
target_years = range(2014, 2025)
industry = "TECH"

environment_scores = []
environment_stds = []
social_scores = []
social_stds = []
governance_scores = []
governance_stds = []

# Process years sequentially, parallelizing within each year
for target_year in tqdm(target_years, desc="Processing years"):
    valid_companies, env_avg, env_std, soc_avg, soc_std, gov_avg, gov_std = process_year(target_year, industry, nlp)
    
    environment_scores.append(env_avg)
    environment_stds.append(env_std)
    social_scores.append(soc_avg)
    social_stds.append(soc_std)
    governance_scores.append(gov_avg)
    governance_stds.append(gov_std)

# Optional: Save results
results = {
    "years": list(target_years),
    "environment_scores": environment_scores,
    "environment_stds": environment_stds,
    "social_scores": social_scores,
    "social_stds": social_stds,
    "governance_scores": governance_scores,
    "governance_stds": governance_stds
}
with open(f"esg_results_{industry}.json", "w") as f:
    json.dump(results, f, indent=4)

print("Processing complete. Results saved to esg_results_TECH.json")