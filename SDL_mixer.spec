%define		major 0
%define		apiver 1.2
%define		libname %mklibname %{name} %{apiver} %{major}
%define		develname %mklibname %{name} -d
%define		_disable_lto 1

%global optflags %{optflags} -Wno-incompatible-function-pointer-types

Name:		SDL_mixer
Version:	1.2.12
Release:	21
Summary:	Simple DirectMedia Layer - mixer
License:	LGPLv2+
Group:		System/Libraries
URL:		https://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz
Patch0:		SDL_mixer-MikMod-1.patch
Patch1:		SDL_mixer-MikMod-2.patch
Patch2:		SDL_mixer-1.2.12-compile.patch
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	libmikmod-devel
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	zlib-devel
BuildRequires:	nas-devel
BuildRequires:	smpeg-devel >= 0.4.3
BuildRequires:	pkgconfig(flac)
BuildRequires:	libstdc++-static-devel
BuildRequires:	locales-extra-charsets

%description
SDL_mixer is a sample multi-channel audio mixer library. It supports any
number of simultaneously playing channels of 16 bit stereo audio, plus a
single channel of music, mixed by the popular MikMod MOD, Timidity MIDI
and SMPEG MP3 libraries.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}SDL_mixer1.2_0 < 1.2.10
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(sdl)
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}%{apiver}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{name}-player
Summary:	Players using %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-player
This package contains binary to test the associated library.

%prep
%autosetup -p1

%build
# (Anssi 02/2010) The below --disable-music-foo-shared options do not disable
# support for the format in question. They just disable dlopen, and using the
# shared libraries directly, allowing rpm autodeps to work. Just using dlopen
# on them would make it quite likely that adding the deps later on downstream
# packages using SDL_mixer manually would be forgotten.
%configure	--enable-music-libmikmod=yes \
		--enable-music-native-midi \
		--disable-music-ogg-shared \
		--disable-music-flac-shared \
		--disable-music-mod-shared \
		--disable-music-mp3-shared \
		--disable-static
%make_build

iconv -f ISO-8859-1 -t UTF-8 CHANGES > CHANGES.tmp
touch -r CHANGES CHANGES.tmp
%__mv CHANGES.tmp CHANGES

%install
%make_install install-bin

%files -n %{name}-player
%doc README
%{_bindir}/playwave
%{_bindir}/playmus

%files -n %{libname}
%doc timidity/FAQ timidity/README
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%doc README CHANGES
%{_libdir}/lib*.so
%{_includedir}/SDL/*
%{_libdir}/pkgconfig/%{name}.pc
