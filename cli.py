from jnpr.junos import Device

dev = Device(host='11.11.11.11', user='root', password='Juniper', gather_facts=False)

dev.open()

print dev.cli("show version", warning=False)

dev.close()
