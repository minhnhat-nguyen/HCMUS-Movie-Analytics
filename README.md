<h1>
  <p align="center">
    Movie Analytics

  </p>
</h1>

This repository contains the code and resources for the Movie Analytics.

## Project Structure

The project is organized into the following folders:

- **data:** Contains datasets or data files used by the project.
- **docs:** Documentation for the project.
- **environments:** Contains the `Dockerfile` for creating developing environment.
- **notebooks:** Jupyter notebooks used for exploration, analysis, or testing.
- **scripts:** Contains scripts for various tasks (e.g., crawl data, training).
- **src:** Main code for this project

## Files

- **.env:** Environment variables file.
- **.gitignore:** Specifies files and directories to ignore for Git version control.
- **.pre-commit-config.yaml:** Configuration for pre-commit hooks.

## Getting started

### Create the environment
```
cd environments
pip install -r requirements.txt
```

## Run the application
```
bash ./scripts/test.sh
```