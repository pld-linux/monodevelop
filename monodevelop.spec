# TODO: use system libgit2, libgit2sharp, nunit, mono-addins
#
# Conditional build:
%bcond_without	subversion	# disable subversion backend
#
%include	/usr/lib/rpm/macros.mono
#
Summary:	Mono IDE
Summary(pl.UTF-8):	IDE dla Mono
Name:		monodevelop
Version:	5.10.0.871
Release:	3
# most of code is MIT-licensed, some parts LGPL v2
License:	LGPL v2, MIT
Group:		Development/Tools
Source0:	http://download.mono-project.com/sources/monodevelop/%{name}-%{version}.tar.bz2
# Source0-md5:	4722cbbaeb7a518dceea8147e6cb6181
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-aspnet.patch
Patch2:		%{name}-nunit.patch
Patch3:		%{name}-avoidgiterrors.patch
Patch4:		%{name}-nuget-unbundle.patch
Patch5:		%{name}-no-nuget-packages.patch
Patch6:		%{name}-json.patch
URL:		http://monodevelop.com/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.10
# gconf-sharp, gnome-sharp, gnome-vfs-sharp
BuildRequires:	dotnet-gconf-sharp-devel
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.12.8
BuildRequires:	dotnet-newtonsoft-json-devel >= 6.0
BuildRequires:	dotnet-nuget-devel
BuildRequires:	dotnet-nunit2 >= 2.6.4
BuildRequires:	gettext-tools
BuildRequires:	mono-csharp >= 3.0.4
BuildRequires:	monodoc >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	dotnet-gtk-sharp2 >= 2.12.8
Requires:	hicolor-icon-theme
Requires:	pkgconfig
%{?with_subversion:Requires:	subversion-libs}
Requires:	xulrunner-libs
Suggests:	ctags
Suggests:	mono-compat-links >= 3.0.4
Suggests:	mono-csharp >= 3.0.4
Suggests:	monodoc >= 1.0
Suggests:	xsp
Obsoletes:	MonoDevelop
ExcludeArch:	alpha i386 sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'mono\\(System.Data.Entity\\)' 'mono\\(System.Web.WebPages.Deployment\\)'

%description
Mono IDE, in the very early stages of development right now, and
progressing quickly. MonoDevelop has many features. Some of these
include:
- Class Management MonoDevelop has a class viewer which allows you to
  list the classes in your project, their methods, and properties. Your
  namespaces are also kept track of to keep the classes separated. When
  you add something to your project, it will automatically be added to
  the class viewer, even if they're namespaces, classes, methods, or
  even variables.
- Code Completion With the .NET and Gtk# frameworks put together, it
  can be challenging to remember all the classes, methods, or properties
  that are at your disposal. MonoDevelop's intelligent code completion
  attempts to complete what you're typing. If it finds a match, just hit
  tab and MonoDevelop will do the typing for you.
- Project Support MonoDevelop comes with built in projects that help
  get you started with your console, Gnome# or Gtk# application.

%description -l pl.UTF-8
MonoDevelop to IDE (zintegrowane środowisko programisty) dla Mono we
wczesnym, ale szybko postępującym stadium rozwoju. Ma wiele
możliwości, a wśród nich:
- zarządzanie klasami MonoDevelop ma przeglądarkę klas pozwalającą
  wyświetlać klasy w projekcie, ich metody oraz własności. Przestrzenie
  nazw są uwzględniane, aby zachować separację klas. Przy dodawaniu
  czegoś do projektu jest to automatycznie dodawane do przeglądarki
  klas, nawet jeśli są to przestrzenie nazw, klasy, metody, a nawet
  zmienne.
- dopełnianie kodu Przy połączeniu szkieletów .NET i Gtk# pamiętanie
  samemu wszystkich klas, metod i własności mogłoby być nie lada
  wyzwaniem. MonoDevelop w sposób inteligentny próbuje dopełniać to, co
  się pisze. Jeśli znajdzie dopasowanie, wystarczy nacisnąć tabulację,
  aby dokończył pisać za nas.
- obsługa projektów MonoDevelop przychodzi z wbudowanymi projektami,
  pomagającymi zacząć tworzyć aplikacje konsolowe, Gnome# albo Gtk#.

%prep
%setup -q -n monodevelop-5.10
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -i -e 's,\.\./version\.config,version.config,' configure.in
# bash is needed because of exec -a; avoid hiding dependency by env
%{__sed} -i -e '1s,#!/usr/bin/env bash,#!/bin/bash,' mdtool.in monodevelop.in

# fake target
touch restore-packages

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-update-mimedb \
	--disable-update-desktopdb \
	%{?with_subversion:--enable-subversion}

cd external/libgit2sharp/Lib/CustomBuildTasks
xbuild CustomBuildTasks.csproj /property:Configuration=Release
ln -snf bin/Release/CustomBuildTasks.dll .
cd ../../../..

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
%{__mv} -f $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT%{_pkgconfigdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/mdtool
%attr(755,root,root) %{_bindir}/monodevelop
%{_prefix}/lib/monodevelop
%{_datadir}/mime/packages/monodevelop.xml
%{_desktopdir}/monodevelop.desktop
%{_pkgconfigdir}/monodevelop-core-addins.pc
%{_pkgconfigdir}/monodevelop.pc
%{_iconsdir}/hicolor/*x*/apps/monodevelop.png
%{_iconsdir}/hicolor/scalable/apps/monodevelop.svg
%{_mandir}/man1/mdtool.1*
%{_mandir}/man1/monodevelop.1*
