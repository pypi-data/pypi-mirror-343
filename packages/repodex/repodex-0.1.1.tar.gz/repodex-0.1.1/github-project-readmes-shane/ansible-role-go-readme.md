# Ansible Role: `go`

[![CI](https://github.com/shaneholloman/ansible-role-go/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-go/actions/workflows/ci.yml)

An Ansible Role that installs Go (the language) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
go_version: "1.17.3"
go_platform: linux
go_arch: amd64
```

Version, platform, and architecture to use when downloading Go.

```yml
go_tarball: go{{ go_version }}.{{ go_platform }}-{{ go_arch }}.tar.gz
go_download_url: https://dl.google.com/go/{{ go_tarball }}
```

These two variables are used to build the download URL when installing Go.

```yml
go_checksum: '550f9845451c0c94be679faf116291e7807a8d78b43149f9506c1b15eb89008c'
```

SHA256 checksum of the Go download. If changing the version, platform, or architecture, you will also need to update this checksum, too.

## Dependencies

None.

## Example Playbook

```yml
- hosts: myserver
  roles:
    - { role: shaneholloman.go }
```

## License

Unlicense

## Author Information

This role was created in 2023
