import requests
from bs4 import BeautifulSoup
import pandas as pd

class BoxOfficeMojoCrawler:
    def __init__(self):
        self.base_url = "https://www.boxofficemojo.com/title/{imdb_id}/?ref_=bo_tt_tab#tabs"

    def fetch_data(self, imdb_id: str):=
        try:
            url = self.base_url.format(imdb_id=imdb_id)
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for IMDb ID {imdb_id}: {e}")
            return None

    def parse_data(self, html_content: str):
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            sections = soup.find_all("div", class_="a-section a-spacing-none a-spacing-top-base")

            data = []
            for section in sections:
                tables = section.find_all("table", class_="a-bordered")
                for table in tables:
                    # Find the region title
                    region_header = table.find_previous_sibling("h3")
                    if region_header:
                        region = self.clean_region_name(region_header.text.strip())

                        # Extract table rows (skip the header row)
                        rows = table.find_all("tr")
                        for row in rows:
                            cells = row.find_all("td")
                            if len(cells) >= 2:
                                opening = self.clean_currency(cells[2].text.strip()) if len(cells) > 1 else None
                                gross = self.clean_currency(cells[3].text.strip()) if len(cells) > 2 else None
                                data.append({"Region": region, "Opening": opening, "Gross": gross})
            return data
        except Exception as e:
            print(f"Error parsing HTML content: {e}")
            return []

    @staticmethod
    def clean_currency(value: str):
        try:
            return int(value.replace("$", "").replace(",", "")) if value else 0
        except ValueError:
            return 0

    @staticmethod
    def clean_region_name(region: str):
        return region.replace(",", "").replace(" ", "_").lower()

    def fetch_and_aggregate(self, imdb_id: str):
        html_content = self.fetch_data(imdb_id)
        if not html_content:
            return {}

        soup = BeautifulSoup(html_content, "html.parser")

        parsed_data = self.parse_data(html_content)
        data_by_region = {}

        for record in parsed_data:
            region = record["Region"]
            opening_key = f"{region}_opening"
            gross_key = f"{region}_gross"

            if opening_key not in data_by_region:
                data_by_region[opening_key] = 0
            if gross_key not in data_by_region:
                data_by_region[gross_key] = 0

            data_by_region[opening_key] += record["Opening"]
            data_by_region[gross_key] += record["Gross"]
        
        try:
            summary_section = soup.find("div", class_="mojo-performance-summary-table")
            if summary_section:
                domestic_section = summary_section.find("div", class_="a-section a-spacing-none")
                if domestic_section:
                    domestic_gross_span = domestic_section.find("span", class_="money")
                    data_by_region["domestic"] = (
                        self.clean_currency(domestic_gross_span.text.strip()) if domestic_gross_span else 0
                    )

                international_section = domestic_section.find_next_sibling("div", class_="a-section a-spacing-none") if domestic_section else None
                if international_section:
                    international_gross_span = international_section.find("span", class_="money")
                    data_by_region["international"] = (
                        self.clean_currency(international_gross_span.text.strip()) if international_gross_span else 0
                    )

                worldwide_section = international_section.find_next_sibling("div", class_="a-section a-spacing-none") if international_section else None
                if worldwide_section:
                    worldwide_gross_span = worldwide_section.find("span", class_="money")
                    data_by_region["worldwide"] = (
                        self.clean_currency(worldwide_gross_span.text.strip()) if worldwide_gross_span else 0
                    )
        except Exception as e:
            print(f"Error extracting summary data for IMDb ID {imdb_id}: {e}")

        return data_by_region


    def process_csv(self, input_file: str, output_file: str):
        try:
            df = pd.read_csv(input_file)

            if 'imdb_id' not in df.columns:
                print("Error: 'imdb_id' column is missing in the input CSV.")
                return

            for index, row in df.iterrows():
                imdb_id = row['imdb_id']
                print(f"Processing IMDb ID: {imdb_id}")
                regional_data = self.fetch_and_aggregate(imdb_id)
                for key, value in regional_data.items():
                    df.loc[index, key] = value

            df.to_csv(output_file, index=False)
            print(f"Processed data saved to {output_file}")
        except Exception as e:
            print(f"Error processing CSV file: {e}")