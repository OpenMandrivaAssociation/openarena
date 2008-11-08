%define data_version	0.8.1
%define oversion	%(echo %{version} | sed -e 's/\\.//g')
%define gamelibdir	%{_libdir}/games/%{name}

Summary:	An open-source content package for Quake III Arena
Name:		openarena
Version:	0.8.1
Release:	%{mkrel 1}
Source0:	http://openarena.ws/svn/source/%{oversion}/%{name}-engine-%{version}-1.tar.bz2
Source1:	http://cheapy.deathmask.net/logo.gif
License:	GPLv2+
Group:		Games/Arcade
URL:		http://openarena.ws/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	GL-devel
BuildRequires:	SDL-devel
BuildRequires:	openal-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	imagemagick
BuildRequires:	%{name}-data = %{data_version}
Requires:	%{name}-data = %{data_version}

%description
OpenArena is an open-source content package for Quake III Arena
licensed under the GPL, effectively creating a free stand-alone
game. You do not need Quake III Arena to play this game.

%prep
%setup -q -n %{name}-engine-%{version}

%build
%make

%install
rm -rf %{buildroot}
%make copyfiles COPYDIR=%{buildroot}%{gamelibdir}
# symlink files from noarch package in arch-specific game dir
ln -sf %{_gamesdatadir}/%{name}/baseoa/* %{buildroot}%{gamelibdir}/baseoa

binary=`basename %{buildroot}%{gamelibdir}/openarena.*`

install -d %{buildroot}%{_gamesbindir}
cat > %{buildroot}%{_gamesbindir}/%{name} <<EOF
#!/bin/sh
cd %{gamelibdir}
exec ./$binary \$*
EOF
chmod 755 %{buildroot}%{_gamesbindir}/%{name}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
convert -scale 128x128 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
convert -scale 64x64 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert -scale 48x48 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=OpenArena
Comment=Quake 3: Arena-like FPS game
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%pretrans
if [ -L %{gamelibdir}/baseoa ]; then
   rm -f %{gamelibdir}/baseoa
fi

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%dir %{gamelibdir}
%{gamelibdir}/missionpack
%{gamelibdir}/oa_ded.*
%{gamelibdir}/openarena.*
%dir %{gamelibdir}/baseoa
%{gamelibdir}/baseoa/*.pk3
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
