#!/bin/bash

# Create a directory named "spider"
mkdir -p spider

# Navigate into the "spider" directory
cd spider

# Download the file from Google Drive
file_id="1TqleXec_OykOYFREKKtschzY29dUcVAQ"
file_name="downloaded_file.zip"

# Attempt to download the file using curl
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${file_id}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=$(awk '/download/ {print $NF}' ./cookie)&id=${file_id}" -o ${file_name}

# Unzip the downloaded file
unzip ${file_name}

# Clean up the downloaded zip file and cookie
rm ${file_name}
rm ./cookie

# Go back to the original directory
cd ..

echo "Download and extraction complete."
