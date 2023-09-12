Name:           hostapd
Version:        2.10
Release:        1%{?dist}
Summary:        IEEE 802.11 AP, IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator
License:        BSD
URL:            http://w1.fi/hostapd
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon

Source0:        http://w1.fi/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=243baa82d621f859d2507d8d5beb0ebda15a75548a62451dc9bca42717dcc8607adac49b354919a41d8257d16d07ac7268203a79750db0cfb34b51f80ff1ce8f

Source1:        %{name}.service
Source2:        %{name}.conf
Source3:        %{name}.conf.5
Source4:        %{name}.sysconfig

BuildRequires:  libnl-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  gcc

BuildRequires:      systemd
BuildRequires: make
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
%{name} is a user space daemon for access point and authentication servers. It
implements IEEE 802.11 access point management, IEEE 802.1X/WPA/WPA2/EAP
Authenticators and RADIUS authentication server.

%{name} is designed to be a "daemon" program that runs in the back-ground and
acts as the backend component controlling authentication. %{name} supports
separate frontend programs and an example text-based frontend, hostapd_cli, is
included with %{name}.

%prep
%autosetup -p1

%build
cd hostapd
cat defconfig | sed \
    -e '$ a CONFIG_SAE=y' \
    -e '/^#CONFIG_DRIVER_NL80211=y/s/^#//' \
    -e '/^#CONFIG_RADIUS_SERVER=y/s/^#//' \
    -e '/^#CONFIG_DRIVER_WIRED=y/s/^#//' \
    -e '/^#CONFIG_DRIVER_NONE=y/s/^#//' \
    -e '/^#CONFIG_IEEE80211N=y/s/^#//' \
    -e '/^#CONFIG_IEEE80211R=y/s/^#//' \
    -e '/^#CONFIG_IEEE80211AC=y/s/^#//' \
    -e '/^#CONFIG_IEEE80211AX=y/s/^#//' \
    -e '/^#CONFIG_FULL_DYNAMIC_VLAN=y/s/^#//' \
    -e '/^#CONFIG_LIBNL32=y/s/^#//' \
    -e '/^#CONFIG_ACS=y/s/^#//' \
    -e '/^#CONFIG_OCV=y/s/^#//' \
    -e '/^#CONFIG_OWE=y/s/^#//' \
    > .config
echo "CFLAGS += -I%{_includedir}/libnl3" >> .config
echo "LIBS += -L%{_libdir}" >> .config
make %{?_smp_mflags} BINDIR=%{_sbindir} LIBDIR=%{_libdir} EXTRA_CFLAGS="$RPM_OPT_FLAGS"

%install
# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# config files
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -pm 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}

install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -pm 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# binaries
install -d %{buildroot}/%{_sbindir}
install -pm 0755 %{name}/%{name} %{buildroot}%{_sbindir}/%{name}
install -pm 0755 %{name}/%{name}_cli %{buildroot}%{_sbindir}/%{name}_cli

# man pages
install -d %{buildroot}%{_mandir}/man{1,5,8}
install -pm 0644 %{name}/%{name}_cli.1 %{buildroot}%{_mandir}/man1
install -pm 0644 %{SOURCE3} %{buildroot}%{_mandir}/man5
install -pm 0644 %{name}/%{name}.8 %{buildroot}%{_mandir}/man8

# prepare docs
cp %{name}/README ./README.%{name}
cp %{name}/README-WPS ./README-WPS.%{name}
cp %{name}/logwatch/README ./README.logwatch

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%doc README README.hostapd README-WPS.hostapd
%doc %{name}/%{name}.conf %{name}/wired.conf
%doc %{name}/%{name}.accept %{name}/%{name}.deny
%doc %{name}/%{name}.eap_user %{name}/%{name}.radius_clients
%doc %{name}/%{name}.vlan %{name}/%{name}.wpa_psk
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}_cli
%dir %{_sysconfdir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_unitdir}/%{name}.service

%changelog
* Sun Jun 11 2023 Oliver Kurth <okurth@gmail.com> 2.10-1
- initial build, adapted from Fedora

