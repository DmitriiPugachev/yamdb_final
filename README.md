![example workflow](https://github.com/dmitriipugachev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Description:
[This one API for YaMDb](https://github.com/DmitriiPugachev/api_yamdb) with a CI/CD pipeline and Docker infrastructure.
#### You can:
  * run the full project in docker containers;
  * create new users;
  * get, create, change and delete users;
  * get and change an own account info;
  * get, create and delete categories;
  * get, create and delete genres;
  * get, create, change and delete title info;
  * get, create, change and delete reviews;
  * get, create, change and delete comments;
#### Techs:
  * requests==2.26.0
  * django==3.0.5
  * djangorestframework==3.11.0
  * djangorestframework-simplejwt==4.3.0
  * python-dotenv==0.13.0
  * django-filter==21.1
  * asgiref==3.2.10
  * gunicorn==20.0.4
  * psycopg2-binary==2.8.5
  * PyJWT==1.7.1
  * pytz==2020.1
  * sqlparse==0.3.1
  * postgres==12.4
  * nginx==1.19.3
### How to run the project local:
Clone the repo and go to the base directory:
```bash
git clone https://github.com/DmitriiPugachev/yamdb_final.git
```
```bash
cd yamdb_final
```
Create ```.env``` file in the root project directory with variables like in ```.env.example``` file.

Install Docker. [This gide](https://docs.docker.com/engine/install/ubuntu/) help you.

Build an image and run all the containers:
```bash
docker-compose up -d --build
```
Apply migrations:
```bash
docker-compose exec web python manage.py migrate --noinput
```
Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```
Collect static files:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```
Copy the datadump in the web container:
```bash
docker cp fixtures.json <CONTAINER_ID>:/code/fixtures.json
```
Load data to the database:
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```
### How to run project global:
Fork [this repo](https://github.com/DmitriiPugachev/yamdb_final.git) to your
GitHub account.

Create your DockerHub account.

Create your remote virtual machine.

On GitHub in repo Settings add secret variables for workflow like 
in ```.env.example``` file.

Run workflow in GitHub Actions.

Connect to your remote virtual machine:
```bash
ssh <username>@<public_ip>
```
Install Docker:
```bash
sudo apt install docker.io
```
Install [docker-compose](https://docs.docker.com/compose/install/).

Copy ```docker-compose.yaml```from local machine to remote virtual machine:
```bash
scp yamdb_final/docker-compose.yaml <username>@<public_ip>:/home/<username>/
```
Create directory for nginx on remote machine:
```bash
mkdir nginx
```
Copy ```nginx/default.conf``` from local machine to remote virtual machine:
```bash
scp yamdb_final/nginx/default.conf <username>@<public_ip>:/home/<username>/nginx/
```
Go to the running web container on your remote virtual machine:
```bash
sudo docker exec -it <CONTAINER_ID> bash
```
Apply migrations, create superuser, collect static files, copy dumpdata 
file to the container and load this data th the database like 
in ```How to run the project local```.

Before every command don't forget to add:
```bash
sudo
```

### Links
[redoc and all possible requests examples](http://localhost/redoc/) this link is for local usage

[admin account](http://localhost/admin/)  this link is for local usage
### Author
Dmitrii Pugachev
