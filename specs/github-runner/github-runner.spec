Name:       github-runner
Version:    2.322.0
Release:    1%{?dist}
Summary:    GitHub Runner
License:    MIT
URL:        https://github.com/actions/runner
%ifarch aarch64
%define gh_arch arm64
%else
%define gh_arch x64
%endif
Source0:    https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-%{gh_arch}-%{version}.tar.gz
Source1:    runner.sh
Source2:    runner-hook-job-started.sh
Source3:    runner@.service

Requires: icu
Requires: krb5
Requires: openssl
Requires: zlib

%description
GitHub Runner

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
tar zxf %{SOURCE0} -C %{buildroot}%{_libdir}/%{name}
# not needed, and would generate a dependency on musl
rm -rf %{buildroot}%{_libdir}/%{name}/externals/node20_alpine/

mkdir -p %{buildroot}/%{_bindir} %{buildroot}/%{_userunitdir}
install -pm 0755 %{SOURCE1} %{buildroot}/%{_bindir}
install -pm 0755 %{SOURCE2} %{buildroot}/%{_bindir}
install -pm 644 %{SOURCE3} %{buildroot}/%{_userunitdir}

%files
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_bindir}/*
%{_userunitdir}/*

%changelog
* Mon Mar 17 2025 Oliver Kurth <oliver.kurth@broadcom.com> - 2.322.0-1
- initial package
