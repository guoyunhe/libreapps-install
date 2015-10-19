#!/usr/bin/env python

__author__ = "Guo Yunhe <guoyunhebrave@gmail.com>"
__date__ = "$2015-10-17 14:36:39$"

import dbus
import argparse
import platform

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='URL of one click package installation')
    args = parser.parse_args()
    url = args.url
    
    # check distro info
    (distname, version, id) = platform.linux_distribution()
    
    # parse packages
    patterns = url[8:].split('&')
    
    ## general packages
    packages = patterns[0].split(',')
    
    ## distro-specified packages
    distname_prefix = distname.strip().lower() + '='
    for pattern in patterns:
        if pattern.find(distname_prefix) == 0:
            packages = pattern.replace(distname_prefix, '').split(',')
    
    ## distro-version-specified packages
    distname_version_prefix = distname.strip().lower() + ':' + version.strip().lower() + '='
    for pattern in patterns:
        if distname_version_prefix in pattern:
            packages = pattern.replace(distname_version_prefix, '').split(',')
        
    try:
        bus = dbus.SessionBus()
    except dbus.DBusException, e:
        print 'PackageKit Connection Expception: %s' % str(e)
        sys.exit()
    try:
        proxy = bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit')
        iface = dbus.Interface(proxy, 'org.freedesktop.PackageKit.Modify')
        iface.InstallPackageNames(dbus.UInt32(0), packages, "show-confirm-search,hide-finished")
    except dbus.DBusException, e:
        print 'PackageKit Exception: %s' % str(e)
