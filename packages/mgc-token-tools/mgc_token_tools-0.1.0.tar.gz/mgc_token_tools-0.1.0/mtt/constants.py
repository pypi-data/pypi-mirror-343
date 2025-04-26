MSAL_KEYRING_ACCOUNT = "MicrosoftGraph.nocae"
MSAL_KEYRING_LABEL = "MsalClientID"
MSAL_KEYRING_SERVICE = "Microsoft.Developer.IdentityService"
MS_GRAPH_API_BASE_URL = "https://graph.microsoft.com"
MSO_LOGIN_URL = "https://login.microsoftonline.com"
MSO_AUTHORIZE_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MSO_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
AUTH_CODE_REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
ENVIRONMENT_DOMAIN = "login.windows.net"

LOGIN_CMD = "mgc login --client-id {client_id} --strategy {strategy}"
LOGOUT_CMD = "mgc logout"
MS_AZURE_POWERSHELL_CLIENT_ID = "1950a258-227b-4e31-a9cf-717495945fc2"

# from https://github.com/secureworks/family-of-client-ids-research/blob/main/known-foci-clients.csv
FOCI_CLIENTS = [
    {
        "client_id": "1950a258-227b-4e31-a9cf-717495945fc2",
        "app_name": "Microsoft Azure PowerShell",
    },
    {
        "client_id": "00b41c95-dab0-4487-9791-b9d2c32c80f2",
        "app_name": "Office 365 Management",
    },
    {
        "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
        "app_name": "Microsoft Azure CLI",
    },
    {
        "client_id": "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
        "app_name": "Microsoft Teams",
    },
    {
        "client_id": "26a7ee05-5602-4d76-a7ba-eae8b7b67941",
        "app_name": "Windows Search",
    },
    {
        "client_id": "27922004-5251-4030-b22d-91ecd9a37ea4",
        "app_name": "Outlook Mobile",
    },
    {
        "client_id": "4813382a-8fa7-425e-ab75-3b753aab3abb",
        "app_name": "Microsoft Authenticator App",
    },
    {
        "client_id": "ab9b8c07-8f02-4f72-87fa-80105867a763",
        "app_name": "OneDrive SyncEngine",
    },
    {
        "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
        "app_name": "Microsoft Office",
    },
    {
        "client_id": "872cd9fa-d31f-45e0-9eab-6e460a02d1f1",
        "app_name": "Visual Studio",
    },
    {
        "client_id": "af124e86-4e96-495a-b70a-90f90ab96707",
        "app_name": "OneDrive iOS App",
    },
    {
        "client_id": "2d7f3606-b07d-41d1-b9d2-0d0c9296a6e8",
        "app_name": "Microsoft Bing Search for Microsoft Edge",
    },
    {
        "client_id": "844cca35-0656-46ce-b636-13f48b0eecbd",
        "app_name": "Microsoft Stream Mobile Native",
    },
    {
        "client_id": "87749df4-7ccf-48f8-aa87-704bad0e0e16",
        "app_name": "Microsoft Teams - Device Admin Agent",
    },
    {
        "client_id": "cf36b471-5b44-428c-9ce7-313bf84528de",
        "app_name": "Microsoft Bing Search",
    },
    {
        "client_id": "0ec893e0-5785-4de6-99da-4ed124e5296c",
        "app_name": "Office UWP PWA",
    },
    {
        "client_id": "22098786-6e16-43cc-a27d-191a01a1e3b5",
        "app_name": "Microsoft To-Do client",
    },
    {"client_id": "4e291c71-d680-4d0e-9640-0a3358e31177", "app_name": "PowerApps"},
    {
        "client_id": "57336123-6e14-4acc-8dcf-287b6088aa28",
        "app_name": "Microsoft Whiteboard Client",
    },
    {
        "client_id": "57fcbcfa-7cee-4eb1-8b25-12d2030b4ee0",
        "app_name": "Microsoft Flow",
    },
    {
        "client_id": "66375f6b-983f-4c2c-9701-d680650f588f",
        "app_name": "Microsoft Planner",
    },
    {
        "client_id": "9ba1a5c7-f17a-4de9-a1f1-6178c8d51223",
        "app_name": "Microsoft Intune Company Portal",
    },
    {
        "client_id": "a40d7d7d-59aa-447e-a655-679a4107e548",
        "app_name": "Accounts Control UI",
    },
    {
        "client_id": "a569458c-7f2b-45cb-bab9-b7dee514d112",
        "app_name": "Yammer iPhone",
    },
    {"client_id": "b26aadf8-566f-4478-926f-589f601d9c74", "app_name": "OneDrive"},
    {
        "client_id": "c0d2a505-13b8-4ae0-aa9e-cddd5eab0b12",
        "app_name": "Microsoft Power BI",
    },
    {"client_id": "d326c1ce-6cc6-4de2-bebc-4591e5e13ef0", "app_name": "SharePoint"},
    {
        "client_id": "e9c51622-460d-4d3d-952d-966a5b1da34c",
        "app_name": "Microsoft Edge",
    },
    {
        "client_id": "eb539595-3fe1-474e-9c1d-feb3625d1be5",
        "app_name": "Microsoft Tunnel",
    },
    {
        "client_id": "ecd6b820-32c2-49b6-98a6-444530e5a77a",
        "app_name": "Microsoft Edge",
    },
    {
        "client_id": "f05ff7c9-f75a-4acd-a3b5-f4b6a870245d",
        "app_name": "SharePoint Android",
    },
    {
        "client_id": "f44b1140-bc5e-48c6-8dc0-5cf5a53c0e34",
        "app_name": "Microsoft Edge",
    },
    {
        "client_id": "be1918be-3fe3-4be9-b32b-b542fc27f02e",
        "app_name": "M365 Compliance Drive Client",
    },
    {
        "client_id": "cab96880-db5b-4e15-90a7-f3f1d62ffe39",
        "app_name": "Microsoft Defender Platform",
    },
    {
        "client_id": "d7b530a4-7680-4c23-a8bf-c52c121d2e87",
        "app_name": "Microsoft Edge Enterprise New Tab Page",
    },
    {
        "client_id": "dd47d17a-3194-4d86-bfd5-c6ae6f5651e3",
        "app_name": "Microsoft Defender for Mobile",
    },
    {
        "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
        "app_name": "Outlook Lite",
    },
]

# -- Cli --
CLIENT_ALIASES = [
    {
        "alias": "msteams",
        "display_name": "Microsoft Teams",
        "client_id": "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
        "interactive_login": True,
        "redirect_type": "nativeclient",
        "foci": True,
    },
    {
        "alias": "onedrive",
        "display_name": "OneDrive SyncEngine",
        "client_id": "ab9b8c07-8f02-4f72-87fa-80105867a763",
        "interactive_login": True,
        "redirect_type": "nativeclient",
        "foci": True,
    },
    {
        "alias": "msoffice",
        "display_name": "Microsoft Office",
        "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
        "interactive_login": False,
        "foci": True,
    },
    {
        "alias": "outlook",
        "display_name": "Outlook Mobile",
        "client_id": "27922004-5251-4030-b22d-91ecd9a37ea4",
        "interactive_login": False,
        "foci": True,
    },
    {
        "alias": "azcli",
        "display_name": "Microsoft Azure CLI",
        "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
        "interactive_login": True,
        "redirect_type": "localhost",
        "foci": True,
    },
    {
        "alias": "azpowershell",
        "display_name": "Microsoft Azure PowerShell",
        "client_id": "1950a258-227b-4e31-a9cf-717495945fc2",
        "interactive_login": True,
        "redirect_type": "localhost",
        "foci": True,
    },
    {
        "alias": "vs",
        "display_name": "Visual Studio - Legacy",
        "client_id": "872cd9fa-d31f-45e0-9eab-6e460a02d1f1",
        "interactive_login": True,
        "redirect_type": "localhost",
        "foci": True,
    },
]
