import netmiko
from netmiko import ConnectHandler
import getpass # enrypt login credentials
import time


# define invetory for devices



numberOfDev = int(input('How much devices ? - '))
for num in range(numberOfDev):

    # define variables for firewall login
    fw_ip = input('Enter Firewall IP Address: ')
    fw_user = input('Enter Firewall SSH User: ')
    fw_pass = getpass.getpass('Enter Firewall SSH Passwqord: ')

    fw_dev = {'ip':fw_ip,
              'username':fw_user,
              'password':fw_pass,
              'device_type': 'paloalto_panos'}
    
    # connect to firewall
    ssh_connect = ConnectHandler(**fw_dev)
    print(f'Successful connection to {fw_ip} address')

     
    # define IPsec tunnel configuration
    ike_gateway_name = input('Define IKE GW Name: ')
    ipsec_tunnel_name = input('Define IPsec Tunnel Name: ')
    peer_public_ip = input('Define Peer Public IP: ')
    pre_shared_key = input('Define PSK: ')
    vpn_zone_name = input('Define VPN Zone Name: ')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()


    # define Tunnel Interface number
    last_created_tunnel_interface = input('Define Last Created Tunnel Interface Number: ')
    tunnel_interface = input('Define Tunnel Interface Number will be created: ')
    check = 3
    while check > 0:

        if int(tunnel_interface) > int(last_created_tunnel_interface):
            check=0
        else:
            break
    
    # choose Phase1 Proposals

    IKE_Crypto_Profile_List = ['Aes256-Sha1-dh14-86400',
                              'Aes256-Sha1-dh5-86400',
                              'Aes256-Sha1-dh14-28800']
    print('IKE-GW-Profile: ', IKE_Crypto_Profile_List)
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()


    ph1_sa = ''
    phase1 = input('Choose one of them(copy and paste here): ')
    if phase1 == 'Aes256-Sha1-dh14-86400':
        ph1_sa = IKE_Crypto_Profile_List[0]
    elif phase1 == 'Aes256-Sha1-dh5-86400':
        ph1_sa = IKE_Crypto_Profile_List[1]
    elif phase1 == 'Aes256-Sha1-dh14-28800':
        ph1_sa = IKE_Crypto_Profile_List[2]

    # choose Phase2 Proposals

    IPsec_Crypto_Profile_List = ['Aes256-Sha1-dh5-86400',
                                'Aes256-Sha1-dh5-28800',
                                'Aes256-Sha1-dh5-3600',
                                'Aes256-Sha1-dh5-no-pfs-3600',
                                'Aes256-Sha1-dh14-86400']
    print('IPsec-GW-Profile: ', IPsec_Crypto_Profile_List)
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()

    ph2_sa = ''
    phase2 = input('Choose one of them(copy and paste here): ')
    if phase2 == 'Aes256-Sha1-dh5-86400':
        ph2_sa = IPsec_Crypto_Profile_List[0]
    elif phase2 == 'Aes256-Sha1-dh5-28800':
        ph2_sa = IPsec_Crypto_Profile_List[1]
    elif phase2 == 'Aes256-Sha1-dh5-3600':
        ph2_sa = IPsec_Crypto_Profile_List[2]
    elif phase2 == 'Aes256-Sha1-dh5-no-pfs-3600':
        ph2_sa = IPsec_Crypto_Profile_List[3]
    elif phase2 == 'Aes256-Sha1-dh14-86400':
        ph2_sa = IPsec_Crypto_Profile_List[4]
    
    print()
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print('Configuration will deploy as soon as...')
    time.sleep(5)
    print('Please wait ...')

    # Create Tunnel Interface 

    command_for_Tunnel_Interface = [f'set network interface tunnel units tunnel.{tunnel_interface} ipv6 enabled no',
                                    f'set network interface tunnel units tunnel.{tunnel_interface} ipv6 interface-id EUI-64',
                                    f'set network interface tunnel units tunnel.{tunnel_interface} comment "Automation"',
                                    f'set zone {vpn_zone_name} network layer3 tunnel.{tunnel_interface}',
                                    f'set network virtual-router "default" interface tunnel.{tunnel_interface}']

    
    configuration_for_Tunnel_Interface = ssh_connect.send_config_set(command_for_Tunnel_Interface)
    print(f'VPN Zone {vpn_zone_name} has been created and assigned to Virtual-Router')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()
    print(f'Tunnel Interface {tunnel_interface} has been created')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()

    # Static VPN Route Configuration
    static_route_size = int(input('How much would you like to add route? : '))
    for route_size in range(static_route_size):
        ip_route_name = input('Define IP Route Name: ')
        ip_route = input('Define destination network: ')

        command_for_VPN_Route = [f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor enable no',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor failure-condition any',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor hold-time 2',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} bfd profile None',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} interface tunnel.{tunnel_interface}',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} metric 10',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} destination {ip_route}',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} route-table unicast']
        
        configuration_for_VPN_Route = ssh_connect.send_config_set(command_for_VPN_Route)
        print(f'VPN Route {ip_route_name} has been created')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()

    command_for_IKE = [f'set network ike gateway {ike_gateway_name} local-address ip 193.41.128.1/30',
                       f'set network ike gateway {ike_gateway_name} local-address interface ethernet1/1',
                       f'set network ike gateway {ike_gateway_name} authentication pre-shared-key key {pre_shared_key}',
                       f'set network ike gateway {ike_gateway_name} protocol ikev1 ike-crypto-profile {ph1_sa}',
                       f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd enable yes',
                       f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd interval 10',
                       f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd retry 2',
                       f'set network ike gateway {ike_gateway_name} protocol ikev2 dpd enable yes',
                       f'set network ike gateway {ike_gateway_name} protocol-common nat-traversal enable no',
                       f'set network ike gateway {ike_gateway_name} peer-address ip {peer_public_ip}',
                       f'set network ike gateway {ike_gateway_name} protocol-common fragmentation enable no']
        
    configuration_for_Phase1 = ssh_connect.send_config_set(command_for_IKE)
    print(f'IKE GW Configuration has been completed')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()


    command_for_IPsec = [f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ike-gateway {ike_gateway_name}',
                         f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ipsec-crypto-profile {ph2_sa}',
                         f'set network tunnel ipsec {ipsec_tunnel_name} tunnel-monitor enable no',
                         f'set network tunnel ipsec {ipsec_tunnel_name} anti-replay yes',
                         f'set network tunnel ipsec {ipsec_tunnel_name} copy-tos no',
                         f'set network tunnel ipsec {ipsec_tunnel_name} tunnel-interface tunnel.{tunnel_interface}',
                         ]
    configuration_for_Phase2 = ssh_connect.send_config_set(command_for_IPsec)
    print(f'IPsec Tunnel Configuration has been completed')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()                         
    
    
    ssh_connect.send_command("save")
    ssh_connect.exit_config_mode()
