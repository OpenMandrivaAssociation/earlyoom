Summary:	Early OOM Daemon for Linux
Name:		earlyoom
Version:	1.8.2
Release:	1
License:	MIT
URL:		https://github.com/rfjakob/earlyoom
Source0:	https://github.com/rfjakob/earlyoom/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:	https://src.fedoraproject.org/rpms/earlyoom/raw/master/f/earlyoom-fedora-options.patch
BuildRequires:	systemd-rpm-macros

%description
The oom-killer generally has a bad reputation among Linux users.
This may be part of the reason Linux invokes it only when it has
absolutely no other choice. It will swap out the desktop
environment, drop the whole page cache and empty every buffer
before it will ultimately kill a process. At least that's what
I think what it will do. I have yet to be patient enough to wait
for it, sitting in front of an unresponsive system.

%prep
%autosetup -p1
sed -e '/systemctl/d' -i Makefile

%build
%set_build_flags
%make_build PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SYSTEMDUNITDIR=%{_unitdir}

%install
%make_install PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SYSTEMDUNITDIR=%{_unitdir}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
