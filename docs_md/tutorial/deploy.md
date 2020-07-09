# Deployment

In the previous part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In this part of the tutorial, you'll learn how to deploy your application (i.e. put it on the web).

## Setting a password

If we were to deploy our study as is, anyone would be able to go to our app and download our study data. Setting a password is easy. Add this to the top of `survey.py`:

```python
from hemlock import settings

settings.update({'password': 'my-password'})
```

Run your app and go to <http://localhost:5000/download/>. You'll be redirected to a login page where you have to enter a password to access the download page.

## Deployment options

Hemlock uses a [Flask](https://flask.palletsprojects.com/en/1.1.x/) backend, which means you can deploy it just as you would any other Flask app. The [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) is, imho, the best resource for learning Flask, including deployment.

I remember deployment was the scariest part of this whole process when I was starting out. So, if you're using the hemlock template and hemlock-CLI, I've built in some tools to make this as easy as possible for you.

## Setup with heroku

The easiest way to deploy web apps is with [heroku](https://heroku.com/). The hemlock-CLI builds on the [heroku-CLI]((https://devcenter.heroku.com/articles/heroku-cli)) for deployment.

You can install these with hemlock-CLI:

```bash
$ hlk setup win --heroku
```

You will be prompted to login and create an account. All deployment options, including heroku, costs money, but not much, and hemlock studies aren't usually resource intensive. For reference, most hemlock studies I've run cost less than $10. Heroku also offers free resources so you can preview your app online without paying anything. 

Close and re-open your terminal, then verify your installation with:

```bash
$ heroku --version
```

## Production-lite

Before scaling up your app, I recommend previewing it in what I call a 'production-lite' environment using free heroku resources:

```bash
$ hlk deploy <my-app-name>
```

Make sure your app name is unique. I do this by adding a few random digits to the end of the app name.

Once this process finishes (expect 5-10 minutes), you'll be able to see your app at <http://my-app-name.herokuapp.com/>.

Go through your app and check for bugs before you start purchasing time on heroku servers. In addition to going through it manually, you can run the debugger in the production environment with:

```bash
$ hlk debug --prod
```

Where's the webdriver? In production, Chromedriver needs to run in 'headless' mode, meaning you won't be able to see the debugger going through the survey in your browser. You will, however, see it going through pages in the terminal window.

If you later discover a bug, you can update your app with:

```bash
$ hlk update
```

## Production

When you're satisfied that your app isn't going to crash, scale it up with:

```bash
$ hlk production
```

This will destroy your existing toy database (and redis server, if you have one), and you'll be prompted to enter the name of your app to confirm.

You're now renting a heroku database and 10 web processes. If you don't know what this means, don't worry. As of 07/09/2020, these resources cost just more than half a cent per minute. If you play with your hemlock app for the next 10 minutes, it'll cost \$0.07. If you run an MTurk study and leave it up for the next 12 hours, it'll cost \$5.

Importantly, when you're done with your app, destroy it with:

```bash
$ hlk destroy
```

## Modifying your resource use

You can modify the resources you use in production by editing the `env/production-scale.yml` file. See <https://heroku.com/> for details on resource use.

## Summary

Congratulations! You've made it through the hemlock tutorial. You can now initialize, modify, and deploy hemlock projects.

On the next page, I talk about some extra bells and whistles you'll likely find helpful.