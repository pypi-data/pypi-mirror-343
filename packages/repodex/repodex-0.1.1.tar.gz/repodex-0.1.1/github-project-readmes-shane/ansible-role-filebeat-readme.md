# Ansible Role: `filebeat`

[![CI](https://github.com/shaneholloman/ansible-role-filebeat/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-filebeat/actions/workflows/ci.yml)

An Ansible Role that installs [Filebeat](https://www.elastic.co/products/beats/filebeat) on RedHat/CentOS or Debian/Ubuntu.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
filebeat_version: 7.x
```

Controls the major version of Filebeat which is installed.

```yml
filebeat_package: filebeat
filebeat_package_state: present
```

The specific package to be installed. You can specify a version of the package using the correct syntax for your platform and package manager by changing the package name. You can also control the package state (e.g. present, absent, or latest).

```yml
filebeat_create_config: true
```

Whether to create the Filebeat configuration file and handle the copying of SSL key and cert for filebeat. If you prefer to create a configuration file yourself you can set this to `false`.

```yml
filebeat_inputs:
    - type: log
    paths:
        - "/var/log/*.log"
```

Inputs that will be listed in the `inputs` section of the Filebeat configuration. Read through the [Filebeat Inputs configuration guide](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-filebeat-options.html) for more options.

```yml
filebeat_output_elasticsearch_enabled: false
filebeat_output_elasticsearch_hosts:
    - "localhost:9200"
```

Whether to enable Elasticsearch output, and which hosts to send output to.

```yml
filebeat_output_elasticsearch_auth:
    username: "admin"
    password: "S3CR3eeet"
```

```yml
# or, only for version 8+
filebeat_output_elasticsearch_auth:
    api_key: "xa-123a-f3ea012d-aaae1"
```

Configures the authentication for the elasticsearch output. Note that api_key and user/pass are mutually exclusive, and api_key is only available from version 8.

```yml
filebeat_output_logstash_enabled: true
filebeat_output_logstash_hosts:
    - "localhost:5000"
```

Whether to enable Logstash output, and which hosts to send output to.

```yml
filebeat_enable_logging: false
filebeat_log_level: warning
filebeat_log_dir: /var/log/filebeat
filebeat_log_filename: filebeat.log
```

Filebeat logging.

```yml
filebeat_ssl_certs_dir: /etc/pki/logstash
filebeat_ssl_private_dir: "{{ filebeat_ssl_certs_dir }}"
```

The path where certificates and keyfiles will be stored.

```yml
filebeat_ssl_ca_file: ""
filebeat_ssl_certificate_file: ""
filebeat_ssl_key_file: ""
```

Local paths to the SSL certificate and key files.

```yml
filebeat_ssl_copy_file: true
```

Wether to copy certificate and key into the `filebeat_ssl_dir`, or use existing ones.

For utmost security, you should use your own valid certificate and keyfile, and update the `filebeat_ssl_*` variables in your playbook to use your certificate.

To generate a self-signed certificate/key pair, you can use use the command:

```sh
sudo openssl req -x509 -batch -nodes -days 3650 -newkey rsa:2048 -keyout filebeat.key -out filebeat.crt
```

Note that filebeat and logstash may not work correctly with self-signed certificates unless you also have the full chain of trust (including the Certificate Authority for your self-signed cert) added on your server. See: <https://github.com/elastic/logstash/issues/4926#issuecomment-203936891>

```yml
filebeat_ssl_insecure: "false"
```

Set this to `"true"` to allow the use of self-signed certificates (when a CA isn't available).

### Overriding the filebeat template

If you can't customize via variables because an option isn't exposed, you can override the template used to generate the filebeat configuration.

```yml
filebeat_template: "filebeat.yml.j2"
```

You can either copy and modify the provided template, or you can, for example, point to a template file in your playbook directory that will be used instead of the managed template.

```yml
filebeat_template: "{{ playbook_dir }}/templates/filebeat.yml.j2"
```

## Dependencies

This role depends on the following Galaxy roles:

- `shaneholloman.java`
- `shaneholloman.elasticsearch`
- `shaneholloman.logstash`
- `shaneholloman.filebeat`

Please ensure these roles are installed before running this role. You can install roles using the `ansible-galaxy` command:

```sh
ansible-galaxy install shaneholloman.java
ansible-galaxy install shaneholloman.elasticsearch
ansible-galaxy install shaneholloman.logstash
ansible-galaxy install shaneholloman.filebeat
```

## Example Playbook

```yml
- hosts: logs

- name: Set the java_packages variable (Debian/Ubuntu).
  set_fact:
    java_packages:
- openjdk-8-jdk
  when: ansible_os_family == 'Debian'

  roles:
    - shaneholloman.java
    - shaneholloman.elasticsearch
    - shaneholloman.logstash
    - shaneholloman.filebeat
```

## License

Unlicense

## Author Information

This role was created in 2023
