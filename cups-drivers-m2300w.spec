%define rname m2300w

Summary:	Konica Minolta magicolor 2300W and 2400W Printer Driver
Name:		cups-drivers-%{rname}
Version:	0.51
Release:	13
License:	GPLv2
Group:		System/Printing
Url:		http://sourceforge.net/projects/m2300w/
Source0:	http://downloads.sourceforge.net/m2300w/%{rname}-%{version}.tar.gz
Patch0:		m2300w-0.3-noppdbuild.patch
Patch1:		m2300w-0.2-ppc-build-fix.patch
Patch2:		m2300w-0.51-LDFLAGS.diff
Requires:	cups
Requires:	foomatic-db-engine

%description
The m2300w driver is a Linux printer driver for the Konica Minolta magicolor
2300W and 2400W color laser printers. It is intended for being used in
conjunction with ghostscript, foomatic and CUPS.

This package contains CUPS drivers (PPD) for the following printers:

 o Minolta magicolor 2300W
 o Minolta magicolor 2400W

%prep

%setup -qn %{rname}-%{version}
%patch0 -p0
%patch1 -p0 -b .ppc
%patch2 -p0

rm -f configure
autoconf

%build
%configure2_5x

# Omit the installation of the PPD in the Makefile, we use the Foomatic
# XML data
sed -i -e "s/src psfiles foomatic ppd/src psfiles/" Makefile
%make

%install
install -d %{buildroot}%{_datadir}/foomatic/db/source/{driver,opt,printer}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}

%makeinstall INSTROOT=%{buildroot}

for dir in driver opt printer; do
    install -c -m 644 foomatic/$dir/*.xml %{buildroot}%{_datadir}/foomatic/db/source/$dir/
done

install -m0644 ppd/*.ppd %{buildroot}%{_datadir}/cups/model/%{rname}/

# cleanup
rm -rf %{buildroot}%{_datadir}/doc

%files
%doc COPYING INSTALL README README.ghostscript
%{_bindir}/%{rname}
%{_bindir}/%{rname}-wrapper
%{_bindir}/m2400w
%{_datadir}/%{rname}
%{_datadir}/foomatic/db/source/opt/*.xml
%{_datadir}/foomatic/db/source/printer/*.xml
%{_datadir}/foomatic/db/source/driver/*.xml
%dir %{_datadir}/cups/model/%{rname}
%{_datadir}/cups/model/%{rname}/magicolor_2300W-%{rname}.ppd*
%{_datadir}/cups/model/%{rname}/magicolor_2400W-m2400w.ppd*

