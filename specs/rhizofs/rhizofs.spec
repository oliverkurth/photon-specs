Name:       rhizofs
Version:    0.2.7
Release:    1%{?dist}
URL:        https://github.com/oliverkurth/rhizofs
Source0:    https://github.com/oliverkurth/rhizofs/archive/refs/tags/v%{version}.tar.gz
%define sha512 %{name}=f11c720a03b66bb3deea6fccb6ace280ff9e885e8afacb1cafc4faa08e7e311de6e751196cd6fcf9d04f6e995e19ced096234a4b0f37afa9eb846aa9ea3f4f31
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
* Fri Nov 22 2024 <okurth@gmail.com> 0.2.7-1
- update to 0.2.7
* Mon Jan 15 2024 <okurth@gmail.com> 0.2.5-1
- update to 0.2.5
* Fri Oct 06 2023 <okurth@gmail.com> 0.2.4-1
- update to 0.2.4
* Mon May 23 2022 <okurth@gmail.com> 0.2.2-1
- initial rpm package
