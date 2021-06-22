import re

TERRAGRUNT_RE_LIST = [
    re.compile(r'^(?P<account>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/(?P<env>[\w-]+)/([\w.-]+/)*?terragrunt\.hcl$')
]

IGNORE_RE_LIST = [
    re.compile(r'^([\w.-]+/)+\.terragrunt-cache/([\w.-]+/)+terragrunt\.hcl$')
]