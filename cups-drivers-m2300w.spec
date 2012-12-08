%define rname m2300w

Summary:	Konica Minolta magicolor 2300W and 2400W Printer Driver
Name:		cups-drivers-%{rname}
Version:	0.51
Release:	%mkrel 13
License:	GPL
Group:		System/Printing
URL:		http://sourceforge.net/projects/m2300w/
Source0:	http://downloads.sourceforge.net/m2300w/%{rname}-%{version}.tar.gz
Patch0:		m2300w-0.3-noppdbuild.patch
Patch1:		m2300w-0.2-ppc-build-fix.patch
Patch2:		m2300w-0.51-LDFLAGS.diff
Requires:	foomatic-db-engine
Requires:	cups
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
Conflicts:	foomatic-db < 1:3.0.2-1.20070820.1mdv2008.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The m2300w driver is a Linux printer driver for the Konica Minolta magicolor
2300W and 2400W color laser printers. It is intended for being used in
conjunction with ghostscript, foomatic and CUPS.

This package contains CUPS drivers (PPD) for the following printers:

 o Minolta magicolor 2300W
 o Minolta magicolor 2400W

%prep

%setup -q -n %{rname}-%{version}
%patch0 -p0
%patch1 -p0 -b .ppc
%patch2 -p0

%build
rm -f configure
autoconf
%configure2_5x

# Omit the installation of the PPD in the Makefile, we use the Foomatic
# XML data
perl -p -i -e "s/src psfiles foomatic ppd/src psfiles/" Makefile
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/foomatic/db/source/{driver,opt,printer}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}

%makeinstall INSTROOT=%{buildroot}

for dir in driver opt printer; do
    install -c -m 644 foomatic/$dir/*.xml %{buildroot}%{_datadir}/foomatic/db/source/$dir/
done

install -m0644 ppd/*.ppd %{buildroot}%{_datadir}/cups/model/%{rname}/

# cleanup
rm -rf %{buildroot}%{_datadir}/doc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING INSTALL README README.ghostscript
%attr(0755,root,root) %{_bindir}/%{rname}
%attr(0755,root,root) %{_bindir}/%{rname}-wrapper
%attr(0755,root,root) %{_bindir}/m2400w
%{_datadir}/%{rname}
%attr(0644,root,root) %{_datadir}/foomatic/db/source/opt/*.xml
%attr(0644,root,root) %{_datadir}/foomatic/db/source/printer/*.xml
%attr(0644,root,root) %{_datadir}/foomatic/db/source/driver/*.xml
%attr(0755,root,root) %dir %{_datadir}/cups/model/%{rname}
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/magicolor_2300W-%{rname}.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/magicolor_2400W-m2400w.ppd*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.51-11mdv2011.0
+ Revision: 663440
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.51-10mdv2011.0
+ Revision: 603872
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.51-9mdv2010.1
+ Revision: 518844
- rebuild

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.51-8mdv2010.0
+ Revision: 413288
- rebuild

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 0.51-7mdv2009.1
+ Revision: 318072
- rediffed one fuzzy patch
- use %%ldflags

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.51-6mdv2009.0
+ Revision: 220542
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 0.51-5mdv2008.1
+ Revision: 149150
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 30 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 0.51-4mdv2008.0
+ Revision: 76061
- Added conflicts to foomatic-db < 1:3.0.2-1.20070820.1mdv2008.0

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-3mdv2008.0
+ Revision: 75329
- fix deps (pixel)

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-2mdv2008.0
+ Revision: 64150
- use the new System/Printing RPM GROUP

* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-1mdv2008.0
+ Revision: 62510
- Import cups-drivers-m2300w



* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 0.51-1mdv2008.0
- initial Mandriva package
