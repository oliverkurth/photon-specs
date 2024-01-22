Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.3.5
Release:        1%{?dist}
URL:            http://www.zeromq.org
License:        LGPLv3+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/zeromq/libzmq/archive/v%{version}.tar.gz
%define sha512 %{name}=108d9c5fa761c111585c30f9c651ed92942dda0ac661155bca52cc7b6dbeb3d27b0dd994abde206eacfc3bc88d19ed24e45b291050c38469e34dca5f8c9a037d
Source1:        vmci_sockets.h

BuildRequires: libsodium-devel

Requires:       libstdc++
Requires:       libsodium

%description
The 0MQ lightweight messaging kernel is a library which extends the standard
socket interfaces with features traditionally provided by specialised messaging
middleware products. 0MQ sockets provide an abstraction of asynchronous message
queues, multiple messaging patterns, message filtering (subscriptions), seamless
access to multiple transport protocols and more.

%package        devel
Summary:        Header and development files for zeromq
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n libzmq-%{version}

%build
cp %{SOURCE1} .
autoreconf -i
%configure \
    --with-libsodium=yes \
    --with-vmci \
    --disable-Werror \
    --disable-static
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make check %{_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS
%{_libdir}/libzmq.so.*
%{_bindir}/curve_keygen

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/

%changelog
*   Mon Jan 22 2024 Oliver Kurth <okurth@vmware.com> 4.3.5-1
-   update to 4.3.5
-   build with libsodium
*   Fri Jul 14 2023 Oliver Kurth <okurth@vmware.com> 4.3.4-3
-   update to snap shot (no release in last 2 years)
-   enable VMCI transport
*   Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 4.3.4-2
-   fix: build fails with gcc 12
*   Fri Jul 09 2021 Nitesh Kumar <kunitesh@vmware.com> 4.3.4-1
-   Upgrade to 4.3.4
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.3-1
-   Automatic Version Bump
*   Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.2-1
-   Automatic Version Bump
*   Mon Jul 22 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-2
-   Apply patch for CVE-2019-13132
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-1
-   Updated to latest version
*   Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 4.1.4-3
-   Remove devpts mount
*   Mon Aug 07 2017 Chang Lee <changlee@vmware.com> 4.1.4-2
-   Fixed %check
*   Thu Apr 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.4-1
-   Initial build. First version
