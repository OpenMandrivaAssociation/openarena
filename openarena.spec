%define data_version	0.8.1
%define oversion	%(echo %{version} | sed -e 's/\\.//g')
%define gamelibdir	%{_libdir}/games/%{name}

Summary:	An open-source content package for Quake III Arena
Name:		openarena
Version:	0.8.8
Release:	%mkrel 2
Source0:	http://openarena.ws/svn/source/%{oversion}/%{name}-engine-source-%{version}.tar.bz2
Source1:	http://cheapy.deathmask.net/logo.gif
Patch0:		openarena-0.8.8-stack.patch
License:	GPLv2+
Group:		Games/Arcade
URL:		http://openarena.ws/
BuildRequires:	GL-devel
BuildRequires:	SDL-devel
BuildRequires:	openal-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	imagemagick
BuildRequires:	curl-devel
Requires:	%{name}-data >= %{data_version}

%description
OpenArena is an open-source content package for Quake III Arena
licensed under the GPL, effectively creating a free stand-alone
game. You do not need Quake III Arena to play this game.

%prep
%setup -q -n %{name}-engine-source-%{version}
%patch0 -p1

%build
%setup_compile_flags
# ATM serverbuild breaks build in Cooker
#serverbuild

%make	USE_CURL=1 \
	USE_CURL_DLOPEN=0 \
	USE_OPENAL=1 \
	USE_OPENAL_DLOPEN=0 \
	USE_CODEC_VORBIS=1 \
	V=1 \
	DEFAULT_BASEDIR=%{_gamesdatadir}/%{name} \
	FULLBINEXT=''

%install
%make copyfiles COPYDIR=%{buildroot}%{_gamesbindir} NO_STRIP=1 FULLBINEXT=''

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

%files
%{_gamesbindir}/%{name}
%{_gamesbindir}/oa_ded
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
