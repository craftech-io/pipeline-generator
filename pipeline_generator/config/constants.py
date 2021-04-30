import re

TERRAGRUNT_RE_LIST = [
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/([\w.-]+/)*?(?P<env>prd|mgt|dev|qa\d?|stg)/([\w.-]+/)*?'
               r'terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$')
]
