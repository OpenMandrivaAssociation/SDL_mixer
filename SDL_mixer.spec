%define	name	SDL_mixer
%define	version	1.2.7
%define	rel	4
%define	lib_name_orig lib%{name}
%define	lib_major 1.2
%define	lib_name %mklibname %{name} %{lib_major}

Summary:	Simple DirectMedia Layer - mixer
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.bz2
Patch1:		SDL_mixer-1.2.7-fix-path-timidity.patch
Patch2:		SDL_mixer-1.2.7-link-against-system-libmikmod.patch
Patch3:		SDL_mixer-1.2.7-timidity-crash.patch
Patch4:		SDL_mixer-1.2.4-64bit-fix.patch
Patch5:		SDL_mixer-1.2.5-endian-fixes.patch
License:	LGPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.libsdl.org/projects/SDL_mixer/
BuildRequires:	SDL-devel >= 1.2.10
BuildRequires:	esound-devel
BuildRequires:	libmikmod-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	smpeg-devel >= 0.4.3

%description
SDL_mixer is a sample multi-channel audio mixer library. It supports any
number of simultaneously playing channels of 16 bit stereo audio, plus a
single channel of music, mixed by the popular MikMod MOD, Timidity MIDI
and SMPEG MP3 libraries.

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Requires:	SDL-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}%{lib_major}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%{name}-player
Summary:	Players using %{name}
Group:		System/Libraries
Obsoletes:	%{lib_name}-test
Provides:	%{lib_name}-test
Requires:	%{lib_name} >= 1.2.6-2mdk

%description -n	%{name}-player
This package contains binary to test the associated library.

%prep
%setup -q
%patch1 -p1 -b .timidity
%patch2 -p1 -b .libmikmod
%patch3 -p0 -b .timidity_crash
%patch4 -p0 -b .64bit
%patch5 -p0 -b .endian

%build
#gw our libtool is too old
%define __cputoolize true
aclocal
autoconf
%configure2_5x	--enable-music-libmikmod \
		--enable-music-native-midi \
		--disable-music-ogg-shared \
		--disable-music-mp3-shared
%make

%install
rm -rf %{buildroot}
%makeinstall install-bin

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{name}-player
%defattr(-, root, root)
%doc README
%{_bindir}/playwave
%{_bindir}/playmus

%files -n %{lib_name}
%defattr(-,root,root)
%doc mikmod/AUTHORS mikmod/README
%doc timidity/FAQ timidity/README
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc README CHANGES
%{_libdir}/*a
%{_libdir}/lib*.so
%{_includedir}/SDL/*


