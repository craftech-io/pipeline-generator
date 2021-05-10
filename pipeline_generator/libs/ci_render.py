import jinja2

from pipeline_generator.libs.ci_path_lib import get_ci_path_list, get_account_list, get_path_list


def render_ci_template(template_path: str, image_registry: str, extra_known_hosts: str, disable_environments: bool):
    """
    Renders the CI/CD pipeline template
    :param template_path: jinja template path
    :param image_registry: registry for default image
    :param extra_known_hosts: host to add to ~/.ssh/known_hosts in the pipeline file
    :param disable_environments: If true, the pipeline doesn't include environment or deployment
    :return: Jinja rendered template
    """
    path_list = get_path_list('./', '**/terragrunt.hcl')
    with open(template_path) as f:
        ci_template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)
    ci_path_list = get_ci_path_list(path_list)
    account_list = get_account_list(ci_path_list)
    return ci_template.render(account_list=account_list, ci_path_list=ci_path_list, image_registry=image_registry,
                              extra_known_hosts=extra_known_hosts, disable_environments=disable_environments)
