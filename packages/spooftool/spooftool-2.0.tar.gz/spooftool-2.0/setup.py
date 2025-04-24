from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

class PostInstallCommand(install):
    def run(self):

        lib_path = Path(self.install_lib) / "spooftool" / "lib"
        lib_path.mkdir(parents=True, exist_ok=True)
        
        useragents_path = lib_path / "useragents.txt"
        if not useragents_path.exists():
            default_useragents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
            ]
            with open(useragents_path, 'w') as f:
                f.write("\n".join(default_useragents))
        
        install.run(self)

setup(
    name="spooftool",
    version="2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "spoof=spoof:main",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    package_data={
        'spooftool': ['lib/useragents.txt'],
    },
    include_package_data=True,
    author="@xinerox",
    description="email spoofing tool using spoofmail api",
)