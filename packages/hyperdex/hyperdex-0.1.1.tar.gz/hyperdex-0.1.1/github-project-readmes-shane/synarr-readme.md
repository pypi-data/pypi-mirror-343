# synarr

[![superlint](https://github.com/shaneholloman/synarr/actions/workflows/superlint.yml/badge.svg)](https://github.com/shaneholloman/synarr/actions/workflows/superlint.yml) [![powershell check](https://github.com/shaneholloman/synarr/actions/workflows/powershell.yml/badge.svg)](https://github.com/shaneholloman/synarr/actions/workflows/powershell.yml)

Is a set of docker compose templates for synology nas, (compatible with synology's operating system DSM v7.*)

This collection of docker-compose's is incidentally used for [trash-guides](https://trash-guides.info/).

TODO:

- [ ] create how to and what to expect sections
- [ ] refactor  compose templates to use linuxserver.io registry
- [ ] share how we use recyclarr to set media profiles etc

## Use

1. Pull script from GitHub

    ```sh
    curl -sL https://raw.githubusercontent.com/shaneholloman/synarr/main/script/synarr-installer.sh > ~/synarr-installer.sh
    ```

2. Run script

    ```sh
    sudo bash ~/synarr-installer.sh
    ```

3. Follow the prompts
