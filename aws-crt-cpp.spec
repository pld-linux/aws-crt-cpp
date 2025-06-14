#
# Conditional build:
%bcond_without	apidocs		# unit tests (require network)
%bcond_with	tests		# unit tests (require network)
#
Summary:	AWS Crt Cpp library
Summary(pl.UTF-8):	Biblioteka AWS Crt Cpp
Name:		aws-crt-cpp
Version:	0.32.8
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-crt-cpp/releases
Source0:	https://github.com/awslabs/aws-crt-cpp/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f191f7e574c8e364a54c733473010e29
URL:		https://github.com/awslabs/aws-crt-cpp
BuildRequires:	aws-c-auth-devel
BuildRequires:	aws-c-cal-devel
BuildRequires:	aws-c-common-devel
BuildRequires:	aws-c-event-stream-devel
BuildRequires:	aws-c-http-devel
BuildRequires:	aws-c-io-devel
BuildRequires:	aws-c-mqtt-devel
BuildRequires:	aws-c-s3-devel
BuildRequires:	aws-checksums-devel
BuildRequires:	cmake >= 3.9
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ wrapper around the aws-c-* libraries. Provides Cross-Platform
Transport Protocols and SSL/TLS implementations for C++.

%description -l pl.UTF-8
Interfejs C++ do bibliotek aws-c-*. Zapewnia wieloplatformowe
implementacje protokołów tranportu oraz SSL/TLS dla C++.

%package devel
Summary:	Header files for AWS Crt Cpp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AWS Crt Cpp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	aws-c-auth-devel
Requires:	aws-c-cal-devel
Requires:	aws-c-event-stream-devel
Requires:	aws-c-http-devel
Requires:	aws-c-mqtt-devel
Requires:	aws-c-s3-devel
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for AWS Crt Cpp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AWS Crt Cpp.

%package apidocs
Summary:	API documentation for AWS Crt Cpp library
Summary(pl.UTF-8):	Dokumentacja API biblioteki AWS Crt Cpp
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for AWS Crt Cpp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki AWS Crt Cpp.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DBUILD_DEPS=OFF \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DUSE_OPENSSL=ON

%{__make}

cd ..

%if %{with tests}
%{__make} test
%endif

%if %{with apidocs}
doxygen docsrc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tests}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{elasticurl_cpp,mqtt5_app,mqtt5_canary}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_libdir}/libaws-crt-cpp.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/aws/crt
%{_includedir}/aws/iot
%{_libdir}/cmake/aws-crt-cpp

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*
%endif
