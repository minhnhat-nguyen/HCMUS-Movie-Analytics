# from src.crawl_data.themovie import MovieCrawler

# crawler = MovieCrawler()

# crawler.save_to_csv(num_pages=2, file_name="movies.csv")

# crawler.add_details_to_csv(input_file="movies.csv", output_file="movies_with_details.csv")

from src.crawl_data.mojo import BoxOfficeMojoCrawler

# crawler = BoxOfficeMojoCrawler()
# imdb_id = "tt16366836"  # IMDb ID của phim
# output_file = "aggregated_box_office_data.csv"

# crawler.crawl_and_aggregate(imdb_id, output_file)

crawler = BoxOfficeMojoCrawler()
input_csv = "data/movies.csv"  # Replace with your input file
output_csv = "data/movies.csv"  # Replace with your desired output file
crawler.process_csv(input_csv, output_csv)