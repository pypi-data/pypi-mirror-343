# Ansible Role: `containerd`

[![CI](https://github.com/shaneholloman/ansible-role-containerd/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-containerd/actions/workflows/ci.yml)

An Ansible Role that installs [containerd](https://containerd.io) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
containerd_package: containerd.io
containerd_package_state: present
```

Package name and state controls.

```yml
containerd_service_state: started
containerd_service_enabled: true
```

Service controls. You can install containerd but not have it running or enabled on boot by changing these defaults.

```yml
containerd_config_default_write: true
```

Write containerd defaults to the containerd config.toml file.

```yml
containerd_config_cgroup_driver_systemd: false
```

Set systemd as cgroup driver in config.toml. Only valid with `containerd_config_default_write: true`

```yml
docker_apt_release_channel: stable
docker_apt_arch: '{{ (ansible_architecture == "aarch64") | ternary("arm64", "amd64") }}'
docker_apt_repository: "deb [arch={{ docker_apt_arch }}] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker_apt_release_channel }}"
docker_apt_ignore_key_error: true
docker_apt_gpg_key: https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg
```

Apt installation parameters, useful if you want to switch from the stable channel releases, or install on a different CPU architecture (e.g. `arm64`).

```yml
docker_yum_repo_url: https://download.docker.com/linux/{{ (ansible_distribution == "Fedora") | ternary("fedora","centos") }}/docker-ce.repo
docker_yum_repo_enable_nightly: '0'
docker_yum_gpg_key: https://download.docker.com/linux/centos/gpg
```

Yum/DNF installation parameters, useful if you want to switch from the stable repository.

## Dependencies

None.

## Example Playbook

```yml
- hosts: all
  roles:
    - shaneholloman.containerd
```

## License

Unlicense

## Author Information

This role was created in 2023
