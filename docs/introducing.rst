.. _introducing:

###########
Introducing
###########

*****
About
*****

VyOS is an open source network operating system based on Debian GNU/Linux.

VyOS provides a free routing platform that competes directly with other
commercially available solutions from well known network providers. Because
VyOS is run on standard amd64, i586 and ARM systems, it is able to be used
as a router and firewall platform for cloud deployments.

We use multiple live versions of our manual hosted thankfully by
https://readthedocs.org. We will provide one version of the manual for every
VyOS major version starting with VyOS 1.2 which will receive Long-term support
(LTS).

The manual version is selected/specified by it's Git branch name. You can
switch between versions of the documentation by selecting the appropriate
branch on the bottom left corner.

VyOS CLI syntax may change between major (and sometimes minor) versions. Please
always refer to the documentation matching your current, running installation.
If a change in the CLI is required, VyOS will ship a so called migration script
which will take care of  adjusting the syntax. No action needs to be taken by
you.

*******
History
*******

VyOS is a Linux-based network operating system that provides software-based
network routing, firewall, and VPN functionality.

The VyOS project was started in late 2013 as a community fork of the
`GPL <https://en.wikipedia.org/wiki/GNU_General_Public_License>`_ portions of
Vyatta Core 6.6R1 with the goal of maintaining a free and open source network
operating system in response to the decision to discontinue the community
edition of Vyatta. Here everyone loves learning, older managers and new users.

VyOS is primarily based on `Debian GNU/Linux <https://www.debian.org/>`_ and
the `Quagga <http://www.nongnu.org/quagga/>`_ routing engine. Its configuration
syntax and :ref:`cli` are loosely derived from Juniper JUNOS as modelled by the
`XORP project <http://www.xorp.org/>`_, which was the original routing engine
for Vyatta.

In the 4.0 release of Vyatta, the routing engine was changed to Quagga. As of
VyOS version 1.2, VyOS now uses `FRRouting <https://frrouting.org/>`_ as the
routing engine.

How is VyOS different from any other router distributions and platform?

- It's more than just a firewall and VPN, VyOS includes extended routing
  capabilities like OSPFv2, OSPFv3, BGP, VRRP, and extensive route policy
  mapping and filtering
- Unified command line interface in the style of hardware routers.
- Scriptable CLI
- Stateful configuration system: prepare changes and commit at once or discard,
  view previous revisions or rollback to them, archive revisions to remote
  server and execute hooks at commit time
- Image-based upgrade: keep multiple versions on the same system and revert to
  previous image if a problem arises
- Multiple VPN capabilities: OpenVPN, IPSec, Wireguard, DPMVPN, IKEv2 and more
- DHCP, TFTP, mDNS repeater, broadcast relay and DNS forwarding support
- Both IPv4 and IPv6 support
- Runs on physical and virtual platforms alike: small x86 boards, big servers,
  KVM, Xen, VMware, Hyper-V, and more
- Completely free and open source, with documented internal APIs and build
  procedures
- Community driven. Patches are welcome and all code, bugs, and nightly builds
  are publicly accessible