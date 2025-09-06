Name:           mosquitto
Version:        2.0.22
Release:        0%{?dist}
Summary:        Open Source MQTT v5/v3.1.x Broker

License:        EPL-2.0
URL:            https://mosquitto.org/
Source0:        https://mosquitto.org/files/source/%{name}-%{version}.tar.gz
Source1:        mosquitto-sysusers.conf
# https://github.com/eclipse-mosquitto/mosquitto/pull/3150
Patch1:         0001-Fix-the-libdir-location-in-the-pkgconf-files.patch

BuildRequires:  c-ares-devel
BuildRequires:  json-c-devel
BuildRequires:  gcc
#BuildRequires:  libuuid-devel
BuildRequires:  libxslt-devel
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
#BuildRequires:  uthash-devel

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Mosquitto is an open source message broker that implements the MQ Telemetry
Transport protocol version v5 and 3.1.x. MQTT provides a lightweight method
of carrying out messaging using a publish/subscribe model. This makes it
suitable for "machine to machine" messaging such as with low power sensors 
or mobile devices such as phones, embedded computers or micro-controllers 
like the Arduino.

%package devel
Requires:     %{name}%{?_isa} = %{version}-%{release}
Summary:      Development files for %{name}

%description devel
Development headers and libraries for %{name}.

%prep
%autosetup -p1
# Don't strip binaries on install: rpmbuild will take care of it
sed -i "s|(INSTALL) -s|(INSTALL)|g" lib/Makefile src/Makefile client/Makefile
# Search for the correct websockets library name
sed -i "s/websockets_shared/websockets/" src/CMakeLists.txt

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
       -DWITH_SYSTEMD=ON \
       -DWITH_SRV=ON \
       -DWITH_TLS=ON \
       %nil

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 service/systemd/%{name}.service.notify %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%files
%license LICENSE.txt 
%doc ChangeLog.txt CONTRIBUTING.md README.md
%{_bindir}/%{name}*
%if 0%{?fedora} < 42 || 0%{?rhel}
%{_sbindir}/%{name}
%endif
%{_libdir}/libmosquitto*.so.1
%{_libdir}/libmosquitto*.so.%{version}

# missing, need to find put why (related to cJSON not found?)
#%{_libdir}/mosquitto_dynamic_security.so

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config %{_sysconfdir}/%{name}/*.example
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_mandir}/man*/%{name}*
%{_mandir}/man7/mqtt.7.*

%files devel
%{_includedir}/mosquitto*.h
%{_includedir}/mqtt*.h
%{_libdir}/libmosquitto*.so
%{_libdir}/pkgconfig/libmosquitto*.pc
%{_mandir}/man3/libmosquitto.3.*

%changelog
* Sat Sep 06 2025 Oliver Kurth <oliver.kurth@broadcom.com> - 2.0.22-0
- initial package for Photon
