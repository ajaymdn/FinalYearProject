from sec_edgar_api import EdgarClient
import json

# Specify user-agent string to pass to SEC to identify
# requests for rate-limiting purposes
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")

# Get submissions for Apple with the additional paginated files
# appended to the recent filings to prevent the need for extra
# manual pagination handling
json_object = json.dumps(edgar.get_submissions(cik="320193"), indent=4)

with open("sample.json", "w") as outfile:
    outfile.write(json_object)

# edgar.get_submissions(cik="320193", handle_pagination=False)

# print(edgar.get_company_concept(cik="320193", taxonomy="us-gaap", tag="AccountsPayableCurrent"))