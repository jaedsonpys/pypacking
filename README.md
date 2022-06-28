# PyPacking

![BADGE](https://img.shields.io/badge/version-2.0.1-green)
![BADGE](https://img.shields.io/badge/license-MIT-red)
![BADGE](https://img.shields.io/badge/OS-Linux-yellow)

PyPacking is a **package manager** and installer for Python designed to be **interactive and user-friendly**. With easy operation, you can install *packages and tools*.

Track changes for *all versions* of PyPacking in the [CHANGELOG.md](https://github.com/jaedsonpys/pypacking/blob/master/CHANGELOG.md) file.

## How to install

surprisingly, we use PyPacking itself to perform its own installation. You just need to run the script from the `install` file and that's it, installed.

To install `PyPacking` on your machine (only **Linux** support), follow the steps below:

1. Clone the official PyPacking repository using `git` or by downloading in zip:

```
git clone git@github.com:jaedsonpys/pypacking.git
```

2. Go to the project **root** and run the available `install` file:

```
./install
```

> If you are using a virtual environment, PyPacking will be installed there.

## How to use

After installing PyPacking, here's a short tutorial on how to use the package manager:

### Configuration file

The *configuration files* are responsible for your entire project, it will contain information about the **package** being distributed. We use `.ini` file extension to store this information.

You can generate your configuration file with a simple command:

```
pypacking generate_config
```

After that, you must fill in some information about your project:

```
Author name:
Author email:
Project name: 
Description (default description): 
Version (1.0.0): 
Python package: 
Entry script (nothing to disable): 
```

By filling this, the `pypacking.ini` file will be created with all the **information** about your project

### Installing packages

You can **install packages with .zip files** on your own computer, as **PyPacking** does not yet have a server to store files. To do this, use the `install` command:

```
pypacking install [package name]
```

Your package will be installed in a location depending on your *environment*, if it is in a virtual environment it will be installed there.

### Uninstalling packages

To uninstalling packages installed by **PyPacking**, use the `uninstall` command:

```
pypacking uninstall [package name]
```

### Listing packages

You can list all packages installed by **PyPacking**, `list` command show the package name and version. See a example:

```
user@computer:~$ pypacking list
PyPacking::1.0.0
OtherPackage::5.3.4
...
```

### Creating packages

To create packages (after creating the configuration file), just run the `dist` command, which will create two directories:

1. The `build/` directory which stores a copy of your entire package;
2. The `dist/` directory that stores the already zipped package.

**PyPacking**, after creating your first project package, the next time you run the `dist` command, it will copy to the `build/` directory only the files that were changed, avoiding **unnecessary processing** to copy the whole package again.

Example of `dist` command:

```
pypacking dist
```

## License

```
MIT License © 2022 Jaedson Silva
```

This project uses the MIT license, follow the license instructions so you can enjoy this open-source project
