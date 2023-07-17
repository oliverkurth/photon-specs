Summary:        lightweight and portable command-line YAML, JSON and XML processor
Name:           yq
Version:        4.34.2
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/mikefarah/yq/archive/refs/tags/yq-%{version}.tar.gz
Source0:        yq-%{version}.tar.gz
%define sha512  %{name}=235bece12983be74458e31b64ae3e38c1958c0e3d09e09c418d7698ec045abb16da75a7ebf0d9e8bb715c90656341f459f38a303392f9d52a38c9c146def2987
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  ca-certificates
BuildRequires:  go

%global debug_package %{nil}

%description
a lightweight and portable command-line YAML, JSON and XML processor. yq uses
jq like syntax but works with yaml files as well as json, xml, properties,
csv and tsv. It doesn't yet support everything jq does - but it does support
the most common operations and functions, and more is being added continuously.

%prep -p exit
%autosetup -p1

%build
export GOROOT=%{_libdir}/golang/
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
* Wed Jul 12 2023 <okurth@vmware.com> 4.34.2-1
- initial release
