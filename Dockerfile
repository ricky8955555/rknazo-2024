FROM rust:alpine AS build

RUN apk add --update --no-cache build-base python3

WORKDIR /rknazo
COPY ./ .

RUN python3 -m build


FROM alpine:latest

RUN apk add --update --no-cache python3 curl bind-tools netcat-openbsd tcpdump

WORKDIR /rknazo
COPY --from=build /rknazo/out ./
RUN mv ./solver /usr/bin/nazosolver

ENTRYPOINT [ "python3", ".utils/start.py" ]
