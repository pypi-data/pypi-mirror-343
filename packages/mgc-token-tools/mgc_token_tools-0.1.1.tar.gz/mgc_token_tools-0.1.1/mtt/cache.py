import base64
import binascii
import json
import pathlib
import platform
import shlex
import sys
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from subprocess import PIPE, STDOUT, run
from typing import Literal, Protocol, Self

from . import constants as c
from .utils import urlreq


# -- Cache and keychain interface classes --
class TokenType(Enum):
    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    REFRESH = "RefreshToken"
    ACCESS = "AccessToken"
    ID = "IdToken"


class MgcCacheItem(Protocol):
    @property
    def key(self) -> str: ...

    def as_cache_dict(self) -> dict: ...

    @classmethod
    def init_from_cache(cls, item: dict) -> Self: ...


@dataclass
class MgcToken(MgcCacheItem):
    tenant_id: str
    user_id: str
    client_id: str
    secret: str

    @property
    def token_type(self) -> str:
        return self.__class__.__name__.replace("Mgc", "")

    @property
    def home_account_id(self) -> str:
        return f"{self.user_id}.{self.tenant_id}"

    @property
    def client_info(self) -> str:
        return (
            base64.urlsafe_b64encode(
                str({"uid": self.user_id, "tid": self.tenant_id}).encode()
            )
            .decode()
            .rstrip("=")
        )

    @classmethod
    def init_from_cache(cls, item: dict):
        user_id = item["home_account_id"].split(".")[0]
        tenant_id = item["home_account_id"].split(".")[1]
        return cls(
            tenant_id=tenant_id,
            client_id=item["client_id"],
            user_id=user_id,
            secret=item["secret"],
        )

    def as_cache_dict(self) -> dict:
        cache_entry = {
            "home_account_id": self.home_account_id,
            "environment": c.ENVIRONMENT_DOMAIN,
            "client_info": self.client_info,
            "client_id": self.client_id,
            "secret": self.secret,
            "credential_type": self.token_type,
            "realm": self.tenant_id,
        }
        return cache_entry

    def json(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "type": self.token_type,
            "client_id": self.client_id,
        }


@dataclass
class MgcAccessToken(MgcToken, MgcCacheItem):
    scopes: list[str]

    @property
    def jwt_claims(self) -> dict:
        return _parse_jwt_claims(self.secret)

    @property
    def username(self) -> str | None:
        return self.jwt_claims["upn"]

    @property
    def issued_at(self) -> int | None:
        return int(self.jwt_claims["iat"])

    @property
    def expires_on(self) -> int | None:
        return int(self.jwt_claims["exp"])

    @property
    def key(self) -> str:
        return f"{self.home_account_id}-{c.ENVIRONMENT_DOMAIN}-{TokenType.ACCESS.value}-{self.client_id}-{self.tenant_id}-{' '.join(self.scopes)}".lower()

    @classmethod
    def init_from_cache(cls, item: dict):
        user_id = item["home_account_id"].split(".")[0]
        tenant_id = item["home_account_id"].split(".")[1]
        claims = _parse_jwt_claims(item["secret"])
        scopes = claims["scp"].split(" ")
        return MgcAccessToken(
            tenant_id=tenant_id,
            client_id=item["client_id"],
            user_id=user_id,
            secret=item["secret"],
            scopes=scopes,
        )

    @classmethod
    def init_from_secret(cls, secret: str):
        claims = _parse_jwt_claims(secret)
        return MgcAccessToken(
            tenant_id=claims["tid"],
            client_id=claims["appid"],
            user_id=claims["oid"],
            secret=secret,
            scopes=claims["scp"].split(" "),
        )

    def as_cache_dict(self) -> dict[str, str]:
        cache_entry = {
            "home_account_id": self.home_account_id,
            "environment": c.ENVIRONMENT_DOMAIN,
            "client_info": self.client_info,
            "client_id": self.client_id,
            "secret": self.secret,
            "credential_type": self.token_type,
            "realm": self.tenant_id,
            "target": " ".join(self.scopes),
            "cached_at": str(self.issued_at),
            "expires_on": str(self.expires_on),
            "extended_expires_on": str(self.expires_on),
            "ext_expires_on": str(self.expires_on),
        }
        return cache_entry


@dataclass
class MgcRefreshToken(MgcToken, MgcCacheItem):
    family_id: int  # foci = 1

    @property
    def _key(self) -> str:
        return f"{self.home_account_id}-{c.ENVIRONMENT_DOMAIN}-{TokenType.REFRESH.value}-{self.family_id}--".lower()

    @property
    def key(self) -> str:
        return f"{self.home_account_id}-{c.ENVIRONMENT_DOMAIN}-{TokenType.ID.value}-{self.client_id}-{self.tenant_id}-".lower()

    @classmethod
    def init_from_cache(cls, item: dict):
        user_id = item["home_account_id"].split(".")[0]
        tenant_id = item["home_account_id"].split(".")[1]
        return MgcRefreshToken(
            tenant_id=tenant_id,
            client_id=item["client_id"],
            user_id=user_id,
            secret=item["secret"],
            family_id=item["family_id"],
        )

    def as_cache_dict(self) -> dict:
        cache_entry = {
            "home_account_id": self.home_account_id,
            "environment": c.ENVIRONMENT_DOMAIN,
            "client_info": self.client_info,
            "client_id": self.client_id,
            "secret": self.secret,
            "credential_type": self.token_type,
            "family_id": str(self.family_id),
        }
        return cache_entry


@dataclass
class MgcIdToken(MgcToken, MgcCacheItem):
    @property
    def jwt_claims(self) -> dict:
        return _parse_jwt_claims(self.secret)

    @property
    def username(self) -> str | None:
        return self.jwt_claims["preferred_username"]

    @property
    def key(self) -> str:
        return f"{self.home_account_id}-{c.ENVIRONMENT_DOMAIN}-{TokenType.ID.value}-{self.client_id}-{self.tenant_id}-".lower()

    @classmethod
    def init_from_secret(cls, secret: str, client_id: str):
        claims = _parse_jwt_claims(secret)
        return MgcIdToken(
            tenant_id=claims["tid"],
            user_id=claims["oid"],
            client_id=client_id,
            secret=secret,
        )


class RefreshResponse:
    def __init__(self, response: dict):
        self.token_type: str = response["token_type"]  # Bearer
        self.scope: str = response["scope"]
        self.expires_in: str = response["expires_in"]
        self.ext_expires_in: str = response["ext_expires_in"]
        self.expires_on: str | None = response.get("expires_on")
        self.not_before: str | None = response.get("not_before")
        self.resource: str | None = response.get(
            "resource"
        )  # https://graph.microsoft.com
        self.access_token: MgcAccessToken = MgcAccessToken.init_from_secret(
            response["access_token"]
        )
        self.foci: int = int(response["foci"])
        self.id_token: MgcIdToken = MgcIdToken(
            tenant_id=self.access_token.tenant_id,
            user_id=self.access_token.user_id,
            secret=response["id_token"],
            client_id=self.access_token.client_id,
        )
        self.refresh_token: MgcRefreshToken = MgcRefreshToken(
            tenant_id=self.access_token.tenant_id,
            user_id=self.access_token.user_id,
            client_id=self.access_token.client_id,
            secret=response["refresh_token"],
            family_id=self.foci,
        )


def _client_id_to_name(client_id: str) -> str | None:
    for client in c.FOCI_CLIENTS:
        if client_id == client["client_id"]:
            return client["app_name"]


class MgcAuthRecord:
    def __init__(self):
        home = pathlib.Path.home()
        try:
            with open(f"{home}/.mgc/authRecord", "r") as f:
                auth_record = "\n".join(f.readlines())
                auth_record = json.loads(auth_record)
        except FileNotFoundError:
            raise AuthRecordNotFoundError()

        self.username: str = auth_record["username"]
        self.authority: str = auth_record["authority"]
        self.tenant_id: str = auth_record["tenantId"]
        self.client_id: str = auth_record["clientId"]
        self.user_id: str = auth_record["homeAccountId"].split(".")[0]
        self.app_name: str | None = _client_id_to_name(self.client_id)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def _commit_auth_record(self) -> None:
        ar = {
            "username": self.username,
            "authority": self.authority,
            "homeAccountId": f"{self.user_id}.{self.tenant_id}",
            "tenantId": self.tenant_id,
            "clientId": self.client_id,
            "version": "1.0",
        }
        home = pathlib.Path.home()
        try:
            with open(f"{home}/.mgc/authRecord", "w") as f:
                f.write(json.dumps(ar))
        except FileNotFoundError:
            raise AuthRecordNotFoundError()

    @classmethod
    def _from_access_token(cls, token: MgcAccessToken) -> None:
        ar = {
            "username": token.username,
            "authority": "login.microsoftonline.com",
            "homeAccountId": f"{token.user_id}.{token.tenant_id}",
            "tenantId": token.tenant_id,
            "clientId": token.client_id,
            "version": "1.0",
        }
        home = pathlib.Path.home()
        try:
            with open(f"{home}/.mgc/authRecord", "w") as f:
                f.write(json.dumps(ar))
        except FileNotFoundError:
            raise AuthRecordNotFoundError()


class AuthRecordNotFoundError(Exception):
    def __init__(
        self, message: str = "AuthRecord not found. Try using the login command first."
    ):
        super().__init__(message)


class MgcCache:
    """
    Token and app storage for mgc

    Stored (using OS keychain functionality) as a dictionary with the following
    top level keys: [AccessToken, RefreshToken, IdToken, Account, AppMetadata]
    which are represented in the MgcCacheItemType Enum.
    """

    def __init__(self):
        if platform.system() == "Linux":
            find_cmd = (
                f"secret-tool lookup {c.MSAL_KEYRING_LABEL} {c.MSAL_KEYRING_SERVICE}"
            )
            output = run(shlex.split(find_cmd), stdout=PIPE, stderr=STDOUT)
            cache = base64.urlsafe_b64decode(output.stdout.decode()).decode("utf-8")
            cache = json.loads(cache)
        elif platform.system() == "Darwin":
            find_cmd = (
                f'security find-generic-password -w -a "{c.MSAL_KEYRING_ACCOUNT}"'
            )
            output = run(shlex.split(find_cmd), stdout=PIPE, stderr=STDOUT)
            try:
                cache = json.loads(output.stdout.decode())
            except json.decoder.JSONDecodeError:
                if "SecKeychainSearchCopyNext" in output.stdout.decode():
                    # Create an empty keychain entry
                    cache = {
                        "AccessToken": {},
                        "RefreshToken": {},
                        "IdToken": {},
                    }
                else:
                    print(f"Error: {output.stdout.decode()}")
                    sys.exit(1)
        else:
            print(f"Error: Unsupported platform {platform.system()}")
            sys.exit(1)

        if cache is None:
            sys.exit(1)

        self.content: dict = cache

    @property
    def tokens(self) -> list[MgcToken]:
        result = []
        for _, v in self.content["AccessToken"].items():
            token = MgcAccessToken.init_from_cache(v)
            result.append(token)

        for _, v in self.content["RefreshToken"].items():
            token = MgcRefreshToken.init_from_cache(v)
            result.append(token)

        for _, v in self.content["IdToken"].items():
            token = MgcIdToken.init_from_cache(v)
            result.append(token)

        result.sort(key=lambda x: x.tenant_id + x.client_id)

        return result

    @property
    def refresh_count(self) -> int:
        return sum(1 for i in self.tokens if i.token_type == TokenType.REFRESH.value)

    def _commit(self) -> None:
        # For some reason, keychain access will prompt for a keychain password for future mgc calls
        # after modifying the token. Even with usage of the -T parameter to update the keychain item's
        # ACL to include mgc.

        if platform.system() == "Darwin":
            add_cmd = f"security add-generic-password -a '{c.MSAL_KEYRING_ACCOUNT}' -s '{c.MSAL_KEYRING_SERVICE}' -w '{json.dumps(self.content)}' -U"  # -T '{mgc_path}"
            add_output = run(shlex.split(add_cmd), stdout=PIPE, stderr=STDOUT)
            print(add_output.stdout.decode())

    @classmethod
    def clear(cls) -> None:
        if platform.system() == "Darwin":
            cmd = f"security delete-generic-password -a '{c.MSAL_KEYRING_ACCOUNT}' -s '{c.MSAL_KEYRING_SERVICE}'"
        elif platform.system() == "Linux":
            cmd = ""
        else:
            print(f"Error: unsupported platform {platform.system()} for `clear`")
            sys.exit(1)
        output = run(shlex.split(cmd), stdout=PIPE, stderr=STDOUT)
        print(output.stdout.decode())

    def insert_token(
        self, secret: str, token_type: TokenType = TokenType.ACCESS
    ) -> None:
        if token_type == TokenType.ACCESS:
            token = MgcAccessToken.init_from_secret(secret)
            self.content[token.token_type][token.key] = token.as_cache_dict()
            self._commit()
        else:
            print("Error: currently only access tokens are supported by this function.")
            sys.exit(1)

    def insert_refresh_response(self, response: RefreshResponse) -> None:
        self.content[TokenType.ACCESS.value][response.access_token.key] = (
            response.access_token.as_cache_dict()
        )
        self.content[TokenType.REFRESH.value][response.refresh_token.key] = (
            response.refresh_token.as_cache_dict()
        )
        self.content[TokenType.ID.value][response.id_token.key] = (
            response.id_token.as_cache_dict()
        )
        self._commit()

    def get_token(
        self, client_id: str, token_type: TokenType = TokenType.ACCESS
    ) -> MgcToken | None:
        for token in self.tokens:
            if token.client_id == client_id and token.token_type == token_type.value:
                return token


# -- Utlities --
def _parse_jwt_claims(jwt: str) -> dict:
    # split out claims from jwt and base64 decode into a dictoinary
    claims = jwt.split(".")[1]  # split jwt
    try:
        claims = base64.urlsafe_b64decode(claims).decode()
    except binascii.Error:  # incorrect padding
        claims = base64.b64decode(claims + "==").decode()
    return json.loads(claims)


def _token_type_from_key(
    t: Literal["AccessToken", "RefreshToken", "IdToken"],
) -> TokenType:
    match t:
        case "AccessToken":
            return TokenType.ACCESS
        case "RefreshToken":
            return TokenType.REFRESH
        case "IdToken":
            return TokenType.ID


def print_tokens(format: str) -> None:
    cache = MgcCache()
    if format == "raw":
        tokens = cache.content
        print(json.dumps(tokens, indent=2))
    else:
        tokens = [token.json() for token in cache.tokens]
        if format == "json":
            for token in tokens:
                print(json.dumps(token, indent=2))
        else:
            print(
                f"{'#': <5} {'tenant_id': <40} {'type': <20} {'client_id': <40} {'alias': <40}"
            )
            for i, token in enumerate(tokens):
                alias = get_alias(token["client_id"]) or ""
                print(
                    f"{i: <5} {token['tenant_id']: <40} {token['type']: <20} {token['client_id']: <40} {alias: <40}"
                )


def run_mgc_cmd(cmd: str, env=None) -> dict | None:
    output = run(shlex.split(cmd), stdout=PIPE, stderr=STDOUT, env=env)
    if output.returncode != 0:
        print(output.stdout.decode())
        return None
    else:
        if output.stdout.decode() == "":
            # For commands that dont output to stdout (ex: mgc login)
            return None
        else:
            try:
                result = json.loads(output.stdout.decode())["value"]
                return result
            except KeyError:
                result = json.loads(output.stdout.decode())
                return result


def login(
    client_id=c.MS_AZURE_POWERSHELL_CLIENT_ID, strategy="InteractiveBrowser", beta=False
) -> None:
    if beta:
        version = "-beta"
    else:
        version = ""
    if strategy in ["InteractiveBrowser", "interactive", "device_code"]:
        run_mgc_cmd(
            c.LOGIN_CMD.format(version=version, client_id=client_id, strategy=strategy)
        )
    else:
        auth_token_login(client_id)


def logout() -> None:
    run_mgc_cmd(c.LOGOUT_CMD)
    MgcCache.clear()


def auth_token_flow(client_id, scope, auth_code) -> RefreshResponse:
    data = {
        "client_id": client_id,
        "redirect_uri": c.AUTH_CODE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "scope": scope,
        "code": auth_code,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }

    r = urlreq("POST", c.MSO_TOKEN_URL, headers=headers, data=data)
    r = RefreshResponse(json.loads(r))
    return r


def auth_token_login(client_id) -> None:
    print()
    scope = "openid offline_access"
    resource = "https://graph.microsoft.com/.default"
    data = {
        "client_id": client_id,
        "scope": f"{scope} {resource}",
        "response_type": "code",
        "redirect_uri": c.AUTH_CODE_REDIRECT_URI,
    }
    params = "&".join(
        "{}={}".format(k, urllib.parse.quote_plus(v)) for k, v in data.items()
    )
    print(f"{c.MSO_AUTHORIZE_URL}?{params}")
    response = input("Enter the url of the response page:\n")
    parsed_query_string = urllib.parse.parse_qs(urllib.parse.urlparse(response).query)
    code = parsed_query_string.get("code")
    if code is not None:
        code = code[0]
        print(code)
        r = auth_token_flow(client_id, f"{scope} {resource}", code)
        MgcCache().insert_refresh_response(r)


def dump_token(client_id: str, token_type: TokenType = TokenType.ACCESS) -> str:
    """
    Returns the first available MSAL token if multiple apps have been logged into
    and no client_id is specified. Otherwise, it will return the token for the specified
    client_id if it exists.
    """
    cache = MgcCache()
    secret = None

    tokens = [token for token in cache.tokens if token_type.value == token.token_type]
    if len(tokens) == 1 and client_id is None:
        secret = tokens[0].secret
    for item in tokens:
        if client_id == item.client_id:
            secret = item.secret

    if secret is None:
        print(
            f"Error: No {token_type.value} tokens found for client-id={client_id} (alias={get_alias(client_id)})"
        )
        sys.exit(1)
    else:
        return secret


def foci_login(
    new_client_id: str,
    tenant_id: str,
    refresh_token: str | None = None,
    refresh_token_client_id: str | None = None,
) -> RefreshResponse:
    """
    Use a refresh token present in the MSAL keyring entry to login as another foci app
    """
    foci_client_ids = [x["client_id"] for x in c.FOCI_CLIENTS]
    if refresh_token is None and refresh_token_client_id is None:
        print(
            "Error: foci_login expects either a refresh_token or a refresh_token_client_id"
        )
        sys.exit(1)

    if not refresh_token:
        if refresh_token_client_id in foci_client_ids:
            refresh_token = dump_token(
                refresh_token_client_id, token_type=TokenType.REFRESH
            )
        else:
            print(
                f"Error: The value supplied for refresh_token_client_id ({refresh_token_client_id}) is not a known foci client."
            )

    if new_client_id in foci_client_ids:
        payload = {
            "resource": c.MS_GRAPH_API_BASE_URL,
            "client_id": new_client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "openid",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }
        r = urlreq(
            method="POST",
            url=f"{c.MSO_LOGIN_URL}/{tenant_id}/oauth2/token",
            headers=headers,
            data=payload,
        )
        return RefreshResponse(response=json.loads(r))
    else:
        print(
            f"Error: The value supplied for new_client_id ({new_client_id}) is not a known foci client."
        )
        sys.exit(1)


def get_alias(client_id: str) -> str | None:
    for a in c.CLIENT_ALIASES:
        if a["client_id"] == client_id:
            return a["alias"]
    else:
        return None


def get_client_id_from_alias(alias: str) -> str | None:
    for a in c.CLIENT_ALIASES:
        if a["alias"] == alias:
            return a["client_id"]
    else:
        return None
