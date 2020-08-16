# Deployment

In the previous part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In this part of the tutorial, you'll learn how to deploy your application (a.k.a. put it into production or put it on the web).

## Setup

The easiest way to deploy web apps is with [heroku](https://heroku.com/). Hemlock-CLI builds on the [heroku-CLI]((https://devcenter.heroku.com/articles/heroku-cli)) for deployment. Find the setup page for your OS for specific instructions:

- [Windows](../setup/win.md)
- [Windows Subsystem for Linux](../setup/wsl.md)
- [Mac](../setup/mac.md)
- [Linux](../setup/linux.md)

## Debugging in a staging environment

Before we deploy our project 'for real', we're going to deploy to a staging environment using free heroku resources and run our debugger one more time. Why? Because the production environment is subtly different from your local environment, which can cause problems in very rare cases. The staging environment is virtually identical to the production environment, so if things go well in staging, our app should run smoothly in production.

### Deploying your app in staging

Deploying your application is as easy as:

```bash
$ hlk deploy
```

You'll be redirected to a page on the heroku website. If this is your first time deploying an app, heroku will prompt you to connect to your github account.

Once you're on the heroku page, make the following modifications to your application configuration:

1. Enter a name for your application.
2. Set your `PASSWORD`. You will need to enter this password to log in to the researcher dashboard to access your data.
3. Set your `URL_ROOT`. For example, if your project is named `my-first-project235`, your `URL_ROOT` would be `https://my-first-project235.herokuapp.com`. This tells the debugger where to look for your app.

Click 'Deploy app' and watch the magic happen. In 2-3 minutes, your survey will be online.

### Running the debugger

In the last part of the tutorial, we ran our debugger in the local environment. Now, we're going to run it in staging. First, let's hook up our project to our online application:

```bash
$ heroku git:remote -a <my-app-name>
```

Replacing `<my-app-name>` with your application name. For example, if your application is named `my-first-project235`, you'd enter:

```bash
$ heroku git:remote -a my-first-project235
```

Now, run the debugger:

```bash
$ hlk debug --staging
```

This is almost exactly what we did in the previous part of the tutorial. The difference is that we added the `--staging` flag, indicating that we're running the debugger in the staging environment.

Where's the webdriver? In production, Chromedriver needs to run in 'headless' mode, meaning you won't be able to see the debugger going through the survey in your browser. You will, however, see it going through pages in the terminal window.

Hopefully the debugger runs smoothly. If it doesn't, fix your code, update your application, and run the debugger again. Update your application with:

```bash
$ hlk update
```

Once you're satisfied that your app is as error-free as possible, we'll destroy the staging version to 'make room' for the production version:

```bash
$ heroku apps:destroy
```

## Deploying your application

We're finally ready to deploy our application *for real*. This is basically the same process as deploying to the staging environment, with a few small changes.

First, open `app.json`:

```bash
$ code app.json
```

We're going to modify this to give us more powerful compute resources. At the top of the file, we'll change our addons and formation from:

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

Save `app.json`.

Let's deploy our app and set our configuration variables like we did before:

```bash
$ hlk deploy
```

1. Enter a name for your application.
2. Set your `PASSWORD`.
3. Set your `URL_ROOT`.
4. **New step.** Set `DEBUG_FUNCTIONS` to `False`. This stops your application from creating debug functions. We're not going to run the debugger again at this point, so debug functions will just slow things down.

Like before, click 'Deploy app' at the bottom of the page.

Your app is now online, ready to send to the world! Don't forget to download your data, and destroy your application when you're finished:

```bash
$ heroku apps:destroy -a <my-app-name>
```

## Cost

How much will it cost me to play around with my app in production? Answer: $0.10. Calculation: This formation gives us a standard-0 database ($50/mo) and 10 standard-1x 'dynos' (like servers, $25/mo/dyno * 10 dynos = $250/mo). That's $300/mo total. Heroku prorates by the second, meaning that if you mess around with the app for 15 minutes, you'll be charged $300/mo * 1 mo/30 days * 1 day/24 hours * 1 hour/60 min * 15 min = $0.10. 

How much will it cost me to run a study with these resources? Answer: $5. Do the same math, but assume your study is online for half a day. 

**Side note.** The exact amount of compute power you need depends on the application. My recommendation for a standard-0 database and 10 standard-1x web dynos is a rough recommendation that will work well for most academic studies. [Read more about heroku resources here](https://www.heroku.com/pricing).

## Alternative deployment options

Hemlock uses a [Flask](https://flask.palletsprojects.com/en/1.1.x/) backend, which means you can deploy it just as you would any other Flask app. The [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) is, imho, the best resource for learning Flask, including deployment.

## Summary

Congratulations! You've made it through the hemlock tutorial. You can now initialize, modify, and deploy hemlock projects.

On the next page, I talk about some extra bells and whistles you'll likely find helpful.