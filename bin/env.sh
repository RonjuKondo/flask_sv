
DOCKER_HOME=$HOME/docker_mysql_flask_sv/docker-mysql

IFS=$'\n'
for line in `cat $DOCKER_HOME/.env`
do
	export $line
done 
