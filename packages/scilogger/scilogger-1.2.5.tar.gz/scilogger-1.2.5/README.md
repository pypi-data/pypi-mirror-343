# SciLogger - Logging for Scientific Applications 

> * **Repository: [github.com/otvam/scilogger](https://github.com/otvam/scilogger)**
> * **PyPi: [pypi.org/project/scilogger](https://pypi.org/project/scilogger)**
> * **Conda: [anaconda.org/conda-forge/scilogger](https://anaconda.org/conda-forge/scilogger)**

## Summary

**SciLogger** is a **Python Logging** module:
* Specially targeted for **scientific applications**.
* Use a **global timer** to measure the **elapsed time**.
* Provide a class for **timing code blocks**.
* Definition of **custom indentation levels**.
* Definition of **colors** for the logging levels.

**SciLogger** is using a global **INI configuration** file:
* First, the **default configuration** is loaded (`scilogger/scilogger.ini`).
* Afterward, a **custom file** can be loaded with an environment variable (`SCILOGGER`)

SciLogger is written in Python without any external dependencies.
SciLogger is respecting **semantic versioning** (starting from version 1.2).

## Warning

* This logging module is **based** on the **Python logging module**.
* The philosophy of this logging module is slightly different. 
* Mixing both modules can create strange/incorrect behaviors.

## Example

An example is located in the `example` folder of the repository:
* `run_logger.py` contains an example file for the logger
* `configlogger.ini` contains a custom configuration file

```bash
# Set the configuration file.
export SCILOGGER="configlocal.ini"

# Run the Python script.
python run_logger.py
```

```text
00:00:00.00 : main     : debug    : debug level log
00:00:00.10 : main     : info     : info level log
00:00:00.20 : main     : error    : error level log
00:00:00.20 : main     : info     : example for the timed blocks : enter : 00:00:00.00
00:00:00.20 : main     : info     :     info level log
00:00:00.30 : main     : info     :     info level log
00:00:00.30 : main     : info     : example for the timed blocks : exit : 00:00:00.10
00:00:00.30 : main     : info     : example for the indented blocks : enter
00:00:00.30 : main     : info     :     info level log
00:00:00.40 : main     : info     :     info level log
00:00:00.40 : main     : info     : example for the indented blocks : exit
00:00:00.40 : main     : error    : exception : builtins / ValueError
00:00:00.40 : main     : error    :     Traceback (most recent call last):
00:00:00.40 : main     : error    :       File "run_logger.py", line 44, in <module>
00:00:00.40 : main     : error    :         raise ValueError("example for the exceptions")
00:00:00.40 : main     : error    :     ValueError: example for the exceptions
00:00:00.41 : mod_a    : info     : module_a
00:00:00.41 : mod_a    : debug    :     debug level log
00:00:00.41 : mod_a    : info     :     info level log
00:00:00.41 : mod_a    : error    :     error level log
00:00:00.41 : mod_b    : info     : module_b
00:00:00.41 : mod_b    : debug    :     debug level log
00:00:00.41 : mod_b    : info     :     info level log
00:00:00.41 : mod_b    : error    :     error level log
00:00:00.41 : main     : info     : timing data
00:00:00.41 : main     : info     :     date = 2025-01-10T18:00:10Z
00:00:00.41 : main     : info     :     duration = 00:00:00.41
00:00:00.41 : main     : info     :     seconds = 0.409
```

## Project Links

* Repository: https://github.com/otvam/scilogger
* Releases: https://github.com/otvam/scilogger/releases
* Tags: https://github.com/otvam/scilogger/tags
* Issues: https://github.com/otvam/scilogger/issues
* PyPi: https://pypi.org/project/scilogger
* Conda: https://anaconda.org/conda-forge/scilogger

## Author

* **Thomas Guillod**
* Email: guillod@otvam.ch
* Website: https://otvam.ch

## Copyright

> (c) 2023 - Thomas Guillod
> 
>  BSD 2-Clause "Simplified" License
