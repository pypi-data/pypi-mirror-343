#!/usr/bin/env python3

import argparse
import json
import sys

from . import constants as c
from .cache import (
    MgcAccessToken,
    MgcAuthRecord,
    MgcCache,
    AuthRecordNotFoundError,
    get_client_id_from_alias,
    login,
    logout,
    print_tokens,
    dump_token,
    TokenType,
    foci_login,
)


def _cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mtt",
        description="Token management tools for the Microsoft Graph CLI (mgc)",
    )
    subparsers = parser.add_subparsers(dest="cmd", metavar="subcommand")

    # login subcommand
    parser_login = subparsers.add_parser(
        name="login",
        help="Login to Microsoft Graph",
    )
    parser_login.add_argument("-c", "--client-id", help="Client id to login as")
    parser_login.add_argument(
        "-s",
        "--strategy",
        default="InteractiveBrowser",
        choices=["InteractiveBrowser", "DeviceCode", "AuthToken"],
        help="Login flow type",
    )

    # logout subcommand
    subparsers.add_parser(
        name="logout",
        help="Delete the token cache and authentication record",
    )

    # list subcommand
    parser_list = subparsers.add_parser(
        name="list", help="Print all MSAL tokens currently stored in the keyring"
    )
    parser_list.add_argument(
        "-f",
        "--format",
        required=False,
        default="table",
        choices=["json", "table", "raw"],
        help="Output format",
    )

    # list-aliases subcommand
    parser_aliases = subparsers.add_parser(
        name="aliases",
        help="List alias for application client ids",
    )
    parser_aliases.add_argument(
        "-f",
        "--format",
        required=False,
        default="table",
        choices=["json", "table"],
        help="Output format",
    )

    # dump subcommand
    parser_dump = subparsers.add_parser(
        name="dump", help="Print an MSAL token from the keyring"
    )
    parser_dump.add_argument(
        "-c", "--client-id", required=False, help="Azure client id"
    )
    parser_dump.add_argument(
        "-t",
        "--token-type",
        default="access",
        choices=["access", "refresh"],
        required=False,
        help="Token type to get - either a refresh token or an access token",
    )

    # refresh-to subcommand
    parser_refresh = subparsers.add_parser(
        name="refresh-to",
        help="Pass a refresh token or use an existing cached refresh token to login to another foci client",
    )
    parser_refresh.add_argument(
        "-c", "--client-id", required=True, help="Client id to login as"
    )

    # insert subcommand
    parser_insert = subparsers.add_parser(
        name="insert",
        help="Insert a token aquired through other means into the token cache",
    )
    parser_insert.add_argument(
        "-s",
        "--secret",
        default=(None if sys.stdin.isatty() else sys.stdin.readline().rstrip()),
        required=False,
        help="",
    )

    # status subcommand
    subparsers.add_parser(
        name="status",
        help="Print current client_id and tenant_id",
    )

    # switch-client subcommand
    parser_switch = subparsers.add_parser(
        name="switch",
        help="Switch to another client with available access tokens",
    )
    parser_switch.add_argument(
        "-c", "--client-id", required=True, help="Client id to login as"
    )

    return parser


def main():
    args = _cli().parse_args()
    if args.cmd:
        # initialize auth record
        try:
            auth_record = MgcAuthRecord()
        except AuthRecordNotFoundError as e:
            if args.cmd in ["login", "logout"]:
                auth_record = None
            else:
                print(f"Error: {e}")
                exit(1)

        # check if client-id is an alias
        try:
            if args.client_id is not None:
                args.client_id = (
                    get_client_id_from_alias(args.client_id) or args.client_id
                )
            else:
                if auth_record is not None:
                    args.client_id = auth_record.client_id
        except AttributeError:
            # args.client_id is not a valid argument for this subcommand
            pass

        # match command
        match args.cmd:
            case "login":
                if args.client_id:
                    login(client_id=args.client_id, strategy=args.strategy)
                else:
                    login()

            case "list":
                print_tokens(args.format)

            case "aliases":
                if args.format == "json":
                    print(json.dumps(c.CLIENT_ALIASES, indent=2))
                else:
                    print(f"{'alias': <20} {'display_name': <30}")
                    for a in c.CLIENT_ALIASES:
                        print(f"{a['alias']: <20} {a['display_name']: <30}")

            case "logout":
                logout()
                print("Logged out.")

            case "dump":
                if args.token_type == "refresh":
                    token_type = TokenType.REFRESH
                else:
                    token_type = TokenType.ACCESS

                print(dump_token(client_id=args.client_id, token_type=token_type))

            case "refresh-to":
                if auth_record is not None:
                    r = foci_login(
                        refresh_token_client_id=auth_record.client_id,
                        new_client_id=args.client_id,
                        tenant_id=auth_record.tenant_id,
                    )
                    m = MgcCache()
                    m.insert_refresh_response(response=r)

            case "insert":
                MgcCache().insert_token(args.secret)

            case "status":
                status = auth_record.__dict__
                token = MgcCache().get_token(status["client_id"])
                if type(token) is MgcAccessToken:
                    status["scopes"] = token.scopes
                print(json.dumps(status, indent=2))

            case "switch":
                cache = MgcCache()
                token = cache.get_token(args.client_id)
                if token is not None:
                    if type(token) is MgcAccessToken:
                        auth_record = MgcAuthRecord._from_access_token(token)
                else:
                    print(f"No valid access token for client_id={args.client_id}")

            case _:
                print("The command specified is not valid.")

    else:
        _cli().print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
