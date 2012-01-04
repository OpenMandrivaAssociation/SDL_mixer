%define	major 0
%define apiver 1.2
%define	libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d
%define version 1.2.11

Summary:	Simple DirectMedia Layer - mixer
Name:		SDL_mixer
Version:	%{version}
Release:	%mkrel 8
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz
Patch0:		SDL_mixer-1.2.11-music-crash-fix.patch
BuildRequires:	SDL-devel >= 1.2.10
BuildRequires:	esound-devel
BuildRequires:	libmikmod-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libz-devel
BuildRequires:	nas-devel
BuildRequires:	smpeg-devel >= 0.4.3
BuildRequires:	libflac-devel
BuildRequires:	libstdc++-static-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

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
Requires:	SDL-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}%{apiver}-devel = %{version}-%{release}
Obsoletes:	%{_lib}SDL_mixer1.2-devel < 1.2.10

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{name}-player
Summary:	Players using %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}SDL_mixer-test < 1.2.10
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-player
This package contains binary to test the associated library.

%prep

%setup -q
%patch0 -p0

%build
# (Anssi 02/2010) The below --disable-music-foo-shared options do not disable
# support for the format in question. They just disable dlopen, and using the
# shared libraries directly, allowing rpm autodeps to work. Just using dlopen
# on them would make it quite likely that adding the deps later on downstream
# packages using SDL_mixer manually would be forgotten.
%configure2_5x	--enable-music-libmikmod=yes \
		--enable-music-native-midi \
		--disable-music-ogg-shared \
		--disable-music-flac-shared \
		--disable-music-mod-shared \
		--disable-music-mp3-shared
%make

iconv -f ISO-8859-1 -t UTF-8 CHANGES > CHANGES.tmp
touch -r CHANGES CHANGES.tmp
mv CHANGES.tmp CHANGES

%install
rm -rf %{buildroot}
%makeinstall_std install-bin

%if "%{_lib}" == "lib64"
perl -pi -e "s|-L/usr/lib\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/*.la
%endif

%clean
rm -rf %{buildroot}

%files -n %{name}-player
%defattr(-, root, root)
%doc README
%{_bindir}/playwave
%{_bindir}/playmus

%files -n %{libname}
%defattr(-,root,root)
##%doc mikmod/AUTHORS mikmod/README
%doc timidity/FAQ timidity/README
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc README CHANGES
%{_libdir}/*a
%{_libdir}/lib*.so
%{_includedir}/SDL/*
%{_libdir}/pkgconfig/%{name}.pc
