# phpipam-dhcp-config-generator
This will generate a very basic DHCP config with use of PHPIPAM systems.

## Requirements
#### PHPIPAM
 - [Custom Fields](https://phpipam.net/news/using-custom-fields-in-phpipam/)
   - domain_name (Optional)
   - static_percentage
   - **next_server (Optional)
   - **bootfile_name (Optional, but you cannot have a next_server with not bootfile_name)
   - A username/password and application with API access
   - [PHPIPAM prettify links](https://phpipam.net/documents/prettified-links-with-mod_rewrite/)

- All subnets must be linked to a VLAN!

#### DHCPD
 - **dhcpd-reservations.include (This file MUST exist and MUST be located in /etc/dhcp)

#### Operating System
This script assumes a CentOS/Fedora based system and all shell commands utilize CentOS syntax (e.g. yum, systemctl, etc.)

&nbsp; 

## Usage
To use this, simply execute the `generate_dhcp_config.py` script with the necessary arguments.
- `generate_dhcp_config.py` arguments
   - [-u|--username] **REQUIRED**
      - This is the username used to authenticate to PHPIPAM with.
   - [-p|--password]
      - This is the password associated with the username in PHPIPAM.
   - [-ocf|--original-cf]
      - This is the location of the original configuration file which will be backed up.
      - This will default to /etc/dhcp/dhcpd.conf
   - [-bcf|--backup-cf]
      - This is the location of where to back up the original configuration file. Must be a full file, not a path.
      - Default will point to a file in /etc/dhcp/ named $DATE_dhcp.conf.bak
   - [-cf|--configuration-file]
      - This is the location of the new configuration file. 
      - Keep in mind the DHCPD process should be looking for the configuration file in this location.
      - This will default to /etc/dhcp/dhcpd.conf
   - [-e|--endpoint] **REQUIRED**
      - This is the endpoint of the PHPIPAM server. (e.g. https://ipam.example.com)
   - [-a|--app-id] **REQUIRED**
      - This is the app ID to use with the username and password

&nbsp;

## Notes
Asterisks next to requirements indicate that this is easily changeable to suit your needs.
 - next_server
   - This is optional in PHPIPAM and you can specify this in the Jinja2 template manually.
 - bootfile_name
   - This is optional in PHPIPAM and you can specify this in the Jinja2 template manually.
 - dhcpd-reservations.include
   - This is optional and the include line can be removed from the Jinja2 template or the location can be changed manually.
   - You can also manually modify this file to fit your needs if you do intend to use it.

I mean, really, it's all optional and can be specified manually, but why not let PHPIPAM handle the load?

