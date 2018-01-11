%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name graphql
%global source_suffix parser-php

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


Summary:      PHP bindings for libgraphqlparser
Name:         php-pecl-graphql
Version:      0.6.0
Release:      1%{?dist}
License:      ASL 2.0
Group:        Development/Languages
URL:          https://github.com/dosten/graphql-parser-php

Source:       https://github.com/dosten/graphql-parser-php/archive/%{pecl_name}-%{source_suffix}-%{version}.tar.gz
Patch0:       graphql.c.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: php70w-devel >= 7.0
#BuildRequires: php-pear >= 1.4.9-1.2
BuildRequires: libgraphqlparser libgraphqlparser-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if 0%{?php_zend_api:1}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif

Requires:     libgraphqlparser

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}


%description
A PHP extension wrapping the libgraphqlparser library for parsing GraphQL.

%prep 
%setup -c -q

cd %{pecl_name}-%{source_suffix}-%{version}

%patch0 -p0

%build
cd %{pecl_name}-%{source_suffix}-%{version}
phpize
%configure 
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{source_suffix}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/z_%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%clean
%{__rm} -rf %{buildroot}

%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{source_suffix}-%{version}/README.md %{pecl_name}-%{source_suffix}-%{version}/LICENSE
%config(noreplace) %{_sysconfdir}/php.d/z_%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%changelog
* Thu Jun 22 2017 Emre Sokullu <emre@phonetworks.org>
- Initial version for CentOS 7
