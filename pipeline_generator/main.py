import click

from pipeline_generator.libs.ci_path_lib import get_template_dict
from pipeline_generator.libs.ci_render import render_ci_template

GIT_PROVIDER_DICT = get_template_dict()


@click.command()
@click.option('--image-registry', '-i', 'image_registry', type=str, required=True, help='Registry for default image')
@click.option('--out', '-o', 'out_filename', type=str, default='', help='Output file name')
@click.option('--extra-know-host', '-e', 'extra_known_host', default='', type=str,
              help='Host that will be added to ~/.ssh/known_hosts. i.e: gitlab.com')
@click.option('--provider', '-p', 'git_provider', type=click.Choice(GIT_PROVIDER_DICT.keys()), required=True,
              help='Git provider, i.e: gitlab ')
def generate_pipeline(image_registry, out_filename, extra_known_host, git_provider):
    ci_template_rendered = render_ci_template(GIT_PROVIDER_DICT.get(git_provider), image_registry, extra_known_host)
    if out_filename:
        with open(out_filename, 'w') as f:
            print(ci_template_rendered, file=f)
    else:
        print(ci_template_rendered)


if __name__ == '__main__':
    generate_pipeline()
