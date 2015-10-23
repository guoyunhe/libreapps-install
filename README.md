# libreapps-install
LibreApps client, handle "install:" protocol and call PackageKit.

## Note for GNOME users

This package will be set as default application to open "install:package1,package2" custom url. In GNOME, it is implemented by a post-install script, which will detect if GNOME is installed. If you install GNOME after installing this package, you need to reinstall this package.
