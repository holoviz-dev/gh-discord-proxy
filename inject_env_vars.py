import os

from yaml import dump, safe_load, YAMLError


PROJECT = 'anaconda-project.yml'
ENV_VARS = [
    'HOLOVIZ_DISCORD_TAGONLY_WEBHOOK',
]

with open(PROJECT, 'r') as f:
    try:
        spec = safe_load(f)
    except YAMLError as e:
        raise YAMLError('invalid file content') from e

variables = {}
for env_var in ENV_VARS:
    val = os.getenv(env_var)
    if val:
        variables[env_var] = val

spec['VARIABLES'] = variables

with open('data.yaml', 'w') as f:
    dump(spec, f)
