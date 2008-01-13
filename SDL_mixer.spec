%define	major 0
%define apiver 1.2
%define	libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d

Summary:	Simple DirectMedia Layer - mixer
Name:		SDL_mixer
Version:	1.2.8
Release:	%mkrel 3
License:	LGPLv+2
Group:		System/Libraries
URL:		http://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.bz2
Patch1:		SDL_mixer-1.2.7-fix-path-timidity.patch
Patch2:		SDL_mixer-1.2.7-link-against-system-libmikmod.patch
Patch3:		SDL_mixer-1.2.7-timidity-crash.patch
Patch4:		SDL_mixer-1.2.4-64bit-fix.patch
Patch5:		SDL_mixer-1.2.5-endian-fixes.patch
BuildRequires:	SDL-devel >= 1.2.10
BuildRequires:	esound-devel
BuildRequires:	libmikmod-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	smpeg-devel >= 0.4.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SDL_mixer is a sample multi-channel audio mixer library. It supports any
number of simultaneously playing channels of 16 bit stereo audio, plus a
single channel of music, mixed by the popular MikMod MOD, Timidity MIDI
and SMPEG MP3 libraries.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}SDL_mixer1.2 < 1.2.8-2

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
Obsoletes:	%{_lib}SDL_mixer1.2-devel < 1.2.8-2

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{name}-player
Summary:	Players using %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}SDL_mixer-test < 1.2.8-3
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-player
This package contains binary to test the associated library.

%prep
%setup -q
%patch1 -p1 -b .timidity
#patch2 -p1 -b .libmikmod
#patch3 -p0 -b .timidity_crash
%patch4 -p0 -b .64bit
#patch5 -p0 -b .endian

%build
#gw our libtool is too old
%define __cputoolize true
aclocal
autoconf
%configure2_5x	--enable-music-libmikmod=yes \
		--enable-music-native-midi \
		--disable-music-ogg-shared \
		--disable-music-mp3-shared
%make

%install
rm -rf %{buildroot}
%makeinstall_std install-bin

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{name}-player
%defattr(-, root, root)
%doc README
%{_bindir}/playwave
%{_bindir}/playmus

%files -n %{libname}
%defattr(-,root,root)
%doc mikmod/AUTHORS mikmod/README
%doc timidity/FAQ timidity/README
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc README CHANGES
%{_libdir}/*a
%{_libdir}/lib*.so
%{_includedir}/SDL/*
