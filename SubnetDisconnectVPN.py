import time
import meraki
import credentials
import pandas as pd

#Import the csv file with the subnets you want to disconnect from VPN in case of WAN 1 Failure

routes = pd.read_csv('routes.csv', names = ['Routes'])

route_list = routes.Routes.to_list()
route_list.pop(0)

#Call Meraki API 
dashboard = meraki.DashboardAPI(credentials.api_key)

i = True

while i == True:
    
    # Ask for the status of all the links in the organization, Fill organizationId with the correct ID

    links = dashboard.organizations.getOrganizationUplinksStatuses(organizationId="XXXXXXXXXXXXXXXXX")
    for network in links:
        try:
            for uplinks in network['uplinks']:
                if uplinks['interface']=='wan1' and uplinks['status']=='active':
                    print(network)
                    print("Primary Uplink is active")
                    routes = dashboard.appliance.getNetworkApplianceStaticRoutes(network['networkId'])
                    vpn = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'])
                    for subnet in vpn['subnets']:
                        if subnet['localSubnet'] in route_list and subnet['useVpn'] == False:
                            subnet['useVpn'] = True
                            del vpn['mode']
                            #print(vpn)
                            print("CHANGE - Reconnecting voice subnet to VPN, main uplink goes up ")
                            update = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                                networkId=network['networkId'], mode='spoke', **vpn)
                        elif subnet['localSubnet'] in route_list and subnet['useVpn'] == True:
                            print("Primary uplink is active, voice vlan is on VPN")

                #In case of failure of the WAN1 link, the subnet will be disconnected from the VPN.

                elif uplinks['interface']=='wan1' and uplinks['status']=='not connected' or uplinks['status']=='failed':
                    print("Primary uplink is down")
                    vpn = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'])
                    for subnet in vpn['subnets']:
                        if subnet['localSubnet'] in route_list and subnet['useVpn']==True:
                            subnet['useVpn']=False
                            del vpn['mode']
                            print("CHANGE - Disconnecting voice vlan from VPN, Primary uplink is down")
                            update = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'], mode='spoke', **vpn)
                        elif subnet['localSubnet'] in route_list and subnet['useVpn'] == False:
                            print("Primary uplink is down, voice vlan is disconnected of the VPN")
        except TypeError as e:
            print(e)
        except meraki.APIError as e:
            print(e)
    time.sleep(5)