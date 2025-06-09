# mininetrepo device 1:

set interfaces ge-0/0/0 unit 0 family inet address 10.10.10.1/24

set interfaces ge-0/0/1 unit 0 family inet address 10.10.10.2/24

set interfaces ge-0/0/2 unit 0 family ethernet-switching vlan members VOICE

set interfaces me0 unit 0 family inet address 100.100.100.1/30

set interfaces vlan unit 10 family inet address 192.168.1.1/24

set protocols ospf area 0.0.0.10 interface ge-0/0/0.0 metric 5

set protocols ospf area 0.0.0.10 interface ge-0/0/1.0 metric 10

set protocols ospf area 0.0.0.10 interface vlan.10

set vlans VOICE vlan-id 10

set vlans VOICE l3-interface vlan.10

Device 2:

set interfaces ge-0/0/0 unit 0 family inet address 10.10.10.8/24

set interfaces ge-0/0/1 unit 0 family inet address 10.10.10.7/24

set interfaces ge-0/0/2 unit 0 family ethernet-switching vlan members DATA

set interfaces vlan unit 20 family inet address 172.16.1.1/24

set protocols ospf area 0.0.0.10 interface ge-0/0/0.0 metric 5

set protocols ospf area 0.0.0.10 interface ge-0/0/1.0 metric 10

set protocols ospf area 0.0.0.10 interface vlan.20

set vlans DATA vlan-id 20

set vlans DATA l3-interface vlan.20
