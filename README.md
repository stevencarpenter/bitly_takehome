# Bitly Take Home Test

This was a fun project for me and I took liberty to explore some new frameworks in the process. This is my first time working with flask. I have done most of my endpoint work in JVM langs and using Spring Boot but I really wanted to use Python here for the ease of data munging, the super easy requests library and the ease with which python syntax can be understood by most people. I have used python extensively over the past year mostly for writing Airflow DAGs and custom mappers for hadoop streaming jobs. 

I made the decision to dockerize this to take away some of the pain involved with python env setup. I included instructions for setting up an env should you want to run the tests as well. As I mention again below, this is a simple, fast docker setup and there is a ton of optimization that could be done on the container, but for this use case it works well enough.

Flask was a natural choice because at least from this minor experience I was able to spin up JUST an endpoint and get going. To keep the endpoint code relatively simple I broke out the munging into functions which also made them easier to test without integrating the API. Instead I could just mock the pieces of the response that needed to be munged. 

## Building and deploying the image
I chose to use docker to deploy due to it's portability. It saves the trouble of scripting a virtualenv setup and will run on any machine that has docker installed. That said, you will need docker in order to run this endpoint. it can be installed from [here]().

Start by navigating to the root directory of my project.

First build the container:
```bash
docker build -t bitly:lastest .
```
This was a quick and dirty implementation so there is a lot of room for improvement on the container. You'll notice the image is a little large. I used the base Python 3 image for speed, but in production I would build a multi-stage build process with tests built in, a base that is super minimal like Alpine and only add the dependencies I need on there.

When the build finishes, look for the image id that is logged. It will look like this 
```bash
Step 7/7 : CMD python api.py
 ---> Running in 7356319556ef
Removing intermediate container 7356319556ef
 ---> 2a35516ea7cc
Successfully built 2a35516ea7cc    <-------**This guy**
Successfully tagged bitly:lastest
~/P/bitly ❯❯❯           
```

Next run the following command with the IMAGE_ID to bring up the container and also the endpoint.
```bash
docker run -d -p 5000:5000 <IMAGE_ID>
```

Everything should be up and running now. The result of the above command should be a long hash which is th econtainer id. To bring the container down when you are done testing, run:
```bash
docker kill <CONTAINER_ID>
```

For production there are much better ways to manage this as well as in dev by using docker-compose and down, but I kept this simple.
 

## curl commands
```bash
curl -X GET 'http://localhost:5000/bitly/clicks/average?access_token=<YOUR_TOKEN_HERE>'
curl -X GET 'http://localhost:5000/bitly/clicks/average?access_token=<YOUR_TOKEN_HERE>&unit=day&units=30'
curl -X GET 'http://localhost:5000/bitly/clicks/average?access_token=<YOUR_TOKEN_HERE>&unit=month&units=1'
curl -X GET 'http://localhost:5000/bitly/clicks/average?access_token=<YOUR_TOKEN_HERE>&unit=week&units=1'
curl -X GET 'http://localhost:5000/bitly/clicks/average?access_token=<YOUR_TOKEN_HERE>&unit=day&units=1'
```

Above are some sample curl commands. The base route with just your token provided will return the average clicks per country over the past 30 days for the default group id's bitlinks. I expanded on this a little bit and allowed the user to provide the units and unit to be used so that the user can drill down more. I also felt weird hardcoding things that seem like they should be configurable, however I did stop short of adding all the variability that I could supply to the existing bitly endpoints due to time and scope of the project.


## Running the tests
Running the tests is a little more involved then spinning up the containers because of the myriad ways that python is installed and managed on every developer's machine.

Start by making sure that you are using python3. You can tell by running 
```bash
python --version
```
Navigate to the root of my project.
You will then want to create a virtual env to hold this project's dependencies. 
```bash
virtualenv --python=/Users/stevecarpenter/.pyenv/versions/3.6.4/bin/python  venv/
```

I source the python version from the .pyenv folder because I use pyenv to manage versions. Your path to the python executable may be different.

Next source the env
```bash
source venv/bin/activate
```

Then install the requirements
```bash
pip install -r app/requirements.txt
```

Add pytest as well (I kept this out of the requirements to slim down the docker container a little bit because I am not running the tests on build in this process. To do that I would want a multi-stage build so that my final container doesn't have the bloat of the test code and dependencies. I felt that was out of scope for a 3-4 hour project.)
```bash
pip install pytest
```

Now to run the test, still from the root of my project run:
```bash
python -m pytest
```

There are four tests. I stopped short of adding integration testing because we do not share access to a token. I mainly tested the helper functions that do the data munging. There are more tests that could be done here like testing the route and integration testing the methods that hit the bitly apis.


## Performance
I wasn't able to get great performance in my testing with a small number of clicks on a few bitlinks. A lot of this came from the bitly endpoints themselves and with the number of API calls for many links it starts to add up. One thing that could be done here would be to add a cache, however if a link is popular then solving the cache invalidation problem to ensure accurate results would have been difficult to solve in the advised 3-4 hour time block.

Additionally, Python is not a performant language, though it's built in dict and list comprehension made the data munging really nice in this case. One area I could improve performance in this project is by using multiprocessing when I get the click metrics for each bitlink. This would be a considerable improvement for groups with many bitlinks,