from playwright.sync_api import sync_playwright
import csv
import pandas as pd

# 5k Data
all_rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 64):
        url = f"https://worldathletics.org/records/all-time-toplists/middlelong/5000-metres/all/men/senior?regionType=world&page={page_num}&bestResultsOnly=true&firstDay=1899-12-31&lastDay=2025-10-02&maxResultsByCountry=all&eventId=10229609&ageCategory=senior"
        page.goto(url, timeout=60000)
        
        page.wait_for_selector("table.records-table tbody tr", timeout=60000)
        rows = page.query_selector_all("table.records-table tbody tr")
        
        if not rows:
            print(f"No rows found on page {page_num}, stopping early.")
            break
        
        for row in rows:
            cells = row.query_selector_all("td")
            row_text = [cell.inner_text().strip() for cell in cells]
            all_rows.append(row_text)

    browser.close()

df = pd.DataFrame(all_rows)
df = df[['rank', 'mark', 'competitor', 'country', 'year']]
df.to_csv("results_5k.csv", index=False, header=False)

# 10k Data
all_rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 71):
        url = f"https://worldathletics.org/records/all-time-toplists/middlelong/10000-metres/all/men/senior?regionType=world&page={page_num}&bestResultsOnly=true&firstDay=1899-12-31&lastDay=2025-10-03&maxResultsByCountry=all&eventId=10229610&ageCategory=senior"
        page.goto(url, timeout=60000)
        
        page.wait_for_selector("table.records-table tbody tr", timeout=60000)
        rows = page.query_selector_all("table.records-table tbody tr")
        
        if not rows:
            print(f"No rows found on page {page_num}, stopping early.")
            break
        
        for row in rows:
            cells = row.query_selector_all("td")
            row_text = [cell.inner_text().strip() for cell in cells]
            all_rows.append(row_text)

    browser.close()

df = pd.DataFrame(all_rows)
df = df[['rank', 'mark', 'competitor', 'country', 'year']]
df.to_csv("results_10k.csv", index=False, header=False)

# Half Marathon Data
all_rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 108):
        url = f"https://worldathletics.org/records/all-time-toplists/middlelong/10000-metres/all/men/senior?regionType=world&page={page_num}&bestResultsOnly=true&firstDay=1899-12-31&lastDay=2025-10-03&maxResultsByCountry=all&eventId=10229610&ageCategory=senior"
        page.goto(url, timeout=60000)
        
        page.wait_for_selector("table.records-table tbody tr", timeout=60000)
        rows = page.query_selector_all("table.records-table tbody tr")
        
        if not rows:
            print(f"No rows found on page {page_num}, stopping early.")
            break
        
        for row in rows:
            cells = row.query_selector_all("td")
            row_text = [cell.inner_text().strip() for cell in cells]
            all_rows.append(row_text)

    browser.close()

df = pd.DataFrame(all_rows)
df = df[['rank', 'mark', 'competitor', 'country', 'year']]
df.to_csv("half_marathon_results.csv", index=False, header=False)

# Marathon Data
all_rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 56):
        url = f"https://worldathletics.org/records/all-time-toplists/road-running/marathon/all/men/senior?regionType=world&page={page_num}&bestResultsOnly=true&firstDay=1899-12-31&lastDay=2025-10-03&maxResultsByCountry=all&eventId=10229634&ageCategory=senior"
        page.goto(url, timeout=60000)
        
        page.wait_for_selector("table.records-table tbody tr", timeout=60000)
        rows = page.query_selector_all("table.records-table tbody tr")
        
        if not rows:
            print(f"No rows found on page {page_num}, stopping early.")
            break
        
        for row in rows:
            cells = row.query_selector_all("td")
            row_text = [cell.inner_text().strip() for cell in cells]
            all_rows.append(row_text)

    browser.close()

df = pd.DataFrame(all_rows)
df = df[['rank', 'mark', 'competitor', 'country', 'year']]
df.to_csv("marathon_results.csv", index=False, header=False)