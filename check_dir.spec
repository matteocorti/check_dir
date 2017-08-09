################################################################################
# File version information:
# $Id: check_updates.spec 1249 2011-05-25 08:27:23Z corti $
# $Revision: 1249 $
# $HeadURL: https://svn.id.ethz.ch/nagios_plugins/check_updates/check_updates.spec $
# $Date: 2011-05-25 10:27:23 +0200 (Wed, 25 May 2011) $
################################################################################

%define version 3.0.0
%define release 1
%define sourcename       check_dir
%define packagename      nagios-plugins-check-dir
%define nagiospluginsdir %{_libdir}/nagios/plugins

# No binaries in this package
%define debug_package    %{nil}

Summary:       Nagios plugin to monitor the number of files in one or more directories.
Name:          %{packagename}
Obsoletes:     check_dir
Version:       %{version}
Release:       %{release}%{?dist}
License:       GPLv3+
Packager:      Matteo Corti <matteo.corti@id.ethz.ch>
Group:         Applications/System
BuildRoot:     %{_tmppath}/%{packagename}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:           https://trac.id.ethz.ch/projects/nagios_plugins/wiki/check_dir
Source:        https://trac.id.ethz.ch/projects/nagios_plugins/downloads/%{sourcename}-%{version}.tar.gz
BuildArch:     noarch

# Fedora build requirement (not needed for EPEL{4,5})

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: perl(Module::Install)
BuildRequires: perl(Monitoring::Plugin)

# Monitoring::Plugin package dependencies are slightly broken on EL6 and don't pull these in (rhbz#1479748)
%if 0%{?rhel} == 6
BuildRequires: perl(Class::Accessor::Fast)
BuildRequires: perl(Config::Tiny)
Requires:      perl(Class::Accessor::Fast)
Requires:      perl(Config::Tiny)
%endif

Requires:      nagios-plugins

%description
Nagios plugin to monitor the number of files in one or more directories.

%prep
%setup -q -n %{sourcename}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor \
    INSTALLSCRIPT=%{nagiospluginsdir} \
    INSTALLVENDORSCRIPT=%{nagiospluginsdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name "*.pod" -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc AUTHORS Changes NEWS README INSTALL TODO COPYING COPYRIGHT
%{nagiospluginsdir}/%{sourcename}
%{_mandir}/man1/%{sourcename}.1*

%changelog
* Wed Aug 09 2017 Matt Dainty <matt@bodgit-n-scarper.com> - 3.0.0-1
- Small fixes to spec file for building on EL6/7

* Wed Jun 29 2011 Matteo Corti <matteo.corti@id.ethz.ch> - 3.0.0-0
- Fixed the build (plugin name, files, dependencies, ...)

* Fri Mar 21 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.5-0
- fixed the missing usage message

* Thu Mar 20 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.4-0
- added -d (which was automatic w/o the option bundling introduced in 2.1.3)

* Thu Mar 20 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.3-0
- short command line options can be bundled and are case sensitive

* Thu Mar 20 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.2-0
- ePN compatibility

* Tue Mar 18 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.1-0
- added more sanity checks

* Tue Mar 18 2008 Matteo Corti <matteo.corti@id.ethz.ch> - 2.1.0-0
- accepts ranges for -c and -w

* Mon Sep 24 2007 Matteo Corti <matteo.corti@id.ethz.ch> - 1.2-0
- first RPM package
