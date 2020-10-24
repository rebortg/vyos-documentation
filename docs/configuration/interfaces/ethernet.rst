.. _ethernet-interface:

########
Ethernet
########

Configuration
#############

1.1.1.1

1.1.1.1

vyos



Address
-------

.. cfgcmd:: interfaces ethernet <interface> address <address | dhcp | dhcpv6>

   .. include:: ../../_include/interface-ip-ipv6-addr.txt

   Example:

   .. code-block:: none

     set interfaces ethernet eth0 address 192.0.2.1/24
     set interfaces ethernet eth0 address 192.0.2.2/24
     set interfaces ethernet eth0 address 2001:db8::ffff/64
     set interfaces ethernet eth0 address 2001:db8:100::ffff/64

.. cfgcmd:: interfaces ethernet <interface> ipv6 address autoconf

   .. include:: ../../_include/interface-ipv6-addr-autoconf.txt

.. cfgcmd:: interfaces ethernet <interface> ipv6 address eui64 <prefix>

   :abbr:`EUI-64 (64-Bit Extended Unique Identifier)` as specified in
   :rfc:`4291` allows a host to assign iteslf a unique 64-Bit IPv6 address.

   .. code-block:: none

     set interfaces ethernet eth0 ipv6 address eui64 2001:db8:beef::/64

Speed/Duplex
------------

.. cfgcmd:: interfaces ethernet <interface> duplex <auto | full | half>

   Configure physical interface duplex setting.

   * auto - interface duplex setting is auto-negotiated
   * full - always use full-duplex
   * half - always use half-duplex

   VyOS default will be `auto`.

.. cfgcmd:: interfaces ethernet <interface> speed <auto | 10 | 100 | 1000 | 2500 | 5000 | 10000 | 25000 | 40000 | 50000 | 100000>

   Configure physical interface speed setting.

   * auto - interface speed is auto-negotiated
   * 10 - 10 MBit/s
   * 100 - 100 MBit/s
   * 1000 - 1 GBit/s
   * 2500 - 2.5 GBit/s
   * 5000 - 5 GBit/s
   * 10000 - 10 GBit/s
   * 25000 - 25 GBit/s
   * 40000 - 40 GBit/s
   * 50000 - 50 GBit/s
   * 100000 - 100 GBit/s

   VyOS default will be `auto`.

Link Administration
-------------------

.. cfgcmd:: interfaces ethernet <interface> description <description>

   Assign given `<description>` to interface. Description will also be passed
   to SNMP monitoring systems.

.. cfgcmd:: interfaces ethernet <interface> disable

   Disable given `<interface>`. It will be placed in administratively down
   (``A/D``) state.

.. cfgcmd:: interfaces ethernet <interface> disable-flow-control

   Disable Ethernet flow control (pause frames).


.. cfgcmd:: interfaces ethernet <interface> mac <mac-address>

   Configure user defined :abbr:`MAC (Media Access Control)` address on given
   `<interface>`.

.. cfgcmd:: interfaces ethernet <interface> mtu <mtu>

   Configure :abbr:`MTU (Maximum Transmission Unit)` on given `<interface>`. It
   is the size (in bytes) of the largest ethernet frame sent on this link.

Operation
#########

.. opcmd:: show interfaces ethernet

   Show brief interface information.

   .. code-block:: none

     vyos@vyos:~$ show interfaces ethernet
     Codes: S - State, L - Link, u - Up, D - Down, A - Admin Down
     Interface        IP Address                        S/L  Description
     ---------        ----------                        ---  -----------
     eth0             172.18.201.10/24                  u/u  LAN
     eth1             172.18.202.11/24                  u/u  WAN
     eth2             -                                 u/D

.. opcmd:: show interfaces ethernet <interface>

   Show detailed information on given `<interface>`

   .. code-block:: none

     vyos@vyos:~$ show interfaces ethernet eth0
     eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
         link/ether 00:50:44:00:f5:c9 brd ff:ff:ff:ff:ff:ff
         inet6 fe80::250:44ff:fe00:f5c9/64 scope link
            valid_lft forever preferred_lft forever

         RX:  bytes    packets     errors    dropped    overrun      mcast
           56735451     179841          0          0          0     142380
         TX:  bytes    packets     errors    dropped    carrier collisions
            5601460      62595          0          0          0          0

.. opcmd:: show interfaces ethernet <interface> physical

   Show information about physical `<interface>`

   .. code-block:: none

     vyos@vyos:~$ show interfaces ethernet eth0 physical
     Settings for eth0:
             Supported ports: [ TP ]
             Supported link modes:   1000baseT/Full
                                     10000baseT/Full
             Supported pause frame use: No
             Supports auto-negotiation: No
             Supported FEC modes: Not reported
             Advertised link modes:  Not reported
             Advertised pause frame use: No
             Advertised auto-negotiation: No
             Advertised FEC modes: Not reported
             Speed: 10000Mb/s
             Duplex: Full
             Port: Twisted Pair
             PHYAD: 0
             Transceiver: internal
             Auto-negotiation: off
             MDI-X: Unknown
             Supports Wake-on: uag
             Wake-on: d
             Link detected: yes
     driver: vmxnet3
     version: 1.4.16.0-k-NAPI
     firmware-version:
     expansion-rom-version:
     bus-info: 0000:0b:00.0
     supports-statistics: yes
     supports-test: no
     supports-eeprom-access: no
     supports-register-dump: yes
     supports-priv-flags: no

.. opcmd:: show interfaces ethernet <interface> physical offload

   Show available offloading functions on given `<interface>`

   .. code-block:: none

     vyos@vyos:~$ show interfaces ethernet eth0 physical offload
     rx-checksumming               on
     tx-checksumming               on
     tx-checksum-ip-generic        on
     scatter-gather                off
     tx-scatter-gather             off
     tcp-segmentation-offload      off
     tx-tcp-segmentation           off
     tx-tcp-mangleid-segmentation  off
     tx-tcp6-segmentation          off
     udp-fragmentation-offload     off
     generic-segmentation-offload  off
     generic-receive-offload       off
     large-receive-offload         off
     rx-vlan-offload               on
     tx-vlan-offload               on
     ntuple-filters                off
     receive-hashing               on
     tx-gre-segmentation           on
     tx-gre-csum-segmentation      on
     tx-udp_tnl-segmentation       on
     tx-udp_tnl-csum-segmentation  on
     tx-gso-partial                on
     tx-nocache-copy               off
     rx-all                        off

.. opcmd:: show interfaces ethernet <interface> transceiver

   Show transceiver information from plugin modules, e.g SFP+, QSFP

   .. code-block:: none

     vyos@vyos:~$ show interfaces ethernet eth5 transceiver
        Identifier              : 0x03 (SFP)
        Extended identifier     : 0x04 (GBIC/SFP defined by 2-wire interface ID)
        Connector               : 0x07 (LC)
        Transceiver codes       : 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00
        Transceiver type        : Ethernet: 1000BASE-SX
        Encoding                : 0x01 (8B/10B)
        BR, Nominal             : 1300MBd
        Rate identifier         : 0x00 (unspecified)
        Length (SMF,km)         : 0km
        Length (SMF)            : 0m
        Length (50um)           : 550m
        Length (62.5um)         : 270m
        Length (Copper)         : 0m
        Length (OM3)            : 0m
        Laser wavelength        : 850nm
        Vendor name             : CISCO-FINISAR
        Vendor OUI              : 00:90:65
        Vendor PN               : FTRJ-8519-7D-CS4
        Vendor rev              : A
        Option values           : 0x00 0x1a
        Option                  : RX_LOS implemented
        Option                  : TX_FAULT implemented
        Option                  : TX_DISABLE implemented
        BR margin, max          : 0%
        BR margin, min          : 0%
        Vendor SN               : FNS092xxxxx
        Date code               : 0506xx


VLAN (802.1q)
-------------

IEEE 802.1q, often referred to as Dot1q, is the networking standard that
supports virtual LANs (VLANs) on an IEEE 802.3 Ethernet network. The
standard defines a system of VLAN tagging for Ethernet frames and the
accompanying procedures to be used by bridges and switches in handling
such frames. The standard also contains provisions for a quality-of-service
prioritization scheme commonly known as IEEE 802.1p and defines the Generic
Attribute Registration Protocol.

Portions of the network which are VLAN-aware (i.e., IEEE 802.1q conformant)
can include VLAN tags. When a frame enters the VLAN-aware portion of the
network, a tag is added to represent the VLAN membership. Each frame must
be distinguishable as being within exactly one VLAN. A frame in the
VLAN-aware portion of the network that does not contain a VLAN tag is
assumed to be flowing on the native VLAN.

The standard was developed by IEEE 802.1, a working group of the IEEE 802
standards committee, and continues to be actively revised. One of the
notable revisions is 802.1Q-2014 which incorporated IEEE 802.1aq (Shortest
Path Bridging) and much of the IEEE 802.1d standard.

802.1a VLAN interfaces are represented as virtual sub-interfaces in VyOS. The
term used for this is ``vif``. Configuration of a tagged sub-interface is
accomplished using the configuration command:
``set interfaces ethernet <name> vif <vlan-id>``

To assign a vif 100 using the VLAN 100 tag to physical interface eth1 use:

.. code-block:: none

  set interfaces ethernet eth1 vif 100 description 'VLAN 100'
  set interfaces ethernet eth1 vif 100 address '192.168.100.1/24'
  set interfaces ethernet eth1 vif 100 address '2001:db8:100::1/64'

Resulting in:

.. code-block:: none

  ethernet eth1 {
      address 192.168.100.1/24
      address 2001:db8:100::1/64
      description INSIDE
      duplex auto
      hw-id 00:53:29:44:3b:19
      smp_affinity auto
      speed auto
      vif 100 {
          address 192.168.100.1/24
          description "VLAN 100"
      }
  }

VLAN interfaces are shown as `<name>.<vlan-id>`, e.g. `eth1.100`:

.. code-block:: none

  vyos@vyos:~$ show interfaces
  Codes: S - State, L - Link, u - Up, D - Down, A - Admin Down
  Interface        IP Address                        S/L  Description
  ---------        ----------                        ---  -----------
  eth0             172.16.51.129/24                  u/u  OUTSIDE
  eth1             192.168.0.1/24                    u/u  INSIDE
  eth1.100         192.168.100.1/24                  u/u  VLAN 100
  lo               127.0.0.1/8                       u/u
                   ::1/128


.. _qinq-interface:

QinQ (802.1ad)
--------------

.. todo::

    improve

IEEE 802.1ad was an Ethernet networking standard informally known as QinQ as
an amendment to IEEE standard ref: vlan-interface. 802.1ad was incorporated
into the base 802.1q standard in 2011. The technique is also known as provider
bridging, Stacked VLANs, or simply QinQ or Q-in-Q. "Q-in-Q" can for supported
devices apply to C-tag stacking on C-tag (Ethernet Type = 0x8100).

The original 802.1q specification allows a single Virtual Local Area Network
(VLAN) header to be inserted into an Ethernet frame. QinQ allows multiple
VLAN tags to be inserted into a single frame, an essential capability for
implementing Metro Ethernet network topologies. Just as QinQ extends 802.1Q,
QinQ itself is extended by other Metro Ethernet protocols.

In a multiple VLAN header context, out of convenience the term "VLAN tag" or
just "tag" for short is often used in place of "802.1Q VLAN header". QinQ
allows multiple VLAN tags in an Ethernet frame; together these tags constitute
a tag stack. When used in the context of an Ethernet frame, a QinQ frame is a
frame that has 2 VLAN 802.1Q headers (double-tagged).

In VyOS the terms **vif-s** and **vif-c** stand for the ethertype tags that
are used:

The inner tag is the tag which is closest to the payload portion of the frame.
It is officially called C-TAG (customer tag, with ethertype 0x8100). The outer
tag is the one closer/closest to the Ethernet header, its name is S-TAG
(service tag with ethertype 0x88a8).

Configuration commands:

.. code-block:: none

  interfaces
      ethernet <eth[0-999]>
          address <ipv4>
          address <ipv6>
          description <txt>
          disable
          ip
              <usual IP options>
          ipv6
              <usual IPv6 options>
          vif-s <[0-4096]>
              address <ipv4>
              address <ipv6>
              description <txt>
              disable
              ip
                  <usual IP options>
              ipv6
                  <usual IPv6 options>
              vif-c <[0-4096]>
                  address <ipv4>
                  address <ipv6>
                  description <txt>
                  disable
                  ip
                      <usual IP options>
                  ipv6
                      <usual IPv6 options>


Example:

.. code-block:: none

  set interfaces ethernet eth0 vif-s 333
  set interfaces ethernet eth0 vif-s 333 address 192.0.2.10/32
  set interfaces ethernet eth0 vif-s 333 vif-c 777
  set interfaces ethernet eth0 vif-s 333 vif-c 777 address 10.10.10.10/24

.. _802.1ad: https://en.wikipedia.org/wiki/IEEE_802.1ad

Troubleshooting
###############

.. include:: ../../_include/interface-renew-dhcp.txt
