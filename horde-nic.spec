
%define	_hordeapp nic
%define	_snap	2007-03-15
#define	_rc		rc1
%define	_rel	4

Summary:	NIC is a suite of simple network utilities
Summary(pl.UTF-8):	NIC - zestaw prostych narzędzi sieciowych
Name:		horde-%{_hordeapp}
Version:	0.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	BSD/GPL
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	7ff2eced2da9db82277bd875a83afb72
Source1:	%{_hordeapp}-apache.conf
Source2:	%{_hordeapp}-httpd.conf
URL:		http://www.horde.org/nic/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	tar >= 1:1.15.1
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	webapps
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq_pear	Horde.*

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
NIC is a suite of simple network utilities given a PHP web frontend.
The list of tools includes:
- Finger
- ICQ lookup
- DNS lookup
- Email address verification
- Ping
- SMTP open relay checking
- Service status
- Traceroute
- Whois

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with nic) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
NIC to zestaw prostych narzędzi sieciowych wyposażonych w interfejs
WWW napisany w PHP. Dostępne są następujące narzędzia:
- finger
- wyszukiwanie ICQ
- wyszukiwanie DNS
- weryfikacja adresów e-mail
- ping
- sprawdzanie SMTP pod kątem open relay
- stan usług
- traceroute
- whois

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla nic)
można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<-EOF
	IMPORTANT:
	If you are installing NIC for the first time, You may need to
	create the NIC database tables. To do so run:
	zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{_hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc LICENSE README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
