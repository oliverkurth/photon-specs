Name:     pwgen
Version:  2.08
Release:  1%{?dist}
Summary:  Automatic Password generation

License: GPL-2
URL:     https://github.com/tytso/pwgen
Source0: https://github.com/tytso/pwgen/archive/refs/tags/v%{version}.tar.gz

BuildRequires: perl

%description
Automatic Password generation

%prep
%autosetup -p1

%build
autoupdate
autoreconf
%configure

%make_build

%install
%make_install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_mandir}/*

%changelog
* Mon Mar 17 2025 Oliver Kurth <oliver.kurth@broadcom.com> - 2.08-1
- initial package
