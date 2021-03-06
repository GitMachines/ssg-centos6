Name:           scap-security-guide
Version:        %{version}
Release:        %{release}
Summary:        Security guidance and baselines in SCAP formats.

Group:          Testing
License:        Public domain and GPL
URL:            https://fedorahosted.org/scap-security-guide/

Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	%{arch}

BuildRequires:  coreutils, libxslt, expat, python, openscap-utils >= 0.9.1, python-lxml
Requires:       filesystem, openscap-utils >= 0.9.1

%description
The scap-security-guide project provides security configuration guidance in
formats of the Security Content Automation Protocol (SCAP).  It provides a
catalog of practical hardening advice and links it to government requirements
where applicable. The project bridges the gap between generalized policy
requirements and specific implementation guidance.
%prep
%setup -q 


%build
cd RHEL6 && make dist


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/xml/scap/ssg/
mkdir -p $RPM_BUILD_ROOT/usr/share/man/en/man8/

# Add in core content (SCAP, guide, tables)
cp -r RHEL6/dist/* $RPM_BUILD_ROOT/usr/share/xml/scap/ssg/
cp JBossEAP5/eap5-* $RPM_BUILD_ROOT/usr/share/xml/scap/ssg/content/
cp JBossEAP5/docs/JBossEAP5_Guide.html $RPM_BUILD_ROOT/usr/share/xml/scap/ssg/guide/

# Add in manpage
gzip -c RHEL6/input/auxiliary/scap-security-guide.8 > $RPM_BUILD_ROOT/usr/share/man/en/man8/scap-security-guide.8.gz
makewhatis
chcon -u system_u $RPM_BUILD_ROOT/usr/share/man/en/man8/scap-security-guide.8.gz

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) /usr/share/xml/scap/ssg
%attr(0644,root,root) /usr/share/man/en/man8/scap-security-guide.8.gz


%changelog
* Wed Jun 26 2013 Shawn Wells <shawn@redhat.com> 0.1-12
- 

* Fri Apr 26 2013 Shawn Wells <shawn@redhat.com> 0.1-11
- Significant amount of OVAL bugfixes
- Incorporation of Draft RHEL6 STIG feedback

* Sat Feb 16 2013 Shawn Wells <shawn@redhat.com> 0.1-10
- SSG now includes JBoss EAP5 content!
- `man scap-security-guide`
- OVAL bug fixes
- NIST 800-53 mappings update

* Tue Nov 28 2012 Shawn Wells <shawn@redhat.com> 0.1-9
- Updated BuildRequires to reflect python-lxml (thank you, Ray S.!)
- Reverting to noarch RPM

* Tue Nov 27 2012 Shawn Wells <shawn@redhat.com> 0.1-8
- Significant copy editing to XCCDF rules per community
  feedback on the DISA RHEL6 STIG Initial Draft

* Thu Nov 1 2012 Shawn Wells <shawn@redhat.com> 0.1-7
- Corrected XCCDF content errors
- OpenSCAP now supports CPE dictionaries, important to
  utilize --cpe-dict when scanning machines with OpenSCAP,
  e.g.:
  $ oscap xccdf eval --profile stig-server \
   --cpe-dict ssg-rhel6-cpe-dictionary.xml ssg-rhel6-xccdf.xml

* Mon Oct 22 2012 Shawn Wells <shawn@redhat.com> 0.1-6
- Corrected RPM versioning, we're on 0.1 release 6 (not version 1 release 6)
- Updated RPM includes feedback received from DoD Consensus meetings

* Fri Oct 5  2012 Jeffrey Blank <blank@eclipse.ncsc.mil> 1.0-5
- Adjusted installation directory to /usr/share/xml/scap.

* Tue Aug 28  2012 Spencer Shimko <sshimko@tresys.com> 1.0-4
- Fix BuildRequires and Requires.

* Wed Jul 3 2012 Jeffrey Blank <blank@eclipse.ncsc.mil> 1.0-3
- Modified install section, made description more concise.

* Thu Apr 19 2012 Spencer Shimko <sshimko@tresys.com> 1.0-2
- Minor updates to pass some variables in from build system.

* Mon Apr 02 2012 Shawn Wells <shawn@redhat.com> 1.0-1
- First attempt at SSG RPM. May ${deity} help us...
