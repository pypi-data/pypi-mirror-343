from setuptools import setup

tmp_basic = []
tmp_server = []
tmp_data = []
tmp_interface = []
tmp_extra = []

status = "basic"
with open("requirements.txt") as f:
    tmp = f.read().strip().split("\n")
    for pos in tmp:
        if "#" in pos:
            status = pos.split("#")[1].strip()
        if pos:
            if status == "basic":
                tmp_basic.append(pos)
            elif status == "server":
                tmp_server.append(pos)
            elif status == "data":
                tmp_data.append(pos)
            elif status == "interface":
                tmp_interface.append(pos)
            elif status == "extra":
                tmp_extra.append(pos)

install_requires = [pos for pos in tmp_basic if pos]

extras_require = {
    "server": [pos for pos in tmp_server if pos],
    "data": [pos for pos in tmp_data if pos],
    "interface": [pos for pos in tmp_interface if pos],
    "extra": [pos for pos in tmp_extra if pos],
}

extras_require["all"] = (
    extras_require["server"] + extras_require["data"] + extras_require["interface"]
)

setup(
    name="pytigon-batteries",
    version="0.250423",
    description="Pytigon library",
    author="Sławomir Chołaj",
    author_email="slawomir.cholaj@gmail.com",
    license="LGPLv3",
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3",
)
