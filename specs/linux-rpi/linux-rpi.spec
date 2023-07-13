%define arch arm64
%define archdir arm64

%define tag 1.20230405

Summary:        Kernel
Name:           linux-rpi
# check Makefile at tag:
Version:        6.1.21
Release:        1%{?dist}
License:        GPLv2
URL:            https://github.com/raspberrypi/linux
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      aarch64

%define uname_r %{version}-%{release}-rpi
%define _modulesdir /lib/modules/%{uname_r}

Source0:        https://github.com/raspberrypi/linux/archive/refs/tags/%{tag}.tar.gz
%define sha512  %{name}=0c8252833bb737977c0981ed48764ff9742de7cb494fefec532c90312e0d8e0e48a230dd14a0d6f99b54b015e6c91e647b579f2ef7408b80e349a547767d9925
Source2:        initramfs.trigger
Source6:        scriptlets.inc
Source18:       spec_install_post.inc
Source19:       %{name}-dracut-%{_arch}.conf

BuildRequires:  bc
BuildRequires:  openssl-devel
BuildRequires:  xz
BuildRequires:  bison


Requires: kmod
Requires: filesystem
Requires(pre):    (coreutils or coreutils-selinux)
Requires(preun):  (coreutils or coreutils-selinux)
Requires(post):   (coreutils or coreutils-selinux)
Requires(postun): (coreutils or coreutils-selinux)

%description
This Linux package contains the Linux kernel for the Raspberry Pi

%package dtb
Summary:        Raspberry DTB files
Group:          System Environment/Kernel
Conflicts: dtb-rpi-overlay
Conflicts: dtb-rpi3
Conflicts: dtb-rpi4
%description dtb
The device tree binary files for the Raspberry Pi

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       gawk
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
%setup -q -n linux-%{tag}

%build
make %{?_smp_mflags} mrproper
make bcm2711_defconfig

sed -i 's/CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION="-%{release}-rpi"/' .config

make %{?_smp_mflags} KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=%{arch} %{?_smp_mflags} Image modules dtbs


%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} ARCH=%{arch} INSTALL_MOD_PATH=%{buildroot} modules_install

install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/linux-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
%endif

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_localstatedir}/lib/initramfs/kernel

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/linux-headers-%{uname_r}' copy

cp .config %{buildroot}%{_usrsrc}/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/linux-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
#find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

mkdir -p %{buildroot}%{_modulesdir}/dracut.conf.d/
cp -p %{SOURCE19} %{buildroot}%{_modulesdir}/dracut.conf.d/%{name}.conf

mkdir -p %{buildroot}/boot/efi
make %{?_smp_mflags} dtbs_install INSTALL_DTBS_PATH=%{buildroot}/boot/efi
pushd %{buildroot}/boot/efi
mv broadcom excluded
mv excluded/*.dtb ./
rm -rf excluded
popd


%include %{SOURCE2}
%include %{SOURCE6}
%include %{SOURCE18}


%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/photon.cfg


%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build

%config(noreplace) %{_modulesdir}/dracut.conf.d/%{name}.conf

%files dtb
%defattr(-,root,root)
/boot/efi/*.dtb
/boot/efi/overlays/*

%files docs
%defattr(-,root,root)
%{_docdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/linux-headers-%{uname_r}


%changelog
* Sun Jul 09 2023 Oliver Kurth <okurth@vmware.com> 6.1.21-1
- initial RPi package
