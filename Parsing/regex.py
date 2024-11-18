import re

res = re.finditer(r"\b\w{5}\b", "Jessa and Kelly, Abigl")

for match in res:
    print(match.group())