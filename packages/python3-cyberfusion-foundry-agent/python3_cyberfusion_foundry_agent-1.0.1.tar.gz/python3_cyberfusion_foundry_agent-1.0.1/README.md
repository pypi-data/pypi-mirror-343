# python3-cyberfusion-foundry-agent

VM/device agent for Foundry.

The agent provides the following modules, passing information to Foundry:

* Heartbeat
    * Sends a heartbeat to Foundry on boot

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-foundry-agent

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

Find an example configuration in `etc/foundry-agent.yml`.

To use the agent, the UUID must be configured.
It is used to uniquely identify VMs/devices in Foundry, and therefore must be retrieved from Foundry.

# Usage

## CLI

Manually run modules using the `foundry-agent` CLI.

## Automatic

Specific modules may run automatically on Debian using systemd.
