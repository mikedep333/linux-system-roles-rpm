Name: rhel-system-roles
Summary: Set of interfaces for unified system management
Version: 0.6
Release: 1%{?dist}

#Group: Development/Libraries
License: GPLv3+ and MIT and BSD
%global rolecompatprefix rhel-system-roles.
%global roleprefix linux-system-roles.

%global commit0 fe8bb81966b60fa8979f3816a12b0c7120d71140
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global rolename0 kdump
%global version0 0.1

%global commit1 43eec5668425d295dce3801216c19b1916df1f9b
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global rolename1 postfix
%global version1 0.1

%global commit2 ebcb133649fb5aba5bf0b7a64f2db2b90aadda1b
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global rolename2 selinux
#%%global version2 0.1

%global commit3 33a1a8c349de10d6281ed83d4c791e9177d7a141
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global rolename3 timesync
%global version3 0.1

%global commit5 b856c7481bf5274d419f71fb62029ea0044b3ec1
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global rolename5 network
%global version5 0.4


Source: https://github.com/linux-system-roles/%{rolename0}/archive/%{version0}.tar.gz#/%{rolename0}-%{version0}.tar.gz
Source1: https://github.com/linux-system-roles/%{rolename1}/archive/%{version1}.tar.gz#/%{rolename1}-%{version1}.tar.gz
Source2: https://github.com/linux-system-roles/%{rolename2}/archive/%{commit2}.tar.gz#/%{rolename2}-%{shortcommit2}.tar.gz
Source3: https://github.com/linux-system-roles/%{rolename3}/archive/%{version3}.tar.gz#/%{rolename3}-%{version3}.tar.gz
Source5:  https://github.com/linux-system-roles/%{rolename5}/archive/%{version5}.tar.gz#/%{rolename5}-%{version5}.tar.gz

Source6: timesync-playbook.yml
Source7: timesync-pool-playbook.yml

Patch1: rhel-system-roles-%{rolename1}-prefix.diff
Patch2: rhel-system-roles-%{rolename2}-prefix.diff
Patch3: rhel-system-roles-%{rolename3}-prefix.diff
Patch5: rhel-system-roles-%{rolename5}-prefix.diff

Patch101: rhel-system-roles-kdump-ssh.diff

Url: https://github.com/linux-system-roles/
BuildArch: noarch

%description
Collection of interfaces serving as a stable API for the management
of the RHEL operating system across major releases, implemented
using Ansible.


%prep
%setup -qc -b1 -b2 -b3 -b5
cd %{rolename0}-%{version0}
%patch101 -p1
cd ..
cd %{rolename1}-%{version1}
%patch1 -p1
cd ..
cd %{rolename2}-%{commit2}
%patch2 -p1
cd ..
cd %{rolename3}-%{version3}
%patch3 -p1
cd ..
cd %{rolename5}-%{version5}
%patch5 -p1
cd ..

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

cp -pR %{rolename0}-%{version0}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}%{rolename0}
cp -pR %{rolename1}-%{version1}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}%{rolename1}
cp -pR %{rolename2}-%{commit2}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}%{rolename2}
cp -pR %{rolename3}-%{version3}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}%{rolename3}
cp -pR %{rolename5}-%{version5}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}%{rolename5}

ln -s    %{rolecompatprefix}%{rolename0}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename0}
ln -s    %{rolecompatprefix}%{rolename1}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename1}
ln -s    %{rolecompatprefix}%{rolename2}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename2}
ln -s    %{rolecompatprefix}%{rolename3}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename3}
ln -s    %{rolecompatprefix}%{rolename5}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename5}

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kdump
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/postfix
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
install -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-playbook.yml
install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-pool-playbook.yml
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/network

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}kdump/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}kdump/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kdump

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}postfix/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}postfix/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/postfix

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}selinux/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}selinux/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}selinux/selinux-playbook.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux/example-selinux-playbook.yml

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}timesync/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}timesync/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/bond-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/bridge-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bridge-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/eth-simple-auto.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth-simple-auto-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/eth-with-vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth-with-vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/infiniband.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-infiniband-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/inventory \
   $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-inventory

rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/test/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/roles/network
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples/roles
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolecompatprefix}network/examples

%files
%dir %{_datadir}/ansible
%dir %{_datadir}/ansible/roles
%{_datadir}/ansible/roles/%{roleprefix}kdump
%{_datadir}/ansible/roles/%{roleprefix}postfix
%{_datadir}/ansible/roles/%{roleprefix}selinux
%{_datadir}/ansible/roles/%{roleprefix}timesync
%{_datadir}/ansible/roles/%{roleprefix}network
%{_datadir}/ansible/roles/%{rolecompatprefix}kdump
%{_datadir}/ansible/roles/%{rolecompatprefix}postfix
%{_datadir}/ansible/roles/%{rolecompatprefix}selinux
%{_datadir}/ansible/roles/%{rolecompatprefix}timesync
%{_datadir}/ansible/roles/%{rolecompatprefix}network
%doc %{_pkgdocdir}/*/example-*-playbook.yml
%doc %{_pkgdocdir}/network/example-inventory
%doc %{_pkgdocdir}/*/README.md
%doc %{_datadir}/ansible/roles/%{rolecompatprefix}kdump/README.md
%doc %{_datadir}/ansible/roles/%{rolecompatprefix}postfix/README.md
%doc %{_datadir}/ansible/roles/%{rolecompatprefix}selinux/README.md
%doc %{_datadir}/ansible/roles/%{rolecompatprefix}timesync/README.md
%doc %{_datadir}/ansible/roles/%{rolecompatprefix}network/README.md


%license %{_pkgdocdir}/*/COPYING
%license %{_datadir}/ansible/roles/%{rolecompatprefix}kdump/COPYING
%license %{_datadir}/ansible/roles/%{rolecompatprefix}postfix/COPYING
%license %{_datadir}/ansible/roles/%{rolecompatprefix}selinux/COPYING
%license %{_datadir}/ansible/roles/%{rolecompatprefix}timesync/COPYING
%license %{_datadir}/ansible/roles/%{rolecompatprefix}network/COPYING

%changelog
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

