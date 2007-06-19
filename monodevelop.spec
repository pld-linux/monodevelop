#
# TODO:
#	- on x86-64: /usr/bin/monodevelop[60]: cd: /usr/lib/monodevelop/bin - No such file or directory
#	- segv on exit:
#		(MonoDevelop:696): Gtk-CRITICAL **: gtk_style_detach: assertion `style->attach_count > 0' failed
#		zsh: segmentation fault  monodevelop
#
# Conditional build:
%bcond_without	subversion	# disable subversion backend
#
%include	/usr/lib/rpm/macros.mono
Summary:	Mono IDE
Summary(pl.UTF-8):	IDE dla Mono
Name:		monodevelop
Version:	0.14
Release:	2
License:	GPL/MIT
Group:		Development/Tools
Source0:	http://go-mono.com/sources/monodevelop/%{name}-%{version}.tar.bz2
# Source0-md5:	b0062669981341523e81003eb3a70614
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
Patch1:		%{name}-locale_names.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-install.patch
Patch4:		%{name}-libdir.patch
URL:		http://www.monodevelop.com/
BuildRequires:	ORBit2-devel >= 2.8.3
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
BuildRequires:	desktop-file-utils
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gecko-sharp2-devel >= 0.10
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.9.0
BuildRequires:	dotnet-gtksourceview-sharp2-devel >= 0.10
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.1.13
BuildRequires:	monodoc >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
BuildRequires:	shared-mime-info
BuildRequires:	xsp
Requires(post,postun):	desktop-file-utils
Requires:	gtkhtml
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Requires:	libgtkembedmoz.so()(64bit)
%else
Requires:	libgtkembedmoz.so
%endif
Requires(post,postun):	shared-mime-info
%{?with_subversion:Requires:	subversion-libs}
Obsoletes:	MonoDevelop
ExcludeArch:	alpha i386 sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

mv po/ja{_JP,}.po
mv po/sl{_SI,}.po

%build
rm -rf autom4te.cache
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-update-mimedb \
	--disable-update-desktopdb \
	--enable-aspnet \
	%{?with_subversion:--enable-subversion}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database

%postun
%update_desktop_database_postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/mime/packages/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
