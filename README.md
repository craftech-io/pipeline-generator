# pipeline-generator

This is a Python CLI that geneartes *.gitlab-ci.yml* or *bitbucket-pipelines.yml* output  in **infrastructure-live** resposioties.


## Prerequisites

* Python 3.6 or higher
* pip
* docker(optional)

## Install package 

You can make a varitual environment:

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

After creating the virtualenv and installing the package you can run the CLI with the following commands located in the root of the infra-live repository:

```shell
$ pipeline-generator -i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c" -p gitlab
```

Where `-i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c"` is the default image for ci/cd pipeline and 
`-p gitlab` generates a .gitlab-ci.yml output style

If you need add a host to ~/.ssh/known_hosts file, use the `-e` option:
```shell
$ pipeline-generator -i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c" -p gitlab -e gitlab.foo.com
```

The --extra-know-host option can be passed multiple times:
```shell
$ pipeline-generator -i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c" -p gitlab -e gitlab.foo.com -e gitlab.bar.com
```

Instead of printing the result to the screen, you can save it to a file with de `-o` or `--out` option:
```shell
$ pipeline-generator -i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c" -p gitlab -e gitlab.foo.com -e gitlab.bar.com -o .gitlab-ci.yml
```

**Note**: the values in the options shown above are for example.

CLI help: 

```
$ pipeline-generator --help
Usage: pipeline-generator [OPTIONS]

Options:
  -i, --image-registry TEXT       Registry for default image  [required]
  -p, --provider [gitlab|bitbucket]
                                  Git provider, i.e: gitlab   [required]
  -o, --out TEXT                  Output file name
  -e, --extra-know-host TEXT      Host that will be added to
                                  ~/.ssh/known_hosts. i.e: gitlab.com

  --help                          Show this message and exit.
```

### Executing with Docker

To build the docker image run the following command in the root of the repository:

```shell
$ docker build -t pipeline-generator:latest .
```

Run a temporary container to execute de CLI:

```shell
$ docker run --rm -it --name pipeline-generator --env LOCAL_USER_ID=$(id -u) -v `pwd`:`pwd` -w `pwd` pipeline-generator:latest /bin/sh
```

## Examples


```shell
$ cd ~/repos/foo/infra/infrastructure-live-foo
$ pipeline-generator -i "craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c" -e gitlab.foo.com -p gitlab

stages:
  - terragrunt plan
  - terragrunt apply

default:
  image: craftech/ci-tools:iac-tools-6c09ee7d23dadcfcfe52159984b888ab6df6012c

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