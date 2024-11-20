import requests
from bs4 import BeautifulSoup
import pandas as pd


class BoxOfficeMojoCrawler:
    def __init__(self):
        self.base_url = "https://www.boxofficemojo.com/title/{imdb_id}/?ref_=bo_tt_tab#tabs"

    def fetch_data(self, imdb_id: str):
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
            sections = soup.find_all("div", class_="a-section mojo-gutter")

            data = []
            for section in sections:
                tables = section.find_all("table", class_="a-bordered")
                for table in tables:
                    # Find the region title
                    region_header = table.find_previous_sibling("h3")
                    if region_header:
                        region = self.clean_region_name(region_header.text.strip())

                        # Extract table rows (skip the header row)
                        rows = table.find_all("tr")[1:]
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

    def crawl_movie(self, imdb_id: str):
        html_content = self.fetch_data(imdb_id)
        if html_content:
            return self.parse_data(html_content)
        return []

    def update_csv_with_box_office(self, input_file: str, output_file: str):
        df = pd.read_csv(input_file)

        regions = ["domestic", "asia_pacific", "europe_middle_east_and_africa", "latin_america"]
        for region in regions:
            df[f"{region}_opening"] = None
            df[f"{region}_gross"] = None

        for index, row in df.iterrows():
            imdb_id = row["imdb_id"] 
            print(f"Processing IMDb ID: {imdb_id}")

            try:
                movie_data = self.crawl_movie(imdb_id)

                region_data = {region: {"opening": None, "gross": None} for region in regions}
                for record in movie_data:
                    region = record["Region"]
                    if region in region_data:
                        region_data[region]["opening"] = record["Opening"]
                        region_data[region]["gross"] = record["Gross"]

                for region in regions:
                    df.at[index, f"{region}_opening"] = region_data[region]["opening"]
                    df.at[index, f"{region}_gross"] = region_data[region]["gross"]

            except Exception as e:
                print(f"Failed to process IMDb ID {imdb_id}: {e}")
                continue

        df.to_csv(output_file, index=False)
        print(f"Updated data saved to {output_file}")