# Ansible Role: `packer`

[![CI](https://github.com/shaneholloman/ansible-role-packer/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-packer/actions/workflows/ci.yml)

Installs [Packer](https://www.packer.io), a Go-based image and box builder.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
packer_version: "1.0.0"
```

The Packer version to install.

```yml
packer_arch: "amd64"
```

The system architecture (e.g. `386` or `amd64`) to use.

```yml
packer_bin_path: /usr/local/bin
```

The location where the Packer binary will be installed (should be in system `$PATH`).

## Dependencies

None.

## Example Playbook

```yml
- hosts: servers
    roles:
    - shaneholloman.packer
```

## License

Unlicense

## Author Information

This role was created in 2023
