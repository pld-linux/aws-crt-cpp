#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	tests		# unit tests (require network)
#
# from submodules in https://github.com/awslabs/aws-crt-cpp/crt
%define	aws_c_auth_ver		0.10.4
%define	aws_c_cal_ver		0.9.15
%define	aws_c_common_ver	0.14.4
%define	aws_c_compression_ver	0.3.2
%define	aws_c_event_stream_ver	0.7.1
%define	aws_c_http_ver		0.11.0
%define	aws_c_io_ver		0.27.6
%define	aws_c_mqtt_ver		0.16.1
%define	aws_c_s3_ver		0.13.5
%define	aws_c_sdkutila_ver	0.2.9
%define	aws_checksums_ver	0.2.10
%define	aws_lc_ver		5.5.0
%define	s2n_ver			1.7.7

Summary:	AWS Crt Cpp library
Summary(pl.UTF-8):	Biblioteka AWS Crt Cpp
Name:		aws-crt-cpp
Version:	0.43.8
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-crt-cpp/releases
Source0:	https://github.com/awslabs/aws-crt-cpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fad43eded7e68c6619ee8f9e492bab20
URL:		https://github.com/awslabs/aws-crt-cpp
BuildRequires:	aws-c-auth-devel >= %{aws_c_auth_ver}
BuildRequires:	aws-c-cal-devel >= %{aws_c_cal_ver}
BuildRequires:	aws-c-common-devel >= %{aws_c_common_ver}
BuildRequires:	aws-c-event-stream-devel >= %{aws_c_event_stream_ver}
BuildRequires:	aws-c-http-devel >= %{aws_c_http_ver}
BuildRequires:	aws-c-io-devel >= %{aws_c_io_ver}
BuildRequires:	aws-c-mqtt-devel >= %{aws_c_mqtt_ver}
BuildRequires:	aws-c-s3-devel >= %{aws_c_s3_ver}
BuildRequires:	aws-checksums-devel >= %{aws_checksums_ver}
BuildRequires:	cmake >= 3.9
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	aws-c-auth >= %{aws_c_auth_ver}
Requires:	aws-c-cal >= %{aws_c_cal_ver}
Requires:	aws-c-common >= %{aws_c_common_ver}
Requires:	aws-c-event-stream >= %{aws_c_event_stream_ver}
Requires:	aws-c-http >= %{aws_c_http_ver}
Requires:	aws-c-io >= %{aws_c_io_ver}
Requires:	aws-c-mqtt >= %{aws_c_mqtt_ver}
Requires:	aws-c-s3 >= %{aws_c_s3_ver}
Requires:	aws-checksums >= %{aws_checksums_ver}
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
Requires:	aws-c-auth-devel >= %{aws_c_auth_ver}
Requires:	aws-c-cal-devel >= %{aws_c_cal_ver}
Requires:	aws-c-common-devel >= %{aws_c_common_ver}
Requires:	aws-c-event-stream-devel >= %{aws_c_event_stream_ver}
Requires:	aws-c-http-devel >= %{aws_c_http_ver}
Requires:	aws-c-io-devel >= %{aws_c_io_ver}
Requires:	aws-c-mqtt-devel >= %{aws_c_mqtt_ver}
Requires:	aws-c-s3-devel >= %{aws_c_s3_ver}
Requires:	aws-checksums-devel >= %{aws_checksums_ver}
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
%{_libdir}/libaws-crt-cpp.so

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
