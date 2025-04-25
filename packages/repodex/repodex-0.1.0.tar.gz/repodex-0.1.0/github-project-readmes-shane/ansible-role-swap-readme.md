# Ansible Role: `swap`

[![CI](https://github.com/shaneholloman/ansible-role-swap/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-swap/actions/workflows/ci.yml)

An Ansible Role that configures swap space on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
swap_file_path: /swapfile
```

The location of the swap file on the server.

```yml
swap_file_size_mb: '512'
```

How large (in mebibytes) to make the swap file.

```yml
swap_swappiness: '60'
```

The `vm.swappiness` value to be configured in sysconfig.

```yml
swap_file_state: present
```

If you wish to _remove_ your swapfile, and disable swap, set this to `absent`. Generally you'd probably want to set this to `present`.

    swap_file_create_command: "dd if=/dev/zero of={{ swap_file_path }} bs=1M count={{ swap_file_size_mb }}"

The command used to create the swap file. You could switch to using `fallocate` to write the swap file more quickly, though there may be inconsistencies if not writing the file with `dd`.

## Dependencies

None.

## Example Playbook

```yml
- hosts: all
  vars:
    swap_file_size_mb: '1024'
  roles:
    - shaneholloman.swap
```

## License

Unlicense

## Author Information

This role was created in 2023
