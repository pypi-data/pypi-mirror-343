#!/usr/bin/python3
# -*- coding: utf-8 -*-


import shutil
from pathlib import Path
from typing import Optional

from slpkg.configs import Configs
from slpkg.repositories import Repositories
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox, DrawPackage


class View(Configs):  # pylint: disable=[R0902]
    """Views packages for build, install, remove or download."""

    def __init__(self, flags: Optional[list[str]] = None, repository: Optional[str] = None, data: Optional[dict[str, dict[str, str]]] = None) -> None:
        super().__init__()

        if flags is None:
            flags = []

        if repository is None:
            repository = 'None'

        if data is None:
            data = {}

        self.flags = flags
        self.repository = repository
        self.data = data

        self.repos = Repositories()
        self.utils = Utilities()
        self.ascii = AsciiBox()
        self.upgrade = Upgrade(repository, data)

        self.sum_install = 0
        self.sum_upgrade = 0
        self.sum_remove = 0
        self.sum_size_comp: float = 0
        self.sum_size_uncomp: float = 0
        self.sum_size_remove = 0
        self.columns, self.rows = shutil.get_terminal_size()

        self.download_only: Path = Path()
        self.summary_message: str = ''
        self.mode: str = 'build'

        self.option_for_reinstall: bool = self.utils.is_option(
            ('-r', '--reinstall'), flags)

        self.option_for_yes: bool = self.utils.is_option(
            ('-y', '--yes'), flags)

    def build_packages(self, slackbuilds: list[str], dependencies: list[str]) -> None:
        """View packages for build method.

        Args:
            slackbuilds (list[str]): Slackbuilds for build.
            dependencies (list[str]): Dependencies for build.
        """
        self.ascii.draw_package_title('The following packages will be build:',
                                      'slpkg build packages')

        for slackbuild in slackbuilds:
            self.draw_build_package(slackbuild)
            self.summary(slackbuild)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_build_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_build(slackbuilds + dependencies)
        print(self.summary_message)

    def install_upgrade_packages(self, packages: list[str], dependencies: list[str], mode: str) -> None:
        """View packages for install or upgrade.

        Args:
            packages (list[str]): Packages for install.
            dependencies (list[str]): Dependencies for install.
            mode (str): Type of mode.
        """
        self.mode = mode
        title: str = 'slpkg install packages'
        if mode == 'upgrade':
            title = 'slpkg upgrade packages'
        self.ascii.draw_package_title('The following packages will be installed or upgraded:', title)

        for package in packages:
            self.draw_install_upgrade_package(package)
            self.summary(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_install_upgrade_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_install_and_upgrade(self.sum_install, self.sum_upgrade,
                                                 self.sum_size_comp, self.sum_size_uncomp)
        print(self.summary_message)

    def download_packages(self, packages: list[str], directory: Path) -> None:
        """View packages for download method.

        Args:
            packages (list[str]): Packages name for download.
            directory (Path): Path to download.
        """
        self.mode = 'download'
        self.download_only = directory
        self.ascii.draw_package_title('The following packages will be downloaded:',
                                      'slpkg download packages')

        for package in packages:
            self.draw_download_package(package)
            self.summary(package)

        self.ascii.draw_bottom_line()
        self.set_summary_for_download(packages, self.sum_size_comp)
        print(self.summary_message)

    def remove_packages(self, packages: list[str], dependencies: list[str]) -> None:
        """View packages for remove.

        Args:
            packages (list[str]): List of packages.
            dependencies (list[str]): List of dependencies.
        """
        self.mode = 'remove'
        self.ascii.draw_package_title('The following packages will be removed:',
                                      'slpkg remove packages')
        for package in packages:
            self.draw_remove_package(package)
            self.summary(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.draw_remove_package(dependency)
                self.summary(dependency)

        self.ascii.draw_bottom_line()
        self.set_summary_for_remove(self.sum_remove, self.sum_size_remove)
        print(self.summary_message)

    def draw_build_package(self, package: str) -> None:
        """Draw line for build package method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.yellow
        version: str = self.data[package]['version']

        package_info = DrawPackage(
            package,
            version,
            size,
            color,
            self.repository
        )

        # self.ascii.draw_package_line(package, version, size, color, self.repository)
        self.ascii.draw_package_line(package_info)

    def draw_install_upgrade_package(self, package: str) -> None:
        """Draw line for install or upgrade package method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']
        installed: str = self.utils.is_package_installed(package)
        upgradable: bool = self.upgrade.is_package_upgradeable(installed)

        if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
            size_comp: float = float(self.data[package]['size_comp']) * 1024
            size = self.utils.convert_file_sizes(size_comp)

        if installed:
            color = self.grey

        if upgradable:
            color = self.violet
            package = self.build_package_and_version(package)

        if installed and self.option_for_reinstall and not upgradable:
            color = self.violet
            package = self.build_package_and_version(package)

        package_info = DrawPackage(
            package,
            version,
            size,
            color,
            self.repository
        )

        self.ascii.draw_package_line(package_info)

    def draw_download_package(self, package: str) -> None:
        """Draw package for download method.

        Args:
            package (str): Package name.
        """
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']

        if self.repository not in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
            size_comp: float = float(self.data[package]['size_comp']) * 1024
            size = self.utils.convert_file_sizes(size_comp)

        package_info = DrawPackage(
            package,
            version,
            size,
            color,
            self.repository
        )

        self.ascii.draw_package_line(package_info)

    def draw_remove_package(self, package: str) -> None:
        """Draw package for remove method.

        Args:
            package (str): Package name.
        """
        count_size: int = self.utils.count_file_size(package)
        installed: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed)['version']
        repo_tag: str = self.utils.split_package(installed)['tag']
        size: str = self.utils.convert_file_sizes(count_size)
        self.repository = repo_tag.lower().replace('_', '')

        package_info = DrawPackage(
            package,
            version,
            size,
            self.red,
            self.repository
        )

        self.ascii.draw_package_line(package_info)

    def summary(self, package: str) -> None:
        """Count packages per method.

        Args:
            package (str): Package name.
        """
        installed: str = self.utils.is_package_installed(package)

        if self.repository not in list(self.repos.repositories)[:2] and self.data:
            self.sum_size_comp += float(self.data[package]['size_comp']) * 1024
            self.sum_size_uncomp += float(self.data[package]['size_uncomp']) * 1024

        if installed and self.mode == 'remove':
            self.sum_size_remove += self.utils.count_file_size(package)

        upgradeable: bool = False
        if self.mode != 'remove':
            upgradeable = self.upgrade.is_package_upgradeable(installed)

        if not installed:
            self.sum_install += 1
        elif installed and self.option_for_reinstall:
            self.sum_upgrade += 1
        elif upgradeable:
            self.sum_upgrade += 1
        elif installed and self.mode == 'remove':
            self.sum_remove += 1

    def set_summary_for_build(self, packages: list[str]) -> None:
        """Set summary message for build.

        Args:
            packages (list): List of packages.
        """
        self.summary_message = (
            f'{self.grey}Total {len(packages)} packages '
            f'will be build in {self.tmp_path} folder.{self.endc}')

    def set_summary_for_install_and_upgrade(self, install: int, upgrade: int, size_comp: float, size_uncomp: float) -> None:
        """Set summary for install or upgrade.

        Args:
            install (int): Counts for installs.
            upgrade (int): Counts for upgrades.
            size_comp (float): Counts of compressed sizes.
            size_uncomp (float): Counts of uncompressed sizes.
        """
        upgrade_message: str = ''
        split_message: str = '\n'
        if self.columns > 80:
            split_message = ''
        total_packages: str = (f'{self.grey}Total {install} packages will be installed and {upgrade} '
                               f'will be upgraded, while a total ')
        total_sizes: str = (f'{self.utils.convert_file_sizes(size_comp)} will be downloaded and '
                            f'{self.utils.convert_file_sizes(size_uncomp)} will be installed.{self.endc}')
        if self.mode == 'upgrade' and not self.package_method:
            if self.upgrade_log_file.is_file():
                upgrade_message = (f'\n{self.red}Some versions failed, '
                                   f'check the /var/log/slpkg/upgrade.log file.{self.endc}')
            else:
                upgrade_message = (f'\n{self.grey}Note: Packages with custom versions may not '
                                   f'compare correctly.{self.endc}')
        self.summary_message = f'{total_packages}{split_message}{total_sizes}{upgrade_message}'

    def set_summary_for_remove(self, remove: int, size_rmv: int) -> None:
        """Set summary for removes.

        Args:
            remove (int): Counts of removes.
            size_rmv (int): Size of removes.
        """
        self.summary_message = (
            f'{self.grey}Total {remove} packages '
            f'will be removed and {self.utils.convert_file_sizes(size_rmv)} '
            f'of space will be freed up.{self.endc}')

    def set_summary_for_download(self, packages: list[str], size_comp: float) -> None:
        """Set summary for downloads.

        Args:
            packages (list[str]): List of packages.
            size_comp (float): Size of downloads.
        """
        self.summary_message = (
            f'{self.grey}Total {len(packages)} packages and {self.utils.convert_file_sizes(size_comp)} '
            f'will be downloaded in {self.download_only} folder.{self.endc}')

    def build_package_and_version(self, package: str) -> str:
        """Build package and version.

        Args:
            package (str): Package name.

        Returns:
            str: Package with the version.
        """
        installed_package: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed_package)['version']
        return f'{package}-{version}'

    def skipping_packages(self, packages: list[str]) -> None:
        """View skipped packages.

        Args:
            packages (list[str]): List of packages.
        """
        if packages:
            print('Packages skipped by the user:\n')
            for name in packages:
                failed: str = f'{self.red}{self.ascii.skipped}{self.endc}'
                print(f"\r{'':>2}{self.bred}{self.ascii.bullet}{self.endc} "
                      f"{self.data[name]['package']} {failed}{' ' * 17}")
            print()

    def missing_dependencies(self, packages: list[str]) -> None:
        """View for missing dependencies.

        Args:
            packages (list[str]): Name of packages.
        """
        if self.view_missing_deps:
            missing_deps: dict = {}
            for package in packages:
                requires_data: list[str] = list(self.data[package]['requires'])
                requires: list[str] = requires_data if isinstance(requires_data, list) else requires_data

                for req in requires:
                    if req not in self.data:
                        missing_deps[package] = [req for req in requires if req not in self.data]
            if missing_deps:
                print('\nPackages with missing dependencies:')
                for pkg, deps in missing_deps.items():
                    if deps and deps != ['']:
                        print(f"> {self.cyan}{pkg}{self.endc}: Requires "
                              f"({len(deps)}) -> {self.red}{', '.join(deps)}{self.endc}")

    def question(self, message: str = 'Do you want to continue?') -> None:
        """View a question.

        Args:
            message (str, optional): Message of question.

        Raises:
            SystemExit: Raise an exit code 0.
        """
        if not self.option_for_yes and self.ask_question:
            answer: str = input(f'\n{message} [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit(0)
        print()
