import requests
import pandas as pd
import os
import time

class MovieCrawler:
    def __init__(self):
        self.api_key = os.getenv("THE_MOVIE_DB_API_KEY")
        self.access_token = os.getenv("THE_MOVIE_DB_ACCESS_TOKEN")
        self.base_url = os.getenv("THE_MOVIE_DB_BASE_URL")
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_movies(self, num_pages: int, max_retries: int = 5) -> pd.DataFrame:
        entries = []
        url_template = self.base_url + "/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc"

        for page in range(1, num_pages + 1):
            for attempt in range(max_retries):
                response = requests.get(url_template.format(page=page), headers=self.headers)
                if response.status_code == 200:
                    break
                time.sleep(1)
            else:
                raise Exception(f"Failed to get data for page {page} after {max_retries} retries.")
            
            data = response.json().get("results", [])
            entries.extend(data)

        return pd.DataFrame(entries)

    def save_to_csv(self, num_pages: int, file_name: str):
        raw_data = self.get_movies(num_pages)
        raw_data.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")

    def get_movie_details(self, movie_id: int) -> dict:
        url = f"{self.base_url}/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch movie details for ID {movie_id}. HTTP Status: {response.status_code}")

        data = response.json()

        return {
            "budget": data.get("budget"),
            "genres": [genre["name"] for genre in data.get("genres", [])],
            "imdb_id": data.get("imdb_id"),
            "production_companies": [company["name"] for company in data.get("production_companies", [])],
            "production_countries": [country["name"] for country in data.get("production_countries", [])],
            "revenue": data.get("revenue"),
            "runtime": data.get("runtime"),
            "status": data.get("status"),
            "tagline": data.get("tagline"),
            "spoken_languages": [lang["name"] for lang in data.get("spoken_languages", [])]
        }

    def add_details_to_csv(self, input_file: str, output_file: str):
        """
        Read a CSV file with movie IDs, fetch additional details for each movie, 
        and save the updated data to a new CSV file.

        Args:
            input_file (str): Path to the input CSV file.
            output_file (str): Path to save the updated CSV file.
        """
        # Load the existing CSV
        movies = pd.read_csv(input_file)

        # Initialize additional fields
        movies["budget"] = None
        movies["genres"] = None
        movies["imdb_id"] = None
        movies["production_companies"] = None
        movies["production_countries"] = None
        movies["revenue"] = None
        movies["runtime"] = None
        movies["status"] = None
        movies["tagline"] = None
        movies["spoken_languages"] = None

        # Fetch details for each movie ID
        for index, row in movies.iterrows():
            try:
                movie_id = row["id"]
                details = self.get_movie_details(movie_id)
                
                # Update the DataFrame with new details
                movies.at[index, "budget"] = details["budget"]
                movies.at[index, "genres"] = ", ".join(details["genres"])
                movies.at[index, "imdb_id"] = details["imdb_id"]
                movies.at[index, "production_companies"] = ", ".join(details["production_companies"])
                movies.at[index, "production_countries"] = ", ".join(details["production_countries"])
                movies.at[index, "revenue"] = details["revenue"]
                movies.at[index, "runtime"] = details["runtime"]
                movies.at[index, "status"] = details["status"]
                movies.at[index, "tagline"] = details["tagline"]
                movies.at[index, "spoken_languages"] = ", ".join(details["spoken_languages"])
            except Exception as e:
                print(f"Failed to fetch details for movie ID {row['id']}: {e}")

        # Save the updated DataFrame to a new CSV file
        movies.to_csv(output_file, index=False)
        print(f"Updated data saved to {output_file}")