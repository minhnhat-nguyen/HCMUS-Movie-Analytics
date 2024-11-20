from src.crawl_data.themovie import MovieCrawler
from src.crawl_data.mojo import BoxOfficeMojoCrawler

crawler_the_movie = MovieCrawler()
crawler_mojo = BoxOfficeMojoCrawler()

crawler_the_movie.save_to_csv(num_pages=200, file_name="data/movies.csv")

crawler_the_movie.add_details_to_csv(input_file="data/movies.csv", output_file="data/movies.csv")

crawler_mojo.update_csv_with_box_office(input_file="data/movies.csv", output_file="data/movies.csv")