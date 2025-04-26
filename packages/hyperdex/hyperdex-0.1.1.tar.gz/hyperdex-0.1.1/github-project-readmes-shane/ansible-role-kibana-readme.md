# Ansible Role: `kibana`

[![CI](https://github.com/shaneholloman/ansible-role-kibana/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-kibana/actions/workflows/ci.yml)

An Ansible Role that installs Kibana on RedHat/CentOS or Debian/Ubuntu.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
kibana_version: "7.x"
```

The version of kibana to install.

```yml
kibana_package: kibana
kibana_package_state: present
```

The specific package to be installed. You can specify a version of the package using the correct syntax for your platform and package manager by changing the package name. You can also control the package state (e.g. `present`, `absent`, or `latest`).

```yml
kibana_service_state: started
kibana_service_enabled: true
```

Controls whether the `kibana` service is started and enabled on system boot.

```yml
kibana_config_template: kibana.yml.j2
kibana_config_file_path: /etc/kibana/kibana.yml
```

The template to use for the Kibana config file, and the path to which the config file will be written.

```yml
kibana_server_port: 5601
kibana_server_host: "0.0.0.0"
```

The FQDN or IP address and port Kibana should use.

```yml
kibana_elasticsearch_url: "http://localhost:9200"
```

The URL (including port) over which Kibana will connect to Elasticsearch.

```yml
kibana_elasticsearch_username: ""
kibana_elasticsearch_password: ""
```

If Elasticsearch is protected by HTTP basic authentication, set the username and password so Kibana can connect.

## Dependencies

None.

## Example Playbook

```yml
- hosts: kibana
  roles:
    - shaneholloman.kibana
```

## License

Unlicense

## Author Information

This role was created in 2023
