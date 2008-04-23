%define name openarena
%define Summary An open-source content package for Quake III Arena
%define version 0.7.6
%define data_version %{version}
%define q3src ioquake3svn1288
%define q3tar %{q3src}plus4
%define release %mkrel 2

%define oversion %(echo %{version} | sed -e 's/\\.//g')
%define gamelibdir %{_libdir}/games/%{name}

Summary: %{Summary}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://openarena.ws/svn/source/%{oversion}/%{q3tar}.tar.bz2
Source1: http://cheapy.deathmask.net/logo.gif
License: GPL/Creative Commons
Group: Games/Arcade
Url: http://openarena.ws/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: GL-devel
BuildRequires: SDL-devel
BuildRequires: openal-devel
BuildRequires: oggvorbis-devel
Requires: %{name}-data = %{data_version}
Requires: %{name}-data

%description
OpenArena is an open-source content package for Quake III Arena
licensed under the GPL, effectively creating a free stand-alone
game. You do not need Quake III Arena to play this game.

%prep
%setup -q -n %{q3src}

%build
%make

%install
rm -rf %{buildroot}
%make copyfiles COPYDIR=%{buildroot}%{gamelibdir}
# symlink files from noarch package in arch-specific game dir
ln -sf %{_gamesdatadir}/%{name}/baseoa/* %{buildroot}%{gamelibdir}/baseoa

binary=`basename %{buildroot}%{gamelibdir}/ioquake3.*`

install -d %{buildroot}%{_gamesbindir}
cat > %{buildroot}%{_gamesbindir}/%{name} <<EOF
#!/bin/sh
cd %{gamelibdir}
exec ./$binary \$*
EOF
chmod 755 $RPM_BUILD_ROOT%{_gamesbindir}/%{name}

install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons/%{name}.gif

install -d %{buildroot}%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=OpenArena
Comment=%{Summary}
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{_datadir}/icons/%{name}.gif
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf %{buildroot}

%pretrans
if [ -L %{gamelibdir}/baseoa ]; then
   rm -f %{gamelibdir}/baseoa
fi

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%dir %{gamelibdir}
%{gamelibdir}/io*.*
%dir %{gamelibdir}/baseoa
%{gamelibdir}/baseoa/*.so
%dir %{gamelibdir}/missionpack
%{gamelibdir}/missionpack/*.so
%{_datadir}/icons/%{name}.gif
%{_datadir}/applications/mandriva-%{name}.desktop


