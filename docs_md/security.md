# Security features

## Heroku and Amazon Web Services

The location of your data depends on your method of deployment. In the tutorial, I suggest deploying through heroku, which in turn deploys your application using AWS cloud computing. Both have extensive security infrastructures. Read more about [heroku security](https://www.heroku.com/policy/security) and [AWS security](https://aws.amazon.com/security/).

## Secure Sockets Layer (SSL) certification

Hemlock-CLI's `hlk production` command, which scales your application in a production environment before distribution to participants, automatically creates an SSL certificate for your application. Hemlock uses [flask talisman](https://github.com/GoogleCloudPlatform/flask-talisman), developed by Google Cloud Platform, to force HTTPS requests.

Hemlock's default content security policy allows application content from only the following third parties:

1. Google API
2. JQuery
3. JSDeliver
4. Bootstrap

## Password protection

Hemlock users should password protect their applications before distribution to participants. This can be done simply with:

```python
from hemlock import settings

settings['password'] = '<my-secret-password>'
```

Hemlock will encrypt your password with the [werkzeug password hash utility](https://werkzeug.palletsprojects.com/en/1.0.x/utils/).

**Note.** Be sure not to have your password set in a public code repository while your application is in production.

## Cross-site request forgery (CSRF) protection

Hemlock uses [flask download button](https://dsbowen.github.io/flask-download-btn/) to protect your data from CSRF attacks. This package employs a standard CSRF prevention technique; it stores a strongly random temporary CSRF authentication token in your browser's session, then authenticates the token when you issue a request to download your data.