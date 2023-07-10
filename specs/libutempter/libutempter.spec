%define utempter_compat_ver 0.5.2

Summary: A privileged helper for utmp/wtmp updates
Name: libutempter
Version: 1.2.1
Release: 1%{?dist}
License: LGPL-2.1-or-later
URL: ftp://ftp.altlinux.org/pub/people/ldv/utempter
%define sha512  %{name}=d3a3bab7d2c2a68534c5ad41dd02bde849eb08df5dbb895a79b50b74d269c48c4cfcd12c4654941ccb7cdd43f486cfdc19148fa470870562f5cd324ce9782429

Source0: ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make

Requires(pre): shadow

Provides: utempter = %{utempter_compat_ver}

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%package devel
Summary: Development environment for utempter
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" \
    libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
%make_install libdir="%{_libdir}" libexecdir="%{_libexecdir}"

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%pre
{
    %{_sbindir}/groupadd -g 22 -r -f utmp || :
    %{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%ldconfig_scriptlets

%files
%license COPYING
%doc README
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.*
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter

%files devel
%{_includedir}/utempter.h
%{_libdir}/libutempter.so
%{_mandir}/man3/*

%changelog
* Sat May 20 2023 Oliver Kurth <okurth@vmware.com> - 1.2.1-1
- initial package

