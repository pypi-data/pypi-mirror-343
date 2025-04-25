# Ansible Role: `github`

[![CI](https://github.com/shaneholloman/ansible-role-github/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-github/actions/workflows/ci.yml)

Create users based on GitHub accounts.

This role will take a GitHub username and create a system account with the same username, and will add all the pubkeys associated with the GitHub account to the user's `authorized_keys`.

It's kind of a cheap way to do public key management for users on your system... but it works!

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
github_users: []
  # You can specify an object with 'name' (required) and 'groups' (optional):
  # - name: shaneholloman
  #   groups: www-data,sudo

  # Or you can specify a GitHub username directly:
  # - shaneholloman
```

A list of users to add to the server; the username will be the `name` (or the bare list item, if it's a string instead of an object). You can add the user to one or more groups (in addition to the `[username]` group) by adding them as a comma-separated list in `groups`.

```yml
github_users_absent: []
  # You can specify an object with 'name' (required):
  # - name: shaneholloman

  # Or you can specify a GitHub username directly:
  # - shaneholloman
```

A list of users who should _not_ be present on the server. The role will ensure these user accounts are removed.

```yml
github_users_authorized_keys_exclusive: true
```

Whether the users' `authorized_keys` files should exclusively contain keys from their GitHub account. This should normally be set to `true` if you are only allowing users to log in using keys available in their GitHub accounts.

```yml
github_url: https://github.com
```

By default, use public GitHub (i.e. <https://github.com>) as the source for users/keys. Override this to use a different GitHub instance/endpoint (e.g. GitHub Enterprise).

If you need to give the user the ability to self-manage their `authorized_keys` file, then you should set this to `no`, and it will only append new keys, but never remove any additional keys (e.g. old keys removed from their GitHub profile, or keys the end user added manually) from the file.

## Dependencies

None.

## Example Playbook

```yml
- hosts: servers

  vars:
    github_users:
      # You can specify the `name`:
      - name: shaneholloman
        groups: sudo,www-data
      - name: LukeSkywalker
        groups: sudo
      # Or if you don't need to override anything, you can specify the
      # GitHub username directly:
      - warpdeck

    github_users_absent:
      - johndoe
      - name: josh

  roles:
    - shaneholloman.github
```

If you want to make sure users' public keys are in sync, it is best to run the playbook on a cron, e.g. every 5 min, 10 min, or some other interval. That way you don't have to manually add new keys for users.

## License

Unlicense

## Author Information

This role was created in 2023
