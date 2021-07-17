import argparse
import datetime
import getpass
import logging
from typing import Dict

from srunbit import model
from srunbit import network
from srunbit import store


def execute():
    logging.getLogger('network').setLevel(logging.DEBUG)
    logging.getLogger('.').setLevel(logging.INFO)
    n = network.Network()

    parser = argparse.ArgumentParser(description='Sign in/out BIT campus network')
    subparsers = parser.add_subparsers(dest='action')

    login_paraser = subparsers.add_parser('login', help='login to network')
    logout_parser = subparsers.add_parser('logout', help='sign out network')
    info_parser = subparsers.add_parser('info', help='get account info')

    config_parser = subparsers.add_parser('config', help='set Username and Password')
    # config_parser.add_argument(dest='username', type=str, help='User ID')
    # config_parser.add_argument(dest='password', type=str, help='Password')

    args = parser.parse_args()
    action = args.action

    if action == 'login':
        account = store.read_account()
        if account is None:
            print('Please run config first')
        else:
            code = n.login(account)
            if code == network.LoginCode.SUCCEED:
                print('Login succeed!')
            elif code == network.LoginCode.ARREARAGE:
                print('Account in arrear.')
            elif code == network.LoginCode.ALREADY_ONLINE:
                print('Account already online.')
            elif code == network.LoginCode.WRONG_PASSWORD:
                print('Wrong password.')
            elif code == network.LoginCode.USER_DISABLED:
                print('User disabled.')
            else:
                print('Login failed.')

    elif action == 'logout':
        account = store.read_account()
        if account is None:
            print('Please run config first')
        else:
            code = n.logout(account)
            if code == network.LogoutCode.SUCCEED:
                print('Logout succeed!')
            elif code == network.LogoutCode.ALREADY_OFFLINE:
                print('You are not online.')
            else:
                print('Logout failed.')
    elif action == 'info':
        info = n.get_info()
        _print_info(info)
    elif action == 'config':
        user = input('UserID: ')
        passwd = getpass.getpass(prompt='Password: ')

        account = model.Account(user, passwd)
        store.write_account(account)


def _print_info(info: Dict):
    if info['error'] != 'ok':
        print(f'IP:\t{info["online_ip"]}')
        print(f'Error:\t{info["error"]}')
        return

    print(f'IP:\t\t{info["online_ip"]}')
    print(f'User Name:\t{info["real_name"]}')
    print(f'User ID:\t{info["user_name"]}')
    print(f'Wallet Balance:\t￥{info["wallet_balance"]:.2f}')
    print(f'User Balance:\t￥{info["user_balance"]:.2f}')
    print(f'Used Traffic:\t{_format_traffic(int(info["sum_bytes"]))}')
    print(f'Elapsed Time:\t{_format_time(int(info["sum_seconds"]))}')


def _format_time(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))


def _format_traffic(bytes: int):
    tb = 1024 * 1024 * 1024 * 1024
    gb = tb / 1024
    mb = gb / 1024
    kb = 1024
    if bytes > tb:
        return f'{bytes / tb:.2f}TB'
    if bytes > gb:
        return f'{bytes / gb:.2f}GB'
    if bytes > mb:
        return f'{bytes / mb:.2f}MB'
    if bytes > kb:
        return f'{bytes / kb:.2f}KB'
    return f'{bytes}B'
