# This dockerfile makes an image that contains our API environment
FROM ubuntu

RUN apt-get update && apt-get install --yes software-properties-common musl-tools
RUN apt-get update && \
    apt-get install --yes \
     build-essential wget unzip emacs vim net-tools graphviz protobuf-compiler sudo ipcalc moreutils
