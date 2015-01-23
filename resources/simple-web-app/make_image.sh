#!/bin/bash
docker build -t lonely_feynman .
CONTAINER_ID="$(docker run -d lonely_feynman /bin/bash)"
docker export ${CONTAINER_ID} > lonely_feynman.tar
