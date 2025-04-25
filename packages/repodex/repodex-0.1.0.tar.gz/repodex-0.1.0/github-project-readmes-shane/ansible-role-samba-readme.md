# Ansible Role: `samba`

[![CI](https://github.com/shaneholloman/ansible-role-samba/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-samba/actions/workflows/ci.yml)

Installs Samba client and server for RHEL/CentOS and Debian Families.

## Requirements

Samba requires ports 137, 138, 139, 445 to be open to function properly. For easy firewall configuration, you can use the `shaneholloman.firewall` role.

## Role Variables

None.

## Dependencies

None.

## Example Playbook

```yml
- hosts: servers
  roles:
    - shaneholloman.samba
```

## License

Unlicense

## Author Information

This role was created in 2023
