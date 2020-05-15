# docker run -it # `docker run` option - interactive session, attach to the container after it starts \
# --rm # `docker run` option - remove the container after it exits \
# mysql:latest # image and version tag we are trying to use \
# mysql # command we are passing to entrypoint of container \
# -h${MYSQL_HOST} # host used by command `mysql` \
# -u${MYSQL_USER} # username used by command `mysql` \
# -p${MYSQL_PASSWORD}  # password used by command `mysql` 

docker run -it \
--rm \
mysql:latest \
mysql \
-h${MYSQL_HOST} \
-u${MYSQL_USER} \
-p${MYSQL_PASSWORD}