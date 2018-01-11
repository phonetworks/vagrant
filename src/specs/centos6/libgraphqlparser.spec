Name:           libgraphqlparser
Version:        0.6.0
Release:        1%{?dist}
Summary:        parser for GraphQL

Group:          System Environment/Libraries
License:        BSD
URL:            https://github.com/graphql/libgraphqlparser
Source0:        https://github.com/graphql/libgraphqlparser/archive/libgraphqlparser-0.6.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:		dump_json_ast.cpp.patch

BuildRequires:  automake libtool cmake python-importlib
BuildRequires:  pkgconfig

%description
libgraphqlparser is a parser for GraphQL, a query language created by Facebook for describing data requirements on complex application data models, implemented in C++11. It can be used on its own in C++ code (or in C code via the pure C API defined in the c subdirectory), or you can use it as the basis for an extension module for your favorite programming language instead of writing your own parser from scratch.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%patch0 -p0

sed -i -e 's|/lib|/%{_lib}|' libgraphqlparser.pc.in
sed -i -e 's|LIBRARY DESTINATION lib|LIBRARY DESTINATION %{_lib}|' CMakeLists.txt
sed -i -e 's|/lib/pkgconfig|/%{_lib}/pkgconfig|' CMakeLists.txt
cmake -DCMAKE_INSTALL_PREFIX=/usr .


%build
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md README.md PATENTS LICENSE
%{_libdir}/libgraphqlparser.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/graphqlparser/GraphQLParser.h
%{_includedir}/graphqlparser/AstVisitor.h
%{_includedir}/graphqlparser/position.hh
%{_includedir}/graphqlparser/lexer.h
%{_includedir}/graphqlparser/stack.hh
%{_includedir}/graphqlparser/syntaxdefs.h
%{_includedir}/graphqlparser/parser.tab.hpp
%{_includedir}/graphqlparser/c/GraphQLAst.h
%{_includedir}/graphqlparser/c/GraphQLParser.h
%{_includedir}/graphqlparser/c/GraphQLAstForEachConcreteType.h
%{_includedir}/graphqlparser/c/GraphQLAstVisitor.h
%{_includedir}/graphqlparser/c/GraphQLAstNode.h
%{_includedir}/graphqlparser/c/GraphQLAstToJSON.h
%{_includedir}/graphqlparser/AstNode.h
%{_includedir}/graphqlparser/Ast.h
%{_includedir}/graphqlparser/JsonVisitor.h
%{_includedir}/graphqlparser/location.hh
%{_libdir}/pkgconfig/libgraphqlparser.pc


%changelog
* Thu Jun 22 2017 Emre Sokullu <emre@phonetworks.org>
- Initial version for CentOS 6
