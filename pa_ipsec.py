from netmiko import ConnectHandler
import getpass # enrypt login credentials
import time
import os

# define invetory for devices
print()
numberOfDev = int(input('How much devices will configure ? - '))
print()
for num in range(numberOfDev):

    # define variables for firewall login
    fw_ip = input('Enter Firewall IP Address: ')
    fw_user = input('Enter Firewall SSH User: ')
    fw_pass = getpass.getpass('Enter Firewall SSH Password: ')

    fw_dev = {'ip':fw_ip,
              'username':fw_user,
              'password':fw_pass,
              'device_type': 'paloalto_panos'}
    
    ssh_connect = ConnectHandler(**fw_dev)

    print()
    delay = 1.2
    char = '. . . .'
    for ch in char:
        print(ch, end="", flush=True)  # print the character without a newline
        time.sleep(delay) 
    print()
    print(f'Successful connection {fw_ip} address')
    time.sleep(3)
    os.system('cls' if os.name=='nt' else 'clear')
     
    # define IPsec tunnel configuration
    ike_gateway_name = input('Define IKE GW Name: ')
    ipsec_tunnel_name = input('Define IPsec Tunnel Name: ')
    local_public_ip = input('Define Local Public IP: (e.g193.41.128.1/24)')
    peer_public_ip = input('Define Peer Public IP: (e.g85.85.85.85)')
    pre_shared_key = input('Define PSK: ')
    vpn_zone_name = input('Define VPN Zone Name(if you have,use it same): ')
    tunnel_interface = int(input('Define Tunnel Interface Number: '))
    time.sleep(5)
    print('Please wait ... ')
    os.system('cls' if os.name=='nt' else 'clear')
    time.sleep(3)

    # define Tunnel Interface number 
    # not working for now
    #last_created_tunnel_interface = int(input('Define Last Created Tunnel Interface Number: '))
    
    #check = 3
    #while check > 0:

        #if int(tunnel_interface) > int(last_created_tunnel_interface):
            #pass
        #else:
            #check = check - 1
            #break
    
    # IKE Profile
    ike_profile = input('Would you like to use existing IKE Crypto Profile(1) or create new one(2) ? - Click, 1 or 2: ')
    # choose existing profile if you have in your PA device
    # you can add your IKE Crypto Profile name which is exist in your PA device(below is for me)
    if ike_profile == '1':
        # if you choose (1), print your crypto profile 
        IKE_Crypto_Profile_List = ['Aes256-Sha1-dh14-86400',
                                   'Aes256-Sha1-dh5-86400',
                                   'Aes256-Sha1-dh14-28800']
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        print('IKE-GW-Profile: ', IKE_Crypto_Profile_List)
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        time.sleep(3)
        print()
        ike_profile_name = ''
        phase1 = input('Choose one of them(copy and paste here): ')
        if phase1 == 'Aes256-Sha1-dh14-86400':
            ike_profile_name = IKE_Crypto_Profile_List[0]
            command_for_IKE_Profile = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} hash sha1',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} encryption aes-256-cbc ',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} dh-group group14',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} lifetime hours 24']
        elif phase1 == 'Aes256-Sha1-dh5-86400':
            ph1_sa = IKE_Crypto_Profile_List[1]
            command_for_IKE_Profile = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} hash sha1',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} encryption aes-256-cbc ',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} dh-group group5',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} lifetime hours 24']
        elif phase1 == 'Aes256-Sha1-dh14-28800':
            ph1_sa = IKE_Crypto_Profile_List[2]
            command_for_IKE_Profile = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} hash sha1',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} encryption aes-256-cbc ',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} dh-group group14',
                                       f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} lifetime seconds 28800']
        print()
        # configuration stage for existing IKE GW Profile
        configuration_for_IKE_Profile = ssh_connect.send_config_set(command_for_IKE_Profile)
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        print('IKE Crypto Profile Setting has been configured...')
        time.sleep(5)
        print('Please wait ...')
        print('IKE Crypto Profile Setting has been completed...')
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        time.sleep(3)
        os.system('cls' if os.name=='nt' else 'clear')
        

    elif ike_profile == '2':
        # if you choose (2), create your own crypto profile
        ike_profile_name = input('Define IKE-Profile name: ')
        # create your authentication values
        ike_auth = ['sha1','sha256','sha384','sha512','md5']
        print()
        print(ike_auth)
        ike_auth_value = input('Define Authentication Header: ')
        if ike_auth_value == 'sha1':
            ike_auth_value == ike_auth[0]
        elif ike_auth_value == 'sha256':
            ike_auth_value == ike_auth[1]
        elif ike_auth_value == 'sha384':
            ike_auth_value == ike_auth[2]
        elif ike_auth_value == 'sha512':
            ike_auth_value == ike_auth[3]
        elif ike_auth_value == 'md5':
            ike_auth_value == ike_auth[4]
        
        # create your encryption values
        ike_encrypt = ['aes-128-cbc','aes-192-cbc','aes256-cbc','3des','aes128-gcm','aes256-gcm']
        print()
        print(ike_encrypt)
        ike_encr_value = input('Define Encryption Header: ')
        if ike_encr_value == 'aes-128-cbc':
            ike_encr_value == ike_encrypt[0]
        elif ike_encr_value == 'aes-192-cbc':
            ike_encr_value == ike_encrypt[1]
        elif ike_encr_value == 'aes-256-cbc':
            ike_encr_value == ike_encrypt[2]
        elif ike_encr_value == '3des':
            ike_encr_value == ike_encrypt[3]
        elif ike_encr_value == 'aes-128-gcm':
            ike_encr_value == ike_encrypt[4]
        elif ike_encr_value == 'aes-256-gcm':
            ike_encr_value == ike_encrypt[5]
        
        # create your diffie-helman values
        ike_diffie_hellman = ['group1','group2','group5','group14','group15']
        print()
        print(ike_diffie_hellman)
        ike_dh_value = input('Define DH Group: ')
        if ike_dh_value == 'group1':
            ike_dh_value == ike_diffie_hellman[0]
        elif ike_dh_value == 'group2':
            ike_dh_value == ike_diffie_hellman[1]
        elif ike_dh_value == 'group5':
            ike_dh_value == ike_diffie_hellman[2]
        elif ike_dh_value == 'group14':
            ike_dh_value == ike_diffie_hellman[3]
        elif ike_dh_value == 'group15':
            ike_dh_value == ike_diffie_hellman[4]

        ike_lifetime = input('Define your lifetime: seconds(click 1) / hours(click 2)')
        if ike_lifetime == '1':
            print('ike life time will accepted like as seconds format')
            ike_lifetime_value = input('Define lifetime : ')
            pan_cmd = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} lifetime seconds {ike_lifetime_value}']
            conf_pan_cmd = ssh_connect.send_config_set(pan_cmd)
        elif ike_lifetime == '2':
            print('ike life time will accepted like as hours format')
            ike_lifetime_value = input('Define lifetime : ')
            pan_cmd = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} lifetime hours {ike_lifetime_value}']
            conf_pan_cmd = ssh_connect.send_config_set(pan_cmd)

        # configuration stage for IKE GW Profile

        command_for_IKE_Profile = [f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} hash {ike_auth_value}',
                                   f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} encryption {ike_encr_value}',
                                   f'set network ike crypto-profiles ike-crypto-profiles {ike_profile_name} dh-group {ike_dh_value}']

        configuration_for_IKE_Profile = ssh_connect.send_config_set(command_for_IKE_Profile)
        print()
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        print()
        print('IKE Crypto Profile Setting has been configured...')
        print()
        time.sleep(5)
        print('Please wait ...')
        print('IKE Crypto Profile Setting has been completed...')
        os.system('cls' if os.name=='nt' else 'clear')
        time.sleep(3)


    # choose Phase2 Proposals
    print()
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
    print()
    print('Configuration phase will start as soon as...')
    print()
    time.sleep(5)
    print('Please wait ...')
    print()

    # Create Tunnel Interface 

    command_for_Tunnel_Interface = [f'set network interface tunnel units tunnel.{tunnel_interface} ipv6 enabled no',
                                    f'set network interface tunnel units tunnel.{tunnel_interface} ipv6 interface-id EUI-64',
                                    f'set network interface tunnel units tunnel.{tunnel_interface} comment "Automation"',
                                    f'set zone {vpn_zone_name} network layer3 tunnel.{tunnel_interface}',
                                    f'set network virtual-router "default" interface tunnel.{tunnel_interface}']
    
    configuration_for_Tunnel_Interface = ssh_connect.send_config_set(command_for_Tunnel_Interface)
    print()
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()
    print('Tunnel Interface Setting has been configured...')
    print()
    time.sleep(5)
    print('Please wait ...')
    print('Tunnel Interface Setting has been completed...')
    print()

    # Static VPN Route Configuration
    static_route_count = 1
    static_route_size = int(input('How much would you like to add route? : '))
    for route_size in range(static_route_size):
        ip_route_name = input(f'{static_route_count}Define IP Route Name: ')
        ip_route = input('Define destination network: ')
        ip_route_metric = input('Define destination route metric: ')
        static_route_count = static_route_count + 1

        command_for_VPN_Route = [f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor enable no',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor failure-condition any',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} path-monitor hold-time 2',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} bfd profile None',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} interface tunnel.{tunnel_interface}',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} metric {ip_route_metric}',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} destination {ip_route}',
                                f'set network virtual-router "default" routing-table ip static-route {ip_route_name} route-table unicast']
        
        configuration_for_VPN_Route = ssh_connect.send_config_set(command_for_VPN_Route)
        print()
        print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
        print()
        time.sleep(5)
        print('Please wait ...')
        print(f'VPN Route {ip_route_name} has been created')
        print()
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()

    # IKE Gateway Configuration
    # You should have to choose your LOCAL INTERFACE ID (at LINE 270)
    command_for_IKE = [f'set network ike gateway {ike_gateway_name} local-address ip {local_public_ip}',
                       f'set network ike gateway {ike_gateway_name} local-address interface ethernet1/1',
                       f'set network ike gateway {ike_gateway_name} authentication pre-shared-key key {pre_shared_key}',
                       f'set network ike gateway {ike_gateway_name} protocol ikev1 ike-crypto-profile {ike_profile_name}',
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

    # IPsec Tunnel Configuration

    command_for_IPsec = [f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ike-gateway {ike_gateway_name}',
                        f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ipsec-crypto-profile {ph2_sa}',
                        f'set network tunnel ipsec {ipsec_tunnel_name} tunnel-monitor enable no',
                        f'set network tunnel ipsec {ipsec_tunnel_name} tunnel-interface tunnel.{tunnel_interface}',
                            ]
    configuration_for_Phase2 = ssh_connect.send_config_set(command_for_IPsec)

    # Proxy ID Configuration If your connection will be Policy-Based VPN
    
    proxy_id = input('Do you need proxy-id ? "Y / N ? - "')   
    print()
    proxy_id_count = 0
    if proxy_id == "Y":
            proxy_id_size = int(input('How much proxy id would you like to add ? '))
            for proxy_id in range(proxy_id_size):
                proxy_id_count = proxy_id_count + 1
                proxy_id_name = input(f'{proxy_id_count}.Define Proxy ID Name: ')
                proxy_id_protocol = 'any'
                proxy_id_local = input('Define Proxy ID Local Subnet: ')
                proxy_id_remote = input('Define Proxy ID Remote Subnet: ')
                print()
                command_for_Proxy_ID = [f'set network tunnel ipsec {ipsec_tunnel_name} auto-key proxy-id {proxy_id_name} protocol {proxy_id_protocol} ',
                                        f'set network tunnel ipsec {ipsec_tunnel_name} auto-key proxy-id {proxy_id_name} local {proxy_id_local}',
                                        f'set network tunnel ipsec {ipsec_tunnel_name} auto-key proxy-id {proxy_id_name} remote {proxy_id_remote}']
                configuration_for_proxy_id = ssh_connect.send_config_set(command_for_Proxy_ID)
            print()
            print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
            print()
    print(f'IPsec Tunnel Configuration has been completed')
    print('#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#')
    print()
