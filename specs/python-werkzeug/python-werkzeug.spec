Summary:        The Swiss Army knife of Python web development
Name:           python3-werkzeug
Version:        3.1.3
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Werkzeug

Source0:        https://files.pythonhosted.org/packages/9f/69/83029f1f6300c5fb2471d621ab06f6ec6b3324685a2ce0f9777fd4a8b71e/werkzeug-%{version}.tar.gz
%define sha512  werkzeug=922c7c377cb10baa76ba9457a2334716969fe058cbc75725989a3d8c61c061a8cf5c6e8bdce70ec098db7822dd12db3391fb8c1471f51d99f48c54df00b182e1

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-requests
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%prep
%autosetup -p1 -n werkzeug-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

#%check
#pip3 install pytest hypothesis
#LANG=en_US.UTF-8 PYTHONPATH=./  python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Feb 17 2025 Oliver Kurth <oliver.kurth@broadcom.com> 3.1.3-1
- update to 3.1.3
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-3
- Fix CVE-2024-34069
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.2-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-3
- Bump version as a part of requests & chardet upgrade
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.1-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.14.1-3
- Mass removal python2
* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-2
- Fix make check
- Moved buildrequires from subpackage
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-1
- Update to version 0.14.1
* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-2
- Fixed rpm check errors
* Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.12.1-1
- Updating package to latest
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.11.15-1
- Initial packaging for Photon.
