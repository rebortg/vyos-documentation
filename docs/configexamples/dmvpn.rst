.. _examples-dmvpn:

#########
DMVPN Hub
#########

General infomration can be found in the vpn-dmvpn chapter.

Configuration
=============

VyOS Hub
--------

.. code-block:: none

  set interfaces tunnel tun100 address '172.16.253.134/29'
  set interfaces tunnel tun100 encapsulation 'gre'
  set interfaces tunnel tun100 local-ip '203.0.113.44'
  set interfaces tunnel tun100 multicast 'enable'
  set interfaces tunnel tun100 parameters ip key '1'

  set protocols nhrp tunnel tun100 cisco-authentication <secret>
  set protocols nhrp tunnel tun100 holding-time '300'
  set protocols nhrp tunnel tun100 multicast 'dynamic'
  set protocols nhrp tunnel tun100 redirect
  set protocols nhrp tunnel tun100 shortcut

  set vpn ipsec esp-group ESP-HUB compression 'disable'
  set vpn ipsec esp-group ESP-HUB lifetime '1800'
  set vpn ipsec esp-group ESP-HUB mode 'tunnel'
  set vpn ipsec esp-group ESP-HUB pfs 'dh-group2'
  set vpn ipsec esp-group ESP-HUB proposal 1 encryption 'aes256'
  set vpn ipsec esp-group ESP-HUB proposal 1 hash 'sha1'
  set vpn ipsec esp-group ESP-HUB proposal 2 encryption '3des'
  set vpn ipsec esp-group ESP-HUB proposal 2 hash 'md5'
  set vpn ipsec ike-group IKE-HUB ikev2-reauth 'no'
  set vpn ipsec ike-group IKE-HUB key-exchange 'ikev1'
  set vpn ipsec ike-group IKE-HUB lifetime '3600'
  set vpn ipsec ike-group IKE-HUB proposal 1 dh-group '2'
  set vpn ipsec ike-group IKE-HUB proposal 1 encryption 'aes256'
  set vpn ipsec ike-group IKE-HUB proposal 1 hash 'sha1'
  set vpn ipsec ike-group IKE-HUB proposal 2 dh-group '2'
  set vpn ipsec ike-group IKE-HUB proposal 2 encryption 'aes128'
  set vpn ipsec ike-group IKE-HUB proposal 2 hash 'sha1'
  set vpn ipsec ipsec-interfaces interface 'eth0'

  set vpn ipsec profile NHRPVPN authentication mode 'pre-shared-secret'
  set vpn ipsec profile NHRPVPN authentication pre-shared-secret <secret>
  set vpn ipsec profile NHRPVPN bind tunnel 'tun100'
  set vpn ipsec profile NHRPVPN esp-group 'ESP-HUB'
  set vpn ipsec profile NHRPVPN ike-group 'IKE-HUB'

Cisco IOS Spoke
---------------

This example is verified with a Cisco 2811 platform running IOS 15.1(4)M9 and
VyOS 1.1.7 (helium) up to VyOS 1.2 (Crux).

.. code-block:: none

  Cisco IOS Software, 2800 Software (C2800NM-ADVENTERPRISEK9-M), Version 15.1(4)M9, RELEASE SOFTWARE (fc3)
  Technical Support: http://www.cisco.com/techsupport
  Copyright (c) 1986-2014 by Cisco Systems, Inc.
  Compiled Fri 12-Sep-14 10:45 by prod_rel_team

  ROM: System Bootstrap, Version 12.3(8r)T7, RELEASE SOFTWARE (fc1)

Use this configuration on your Cisco device:

.. code-block:: none

  crypto pki token default removal timeout 0
  crypto keyring DMVPN
    pre-shared-key address 198.51.100.2 key <secretkey>
  !
  crypto isakmp policy 10
   encr aes 256
   authentication pre-share
   group 2
  !
  crypto isakmp invalid-spi-recovery
  crypto isakmp keepalive 30 30 periodic
  crypto isakmp profile DMVPN
     keyring DMVPN
     match identity address 203.0.113.44 255.255.255.255
  !
  crypto ipsec transform-set DMVPN-AES256 esp-aes 256 esp-sha-hmac
   mode transport
  !
  crypto ipsec profile DMVPN
   set security-association idle-time 720
   set transform-set DMVPN-AES256
   set isakmp-profile DMVPN
  !
  interface Tunnel10
   description Tunnel to DMVPN HUB
   ip address 172.16.253.129 255.255.255.248
   no ip redirects
   ip nhrp authentication <nhrp secret key>
   ip nhrp map multicast 203.0.113.44
   ip nhrp map 172.16.253.134 203.0.113.44
   ip nhrp network-id 1
   ip nhrp holdtime 600
   ip nhrp nhs 172.16.253.134
   ip nhrp registration timeout 75
   tunnel source Dialer1
   tunnel mode gre multipoint
   tunnel key 1


.. _vpn-dmvpn:

.. todo::

    move to examples

DMVPN
-----

**D** ynamic **M** ultipoint **V** irtual **P** rivate **N** etworking

DMVPN is a dynamic VPN technology originally developed by Cisco. While their
implementation was somewhat proprietary, the underlying technologies are
actually standards based. The three technologies are:

* **NHRP** - NBMA Next Hop Resolution Protocol :rfc:`2332`
* **mGRE** - Multipoint Generic Routing Encapsulation / mGRE :rfc:`1702`
* **IPSec** - IP Security (too many RFCs to list, but start with :rfc:`4301`)

NHRP provides the dynamic tunnel endpoint discovery mechanism (endpoint
registration, and endpoint discovery/lookup), mGRE provides the tunnel
encapsulation itself, and the IPSec protocols handle the key exchange, and
crypto mechanism.

In short, DMVPN provides the capability for creating a dynamic-mesh VPN
network without having to pre-configure (static) all possible tunnel end-point
peers.

.. note:: DMVPN only automates the tunnel endpoint discovery and setup. A
   complete solution also incorporates the use of a routing protocol. BGP is
   particularly well suited for use with DMVPN.

Baseline Configuration:

**STEPS:**

#. Create tunnel config (`interfaces tunnel`)
#. Create nhrp (`protocols nhrp`)
#. Create ipsec vpn (optional, but recommended for security) (`vpn ipsec`)

The tunnel will be set to mGRE if for encapsulation `gre` is set, and no
`remote-ip` is set. If the public ip is provided by DHCP the tunnel `local-ip`
can be set to "0.0.0.0". If you do set the `remote-ip` directive at any point, the interface will need to be `delete`'d from the config and recreated without the `remote-ip` config ever being set.

.. figure:: /_static/images/vpn_dmvpn_topology01.png
   :scale: 40 %
   :alt: Baseline DMVPN topology

   Baseline DMVPN topology

HUB Configuration
^^^^^^^^^^^^^^^^^

.. code-block:: none

  interfaces
      tunnel <tunN> {
          address <ipv4>
          encapsulation gre
          local-ip <public ip>
          multicast enable
          description <txt>
          parameters {
              ip {
                  <usual IP options>
              }
          }
      }
  }
  protocols {
      nhrp {
          tunnel <tunN> {
              cisco-authentication <key phrase>
              holding-time <seconds>
              multicast dynamic
              redirect
          }
      }
  }
  vpn {
      ipsec {
          esp-group <text> {
              lifetime <30-86400>
              mode tunnel
              pfs enable
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption 3des
                  hash md5
              }
          }
          ike-group <text> {
              key-exchange ikev1
              lifetime <30-86400>
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption aes128
                  hash sha1
              }
          }
          ipsec-interfaces {
              interface <ethN>
          }
          profile <text> {
              authentication {
                  mode pre-shared-secret
                  pre-shared-secret <key phrase>
              }
              bind {
                  tunnel <tunN>
              }
              esp-group <text>
              ike-group <text>
          }
      }
  }

HUB Example Configuration:

.. code-block:: none

  set interfaces ethernet eth0 address '198.51.100.41/30'
  set interfaces ethernet eth1 address '192.168.1.1/24'
  set system host-name 'HUB'

  set interfaces tunnel tun0 address 10.0.0.1/24
  set interfaces tunnel tun0 encapsulation gre
  set interfaces tunnel tun0 local-ip 198.51.100.41
  set interfaces tunnel tun0 multicast enable
  set interfaces tunnel tun0 parameters ip key 1

  set protocols nhrp tunnel tun0 cisco-authentication SECRET
  set protocols nhrp tunnel tun0 holding-time  300
  set protocols nhrp tunnel tun0 multicast dynamic
  set protocols nhrp tunnel tun0 redirect

  set vpn ipsec ipsec-interfaces interface eth0
  set vpn ipsec ike-group IKE-HUB proposal 1
  set vpn ipsec ike-group IKE-HUB proposal 1 encryption aes256
  set vpn ipsec ike-group IKE-HUB proposal 1 hash sha1
  set vpn ipsec ike-group IKE-HUB proposal 2 encryption aes128
  set vpn ipsec ike-group IKE-HUB proposal 2 hash sha1
  set vpn ipsec ike-group IKE-HUB lifetime 3600
  set vpn ipsec esp-group ESP-HUB proposal 1 encryption aes256
  set vpn ipsec esp-group ESP-HUB proposal 1 hash sha1
  set vpn ipsec esp-group ESP-HUB proposal 2 encryption 3des
  set vpn ipsec esp-group ESP-HUB proposal 2 hash md5
  set vpn ipsec esp-group ESP-HUB lifetime 1800
  set vpn ipsec esp-group ESP-HUB pfs dh-group2

  set vpn ipsec profile NHRPVPN
  set vpn ipsec profile NHRPVPN authentication mode pre-shared-secret
  set vpn ipsec profile NHRPVPN authentication pre-shared-secret SECRET
  set vpn ipsec profile NHRPVPN bind tunnel tun0
  set vpn ipsec profile NHRPVPN esp-group ESP-HUB
  set vpn ipsec profile NHRPVPN ike-group IKE-HUB

  set protocols static route 0.0.0.0/0 next-hop 1.1.1.2
  set protocols static route 192.168.2.0/24 next-hop 10.0.0.2
  set protocols static route 192.168.3.0/24 next-hop 10.0.0.3

HUB on AWS Configuration Specifics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Setting this up on AWS will require a "Custom Protocol Rule" for protocol number "47" (GRE) Allow Rule in TWO places. Firstly on the VPC Network ACL, and secondly on the security group network ACL attached to the EC2 instance. This has been tested as working for the official AMI image on the AWS Marketplace. (Locate the correct VPC and security group by navigating through the details pane below your EC2 instance in the AWS console)

SPOKE Configuration
^^^^^^^^^^^^^^^^^^^

SPOKE1 Configuration:

.. code-block:: none

  interfaces
      tunnel <tunN> {
          address <ipv4>
          encapsulation gre
          local-ip <public ip>
          multicast enable
          description <txt>
          parameters {
              ip {
                  <usual IP options>
              }
          }
      }
  }
  protocols {
      nhrp {
          tunnel <tunN> {
              cisco-authentication <key phrase>
              map <ipv4/net> {
                  nbma-address <ipv4>
                  register
              }
              holding-time <seconds>
              multicast nhs
              redirect
              shortcut
          }
      }
  }
  vpn {
      ipsec {
          esp-group <text> {
              lifetime <30-86400>
              mode tunnel
              pfs enable
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption 3des
                  hash md5
              }
          }
          ike-group <text> {
              key-exchange ikev1
              lifetime <30-86400>
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption aes128
                  hash sha1
              }
          }
          ipsec-interfaces {
              interface <ethN>
          }
          profile <text> {
              authentication {
                  mode pre-shared-secret
                  pre-shared-secret <key phrase>
              }
              bind {
                  tunnel <tunN>
              }
              esp-group <text>
              ike-group <text>
          }
      }
  }

SPOKE1 Example Configuration

.. code-block:: none

  set interfaces ethernet eth0 address 'dhcp'
  set interfaces ethernet eth1 address '192.168.2.1/24'
  set system host-name 'SPOKE1'

  set interfaces tunnel tun0 address 10.0.0.2/24
  set interfaces tunnel tun0 encapsulation gre
  set interfaces tunnel tun0 local-ip 0.0.0.0
  set interfaces tunnel tun0 multicast enable
  set interfaces tunnel tun0 parameters ip key 1

  set protocols nhrp tunnel tun0 cisco-authentication 'SECRET'
  set protocols nhrp tunnel tun0 map 10.0.0.1/24 nbma-address 198.51.100.41
  set protocols nhrp tunnel tun0 map 10.0.0.1/24 'register'
  set protocols nhrp tunnel tun0 multicast 'nhs'
  set protocols nhrp tunnel tun0 'redirect'
  set protocols nhrp tunnel tun0 'shortcut'

  set vpn ipsec ipsec-interfaces interface eth0
  set vpn ipsec ike-group IKE-SPOKE proposal 1
  set vpn ipsec ike-group IKE-SPOKE proposal 1 encryption aes256
  set vpn ipsec ike-group IKE-SPOKE proposal 1 hash sha1
  set vpn ipsec ike-group IKE-SPOKE proposal 2 encryption aes128
  set vpn ipsec ike-group IKE-SPOKE proposal 2 hash sha1
  set vpn ipsec ike-group IKE-SPOKE lifetime 3600
  set vpn ipsec esp-group ESP-SPOKE proposal 1 encryption aes256
  set vpn ipsec esp-group ESP-SPOKE proposal 1 hash sha1
  set vpn ipsec esp-group ESP-SPOKE proposal 2 encryption 3des
  set vpn ipsec esp-group ESP-SPOKE proposal 2 hash md5
  set vpn ipsec esp-group ESP-SPOKE lifetime 1800
  set vpn ipsec esp-group ESP-SPOKE pfs dh-group2

  set vpn ipsec profile NHRPVPN
  set vpn ipsec profile NHRPVPN authentication mode pre-shared-secret
  set vpn ipsec profile NHRPVPN authentication pre-shared-secret SECRET
  set vpn ipsec profile NHRPVPN bind tunnel tun0
  set vpn ipsec profile NHRPVPN esp-group ESP-SPOKE
  set vpn ipsec profile NHRPVPN ike-group IKE-SPOKE

  set protocols static route 192.168.1.0/24 next-hop 10.0.0.1
  set protocols static route 192.168.3.0/24 next-hop 10.0.0.3


SPOKE2 Configuration

.. code-block:: none

  interfaces
      tunnel <tunN> {
          address <ipv4>
          encapsulation gre
          local-ip <public ip>
          multicast enable
          description <txt>
          parameters {
              ip {
                  <usual IP options>
              }
          }
      }
  }
  protocols {
      nhrp {
          tunnel <tunN> {
              cisco-authentication <key phrase>
              map <ipv4/net> {
                  nbma-address <ipv4>
                  register
              }
              holding-time <seconds>
              multicast nhs
              redirect
              shortcut
          }
      }
  }
  vpn {
      ipsec {
          esp-group <text> {
              lifetime <30-86400>
              mode tunnel
              pfs enable
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption 3des
                  hash md5
              }
          }
          ike-group <text> {
              key-exchange ikev1
              lifetime <30-86400>
              proposal <1-65535> {
                  encryption aes256
                  hash sha1
              }
              proposal <1-65535> {
                  encryption aes128
                  hash sha1
              }
          }
          ipsec-interfaces {
              interface <ethN>
          }
          profile <text> {
              authentication {
                  mode pre-shared-secret
                  pre-shared-secret <key phrase>
              }
              bind {
                  tunnel <tunN>
              }
              esp-group <text>
              ike-group <text>
          }
      }
  }

SPOKE2 Example Configuration

.. code-block:: none

  set interfaces ethernet eth0 address 'dhcp'
  set interfaces ethernet eth1 address '192.168.3.1/24'
  set system host-name 'SPOKE2'

  set interfaces tunnel tun0 address 10.0.0.3/24
  set interfaces tunnel tun0 encapsulation gre
  set interfaces tunnel tun0 local-ip 0.0.0.0
  set interfaces tunnel tun0 multicast enable
  set interfaces tunnel tun0 parameters ip key 1

  set protocols nhrp tunnel tun0 cisco-authentication SECRET
  set protocols nhrp tunnel tun0 map 10.0.0.1/24 nbma-address 198.51.100.41
  set protocols nhrp tunnel tun0 map 10.0.0.1/24 register
  set protocols nhrp tunnel tun0 multicast nhs
  set protocols nhrp tunnel tun0 redirect
  set protocols nhrp tunnel tun0 shortcut

  set vpn ipsec ipsec-interfaces interface eth0
  set vpn ipsec ike-group IKE-SPOKE proposal 1
  set vpn ipsec ike-group IKE-SPOKE proposal 1 encryption aes256
  set vpn ipsec ike-group IKE-SPOKE proposal 1 hash sha1
  set vpn ipsec ike-group IKE-SPOKE proposal 2 encryption aes128
  set vpn ipsec ike-group IKE-SPOKE proposal 2 hash sha1
  set vpn ipsec ike-group IKE-SPOKE lifetime 3600
  set vpn ipsec esp-group ESP-SPOKE proposal 1 encryption aes256
  set vpn ipsec esp-group ESP-SPOKE proposal 1 hash sha1
  set vpn ipsec esp-group ESP-SPOKE proposal 2 encryption 3des
  set vpn ipsec esp-group ESP-SPOKE proposal 2 hash md5
  set vpn ipsec esp-group ESP-SPOKE lifetime 1800
  set vpn ipsec esp-group ESP-SPOKE pfs dh-group2

  set vpn ipsec profile NHRPVPN
  set vpn ipsec profile NHRPVPN authentication mode pre-shared-secret
  set vpn ipsec profile NHRPVPN authentication pre-shared-secret SECRET
  set vpn ipsec profile NHRPVPN bind tunnel tun0
  set vpn ipsec profile NHRPVPN esp-group ESP-SPOKE
  set vpn ipsec profile NHRPVPN ike-group IKE-SPOKE

  set protocols static route 192.168.1.0/24 next-hop 10.0.0.1
  set protocols static route 192.168.2.0/24 next-hop 10.0.0.2
