# Check if the .env file exists
if [ -f .env ]; then
    # Load environment variables from the .env file
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found!"
fi
# Set the working directory to the current directory
export WORKDIR=$(pwd)
# Add the working directory to the PYTHONPATH
export PYTHONPATH="$WORKDIR:$PYTHONPATH"
python ./src/task/crawl_themovie.py