# Ansible Role: `helm`

[![CI](https://github.com/shaneholloman/ansible-role-helm/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-helm/actions/workflows/ci.yml)

This role installs the [Helm](https://helm.sh) binary on any supported host.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
helm_version: 'v3.2.1'
helm_platform: linux
helm_arch: amd64
```

Controls for the version of Helm to be installed. See [available Helm releases](https://github.com/helm/helm/releases/). You can upgrade or downgrade versions by changing the `helm_version`.

```yml
helm_repo_path: "https://get.helm.sh"
```

The path to the main Helm repo. Unless you need to override this for special reasons (e.g. running on servers without public Internet access), you should leave it as the default.

```yml
helm_bin_path: /usr/local/bin/helm
```

The location where the Helm binary will be installed.

## Dependencies

None.

## Example Playbook

```yml
- hosts: all
  roles:
    - role: shaneholloman.helm
```

## License

Unlicense

## Author Information

This role was created in 2023
