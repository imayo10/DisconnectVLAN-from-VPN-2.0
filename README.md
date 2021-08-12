# DisconnectVLAN-from-VPN-2.0

Monitor all the networks in the org and disconnect a VLAN from the VPN in case of failure of the primary link.

With this code you can monitor the status of the main link (WAN 1) in a Meraki MX, and in case of failure of this link, 
"automagically" stop announcing a certain VLAN over the SD-WAN, for example a VLAN that consumes a lot of bandwidth, 
like the one used for CCTV, Voice, Video, etc.

Great to use when your secondary link is Satellite or Cellular, and you want to avoid large charges for passing non 
critical traffic over Meraki SD-WAN/AutoVPN
