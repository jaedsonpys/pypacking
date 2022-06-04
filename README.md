# PyPacking

![BADGE](https://img.shields.io/badge/version-1.0.0-green)
![BADGE](https://img.shields.io/badge/license-MIT-red)
![BADGE](https://img.shields.io/badge/OS-Linux-yellow)

PyPacking is a **package manager** and installer for Python designed to be **interactive and user-friendly**. With easy operation, you can install *packages and tools*.

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

# How to use

After installing PyPacking, here's a short tutorial on how to use the package manager:

## Configuration file

The *configuration files* are responsible for your entire project, it will contain information about the **package** being distributed. We use `.ini` file extension to store this information.

You can generate your configuration file with a simple command:

```
pypacking generate_config
```

After that, you must fill in some information about your project:

```
Name: 
Description (default description): 
Version (1.0.0): 
Python package: 
Entry script (nothing to disable): 
```

By filling this, the `pypacking.ini` file will be created with all the **information** about your project

## License

```
MIT License © 2022 Jaedson Silva
```

This project uses the MIT license, follow the license instructions so you can enjoy this open-source project