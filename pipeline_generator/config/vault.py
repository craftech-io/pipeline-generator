VAULT_AUTH_METHODS = {
    'jwt': {
        'command': 'export VAULT_TOKEN="$(vault write -field=token auth/jwt/login role=<vault_role> '
                   'jwt=$CI_JOB_JWT)"'
    },
    'userpass': {
        'command': 'vault login -method=userpass username=${VAULT_USERNAME} password=${VAULT_PASSWORD}'
    }
}
