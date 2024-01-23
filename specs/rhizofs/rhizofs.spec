Name:       rhizofs
Version:    0.2.5
Release:    1%{?dist}
URL:        https://github.com/oliverkurth/rhizofs
Source0:    https://github.com/oliverkurth/rhizofs/archive/refs/tags/v%{version}.tar.gz
%define sha512 %{name}=fe272811506130905e82e98bc348798ccbd3859a5e2d792118c30ad7c3d07f1d12bd740d78c5d31dc6408042134376e7ab238bb43f8f6b7653054f115c3bb860
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
%{_bindir}/rhizo-keygen

%files server
%{_bindir}/rhizosrv
%{_bindir}/rhizo-keygen

%changelog
* Mon Jan 15 2024 <okurth@gmail.com> 0.2.5-1
- update to 0.2.4
* Fri Oct 06 2023 <okurth@gmail.com> 0.2.4-1
- update to 0.2.4
* Mon May 23 2022 <okurth@gmail.com> 0.2.2-1
- initial rpm package
