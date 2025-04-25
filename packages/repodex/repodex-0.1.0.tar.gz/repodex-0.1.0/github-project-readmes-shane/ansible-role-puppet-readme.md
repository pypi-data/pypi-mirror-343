# Ansible Role: `puppet`

[![CI](https://github.com/shaneholloman/ansible-role-puppet/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-puppet/actions/workflows/ci.yml)

An Ansible Role that installs [Puppet](https://www.puppet.com) on Linux.

## Requirements

Requires Java 7 or later to be installed on the server (you can use the `shaneholloman.java` role to install Java if needed; see the test playbook in `tests/` for an example).

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
puppet_package: puppetserver
```

The package to be installed.

```yml
puppet_service: puppetserver
puppet_service_state: started
puppet_service_enabled: false
puppet_service_manage: false
```

The service that should be run on this server. By default, this role will not manage a Puppet service, and will not enable it at boot time.

```yml
puppet_bin_path: /opt/puppetlabs/bin
```

The path to all the Puppet Labs binaries (after the package is installed).

```yml
puppet_version: 7
```

The major version of Puppet to be installed.

```yml
# Used only for Debian/Ubuntu.
puppet_apt_deb: "https://apt.puppetlabs.com/puppet{{ puppet_version }}-release-{{ ansible_distribution_release }}.deb"
```

The .deb file for installation on Debian-based OSes.

```yml
# Used only for RedHat/CentOS.
puppet_yum_rpm: "https://yum.puppet.com/puppet{{ puppet_version }}-release-el-{{ ansible_distribution_major_version }}.noarch.rpm"
```

The .rpm file for installation on RedHat-based OSes.

## Dependencies

None.

## Example Playbook

```yml
- hosts: all
  roles:
    - shaneholloman.puppet
```

## License

Unlicense

## Author Information

This role was created in 2023
