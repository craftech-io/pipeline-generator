import re

TERRAGRUNT_RE_LIST = [
    re.compile(r'^(?P<account>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/_global/([\w.-]+/)*?terragrunt\.hcl$'),
    re.compile(r'^(?P<account>[\w-]+)/(?P<region>[\w-]+)/(?P<env>[\w-]+)/([\w.-]+/)*?terragrunt\.hcl$')
]

IGNORE_RE_LIST = [
    re.compile(r'^([\w.-]+/)+\.terragrunt-cache/([\w.-]+/)+terragrunt\.hcl$')
]

IMAGE_DEFAULT = 'craftech/ci-tools:iac-tools-deaefcf14545724c6e4851c2841a9ae502f00380'
