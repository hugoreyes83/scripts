import re

show_route = '''
0.0.0.0/0          *[BGP/170] 23:37:40, localpref 100
                      AS path: 16509 I, validation-state: unverified
                    > to 100.65.62.8 via ae11.0
                      to 100.65.62.136 via ae12.0
                      to 100.65.63.8 via ae13.0
                      to 100.65.63.136 via ae14.0
                    [BGP/170] 23:37:28, localpref 100
                      AS path: 16509 I, validation-state: unverified
                    > to 100.65.62.136 via ae12.0
                    [BGP/170] 23:37:43, localpref 100
                      AS path: 16509 I, validation-state: unverified
                    > to 100.65.63.8 via ae13.0
                    [BGP/170] 23:37:44, localpref 100
                      AS path: 16509 I, validation-state: unverified
                    > to 100.65.63.136 via ae14.0
52.119.214.91/32   *[Direct/0] 2d 03:58:16
                    > via lo0.0
100.65.62.8/31     *[Direct/0] 2d 03:42:58
                    > via ae11.0
100.65.62.9/32     *[Local/0] 2d 03:58:17
                      Local via ae11.0
100.65.62.136/31   *[Direct/0] 2d 03:42:57
                    > via ae12.0
100.65.62.137/32   *[Local/0] 2d 03:58:17
                      Local via ae12.0
100.65.63.8/31     *[Direct/0] 2d 03:42:57
                    > via ae13.0
100.65.63.9/32     *[Local/0] 2d 03:58:17
                      Local via ae13.0
100.65.63.136/31   *[Direct/0] 2d 03:42:58
                    > via ae14.0
100.65.63.137/32   *[Local/0] 2d 03:58:17
                      Local via ae14.0
192.168.0.0/29     *[Direct/0] 2d 03:56:47
                    > via xe-0/0/0.0
192.168.0.1/32     *[Local/0] 2d 03:56:59
                      Local via xe-0/0/0.0
192.168.0.8/29     *[Direct/0] 2d 03:56:47
                    > via xe-0/0/1.0
192.168.0.9/32     *[Local/0] 2d 03:56:59
                      Local via xe-0/0/1.0
192.168.0.16/29    *[Direct/0] 2d 03:56:46
                    > via xe-0/0/2.0
192.168.0.17/32    *[Local/0] 2d 03:56:58
                      Local via xe-0/0/2.0
192.168.0.24/29    *[Direct/0] 2d 03:56:47
                    > via xe-0/0/3.0
192.168.0.25/32    *[Local/0] 2d 03:56:58
                      Local via xe-0/0/3.0
192.168.0.32/29    *[Direct/0] 2d 03:56:47
                    > via xe-0/0/4.0
192.168.0.33/32    *[Local/0] 2d 03:56:58
                      Local via xe-0/0/4.0
192.168.0.40/29    *[Direct/0] 2d 03:56:46
                    > via xe-0/0/5.0
192.168.0.41/32    *[Local/0] 2d 03:56:58
                      Local via xe-0/0/5.0
192.168.0.48/29    *[Direct/0] 2d 03:56:46
                    > via xe-0/0/6.0
192.168.0.49/32    *[Local/0] 2d 03:56:58
                      Local via xe-0/0/6.0
192.168.0.56/29    *[Direct/0] 2d 03:56:46
                    > via xe-0/0/7.0
'''

new_dict = {}
for i in show_route.splitlines():
    grab_prefix = re.search('\d+\.\d+\.\d+\.\d+\/\d+', i)
    grab_outgoing_interfaces = re.search('ae\d{2}|xe[\-\/\d\.]+|lo\d\.\d', i)
    if grab_prefix:
        new_dict[grab_prefix.group(0)] = set()
        current_prefix = grab_prefix.group(0)
    if grab_outgoing_interfaces:
            new_dict[current_prefix].add(grab_outgoing_interfaces.group(0))
for prefix in new_dict:
        for interface in new_dict[prefix]:
            print('{} is reachable via {}'.format(prefix,interface))
