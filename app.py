"""
Flask proxy to forward filtered out and formatted Github webhook events to the HoloViz Discord.
"""

import os

import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

TAGONLY_URL = os.getenv('HOLOVIZ_DISCORD_TAGONLY_WEBHOOK')
if not TAGONLY_URL:
    raise KeyError('Missing env var HOLOVIZ_DISCORD_TAGONLY_WEBHOOK')


@app.get('/')
def root():
    return 'Up and running'


@app.get('/health')
def health_check():
    return  jsonify({"status": "ok"}), 200


@app.post('/tagonly')
def tagonly():
    gh_event = request.headers.get('X-GitHub-Event')
    if gh_event == 'ping':
        return jsonify({
            'status': 'ignored',
            'message': 'Github ping successful',
        }), 200
    elif gh_event != 'create':
        return jsonify({
            'status': 'ignored',
            'message': f'Only "X-GitHub-Event: create" is supported, not {gh_event!r}',
        }), 200
    payload = request.get_json()
    ref_type = payload.get('ref_type', None)
    if ref_type != 'tag':
        return jsonify({
            'status': 'ignored',
            'message': f'Only "tag" event is supported, not {ref_type!r}',
        }), 200
    headers =  {
        'Content-Type': 'application/json',
        'charset': 'utf-8',
        # We must set X-GitHub-Event for Discord to render the message
        'X-GitHub-Event': 'create',
    }
    resp = requests.post(TAGONLY_URL+'/github', headers=headers, json=payload)
    if not resp.ok:
        return jsonify({
            'status': 'error',
            'message': f'Post request to the Discord webhook failed with code ({resp.status_code}) {resp.text}',
        }), 500
    return jsonify({
        'status': 'success',
        'message': 'Webhook event processed and forwarded successfully',
    }), 200


# @app.post('/failure_scheduled_run')
# def failure_scheduled_run():
#     gh_event = request.headers.get('X-GitHub-Event')
#     if gh_event == 'ping':
#         return 'Github ping successful', 200
#     elif gh_event != 'workflow_run':
#         return f'Only "X-GitHub-Event: workflow_run" is supported, not {gh_event!r}', 400
#     payload = request.get_json()
#     action = payload.get('action', None)
#     event = payload.get('workflow_run', {}).get('event', None)
#     conclusion = payload.get('workflow_run', {}).get('conclusion', None)
#     if not (event == 'schedule' and action == 'completed' and conclusion == 'failure'):
#         return f'Only accepting schedule workflow runs that completed with failure', 400
#     headers =  {
#         'Content-Type': 'application/json',
#         'charset': 'utf-8',
#         # We must set X-GitHub-Event for Discord to render the message
#         'X-GitHub-Event': 'workflow_run',
#     }
#     resp = requests.post(TAGONLY_URL+'/github', headers=headers, json=payload)
#     if not resp.ok:
#         return f'Post request to the Discord webhook failed with code ({resp.status_code}) {resp.text}', 500
#     return 'Success'
