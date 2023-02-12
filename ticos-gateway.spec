%define name ticos-gateway
%define version 3.2
%define unmangled_version 3.2
%define release 1

Summary: Ticos Gateway for IoT devices.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}.service
Source1: configs.tar.gz
License: Apache Software License (Apache Software License 2.0)
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Ticos <info@ticos.io>
Url: https://github.com/ticos/ticos-gateway
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/pip3, /usr/bin/mkdir, /usr/bin/cp
Requires(post): /usr/bin/systemctl, /usr/bin/cp, /usr/bin/rm, /usr/bin/chown, /usr/bin/sed
Requires(postun): /usr/sbin/userdel, /usr/bin/rm, /usr/bin/systemctl

%description
The Ticos IoT Gateway is an open-source solution that allows you to integrate devices connected to legacy and third-party systems with Ticos.

%pre
/usr/bin/getent passwd ticos_gateway || /usr/sbin/useradd -c "Ticos-Gateway Service" -r -U -d /var/lib/ticos_gateway ticos_gateway && passwd -d ticos_gateway
/usr/bin/pip3 install ticos-gateway==%{version}
sudo find $(python3 -c "from ticos_gateway import __path__; print(str(__path__[0])+'/extensions')") -name "*.pyc" -exec rm -f {} \;

%build
mkdir -p $RPM_BUILD_ROOT/etc/ticos-gateway || echo "Ticos config folder already exists"
mkdir -p $RPM_BUILD_ROOT/var/lib/ticos_gateway || echo "Ticos user home directory already exists"
mkdir -p $RPM_BUILD_ROOT/var/lib/ticos_gateway/extensions || echo 0 > /dev/null
mkdir -p $RPM_BUILD_ROOT/var/log/ticos-gateway || echo "Ticos log directory already exists"
sudo chown -R ticos_gateway:ticos_gateway $RPM_BUILD_ROOT/var/log/ticos-gateway
sudo install -p -D -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/systemd/system/ticos-gateway.service
sudo install -p -D -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/ticos-gateway/
sudo /usr/bin/chown ticos_gateway:ticos_gateway $RPM_BUILD_ROOT/etc/ticos-gateway -R
sudo /usr/bin/chown ticos_gateway:ticos_gateway $RPM_BUILD_ROOT/var/log/ticos-gateway -R
sudo /usr/bin/chown ticos_gateway:ticos_gateway $RPM_BUILD_ROOT/var/lib/ticos_gateway -R
# sudo find $(python3 -c "from ticos_gateway import __path__; print(str(__path__[0])+'/extensions')") \( -iname '*' ! -iname "*.pyc" \) -exec cp {} $RPM_BUILD_ROOT/var/lib/ticos_gateway/extensions \;
# sudo cp -r $(python3 -c "from ticos_gateway import __path__; print(str(__path__[0])+'/extensions')") $RPM_BUILD_ROOT/var/lib/ticos_gateway/

# %install
# sudo find %{buildroot} -name ".pyc" -delete

%post
/usr/bin/sed -i 's/\.\/logs/\/var\/log\/ticos-gateway/g' /etc/ticos-gateway/config/logs.conf >> /etc/ticos-gateway/config/logs.conf
/usr/bin/rm -rf $RPM_BUILD_ROOT/etc/ticos-gateway/ticos-gateway
/usr/bin/rm -f $RPM_BUILD_ROOT/etc/ticos-gateway/configs.tar.gz
/usr/bin/systemctl enable ticos-gateway.service
/usr/bin/systemctl start ticos-gateway.service

%clean
sudo rm -rf $RPM_BUILD_ROOT

%files
/etc/systemd/system/ticos-gateway.service
/etc/ticos-gateway/
/var/log/ticos-gateway/
/var/lib/ticos_gateway/
%exclude /usr/local/lib/*
%exclude /usr/local/bin/ticos-gateway
%exclude /usr/local/bin/ticos-gateway-configurator
%defattr(-,ticos_gateway,ticos_gateway)

%postun
systemctl stop ticos-gateway
userdel ticos_gateway
/usr/sbin/userdel ticos_gateway
/usr/bin/rm -rf $RPM_BUILD_ROOT/var/log/ticos-gateway
/usr/bin/rm -rf $RPM_BUILD_ROOT/var/lib/ticos_gateway
