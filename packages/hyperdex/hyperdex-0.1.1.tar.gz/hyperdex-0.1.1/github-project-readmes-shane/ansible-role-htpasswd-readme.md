# Ansible Role: `htpasswd`

[![CI](https://github.com/shaneholloman/ansible-role-htpasswd/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-htpasswd/actions/workflows/ci.yml)

An Ansible Role that installs `htpasswd` and allows easy configuration of `htpasswd` authentication files and credentials (used for HTTP basic authentication with webservers like Apache and Nginx) on Linux-based servers.

This role is in development. Please don't depend on this role unless you know what you're doing.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
htpasswd_nolog: true
```

Whether to show htpasswd credentials in Ansible's log output. Should remain `true` unless you're debugging something.

```yml
htpasswd_credentials:
  - path: /etc/nginx/passwdfile
    name: johndoe
    password: 'supersecure'
    owner: root
    group: www-data
    mode: 'u+rw,g+r'

  - path: /etc/apache2/passwdfile
    name: janedoe
    password: 'supersecure'
    owner: root
    group: www-data
    mode: 'u+rw,g+r'
```

A list of credentials to be generated (or removed) in the respective files defined by the `path` key for each dict. All parameters except `mode` are required (`mode` defaults to `'u+rw,g+r'` (`0640` in octal)).

```yml
htpasswd_required_packages:
  - apache2-utils
  - python3-passlib
```

(Debian defaults displayed). You can override the installed packages using this variable (e.g. for CentOS 7, you could change `python3-passlib` to `python-passlib`).

## Dependencies

None.

## Example Playbooks

### Apache Example

```yml
---
- hosts: apache-server

  vars:
    htpasswd_credentials:
      - path: /etc/apache-passwdfile
        name: johndoe
        password: 'supersecure'
        owner: root
        group: apache
        mode: 'u+rw,g+r'

    apache_remove_default_vhost: True
    apache_vhosts:
      - listen: "80"
        servername: "htpassword.test"
        documentroot: "/var/www/html"
        extra_parameters: |
              <Directory "/var/www/html">
                  AuthType Basic
                  AuthName "Apache with basic auth."
                  AuthUserFile /etc/apache-passwdfile
                  Require valid-user
              </Directory>

  pre_tasks:
    - name: Update apt cache.
      ansible.builtin.apt: update_cache=yes cache_valid_time=600
      when: ansible_os_family == 'Debian'

  roles:
    - shaneholloman.apache
    - shaneholloman.htpasswd
```

### Nginx Example

```yml
---
- hosts: nginx-server

  vars:
    htpasswd_credentials:
      - path: /etc/nginx/passwdfile
        name: johndoe
        password: 'supersecure'
        owner: root
        group: www-data
        mode: 'u+rw,g+r'

    nginx_remove_default_vhost: True
    nginx_vhosts:
      - listen: "80"
        server_name: "htpassword.test"
        root: "/var/www/html"
        index: "index.html index.html index.nginx-debian.html"
        filename: "htpassword.test.conf"
        extra_parameters: |
              location / {
                  auth_basic           "Nginx with basic auth.";
                  auth_basic_user_file /etc/nginx/passwdfile;
              }

  pre_tasks:
    - name: Update apt cache.
      ansible.builtin.apt: update_cache=yes cache_valid_time=600
      when: ansible_os_family == 'Debian'

  roles:
    - shaneholloman.nginx
    - shaneholloman.htpasswd
```

## License

Unlicense

## Author Information

This role was created in 2023
