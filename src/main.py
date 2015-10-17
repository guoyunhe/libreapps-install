
__author__ = "Guo Yunhe <guoyunhebrave@gmail.com>"
__date__ = "$2015-10-17 14:36:39$"

import dbus

if __name__ == "__main__":
    print "Hello World"

    try:
        bus = dbus.SessionBus()
    except dbus.DBusException, e:
        print 'Unable to connect to dbus: %s' % str(e)
        sys.exit()
    try:
        proxy = bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit')
        iface = dbus.Interface(proxy, 'org.freedesktop.PackageKit.Modify')
        iface.InstallPackageNames(dbus.UInt32(0), ["openoffice-clipart", "openoffice-clipart-extras"], "show-confirm-search,hide-finished")
    except dbus.DBusException, e:
        print 'Unable to use PackageKit: %s' % str(e)
