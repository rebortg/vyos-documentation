:orphan:

########
Coverage
########

Overview over all commands, which are documented in the ``.. cfgcmd::`` or ``.. opcmd::`` Directives.

| The build process take all xml definition files from `vyos-1x <https://github.com/vyos/vyos-1x>`_  and extract each leaf command or executable command.
| After this the commands are compare and shown in the follwoing two tables.

**There are 2 kind of problems:**   

| ``Not documented yet``
| A XML command are not found in ``.. cfgcmd::`` or ``.. opcmd::`` Commands
| The command should be documented

| ``Nothing found in XML Definitions``: 
| ``.. cfgcmd::`` or ``.. opcmd::`` Command are not found in a XML command
| Maybe the command where changed in the XML Definition, or the feature is not anymore in vyos
| Some commands are not yet translated to XML


Configuration Commands
======================

.. cfgcmdlist::
    :show-coverage:


Operational Commands
====================

.. opcmdlist::
    :show-coverage: