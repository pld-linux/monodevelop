%include	/usr/lib/rpm/macros.mono
Summary:	Mono IDE
Summary(pl):	IDE dla Mono
Name:		monodevelop
Version:	0.8
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://go-mono.com/sources/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	23f7c636b8e9533799a33bdf25c37bdd
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
Patch1:		%{name}-locale_names.patch
#Patch2:		%{name}-libdir.patch
#Patch3:		%{name}-desktop.patch
Patch4:		%{name}-install.patch
URL:		http://www.monodevelop.com/
BuildRequires:	ORBit2-devel >= 2.8.3
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.7
BuildRequires:	dotnet-gecko-sharp2-devel >= 0.10
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.5.92
BuildRequires:	dotnet-gtksourceview-sharp-devel >= 0.10
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.1
BuildRequires:	monodoc >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	shared-mime-info
Requires:	mozilla-embedded
Requires(post,postun):	shared-mime-info
Obsoletes:	MonoDevelop
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mono IDE, in the very early stages of development right now, and
progressing quickly. MonoDevelop has many features. Some of these
include:
- Class Management
  MonoDevelop has a class viewer which allows you to list the classes
  in your project, their methods, and properties. Your namespaces are
  also kept track of to keep the classes separated. When you add
  something to your project, it will automatically be added to the
  class viewer, even if they're namespaces, classes, methods, or even
  variables.
- Code Completion
  With the .NET and Gtk# frameworks put together, it can be
  challenging to remember all the classes, methods, or properties that
  are at your disposal. MonoDevelop's intelligent code completion
  attempts to complete what you're typing. If it finds a match, just
  hit tab and MonoDevelop will do the typing for you.
- Project Support
  MonoDevelop comes with built in projects that help get you started
  with your console, Gnome# or Gtk# application.

%description -l pl
MonoDevelop to IDE (zintegrowane ¶rodowisko programisty) dla Mono we
wczesnym, ale szybko postêpuj±cym stadium rozwoju. Ma wiele
mo¿liwo¶ci, a w¶ród nich:
- zarz±dzanie klasami
  MonoDevelop ma przegl±darkê klas pozwalaj±c± wy¶wietlaæ klasy w
  projekcie, ich metody oraz w³asno¶ci. Przestrzenie nazw s±
  uwzglêdniane, aby zachowaæ separacjê klas. Przy dodawaniu czego¶ do
  projektu jest to automatycznie dodawane do przegl±darki klas, nawet
  je¶li s± to przestrzenie nazw, klasy, metody, a nawet zmienne.
- dope³nianie kodu
  Przy po³±czeniu szkieletów .NET i Gtk# pamiêtanie samemu wszystkich
  klas, metod i w³asno¶ci mog³oby byæ nie lada wyzwaniem. MonoDevelop
  w sposób inteligentny próbuje dope³niaæ to, co siê pisze. Je¶li
  znajdzie dopasowanie, wystarczy nacisn±æ tabulacjê, aby dokoñczy³
  pisaæ za nas.
- obs³uga projektów
  MonoDevelop przychodzi z wbudowanymi projektami, pomagaj±cymi zacz±æ
  tworzyæ aplikacje konsolowe, Gnome# albo Gtk#.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4	-p1
# ignore errors from it
#sed -e 's/update-mime-database/-&/' -i Makefile.am

mv po/ja{_JP,}.po

%build
rm -rf autom4te.cache
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-mime-database %{_datadir}/mime ||:

%postun
update-mime-database %{_datadir}/mime

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/mime/packages/*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
