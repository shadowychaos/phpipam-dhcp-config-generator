# phpipam-dhcp-config-generator
This will generate a very basic DHCP config with use of PHPIPAM systems.

## Requirements
#### PHPIPAM
 - Custom Fields
   - domain_name (Optional)
   - static_percentage
   - **next_server (Optional)
   - **bootfile_name (Optional, but you cannot have a next_server with not bootfile_name)
   - A username/password and application with API access
   - PHPIPAM prettify links (https://phpipam.net/documents/prettified-links-with-mod_rewrite/)
#### DHCPD
 - **dhcpd-reservations.include (This file MUST exist and MUST be located in /etc/dhcp)

&nbsp; 

## Usage
To use this, simply execute the `generate_dhcp_config.py` script with the necessary arguments.

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
