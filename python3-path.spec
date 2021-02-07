#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test unit tests

Summary:	Python 2 module wrapper for os.path
Summary(pl.UTF-8):	Moduł Pythona 2 obudowujący os.path
Name:		python3-path
Version:	15.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/path/
Source0:	https://files.pythonhosted.org/packages/source/p/path/path-%{version}.tar.gz
# Source0-md5:	7fa391550400e7aa47849386d99598a7
URL:		https://github.com/jaraco/path
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-appdirs
BuildRequires:	python3-packaging
BuildRequires:	python3-pygments
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black >= 0.3.7
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-flake8
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-alabaster
BuildRequires:	python3-jaraco.packaging >= 8.2
BuildRequires:	python3-rst.linker >= 1.9
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
path implements a path objects as first-class entities, allowing
common operations on files to be invoked on those path objects
directly.

%description -l pl.UTF-8
path implementuje obiekty ścieżek jako instancje pierwszoklasowe,
pozwalające na wykonywanie ogólnych operacji na plikach bezpośrednio
na tych ścieżkach.

%package apidocs
Summary:	Documentation for Python path module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona path
Group:		Documentation

%description apidocs
Documentation for Python path module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu Pythona path.

%prep
%setup -q -n path-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_cov.plugin,pytest_flake8" \
%{__python3} -m pytest test_path.py
%endif

%if %{with doc}
# disable warnings (-W in SPHINXOPTS) to ignore objects.inv fetching error on builders
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3 \
	SPHINXOPTS=
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/path
%{py3_sitescriptdir}/path-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
