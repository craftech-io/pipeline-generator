import jinja2

from pipeline_generator.libs.ci_path_lib import get_ci_path_list, get_account_list, get_path_list


def render_ci_template(template_path: str, **kwargs):
    """
    Renders the CI/CD pipeline template
    :param template_path: jinja template path
    :param kwargs: keyword arguments to pass to the render function
    :return: Jinja rendered template
    """
    path_list = get_path_list('./', '**/terragrunt.hcl')
    with open(template_path, 'r') as f:
        ci_template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)
    kwargs['ci_path_list'] = get_ci_path_list(path_list)
    kwargs['account_list'] = get_account_list(kwargs['ci_path_list'])
    return ci_template.render(kwargs)
