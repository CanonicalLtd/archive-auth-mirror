"""Manage users for repository access through basic authentication."""

import subprocess
import argparse

from ..utils import get_paths


def add_user(auth_file, user, passwd):
    """Add a user."""
    subprocess.run(
        ['htpasswd', '-i', str(auth_file), user],
        input=passwd.encode('utf8'), stderr=subprocess.DEVNULL,
        check=True)


def list_users(auth_file):
    """List existing users."""
    if not auth_file.exists():
        return []
    with auth_file.open() as fh:
        return [line.split(':')[0] for line in fh]


def remove_user(auth_file, user):
    """Remove a user."""
    subprocess.check_call(
        ['htpasswd', '-D', str(auth_file), user],
        stderr=subprocess.DEVNULL)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='action', help='action to perform')
    subparsers.required = True

    add_action = subparsers.add_parser(
        'add',
        help='add a user. If the user exists, their password is updated')
    add_action.add_argument('user', help='the username to add')
    add_action.add_argument('password', help='the password for the user')

    subparsers.add_parser('list', help='list users')

    remove_action = subparsers.add_parser('remove', help='remove a user')
    remove_action.add_argument('user', help='the user to remove')

    return parser


def main():
    args = get_parser().parse_args()
    auth_file = get_paths()['basic-auth']

    if args.action == 'add':
        add_user(auth_file, args.user, args.password)
    elif args.action == 'remove':
        remove_user(auth_file, args.user)
    elif args.action == 'list':
        for user in list_users(auth_file):
            print(user)
