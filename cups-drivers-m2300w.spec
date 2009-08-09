%define rname m2300w

Summary:	Konica Minolta magicolor 2300W and 2400W Printer Driver
Name:		cups-drivers-%{rname}
Version:	0.51
Release:	%mkrel 8
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
