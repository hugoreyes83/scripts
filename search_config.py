from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

def main():
config = "set snmp community asdfgh"
try:
    dev = Device(host='172.16.1.100', user='hugo', password='9jaguarxj11')
    dev.open()

finally:
    dev.close()

if __name__ == "__main__":
    main()
