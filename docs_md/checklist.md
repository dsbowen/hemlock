# Checklist

This is a checklist of the steps involved in initializing, editing, and deploying a hemlock project.

This will make sense after you [go through the tutorial](tutorial/intro.md).

## Initialize

```bash
$ hlk init <my-project-name> <my-github-username> <my-github-token>
$ cd <my-project-name>
```

!!! note "Additional steps for Windows git bash"
    ```bash
    hlk setup-venv <my-project-name>
    ```

!!! note "Additional steps for WSL"
    Open `env.yaml` and add the following line:

    ```yaml
    WSL_DISTRIBUTION: Ubuntu-20.04 # or other WSL distribution
    ```

## Edit

Iterate quickly on the blackboard:

```bash
$ jupyter notebook # open blackboard.ipynb, Kernel >> Change kernel >> <my-project-name>
```

Edit survey files:

```bash
$ code survey.py
```

Run locally:

```bash
$ hlk serve
```

Debug:

```bash
$ hlk debug
```

## Deploy

Deploy to and debug in staging:

```bash
$ hlk deploy # make sure to set the PASSWORD and URL_ROOT environment variables
$ heroku git:remote -a <my-app-name>
$ hlk debug --staging
```

Destroy the staging app:

```bash
$ heroku apps:destroy
```

Change `app.json` from:

```json
{
    "addons": ["heroku-postgresql:hobby-dev"],
    "formation": {
        "web": {"quantity": 1, "size": "free"}
    },
    ...
```

to:

```json
{
    "addons": ["heroku-postgresql:standard-0"],
    "formation": {
        "web": {"quantity": 10, "size": "standard-1x"}
    },
    ...
```

Deploy in production:

```bash
hlk deploy # set PASSWORD, URL_ROOT, and DEBUG_FUNCTIONS
```