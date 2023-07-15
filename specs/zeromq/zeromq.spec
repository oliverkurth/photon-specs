%define tag ecc63d0d3b0e1a62c90b58b1ccdb5ac16cb2400a
Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.3.4
Release:        3%{?dist}
URL:            http://www.zeromq.org
License:        LGPLv3+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/zeromq/libzmq/archive/%{tag}.tar.gz
%define sha512 %{name}=4e8f709691d8f3f64d41cc0f0fd70fe0a676247dc88b1283fa90f41b838f5b83100ccabd18714e5638cfa66c5cec0ac67943a3559d535357ff3499de62e47069
Source1:        vmci_sockets.h

Requires:       libstdc++

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
%autosetup -p1 -n libzmq-%{tag}

%build
cp %{SOURCE1} .
autoreconf -i
%configure \
    --with-libsodium=no \
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

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/

%changelog
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
