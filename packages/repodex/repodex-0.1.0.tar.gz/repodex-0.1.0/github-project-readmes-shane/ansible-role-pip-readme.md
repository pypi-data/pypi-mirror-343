# Ansible Role: `pip`

[![CI](https://github.com/shaneholloman/ansible-role-pip/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-pip/actions/workflows/ci.yml)

An Ansible Role that installs [Pip](https://pip.pypa.io) on Linux.

## Requirements

On RedHat/CentOS, you may need to have EPEL installed before running this role. You can use the `shaneholloman.epel` role if you need a simple way to ensure it's installed.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
  pip_package: python3-pip
```

The name of the package to install to get `pip` on the system. For older systems that don't have Python 3 available, you can set this to `python-pip`.

```yml
pip_executable: pip3
```

The role will try to autodetect the pip executable based on the `pip_package` (e.g. `pip` for Python 2 and `pip3` for Python 3). You can also override this explicitly, e.g. `pip_executable: pip3.6`.

```yml
pip_install_packages: []
```

A list of packages to install with pip. Examples below:

```yml
pip_install_packages:
  # Specify names and versions.
  - name: docker
    version: "1.2.3"
  - name: awscli
    version: "1.11.91"

  # Or specify bare packages to get the latest release.
  - docker
  - awscli

  # Or uninstall a package.
  - name: docker
    state: absent

  # Or update a package to the latest version.
  - name: docker
    state: latest

  # Or force a reinstall.
  - name: docker
    state: forcereinstall

  # Or install a package in a particular virtualenv.
  - name: docker
    virtualenv: /my_app/venv

  # Or pass through any extra arguments.
  - name: my_special_package_from_my_special_repo
    extra_args: --extra-index-url https://my-domain/pypi/pypi-master/simple
```

## Dependencies

None.

## Example Playbook

```yml
- hosts: all

  vars:
    pip_install_packages:
      - name: docker
      - name: awscli

  roles:
    - shaneholloman.pip
```

## License

Unlicense

## Author Information

This role was created in 2023
