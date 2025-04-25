# Ansible Role: `bootstrap`

[![CI](https://github.com/shaneholloman/ansible-role-bootstrap/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-bootstrap/actions/workflows/ci.yml)

Prepare your system to be managed by Ansible.

## Example Playbook

This example is taken from [`molecule/default/converge.yml`](https://github.com/shaneholloman/ansible-role-bootstrap/blob/main/molecule/default/converge.yml) and is tested on each push, pull request and release.

```yml
---
- name: Converge
  hosts: all
  # This role installs packages using the `raw` module and needs to connect as
  # `root`. (`sudo` is not available before bootstrapping.) All tasks in the
  # role have `become` set to `no`, so you can use either `no` or `yes` for
  # `become`, the role will not use become (so `sudo`) for any task.
  become: true  # `no` will also work.
  # This role installs python, gathering facts can't be done before `python` is
  # installed. This role runs the `setup` module, so facts will be available
  # after running the role.
  gather_facts: false

  roles:
    - role: shaneholloman.bootstrap
```

Also see a [full explanation and example](https://shaneholloman.com/how-to-use-these-roles.html) on how to use these roles.

## Role Variables

The default values for the variables are set in [`defaults/main.yml`](https://github.com/shaneholloman/ansible-role-bootstrap/blob/main/defaults/main.yml):

```yml
---
# defaults file for bootstrap

# Do you want to wait for the host to be available?
bootstrap_wait_for_host: false

# The number of seconds you want to wait during connection test before failing.
bootstrap_timeout: 3

# Tell the role to "become" or not.
bootstrap_become: true
```

## Requirements

- pip packages listed in [requirements.txt](https://github.com/shaneholloman/ansible-role-bootstrap/blob/main/requirements.txt).

## Compatibility

This role has been tested on these [container images](https://hub.docker.com/u/shaneholloman):

The minimum version of Ansible required is 2.12, tests have been done to:

- The previous version.
- The current version.
- The development version.

If you find issues, please register them in [GitHub](https://github.com/shaneholloman/ansible-role-bootstrap/issues)

## License

Unlicense

## Author Information

This role was created in 2023
