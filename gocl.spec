%global api_version 0.1

Name:           gocl
Version:        0.1.4
Release:        2%{?dist}
Summary:        GLib/GObject based library for OpenCL

License:        LGPLv3
URL:            https://github.com/elima/gocl/
Source0:        https://github.com/elima/gocl/archive/%{version}.tar.gz#%{name}-%{version}.tar.gz

# Tracked upstream in https://github.com/elima/gocl/pull/1
Patch0:         gocl-build.patch

BuildRequires:  automake
BuildRequires:  glibc-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  ocl-icd-devel opencl-headers


%description
Gocl is a GLib/GObject based library that aims at simplifying the
use of OpenCL in GNOME software. It is intended to be a lightweight
wrapper that adapts OpenCL programming patterns and boilerplate, and
expose a simpler API that is known and comfortable to GNOME
developers. Examples of such adaptations are the integration with
GLib’s main loop, exposing non-blocking APIs, GError based error
reporting and full gobject-introspection support. It will also be
including convenient API to simplify code for the most common use
patterns. 


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .build


%build
./autogen.sh
%configure --disable-static --enable-introspection=yes --enable-tests=yes --enable-gtk-doc
make %{?_smp_mflags}


%install
%make_install

# NOTE: We intentionally don't ship *.la files
find %{buildroot} -type f -name '*.la' | xargs rm -f -- || :


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc COPYING examples/js/helloWorld.js
%{_libdir}/libgocl-%{api_version}.so.*
%{_libdir}/girepository-1.0/


%files devel
%doc examples/hello-world.c examples/hello-world.cl examples/hello-world-sync.c examples/gaussian-blur.c examples/gaussian-blur.cl
%{_libdir}/libgocl-%{api_version}.so
%{_libdir}/pkgconfig/%{name}-%{api_version}.pc
%{_datadir}/gir-1.0/
%{_datadir}/gtk-doc/
%{_includedir}/gocl-%{api_version}/


%changelog
* Wed Sep 11 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.1.4-2
- Own directories
- Package examples
- Use global instead of define

* Sun Aug 18 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.1.4-1
- Initial package
