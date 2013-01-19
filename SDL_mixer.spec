%define		major 0
%define		apiver 1.2
%define		libname %mklibname %{name} %{apiver} %{major}
%define		develname %mklibname %{name} -d

Name:		SDL_mixer
Version:	1.2.12
Release:	3
Summary:	Simple DirectMedia Layer - mixer
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz
Patch0:		SDL_mixer-MikMod-1.patch
Patch1:		SDL_mixer-MikMod-2.patch
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(esound)
BuildRequires:	libmikmod-devel
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	zlib-devel
BuildRequires:	nas-devel
BuildRequires:	smpeg-devel >= 0.4.3
BuildRequires:	pkgconfig(flac)
BuildRequires:	libstdc++-static-devel

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
%setup -q
%patch0 -p1
%patch1 -p1

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
		--disable-music-mp3-shared \
		--disable-static
%make

iconv -f ISO-8859-1 -t UTF-8 CHANGES > CHANGES.tmp
touch -r CHANGES CHANGES.tmp
%__mv CHANGES.tmp CHANGES

%install
%makeinstall_std install-bin

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

%changelog
* Mon Mar 19 2012 Andrey Bondrov <abondrov@mandriva.org> 1.2.12-1mdv2012.0
+ Revision: 785613
- New version 1.2.12, don't build static lib, update file list

* Wed Jan 04 2012 Andrey Bondrov <abondrov@mandriva.org> 1.2.11-8
+ Revision: 753220
- Rebuild for .la files issue

* Sun Aug 21 2011 Tomas Kindl <supp@mandriva.org> 1.2.11-7
+ Revision: 696013
- add patch that MAY help to fix #58059

* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.11-6
+ Revision: 686304
- avoid pulling 32 bit libraries on 64 bit arch

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 1.2.11-5
+ Revision: 672098
- add br

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 1.2.11-4mdv2011.0
+ Revision: 622468
- rebuild for new directfb

  + Tomas Kindl <supp@mandriva.org>
    - add provides for lib(64)SDL_mixer

* Wed Feb 17 2010 Frederic Crozat <fcrozat@mandriva.com> 1.2.11-3mdv2010.1
+ Revision: 507126
- force rebuild

* Mon Feb 15 2010 Anssi Hannula <anssi@mandriva.org> 1.2.11-2mdv2010.1
+ Revision: 506234
- do not use dlopen for music libraries to avoid missed dependencies on
  downstream packages and 3rdparty applications

* Fri Feb 05 2010 Tomas Kindl <supp@mandriva.org> 1.2.11-1mdv2010.1
+ Revision: 501019
- remove old/obsolete patches
- bump to 1.2.11, rendering most patches obsolete

* Sun Jan 03 2010 Funda Wang <fwang@mandriva.org> 1.2.8-12mdv2010.1
+ Revision: 485994
- rebuild

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 1.2.8-11mdv2010.1
+ Revision: 463086
- rebuild for new dfb

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.8-10mdv2010.0
+ Revision: 413010
- rebuild

  + Christophe Fergeau <cfergeau@mandriva.com>
    - remove unneeded calls to autoconf/aclocal/libtoolize
    - add missing -lm in linker flags

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.8-9mdv2009.1
+ Revision: 301474
- rebuilt against new libxcb

* Thu Aug 14 2008 Götz Waschk <waschk@mandriva.org> 1.2.8-8mdv2009.0
+ Revision: 271781
- rebuild

* Sun Jul 27 2008 Götz Waschk <waschk@mandriva.org> 1.2.8-7mdv2009.0
+ Revision: 250614
- patch for bug #42160 (double free error)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 30 2008 Funda Wang <fwang@mandriva.org> 1.2.8-6mdv2009.0
+ Revision: 213219
- BR libz

* Mon Mar 10 2008 Olivier Blin <blino@mandriva.org> 1.2.8-5mdv2008.1
+ Revision: 183454
- remove pulseaudio-devel requirement in devel package
  (SDL is not dynamically linked with pulseaudio anymore)

* Fri Mar 07 2008 Olivier Blin <blino@mandriva.org> 1.2.8-4mdv2008.1
+ Revision: 181200
- explicitely require pulseaudio-devel in devel package
  (find-requires does not parse .la files, #38653, breaks toppler build)

* Sun Jan 13 2008 Anssi Hannula <anssi@mandriva.org> 1.2.8-3mdv2008.1
+ Revision: 151077
- obsolete old library name
- provide %%name-devel
- versionize obsoletes
- do not provide old -devel name
- fix wrongly changed obsoletes of player subpkg
- fix typo in versioned requires of -devel

* Sun Jan 13 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.8-2mdv2008.1
+ Revision: 150946
- new license policy
- new devel library policy
- spec file clean
- correct libification

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jul 26 2007 Funda Wang <fwang@mandriva.org> 1.2.8-1mdv2008.0
+ Revision: 55751
- New version

* Thu May 31 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.2.7-6mdv2008.0
+ Revision: 33460
- Rebuild with libslang2.

* Mon May 21 2007 Funda Wang <fwang@mandriva.org> 1.2.7-5mdv2008.0
+ Revision: 29147
- Rebuild for new directfb


* Sat Feb 24 2007 Giuseppe Ghibò <ghibo@mandriva.com> 1.2.7-4mdv2007.0
+ Revision: 125375
- Rebuilt against libgii|libggi.

  + Per Øyvind Karlsen <pkarlsen@mandriva.com>
    - ouch, fix libmikmod patch
    - versioned provides for %%{name}-devel
    - link against smpeg, otherwise it won't pull in required dependency
      link against system libmikmod (P2, derived from debian, then fixed)
      fix timidity crash (P3, from SuSE)
      64 bit fixes (P4, from SuSE)
      endian fixes (P5, from SuSE)
    - Import SDL_mixer

* Sun Jun 25 2006 G�tz Waschk <waschk@mandriva.org> 1.2.7-1mdv2007.0
- fix installation
- bump deps
- update patch 1
- New release 1.2.7

* Tue May 16 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2.6-4mdk
- rebuild for sparc

* Sat Jan 07 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2.6-3mdk
- make rpmbuildupdate aware
- BuildRequires: libmikmod-devel

* Sat Oct 15 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.6-2mdk
- update, fix and reenable timidity patch (P1) (why was it disabled?)
- make the player require the library on release as there are fixes
  in the library for it to play midi
- %%mkrel
- drop gcc3.3 (P2) and 64 bit (P3) patches as they're no longer used
- drop copyright docs
- cosmetics

* Wed Mar 23 2005 Giuseppe Ghib� <ghibo@mandrakesoft.com> 1.2.6-1mdk
- Release: 1.2.6.

* Sat Nov 13 2004 Götz Waschk <waschk@linux-mandrake.com> 1.2.5-5mdk
- rebuild

* Fri Jul 30 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.5-4mdk
- merged Gwenole 64-bit fixes from 1.2.5-3.1mdk (AMD64).

