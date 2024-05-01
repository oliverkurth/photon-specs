Name:           partfs
Version:        0.1.0
Release:        1
Summary:        FUSE-based file system for accessing partitions on a disk

License:        BSD-3-Clause
URL:            https://github.com/braincorp/partfs
Source0:        https://github.com/braincorp/partfs/archive/refs/tags/v%{version}.tar.gz
%define sha512  %{name}=1446bb2ef5c242fdafff0edef7700833fbaae3959a249a5eed3e50d45e99d5c9218b9d74b43d0b091564249fcff21fe10d534377b52c31562d1a2eba6cf3dcf6

BuildRequires:  cmake
BuildRequires:  util-linux-devel
BuildRequires:  fuse-devel
BuildRequires:  pkg-config

Requires: fuse
Requires: util-linux

%description
partfs allows one to access partitions within a device or file.
The main purpose of partfs is to allow the creation of disk
images without superuser privileges. This can be useful for the
enabling automatic partition discovery for containers or for
building disk images for embedded software.

%prep
%autosetup

%build
make

%install
install -m 0755 -D -p build/bin/partfs %{buildroot}%{_bindir}/partfs

%files
%license LICENSE
%doc README.md
%{_bindir}/partfs

%changelog
* Wed Apr 17 2024 Oliver Kurth <oliver.kurth@broadcom.com> - 6.2.8-1
- initial package
