# Ansible Role: `composer`

[![CI](https://github.com/shaneholloman/ansible-role-composer/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-composer/actions/workflows/ci.yml)

Installs Composer, the PHP Dependency Manager, on any Linux or UNIX system.

## Requirements

  - `php` (version 5.4+) should be installed and working (you can use the `shaneholloman.php` role to install).
  - `git` should be installed and working (you can use the `shaneholloman.git` role to install).

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
composer_path: /usr/local/bin/composer
```

The path where composer will be installed and available to your system. Should be in your user's `$PATH` so you can run commands simply with `composer` instead of the full path.

```yml
composer_keep_updated: false
```

Set this to `true` to update Composer to the latest release every time the playbook is run.

```yml
composer_home_path: '~/.composer'
composer_home_owner: root
composer_home_group: root
```

The `COMPOSER_HOME` path and directory ownership; this is the directory where global packages will be installed.

```yml
composer_version: ''
```

You can install a specific release of Composer, e.g. `composer_version: '1.0.0-alpha11'`. If left empty the latest development version will be installed. Note that `composer_keep_updated` will override this variable, as it will always install the latest development version.

```yml
composer_version_branch: '--2'
```

You can choose which major branch of composer you wish to use. Default is `--2`. Note that `composer_keep_updated` will update the latest version available for this branch.

```yml
composer_global_packages: []
```

A list of packages to install globally (using `composer global require`). If you want to install any packages globally, add a list item with a dictionary with the `name` of the package and a `release`, e.g. `- { name: phpunit/phpunit, release: "4.7.*" }`. The 'release' is optional, and defaults to `@stable`.

```yml
composer_add_to_path: true
```

If `true`, and if there are any configured `composer_global_packages`, the `vendor/bin` directory inside `composer_home_path` will be added to the system's default `$PATH` (for all users).

```yml
composer_project_path: /path/to/project
```

Path to a composer project.

```yml
composer_add_project_to_path: false
```

If `true`, and if you have configured a `composer_project_path`, the `vendor/bin` directory inside `composer_project_path` will be added to the system's default `$PATH` (for all users).

```yml
composer_github_oauth_token: ''
```

GitHub OAuth token, used to avoid GitHub API rate limiting errors when building and rebuilding applications using Composer. Follow GitHub's directions to [Create a personal access token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) if you run into these rate limit errors.

```yml
php_executable: php
```

The executable name or full path to the PHP executable. This is defaulted to `php` if you don't override the variable.

### Staying on Composer 1

While projects are upgrading to support Composer 2, it may be helpful to run Composer 1 instead. To do that, set these variables:

```yml
composer_version_branch: ''
composer_version: '1.10.12'
```

## Dependencies

None (but make sure you've installed PHP; the `shaneholloman.php` role is recommended).

## Example Playbook

```yml
- hosts: servers
  roles:
    - shaneholloman.composer
```

After the playbook runs, `composer` will be placed in `/usr/local/bin/composer` (this location is configurable), and will be accessible via normal system accounts.

## License

Unlicense

## Author Information

This role was created in 2023
