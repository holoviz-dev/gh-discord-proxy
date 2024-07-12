# Github webhooks proxy for Discord

HoloViz developers benefit from having Github events reflected in Discord. Discord has some integration with Github webhooks, however, they are sometimes too noisy or some events are just not supported by Discord. This repository contains a small Flask app that acts as a proxy for Github webhooks, filtering them out and formatting them.

## Set up

### Github

Create a webhook on Github at the organization level, selecting for instance the *Branch or tag creation* event. The *payload URL* is the endpoint you want to hit on the proxy, i.e. `https://gh-discord-proxy.holoviz-demo.anaconda.com/<endpoint>`. Set the *Content type* to *application/json* and disable *SSL verification*.

### Discord

On a channel settings go to the *Integrations* tab and create a new webhook. Copy its URL, it should look something like `https://discord.com/api/webhooks/{some_id}/{some_id}`.

### App

Now deploy the app by setting the environment variabled `HOLOVIZ_DISCORD_<endpoint>_WEBHOOK` to the webhook you just created.

## Endpoints

### `/tagonly`

The Github webhook *Branch or tag creation* is too noisy, we only want *tag* events to be sent to `releases` Discord channel and this is what this endpoing does. `HOLOVIZ_DISCORD_TAGONLY_WEBHOOK` must be set.
