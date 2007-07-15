%define name openarena
%define Summary An open-source content package for Quake III Arena
%define version 0.7.0
%define q3src ioq3-svn982
%define release %mkrel 3

%define oversion %(echo %{version} | sed -e 's/\\.//g')
%define gamelibdir %{_libdir}/games/%{name}

Summary: %{Summary}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://openarena.ws/rel/%{oversion}/ioq3-src-oa.tar.bz2
Source1: http://cheapy.deathmask.net/logo.gif
Source2: http://openarena.ws/svn/missionpack/ui/menudef.h
License: GPL/Creative Commons
Group: Games/Arcade
Url: http://openarena.ws/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: GL-devel
BuildRequires: SDL-devel
BuildRequires: openal-devel
BuildRequires: oggvorbis-devel
Requires: %{name}-data

%description
OpenArena is an open-source content package for Quake III Arena
licensed under the GPL, effectively creating a free stand-alone
game. You do not need Quake III Arena to play this game.

%prep
%setup -q -c
install -D %{SOURCE2} ui/menudef.h

%build
%make

%install
rm -rf %{buildroot}
%make copyfiles COPYDIR=%{buildroot}%{gamelibdir}
ln -s ../../../share/games/%{name}/baseoa %{buildroot}%{gamelibdir}

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
Encoding=UTF-8
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
if [ -d %{gamelibdir}/baseoa ]; then
   mv %{gamelibdir}/baseoa{,.rpmsave}
   ln -s baseoa.rpmsave %{gamelibdir}/baseoa
fi

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{gamelibdir}/*
%{_datadir}/icons/%{name}.gif
%{_datadir}/applications/mandriva-%{name}.desktop


