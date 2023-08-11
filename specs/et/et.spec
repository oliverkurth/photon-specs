Name:           et
Version:        6.2.4
Release:        1
Summary:        Remote shell that survives IP roaming and disconnect

License:        ASL 2.0
URL:            https://mistertea.github.io/EternalTerminal/
Source0:        https://github.com/MisterTea/EternalTerminal/archive/et-v%{version}.tar.gz
%define sha512  %{name}=36cc593c4686730557954a3998c6be50f20b7d5b53f65409ea4cbf171956f9361db920111460d95974277627380ef4f51fb0b74a0b235b861d3d35fb5abc2b35
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
  -DDISABLE_VCPKG=TRUE
%cmake_build


%install
%cmake_install
mkdir -p \
  %{buildroot}%{_unitdir} \
  %{buildroot}%{_sysconfdir}
install -m 0644 -p systemctl/et.service %{buildroot}%{_unitdir}/et.service
install -m 0644 -p etc/et.cfg %{buildroot}%{_sysconfdir}/et.cfg

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
%changelog
* Thu Jun 29 2023 Oliver Kurth <okurth@vmware.com> - 6.2.4-1
- initial package
