## mimosis\_unpacker

### Setting up the software

1. Make sure python3 is installed.
2. Set up Python virtual environment (venv), especially if on Linux as user w/ limited permissions.
3. Install the package (along with dependencies).

For example:

    python3 -V
    python3 -m venv ~/.pyvenv/py34 # <- Linux only
    source ~/.pyvenv/py34/bin/activate # <- Linux only
    pip install --upgrade https://github.com/pklaus/mimosis_unpacker/archive/master.zip
    # or if you have the repository downloaded or cloned to a local directory:
    pip install --upgrade .

The JTAG control part of the software works on Windows only as it relies on
inter-process communication (COM) with the respective GUI tool.

### Running the software

    source ~/.pyvenv/py34/bin/activate # <- Linux only
    mimosis_unpacker --host 192.168.0.103 timed_stats --interval 0.5
    # or to get a time-integrated image of the matrix:
    mimosis_unpacker --host 192.168.0.103 matrix_image --filename test_0021.png
