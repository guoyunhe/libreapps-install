#!/usr/bin/env python2

__author__ = "Guo Yunhe <guoyunhebrave@gmail.com>"
__date__ = "$2015-10-17 14:36:39$"

import dbus
import argparse
import os.path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='URL of one click package installation')
    args = parser.parse_args()
    url = args.url
    
    # parse packages
    patterns = url[8:].split('&')
    
    ## general packages
    packages = patterns[0].split(',')
    
    # check distro info
    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as release_file:
            for line in release_file:
                name, var = line.partition("=")[::2]
                if name.strip() == 'ID':
                    dist_name = var.strip()
                elif name.strip() == 'VERSION_ID':
                    dist_version = var.replace('"', '').strip()
        print dist_name, dist_version
        ## distro-specified packages
        dist_prefix = dist_name + '='
        for pattern in patterns:
            if pattern.find(dist_prefix) == 0:
                packages = pattern.replace(dist_prefix, '').split(',')

        ## distro-version-specified packages
        dist_prefix = dist_name + ':' + dist_version + '='
        for pattern in patterns:
            if pattern.find(dist_prefix) == 0:
                packages = pattern.replace(dist_prefix, '').split(',')
    else:
        print 'unknown ditribution'

    try:
        bus = dbus.SessionBus()
    except dbus.DBusException, e:
        print 'PackageKit Connection Expception: %s' % str(e)
        exit()
    try:
        proxy = bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit')
        iface = dbus.Interface(proxy, 'org.freedesktop.PackageKit.Modify')
        iface.InstallPackageNames(dbus.UInt32(0), packages, "show-confirm-search,hide-finished")
    except dbus.DBusException, e:
        print 'PackageKit Exception: %s' % str(e)
