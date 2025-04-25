# Ansible Role: `nfs`

[![CI](https://github.com/shaneholloman/ansible-role-nfs/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-nfs/actions/workflows/ci.yml)

Installs NFS utilities on RedHat/CentOS or Debian/Ubuntu.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
nfs_exports: []
```

A list of exports which will be placed in the `/etc/exports` file. See Ubuntu's simple [Network File System (NFS)](https://ubuntu.com/server/docs/service-nfs) guide for more info and examples. (Simple example: `nfs_exports: [ "/home/public    *(rw,sync,no_root_squash)" ]`).

```yml
nfs_rpcbind_state: started
nfs_rpcbind_enabled: true
```

(RedHat/CentOS/Fedora only) The state of the `rpcbind` service, and whether it should be enabled at system boot.

## Dependencies

None.

## Example Playbook

```yml
- hosts: db-servers
  roles:
    - { role: shaneholloman.nfs }
```

## License

Unlicense

## Author Information

This role was created in 2023
