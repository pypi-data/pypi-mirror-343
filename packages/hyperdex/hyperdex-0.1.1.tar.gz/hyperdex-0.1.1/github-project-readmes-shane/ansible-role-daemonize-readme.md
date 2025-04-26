# Ansible Role: `daemonize`

[![CI](https://github.com/shaneholloman/ansible-role-daemonize/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-daemonize/actions/workflows/ci.yml)

Installs [Daemonize](http://software.clapper.org/daemonize/), a tool for running commands as a Unix daemon.

## Requirements

Make sure you have `gcc` or other build tools installed (e.g. `yum install make automake gcc gcc-c++ kernel-devel` on RedHat, or `apt-get install build-essential` on Debian) prior to running this role, as it builds Daemonize from source.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
workspace: /root
```

The location where code will be downloaded and compiled.

```yml
daemonize_version: '1.7.5'
```

The daemonize release version to install.

    daemonize_install_path: "/usr"

The path where the compiled daemonize binary will be installed.

## Dependencies

None.

## Example Playbook

```yml
- hosts: servers
    roles:
    - { role: shaneholloman.daemonize }
```

## License

Unlicense

## Author Information

This role was created in 2023
