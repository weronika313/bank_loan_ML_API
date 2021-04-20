# bank loan ML API
Restful api for compare ML algorithms and predict bank loan status

## Technologies used

* **[Python3](https://www.python.org/downloads/)** - A programming language
* **[DRF](https://www.django-rest-framework.org/)** - Django REST framework is a powerful and flexible toolkit for building Web APIs.
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[Docker](https://docs.docker.com/)** – An open platform for developing, shipping, and running applications.

## Running

### Run localy

    $ docker build -t web:latest .
    $ docker run -d --name djangoProject -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
   
Stop then remove the running container once done:


    $ docker stop djangoProject
    $ docker rm djangoProject
    

## Usage

*  ### Compare ML algorithms
*  ### Predict bank loan status
*  ### Login
*  ### Register
*  ### Check avaiable ml algorithms 
*  ### Get API authentication Token



## Demployment

https://bank-loan-api.herokuapp.com/api/v1/





