%if 0%{?rhel}
Name: rhel-system-roles
%else
Name: linux-system-roles
%endif
Summary: Set of interfaces for unified system management
Version: 1.0
Release: 7%{?dist}

#Group: Development/Libraries
License: GPLv3+ and MIT and BSD
%if 0%{?rhel}
%global rolealtprefix linux-system-roles.
%endif
%global roleprefix %{name}.

%define defcommit() %{expand:%%global id%{1} %{2}
%%global shortid%{1} %%(c=%%{id%{1}}; echo ${c:0:7})
}

%define deftag() %{expand:%%global id%{1} %{2}
%%global shortid%{1} %{2}
}

#%%defcommit 0 fe8bb81966b60fa8979f3816a12b0c7120d71140
%global rolename0 kdump
%deftag 0 1.0.0

%defcommit 1 611754bcc79783d026177c79a796c6d6343d1be5
%global rolename1 postfix
#%%deftag 1 0.1

#%%defcommit 2 6dd057aa434a31cb6ee67d02967362f9131e0c50
%global rolename2 selinux
%deftag 2 1.0.0

#%%defcommit 3 33a1a8c349de10d6281ed83d4c791e9177d7a141
%global rolename3 timesync
%deftag 3 1.0.0

%defcommit 5 64b2d76de74df2d480394d02aae204beda4d9257
%global rolename5 network
#%%deftag 5 1.0.0

Source: https://github.com/linux-system-roles/%{rolename0}/archive/%{id0}.tar.gz#/%{rolename0}-%{shortid0}.tar.gz
Source1: https://github.com/linux-system-roles/%{rolename1}/archive/%{id1}.tar.gz#/%{rolename1}-%{shortid1}.tar.gz
Source2: https://github.com/linux-system-roles/%{rolename2}/archive/%{id2}.tar.gz#/%{rolename2}-%{shortid2}.tar.gz
Source3: https://github.com/linux-system-roles/%{rolename3}/archive/%{id3}.tar.gz#/%{rolename3}-%{shortid3}.tar.gz
Source5: https://github.com/linux-system-roles/%{rolename5}/archive/%{id5}.tar.gz#/%{rolename5}-%{shortid5}.tar.gz

# 2018-10-23: Submitted upstream: https://github.com/linux-system-roles/timesync/pull/25
Source6: single-pool.yml
Source7: multiple-ntp-servers.yml

# 2018-10-23: Submitted upstream
Source8: md2html.sh

%if "%{roleprefix}" != "linux-system-roles."
Patch1: rhel-system-roles-%{rolename1}-prefix.diff
Patch2: rhel-system-roles-%{rolename2}-prefix.diff
Patch3: rhel-system-roles-%{rolename3}-prefix.diff
Patch5: rhel-system-roles-%{rolename5}-prefix.diff
%endif

# Not suitable for upstream, since the files need to be executable there
Patch52: network-permissions.diff

Url: https://github.com/linux-system-roles/
BuildArch: noarch

BuildRequires: asciidoc
BuildRequires: pandoc
BuildRequires: highlight

Obsoletes: rhel-system-roles-techpreview < 1.0-3

%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Red Hat Enterprise Linux.


%prep
%setup -qc -a1 -a2 -a3 -a5
cd %{rolename0}-%{id0}
#kdump patches here if necessary
cd ..
cd %{rolename1}-%{id1}
%if "%{roleprefix}" != "linux-system-roles."
%patch1 -p1
%endif
cd ..
cd %{rolename2}-%{id2}
%if "%{roleprefix}" != "linux-system-roles."
%patch2 -p1
%endif
cd ..
cd %{rolename3}-%{id3}
%if "%{roleprefix}" != "linux-system-roles."
%patch3 -p1
%endif
cd ..
cd %{rolename5}-%{id5}
%if "%{roleprefix}" != "linux-system-roles."
%patch5 -p1
%endif
%patch52 -p1
cd ..

%build
sh %{SOURCE8} \
%{rolename0}-%{id0}/README.md \
%{rolename1}-%{id1}/README.md \
%{rolename2}-%{id2}/README.md \
%{rolename3}-%{id3}/README.md \
%{rolename5}-%{id5}/README.md

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

cp -pR %{rolename0}-%{id0}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename0}
cp -pR %{rolename1}-%{id1}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename1}
cp -pR %{rolename2}-%{id2}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename2}
cp -pR %{rolename3}-%{id3}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename3}
cp -pR %{rolename5}-%{id5}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename5}

%if 0%{?rolealtprefix:1}
ln -s    %{roleprefix}%{rolename0}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename0}
ln -s    %{roleprefix}%{rolename1}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename1}
ln -s    %{roleprefix}%{rolename2}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename2}
ln -s    %{roleprefix}%{rolename3}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename3}
ln -s    %{roleprefix}%{rolename5}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename5}
%endif

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kdump
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/postfix
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
install -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-single-pool.yml
install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-multiple-ntp-servers.yml
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/network

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kdump

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/postfix

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/selinux-playbook.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux/example-selinux-playbook.yml

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/bond-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/bridge-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bridge-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth-simple-auto.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth-simple-auto-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/infiniband.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-infiniband-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/macvlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-macvlan-playbook.yml
cp $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/remove-profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-remove-profile-playbook.yml
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/remove-profile.yml
cp $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/down-profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-down-profile-playbook.yml
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/down-profile.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/inventory \
   $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-inventory

rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/tests/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/roles
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples

%files
%dir %{_datadir}/ansible
%dir %{_datadir}/ansible/roles
%if 0%{?rolealtprefix:1}
%{_datadir}/ansible/roles/%{rolealtprefix}kdump
%{_datadir}/ansible/roles/%{rolealtprefix}postfix
%{_datadir}/ansible/roles/%{rolealtprefix}selinux
%{_datadir}/ansible/roles/%{rolealtprefix}timesync
%{_datadir}/ansible/roles/%{rolealtprefix}network
%endif
%{_datadir}/ansible/roles/%{roleprefix}kdump
%{_datadir}/ansible/roles/%{roleprefix}postfix
%{_datadir}/ansible/roles/%{roleprefix}selinux
%{_datadir}/ansible/roles/%{roleprefix}timesync
%{_datadir}/ansible/roles/%{roleprefix}network
%doc %{_pkgdocdir}/*/example-*-playbook.yml
%doc %{_pkgdocdir}/network/example-inventory
%doc %{_pkgdocdir}/*/README.md
%doc %{_pkgdocdir}/*/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}kdump/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}postfix/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}selinux/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}timesync/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}network/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}kdump/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}postfix/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}selinux/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}timesync/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}network/README.html


%license %{_pkgdocdir}/*/COPYING
%license %{_pkgdocdir}/*/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}kdump/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}postfix/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}selinux/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}timesync/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}network/LICENSE

%changelog
* Wed Oct 24 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-7
- Update to latest versions of selinux, kdump and timesync.
- Update to the latest revision of postfix, fixes README markup
- Add Obsoletes for the -techpreview subpackage introduced mistakenly in 1.0-1

* Tue Oct 23 2018 Till Maas <opensource@till.name> - 1.0-6
- Update Network system role to latest commit to include Fedora 29 fixes
- Update example timesync example playbooks
- Add comments about upstream status

* Tue Aug 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-4
- Format the READMEs as html, by vdolezal, with changes to use highlight
  (source-highlight does not understand YAML)

* Thu Aug  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-3
- Rebase the network role to the last revision (d866422).
  Many improvements to tests, introduces autodetection of the current provider
  and defaults to using profile name as interface name.
- Rebase the selinux, timesync and kdump roles to their 1.0rc1 versions.
  Many changes to the role interfaces to make them more consistent
  and conforming to Ansible best practices.
- Update the description.

* Fri May 11 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-4
- Fix complaints about /usr/bin/python during RPM build by making the affected scripts non-exec
- Fix merge botch

* Mon Mar 19 2018 Troy Dawson <tdawson@redhat.com> - 0.6-3.1
- Use -a (after cd) instead of -b (before cd) in %setup

* Wed Mar 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-3
- Minor corrections of the previous change by Till Maas.

* Fri Mar  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-2
- Document network role options: static routes, ethernet, dns
  Upstream PR#36, bz1550128, documents bz1487747 and bz1478576

* Tue Jan 30 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-1
- Drop hard dependency on ansible (#1525655), patch from Yaakov Selkowitz
- Update the network role to version 0.4, solves bz#1487747, bz#1478576

* Tue Dec 19 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-3
- kdump: fix the wrong conditional for ssh checking and improve test (PR#10)

* Tue Nov 07 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-2
- kdump: add ssh support. upstream PR#9, rhbz1478707

* Tue Oct 03 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-1
- SELinux: fix policy reload when SELinux is disabled on CentOS/RHEL 6
  (bz#1493574)
- network: update to b856c7481bf5274d419f71fb62029ea0044b3ec1 :
  makes the network role idempotent (bz#1476053) and fixes manual
  network provider selection (bz#1485074).

* Mon Aug 28 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.4-1
- network: update to b9b6f0a7969e400d8d6ba0ac97f69593aa1e8fa5:
  ensure that state:absent followed by state:up works (bz#1478910), and change
  the example IP adresses to the IANA-assigned ones.
- SELinux: fix the case when SELinux is disabled (bz#1479546).

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-2
- We can't change directories to symlinks (rpm bug #447156) so keep the old
  names and create the new names as symlinks.

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-1
- Change the prefix to linux-system-roles., keeping compatibility
  symlinks.
- Update the network role to dace7654feb7b5629ded0734c598e087c2713265:
  adds InfiniBand support and other fixes.
- Drop a patch included upstream.

* Mon Jun 26 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-2
- Leave a copy of README and COPYING in every role's directory, as suggested by T. Bowling.
- Move the network example inventory to the documentation directory together.
  with the example playbooks and delete the now empty "examples" directory.
- Use proper reserved (by RFC 7042) MAC addresses in the network examples.

* Tue Jun 6 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-1
- Update the networking role to version 0.2 (#1459203)
- Version every role and the package separately. They live in separate repos
  and upstream release tags are not coordinated.

* Mon May 22 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-2
- Prefix the roles in examples and documentation with rhel-system-roles.

* Thu May 18 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-1
- Update to 0.1 (first upstream release).
- Remove the tuned role, it is not ready yet.
- Move the example playbooks to /usr/share/doc/rhel-system-roles/$SUBSYSTEM
  directly to get rid of an extra directory.
- Depend on ansible.

* Thu May 4 2017  Pavel Cahyna <pcahyna@redhat.com> - 0-0.1.20170504
- Initial release.
- kdump r. fe8bb81966b60fa8979f3816a12b0c7120d71140
- postfix r. 43eec5668425d295dce3801216c19b1916df1f9b
- selinux r. 1e4a21f929455e5e76dda0b12867abaa63795ae7
- timesync r. 33a1a8c349de10d6281ed83d4c791e9177d7a141
- tuned r. 2e8bb068b9815bc84287e9b6dc6177295ffdf38b
- network r. 03ff040df78a14409a0d89eba1235b8f3e50a750

