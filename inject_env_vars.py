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
        print(f"Injecting variable {env_var}")
        variables[env_var] = val
    else:
        raise LookupError(f"Missing env var {env_var}")

spec['variables'] = variables

print("Overriding anaconda-project file.")

with open(PROJECT, 'w') as f:
    dump(spec, f)
