Name:       rhizofs
Version:    0.2.2
Release:    1%{?dist}
URL:        https://github.com/oliverkurth/rhizofs
Source0:    %{name}-%{version}.tar.gz
%define sha512 %{name}=4fb07af2aa21631c1b9ebe2416ff749b61b7f8723bade6230f90596d7305797c35fc959d7899fdc31b0c9f83e7850a526f0e083a9dd32a93c05cdabd9331d5a8
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

%changelog
* Mon May 23 2022 <okurth@vmware.com> 0.2.2-1
- initial rpm package
