import json
from collections import namedtuple
from collections.abc import MutableMapping

from IPy import IP


class DHCPDError(Exception):
    pass


class GeneratorError(Exception):
    pass


class IPAMObject(MutableMapping):
    def __init__(self, **kwargs):
        """
        Pass a dictionary from PHPIPAM to this class.
        Example:
        ipam_data = {
            'subnet': '10.0.3.0',
            'mask': 24,
            'custom_Static': 90,
        }
        net = IPAMObject(**ipam_data)

        Usage:
        netmask = net.netmask
        cidr = net.cidr
        broadcast_address = net.broadcast
        subnet_id = net.subnet_id
        first_ip = net.first_ip
        last_ip = net.last_ip
        dhcp_range = net.dhcp_range
        data_in_json = net.to_json()
        """
        self.store = dict()
        self.store.update(dict(**kwargs))

        # This is required as sometimes we aren't passing
        # an actual subnet, but a dict containing other items
        try:
            self.net = IP(f"{self.subnet}/{self.mask}")
        except AttributeError:
            pass

        new_dict = {}
        for k, v in self.store.items():
            if "custom_" in k:
                new_key = k.replace("custom_", "")
                new_dict[new_key] = v
            else:
                new_dict[k] = v

        self.store = new_dict

    def __getattr__(self, key):
        print(self.store)
        if key not in self.store:
            raise AttributeError(f'{__class__.__name__} has no attribute "{key}"')

        value = self.store[key]

        if isinstance(value, dict):
            value = IPAMObject(**value)

        if isinstance(value, list):
            new_value = []
            if len(value) > 1:
                for val in value:
                    if isinstance(val, dict):
                        new_value.append(IPAMObject(**val))
            elif len(value) == 1:
                new_value = IPAMObject(**value[0])

            if new_value:
                value = new_value

        return value

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        for ip in self.net:
            yield ip.strNormal()

    def __len__(self):
        return self.net.len()

    @property
    def netmask(self):
        return self.net.netmask().strNormal()

    @property
    def cidr(self):
        return str(self.net)

    @property
    def broadcast(self):
        return self.net.broadcast().strNormal()

    @property
    def subnet_id(self):
        return self.net.net().strNormal()

    @property
    def first_ip(self):
        return self.net[1].strNormal()

    @property
    def last_ip(self):
        return self.net[-2].strNormal()

    @property
    def dhcp_range(self):
        dhcp_tuple = namedtuple("DHCPRange", ["first_ip", "last_ip"])
        reserved_ips = 6
        static_integer = int(self.static_percentage)
        if static_integer == 100:
            return None
        static_cent = int(static_integer * self.net.len() / 100) + reserved_ips
        # +1 to account for the subnet address, :-1 to remove broadcast address
        dhcp_range = self.net[static_cent + 1:][:-1]
        return dhcp_tuple(dhcp_range[0].strNormal(), dhcp_range[-1].strNormal())

    def to_json(self):
        """
        Returns the original dictionary passed to this class in JSON format.
        """
        return json.dumps(self.store)
