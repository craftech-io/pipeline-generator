#!/bin/sh
# Ref.: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or fallback

USER_ID=${LOCAL_USER_ID:-9001}

echo "Starting with UID : $USER_ID"

if id craftech >/dev/null 2>&1; then
  echo ""
else
  adduser --shell /bin/sh --uid "${USER_ID}" --disabled-password --home /home/craftech craftech craftech
fi
export HOME=/home/craftech

su-exec craftech:"${USER_ID}" "$@"
