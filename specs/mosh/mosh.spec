Name:    mosh
Version: 1.4.0
Release: 1%{?dist}
Summary: Mobile shell that supports roaming and intelligent local echo

License: GPLv3+
URL:     https://mosh.mit.edu/
Source0: https://mosh.mit.edu/mosh-%{version}.tar.gz
%define sha512 %{name}=38c11f52ff1e42965b50a22bf6de80b0fa8ebbff841d825e760abf69c788a2bf5f34e6f7fc047574d595118334eef9edf8da5520b52cdde3ac1a79d7ad70312e

BuildRequires: libutempter-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: perl
BuildRequires: protobuf-devel
BuildRequires: zlib-devel
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-server = %{version}-%{release}
Requires: openssl

%description
Mosh is a remote terminal application that supports:
  - intermittent network connectivity,
  - roaming to different IP address without dropping the connection, and
  - intelligent local echo and line editing to reduce the effects
    of "network lag" on high-latency connections.

%package client
Summary: mosh client
Requires: openssh-clients
Requires: openssl
Requires: perl

%description client
This provides the mosh client

%package server
Summary: mosh client
Requires: openssl

%description server
This provides the mosh server

%prep
%setup -q

%build
%configure --disable-silent-rules
%make_build

%install
%make_install

%files
%defattr(-,root,root)

%files client
%doc README.md ChangeLog
%license COPYING
%{_bindir}/mosh
%{_bindir}/mosh-client
%{_mandir}/man1/mosh.1.gz
%{_mandir}/man1/mosh-client.1.gz

%files server
%doc README.md ChangeLog
%license COPYING
%{_bindir}/mosh-server
%{_mandir}/man1/mosh-server.1.gz

%changelog
* Sat May 20 2023 Oliver Kurth <okurth@vmware.com> - 1.4.0-1
- initial package
