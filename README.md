#Byprice test#

##Description##
Phantomjs and Selenium based webscraper that saves data to a PSQL database and API  to obtain data in json form


##clone the repo##

##Download phantomjs into scraper folder##

```$ mkdir scraper/phantomjs

$ cd scraper/phantomjs

$ curl -L -O https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2

$ tar --strip-components=1 -xvf phantomjs-$PHANTOM_JS_TAG-linux-x86_64.tar.bz2

$ mv bin/phantomjs ../.. && cd ../.. && rm -rf bin && cd ..```

##make virtual env##

```
$ pyvenv-3.5 env

$ source env/bin/activate
```
##install autoenv##

```
$ pip install autoenv==1.0.0

$ touch .env

$ echo "source `which activate.sh`" >> ~/.bashrc

$ source ~/.bashrc
```

##if postgresql is installed##

make the database:
```
$createdb bypricet
```
###set up locals in .env###

```
# Local DATABASE VARS:
export LDB_USER="$USER"
export LDB_PASSWORD="pass" # <- set this
export LDB_HOST="127.0.0.1"
export LDB_PORT="5432"
export LDB_DATABASE="bypricet"
```

##run migrations##
```
$ cd web
$ python manage.py db upgrade
$ cd ..
```

##Run the scraper##

```
$ python web/chedrauiScraper.py
```

##Run the application##

```
$ python web/app.py
```
