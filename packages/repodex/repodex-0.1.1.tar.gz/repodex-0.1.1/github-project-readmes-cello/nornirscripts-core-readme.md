# nornirscripts-core

Nornir based scripts for CORE devices based on `m-chc01-nms01`

## Setup

- Repo should be replicated to `/opt/nornirscripts-core`

- Configuration / Credentials to services will need to be set in config.yaml, there is an example file in the root directory. These should be set individually per device and never exposed to github

- a virtual env will need to be created inside the `/opt/nornirscripts-core` directory and requirements.txt installed

```sh
cd /opt
sudo mkdir nornirscripts-core
cd /opt/nornirscripts-core
sudo git init
sudo git pull https://github.com/CelloCommunications/nornirscripts-core.git
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Scripts

- `checksavedxe`: This script is used for finding and emailing a list of XE Core devices without saved configurations

- `addconfigxe`: This is a user-editable script used for bulk configuration changes on cisco IOS-XE devices

- `addconfigxr`: This is a user-editable script used for bulk configuration changes on cisco IOS-XR devices
