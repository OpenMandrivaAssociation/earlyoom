Name: earlyoom
Version: 1.3
Release: 1
License: MIT
URL: https://github.com/rfjakob/earlyoom
Summary: Early OOM Daemon for Linux
Source0: https://github.com/rfjakob/earlyoom/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: systemd

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
%make_build

%install
%make_install PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SYSTEMDUNITDIR=%{_unitdir}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%config(noreplace) %{_sysconfdir}/default/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
