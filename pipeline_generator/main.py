import click

from pipeline_generator.libs.ci_path_lib import get_template_dict
from pipeline_generator.libs.ci_render import render_ci_template

GIT_PROVIDER_DICT = get_template_dict()


@click.command()
@click.version_option()
@click.option('--image-registry', '-i', 'image_registry', type=str, required=True, help='Registry for default image')
@click.option('--provider', '-p', 'git_provider', type=click.Choice(GIT_PROVIDER_DICT.keys()), required=True,
              help='Git provider, i.e: gitlab ')
@click.option('--out', '-o', 'out_filename', type=str, default='', help='Output file name')
@click.option('--extra-know-host', '-e', 'extra_known_hosts', multiple=True,
              help='Host that will be added to ~/.ssh/known_hosts. i.e: gitlab.com')
@click.option('--branch', '-b', 'branch_name', type=str, default='master', help='Default branch name')
@click.option('--enable-vault-envs', 'enable_vault_envs', is_flag=True,
              help='Enable vault to download environment variables')
@click.option('--vault-role', 'vault_role', type=str, default='terraform-pipeline', help='Vault role name')
@click.option('--vault-base-path', 'vault_base_path', type=str, default='terraform', help='Vault base path')
def generate_pipeline(image_registry, out_filename, extra_known_hosts, git_provider, branch_name, enable_vault_envs,
                      vault_role, vault_base_path):
    ci_template_rendered = render_ci_template(
        GIT_PROVIDER_DICT.get(git_provider),
        image_registry=image_registry,
        extra_known_hosts=extra_known_hosts,
        branch_name=branch_name,
        enable_vault_envs=enable_vault_envs,
        vault_role=vault_role,
        vault_base_path=vault_base_path
    )
    if out_filename:
        try:
            with open(out_filename, 'w') as f:
                print(ci_template_rendered, file=f)
        except IOError as err:
            print(f"The file {out_filename} could not be opened: ", err)
            exit(1)
    else:
        print(ci_template_rendered)


if __name__ == '__main__':
    generate_pipeline()
