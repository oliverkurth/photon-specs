Name:       rhizofs
Version:    0.2.4
Release:    1%{?dist}
URL:        https://github.com/oliverkurth/rhizofs
Source0:    https://github.com/oliverkurth/rhizofs/archive/refs/tags/v%{version}.tar.gz
%define sha512 %{name}=6b6ec3e9f0db0f3d6f8d55912b1a750175071c6287cdadd9a0e131d0177fab79cfb51eeba27e4a9322f72e962153588bf9d1a267337c3a4cf61092f30afbd332
Summary:    A simple remote filesystem based on FUSE, ZeroMQ and protobuf-c
License:    BSD

BuildRequires: protobuf-c-devel
BuildRequires: fuse-devel
BuildRequires: zeromq-devel

%description
This package contains the client.

%package        server
Summary:        RhizoFS server

%description    server
This package contains the server.

%prep
%autosetup

%build
%make_build

%install
mkdir -p %{buildroot}/%{_bindir}
export PREFIX=%{buildroot}/%{_prefix}
%make_install

%files
%{_bindir}/rhizofs

%files server
%{_bindir}/rhizosrv
%{_bindir}/rhizo-keygen

%changelog
* Fri Oct 06 2023 <okurth@gmail.com> 0.2.4-1
- update to 0.2.4
* Mon May 23 2022 <okurth@vmware.com> 0.2.2-1
- initial rpm package
