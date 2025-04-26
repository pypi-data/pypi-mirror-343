# Radiator Maintenance

Used by IT Dept.

<!-- TOC -->

- [Radiator Maintenance](#radiator-maintenance)
  - [Installation](#installation)
  - [Explainers](#explainers)
    - [Radiator Health Check](#radiator-health-check)
    - [Radiator Move Logs](#radiator-move-logs)

<!-- /TOC -->

Radiator Health Check, Auto-Restart and log management Scripts

## Installation

> [!TIP]
> Usually done via ansible playbook, but feel free to do manually.

First, ssh to a radiator server and run the following commands:

Either sudo all commands or `sudo su` to root:

```sh
cd /opt
git pull <github-address> # you may need to setup your git user  or scp from your machine
sudo chown -R root:root radiator-maintenance
cd radiator-maintenance
```

Create log archive dir:

```sh
sudo mkdir -p /var/log/radiator/archive
```

Edit credentials:

```sh
sudo nano radiator-health-check.sh
```

- `RADIATOR_PASSWORD="redacted"`
- `RADIATOR_SECRET="redacted"`
  - See 1password for "redacted" values

```sh
sudo crontab -l # check if there are existing crons
sudo ./radiator-setup-crons.sh # this can add them for you
```

Thats it!

## Explainers

### Radiator Health Check

[Radiator Health Check](./radiator-health-check.sh)

This script performs a health check on the Radiator service. If the service is unresponsive, it automatically restarts the service and sends an email notification to the specified recipients. The script dynamically determines the server's hostname and IP address, making it portable across different servers without manual configuration

```sh
./radiator-health-check.sh
```

### Radiator Move Logs

[Radiator Move Logs](./radiator-move-logs.sh)

This script manages Radiator log files by performing three main tasks: moving logs older than 7 days to an archive directory, compressing uncompressed logs in the archive, and deleting compressed logs older than 180 days.

```sh
./radiator-move-logs.sh
```
