Summary:	Mono IDE
Summary(pl):	IDE dla Mono
Name:		monodevelop
Version:	0.4
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://go-mono.com/archive/beta2/%{name}-%{version}.tar.gz
# Source0-md5:	b57c29af39bfc44842799cc211d6564d
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
URL:		http://www.monodevelop.com/
BuildRequires:	ORBit2-devel >= 2.8.3
BuildRequires:	autoconf
BuildRequires:	automake >= 1.7
BuildRequires:	dotnet-gtk-sharp-devel >= 0.93
BuildRequires:	dotnet-gtksourceview-sharp-devel >= 0.3
BuildRequires:	libtool
BuildRequires:	mono-csharp
BuildRequires:	mono-devel >= 0.95
BuildRequires:	monodoc >= 0.16
BuildRequires:	dotnet-gecko-sharp-devel >= 0.4
BuildRequires:	sed >= 4.0
BuildRequires:	shared-mime-info
Requires:	dotnet-gtksourceview-sharp
Requires(post,postun):	shared-mime-info
Obsoletes:	MonoDevelop
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
MonoDevelop to IDE (zintegrowane �rodowisko programisty) dla Mono we
wczesnym, ale szybko post�puj�cym stadium rozwoju. Ma wiele
mo�liwo�ci, a w�r�d nich:
- zarz�dzanie klasami
  MonoDevelop ma przegl�dark� klas pozwalaj�c� wy�wietla� klasy w
  projekcie, ich metody oraz w�asno�ci. Przestrzenie nazw s�
  uwzgl�dniane, aby zachowa� separacj� klas. Przy dodawaniu czego� do
  projektu jest to automatycznie dodawane do przegl�darki klas, nawet
  je�li s� to przestrzenie nazw, klasy, metody, a nawet zmienne.
- dope�nianie kodu
  Przy po��czeniu szkielet�w .NET i Gtk# pami�tanie samemu wszystkich
  klas, metod i w�asno�ci mog�oby by� nie lada wyzwaniem. MonoDevelop
  w spos�b inteligentny pr�buje dope�nia� to, co si� pisze. Je�li
  znajdzie dopasowanie, wystarczy nacisn�� tabulacj�, aby doko�czy�
  pisa� za nas.
- obs�uga projekt�w
  MonoDevelop przychodzi z wbudowanymi projektami, pomagaj�cymi zacz��
  tworzy� aplikacje konsolowe, Gnome# albo Gtk#.

%prep
%setup -q
%patch0 -p1
# ignore errors from it
sed -e 's/update-mime-database/-&/' -i Makefile.am

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
update-mime-database %{_datadir}/mime

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
