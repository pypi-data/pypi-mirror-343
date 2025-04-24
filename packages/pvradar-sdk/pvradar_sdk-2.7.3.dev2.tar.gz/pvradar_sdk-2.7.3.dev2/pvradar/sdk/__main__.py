from getpass import getpass
import argparse

from .common.exceptions import PvradarSdkError
from .caching.caching_factory import make_kv_storage
from .caching.kv_storage.kv_storage_with_expiration_adaptor import KVStorageWithExpirationAdaptor
from .common.settings import SdkSettings
from .client.client import PvradarClient
from . import __version__

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='pvradar.sdk', description='CLI for pvradar SDK', usage='python -m pvradar.sdk [-hv] {command}'
    )

    truncate_choice = 'cache_truncate'
    clean_expired_choice = 'cache_clean_expired'
    api_key_choice = 'api_key'
    command_choices = [truncate_choice, clean_expired_choice, api_key_choice]

    parser.add_argument('command', choices=command_choices)

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument(
        '--disable-httpx-verify',
        action='store_true',
        help='set verify=False when making requests with httpx',
    )
    args = parser.parse_args()
    if args.command == truncate_choice:
        make_kv_storage(settings=SdkSettings.instance()).truncate()
        print('cache truncated')
    elif args.command == clean_expired_choice:
        kv_storage = make_kv_storage(settings=SdkSettings.instance())
        if isinstance(kv_storage, KVStorageWithExpirationAdaptor):
            print(f'{kv_storage.clean_expired()} expired keys removed')
        else:
            raise NotImplementedError(
                f'Command {clean_expired_choice} is not supported for {kv_storage}.'
                f' It should be a subclass of KVStorageWithExpirationAdaptor'
            )
    elif args.command == api_key_choice:
        try:
            print('args', args)
            api_key = getpass('Enter your API key or press Ctrl+C to cancel: ')
            PvradarClient.set_api_key(api_key, disable_httpx_verify=args.disable_httpx_verify)
            print('API key set successfully!')
        except KeyboardInterrupt:
            print('\nAPI key setting cancelled by user')
            exit(130)
        except PvradarSdkError as e:
            print(f'Error: {e}')
            exit(1)
    else:
        raise ValueError(f'Unexpected command: {args.command}. Expected one of {command_choices}')
