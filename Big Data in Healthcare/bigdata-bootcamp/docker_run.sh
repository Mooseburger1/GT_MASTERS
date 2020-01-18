docker run -it --privileged=true \
  --cap-add=SYS_ADMIN \
  -m 8192m -h bootcamp.local \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  -v /:/mnt/host \
  sunlab/bigbox:latest \
  /bin/bash
