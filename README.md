# EIA
or EVE Industry Assistant is an EVE online tool to help me manage my industry. It may or may not work for you as i am one of the few people actually running on linux(KUbuntu) , so windows, mac and even other linux flavours are unknown. Also I am **NOT** a developer so do not expect some thing mindblowing.

# Current plans

Tackle things regarding PI first, get to know how to use the EVE API and look forward from there, but there is alot of work to do before "real" industry can be done with this tool.

# Requirements

Use poetry to generate and use a virtual environment with all the nessesary packages. Also this application requires an database containing SDE data to function properly, you can get it from [fuzzworks dump](https://www.fuzzwork.co.uk/dump/). As of the time of writing this README get the latest sqlite one.

## Step by step

1. install [Poetry](https://python-poetry.org/docs/) as i use it to manage python virutal environments
2. download the latest sqlite from [fuzzworks dump](https://www.fuzzwork.co.uk/dump/) (almost 500Mb when unpacked)
3. unpack and place sqlite file in the sqlite folder 
    - make sure the unpacked file name is the same as in sqlitestuff.py connectToSDE
4. ```poetry install```
5. ```poetry shell```
6. ```python eia.py```