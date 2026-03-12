#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test unit tests

Summary:	Python module wrapper for os.path
Summary(pl.UTF-8):	Moduł Pythona obudowujący os.path
Name:		python3-path
Version:	17.1.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/path/
Source0:	https://files.pythonhosted.org/packages/source/p/path/path-%{version}.tar.gz
# Source0-md5:	c7ab103cb96b36758daeccd1ed52b587
URL:		https://github.com/jaraco/path
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-build
BuildRequires:	python3-coherent.licensed
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-appdirs
BuildRequires:	python3-more_itertools
BuildRequires:	python3-packaging
BuildRequires:	python3-pygments
BuildRequires:	python3-pytest >= 6
# lint only?
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-enabler >= 2.2
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-pytest-ruff >= 0.2.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 3.5
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
%endif
Requires:	python3-modules >= 1:3.9
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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest path tests
%endif

%if %{with doc}
# disable warnings (-W in SPHINXOPTS) to ignore objects.inv fetching error on builders
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3 \
	SPHINXOPTS=
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst SECURITY.md
%{py3_sitescriptdir}/path
%{py3_sitescriptdir}/path-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
