import requests
from bs4 import BeautifulSoup, Comment


URL = "https://www.hicentral.com/hawaii-mortgage-rates.php"


def find_mortgage_table(soup):
	"""Find the most likely mortgage-rate table on the page."""
	candidate_tables = []

	for table in soup.find_all("table"):
		rows = table.find_all("tr")
		text = table.get_text(" ", strip=True).lower()
		has_rate_keywords = any(keyword in text for keyword in ["15-yr", "30-yr", "arm"])

		# Prefer tables that have many rows and rate-related keywords.
		if rows and has_rate_keywords:
			candidate_tables.append((len(rows), table))

	if not candidate_tables:
		return None

	candidate_tables.sort(key=lambda item: item[0], reverse=True)
	return candidate_tables[0][1]


def extract_mortgage_rows(table):
	"""Extract mortgage rate rows into dictionaries."""
	extracted_rows = []
	current_lender = ""

	for tr in table.find_all("tr"):
		cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
		if len(cells) not in (4, 5):
			continue

		if len(cells) == 5:
			lender_cell, loan_type, rate, points, apr = cells
		else:
			lender_cell = ""
			loan_type, rate, points, apr = cells

		# Lender appears only on the first line of each lender block.
		if lender_cell:
			current_lender = lender_cell

		extracted_rows.append(
			{
				"lender": current_lender,
				"loan_type": loan_type,
				"rate": rate,
				"points": points,
				"apr": apr,
			}
		)

	return extracted_rows


def extract_html_comments(soup):
	"""Extract non-empty HTML comments from the page."""
	comments = []

	for node in soup.find_all(string=lambda text: isinstance(text, Comment)):
		cleaned = " ".join(node.strip().split())
		if cleaned:
			comments.append(cleaned)

	return comments


response = requests.get(URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

mortgage_table = find_mortgage_table(soup)
if mortgage_table is None:
	raise RuntimeError("Could not find a mortgage rate table on the page.")

mortgage_rows = extract_mortgage_rows(mortgage_table)

print("Mortgage rate rows:")
for i, row in enumerate(mortgage_rows, start=1):
	print(
		f"{i:02d}. Bank: {row['lender']} | "
		f"Type: {row['loan_type']} | Rate: {row['rate']} | "
		f"Points: {row['points']} | APR: {row['apr']}"
	)

html_comments = extract_html_comments(soup)

print("\nHTML comments found:")
if html_comments:
	for i, comment in enumerate(html_comments, start=1):
		print(f"{i:02d}. {comment}")
else:
	print("No HTML comments found.")
