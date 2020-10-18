#!/usr/bin/env bash

die () { echo "$1" >&2; exit 1; }

hash docker || { die "docker is not installed. Exiting..."; }

tag="fwf_parser"
dockerRun="docker run -t $tag"

echo "Building the image..."
if ! docker build --target app -f Dockerfile -t $tag .; then
    die "Failed to build the image"
fi

docker run -v $(pwd)/sample_data:/opt/code/fwf_parser/sample_data -t $tag $1 $2 $3 $4
