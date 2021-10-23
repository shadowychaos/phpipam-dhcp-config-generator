#!/usr/bin/python3
from inspect import cleandoc

from jinja2 import Template
from helpers import get_dns_servers


def DHCPTemplate(subnets):
    tmp = Template(
        cleandoc(
            """
            {% raw -%}
            #
            # DHCP Server Configuration file.
            #   see /usr/share/doc/dhcp-server/dhcpd.conf.example
            #   see dhcpd.conf(5) man page
            #

            one-lease-per-client true;
            log-facility local7;
            ddns-update-style interim;

            # Declare DHCP Server
            authoritative;

            # The default DHCP lease time
            default-lease-time 7200;

            # Set the maximum lease time
            max-lease-time 7200;

            {%- endraw %}
            {% for subnet in subnets %}
            # {{ subnet.description }} VLAN - VLAN {{ subnet.vlan_info.number }}
            subnet {{ subnet.subnet_id }} netmask {{ subnet.netmask }} {
                # Range of IP addresses to allocate
                pool {
                # Range calulated with 6 reserved IPs and a {{ subnet.static_percentage }}% static reservation.
                    range {{ subnet.dhcp_range.first_ip }} {{ subnet.dhcp_range.last_ip }};
                }

                # Provide broadcast address
                option broadcast-address {{ subnet.broadcast }};

                # Set default gateway
                option routers {{ subnet.first_ip }};

                {%- if subnet.get("domain_name") %}
                option domain-name "{{ subnet.domain_name }}";
                {%- endif %}
                {%- if subnet.get("nameservers") %}
                {%- set nameservers = ", ".join(subnet.nameservers.namesrv1.split(";")) %}
                option domain-name-servers {{ nameservers }};
                {%- else %}
                option domain-name-servers {{ dns_servers }};
                {% endif %}

                {%- if subnet.get("next_server") %}
                next-server {{ subnet.next_server }};
                option bootfile-name "{{ subnet.bootfile_name }}";
                {%- endif %}
            }
            {% endfor %}

            include "/etc/dhcp/dhcpd-reservations.include";
            """
        )
    )
    return tmp.render(
        subnets=subnets,
        dns_servers=get_dns_servers(),
    )
