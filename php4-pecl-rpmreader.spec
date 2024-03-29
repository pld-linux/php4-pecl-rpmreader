%define		_modname	rpmreader
%define		_status		beta
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - RPM file meta information reader
Summary(pl.UTF-8):	%{_modname} - odczyt metainformacji z plików RPM
Name:		php4-pecl-%{_modname}
Version:	0.3
Release:	1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	73aca25e6f5b7b17dffe4dfb63110505
URL:		http://pecl.php.net/package/rpmreader/
BuildRequires:	php4-devel >= 3:4.3.0
BuildRequires:	rpmbuild(macros) >= 1.344
Requires:	php4-common >= 3:4.4.0-3
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rpmreader is an extension that provides the ability to read RPM
Package Manager (RPM) files' header information. This extension
currently does not provide the functionality to read the signature or
archive sections of the RPM file.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
rpmreader jest rozszerzeniem umożliwiającym odczyt informacji z
nagłówków plików RPM (RPM Package Manager). Rozszerzenie to na chwilę
obecną nie udostępnia możliwości odczytu podpisu ani zawartości
archiwum pliku RPM.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php4_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php4_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,examples}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
