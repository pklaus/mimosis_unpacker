## mimosis\_unpacker

### Setting up the software

1. Make sure, python3 is installed
2. Set up Python venv (virtual environment)
3. Install the package (into new venv, along with dependencies)

For example:

    python3 -V
    python3 -m venv ~/.pyvenv/py34
    source ~/.pyvenv/py34/bin/activate
    pip install --upgrade https://github.com/pklaus/mimosis_unpacker/archive/master.zip
    # or if you have the repository downloaded or cloned to a local directory:
    pip install --upgrade .

If you need the JTAG / Windows COM functions to work (i.e. you're using the package on Windows)
please install pywin32 in addition:

    pip install pywin32

### Running the software

    source ~/.pyvenv/py34/bin/activate
    mimosis_unpacker --host 192.168.0.103 timed_stats --interval 0.5
    # or to get a time-integrated image of the matrix:
    mimosis_unpacker --host 192.168.0.103 matrix_image --filename test_0021.png

