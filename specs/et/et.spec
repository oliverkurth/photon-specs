Name:           et
Version:        6.2.9
Release:        1
Summary:        Remote shell that survives IP roaming and disconnect

License:        ASL 2.0
URL:            https://mistertea.github.io/EternalTerminal/
Source0:        https://github.com/MisterTea/EternalTerminal/archive/et-v%{version}.tar.gz
Patch0:         0001-remove-stdc-fs.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gflags-devel
BuildRequires:  curl-devel
BuildRequires:  libsodium-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libutempter-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-c-static
BuildRequires:  protobuf-c-devel
BuildRequires:  systemd
BuildRequires:  zlib-devel


%{?systemd_requires}

%description
Eternal Terminal (ET) is a remote shell that automatically reconnects without
interrupting the session.


%prep
%autosetup -p1 -n EternalTerminal-et-v%{version}
# use this if we have patches we need to apply by hand
# %%setup -q -n EternalTerminal-et-v%%{version}


%build
%cmake \
  -DDISABLE_VCPKG=TRUE \
  -DCMAKE_EXE_LINKER_FLAGS="-Wl,--copy-dt-needed-entries" -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--copy-dt-needed-entries"
%cmake_build


%install
%cmake_install
mkdir -p \
  %{buildroot}%{_unitdir} \
  %{buildroot}%{_sysconfdir}
install -m 0644 -p systemctl/et.service %{buildroot}%{_unitdir}/et.service
install -m 0644 -p etc/et.cfg %{buildroot}%{_sysconfdir}/et.cfg
rm -rf %{buildroot}/usr/lib64/cmake
rm -f %{buildroot}/usr/include/httplib.h
rm -f %{buildroot}/usr/lib64/libcrashpad*.a
rm -f %{buildroot}/usr/lib64/libmini_chromium.a
rm -f rf %{buildroot}%{_bindir}/crashpad_handler

%post
%systemd_post et.service

%preun
%systemd_preun et.service

%postun
%systemd_postun_with_restart et.service


%files
%license LICENSE
%doc README.md
%{_bindir}/et
%{_bindir}/etserver
%{_bindir}/etterminal
%{_bindir}/htm
%{_bindir}/htmd
%config(noreplace) %{_sysconfdir}/et.cfg
%{_unitdir}/et.service


%changelog
* Sat Mar 8 2025 Oliver Kurth <okurth@vmware.com> - 6.2.9-1
- update to 6.2.9
* Tue Dec 12 2023 Oliver Kurth <okurth@vmware.com> - 6.2.8-1
- update to 6.2.8
* Thu Jun 29 2023 Oliver Kurth <okurth@vmware.com> - 6.2.4-1
- initial package
