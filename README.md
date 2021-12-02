# pipeline-generator

This is a Python CLI that generates *.gitlab-ci.yml* or *bitbucket-pipelines.yml* output  in **infrastructure-live** repositories.


## Prerequisites

* Python 3.6 or higher
* pip
* docker(optional)

## Install package 

You can make a virtual environment:

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
$ pipeline-generator
```
The default image for ci/cd pipeline is `"craftech/ci-tools:iac-tools-deaefcf14545724c6e4851c2841a9ae502f00380"` and 
the default provider is `gitlab` (generates a .gitlab-ci.yml output style).

To set a custom image use the `-i` flag:
```shell
$ pipeline-generator -i mycustomimage:v1.0.0
```

By default, the branch name is **master**. You can change it with e `-b` or `--branch` option, e.g:

```shell
$ pipeline-generator -b main
```

If you need add a host to ~/.ssh/known_hosts file, use the `-e` option:
```shell
$ pipeline-generator  -e gitlab.foo.com
```

The --extra-know-host option can be passed multiple times:
```shell
$ pipeline-generator  -e gitlab.foo.com -e gitlab.bar.com
```

Instead of printing the result to the screen, you can save it to a file with de `-o` or `--out` option:
```shell
$ pipeline-generator  -e gitlab.foo.com -e gitlab.bar.com -o .gitlab-ci.yml
```

### Download environment variables from Vault

#### Requirements

Image requirements(already installed in the default image):
* vault-cli
* jq

CI/CD environment variables:
* **VAULT_ADDR**: Address of the Vault server expressed as a URL and port (https://www.vaultproject.io/docs/commands#vault_addr)

CI/CD environment variables for `userpass` authentication method:
* **VAULT_USERNAME** 
* **VAULT_PASSWORD**

#### How to use it

You can use the flag `--enable-vault-envs` to download environment variables from a Vault server

```shell
$ pipeline-generator --enable-vault-envs
```
By default, it uses the `jwt` authentication method with a role named `terraform-pipeline` and a root path named `terraform`.

JWT authentication method reference:
https://docs.gitlab.com/ee/ci/examples/authenticating-with-hashicorp-vault/
https://www.vaultproject.io/docs/auth/jwt#jwt-authentication

To change the role name use the flag `--vault-role`:

```shell
$ pipeline-generator --enable-vault-envs --vault-role=mycustomrole
```

To change the Vault root path use the flag `--vault-base-path`:

```shell
$ pipeline-generator --enable-vault-envs --vault-base-path=gitlab-ci-secrets
```

If you want to the `userpass` auth method instead `jwt`, use the flag `--vault-auth-method`:

```shell
$ pipeline-generator --enable-vault-envs --vault-auth-method=userpass
```

### Avoid GitLab variable inheritance conflicts

Sometimes there are variables defined at group level like `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY`. These variables 
have more precedence than job variables, check de documentation:

https://docs.gitlab.com/ee/ci/variables/#cicd-variable-precedence

To avoid this situation you can use the `--export-aws-vars` to export `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables
in the script section. eg:

```yaml
.dev_terragrunt_plan_template:
  stage: terragrunt-plan
  variables:
    AWS_ACCESS_KEY_ID: "$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$DEV_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  script:
    - export AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
    - terragrunt plan -input=false -refresh=true -out=$TERRAPLAN_NAME

.dev_terragrunt_apply_template:
  stage: terragrunt-apply
  variables:
    AWS_ACCESS_KEY_ID: "$DEV_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$DEV_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - export AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
    - terragrunt apply -input=false -refresh=false -auto-approve=true $TERRAPLAN_NAME

.mgt_terragrunt_plan_template:
  stage: terragrunt-plan
  variables:
    AWS_ACCESS_KEY_ID: "$MGT_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$MGT_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  script:
    - export AWS_ACCESS_KEY_ID=$MGT_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$MGT_AWS_SECRET_ACCESS_KEY
    - terragrunt plan -input=false -refresh=true -out=$TERRAPLAN_NAME

.mgt_terragrunt_apply_template:
  stage: terragrunt-apply
  variables:
    AWS_ACCESS_KEY_ID: "$MGT_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$MGT_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - export AWS_ACCESS_KEY_ID=$MGT_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$MGT_AWS_SECRET_ACCESS_KEY
    - terragrunt apply -input=false -refresh=false -auto-approve=true $TERRAPLAN_NAME

.prd_terragrunt_plan_template:
  stage: terragrunt-plan
  variables:
    AWS_ACCESS_KEY_ID: "$PRD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$PRD_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  script:
    - export AWS_ACCESS_KEY_ID=$PRD_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$PRD_AWS_SECRET_ACCESS_KEY
    - terragrunt plan -input=false -refresh=true -out=$TERRAPLAN_NAME

.prd_terragrunt_apply_template:
  stage: terragrunt-apply
  variables:
    AWS_ACCESS_KEY_ID: "$PRD_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: "$PRD_AWS_SECRET_ACCESS_KEY"
  extends: .terragrunt_template
  when: manual
  script:
    - export AWS_ACCESS_KEY_ID=$PRD_AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$PRD_AWS_SECRET_ACCESS_KEY
    - terragrunt apply -input=false -refresh=false -auto-approve=true $TERRAPLAN_NAME
```

### CLI help

``` shell
$ pipeline-generator --help
Usage: pipeline-generator [OPTIONS]

Options:
  --version                       Show the version and exit.
  -i, --image-registry TEXT       Registry for default image
  -p, --provider [gitlab]         Git provider, i.e: gitlab  [default: gitlab]
  -o, --out TEXT                  Output file name
  -e, --extra-know-host TEXT      Host that will be added to
                                  ~/.ssh/known_hosts. i.e: gitlab.com
  -b, --branch TEXT               Default branch name  [default: master]
  --export-aws-vars               Export AWS variables in the script section
  --enable-vault-envs             Enable vault to download environment
                                  variables
  --vault-role TEXT               Vault role name  [default: terraform-
                                  pipeline]
  --vault-base-path TEXT          Vault base path  [default: terraform]
  --vault-auth-method [jwt|userpass]
                                  Vault auth method  [default: jwt]
  --help                          Show this message and exit.
```

## Executing with Docker

To build the docker image run the following command in the root of the repository:

```shell
$ docker build -t pipeline-generator:latest .
```

Or use the Docker Hub image(https://hub.docker.com/r/craftech/pipeline-generator/tags)
```shell
docker pull craftech/pipeline-generator:latest
```

Run a temporary container to execute de CLI:

```shell
$ docker run --rm -it --name pipeline-generator --env LOCAL_USER_ID=$(id -u) -v `pwd`:`pwd` -w `pwd` pipeline-generator:latest /bin/sh
```


## Examples


```shell
$ cd ~/repos/foo/infra/infrastructure-live-foo
$ pipeline-generator -i "craftech/ci-tools:iac-tools-deaefcf14545724c6e4851c2841a9ae502f00380" -e gitlab.foo.com -p gitlab

stages:
  - terragrunt plan
  - terragrunt apply

default:
  image: craftech/ci-tools:iac-tools-deaefcf14545724c6e4851c2841a9ae502f00380

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