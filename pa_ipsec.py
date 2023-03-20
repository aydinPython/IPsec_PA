import paramiko
import getpass # enrypt login credentials
import time


# define invetory for devices

numberOfDev = int('How much devices ? - ')
for num in range(numberOfDev):

    # define variables for firewall login
    fw_ip = input('Enter Firewall IP Address: ')
    fw_user = input('Enter Firewall SSH User: ')
    fw_pass = getpass.getpass('Enter Firewall SSH Passwqord: ')

    # create SSH client object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to firewall
    ssh.connect(fw_ip, username=fw_user, password=fw_pass)

    # define IPsec tunnel configuration
    ike_gateway_name = input('Define IKE GW Name: ')
    ipsec_tunnel_name = input('Define IPsec Tunnel Name: ')
    peer_public_ip = input('Peer Public IP: ')
    pre_shared_key = input('PSK: ')
    
    # define Tunnel Interface number
    last_created_tunnel_interface = '28'
    tunnel_interface = input('Define Tunnel Interface Number: ')
    check = 3
    while check > 0:
        if int(tunnel_interface) <= int(last_created_tunnel_interface):
            print(f'The Tunnel Number {check} already exist,try highest number')
            check=check-1
            if check == 0:
                break
        elif int(tunnel_interface) > int(last_created_tunnel_interface):
            print(f'The Tunnel Number {check} will be created')
            check=check-1

    # choose Phase1 Proposals

    IKE_Crypto_Profile_List = ['Aes256-Sha1-dh14-86400',
                              'Aes256-Sha1-dh5-86400',
                              'Aes256-Sha1-dh14-28800']
    print(IKE_Crypto_Profile_List)
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
    print(IPsec_Crypto_Profile_List)
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
    

    # configure IKE gateway

    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} local-address ip x.y.w.z/x')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} local-address interface ae00.xywz')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} pre-shared-key ascii-text {pre_shared_key}')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol ikev1 ike-crypto-profile {ph1_sa}')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd enable yes')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd interval 10')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol ikev1 dpd retry 2')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol ikev2 dpd enable yes')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol-common nat-traversal enable no')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} protocol-common fragmentation enable no')
    stdin, stdout, stderr = ssh.exec_command(f'set network ike gateway {ike_gateway_name} peer-address ip {peer_public_ip}')

    # configure IPsec tunnel
    stdin, stdout, stderr = ssh.exec_command(f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ike-gateway {ike_gateway_name}')
    stdin, stdout, stderr = ssh.exec_command(f'set network tunnel ipsec {ipsec_tunnel_name} auto-key ipsec-crypto-profile {ph2_sa)
    stdin, stdout, stderr = ssh.exec_command(f'set network tunnel ipsec {ipsec_tunnel_name} tunnel-interface {tunnel_interface}')

    # save configuration
    stdin, stdout, stderr = ssh.exec_command('commit')

    # disconnect from firewall
    ssh.close()
