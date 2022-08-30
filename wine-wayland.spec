%global debug_package   %{nil}

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

#%%define _smp_mflags -j1

%global no64bit   0
%global winegecko 2.47.2
%global winemono  6.2.0
%global _default_patch_fuzz 2
%ifarch %{ix86}
%global winepedir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winepedir x86_64-windows
%global winesodir x86_64-unix
%endif
%ifarch %{arm}
%global winepedir arm-windows
%global winesodir arm-unix
%endif
%ifarch aarch64
%global winepedir aarch64-windows
%global winesodir aarch64-unix
%endif

# wine-wayland related
%global gitdate     20210828
%global commit      61270cce427ea5101b446b151c3bda536b90797a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global version     6.15
%global release     1


# build with wine-staging patches, see:  https://github.com/wine-staging/wine-staging
%if 0%{?fedora}
%global wine_staging 1
%endif
# 0%%{?fedora}

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

Name:           wine-wayland
Version:        %{version}
Release:        0.%{release}.%{gitdate}.git%{shortcommit}%{?dist}
Summary:        A compatibility layer for windows applications

License:        LGPLv2+
URL:            https://gitlab.collabora.com/alf/wine/-/tree/wayland
Source0:        https://gitlab.collabora.com/alf/wine/-/archive/wayland/wine-wayland-%{version}-git%{shortcommit}.tar.gz

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop

# AppData files
Source150:      wine.appdata.xml

# wine bugs

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Patch511:       wine-cjk.patch

%if 0%{?wine_staging}
# wine-staging patches
# pulseaudio-patch is covered by that patch-set, too.
Source900: https://github.com/wine-staging/wine-staging/archive/v%{version}.tar.gz#/wine-staging-%{version}.tar.gz

# fysnc, futex2 and childwindow patches
# https://github.com/Frogging-Family/wine-tkg-git/tree/master/wine-tkg-git/wine-tkg-patches/proton
Patch900:       fsync-unix-staging.patch
Patch901:       fsync-staging-no_alloc_handle.patch
Patch902:       fsync_futex2.patch
# https://bugs.winehq.org/show_bug.cgi?id=45277
Patch903:       0010-winex11.drv-Use-XPresentPixmap-instead-of-XCopyArea-.patch
Patch904:       wine-6.15-fix-for-BZ51596.patch

%endif

%if !%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  freeglut-devel
BuildRequires:  lcms2-devel
BuildRequires:  libieee1284-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libusb-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
%if 0%{?fedora}
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
%endif
BuildRequires:  openldap-devel
BuildRequires:  perl-generators
BuildRequires:  unixODBC-devel
BuildRequires:  sane-backends-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  fontforge freetype-devel
BuildRequires:  libgphoto2-devel
%if 0%{?fedora} && 0%{?fedora} <= 30
BuildRequires:  isdn4k-utils-devel
%endif
BuildRequires:  libpcap-devel
# modular x
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel mesa-libOSMesa-devel
BuildRequires:  libXxf86dga-devel libXxf86vm-devel
BuildRequires:  libXrandr-devel libXrender-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  cups-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libXcursor-devel
BuildRequires:  dbus-devel
BuildRequires:  gnutls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  gsm-devel
BuildRequires:  libv4l-devel
BuildRequires:  fontpackages-devel
BuildRequires:  libtiff-devel
BuildRequires:  gettext-devel
BuildRequires:  chrpath
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%if 0%{?fedora} > 24
BuildRequires:  mpg123-devel
%endif
BuildRequires:  SDL2-devel
BuildRequires:  libvkd3d-devel
BuildRequires:  libvkd3d-shader-devel
BuildRequires:  vulkan-devel
BuildRequires:  libFAudio-devel
BuildRequires:  libappstream-glib

# wayland
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  egl-wayland-devel
# end wayland

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  gtk3-devel
BuildRequires:  libattr-devel
BuildRequires:  libva-devel
%endif
# 0%%{?wine_staging}

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildRequires:  openal-soft-devel
BuildRequires:  icoutils
%endif

Requires:       wine-common = %{version}-%{release}
Requires:       wine-desktop = %{version}-%{release}
Requires:       wine-fonts = %{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
%if 0%{?fedora} || 0%{?rhel} <= 6
Requires:       wine-core(x86-32) = %{version}-%{release}
Requires:       wine-capi(x86-32) = %{version}-%{release}
Requires:       wine-cms(x86-32) = %{version}-%{release}
Requires:       wine-ldap(x86-32) = %{version}-%{release}
Requires:       wine-twain(x86-32) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} == 6
Requires:       wine-openal(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       wine-opencl(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
#  wait for rhbz#968860 to require arch-specific samba-winbind-clients
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-32)
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
Requires:       wine-capi(x86-64) = %{version}-%{release}
Requires:       wine-cms(x86-64) = %{version}-%{release}
Requires:       wine-ldap(x86-64) = %{version}-%{release}
Requires:       wine-twain(x86-64) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-openal(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       wine-opencl(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
Requires:       mesa-dri-drivers(x86-64)
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{version}-%{release}
Requires:       wine-capi = %{version}-%{release}
Requires:       wine-cms = %{version}-%{release}
Requires:       wine-ldap = %{version}-%{release}
Requires:       wine-twain = %{version}-%{release}
Requires:       wine-pulseaudio = %{version}-%{release}
Requires:       wine-openal = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl = %{version}-%{release}
%endif
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{version}-%{release}
Requires:       wine-capi(aarch-64) = %{version}-%{release}
Requires:       wine-cms(aarch-64) = %{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{version}-%{release}
Requires:       wine-twain(aarch-64) = %{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{version}-%{release}
Requires:       wine-openal(aarch-64) = %{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package -n wine-core
Summary:        Wine core package
Requires(postun): /sbin/ldconfig
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       (nss-mdns(x86-32) if nss-mdns(x86-64))
Requires:       gnutls(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       (nss-mdns(x86-64) if nss-mdns(x86-32))
Requires:       gnutls(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
%endif
%endif

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{version}-%{release}

%description -n wine-core
Wine core package includes the basic wine stuff needed by all other packages.

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%package -n wine-systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description -n wine-systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.
%endif

%if 0%{?rhel} == 6
%package -n wine-sysvinit
Summary:        SysV initscript for the wine binfmt handler
BuildArch:      noarch
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service

%description -n wine-sysvinit
Register the wine binary handler for windows executables via SysV init files.
%endif

%package -n wine-filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description -n wine-filesystem
Filesystem directories and basic configuration for wine.

%package -n wine-common
Summary:        Common files
Requires:       wine-core = %{version}-%{release}
BuildArch:      noarch

%description -n wine-common
Common wine files and scripts.

%package -n wine-desktop
Summary:        Desktop integration features for wine
Requires(post): desktop-file-utils >= 0.8
Requires(postun): desktop-file-utils >= 0.8
Requires:       wine-core = %{version}-%{release}
Requires:       wine-common = %{version}-%{release}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires:       wine-systemd = %{version}-%{release}
%endif
%if 0%{?rhel} == 6
Requires:       wine-sysvinit = %{version}-%{release}
%endif
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description -n wine-desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package -n wine-fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with wine-staging patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{version}-%{release}
%else
# 0%%{?wine_staging}
Obsoletes:     wine-arial-fonts <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
Requires:      wine-courier-fonts = %{version}-%{release}
Requires:      wine-fixedsys-fonts = %{version}-%{release}
Requires:      wine-small-fonts = %{version}-%{release}
Requires:      wine-system-fonts = %{version}-%{release}
Requires:      wine-marlett-fonts = %{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{version}-%{release}
Requires:      wine-tahoma-fonts = %{version}-%{release}
# times-new-roman-fonts are available with wine_staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{version}-%{release}
%else
# 0%%{?wine_staging}
Obsoletes:     wine-times-new-roman-fonts <= %{version}-%{release}
Obsoletes:     wine-times-new-roman-fonts-system <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
Requires:      wine-symbol-fonts = %{version}-%{release}
Requires:      wine-webdings-fonts = %{version}-%{release}
Requires:      wine-wingdings-fonts = %{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
%if 0%{?fedora} > 12
Requires:      liberation-narrow-fonts
%endif

%description -n wine-fonts
%{summary}

%if 0%{?wine_staging}
%package -n wine-arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-arial-fonts
%{summary}
%endif
# 0%%{?wine_staging}

%package -n wine-courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-courier-fonts
%{summary}

%package -n wine-fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-fixedsys-fonts
%{summary}

%package -n wine-small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-small-fonts
%{summary}

%package -n wine-system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-system-fonts
%{summary}


%package -n wine-marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-marlett-fonts
%{summary}


%package -n wine-ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package -n wine-tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description -n wine-tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package -n wine-tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{version}-%{release}

%description -n wine-tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package -n wine-times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description -n wine-times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package -n wine-times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{version}-%{release}

%description -n wine-times-new-roman-fonts-system
%{summary}
%endif

%package -n wine-symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-symbol-fonts
%{summary}

%package -n wine-webdings-fonts
Summary:       Wine Webdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-webdings-fonts
%{summary}

%package -n wine-wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description -n wine-wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package -n wine-wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{version}-%{release}

%description -n wine-wingdings-fonts-system
%{summary}


%package -n wine-ldap
Summary: LDAP support for wine
Requires: wine-core = %{version}-%{release}

%description -n wine-ldap
LDAP support for wine

%package -n wine-cms
Summary: Color Management for wine
Requires: wine-core = %{version}-%{release}

%description -n wine-cms
Color Management for wine

%package -n wine-twain
Summary: Twain support for wine
Requires: wine-core = %{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description -n wine-twain
Twain support for wine

%package -n wine-capi
Summary: ISDN support for wine
Requires: wine-core = %{version}-%{release}
%if 0%{?fedora} <= 30
%ifarch x86_64
Requires:       isdn4k-utils(x86-64)
%endif
%ifarch %{ix86}
Requires:       isdn4k-utils(x86-32)
%endif
%ifarch %{arm} aarch64
Requires:       isdn4k-utils
%endif
%endif

%description -n wine-capi
ISDN support for wine

%package -n wine-devel
Summary: Wine development environment
Requires: wine-core = %{version}-%{release}

%description -n wine-devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package -n wine-pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{version}-%{release}

%description -n wine-pulseaudio
This package adds a pulseaudio driver for wine.

%package -n wine-alsa
Summary: Alsa support for wine
Requires: wine-core = %{version}-%{release}

%description -n wine-alsa
This package adds an alsa driver for wine.

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%package -n wine-openal
Summary: Openal support for wine
Requires: wine-core = %{version}-%{release}

%description -n wine-openal
This package adds an openal driver for wine.
%endif

%if 0%{?fedora}
%package -n wine-opencl
Summary: OpenCL support for wine
Requires: wine-core = %{version}-%{release}

%description -n wine-opencl
This package adds the opencl driver for wine.
%endif

%prep
%setup -q -n %{name}
%patch511 -p1 -b.cjk

%if 0%{?wine_staging}
# setup and apply wine-staging patches
gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

patches/patchinstall.sh DESTDIR="`pwd`" --all

#%%patch900 -p1
#%%patch901 -p1
#%%patch902 -p1
#%%patch903 -p1
%patch904 -p1

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

autoreconf -vfi

%endif
# 0%%{?wine_staging}

%build
# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

%ifarch aarch64
%if 0%{?fedora} >= 33
%global toolchain clang
%else
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`"
%endif
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
 --with-wayland \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%{?wine_staging: --with-xattr} \
 --disable-tests

make %{?_smp_mflags} TARGETFLAGS=""

%install

%makeinstall \
        includedir=%{buildroot}%{_includedir} \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
# do not ship typelibs in 32-bit packages
# https://www.winehq.org/pipermail/wine-devel/2020-June/167283.html
rm %{buildroot}%{_includedir}/wine/windows/*.tlb
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
touch %{buildroot}%{_bindir}/wineserver
mv %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-dxgi.dll
mv %{buildroot}%{_libdir}/wine/%{winesodir}/dxgi.dll.so %{buildroot}%{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d9.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d11.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.dll
touch %{buildroot}%{_libdir}/wine/%{winesodir}/dxgi.dll.so
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.dll

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
%if 0%{?rhel} < 7
mkdir -p %{buildroot}%{_initrddir}
install -p -c -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/wine
%endif
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf
%endif

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
%if 0%{?fedora} > 10
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'
MAIN_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="8"\n'\
'   y="8"\n'\
'   viewBox="8, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

%endif

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

cp -p %{SOURCE3} README-FEDORA

cp -p %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64 aarch64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

%if 0%{?fedora} || 0%{?rhel} > 6
rm -f %{buildroot}%{_initrddir}/wine
%endif

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1

# install and validate AppData file
mkdir -p %{buildroot}/%{_metainfodir}/
install -p -m 0644 %{SOURCE150} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml


%if 0%{?rhel} == 6
%post -n wine-sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun wine-sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} > 6
%post -n wine-systemd
%binfmt_apply wine.conf

%postun -n wine-systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi
%endif

%ldconfig_post wine-core

%posttrans -n wine-core
# handle upgrades for a few package updates
%{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/wine-dxgi.dll.so
%{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/wine-d3d9.dll
%{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/wine-d3d10.dll
%{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/wine-d3d11.dll
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%ifnarch %{arm}
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%endif
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/dxgi.dll \
  'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.dll 10 \
  --slave  %{_libdir}/wine/%{winesodir}/dxgi.dll.so 'wine-dxgi-so%{?_isa}' %{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d9.dll \
  'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.dll 10
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d10.dll \
  'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.dll 10 \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10_1.dll 'wine-d3d10_1%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10core.dll 'wine-d3d10core%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d11.dll \
  'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.dll 10

%postun -n wine-core
%{?ldconfig}
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
  %{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.dll
  %{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.dll
  %{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.dll
  %{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.dll
fi

%ldconfig_scriptlets ldap

%ldconfig_scriptlets cms

%ldconfig_scriptlets twain

%ldconfig_scriptlets capi

%ldconfig_scriptlets alsa

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%ldconfig_scriptlets openal
%endif

%files
# meta package

%files -n wine-core
%doc ANNOUNCE
%doc COPYING.LIB
%doc LICENSE
%doc LICENSE.OLD
%doc AUTHORS
%doc README-FEDORA
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
# wayland
#%%if 0%%{?wine_staging}
%{_bindir}/msidb
#%%endif
# end wayland
%{_bindir}/winedump
%{_libdir}/wine/%{winepedir}/explorer.exe
%{_libdir}/wine/%{winepedir}/cabarc.exe
%{_libdir}/wine/%{winepedir}/control.exe
%{_libdir}/wine/%{winepedir}/cmd.exe
%{_libdir}/wine/%{winepedir}/dxdiag.exe
%{_libdir}/wine/%{winepedir}/notepad.exe
%{_libdir}/wine/%{winepedir}/plugplay.exe
%{_libdir}/wine/%{winepedir}/progman.exe
%{_libdir}/wine/%{winepedir}/taskmgr.exe
%{_libdir}/wine/%{winepedir}/winedbg.exe
%{_libdir}/wine/%{winesodir}/winedbg.exe.so
%{_libdir}/wine/%{winepedir}/winefile.exe
%{_libdir}/wine/%{winepedir}/winemine.exe
%{_libdir}/wine/%{winepedir}/winemsibuilder.exe
%{_libdir}/wine/%{winepedir}/winepath.exe
%{_libdir}/wine/%{winepedir}/winmgmt.exe
%{_libdir}/wine/%{winepedir}/winver.exe
%{_libdir}/wine/%{winepedir}/wordpad.exe
%{_libdir}/wine/%{winepedir}/write.exe
%{_libdir}/wine/%{winepedir}/wusa.exe

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{_bindir}/wine32-preloader
%endif
%{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine

%{_libdir}/wine/%{winepedir}/attrib.exe
%{_libdir}/wine/%{winepedir}/arp.exe
%{_libdir}/wine/%{winepedir}/aspnet_regiis.exe
%{_libdir}/wine/%{winepedir}/cacls.exe
%{_libdir}/wine/%{winepedir}/conhost.exe
%{_libdir}/wine/%{winepedir}/cscript.exe
%{_libdir}/wine/%{winepedir}/dism.exe
%{_libdir}/wine/%{winepedir}/dplaysvr.exe
%{_libdir}/wine/%{winepedir}/dpnsvr.exe
%{_libdir}/wine/%{winepedir}/dpvsetup.exe
%{_libdir}/wine/%{winepedir}/eject.exe
%{_libdir}/wine/%{winepedir}/expand.exe
%{_libdir}/wine/%{winepedir}/extrac32.exe
%{_libdir}/wine/%{winepedir}/fc.exe
%{_libdir}/wine/%{winepedir}/find.exe
%{_libdir}/wine/%{winepedir}/findstr.exe
%{_libdir}/wine/%{winepedir}/fsutil.exe
%{_libdir}/wine/%{winepedir}/hostname.exe
%{_libdir}/wine/%{winepedir}/ipconfig.exe
%{_libdir}/wine/%{winepedir}/winhlp32.exe
%{_libdir}/wine/%{winepedir}/mshta.exe
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/msidb.exe
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/msiexec.exe
%{_libdir}/wine/%{winepedir}/net.exe
%{_libdir}/wine/%{winepedir}/netstat.exe
%{_libdir}/wine/%{winepedir}/ngen.exe
%{_libdir}/wine/%{winepedir}/ntoskrnl.exe
%{_libdir}/wine/%{winepedir}/oleview.exe
%{_libdir}/wine/%{winepedir}/ping.exe
%{_libdir}/wine/%{winepedir}/powershell.exe
%{_libdir}/wine/%{winepedir}/reg.exe
%{_libdir}/wine/%{winepedir}/regasm.exe
%{_libdir}/wine/%{winepedir}/regedit.exe
%{_libdir}/wine/%{winepedir}/regsvcs.exe
%{_libdir}/wine/%{winepedir}/regsvr32.exe
%{_libdir}/wine/%{winepedir}/rpcss.exe
%{_libdir}/wine/%{winepedir}/rundll32.exe
%{_libdir}/wine/%{winepedir}/schtasks.exe
%{_libdir}/wine/%{winepedir}/sdbinst.exe
%{_libdir}/wine/%{winepedir}/secedit.exe
%{_libdir}/wine/%{winepedir}/servicemodelreg.exe
%{_libdir}/wine/%{winepedir}/services.exe
%{_libdir}/wine/%{winepedir}/start.exe
%{_libdir}/wine/%{winepedir}/tasklist.exe
%{_libdir}/wine/%{winepedir}/termsv.exe
%{_libdir}/wine/%{winepedir}/view.exe
%{_libdir}/wine/%{winepedir}/wevtutil.exe
%{_libdir}/wine/%{winepedir}/where.exe
%{_libdir}/wine/%{winepedir}/whoami.exe
%{_libdir}/wine/%{winepedir}/wineboot.exe
%{_libdir}/wine/%{winepedir}/winebrowser.exe
%{_libdir}/wine/%{winesodir}/winebrowser.exe.so
%{_libdir}/wine/%{winepedir}/wineconsole.exe
%{_libdir}/wine/%{winepedir}/winemenubuilder.exe
%{_libdir}/wine/%{winesodir}/winemenubuilder.exe.so
%{_libdir}/wine/%{winepedir}/winecfg.exe
%{_libdir}/wine/%{winesodir}/winecfg.exe.so
%{_libdir}/wine/%{winepedir}/winedevice.exe
%{_libdir}/wine/%{winepedir}/wmplayer.exe
%{_libdir}/wine/%{winepedir}/wscript.exe
%{_libdir}/wine/%{winepedir}/uninstaller.exe

%{_libdir}/wine/%{winesodir}/libwine.so.1*

%{_libdir}/wine/%{winepedir}/acledit.dll
%{_libdir}/wine/%{winepedir}/aclui.dll
%{_libdir}/wine/%{winepedir}/activeds.dll
%{_libdir}/wine/%{winepedir}/activeds.tlb
%{_libdir}/wine/%{winepedir}/actxprxy.dll
%{_libdir}/wine/%{winepedir}/adsldp.dll
%{_libdir}/wine/%{winepedir}/adsldpc.dll
%{_libdir}/wine/%{winepedir}/advapi32.dll
%{_libdir}/wine/%{winepedir}/advpack.dll
%{_libdir}/wine/%{winepedir}/amsi.dll
%{_libdir}/wine/%{winepedir}/amstream.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-identity-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-runtime-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-runtime-l1-1-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-apiquery-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-appcompat-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-appinit-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-atoms-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-bem-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-comm-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l2-1-0.dll
# wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l3-2-0.dll
# end wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-crt-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-crt-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-datetime-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-datetime-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-debug-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-debug-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-delayload-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-delayload-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-3.dll
# wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-featurestaging-l1-1-0.dll
# end wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-fibers-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-fibers-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-ansi-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-fromapp-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-handle-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-interlocked-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-interlocked-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-io-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-io-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-job-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-job-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-largeinteger-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-2.dll
# wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-5.dll
# end wayland
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-private-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-3-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localregistry-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-3.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-4.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-misc-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-ansi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namespace-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-normalization-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-path-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-privateprofile-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processenvironment-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processenvironment-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-2.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-3.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processtopology-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-profile-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-ansi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-quirks-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-realtime-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l2-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registryuserspecific-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-rtlsupport-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-rtlsupport-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-obsolete-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shutdown-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sidebyside-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-stringansi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-stringloader-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-2-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-ansi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-2-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-systemtopology-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-timezone-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-toolhelp-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-url-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-util-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-versionansi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-windowserrorreporting-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-error-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-error-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-errorprivate-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-registration-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-roparameterizediid-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-string-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-string-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-wow64-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-wow64-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-xstate-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-core-xstate-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-conio-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-convert-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-environment-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-filesystem-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-heap-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-locale-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-math-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-multibyte-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-process-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-runtime-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-stdio-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-string-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-time-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-utility-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-config-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-config-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-query-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-advapi32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-advapi32-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-kernel32-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-normaliz-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-ole32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shell32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shlwapi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shlwapi-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-user32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-version-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-dx-d3dkmt-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-classicprovider-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-consumer-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-controller-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-provider-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-eventlog-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-gaming-tcui-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-gdi-dpiinfo-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-joystick-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-misc-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-mme-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-time-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-dc-access-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-rectangle-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-sysparams-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-perf-legacy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-power-base-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-power-setting-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-draw-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-private-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-private-l1-1-4.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-window-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-winevent-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-activedirectoryclient-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-audit-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-private-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-credentials-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-cryptoapi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-grouppolicy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l2-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsapolicy-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-provider-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-sddl-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-security-systemfunctions-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-core-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-core-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-management-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-management-l2-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-private-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-winsvc-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-service-winsvc-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-obsolete-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-scaling-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-scaling-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-stream-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-stream-winrt-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-thread-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shell-shellcom-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/api-ms-win-shell-shellfolders-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/apphelp.dll
%{_libdir}/wine/%{winepedir}/appwiz.cpl
%{_libdir}/wine/%{winepedir}/atl.dll
%{_libdir}/wine/%{winepedir}/atl80.dll
%{_libdir}/wine/%{winepedir}/atl90.dll
%{_libdir}/wine/%{winepedir}/atl100.dll
%{_libdir}/wine/%{winepedir}/atl110.dll
%{_libdir}/wine/%{winepedir}/atlthunk.dll
%{_libdir}/wine/%{winepedir}/atmlib.dll
%{_libdir}/wine/%{winepedir}/authz.dll
%{_libdir}/wine/%{winepedir}/avicap32.dll
%{_libdir}/wine/%{winesodir}/avicap32.dll.so
%{_libdir}/wine/%{winepedir}/avifil32.dll
%{_libdir}/wine/%{winepedir}/avrt.dll
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winepedir}/bcrypt.dll
%{_libdir}/wine/%{winepedir}/bluetoothapis.dll
%{_libdir}/wine/%{winepedir}/browseui.dll
%{_libdir}/wine/%{winepedir}/bthprops.cpl
%{_libdir}/wine/%{winepedir}/cabinet.dll
%{_libdir}/wine/%{winepedir}/cards.dll
%{_libdir}/wine/%{winepedir}/cdosys.dll
%{_libdir}/wine/%{winepedir}/cfgmgr32.dll
%{_libdir}/wine/%{winepedir}/chcp.com
%{_libdir}/wine/%{winepedir}/clock.exe
%{_libdir}/wine/%{winepedir}/clusapi.dll
%{_libdir}/wine/%{winepedir}/combase.dll
%{_libdir}/wine/%{winepedir}/comcat.dll
%{_libdir}/wine/%{winepedir}/comctl32.dll
%{_libdir}/wine/%{winepedir}/comdlg32.dll
%{_libdir}/wine/%{winepedir}/compstui.dll
%{_libdir}/wine/%{winepedir}/comsvcs.dll
%{_libdir}/wine/%{winepedir}/concrt140.dll
%{_libdir}/wine/%{winepedir}/connect.dll
%{_libdir}/wine/%{winepedir}/credui.dll
%{_libdir}/wine/%{winepedir}/crtdll.dll
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winepedir}/crypt32.dll
%{_libdir}/wine/%{winepedir}/cryptdlg.dll
%{_libdir}/wine/%{winepedir}/cryptdll.dll
%{_libdir}/wine/%{winepedir}/cryptext.dll
%{_libdir}/wine/%{winepedir}/cryptnet.dll
%{_libdir}/wine/%{winepedir}/cryptsp.dll
%{_libdir}/wine/%{winepedir}/cryptui.dll
%{_libdir}/wine/%{winepedir}/ctapi32.dll
%{_libdir}/wine/%{winesodir}/ctapi32.dll.so
%{_libdir}/wine/%{winepedir}/ctl3d32.dll
%{_libdir}/wine/%{winepedir}/d2d1.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10_1.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10core.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d11.dll
%{_libdir}/wine/%{winepedir}/wine-d3d11.dll
%{_libdir}/wine/%{winepedir}/d3d12.dll
%{_libdir}/wine/%{winesodir}/d3d12.dll.so
%{_libdir}/wine/%{winepedir}/d3dcompiler_*.dll
%{_libdir}/wine/%{winepedir}/d3dim.dll
%{_libdir}/wine/%{winepedir}/d3dim700.dll
%{_libdir}/wine/%{winepedir}/d3drm.dll
%{_libdir}/wine/%{winepedir}/d3dx9_*.dll
%{_libdir}/wine/%{winepedir}/d3dx10_*.dll
%{_libdir}/wine/%{winepedir}/d3dx11_42.dll
%{_libdir}/wine/%{winepedir}/d3dx11_43.dll
%{_libdir}/wine/%{winepedir}/d3dxof.dll
%{_libdir}/wine/%{winepedir}/davclnt.dll
%{_libdir}/wine/%{winepedir}/dbgeng.dll
%{_libdir}/wine/%{winepedir}/dbghelp.dll
%{_libdir}/wine/%{winepedir}/dciman32.dll
%{_libdir}/wine/%{winepedir}/dcomp.dll
%{_libdir}/wine/%{winepedir}/ddraw.dll
%{_libdir}/wine/%{winepedir}/ddrawex.dll
%{_libdir}/wine/%{winepedir}/devenum.dll
%{_libdir}/wine/%{winepedir}/dhcpcsvc.dll
%{_libdir}/wine/%{winepedir}/dhtmled.ocx
%{_libdir}/wine/%{winepedir}/difxapi.dll
%{_libdir}/wine/%{winepedir}/dinput.dll
%{_libdir}/wine/%{winesodir}/dinput.dll.so
%{_libdir}/wine/%{winepedir}/dinput8.dll
%{_libdir}/wine/%{winesodir}/dinput8.dll.so
%{_libdir}/wine/%{winepedir}/directmanipulation.dll
%{_libdir}/wine/%{winepedir}/dispex.dll
%{_libdir}/wine/%{winepedir}/dmband.dll
%{_libdir}/wine/%{winepedir}/dmcompos.dll
%{_libdir}/wine/%{winepedir}/dmime.dll
%{_libdir}/wine/%{winepedir}/dmloader.dll
%{_libdir}/wine/%{winepedir}/dmscript.dll
%{_libdir}/wine/%{winepedir}/dmstyle.dll
%{_libdir}/wine/%{winepedir}/dmsynth.dll
%{_libdir}/wine/%{winepedir}/dmusic.dll
%{_libdir}/wine/%{winepedir}/dmusic32.dll
%{_libdir}/wine/%{winepedir}/dplay.dll
%{_libdir}/wine/%{winepedir}/dplayx.dll
%{_libdir}/wine/%{winepedir}/dpnaddr.dll
%{_libdir}/wine/%{winepedir}/dpnet.dll
%{_libdir}/wine/%{winepedir}/dpnhpast.dll
%{_libdir}/wine/%{winepedir}/dpnhupnp.dll
#%%{_libdir}/wine/%%{winesodir}/dpnhupnp.dll.so
%{_libdir}/wine/%{winepedir}/dpnlobby.dll
%{_libdir}/wine/%{winepedir}/dpvoice.dll
%{_libdir}/wine/%{winepedir}/dpwsockx.dll
%{_libdir}/wine/%{winepedir}/drmclien.dll
%{_libdir}/wine/%{winepedir}/dsound.dll
%{_libdir}/wine/%{winepedir}/dsdmo.dll
%{_libdir}/wine/%{winepedir}/dsquery.dll
%{_libdir}/wine/%{winepedir}/dssenh.dll
%{_libdir}/wine/%{winepedir}/dsuiext.dll
%{_libdir}/wine/%{winepedir}/dswave.dll
%{_libdir}/wine/%{winepedir}/dwmapi.dll
%{_libdir}/wine/%{winepedir}/dwrite.dll
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winepedir}/dx8vb.dll
%{_libdir}/wine/%{winepedir}/dxdiagn.dll
%ghost %{_libdir}/wine/%{winepedir}/dxgi.dll
%{_libdir}/wine/%{winepedir}/wine-dxgi.dll
%ghost %{_libdir}/wine/%{winesodir}/dxgi.dll.so
%{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/dxgkrnl.sys
%{_libdir}/wine/%{winepedir}/dxgmms1.sys
%endif
%{_libdir}/wine/%{winepedir}/dxtrans.dll
%{_libdir}/wine/%{winepedir}/dxva2.dll
%{_libdir}/wine/%{winepedir}/esent.dll
%{_libdir}/wine/%{winepedir}/evr.dll
%{_libdir}/wine/%{winepedir}/explorerframe.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-authz-context-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-domainjoin-netjoin-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-dwmapi-ext-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-create-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-create-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-devcaps-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-draw-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-draw-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-font-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-font-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-render-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-kernel32-package-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-kernel32-package-current-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-dialogbox-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-draw-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-gui-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-gui-l1-3-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-keyboard-l1-3-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-5-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-message-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-message-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-mouse-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-private-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-private-l1-3-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-rectangle-ext-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-uicontext-ext-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-4.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-windowclass-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-windowclass-l1-1-1.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-oleacc-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-ras-rasapi32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-object-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-rgn-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-security-credui-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-security-cryptui-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-comctl32-init-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-comdlg32-l1-1-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-shell32-l1-2-0.dll
%{_libdir}/wine/%{winepedir}/ext-ms-win-uxtheme-themes-l1-1-0.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/ext-ms-win-appmodel-usercontext-l1-1-0.dll
%{_libdir}/wine/%{winesodir}/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/%{winepedir}/ext-ms-win-xaml-pal-l1-1-0.dll
%{_libdir}/wine/%{winesodir}/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/%{winepedir}/faultrep.dll
%{_libdir}/wine/%{winepedir}/feclient.dll
%{_libdir}/wine/%{winepedir}/fltlib.dll
%{_libdir}/wine/%{winepedir}/fltmgr.sys
%{_libdir}/wine/%{winepedir}/fntcache.dll
%{_libdir}/wine/%{winepedir}/fontsub.dll
%{_libdir}/wine/%{winepedir}/fusion.dll
%{_libdir}/wine/%{winepedir}/fwpuclnt.dll
%{_libdir}/wine/%{winepedir}/gameux.dll
%{_libdir}/wine/%{winepedir}/gamingtcui.dll
%{_libdir}/wine/%{winesodir}/gdi32.so
%{_libdir}/wine/%{winepedir}/gdi32.dll
%{_libdir}/wine/%{winepedir}/gdiplus.dll
%{_libdir}/wine/%{winepedir}/glu32.dll
%{_libdir}/wine/%{winepedir}/gphoto2.ds
%{_libdir}/wine/%{winesodir}/gphoto2.ds.so
%{_libdir}/wine/%{winepedir}/gpkcsp.dll
%{_libdir}/wine/%{winepedir}/hal.dll
%{_libdir}/wine/%{winepedir}/hh.exe
%{_libdir}/wine/%{winepedir}/hhctrl.ocx
%{_libdir}/wine/%{winepedir}/hid.dll
%{_libdir}/wine/%{winepedir}/hidclass.sys
%{_libdir}/wine/%{winepedir}/hlink.dll
%{_libdir}/wine/%{winepedir}/hnetcfg.dll
%{_libdir}/wine/%{winepedir}/http.sys
%{_libdir}/wine/%{winepedir}/httpapi.dll
%{_libdir}/wine/%{winepedir}/icacls.exe
%{_libdir}/wine/%{winepedir}/iccvid.dll
%{_libdir}/wine/%{winepedir}/icinfo.exe
%{_libdir}/wine/%{winepedir}/icmp.dll
%{_libdir}/wine/%{winepedir}/ieframe.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/iertutil.dll
%endif
%{_libdir}/wine/%{winepedir}/ieproxy.dll
%{_libdir}/wine/%{winepedir}/imaadp32.acm
%{_libdir}/wine/%{winepedir}/imagehlp.dll
%{_libdir}/wine/%{winepedir}/imm32.dll
%{_libdir}/wine/%{winepedir}/inetcomm.dll
%{_libdir}/wine/%{winepedir}/inetcpl.cpl
%{_libdir}/wine/%{winepedir}/inetmib1.dll
%{_libdir}/wine/%{winepedir}/infosoft.dll
%{_libdir}/wine/%{winepedir}/initpki.dll
%{_libdir}/wine/%{winepedir}/inkobj.dll
%{_libdir}/wine/%{winepedir}/inseng.dll
%{_libdir}/wine/%{winepedir}/iphlpapi.dll
%{_libdir}/wine/%{winesodir}/iphlpapi.dll.so
%{_libdir}/wine/%{winepedir}/iprop.dll
%{_libdir}/wine/%{winepedir}/irprops.cpl
%{_libdir}/wine/%{winepedir}/itircl.dll
%{_libdir}/wine/%{winepedir}/itss.dll
%{_libdir}/wine/%{winepedir}/joy.cpl
%{_libdir}/wine/%{winepedir}/jscript.dll
%{_libdir}/wine/%{winepedir}/jsproxy.dll
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winepedir}/kerberos.dll
%{_libdir}/wine/%{winepedir}/kernel32.dll
%{_libdir}/wine/%{winepedir}/kernelbase.dll
%{_libdir}/wine/%{winepedir}/ksecdd.sys
%{_libdir}/wine/%{winepedir}/ksproxy.ax
%{_libdir}/wine/%{winepedir}/ksuser.dll
%{_libdir}/wine/%{winepedir}/ktmw32.dll
%if 0%{?fedora} > 24
%{_libdir}/wine/%{winepedir}/l3codeca.acm
%{_libdir}/wine/%{winesodir}/l3codeca.acm.so
%endif
%{_libdir}/wine/%{winepedir}/light.msstyles
%{_libdir}/wine/%{winepedir}/loadperf.dll
%{_libdir}/wine/%{winepedir}/localspl.dll
%{_libdir}/wine/%{winepedir}/localui.dll
%{_libdir}/wine/%{winepedir}/lodctr.exe
%{_libdir}/wine/%{winepedir}/lz32.dll
%{_libdir}/wine/%{winepedir}/mapi32.dll
%{_libdir}/wine/%{winepedir}/mapistub.dll
%{_libdir}/wine/%{winepedir}/mciavi32.dll
%{_libdir}/wine/%{winepedir}/mcicda.dll
%{_libdir}/wine/%{winepedir}/mciqtz32.dll
%{_libdir}/wine/%{winepedir}/mciseq.dll
%{_libdir}/wine/%{winepedir}/mciwave.dll
%{_libdir}/wine/%{winepedir}/mf.dll
%{_libdir}/wine/%{winepedir}/mf3216.dll
%{_libdir}/wine/%{winepedir}/mferror.dll
%{_libdir}/wine/%{winepedir}/mfmediaengine.dll
%{_libdir}/wine/%{winepedir}/mfplat.dll
%{_libdir}/wine/%{winepedir}/mfplay.dll
%{_libdir}/wine/%{winepedir}/mfreadwrite.dll
%{_libdir}/wine/%{winepedir}/mgmtapi.dll
%{_libdir}/wine/%{winepedir}/midimap.dll
%{_libdir}/wine/%{winepedir}/mlang.dll
%{_libdir}/wine/%{winepedir}/mmcndmgr.dll
%{_libdir}/wine/%{winepedir}/mmdevapi.dll
%{_libdir}/wine/%{winepedir}/mofcomp.exe
%{_libdir}/wine/%{winepedir}/mountmgr.sys
%{_libdir}/wine/%{winesodir}/mountmgr.sys.so
%{_libdir}/wine/%{winepedir}/mp3dmod.dll
%{_libdir}/wine/%{winesodir}/mp3dmod.dll.so
%{_libdir}/wine/%{winepedir}/mpr.dll
%{_libdir}/wine/%{winepedir}/mprapi.dll
%{_libdir}/wine/%{winepedir}/msacm32.dll
%{_libdir}/wine/%{winepedir}/msacm32.drv
%{_libdir}/wine/%{winepedir}/msado15.dll
%{_libdir}/wine/%{winepedir}/msadp32.acm
%{_libdir}/wine/%{winepedir}/msasn1.dll
%{_libdir}/wine/%{winepedir}/mscat32.dll
%{_libdir}/wine/%{winepedir}/mscoree.dll
%{_libdir}/wine/%{winepedir}/mscorwks.dll
%{_libdir}/wine/%{winepedir}/msctf.dll
%{_libdir}/wine/%{winepedir}/msctfp.dll
%{_libdir}/wine/%{winepedir}/msdaps.dll
%{_libdir}/wine/%{winepedir}/msdelta.dll
%{_libdir}/wine/%{winepedir}/msdmo.dll
%{_libdir}/wine/%{winepedir}/msdrm.dll
%{_libdir}/wine/%{winepedir}/msftedit.dll
%{_libdir}/wine/%{winepedir}/msg711.acm
%{_libdir}/wine/%{winepedir}/msgsm32.acm
%{_libdir}/wine/%{winesodir}/msgsm32.acm.so
%{_libdir}/wine/%{winepedir}/mshtml.dll
%{_libdir}/wine/%{winepedir}/mshtml.tlb
%{_libdir}/wine/%{winepedir}/msi.dll
%{_libdir}/wine/%{winepedir}/msident.dll
%{_libdir}/wine/%{winepedir}/msimtf.dll
%{_libdir}/wine/%{winepedir}/msimg32.dll
%{_libdir}/wine/%{winepedir}/msimsg.dll
%{_libdir}/wine/%{winepedir}/msinfo32.exe
%{_libdir}/wine/%{winepedir}/msisip.dll
%{_libdir}/wine/%{winepedir}/msisys.ocx
%{_libdir}/wine/%{winepedir}/msls31.dll
%{_libdir}/wine/%{winepedir}/msnet32.dll
%{_libdir}/wine/%{winepedir}/mspatcha.dll
%{_libdir}/wine/%{winepedir}/msports.dll
%{_libdir}/wine/%{winepedir}/msscript.ocx
%{_libdir}/wine/%{winepedir}/mssign32.dll
%{_libdir}/wine/%{winepedir}/mssip32.dll
%{_libdir}/wine/%{winepedir}/msrle32.dll
%{_libdir}/wine/%{winepedir}/mstask.dll
%{_libdir}/wine/%{winepedir}/msv1_0.dll
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winepedir}/msvcirt.dll
%{_libdir}/wine/%{winepedir}/msvcm80.dll
%{_libdir}/wine/%{winepedir}/msvcm90.dll
%{_libdir}/wine/%{winepedir}/msvcp60.dll
%{_libdir}/wine/%{winepedir}/msvcp70.dll
%{_libdir}/wine/%{winepedir}/msvcp71.dll
%{_libdir}/wine/%{winepedir}/msvcp80.dll
%{_libdir}/wine/%{winepedir}/msvcp90.dll
%{_libdir}/wine/%{winepedir}/msvcp100.dll
%{_libdir}/wine/%{winepedir}/msvcp110.dll
%{_libdir}/wine/%{winepedir}/msvcp120.dll
%{_libdir}/wine/%{winepedir}/msvcp120_app.dll
%{_libdir}/wine/%{winepedir}/msvcp140.dll
%{_libdir}/wine/%{winepedir}/msvcp140_1.dll
%{_libdir}/wine/%{winepedir}/msvcr70.dll
%{_libdir}/wine/%{winepedir}/msvcr71.dll
%{_libdir}/wine/%{winepedir}/msvcr80.dll
%{_libdir}/wine/%{winepedir}/msvcr90.dll
%{_libdir}/wine/%{winepedir}/msvcr100.dll
%{_libdir}/wine/%{winepedir}/msvcr110.dll
%{_libdir}/wine/%{winepedir}/msvcr120.dll
%{_libdir}/wine/%{winepedir}/msvcr120_app.dll
%{_libdir}/wine/%{winepedir}/msvcrt.dll
%{_libdir}/wine/%{winepedir}/msvcrt20.dll
%{_libdir}/wine/%{winepedir}/msvcrt40.dll
%{_libdir}/wine/%{winepedir}/msvcrtd.dll
%{_libdir}/wine/%{winepedir}/msvfw32.dll
%{_libdir}/wine/%{winepedir}/msvidc32.dll
%{_libdir}/wine/%{winepedir}/mswsock.dll
%{_libdir}/wine/%{winepedir}/msxml.dll
%{_libdir}/wine/%{winepedir}/msxml2.dll
%{_libdir}/wine/%{winepedir}/msxml3.dll
%{_libdir}/wine/%{winesodir}/msxml3.dll.so
%{_libdir}/wine/%{winepedir}/msxml4.dll
%{_libdir}/wine/%{winepedir}/msxml6.dll
%{_libdir}/wine/%{winepedir}/mtxdm.dll
%{_libdir}/wine/%{winepedir}/nddeapi.dll
%{_libdir}/wine/%{winepedir}/ncrypt.dll
%{_libdir}/wine/%{winepedir}/ndis.sys
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winepedir}/netapi32.dll
%{_libdir}/wine/%{winepedir}/netcfgx.dll
%{_libdir}/wine/%{winepedir}/netio.sys
%{_libdir}/wine/%{winepedir}/netprofm.dll
%{_libdir}/wine/%{winepedir}/netsh.exe
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/netutils.dll
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/newdev.dll
%{_libdir}/wine/%{winepedir}/ninput.dll
%{_libdir}/wine/%{winepedir}/normaliz.dll
%{_libdir}/wine/%{winepedir}/npmshtml.dll
%{_libdir}/wine/%{winepedir}/npptools.dll
%{_libdir}/wine/%{winepedir}/nsi.dll
%{_libdir}/wine/%{winepedir}/nsiproxy.sys
%{_libdir}/wine/%{winesodir}/nsiproxy.sys.so
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winepedir}/ntdll.dll
%{_libdir}/wine/%{winepedir}/ntdsapi.dll
%{_libdir}/wine/%{winepedir}/ntprint.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/nvcuda.dll
%{_libdir}/wine/%{winesodir}/nvcuda.dll.so
%{_libdir}/wine/%{winepedir}/nvcuvid.dll
%{_libdir}/wine/%{winesodir}/nvcuvid.dll.so
%endif
%{_libdir}/wine/%{winepedir}/objsel.dll
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winepedir}/odbc32.dll
%{_libdir}/wine/%{winepedir}/odbcbcp.dll
%{_libdir}/wine/%{winepedir}/odbccp32.dll
%{_libdir}/wine/%{winepedir}/odbccu32.dll
%{_libdir}/wine/%{winepedir}/ole32.dll
%{_libdir}/wine/%{winepedir}/oleacc.dll
%{_libdir}/wine/%{winepedir}/oleaut32.dll
%{_libdir}/wine/%{winepedir}/olecli32.dll
%{_libdir}/wine/%{winepedir}/oledb32.dll
%{_libdir}/wine/%{winepedir}/oledlg.dll
%{_libdir}/wine/%{winepedir}/olepro32.dll
%{_libdir}/wine/%{winepedir}/olesvr32.dll
%{_libdir}/wine/%{winepedir}/olethk32.dll
%{_libdir}/wine/%{winepedir}/opcservices.dll
%{_libdir}/wine/%{winepedir}/packager.dll
%{_libdir}/wine/%{winepedir}/pdh.dll
%{_libdir}/wine/%{winepedir}/photometadatahandler.dll
%{_libdir}/wine/%{winepedir}/pidgen.dll
%{_libdir}/wine/%{winepedir}/powrprof.dll
%{_libdir}/wine/%{winepedir}/presentationfontcache.exe
%{_libdir}/wine/%{winepedir}/printui.dll
%{_libdir}/wine/%{winepedir}/prntvpt.dll
%{_libdir}/wine/%{winepedir}/propsys.dll
%{_libdir}/wine/%{winepedir}/psapi.dll
%{_libdir}/wine/%{winepedir}/pstorec.dll
%{_libdir}/wine/%{winepedir}/pwrshplugin.dll
%{_libdir}/wine/%{winepedir}/qasf.dll
%{_libdir}/wine/%{winepedir}/qcap.dll
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winepedir}/qdvd.dll
%{_libdir}/wine/%{winepedir}/qedit.dll
%{_libdir}/wine/%{winepedir}/qmgr.dll
%{_libdir}/wine/%{winepedir}/qmgrprxy.dll
%{_libdir}/wine/%{winepedir}/quartz.dll
%{_libdir}/wine/%{winepedir}/query.dll
%{_libdir}/wine/%{winepedir}/qwave.dll
%{_libdir}/wine/%{winepedir}/rasapi32.dll
%{_libdir}/wine/%{winepedir}/rasdlg.dll
%{_libdir}/wine/%{winepedir}/regapi.dll
%{_libdir}/wine/%{winepedir}/regini.exe
%{_libdir}/wine/%{winepedir}/resutils.dll
%{_libdir}/wine/%{winepedir}/riched20.dll
%{_libdir}/wine/%{winepedir}/riched32.dll
%{_libdir}/wine/%{winepedir}/rpcrt4.dll
%{_libdir}/wine/%{winepedir}/rsabase.dll
%{_libdir}/wine/%{winepedir}/rsaenh.dll
%{_libdir}/wine/%{winepedir}/rstrtmgr.dll
%{_libdir}/wine/%{winepedir}/rtutils.dll
%{_libdir}/wine/%{winepedir}/rtworkq.dll
%{_libdir}/wine/%{winepedir}/samlib.dll
%{_libdir}/wine/%{winepedir}/sapi.dll
%{_libdir}/wine/%{winepedir}/sas.dll
%{_libdir}/wine/%{winepedir}/sc.exe
%{_libdir}/wine/%{winepedir}/scarddlg.dll
%{_libdir}/wine/%{winepedir}/sccbase.dll
%{_libdir}/wine/%{winepedir}/schannel.dll
%{_libdir}/wine/%{winepedir}/scrobj.dll
%{_libdir}/wine/%{winepedir}/scrrun.dll
%{_libdir}/wine/%{winepedir}/scsiport.sys
%{_libdir}/wine/%{winepedir}/sechost.dll
%{_libdir}/wine/%{winepedir}/secur32.dll
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winepedir}/sensapi.dll
%{_libdir}/wine/%{winepedir}/serialui.dll
%{_libdir}/wine/%{winepedir}/setupapi.dll
%{_libdir}/wine/%{winepedir}/sfc_os.dll
%{_libdir}/wine/%{winepedir}/shcore.dll
%{_libdir}/wine/%{winepedir}/shdoclc.dll
%{_libdir}/wine/%{winepedir}/shdocvw.dll
%{_libdir}/wine/%{winepedir}/schedsvc.dll
%{_libdir}/wine/%{winepedir}/shell32.dll
%{_libdir}/wine/%{winesodir}/shell32.dll.so
%{_libdir}/wine/%{winepedir}/shfolder.dll
%{_libdir}/wine/%{winepedir}/shlwapi.dll
%{_libdir}/wine/%{winepedir}/shutdown.exe
%{_libdir}/wine/%{winepedir}/slbcsp.dll
%{_libdir}/wine/%{winepedir}/slc.dll
%{_libdir}/wine/%{winepedir}/snmpapi.dll
%{_libdir}/wine/%{winepedir}/softpub.dll
%{_libdir}/wine/%{winepedir}/spoolsv.exe
%{_libdir}/wine/%{winepedir}/sppc.dll
%{_libdir}/wine/%{winepedir}/srclient.dll
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/srvcli.dll
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/sspicli.dll
%{_libdir}/wine/%{winepedir}/stdole2.tlb
%{_libdir}/wine/%{winepedir}/stdole32.tlb
%{_libdir}/wine/%{winepedir}/sti.dll
%{_libdir}/wine/%{winepedir}/strmdll.dll
%{_libdir}/wine/%{winepedir}/subst.exe
%{_libdir}/wine/%{winepedir}/svchost.exe
%{_libdir}/wine/%{winepedir}/svrapi.dll
%{_libdir}/wine/%{winepedir}/sxs.dll
%{_libdir}/wine/%{winepedir}/systeminfo.exe
%{_libdir}/wine/%{winepedir}/t2embed.dll
%{_libdir}/wine/%{winepedir}/tapi32.dll
%{_libdir}/wine/%{winepedir}/taskkill.exe
%{_libdir}/wine/%{winepedir}/taskschd.dll
%{_libdir}/wine/%{winepedir}/tbs.dll
%{_libdir}/wine/%{winepedir}/tdh.dll
%{_libdir}/wine/%{winepedir}/tdi.sys
%{_libdir}/wine/%{winepedir}/traffic.dll
%{_libdir}/wine/%{winepedir}/tzres.dll
%{_libdir}/wine/%{winepedir}/ucrtbase.dll
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/uianimation.dll
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/uiautomationcore.dll
%{_libdir}/wine/%{winepedir}/uiribbon.dll
%{_libdir}/wine/%{winepedir}/unicows.dll
%{_libdir}/wine/%{winepedir}/unlodctr.exe
%{_libdir}/wine/%{winepedir}/updspapi.dll
%{_libdir}/wine/%{winepedir}/url.dll
%{_libdir}/wine/%{winepedir}/urlmon.dll
%{_libdir}/wine/%{winepedir}/usbd.sys
%{_libdir}/wine/%{winesodir}/user32.so
%{_libdir}/wine/%{winepedir}/user32.dll
%{_libdir}/wine/%{winepedir}/usp10.dll
%{_libdir}/wine/%{winepedir}/utildll.dll
%{_libdir}/wine/%{winepedir}/uxtheme.dll
%{_libdir}/wine/%{winepedir}/userenv.dll
%{_libdir}/wine/%{winepedir}/vbscript.dll
%{_libdir}/wine/%{winepedir}/vcomp.dll
%{_libdir}/wine/%{winepedir}/vcomp90.dll
%{_libdir}/wine/%{winepedir}/vcomp100.dll
%{_libdir}/wine/%{winepedir}/vcomp110.dll
%{_libdir}/wine/%{winepedir}/vcomp120.dll
%{_libdir}/wine/%{winepedir}/vcomp140.dll
%{_libdir}/wine/%{winepedir}/vcruntime140.dll
%{_libdir}/wine/%{winepedir}/vcruntime140_1.dll
%{_libdir}/wine/%{winepedir}/vdmdbg.dll
%{_libdir}/wine/%{winepedir}/version.dll
%{_libdir}/wine/%{winepedir}/vga.dll
%{_libdir}/wine/%{winepedir}/virtdisk.dll
%{_libdir}/wine/%{winepedir}/vssapi.dll
%{_libdir}/wine/%{winepedir}/vulkan-1.dll
%{_libdir}/wine/%{winepedir}/wbemdisp.dll
%{_libdir}/wine/%{winepedir}/wbemprox.dll
%{_libdir}/wine/%{winepedir}/wdscore.dll
%{_libdir}/wine/%{winepedir}/webservices.dll
%{_libdir}/wine/%{winepedir}/websocket.dll
%{_libdir}/wine/%{winepedir}/wer.dll
%{_libdir}/wine/%{winepedir}/wevtapi.dll
%{_libdir}/wine/%{winepedir}/wevtsvc.dll
%{_libdir}/wine/%{winepedir}/wiaservc.dll
%{_libdir}/wine/%{winepedir}/wimgapi.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/win32k.sys
%endif
%{_libdir}/wine/%{winepedir}/win32u.dll
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/windows.gaming.input.dll
%{_libdir}/wine/%{winepedir}/windows.globalization.dll
%{_libdir}/wine/%{winepedir}/windows.media.speech.dll
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/windows.media.devices.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/windows.networking.connectivity
%endif
%{_libdir}/wine/%{winepedir}/windowscodecs.dll
%{_libdir}/wine/%{winesodir}/windowscodecs.so
%{_libdir}/wine/%{winepedir}/windowscodecsext.dll
%{_libdir}/wine/%{winepedir}/winebus.sys
%{_libdir}/wine/%{winesodir}/winebus.sys.so
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winepedir}/winegstreamer.dll
%{_libdir}/wine/%{winepedir}/winehid.sys
%{_libdir}/wine/%{winepedir}/winejoystick.drv
%{_libdir}/wine/%{winesodir}/winejoystick.drv.so
%{_libdir}/wine/%{winepedir}/winemapi.dll
%{_libdir}/wine/%{winepedir}/wineusb.sys
%{_libdir}/wine/%{winesodir}/wineusb.sys.so
%{_libdir}/wine/%{winesodir}/winevulkan.so
%{_libdir}/wine/%{winepedir}/winevulkan.dll
# wayland
%{_libdir}/wine/%{winepedir}/winewayland.drv
%{_libdir}/wine/%{winesodir}/winewayland.drv.so
# end wayland
%{_libdir}/wine/%{winepedir}/winex11.drv
%{_libdir}/wine/%{winesodir}/winex11.drv.so
%{_libdir}/wine/%{winepedir}/wing32.dll
%{_libdir}/wine/%{winepedir}/winhttp.dll
%{_libdir}/wine/%{winepedir}/wininet.dll
%{_libdir}/wine/%{winepedir}/winmm.dll
%{_libdir}/wine/%{winepedir}/winnls32.dll
%{_libdir}/wine/%{winepedir}/winspool.drv
%{_libdir}/wine/%{winesodir}/winspool.drv.so
%{_libdir}/wine/%{winepedir}/winsta.dll
%{_libdir}/wine/%{winepedir}/wmasf.dll
%{_libdir}/wine/%{winepedir}/wmi.dll
%{_libdir}/wine/%{winepedir}/wmic.exe
%{_libdir}/wine/%{winepedir}/wmiutils.dll
%{_libdir}/wine/%{winepedir}/wmp.dll
%{_libdir}/wine/%{winepedir}/wmvcore.dll
%{_libdir}/wine/%{winepedir}/spoolss.dll
%{_libdir}/wine/%{winepedir}/winscard.dll
%{_libdir}/wine/%{winepedir}/wintab32.dll
%{_libdir}/wine/%{winepedir}/wintrust.dll
%{_libdir}/wine/%{winepedir}/winusb.dll
%{_libdir}/wine/%{winepedir}/wlanapi.dll
%{_libdir}/wine/%{winepedir}/wlanui.dll
%{_libdir}/wine/%{winesodir}/wmphoto.so
%{_libdir}/wine/%{winepedir}/wmphoto.dll
%{_libdir}/wine/%{winepedir}/wnaspi32.dll
%{_libdir}/wine/%{winesodir}/wnaspi32.dll.so
# wayland
#%%if 0%%{?wine_staging}
%ifarch x86_64
%{_libdir}/wine/%{winepedir}/wow64.dll
%{_libdir}/wine/%{winepedir}/wow64cpu.dll
%{_libdir}/wine/%{winepedir}/wow64win.dll
%endif
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/wpc.dll
%{_libdir}/wine/%{winepedir}/wpcap.dll
%{_libdir}/wine/%{winesodir}/wpcap.so
%{_libdir}/wine/%{winepedir}/ws2_32.dll
%{_libdir}/wine/%{winesodir}/ws2_32.so
%{_libdir}/wine/%{winepedir}/wsdapi.dll
%{_libdir}/wine/%{winepedir}/wshom.ocx
%{_libdir}/wine/%{winepedir}/wsnmp32.dll
%{_libdir}/wine/%{winepedir}/wsock32.dll
%{_libdir}/wine/%{winepedir}/wtsapi32.dll
%{_libdir}/wine/%{winepedir}/wuapi.dll
%{_libdir}/wine/%{winepedir}/wuaueng.dll
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/wuauserv.exe
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/wuauserv.exe.so
%endif
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/security.dll
%{_libdir}/wine/%{winepedir}/sfc.dll
%{_libdir}/wine/%{winepedir}/wineps.drv
%{_libdir}/wine/%{winepedir}/d3d8.dll
%{_libdir}/wine/%{winepedir}/d3d8thk.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d9.dll
%{_libdir}/wine/%{winepedir}/wine-d3d9.dll
%{_libdir}/wine/%{winepedir}/opengl32.dll
%{_libdir}/wine/%{winesodir}/opengl32.dll.so
%{_libdir}/wine/%{winepedir}/wined3d.dll
%{_libdir}/wine/%{winesodir}/wined3d.dll.so
%{_libdir}/wine/%{winepedir}/dnsapi.dll
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winepedir}/iexplore.exe
%{_libdir}/wine/%{winepedir}/x3daudio1_0.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_0.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_1.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_1.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_2.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_2.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_3.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_3.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_4.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_4.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_5.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_5.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_6.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_6.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_7.dll
%{_libdir}/wine/%{winesodir}/x3daudio1_7.dll.so
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winepedir}/xactengine2_0.dll
%{_libdir}/wine/%{winesodir}/xactengine2_0.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_4.dll
%{_libdir}/wine/%{winesodir}/xactengine2_4.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_7.dll
%{_libdir}/wine/%{winesodir}/xactengine2_7.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_9.dll
%{_libdir}/wine/%{winesodir}/xactengine2_9.dll.so
#%%endif
# end wayland
%{_libdir}/wine/%{winepedir}/xactengine3_0.dll
%{_libdir}/wine/%{winesodir}/xactengine3_0.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_1.dll
%{_libdir}/wine/%{winesodir}/xactengine3_1.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_2.dll
%{_libdir}/wine/%{winesodir}/xactengine3_2.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_3.dll
%{_libdir}/wine/%{winesodir}/xactengine3_3.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_4.dll
%{_libdir}/wine/%{winesodir}/xactengine3_4.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_5.dll
%{_libdir}/wine/%{winesodir}/xactengine3_5.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_6.dll
%{_libdir}/wine/%{winesodir}/xactengine3_6.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_7.dll
%{_libdir}/wine/%{winesodir}/xactengine3_7.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_1.dll
%{_libdir}/wine/%{winesodir}/xapofx1_1.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_2.dll
%{_libdir}/wine/%{winesodir}/xapofx1_2.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_3.dll
%{_libdir}/wine/%{winesodir}/xapofx1_3.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_4.dll
%{_libdir}/wine/%{winesodir}/xapofx1_4.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_5.dll
%{_libdir}/wine/%{winesodir}/xapofx1_5.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_0.dll
%{_libdir}/wine/%{winesodir}/xaudio2_0.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_1.dll
%{_libdir}/wine/%{winesodir}/xaudio2_1.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_2.dll
%{_libdir}/wine/%{winesodir}/xaudio2_2.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_3.dll
%{_libdir}/wine/%{winesodir}/xaudio2_3.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_4.dll
%{_libdir}/wine/%{winesodir}/xaudio2_4.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_5.dll
%{_libdir}/wine/%{winesodir}/xaudio2_5.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_6.dll
%{_libdir}/wine/%{winesodir}/xaudio2_6.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_7.dll
%{_libdir}/wine/%{winesodir}/xaudio2_7.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_8.dll
%{_libdir}/wine/%{winesodir}/xaudio2_8.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_9.dll
%{_libdir}/wine/%{winesodir}/xaudio2_9.dll.so
%{_libdir}/wine/%{winepedir}/xcopy.exe
%{_libdir}/wine/%{winepedir}/xinput1_1.dll
%{_libdir}/wine/%{winepedir}/xinput1_2.dll
%{_libdir}/wine/%{winepedir}/xinput1_3.dll
%{_libdir}/wine/%{winepedir}/xinput1_4.dll
%{_libdir}/wine/%{winepedir}/xinput9_1_0.dll
%{_libdir}/wine/%{winepedir}/xmllite.dll
%{_libdir}/wine/%{winepedir}/xolehlp.dll
%{_libdir}/wine/%{winepedir}/xpsprint.dll
%{_libdir}/wine/%{winepedir}/xpssvcs.dll

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winepedir}/nvapi64.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/nvapi64.dll.so
%endif
%{_libdir}/wine/%{winepedir}/nvencodeapi64.dll
%{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%else
%{_libdir}/wine/%{winepedir}/nvapi.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/nvapi.dll.so
%endif
%{_libdir}/wine/%{winepedir}/nvencodeapi.dll
%{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/%{winepedir}/winevdm.exe
%{_libdir}/wine/%{winesodir}/winevdm.exe.so
%{_libdir}/wine/%{winepedir}/ifsmgr.vxd
%{_libdir}/wine/%{winepedir}/mmdevldr.vxd
%{_libdir}/wine/%{winepedir}/monodebg.vxd
%{_libdir}/wine/%{winepedir}/rundll.exe16
%{_libdir}/wine/%{winepedir}/vdhcp.vxd
%{_libdir}/wine/%{winepedir}/user.exe16
%{_libdir}/wine/%{winepedir}/vmm.vxd
%{_libdir}/wine/%{winepedir}/vnbt.vxd
%{_libdir}/wine/%{winepedir}/vnetbios.vxd
%{_libdir}/wine/%{winepedir}/vtdapi.vxd
%{_libdir}/wine/%{winepedir}/vwin32.vxd
%{_libdir}/wine/%{winepedir}/w32skrnl.dll
%{_libdir}/wine/%{winepedir}/avifile.dll16
%{_libdir}/wine/%{winepedir}/comm.drv16
%{_libdir}/wine/%{winepedir}/commdlg.dll16
%{_libdir}/wine/%{winepedir}/compobj.dll16
%{_libdir}/wine/%{winepedir}/ctl3d.dll16
%{_libdir}/wine/%{winepedir}/ctl3dv2.dll16
%{_libdir}/wine/%{winepedir}/ddeml.dll16
%{_libdir}/wine/%{winepedir}/dispdib.dll16
%{_libdir}/wine/%{winepedir}/display.drv16
%{_libdir}/wine/%{winepedir}/gdi.exe16
%{_libdir}/wine/%{winepedir}/imm.dll16
%{_libdir}/wine/%{winepedir}/krnl386.exe16
%{_libdir}/wine/%{winepedir}/keyboard.drv16
%{_libdir}/wine/%{winepedir}/lzexpand.dll16
%{_libdir}/wine/%{winepedir}/mmsystem.dll16
%{_libdir}/wine/%{winepedir}/mouse.drv16
%{_libdir}/wine/%{winepedir}/msacm.dll16
%{_libdir}/wine/%{winepedir}/msvideo.dll16
%{_libdir}/wine/%{winepedir}/ole2.dll16
%{_libdir}/wine/%{winepedir}/ole2conv.dll16
%{_libdir}/wine/%{winepedir}/ole2disp.dll16
%{_libdir}/wine/%{winepedir}/ole2nls.dll16
%{_libdir}/wine/%{winepedir}/ole2prox.dll16
%{_libdir}/wine/%{winepedir}/ole2thk.dll16
%{_libdir}/wine/%{winepedir}/olecli.dll16
%{_libdir}/wine/%{winepedir}/olesvr.dll16
%{_libdir}/wine/%{winepedir}/rasapi16.dll16
%{_libdir}/wine/%{winepedir}/setupx.dll16
%{_libdir}/wine/%{winepedir}/shell.dll16
%{_libdir}/wine/%{winepedir}/sound.drv16
%{_libdir}/wine/%{winepedir}/storage.dll16
%{_libdir}/wine/%{winepedir}/stress.dll16
%{_libdir}/wine/%{winepedir}/system.drv16
%{_libdir}/wine/%{winepedir}/toolhelp.dll16
%{_libdir}/wine/%{winepedir}/twain.dll16
%{_libdir}/wine/%{winepedir}/typelib.dll16
%{_libdir}/wine/%{winepedir}/ver.dll16
%{_libdir}/wine/%{winepedir}/w32sys.dll16
%{_libdir}/wine/%{winepedir}/win32s16.dll16
%{_libdir}/wine/%{winepedir}/win87em.dll16
%{_libdir}/wine/%{winepedir}/winaspi.dll16
%{_libdir}/wine/%{winepedir}/windebug.dll16
%{_libdir}/wine/%{winepedir}/wineps16.drv16
%{_libdir}/wine/%{winepedir}/wing.dll16
%{_libdir}/wine/%{winepedir}/winhelp.exe16
%{_libdir}/wine/%{winepedir}/winnls.dll16
%{_libdir}/wine/%{winepedir}/winoldap.mod16
%{_libdir}/wine/%{winepedir}/winsock.dll16
%{_libdir}/wine/%{winepedir}/wintab.dll16
%{_libdir}/wine/%{winepedir}/wow32.dll
%endif

# ARM SOs
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/explorer.exe.so
%{_libdir}/wine/%{winesodir}/cabarc.exe.so
%{_libdir}/wine/%{winesodir}/control.exe.so
%{_libdir}/wine/%{winesodir}/cmd.exe.so
%{_libdir}/wine/%{winesodir}/dxdiag.exe.so
%{_libdir}/wine/%{winesodir}/notepad.exe.so
%{_libdir}/wine/%{winesodir}/plugplay.exe.so
%{_libdir}/wine/%{winesodir}/progman.exe.so
%{_libdir}/wine/%{winesodir}/taskmgr.exe.so
%{_libdir}/wine/%{winesodir}/winefile.exe.so
%{_libdir}/wine/%{winesodir}/winemine.exe.so
%{_libdir}/wine/%{winesodir}/winemsibuilder.exe.so
%{_libdir}/wine/%{winesodir}/winepath.exe.so
%{_libdir}/wine/%{winesodir}/winmgmt.exe.so
%{_libdir}/wine/%{winesodir}/winver.exe.so
%{_libdir}/wine/%{winesodir}/wordpad.exe.so
%{_libdir}/wine/%{winesodir}/write.exe.so
%{_libdir}/wine/%{winesodir}/wusa.exe.so
%{_libdir}/wine/%{winesodir}/attrib.exe.so
%{_libdir}/wine/%{winesodir}/arp.exe.so
%{_libdir}/wine/%{winesodir}/aspnet_regiis.exe.so
%{_libdir}/wine/%{winesodir}/cacls.exe.so
%{_libdir}/wine/%{winesodir}/conhost.exe.so
%{_libdir}/wine/%{winesodir}/cscript.exe.so
%{_libdir}/wine/%{winesodir}/dism.exe.so
%{_libdir}/wine/%{winesodir}/dplaysvr.exe.so
%{_libdir}/wine/%{winesodir}/dpnsvr.exe.so
%{_libdir}/wine/%{winesodir}/dpvsetup.exe.so
%{_libdir}/wine/%{winesodir}/eject.exe.so
%{_libdir}/wine/%{winesodir}/expand.exe.so
%{_libdir}/wine/%{winesodir}/extrac32.exe.so
%{_libdir}/wine/%{winesodir}/fc.exe.so
%{_libdir}/wine/%{winesodir}/find.exe.so
%{_libdir}/wine/%{winesodir}/findstr.exe.so
%{_libdir}/wine/%{winesodir}/fsutil.exe.so
%{_libdir}/wine/%{winesodir}/hostname.exe.so
%{_libdir}/wine/%{winesodir}/ipconfig.exe.so
%{_libdir}/wine/%{winesodir}/winhlp32.exe.so
%{_libdir}/wine/%{winesodir}/mshta.exe.so
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winesodir}/msidb.exe.so
#%%endif
# end wayland
%{_libdir}/wine/%{winesodir}/msiexec.exe.so
%{_libdir}/wine/%{winesodir}/net.exe.so
%{_libdir}/wine/%{winesodir}/netstat.exe.so
%{_libdir}/wine/%{winesodir}/ngen.exe.so
%{_libdir}/wine/%{winesodir}/ntoskrnl.exe.so
%{_libdir}/wine/%{winesodir}/oleview.exe.so
%{_libdir}/wine/%{winesodir}/ping.exe.so
%{_libdir}/wine/%{winesodir}/powershell.exe.so
%{_libdir}/wine/%{winesodir}/reg.exe.so
%{_libdir}/wine/%{winesodir}/regasm.exe.so
%{_libdir}/wine/%{winesodir}/regedit.exe.so
%{_libdir}/wine/%{winesodir}/regsvcs.exe.so
%{_libdir}/wine/%{winesodir}/regsvr32.exe.so
%{_libdir}/wine/%{winesodir}/rpcss.exe.so
%{_libdir}/wine/%{winesodir}/rundll32.exe.so
%{_libdir}/wine/%{winesodir}/schtasks.exe.so
%{_libdir}/wine/%{winesodir}/sdbinst.exe.so
%{_libdir}/wine/%{winesodir}/secedit.exe.so
%{_libdir}/wine/%{winesodir}/servicemodelreg.exe.so
%{_libdir}/wine/%{winesodir}/services.exe.so
%{_libdir}/wine/%{winesodir}/start.exe.so
%{_libdir}/wine/%{winesodir}/tasklist.exe.so
%{_libdir}/wine/%{winesodir}/termsv.exe.so
%{_libdir}/wine/%{winesodir}/view.exe.so
%{_libdir}/wine/%{winesodir}/wevtutil.exe.so
%{_libdir}/wine/%{winesodir}/where.exe.so
%{_libdir}/wine/%{winesodir}/whoami.exe.so
%{_libdir}/wine/%{winesodir}/wineboot.exe.so
%{_libdir}/wine/%{winesodir}/wineconsole.exe.so
%{_libdir}/wine/%{winesodir}/winedevice.exe.so
%{_libdir}/wine/%{winesodir}/wmplayer.exe.so
%{_libdir}/wine/%{winesodir}/wscript.exe.so
%{_libdir}/wine/%{winesodir}/uninstaller.exe.so
%{_libdir}/wine/%{winesodir}/acledit.dll.so
%{_libdir}/wine/%{winesodir}/aclui.dll.so
%{_libdir}/wine/%{winesodir}/activeds.dll.so
%{_libdir}/wine/%{winesodir}/activeds.tlb.so
%{_libdir}/wine/%{winesodir}/actxprxy.dll.so
%{_libdir}/wine/%{winesodir}/adsldp.dll.so
%{_libdir}/wine/%{winesodir}/adsldpc.dll.so
%{_libdir}/wine/%{winesodir}/advapi32.dll.so
%{_libdir}/wine/%{winesodir}/advpack.dll.so
%{_libdir}/wine/%{winesodir}/amsi.dll.so
%{_libdir}/wine/%{winesodir}/amstream.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-appmodel-identity-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-appmodel-runtime-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-appmodel-runtime-l1-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-apiquery-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-appcompat-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-appinit-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-atoms-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-bem-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-com-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-com-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-com-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-comm-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-console-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-console-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-console-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-crt-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-crt-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-datetime-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-datetime-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-debug-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-debug-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-delayload-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-delayload-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-errorhandling-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-errorhandling-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-errorhandling-l1-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-errorhandling-l1-1-3.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-fibers-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-fibers-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l1-2-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l1-2-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l2-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-l2-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-ansi-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-file-fromapp-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-handle-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-heap-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-heap-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-heap-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-heap-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-interlocked-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-interlocked-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-io-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-io-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-job-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-job-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-largeinteger-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-kernel32-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-kernel32-legacy-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-kernel32-legacy-l1-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-kernel32-private-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l1-2-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l1-2-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-libraryloader-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-l1-2-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-l1-2-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-obsolete-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-obsolete-l1-3-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localization-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-localregistry-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-memory-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-memory-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-memory-l1-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-memory-l1-1-3.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-memory-l1-1-4.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-misc-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-namedpipe-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-namedpipe-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-namedpipe-ansi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-namespace-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-normalization-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-path-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-privateprofile-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processenvironment-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processenvironment-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processthreads-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processthreads-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processthreads-l1-1-2.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processthreads-l1-1-3.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-processtopology-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-profile-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-psapi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-psapi-ansi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-psapi-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-quirks-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-realtime-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-registry-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-registry-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-registry-l2-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-registryuserspecific-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-rtlsupport-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-rtlsupport-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-shlwapi-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-shlwapi-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-shlwapi-obsolete-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-shutdown-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-sidebyside-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-string-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-string-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-string-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-stringansi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-stringloader-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-synch-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-synch-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-synch-l1-2-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-synch-ansi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-sysinfo-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-sysinfo-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-sysinfo-l1-2-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-systemtopology-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-threadpool-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-threadpool-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-threadpool-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-threadpool-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-timezone-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-toolhelp-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-url-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-util-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-version-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-version-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-version-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-versionansi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-windowserrorreporting-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-error-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-error-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-errorprivate-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-registration-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-roparameterizediid-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-string-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-winrt-string-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-wow64-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-wow64-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-xstate-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-core-xstate-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-conio-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-convert-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-environment-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-filesystem-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-heap-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-locale-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-math-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-multibyte-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-process-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-runtime-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-stdio-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-string-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-time-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-crt-utility-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-devices-config-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-devices-config-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-devices-query-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-advapi32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-advapi32-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-kernel32-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-normaliz-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-ole32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-shell32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-shlwapi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-shlwapi-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-user32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-downlevel-version-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-dx-d3dkmt-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventing-classicprovider-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventing-consumer-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventing-controller-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventing-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventing-provider-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-eventlog-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-gaming-tcui-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-gdi-dpiinfo-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-mm-joystick-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-mm-misc-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-mm-mme-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-mm-time-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-ntuser-dc-access-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-ntuser-rectangle-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-ntuser-sysparams-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-perf-legacy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-power-base-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-power-setting-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-draw-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-private-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-private-l1-1-4.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-window-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-winevent-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-activedirectoryclient-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-audit-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-base-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-base-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-base-private-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-credentials-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-cryptoapi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-grouppolicy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-lsalookup-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-lsalookup-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-lsalookup-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-lsalookup-l2-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-lsapolicy-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-provider-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-sddl-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-security-systemfunctions-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-core-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-core-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-management-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-management-l2-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-private-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-winsvc-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-service-winsvc-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-obsolete-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-scaling-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-scaling-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-stream-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-stream-winrt-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shcore-thread-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shell-shellcom-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/api-ms-win-shell-shellfolders-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/apphelp.dll.so
%{_libdir}/wine/%{winesodir}/appwiz.cpl.so
%{_libdir}/wine/%{winesodir}/atl.dll.so
%{_libdir}/wine/%{winesodir}/atl80.dll.so
%{_libdir}/wine/%{winesodir}/atl90.dll.so
%{_libdir}/wine/%{winesodir}/atl100.dll.so
%{_libdir}/wine/%{winesodir}/atl110.dll.so
%{_libdir}/wine/%{winesodir}/atlthunk.dll.so
%{_libdir}/wine/%{winesodir}/atmlib.dll.so
%{_libdir}/wine/%{winesodir}/authz.dll.so
%{_libdir}/wine/%{winesodir}/avifil32.dll.so
%{_libdir}/wine/%{winesodir}/avrt.dll.so
%{_libdir}/wine/%{winesodir}/bcrypt.dll.so
%{_libdir}/wine/%{winesodir}/bluetoothapis.dll.so
%{_libdir}/wine/%{winesodir}/browseui.dll.so
%{_libdir}/wine/%{winesodir}/bthprops.cpl.so
%{_libdir}/wine/%{winesodir}/cabinet.dll.so
%{_libdir}/wine/%{winesodir}/cards.dll.so
%{_libdir}/wine/%{winesodir}/cdosys.dll.so
%{_libdir}/wine/%{winesodir}/cfgmgr32.dll.so
%{_libdir}/wine/%{winesodir}/chcp.com.so
%{_libdir}/wine/%{winesodir}/clock.exe.so
%{_libdir}/wine/%{winesodir}/clusapi.dll.so
%{_libdir}/wine/%{winesodir}/combase.dll.so
%{_libdir}/wine/%{winesodir}/comcat.dll.so
%{_libdir}/wine/%{winesodir}/comctl32.dll.so
%{_libdir}/wine/%{winesodir}/comdlg32.dll.so
%{_libdir}/wine/%{winesodir}/compstui.dll.so
%{_libdir}/wine/%{winesodir}/comsvcs.dll.so
%{_libdir}/wine/%{winesodir}/concrt140.dll.so
%{_libdir}/wine/%{winesodir}/connect.dll.so
%{_libdir}/wine/%{winesodir}/credui.dll.so
%{_libdir}/wine/%{winesodir}/crtdll.dll.so
%{_libdir}/wine/%{winesodir}/crypt32.dll.so
%{_libdir}/wine/%{winesodir}/cryptdlg.dll.so
%{_libdir}/wine/%{winesodir}/cryptdll.dll.so
%{_libdir}/wine/%{winesodir}/cryptext.dll.so
%{_libdir}/wine/%{winesodir}/cryptnet.dll.so
%{_libdir}/wine/%{winesodir}/cryptsp.dll.so
%{_libdir}/wine/%{winesodir}/cryptui.dll.so
%{_libdir}/wine/%{winesodir}/ctl3d32.dll.so
%{_libdir}/wine/%{winesodir}/d2d1.dll.so
%{_libdir}/wine/%{winesodir}/d3d10.dll.so
%{_libdir}/wine/%{winesodir}/d3d10_1.dll.so
%{_libdir}/wine/%{winesodir}/d3d10core.dll.so
%{_libdir}/wine/%{winesodir}/d3d11.dll.so
%{_libdir}/wine/%{winesodir}/d3dcompiler_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dim.dll.so
%{_libdir}/wine/%{winesodir}/d3dim700.dll.so
%{_libdir}/wine/%{winesodir}/d3drm.dll.so
%{_libdir}/wine/%{winesodir}/d3dx9_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dx10_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dx11_42.dll.so
%{_libdir}/wine/%{winesodir}/d3dx11_43.dll.so
%{_libdir}/wine/%{winesodir}/d3dxof.dll.so
%{_libdir}/wine/%{winesodir}/davclnt.dll.so
%{_libdir}/wine/%{winesodir}/dbgeng.dll.so
%{_libdir}/wine/%{winesodir}/dbghelp.dll.so
%{_libdir}/wine/%{winesodir}/dciman32.dll.so
%{_libdir}/wine/%{winesodir}/dcomp.dll.so
%{_libdir}/wine/%{winesodir}/ddraw.dll.so
%{_libdir}/wine/%{winesodir}/ddrawex.dll.so
%{_libdir}/wine/%{winesodir}/devenum.dll.so
%{_libdir}/wine/%{winesodir}/dhcpcsvc.dll.so
%{_libdir}/wine/%{winesodir}/dhtmled.ocx.so
%{_libdir}/wine/%{winesodir}/difxapi.dll.so
%{_libdir}/wine/%{winesodir}/directmanipulation.dll.so
%{_libdir}/wine/%{winesodir}/dispex.dll.so
%{_libdir}/wine/%{winesodir}/dmband.dll.so
%{_libdir}/wine/%{winesodir}/dmcompos.dll.so
%{_libdir}/wine/%{winesodir}/dmime.dll.so
%{_libdir}/wine/%{winesodir}/dmloader.dll.so
%{_libdir}/wine/%{winesodir}/dmscript.dll.so
%{_libdir}/wine/%{winesodir}/dmstyle.dll.so
%{_libdir}/wine/%{winesodir}/dmsynth.dll.so
%{_libdir}/wine/%{winesodir}/dmusic.dll.so
%{_libdir}/wine/%{winesodir}/dmusic32.dll.so
%{_libdir}/wine/%{winesodir}/dplay.dll.so
%{_libdir}/wine/%{winesodir}/dplayx.dll.so
%{_libdir}/wine/%{winesodir}/dpnaddr.dll.so
%{_libdir}/wine/%{winesodir}/dpnet.dll.so
%{_libdir}/wine/%{winesodir}/dpnhpast.dll.so
%{_libdir}/wine/%{winesodir}/dpnlobby.dll.so
%{_libdir}/wine/%{winesodir}/dpvoice.dll.so
%{_libdir}/wine/%{winesodir}/dpwsockx.dll.so
%{_libdir}/wine/%{winesodir}/drmclien.dll.so
%{_libdir}/wine/%{winesodir}/dsound.dll.so
%{_libdir}/wine/%{winesodir}/dsdmo.dll.so
%{_libdir}/wine/%{winesodir}/dsquery.dll.so
%{_libdir}/wine/%{winesodir}/dssenh.dll.so
%{_libdir}/wine/%{winesodir}/dsuiext.dll.so
%{_libdir}/wine/%{winesodir}/dswave.dll.so
%{_libdir}/wine/%{winesodir}/dwmapi.dll.so
%{_libdir}/wine/%{winesodir}/dwrite.dll.so
%{_libdir}/wine/%{winesodir}/dx8vb.dll.so
%{_libdir}/wine/%{winesodir}/dxdiagn.dll.so
%{_libdir}/wine/%{winesodir}/dxgkrnl.sys.so
%{_libdir}/wine/%{winesodir}/dxgmms1.sys.so
%{_libdir}/wine/%{winesodir}/dxva2.dll.so
%{_libdir}/wine/%{winesodir}/esent.dll.so
%{_libdir}/wine/%{winesodir}/evr.dll.so
%{_libdir}/wine/%{winesodir}/explorerframe.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-authz-context-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-domainjoin-netjoin-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-dwmapi-ext-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-dc-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-dc-create-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-dc-create-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-devcaps-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-draw-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-draw-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-font-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-font-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-gdi-render-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-kernel32-package-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-kernel32-package-current-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-dialogbox-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-draw-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-gui-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-gui-l1-3-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-keyboard-l1-3-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-misc-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-misc-l1-5-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-message-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-message-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-misc-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-mouse-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-private-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-private-l1-3-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-rectangle-ext-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-uicontext-ext-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-window-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-window-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-window-l1-1-4.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-windowclass-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ntuser-windowclass-l1-1-1.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-oleacc-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-ras-rasapi32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-gdi-object-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-gdi-rgn-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-security-credui-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-security-cryptui-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-shell-comctl32-init-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-shell-comdlg32-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-shell-shell32-l1-2-0.dll.so
%{_libdir}/wine/%{winesodir}/ext-ms-win-uxtheme-themes-l1-1-0.dll.so
%{_libdir}/wine/%{winesodir}/faultrep.dll.so
%{_libdir}/wine/%{winesodir}/feclient.dll.so
%{_libdir}/wine/%{winesodir}/fltlib.dll.so
%{_libdir}/wine/%{winesodir}/fltmgr.sys.so
%{_libdir}/wine/%{winesodir}/fntcache.dll.so
%{_libdir}/wine/%{winesodir}/fontsub.dll.so
%{_libdir}/wine/%{winesodir}/fusion.dll.so
%{_libdir}/wine/%{winesodir}/fwpuclnt.dll.so
%{_libdir}/wine/%{winesodir}/gameux.dll.so
%{_libdir}/wine/%{winesodir}/gamingtcui.dll.so
%{_libdir}/wine/%{winesodir}/gdi32.dll.so
%{_libdir}/wine/%{winesodir}/gdiplus.dll.so
%{_libdir}/wine/%{winesodir}/glu32.dll.so
%{_libdir}/wine/%{winesodir}/gpkcsp.dll.so
%{_libdir}/wine/%{winesodir}/hal.dll.so
%{_libdir}/wine/%{winesodir}/hh.exe.so
%{_libdir}/wine/%{winesodir}/hhctrl.ocx.so
%{_libdir}/wine/%{winesodir}/hid.dll.so
%{_libdir}/wine/%{winesodir}/hidclass.sys.so
%{_libdir}/wine/%{winesodir}/hlink.dll.so
%{_libdir}/wine/%{winesodir}/hnetcfg.dll.so
%{_libdir}/wine/%{winesodir}/http.sys.so
%{_libdir}/wine/%{winesodir}/httpapi.dll.so
%{_libdir}/wine/%{winesodir}/icacls.exe.so
%{_libdir}/wine/%{winesodir}/iccvid.dll.so
%{_libdir}/wine/%{winesodir}/icinfo.exe.so
%{_libdir}/wine/%{winesodir}/icmp.dll.so
%{_libdir}/wine/%{winesodir}/ieframe.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/iertutil.dll.so
%endif
%{_libdir}/wine/%{winesodir}/ieproxy.dll.so
%{_libdir}/wine/%{winesodir}/imaadp32.acm.so
%{_libdir}/wine/%{winesodir}/imagehlp.dll.so
%{_libdir}/wine/%{winesodir}/imm32.dll.so
%{_libdir}/wine/%{winesodir}/inetcomm.dll.so
%{_libdir}/wine/%{winesodir}/inetcpl.cpl.so
%{_libdir}/wine/%{winesodir}/inetmib1.dll.so
%{_libdir}/wine/%{winesodir}/infosoft.dll.so
%{_libdir}/wine/%{winesodir}/initpki.dll.so
%{_libdir}/wine/%{winesodir}/inkobj.dll.so
%{_libdir}/wine/%{winesodir}/inseng.dll.so
%{_libdir}/wine/%{winesodir}/iprop.dll.so
%{_libdir}/wine/%{winesodir}/irprops.cpl.so
%{_libdir}/wine/%{winesodir}/itircl.dll.so
%{_libdir}/wine/%{winesodir}/itss.dll.so
%{_libdir}/wine/%{winesodir}/joy.cpl.so
%{_libdir}/wine/%{winesodir}/jscript.dll.so
%{_libdir}/wine/%{winesodir}/jsproxy.dll.so
%{_libdir}/wine/%{winesodir}/kerberos.dll.so
%{_libdir}/wine/%{winesodir}/kernel32.dll.so
%{_libdir}/wine/%{winesodir}/kernelbase.dll.so
%{_libdir}/wine/%{winesodir}/ksecdd.sys.so
%{_libdir}/wine/%{winesodir}/ksproxy.ax.so
%{_libdir}/wine/%{winesodir}/ksuser.dll.so
%{_libdir}/wine/%{winesodir}/ktmw32.dll.so
%{_libdir}/wine/%{winesodir}/light.msstyles.so
%{_libdir}/wine/%{winesodir}/loadperf.dll.so
%{_libdir}/wine/%{winesodir}/localspl.dll.so
%{_libdir}/wine/%{winesodir}/localui.dll.so
%{_libdir}/wine/%{winesodir}/lodctr.exe.so
%{_libdir}/wine/%{winesodir}/lz32.dll.so
%{_libdir}/wine/%{winesodir}/mapi32.dll.so
%{_libdir}/wine/%{winesodir}/mapistub.dll.so
%{_libdir}/wine/%{winesodir}/mciavi32.dll.so
%{_libdir}/wine/%{winesodir}/mcicda.dll.so
%{_libdir}/wine/%{winesodir}/mciqtz32.dll.so
%{_libdir}/wine/%{winesodir}/mciseq.dll.so
%{_libdir}/wine/%{winesodir}/mciwave.dll.so
%{_libdir}/wine/%{winesodir}/mf.dll.so
%{_libdir}/wine/%{winesodir}/mf3216.dll.so
%{_libdir}/wine/%{winesodir}/mferror.dll.so
%{_libdir}/wine/%{winesodir}/mfmediaengine.dll.so
%{_libdir}/wine/%{winesodir}/mfplat.dll.so
%{_libdir}/wine/%{winesodir}/mfplay.dll.so
%{_libdir}/wine/%{winesodir}/mfreadwrite.dll.so
%{_libdir}/wine/%{winesodir}/mgmtapi.dll.so
%{_libdir}/wine/%{winesodir}/midimap.dll.so
%{_libdir}/wine/%{winesodir}/mlang.dll.so
%{_libdir}/wine/%{winesodir}/mmcndmgr.dll.so
%{_libdir}/wine/%{winesodir}/mmdevapi.dll.so
%{_libdir}/wine/%{winesodir}/mofcomp.exe.so
%{_libdir}/wine/%{winesodir}/mpr.dll.so
%{_libdir}/wine/%{winesodir}/mprapi.dll.so
%{_libdir}/wine/%{winesodir}/msacm32.dll.so
%{_libdir}/wine/%{winesodir}/msacm32.drv.so
%{_libdir}/wine/%{winesodir}/msado15.dll.so
%{_libdir}/wine/%{winesodir}/msadp32.acm.so
%{_libdir}/wine/%{winesodir}/msasn1.dll.so
%{_libdir}/wine/%{winesodir}/mscat32.dll.so
%{_libdir}/wine/%{winesodir}/mscoree.dll.so
%{_libdir}/wine/%{winesodir}/mscorwks.dll.so
%{_libdir}/wine/%{winesodir}/msctf.dll.so
%{_libdir}/wine/%{winesodir}/msctfp.dll.so
%{_libdir}/wine/%{winesodir}/msdaps.dll.so
%{_libdir}/wine/%{winesodir}/msdelta.dll.so
%{_libdir}/wine/%{winesodir}/msdmo.dll.so
%{_libdir}/wine/%{winesodir}/msdrm.dll.so
%{_libdir}/wine/%{winesodir}/msftedit.dll.so
%{_libdir}/wine/%{winesodir}/msg711.acm.so
%{_libdir}/wine/%{winesodir}/mshtml.dll.so
%{_libdir}/wine/%{winesodir}/mshtml.tlb.so
%{_libdir}/wine/%{winesodir}/msi.dll.so
%{_libdir}/wine/%{winesodir}/msident.dll.so
%{_libdir}/wine/%{winesodir}/msimtf.dll.so
%{_libdir}/wine/%{winesodir}/msimg32.dll.so
%{_libdir}/wine/%{winesodir}/msimsg.dll.so
%{_libdir}/wine/%{winesodir}/msinfo32.exe.so
%{_libdir}/wine/%{winesodir}/msisip.dll.so
%{_libdir}/wine/%{winesodir}/msisys.ocx.so
%{_libdir}/wine/%{winesodir}/msls31.dll.so
%{_libdir}/wine/%{winesodir}/msnet32.dll.so
%{_libdir}/wine/%{winesodir}/mspatcha.dll.so
%{_libdir}/wine/%{winesodir}/msports.dll.so
%{_libdir}/wine/%{winesodir}/msscript.ocx.so
%{_libdir}/wine/%{winesodir}/mssign32.dll.so
%{_libdir}/wine/%{winesodir}/mssip32.dll.so
%{_libdir}/wine/%{winesodir}/msrle32.dll.so
%{_libdir}/wine/%{winesodir}/mstask.dll.so
%{_libdir}/wine/%{winesodir}/msv1_0.dll.so
%{_libdir}/wine/%{winesodir}/msvcirt.dll.so
%{_libdir}/wine/%{winesodir}/msvcm80.dll.so
%{_libdir}/wine/%{winesodir}/msvcm90.dll.so
%{_libdir}/wine/%{winesodir}/msvcp60.dll.so
%{_libdir}/wine/%{winesodir}/msvcp70.dll.so
%{_libdir}/wine/%{winesodir}/msvcp71.dll.so
%{_libdir}/wine/%{winesodir}/msvcp80.dll.so
%{_libdir}/wine/%{winesodir}/msvcp90.dll.so
%{_libdir}/wine/%{winesodir}/msvcp100.dll.so
%{_libdir}/wine/%{winesodir}/msvcp110.dll.so
%{_libdir}/wine/%{winesodir}/msvcp120.dll.so
%{_libdir}/wine/%{winesodir}/msvcp120_app.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140_1.dll.so
%{_libdir}/wine/%{winesodir}/msvcr70.dll.so
%{_libdir}/wine/%{winesodir}/msvcr71.dll.so
%{_libdir}/wine/%{winesodir}/msvcr80.dll.so
%{_libdir}/wine/%{winesodir}/msvcr90.dll.so
%{_libdir}/wine/%{winesodir}/msvcr100.dll.so
%{_libdir}/wine/%{winesodir}/msvcr110.dll.so
%{_libdir}/wine/%{winesodir}/msvcr120.dll.so
%{_libdir}/wine/%{winesodir}/msvcr120_app.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt20.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt40.dll.so
%{_libdir}/wine/%{winesodir}/msvcrtd.dll.so
%{_libdir}/wine/%{winesodir}/msvfw32.dll.so
%{_libdir}/wine/%{winesodir}/msvidc32.dll.so
%{_libdir}/wine/%{winesodir}/mswsock.dll.so
%{_libdir}/wine/%{winesodir}/msxml.dll.so
%{_libdir}/wine/%{winesodir}/msxml2.dll.so
%{_libdir}/wine/%{winesodir}/msxml4.dll.so
%{_libdir}/wine/%{winesodir}/msxml6.dll.so
%{_libdir}/wine/%{winesodir}/mtxdm.dll.so
%{_libdir}/wine/%{winesodir}/nddeapi.dll.so
%{_libdir}/wine/%{winesodir}/ncrypt.dll.so
%{_libdir}/wine/%{winesodir}/ndis.sys.so
%{_libdir}/wine/%{winesodir}/netapi32.dll.so
%{_libdir}/wine/%{winesodir}/netcfgx.dll.so
%{_libdir}/wine/%{winesodir}/netio.sys.so
%{_libdir}/wine/%{winesodir}/netprofm.dll.so
%{_libdir}/wine/%{winesodir}/netsh.exe.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/netutils.dll.so
%endif
%{_libdir}/wine/%{winesodir}/newdev.dll.so
%{_libdir}/wine/%{winesodir}/ninput.dll.so
%{_libdir}/wine/%{winesodir}/normaliz.dll.so
%{_libdir}/wine/%{winesodir}/npmshtml.dll.so
%{_libdir}/wine/%{winesodir}/npptools.dll.so
%{_libdir}/wine/%{winesodir}/nsi.dll.so
%{_libdir}/wine/%{winesodir}/ntdll.dll.so
%{_libdir}/wine/%{winesodir}/ntdsapi.dll.so
%{_libdir}/wine/%{winesodir}/ntprint.dll.so
%{_libdir}/wine/%{winesodir}/objsel.dll.so
%{_libdir}/wine/%{winesodir}/odbc32.dll.so
%{_libdir}/wine/%{winesodir}/odbcbcp.dll.so
%{_libdir}/wine/%{winesodir}/odbccp32.dll.so
%{_libdir}/wine/%{winesodir}/odbccu32.dll.so
%{_libdir}/wine/%{winesodir}/ole32.dll.so
%{_libdir}/wine/%{winesodir}/oleacc.dll.so
%{_libdir}/wine/%{winesodir}/oleaut32.dll.so
%{_libdir}/wine/%{winesodir}/olecli32.dll.so
%{_libdir}/wine/%{winesodir}/oledb32.dll.so
%{_libdir}/wine/%{winesodir}/oledlg.dll.so
%{_libdir}/wine/%{winesodir}/olepro32.dll.so
%{_libdir}/wine/%{winesodir}/olesvr32.dll.so
%{_libdir}/wine/%{winesodir}/olethk32.dll.so
%{_libdir}/wine/%{winesodir}/opcservices.dll.so
%{_libdir}/wine/%{winesodir}/packager.dll.so
%{_libdir}/wine/%{winesodir}/pdh.dll.so
%{_libdir}/wine/%{winesodir}/photometadatahandler.dll.so
%{_libdir}/wine/%{winesodir}/pidgen.dll.so
%{_libdir}/wine/%{winesodir}/powrprof.dll.so
%{_libdir}/wine/%{winesodir}/presentationfontcache.exe.so
%{_libdir}/wine/%{winesodir}/printui.dll.so
%{_libdir}/wine/%{winesodir}/prntvpt.dll.so
%{_libdir}/wine/%{winesodir}/propsys.dll.so
%{_libdir}/wine/%{winesodir}/psapi.dll.so
%{_libdir}/wine/%{winesodir}/pstorec.dll.so
%{_libdir}/wine/%{winesodir}/pwrshplugin.dll.so
%{_libdir}/wine/%{winesodir}/qasf.dll.so
%{_libdir}/wine/%{winesodir}/qcap.dll.so
%{_libdir}/wine/%{winesodir}/qdvd.dll.so
%{_libdir}/wine/%{winesodir}/qedit.dll.so
%{_libdir}/wine/%{winesodir}/qmgr.dll.so
%{_libdir}/wine/%{winesodir}/qmgrprxy.dll.so
%{_libdir}/wine/%{winesodir}/quartz.dll.so
%{_libdir}/wine/%{winesodir}/query.dll.so
%{_libdir}/wine/%{winesodir}/qwave.dll.so
%{_libdir}/wine/%{winesodir}/rasapi32.dll.so
%{_libdir}/wine/%{winesodir}/rasdlg.dll.so
%{_libdir}/wine/%{winesodir}/regapi.dll.so
%{_libdir}/wine/%{winesodir}/regini.exe.so
%{_libdir}/wine/%{winesodir}/resutils.dll.so
%{_libdir}/wine/%{winesodir}/riched20.dll.so
%{_libdir}/wine/%{winesodir}/riched32.dll.so
%{_libdir}/wine/%{winesodir}/rpcrt4.dll.so
%{_libdir}/wine/%{winesodir}/rsabase.dll.so
%{_libdir}/wine/%{winesodir}/rsaenh.dll.so
%{_libdir}/wine/%{winesodir}/rstrtmgr.dll.so
%{_libdir}/wine/%{winesodir}/rtutils.dll.so
%{_libdir}/wine/%{winesodir}/rtworkq.dll.so
%{_libdir}/wine/%{winesodir}/samlib.dll.so
%{_libdir}/wine/%{winesodir}/sapi.dll.so
%{_libdir}/wine/%{winesodir}/sas.dll.so
%{_libdir}/wine/%{winesodir}/sc.exe.so
%{_libdir}/wine/%{winesodir}/scarddlg.dll.so
%{_libdir}/wine/%{winesodir}/sccbase.dll.so
%{_libdir}/wine/%{winesodir}/schannel.dll.so
%{_libdir}/wine/%{winesodir}/scrobj.dll.so
%{_libdir}/wine/%{winesodir}/scrrun.dll.so
%{_libdir}/wine/%{winesodir}/scsiport.sys.so
%{_libdir}/wine/%{winesodir}/sechost.dll.so
%{_libdir}/wine/%{winesodir}/secur32.dll.so
%{_libdir}/wine/%{winesodir}/sensapi.dll.so
%{_libdir}/wine/%{winesodir}/serialui.dll.so
%{_libdir}/wine/%{winesodir}/setupapi.dll.so
%{_libdir}/wine/%{winesodir}/sfc_os.dll.so
%{_libdir}/wine/%{winesodir}/shcore.dll.so
%{_libdir}/wine/%{winesodir}/shdoclc.dll.so
%{_libdir}/wine/%{winesodir}/shdocvw.dll.so
%{_libdir}/wine/%{winesodir}/schedsvc.dll.so
%{_libdir}/wine/%{winesodir}/shfolder.dll.so
%{_libdir}/wine/%{winesodir}/shlwapi.dll.so
%{_libdir}/wine/%{winesodir}/shutdown.exe.so
%{_libdir}/wine/%{winesodir}/slbcsp.dll.so
%{_libdir}/wine/%{winesodir}/slc.dll.so
%{_libdir}/wine/%{winesodir}/snmpapi.dll.so
%{_libdir}/wine/%{winesodir}/softpub.dll.so
%{_libdir}/wine/%{winesodir}/spoolsv.exe.so
%{_libdir}/wine/%{winesodir}/sppc.dll.so
%{_libdir}/wine/%{winesodir}/srclient.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/srvcli.dll.so
%endif
%{_libdir}/wine/%{winesodir}/sspicli.dll.so
%{_libdir}/wine/%{winesodir}/stdole2.tlb.so
%{_libdir}/wine/%{winesodir}/stdole32.tlb.so
%{_libdir}/wine/%{winesodir}/sti.dll.so
%{_libdir}/wine/%{winesodir}/strmdll.dll.so
%{_libdir}/wine/%{winesodir}/subst.exe.so
%{_libdir}/wine/%{winesodir}/svchost.exe.so
%{_libdir}/wine/%{winesodir}/svrapi.dll.so
%{_libdir}/wine/%{winesodir}/sxs.dll.so
%{_libdir}/wine/%{winesodir}/systeminfo.exe.so
%{_libdir}/wine/%{winesodir}/t2embed.dll.so
%{_libdir}/wine/%{winesodir}/tapi32.dll.so
%{_libdir}/wine/%{winesodir}/taskkill.exe.so
%{_libdir}/wine/%{winesodir}/taskschd.dll.so
%{_libdir}/wine/%{winesodir}/tbs.dll.so
%{_libdir}/wine/%{winesodir}/tdh.dll.so
%{_libdir}/wine/%{winesodir}/tdi.sys.so
%{_libdir}/wine/%{winesodir}/traffic.dll.so
%{_libdir}/wine/%{winesodir}/tzres.dll.so
%{_libdir}/wine/%{winesodir}/ucrtbase.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/uianimation.dll.so
%endif
%{_libdir}/wine/%{winesodir}/uiautomationcore.dll.so
%{_libdir}/wine/%{winesodir}/uiribbon.dll.so
%{_libdir}/wine/%{winesodir}/unicows.dll.so
%{_libdir}/wine/%{winesodir}/unlodctr.exe.so
%{_libdir}/wine/%{winesodir}/updspapi.dll.so
%{_libdir}/wine/%{winesodir}/url.dll.so
%{_libdir}/wine/%{winesodir}/urlmon.dll.so
%{_libdir}/wine/%{winesodir}/usbd.sys.so
%{_libdir}/wine/%{winesodir}/user32.dll.so
%{_libdir}/wine/%{winesodir}/usp10.dll.so
%{_libdir}/wine/%{winesodir}/utildll.dll.so
%{_libdir}/wine/%{winesodir}/uxtheme.dll.so
%{_libdir}/wine/%{winesodir}/userenv.dll.so
%{_libdir}/wine/%{winesodir}/vbscript.dll.so
%{_libdir}/wine/%{winesodir}/vcomp.dll.so
%{_libdir}/wine/%{winesodir}/vcomp90.dll.so
%{_libdir}/wine/%{winesodir}/vcomp100.dll.so
%{_libdir}/wine/%{winesodir}/vcomp110.dll.so
%{_libdir}/wine/%{winesodir}/vcomp120.dll.so
%{_libdir}/wine/%{winesodir}/vcomp140.dll.so
%{_libdir}/wine/%{winesodir}/vcruntime140.dll.so
%{_libdir}/wine/%{winesodir}/vcruntime140_1.dll.so
%{_libdir}/wine/%{winesodir}/vdmdbg.dll.so
%{_libdir}/wine/%{winesodir}/version.dll.so
%{_libdir}/wine/%{winesodir}/vga.dll.so
%{_libdir}/wine/%{winesodir}/virtdisk.dll.so
%{_libdir}/wine/%{winesodir}/vssapi.dll.so
%{_libdir}/wine/%{winesodir}/vulkan-1.dll.so
%{_libdir}/wine/%{winesodir}/wbemdisp.dll.so
%{_libdir}/wine/%{winesodir}/wbemprox.dll.so
%{_libdir}/wine/%{winesodir}/wdscore.dll.so
%{_libdir}/wine/%{winesodir}/webservices.dll.so
%{_libdir}/wine/%{winesodir}/websocket.dll.so
%{_libdir}/wine/%{winesodir}/wer.dll.so
%{_libdir}/wine/%{winesodir}/wevtapi.dll.so
%{_libdir}/wine/%{winesodir}/wevtsvc.dll.so
%{_libdir}/wine/%{winesodir}/wiaservc.dll.so
%{_libdir}/wine/%{winesodir}/wimgapi.dll.so
%{_libdir}/wine/%{winesodir}/win32u.dll.so
# wayland
#%%if 0%%{?wine_staging}
%{_libdir}/wine/%{winesodir}/windows.gaming.input.dll.so
%{_libdir}/wine/%{winesodir}/windows.globalization.dll.so
%{_libdir}/wine/%{winesodir}/windows.media.speech.dll.so
#%%endif
# end wayland
%{_libdir}/wine/%{winesodir}/windows.media.devices.dll.so
# wayland
#%%{_libdir}/wine/%%{winesodir}/windows.networking.connectivity
# end wayland
%{_libdir}/wine/%{winesodir}/windowscodecs.dll.so
%{_libdir}/wine/%{winesodir}/windowscodecsext.dll.so
%{_libdir}/wine/%{winesodir}/winegstreamer.dll.so
%{_libdir}/wine/%{winesodir}/winehid.sys.so
%{_libdir}/wine/%{winesodir}/winemapi.dll.so
%{_libdir}/wine/%{winesodir}/winevulkan.dll.so

%{_libdir}/wine/%{winesodir}/wing32.dll.so
%{_libdir}/wine/%{winesodir}/winhttp.dll.so
%{_libdir}/wine/%{winesodir}/wininet.dll.so
%{_libdir}/wine/%{winesodir}/winmm.dll.so
%{_libdir}/wine/%{winesodir}/winnls32.dll.so
%{_libdir}/wine/%{winesodir}/winsta.dll.so
%{_libdir}/wine/%{winesodir}/wmasf.dll.so
%{_libdir}/wine/%{winesodir}/wmi.dll.so
%{_libdir}/wine/%{winesodir}/wmic.exe.so
%{_libdir}/wine/%{winesodir}/wmiutils.dll.so
%{_libdir}/wine/%{winesodir}/wmp.dll.so
%{_libdir}/wine/%{winesodir}/wmvcore.dll.so
%{_libdir}/wine/%{winesodir}/spoolss.dll.so
%{_libdir}/wine/%{winesodir}/winscard.dll.so
%{_libdir}/wine/%{winesodir}/wintab32.dll.so
%{_libdir}/wine/%{winesodir}/wintrust.dll.so
%{_libdir}/wine/%{winesodir}/winusb.dll.so
%{_libdir}/wine/%{winesodir}/wlanapi.dll.so
%{_libdir}/wine/%{winesodir}/wlanui.dll.so
%{_libdir}/wine/%{winesodir}/wmphoto.dll.so
%{_libdir}/wine/%{winesodir}/wpc.dll.so
%{_libdir}/wine/%{winesodir}/wpcap.dll.so
%{_libdir}/wine/%{winesodir}/wsdapi.dll.so
%{_libdir}/wine/%{winesodir}/wshom.ocx.so
%{_libdir}/wine/%{winesodir}/wsnmp32.dll.so
%{_libdir}/wine/%{winesodir}/wsock32.dll.so
%{_libdir}/wine/%{winesodir}/wtsapi32.dll.so
%{_libdir}/wine/%{winesodir}/wuapi.dll.so
%{_libdir}/wine/%{winesodir}/wuaueng.dll.so

%{_libdir}/wine/%{winesodir}/security.dll.so
%{_libdir}/wine/%{winesodir}/sfc.dll.so
%{_libdir}/wine/%{winesodir}/wineps.drv.so
%{_libdir}/wine/%{winesodir}/d3d8.dll.so
%{_libdir}/wine/%{winesodir}/d3d8thk.dll.so
%{_libdir}/wine/%{winesodir}/d3d9.dll.so
%{_libdir}/wine/%{winesodir}/dnsapi.dll.so
%{_libdir}/wine/%{winesodir}/iexplore.exe.so
%{_libdir}/wine/%{winesodir}/xcopy.exe.so
%{_libdir}/wine/%{winesodir}/xinput1_1.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_2.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_3.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_4.dll.so
%{_libdir}/wine/%{winesodir}/xinput9_1_0.dll.so
%{_libdir}/wine/%{winesodir}/xmllite.dll.so
%{_libdir}/wine/%{winesodir}/xolehlp.dll.so
%{_libdir}/wine/%{winesodir}/xpsprint.dll.so
%{_libdir}/wine/%{winesodir}/xpssvcs.dll.so
%endif

%files -n wine-filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/nls/

%files -n wine-common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files -n wine-fonts
# meta package

%if 0%{?wine_staging}
%files -n wine-arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif
#0%%{?wine_staging}

%files -n wine-courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files -n wine-fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files -n wine-system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files -n wine-small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files -n wine-marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files -n wine-ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files -n wine-tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files -n wine-tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files -n wine-times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files -n wine-times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files -n wine-symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files -n wine-webdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/webdings.ttf

%files -n wine-wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files -n wine-wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files -n wine-desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_metainfodir}/%{name}.appdata.xml
%if 0%{?fedora} >= 10
%{_datadir}/icons/hicolor/scalable/apps/*svg
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%files -n wine-systemd
%config %{_binfmtdir}/wine.conf
%endif

%if 0%{?rhel} == 6
%files -n wine-sysvinit
%{_initrddir}/wine
%endif

# ldap subpackage
%files -n wine-ldap
%{_libdir}/wine/%{winesodir}/wldap32.so
%{_libdir}/wine/%{winepedir}/wldap32.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/wldap32.dll.so
%endif

# cms subpackage
%files -n wine-cms
%{_libdir}/wine/%{winesodir}/mscms.so
%{_libdir}/wine/%{winepedir}/mscms.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/mscms.dll.so
%endif

# twain subpackage
%files -n wine-twain
%{_libdir}/wine/%{winepedir}/twain_32.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/twain_32.dll.so
%endif
%{_libdir}/wine/%{winepedir}/sane.ds
%{_libdir}/wine/%{winesodir}/sane.ds.so

# capi subpackage
%files -n wine-capi
%{_libdir}/wine/%{winepedir}/capi2032.dll
%{_libdir}/wine/%{winesodir}/capi2032.dll.so

%files -n wine-devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%ifarch %{ix86} x86_64
%{_libdir}/wine/%{winepedir}/*.a
%endif
%{_libdir}/wine/%{winesodir}/*.a
%{_libdir}/wine/%{winesodir}/*.def


%files -n wine-pulseaudio
%{_libdir}/wine/%{winepedir}/winepulse.drv
%{_libdir}/wine/%{winesodir}/winepulse.so
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/winepulse.drv.so
%endif

%files -n wine-alsa
%{_libdir}/wine/%{winepedir}/winealsa.drv
%{_libdir}/wine/%{winesodir}/winealsa.drv.so

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%files -n wine-openal
%{_libdir}/wine/%{winepedir}/openal32.dll
%{_libdir}/wine/%{winesodir}/openal32.dll.so
%endif

%if 0%{?fedora}
%files -n wine-opencl
%{_libdir}/wine/%{winepedir}/opencl.dll
%ifarch %{arm} aarch64
%{_libdir}/wine/%{winesodir}/opencl.dll.so
%endif
%{_libdir}/wine/%{winesodir}/opencl.so
%endif

%changelog
* Sat Aug 28 2021 Patrick Laimbock <patrick@laimbock.com> - 6.15-0.1
- update to the latest wayland branch of 6.15
- wine-6.15-fix-for-BZ51596.patch

* Sun Aug 01 2021 Patrick Laimbock <patrick@laimbock.com> - 6.13-0.2
- enable staging

* Sun Aug 01 2021 Patrick Laimbock <patrick@laimbock.com> - 6.13-0.1
- update to the latest wayland branch of 6.13

* Sun Jun 20 2021 Patrick Laimbock <patrick@laimbock.com> - 6.9-0.3
- update to git rev 47bdc961a3effc4475fe845ebc6be20a6754605c

* Mon Jun 14 2021 Patrick Laimbock <patrick@laimbock.com> - 6.9-0.2
- move README-Fedora out of the way to prevent install conflict

* Sun Jun 13 2021 Patrick Laimbock <patrick@laimbock.com> - 6.9-0.1
- initial build of wine-wayland from
- https://gitlab.collabora.com/alf/wine/-/tree/wayland
- based on the wine.spec from koji (kudos to Michael)

