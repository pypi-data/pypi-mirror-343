from os import getenv, path
from yaml import safe_load

# environment
user_name = getenv('JIRA_USERNAME')
token = getenv('JIRA_TOKEN')
domain = getenv('JIRA_DOMAIN')
home_dir = getenv('HOME')

# static
ticket_excerpt_length = 60
powerjira_directory = f'{home_dir}/.sleepyconfig/powerjira'
powerjira_editor = 'vscode'

# init templates
templates = {
  'ticket.yml': '''# pj --help

#───TICKET───────────────────
reporter: jack
assignee: jill

init_status: to do # new, to do, in progress, done, backlog

project: sales # sales, marketing, frontend
priority: medium # low, medium, high (ignored if epic)
issue_type: task # task, epic
parent_epic: '' # leave empty for standalone task or epic


#───GIT──────────────────────
parent_branch: main
# ℹ️ naming convention must include <ticket_key>
branch_naming_convention: feature/<ticket_key>_<branch_suffix>
branch_name_params: # custom branch name parameters
  branch_suffix: implement_thing''',

  'summary.txt': '''This is the ticket's title, which jira calls the "summary"''',

  'description.txt': '''This is the ticket's description''',
}


#───CONFIG FILE──────────────
global_config_path = f'{home_dir}/.sleepyconfig/params.yml'
config_file_exists = path.exists(global_config_path)

def resolveValue(default:any, config_key:str) -> any:
  '''returns config value if exists, else default'''
  if not config_file_exists:
    return default
  with open(global_config_path, 'r') as f:
    raw_config = safe_load(f)
    if config_key not in raw_config:
      return default
    return raw_config[config_key]

## defaults
default_powerjira_table_style = 'rounded_outline'
default_shell = '/bin/zsh'
## config file
result_table_style = resolveValue(default_powerjira_table_style, 'pj_table_style')
powerjira_shell = resolveValue(default_shell, 'subprocess_shell')