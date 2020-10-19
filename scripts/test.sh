#!/usr/bin/env bash

die () { echo "$1" >&2; exit 1; }

hash docker || { die "docker is not installed. Exiting..."; }

dockerOptions="-v """$(pwd):/opt/code/fwf_parser""""
tag="fwf_parser-test"
dockerRun="docker run $dockerOptions -t $tag"

echo "Building the image..."
if ! docker build --target test -f Dockerfile -t $tag .; then
    die "Failed to build the image"
fi

echo "Running the linter..."
if ! $dockerRun pylint fwf_parser tests; then

    die "Failed linting"
fi

echo "Running the tests..."
if ! $dockerRun pytest -v --cov fwf_parser; then

    die "Failed tests"
fi
