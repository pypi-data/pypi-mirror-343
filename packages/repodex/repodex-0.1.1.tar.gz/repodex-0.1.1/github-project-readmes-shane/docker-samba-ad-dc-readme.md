# samba-ad-dc

[![release alma](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-alma.yml/badge.svg)](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-alma.yml) [![release debian](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-debian.yml/badge.svg)](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-debian.yml) [![release rocky](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-rocky.yml/badge.svg)](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-rocky.yml) [![release ubuntu](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-ubuntu.yml/badge.svg)](https://github.com/shaneholloman/docker-samba-ad-dc/actions/workflows/release-ubuntu.yml)

Samba Active Directory Domain Controller Docker Image - still dev stage - don't use in production yet

If you run the docker-compose file:

```sh
docker-compose -f docker-compose-dc1.yml up -d
```

You can test the DC like this:

But before you do you need to make sure that the docker context is correct for the host you are running on. For example, and by the way I haven't got a full handle why this is yet:

```sh
docker context ls
NAME                TYPE                DESCRIPTION                               DOCKER ENDPOINT                                    KUBERNETES ENDPOINT   ORCHESTRATOR
default             moby                Current DOCKER_HOST based configuration   unix:///var/run/docker.sock
desktop-linux *     moby                Docker Desktop                            unix:///home/shadmin/.docker/desktop/docker.sock
```

```sh
docker context use default
default
Current context is now "default"
```

- Or pick the context that works for you. Just FYI, I usually pick `desktop-linux` BUT, for some reason, it doesn't work for this container. I'm still trying to figure out why.  So I choose `default` as above, then all is well.

```sh
docker exec dc1 samba-tool domain level show
```

```sh --results=verbatim
Domain and forest function level for domain 'DC=yoyo,DC=io'

Forest function level: (Windows) 2008 R2
Domain function level: (Windows) 2008 R2
Lowest function level of a DC: (Windows) 2008 R2
```

```sh
docker inspect dc1
```

```sh
docker logs dc1
```

```sh
docker exec dc1 samba-tool user list
```

```sh --results=verbatim
Guest
Administrator
krbtgt
```

```sh
docker exec dc1 samba-tool dns query localhost yoyo.io dc1 A --username=administrator --password=Passw0rd
```

```sh --results=verbatim
WARNING: Using passwords on command line is insecure. Installing the setproctitle python module will hide these from shortly after program start.
  Name=, Records=1, Children=0
    A: 20.0.0.253 (flags=f0, serial=1, ttl=900)
```

```sh
docker exec dc1 samba-tool user create yoda Passw0rd
```

```sh --results=verbatim
User 'yoda' added successfully
```

```sh
docker exec dc1 samba-tool user list
```

```sh --results=verbatim
Guest
Administrator
krbtgt
yoda
```

```sh
docker exec dc1 samba-tool dns query localhost yoyo.io dc1 A --username=yoda --password=Passw0rd
```

```sh --results=verbatim
WARNING: Using passwords on command line is insecure. Installing the setproctitle python module will hide these from shortly after program start.
  Name=, Records=1, Children=0
    A: 20.0.0.253 (flags=f0, serial=1, ttl=900)
```

1. Provision a new domain

    ```sh
    docker run -d --privileged \
      --restart=unless-stopped --network=host \
      -e REALM='YOYO.IO' \
      -e DOMAIN='YOYO' \
      -e ADMIN_PASS='Passw0rd' \
      -e DNS_FORWARDER='1.1.1.1' \
      -v dc1-samba:/usr/local/samba \
      --name dc1 --hostname DC1 shaneholloman/samba-ad-dc-ubuntu:latest
    ```

2. Show logs and run additional tests. The reason this works is because the script `./sbin/samba-tests` was pushed to the container during then build process.

    ```sh
    docker logs dc1 -f
    docker exec dc1 samba-tests
    ```

3. For external access, update the `/etc/resolv.conf` and `/etc/hosts` from your host, replacing `host_ip`

    ```sh
    nano /etc/resolv.conf
    ```

    ```ini
    search yoyo.io
    nameserver host_ip
    ```

    ```sh
    nano /etc/hosts
    ```

    ```ini
    127.0.0.1       localhost
    host_ip       DC1.yoyo.io     DC1
    ```

4. For multiple dc testing (no external access)

    ```sh
    git clone --single-branch https://github.com/shaneholloman/docker-samba-ad-dc
    cd docker-samba-ad-dc
    docker compose build
    docker compose up -d
    docker compose logs -f
    for dc in dc{1,2,3,4}; do docker compose exec $dc samba-tests; done
    ```

Links:

- [Setup](https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller)
- [Dependencies](https://wiki.samba.org/index.php/Package_Dependencies_Required_to_Build_Samba)
- [Ports](https://wiki.samba.org/index.php/Samba_AD_DC_Port_Usage)
