# pipeline-generator

This is a Python CLI that geneartes a *.gitlab-ci.yml* in **infrastructure-live** resposioties.


## Prerequisites

* Python 3.6 or higher
* pip

## Install package 

You can make a varitualenv:

```shell
$ virtualenv venv
$ . venv/bin/activate
```
Another option can be:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

Install the package with pip:

```shell
$ pip install .
```

To install in editable mode("develop mode"):
```shell
$ pip install -e .
```


## Executing the CLI

After creating the virtualenv and installing the package you can run the CLI with the following command:

```shell
$ pipeline-generator -i "9594.dkr.ecr.us-east-2.amazonaws.com/cirunner:tf0.13.5"
```

If you need add a host to ~/.ssh/known_hosts file, use the `-e` option:
```shell
$ pipeline-generator -i "9594.dkr.ecr.us-east-2.amazonaws.com/cirunner:tf0.13.5" -e gitlab.foo.com
```


CLI help: 

```
$ pipeline-generator --help
Usage: pipeline-generator [OPTIONS]

Options:
  -i, --image-registry TEXT   Registry for default image  [required]
  -o, --out TEXT              Output file name
  -e, --extra-know-host TEXT  Host that will be added to ~/.ssh/known_hosts.
                              i.e: gitlab.com

  --help                      Show this message and exit.
```

## Examples


```shell
$ cd ~/repos/foo/infra/infrastructure-live-foo
$ pipeline-generator -i "9594.dkr.ecr.us-east-2.amazonaws.com/cirunner:tf0.13.5" -e gitlab.foo.com 

stages:
  - terragrunt plan
  - terragrunt apply
  - terragrunt destroy

default:
  image: 9594.dkr.ecr.us-east-2.amazonaws.com/cirunner:tf0.13.5

variables:
  PLAN_OUT_DIR: $CI_PROJECT_DIR/plan-outs

.terragrunt_template:
  before_script:
    - mkdir -p ~/.ssh
    - echo "$GITLAB_DEPLOY_KEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - eval $(ssh-agent -s)
    - ssh-add ~/.ssh/id_rsa
    - ssh-keyscan -H gitlab.foo.com >> ~/.ssh/known_hosts
    - ssh-keyscan -H github.com >> ~/.ssh/known_hosts
    - LOCATION=$(echo ${CI_JOB_NAME} | cut -d":" -f2)
    - cd ${LOCATION}


.dev_terragrunt_plan_template:
  stage: terragrunt plan
  variables:
    AWS_ACCESS_KEY_ID: "$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$DEV_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  script:
    - mkdir -p $PLAN_OUT_DIR/${CI_JOB_NAME}
    - terragrunt plan -input=false -refresh=true

.dev_terragrunt_apply_template:
  stage: terragrunt apply
  variables:
    AWS_ACCESS_KEY_ID: "$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$DEV_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - terragrunt apply -input=false -refresh=false -auto-approve=true

.dev_terragrunt_destroy_template:
  stage: terragrunt destroy
  variables:
    AWS_ACCESS_KEY_ID: "$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$DEV_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - terragrunt destroy -input=false -refresh=true -auto-approve=true

.prd_terragrunt_plan_template:
  stage: terragrunt plan
  variables:
    AWS_ACCESS_KEY_ID: "$PRD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$PRD_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  script:
    - mkdir -p $PLAN_OUT_DIR/${CI_JOB_NAME}
    - terragrunt plan -input=false -refresh=true

.prd_terragrunt_apply_template:
  stage: terragrunt apply
  variables:
    AWS_ACCESS_KEY_ID: "$PRD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$PRD_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - terragrunt apply -input=false -refresh=false -auto-approve=true

.prd_terragrunt_destroy_template:
  stage: terragrunt destroy
  variables:
    AWS_ACCESS_KEY_ID: "$PRD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$PRD_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - terragrunt destroy -input=false -refresh=true -auto-approve=true



terragrunt-plan:dev/_global/route53/dev.foo.com:
  extends: .dev_terragrunt_plan_template
  only:
    refs:
      - master
    changes:
      - dev/_global/route53/dev.foo.com/terragrunt.hcl

terragrunt-apply:dev/_global/route53/dev.foo.com:
  extends: .dev_terragrunt_apply_template
  only:
    refs:
      - master
    changes:
      - dev/_global/route53/dev.foo.com/terragrunt.hcl

terragrunt-destroy:dev/_global/route53/dev.foo.com:
  extends: .dev_terragrunt_destroy_template
  only:
    refs:
      - master
    changes:
      - dev/_global/route53/dev.foo.com/terragrunt.hcl

terragrunt-plan:dev/us-east-1/_global/vpc:
  extends: .dev_terragrunt_plan_template
  only:
    refs:
      - master
    changes:
      - dev/us-east-1/_global/vpc/terragrunt.hcl

terragrunt-apply:dev/us-east-1/_global/vpc:
  extends: .dev_terragrunt_apply_template
  only:
    refs:
      - master
    changes:
      - dev/us-east-1/_global/vpc/terragrunt.hcl

terragrunt-destroy:dev/us-east-1/_global/vpc:
  extends: .dev_terragrunt_destroy_template
  only:
    refs:
      - master
    changes:
      - dev/us-east-1/_global/vpc/terragrunt.hcl

terragrunt-plan:dev/us-east-1/_global/acm:
  extends: .dev_terragrunt_plan_template
  only:
    refs:
      - master
    changes:
      - dev/us-east-1/_global/acm/terragrunt.hcl

terragrunt-apply:dev/us-east-1/_global/acm:
  extends: .dev_terragrunt_apply_template
  only:
    refs:
      - master
    changes:
      - dev/us-east-1/_global/acm/terragrunt.hcl
```