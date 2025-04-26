# mgc-token-tools
> Token management tools for the Microsoft Graph CLI (`mgc`)

!WIP! - This project is a work-in-progress and may not be functional. 

## Features
- Print an access or refresh token from the OS keyring for a specific client (via the client id) to pass to another tool
- [FOCI client](https://github.com/secureworks/family-of-client-ids-research/tree/main) login similar to `Invoke-RefreshTo<X>` commands provided by [TokenTactics](https://github.com/rvrsh3ll/TokenTactics)
- Store a correctly-formatted access or refresh token sourced outside `mgc` in the `mgc` token cache
- Provides aliases for useful first-party Microsoft clients


## Installation & Requirements
The script has no external *python* dependencies, but does use the [security](https://ss64.com/mac/security.html) command on MacOS or [secret-tool](https://manpages.ubuntu.com/manpages/mantic/man1/secret-tool.1.html) on Linux for keyring access. 

One option for installation is to download the script and save it to some folder in your $PATH.
```
#!/bin/bash

wget https://raw.githubusercontent.com/petergs/mgc-token-tools/refs/heads/main/mgc-token-tools -O ~/.local/bin/mgc-token-tools   

```

## Keyring Support
So far, this has been tested with MacOS Keychain and GNOME Keyring on Linux.
