#!/bin/bash

docker run \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio1 \
   -v H:\\minio_storage:/data \
   -e "MINIO_ROOT_USER=ROOTUSER" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   -d \
   quay.io/minio/minio server /data --console-address ":9090" 