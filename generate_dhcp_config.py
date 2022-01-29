#!/usr/bin/env python
import getpass
import subprocess
import sys

from datetime import datetime
from phpipam_client import PhpIpamClient

from classes import DHCPDError, GeneratorError, IPAMObject
from dhcp_config_template import DHCPTemplate
from helpers import get_args


class DHCPDConfigGen:
    def __init__(
        self, endpoint, username, passwd, app_id, original_cf, backup_cf, new_cf
    ):
        self.username = username
        self.password = passwd
        self.endpoint = endpoint
        self.app_id = app_id
        self.client = PhpIpamClient(
            url=self.endpoint,
            app_id=self.app_id,
            username=self.username,
            password=self.password,
        )
        self.original_cf = original_cf
        self.backup_cf = backup_cf
        self.cf = new_cf

    def get_subnets(self):
        return self.client.get("/subnets/")

    def _get_associated_vlan(self, vlan_id):
        vlan = self.client.get(f"/vlan/{vlan_id}/")
        return vlan

    def _get_subnet_dhcp_ranges(self):
        subnets = self.get_subnets()
        dhcp_list = []
        for subnet in subnets:
            subnet_info = IPAMObject(**subnet)
            try:
                dhcp_range = subnet_info.dhcp_range
            except AttributeError:
                raise GeneratorError(
                    f"'{subnet_info.desc}' subnet is missing static_percentage value"
                )
            vlan = self._get_associated_vlan(subnet_info.vlanId)
            if dhcp_range:
                subnet_info.update({"vlan_info": vlan})
                dhcp_list.append(subnet_info)
        return dhcp_list

    def _dhcp_config_generator(self):
        print("Getting subnet DHCP data.")
        ranges = self._get_subnet_dhcp_ranges()
        print("Got subnet DHCP data. Generating config.")
        config = DHCPTemplate(ranges)
        print("Config generated.")
        return config

    def _backup_config(self):
        if self.original_cf is None:
            original_cf = "/etc/dhcp/dhcpd.conf"
        if self.backup_cf is None:
            today = str(datetime.now().date())
            backup_cf = f"/etc/dhcp/{today}_dhcp.conf.bak"
        try:
            print("Backing up original config.")
            with open(original_cf, "r") as orig_file:
                old_conf = orig_file.read()

            with open(backup_cf, "w+") as backup_file:
                backup_file.write(old_conf)
            print("Original config backed up.")
        except FileNotFoundError:
            return
        except PermissionError:
            subprocess.call(["sudo", "python3", *sys.argv])
        return

    def _restart_dhcpd(self, cf):
        print("Restarting dhcpd.")
        runcmd = subprocess.Popen(
            ["systemctl", "restart", "dhcpd", "-cf", cf],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = runcmd.communicate()
        returncode = runcmd.returncode
        if returncode == 0:
            print("dhcpd restarted successfully.")
        else:
            print("Error restarting dhcpd.")
        return (returncode, stdout, stderr)

    def create_config(self):
        self._backup_config()
        config = self._dhcp_config_generator()
        if self.cf is None:
            cf = "/etc/dhcp/dhcpd.conf"
        try:
            print("Writing config to file.")
            with open(cf, "w+") as file:
                file.write(config)
            print("Config written to file.")
        except PermissionError:
            subprocess.call(["sudo", "python3", *sys.argv])

        rc, stdout, stderr = self._restart_dhcpd(cf)
        if rc == 0:
            return cf
        else:
            raise DHCPDError(stderr)


def main():
    args = get_args()
    password = args.password
    if not args.password:
        password = getpass.getpass()
    run = DHCPDConfigGen(
        args.endpoint,
        args.username,
        password,
        args.app_id,
        args.original_cf,
        args.backup_cf,
        args.cf,
    )
    result = run.create_config()
    if result:
        return f"Success! File located in {result}"
    else:
        raise GeneratorError("Failure in generating the DHCP configuration file!")


if __name__ == "__main__":
    print(main())
