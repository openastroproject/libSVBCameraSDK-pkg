%define debug_package %{nil}

Name:           libsvbcamerasdk
Version:        1.6.2.11
Release:        0
Summary:        SVBony camera SDK
License:        expat
URL:            http://astronomy-imaging-camera.com/
Prefix:         %{_prefix}
Provides:       libsvbcamerasdk = %{version}-%{release}
Obsoletes:      libsvbcamerasdk < 1.6.2.11
Requires:       libusbx
Source:         libsvbcamerasdk-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libSVBCameraSDK is a user-space driver for SVBony astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libsvbcamerasdk-devel = %{version}-%{release}
Obsoletes:      libsvbcamerasdk-devel < 1.6.2.11

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libsvbcamerasdk2.pc.in > libsvbcamerasdk2.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/demo
mkdir -p %{buildroot}/etc/udev/rules.d

case %{_arch} in
  i386)
    cp lib/x86/libSVBCameraSDK*.so.%{version} %{buildroot}%{_libdir}
    ;;
  x86_64)
    cp lib/x64/libSVBCameraSDK*.so.%{version} %{buildroot}%{_libdir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp include/*.h %{buildroot}%{_includedir}
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp demo/Makefile %{buildroot}%{_docdir}/%{name}-%{version}/demo
cp demo/*.* %{buildroot}%{_docdir}/%{name}-%{version}/demo
cp 70-svb-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/SVBCameraSDK.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_docdir}/%{name}-%{version}/demo/Makefile
%{_docdir}/%{name}-%{version}/demo/*.*

%changelog
* Fri Aug 20 2021 James Fidell <james@openastroproject.org> - 1.6.2.11
- Initial RPM release

