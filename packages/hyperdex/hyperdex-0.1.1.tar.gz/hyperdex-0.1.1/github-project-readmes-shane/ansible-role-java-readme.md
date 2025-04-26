# Ansible Role: `java`

[![CI](https://github.com/shaneholloman/ansible-role-java/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-java/actions/workflows/ci.yml)

Installs Java for RedHat/CentOS and Debian/Ubuntu linux servers.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values:

```yml
# The defaults provided by this role are specific to each distribution.
java_packages:
  - java-1.8.0-openjdk
```

Set the version/development kit of Java to install, along with any other necessary Java packages. Some other options include are included in the distribution-specific files in this role's 'defaults' folder.

```yml
java_home: ""
```

If set, the role will set the global environment variable `JAVA_HOME` to this value.

## Dependencies

None.

## Example Playbook (using default package)

```yml
- hosts: servers
  roles:
    - role: shaneholloman.java
      become: yes
```

## Example Playbook (using custom package)

For RHEL / CentOS:

```yml
- hosts: server
  roles:
    - role: shaneholloman.java
      when: "ansible_os_family == 'RedHat'"
      java_packages:
        - java-1.8.0-openjdk
```

For Ubuntu < 20.04:

```yml
- hosts: server
  tasks:
    - name: installing repo for Java 8 in Ubuntu
      ansible.builtin.apt_repository: repo='ppa:openjdk-r/ppa'

- hosts: server
  roles:
    - role: shaneholloman.java
      when: "ansible_os_family == 'Debian'"
      java_packages:
        - openjdk-8-jdk
```

## License

Unlicense

## Author Information

This role was created in 2023
