# Ansible Role: `redis`

[![CI](https://github.com/shaneholloman/ansible-role-redis/actions/workflows/ci.yml/badge.svg)](https://github.com/shaneholloman/ansible-role-redis/actions/workflows/ci.yml)

Installs [Redis](http://redis.io/) on Linux.

## Requirements

On RedHat-based distributions, requires the EPEL repository (you can simply add the role `shaneholloman.epel` to install ensure EPEL is available).

## Role Variables

```yml
redis_enablerepo: epel
```

(Used only on RHEL/CentOS) The repository to use for Redis installation.

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
redis_port: 6379
redis_bind_interface: 127.0.0.1
```

Port and interface on which Redis will listen. Set the interface to `0.0.0.0` to listen on all interfaces.

```yml
redis_unixsocket: ''
```

If set, Redis will also listen on a local Unix socket.

```yml
redis_timeout: 300
```

Close a connection after a client is idle `N` seconds. Set to `0` to disable timeout.

```yml
redis_loglevel: "notice"
redis_logfile: /var/log/redis/redis-server.log
```

Log level and log location (valid levels are `debug`, `verbose`, `notice`, and `warning`).

```yml
redis_databases: 16
```

The number of Redis databases.

```yml
# Set to an empty set to disable persistence (saving the DB to disk).
redis_save:
  - 900 1
  - 300 10
  - 60 10000
```

Snapshotting configuration; setting values in this list will save the database to disk if the given number of seconds (e.g. `900`) and the given number of write operations (e.g. `1`) have occurred.

```yml
redis_rdbcompression: "yes"
redis_dbfilename: dump.rdb
redis_dbdir: /var/lib/redis
```

Database compression and location configuration.

```yml
    redis_maxmemory: 0
```

Limit memory usage to the specified amount of bytes. Leave at 0 for unlimited.

```yml
redis_maxmemory_policy: "noeviction"
```

The method to use to keep memory usage below the limit, if specified. See [Using Redis as an LRU cache](http://redis.io/topics/lru-cache).

```yml
redis_maxmemory_samples: 5
```

Number of samples to use to approximate LRU. See [Using Redis as an LRU cache](http://redis.io/topics/lru-cache).

```yml
redis_appendonly: "no"
```

The appendonly option, if enabled, affords better data durability guarantees, at the cost of slightly slower performance.

```yml
redis_appendfsync: "everysec"
```

Valid values are `always` (slower, safest), `everysec` (happy medium), or `no` (let the filesystem flush data when it wants, most risky).

```yml
# Add extra include files for local configuration/overrides.
redis_includes: []
```

Add extra include file paths to this list to include more/localized Redis configuration.

The redis package name for installation via the system package manager. Defaults to `redis-server` on Debian and `redis` on RHEL.

```yml
redis_package_name: "redis-server"
```

(Default for RHEL shown) The redis package name for installation via the system package manager. Defaults to `redis-server` on Debian and `redis` on RHEL.

```yml
redis_requirepass: ""
```

Set a password to require authentication to Redis. You can generate a strong password using `echo "my_password_here" | sha256sum`.

```yml
redis_disabled_commands: []
```

For extra security, you can disable certain Redis commands (this is especially important if Redis is publicly accessible). For example:

```yml
redis_disabled_commands:
  - FLUSHDB
  - FLUSHALL
  - KEYS
  - PEXPIRE
  - DEL
  - CONFIG
  - SHUTDOWN
```

```yml
redis_extra_config: |-
  # Extra redis configuration lines can be added here.
```

Extra Redis configuration lines that will be appended to the end of the `redis.conf` file.

## Dependencies

None.

## Example Playbook

```yml
- hosts: all
  roles:
    - role: shaneholloman.redis
```

## License

Unlicense

## Author Information

This role was created in 2023
