#!/bin/bash

# Execute the command to generate files
docker run --rm -v $(pwd):/out -v $(pwd):/protos pseudomuto/protoc-gen-doc --doc_opt=html,index.html val.proto types.proto

/home/ruz4fe/Downloads/protodot -src $(pwd)/val.proto -generated $(pwd) -output val

# Check if index.html file exists and open it in Chrome
if [ -f "$(pwd)/index.html" ]; then
    echo "index.html file generated successfully."
    google-chrome $(pwd)/index.html &
else
    echo "Error: index.html file not generated."
fi

# Check if val.dot.svg file exists and open it in Chrome
if [ -f "$(pwd)/val.dot.svg" ]; then
    echo "val.dot.svg file generated successfully."
    google-chrome $(pwd)/val.dot.svg &
else
    echo "Error: val.dot.svg file not generated."
fi
