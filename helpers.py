import argparse
import dns.resolver


def get_args():
    parser = argparse.ArgumentParser(description="Generate DHCP configuration file.")
    parser.add_argument(
        "--username",
        "-u",
        action="store",
        dest="username",
        metavar="",
        required=True,
        help="Username to authenticate with to the IPAM server.",
    )
    parser.add_argument(
        "--password",
        "-p",
        action="store",
        dest="password",
        metavar="",
        help="Password to authenticate with to the IPAM server.",
    )
    parser.add_argument(
        "--original-cf",
        "-ocf",
        action="store",
        dest="original_cf",
        metavar="",
        default=None,
        help="Full file path of the original configuration file for dhcpd.",
    )
    parser.add_argument(
        "--backup-cf",
        "-bcf",
        action="store",
        dest="backup_cf",
        metavar="",
        default=None,
        help="Full file path of the newly created backup dhcpd config.",
    )
    parser.add_argument(
        "--configuration-file",
        "-cf",
        action="store",
        dest="cf",
        metavar="",
        default=None,
        help="Full file path of the new configuration file for dhcpd.",
    )
    parser.add_argument(
        "--endpoint",
        "-e",
        action="store",
        dest="endpoint",
        metavar="",
        required=True,
        help="Full URL of the PHPIPAM endpoint. e.g. https://ipam.example.com",
    )
    parser.add_argument(
        "--app-id",
        "-a",
        action="store",
        dest="app_id",
        metavar="",
        required=True,
        help="Application ID chosen during creation of application in PHPIPAM.",
    )
    return parser.parse_args()


def get_dns_servers():
    dns_servers = dns.resolver.Resolver()
    return ", ".join(dns_servers.nameservers)
