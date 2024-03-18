%define libname %mklibname wireplumber
%define devname %mklibname -d wireplumber
#define api %(echo %{version} |cut -d. -f1-2)
%define api 0.5

Name:       wireplumber
Version:    0.5.0
Release:    1
Summary:    A modular session/policy manager for PipeWire

License:    MIT
URL:        https://pipewire.pages.freedesktop.org/wireplumber/
Source0:    https://gitlab.freedesktop.org/pipewire/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  meson gcc pkgconfig gettext
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libspa-0.2) >= 0.2
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.26
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(lua)
BuildRequires:  gobject-introspection-devel
BuildRequires:  python-lxml doxygen
BuildRequires:  systemd-rpm-macros
%{?systemd_ordering}

# Make sure that we have -libs package in the same version
Requires:       %{libname} = %{EVRD}
Recommends:     %{libname}-gobject%{?_isa} = %{EVRD}

Provides:       pipewire-session-manager
Conflicts:      pipewire-session-manager

%package -n %{libname}
Summary:        Libraries for WirePlumber clients
Recommends:     %{name}%{?_isa} = %{EVRD}

%description -n %{libname}
This package contains the runtime libraries for any application that wishes
to interface with WirePlumber.

%package -n %{libname}-gobject
Summary:        GObject TypeLibraries for WirePlumber clients
Requires:	%{libname} = %{EVRD}

%description -n %{libname}-gobject
This package contains the runtime libraries for any application that wishes
to interface with WirePlumber using GObject.

%package -n %{devname}
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{EVRD}
Requires:       %{libname}%{?_isa} = %{EVRD}
Recommends:     %{devname}-gobject{?_isa} = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n %{devname}-gobject
Summary:        Development files for %{name}
Requires:       %{devname}%{?_isa} = %{EVRD}
Requires:       %{libname}-gobject%{?_isa} = %{EVRD}

%description -n %{devname}-gobject
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} with GObject

%description
WirePlumber is a modular session/policy manager for PipeWire and a
GObject-based high-level library that wraps PipeWire's API, providing
convenience for writing the daemon's modules as well as external tools for
managing PipeWire.

%prep
%autosetup -p1
%meson -Dsystem-lua=true \
       -Ddoc=disabled \
       -Dsystemd=enabled \
       -Dsystemd-user-service=true \
       -Dintrospection=enabled \
       -Delogind=disabled

%build
%meson_build

%install
%meson_install

# Create local config skeleton
mkdir -p %{buildroot}%{_sysconfdir}/wireplumber/{bluetooth.lua.d,common,main.lua.d,policy.lua.d}

%find_lang wireplumber

%posttrans
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files -f wireplumber.lang
%doc %{_datadir}/doc/wireplumber/examples/
%license LICENSE
%{_bindir}/wireplumber
%{_bindir}/wpctl
%{_bindir}/wpexec
%dir %{_sysconfdir}/wireplumber
%dir %{_sysconfdir}/wireplumber/bluetooth.lua.d
%dir %{_sysconfdir}/wireplumber/common
%dir %{_sysconfdir}/wireplumber/main.lua.d
%dir %{_sysconfdir}/wireplumber/policy.lua.d
%{_datadir}/wireplumber/
%{_datadir}/zsh/site-functions/_wpctl
#{_datadir}/pipewire/wireplumber.conf
#{_datadir}/pipewire/wireplumber.conf.d/alsa-vm.conf
%{_userunitdir}/wireplumber.service
%{_userunitdir}/wireplumber@.service

%files -n %{libname}
%license LICENSE
%dir %{_libdir}/wireplumber-%{api}/
%{_libdir}/wireplumber-%{api}/libwireplumber-*.so
%{_libdir}/libwireplumber-%{api}.so.*

%files -n %{libname}-gobject
%{_libdir}/girepository-1.0/Wp-%{api}.typelib

%files -n %{devname}
%{_includedir}/wireplumber-%{api}/
%{_libdir}/libwireplumber-%{api}.so
%{_libdir}/pkgconfig/wireplumber-%{api}.pc

%files -n %{devname}-gobject
%{_datadir}/gir-1.0/Wp-%{api}.gir
