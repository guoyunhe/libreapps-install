__author__ = "Guo Yunhe <guoyunhebrave@gmail.com>"
__date__ = "$2015-10-17 14:36:39$"

import dbus
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='URL of one click package installation')
    args = parser.parse_args()
    url = args.url
    packages = url[8:].split(',')
    
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
