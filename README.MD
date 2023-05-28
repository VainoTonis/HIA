# EIA
or EVE Industry Assistant is an EVE online tool to help me manage my industry. It may or may not work for you as i am one of the few people actually running on linux, so windows, mac and even other linux flavours are unknown.


# Current plans

Basicly get everything related to PI, first off the info from EVE API, then move to more advanced stuff with the SDE.

# Running from source

1. Install Poetry
2. Activate poetry (poetry install command)
3. Activate virtual environment (poetry shell)
3. generate static files (python manage.py collectstatic)
4. Choose one way to run the server
    a. python manage.py runserver
        - This will simply run the django web server without the embedded web view
    b. python threadedEmbededWebView.py
        - This one runs django and embedded web browser in seperate threads

# PSA!
This is not something to be launched as a seperate website, i am simply using a browser as a frontend because it looks nicer faster (i am sorry pyfa). Also I am sort of familiar with doing websites so this seemed like a great project to refresh and lean new things both python and web dev related.

I  am not sure where this project is heading (Project completion and garbage bin are both very viable options), so one day this might be just depricated and slowly (or quickly) will decay away.

# Requirements

Atm while developing im using a seperate postgres server for my DB, depending how much people want other options i am willing to maybe think of sqlite or something similar. (Yes this app requires a database, i dont want to mess with 10 billion text files or massive CSV files like a caveman)

# Licence
TODO: ADD LICENCE