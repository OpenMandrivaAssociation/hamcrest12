%{?_javapackages_macros:%_javapackages_macros}
%global oname hamcrest

Name:           hamcrest12
Version:        1.2
Release:        7.0%{?dist}
Epoch:          0
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            http://code.google.com/p/hamcrest/

Source0:        http://hamcrest.googlecode.com/files/hamcrest-1.2.tgz
Source1:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-library/1.2/hamcrest-library-1.2.pom
Source2:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-generator/1.2/hamcrest-generator-1.2.pom
Source3:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.2/hamcrest-core-1.2.pom
Source4:        hamcrest-all-1.2.pom
Source5:        hamcrest-core-MANIFEST.MF
Patch0:         hamcrest-1.1-build.patch
Patch1:         hamcrest-1.1-no-jarjar.patch
Patch2:         hamcrest-1.1-no-integration.patch
Patch3:         hamcrest1.2-build.patch
Requires:       java >= 1:1.6.0
Requires:       easymock3
Requires:       qdox
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  zip
BuildRequires:  easymock3
BuildRequires:  junit
BuildRequires:  qdox

BuildArch:      noarch

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc

Summary:        API documentation for %{name}
BuildArch:      noarch
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{oname}-%{version}
find . -type f -name "*.jar" | xargs -t rm
ln -sf $(build-classpath qdox) lib/generator/
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1

perl -pi -e 's/\r$//g' LICENSE.txt

%build
export CLASSPATH=$(build-classpath qdox):build/hamcrest-core-%{version}.jar
export OPT_JAR_LIST="junit ant/ant-junit"
ant -Dversion=%{version} clean core
ant -Dversion=%{version} generator
ant -Dversion=%{version} library bigjar javadoc

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE5} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{oname}-core-%{version}.jar META-INF/MANIFEST.MF

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -m 644 build/%{oname}-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/all.jar
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-all.pom
%add_maven_depmap JPP.%{name}-all.pom %{name}/all.jar

install -m 644 build/%{oname}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/core.jar
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-core.pom
%add_maven_depmap JPP.%{name}-core.pom %{name}/core.jar

install -m 644 build/%{oname}-generator-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/generator.jar
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-generator.pom
%add_maven_depmap JPP.%{name}-generator.pom %{name}/generator.jar

install -m 644 build/%{oname}-library-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/library.jar
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-library.pom
%add_maven_depmap JPP.%{name}-library.pom %{name}/library.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc LICENSE.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/all.jar
%{_javadir}/%{name}/core.jar
%{_javadir}/%{name}/generator.jar
%{_javadir}/%{name}/library.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Jul 25 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-7
- Build against easymock3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-4
- Remove erroneous line breaks in manifest

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-3
- package review fixes

* Mon Feb 13 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-2
- disable integration, update POM files to 1.2

* Mon Feb 13 2012 Andy Grimm <agrimm@gmail.com> 0:1.2-1
- Initial 1.2 package, loosely based on Fedora hamcrest 1.1 package
