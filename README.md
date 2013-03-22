# Dropbox CLI Uploader

I made this little python script to backup edited videos to a Dropbox's folder from a workstation where i don't want to install the desktop software.

Take into account that if you run this in a computer that has that dropbox account installed, you should ignore the 'App/cli upload' folder in Preferences | Advanced | Selective Sync to avoid syncronization.

# Installation

```bash
pip install https://github.com/drkloc/dropboxcli.git
```

# Usage

```bash
dropboxcli <path_to_file>
```