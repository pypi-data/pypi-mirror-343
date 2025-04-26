# Ansible Role: `phps`

[![CI](https://github.com/shaneholloman/ansible-role-phps/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-phps/actions/workflows/ci.yml)

Allows different PHP versions to be installed when using the `shaneholloman.php` role (or a similar role). This role is a mechanism for switching PHP versions.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
php_version: '8.2'
```

The PHP version to be installed. Any [currently-supported PHP major version](http://php.net/supported-versions.php) is a valid option (e.g. `7.4`, `8.0`, `8.1`, or `8.2`).

    php_versions_install_recommends: false

(For Debian OSes only) Whether to install recommended packages. This is set to `no` by default because setting it to `yes` often leads to multiple PHP versions being installed (thus making a bit of a mess) when using repos like Ondrej's PHP PPA for Ubuntu.

## Dependencies

  - shaneholloman.php is a soft dependency as the `php_version` variable is required to be set.
  - shaneholloman.remi, if you're using CentOS or a Red Hat derivative.

## Example Playbook

```yml
- hosts: webservers
  become: true

  vars:
    php_version: '8.2'

  roles:
    - name: shaneholloman.remi
      when: ansible_os_family == 'RedHat'
    - shaneholloman.phps
    - shaneholloman.php
```

## License

Unlicense

## Author Information

This role was created 2023
