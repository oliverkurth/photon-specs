%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        lightweight and portable command-line YAML, JSON and XML processor
Name:           yq
Version:        4.34.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/mikefarah/yq/archive/refs/tags/v%{version}.tar.gz
Source0:        yq-%{version}.tar.gz
%define sha512  %{name}=584f379f9a9c808dda643e60c55475e81949fe92a0d3bfa3b515145e310e1dfa7e65883b0d391db628f90e48426ae39da5fb0b9a5355d3ac83505fe57501e55c
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go

%global debug_package %{nil}

%description
a lightweight and portable command-line YAML, JSON and XML processor. yq uses
jq like syntax but works with yaml files as well as json, xml, properties,
csv and tsv. It doesn't yet support everything jq does - but it does support
the most common operations and functions, and more is being added continuously.

%prep -p exit
%autosetup -p1 -n yq-%{version}

%build
export GOROOT=/usr/lib/golang/
mkdir -p bin
go build -buildmode=pie -ldflags="-X 'main.buildVersion=${VERSION}' -X 'main.buildDate=${BUILD_DATE}'" -o bin/yq

%install
install -m 755 -d %{buildroot}%{_bindir}
install bin/yq %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Wed May 24 2023 <okurth@vmware.com> 4.34.1-1
- initial release
