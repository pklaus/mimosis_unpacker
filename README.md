## mimosis\_unpacker

### Setting up the software

1. Make sure, python3 is installed
2. Set up Python venv (virtual environment)
3. Install additional packages (into venv)

For example:

    python3 -V
    python3 -m venv ~/.pyvenv/py34
    source ~/.pyvenv/py34/bin/activate
    pip install -r requirements.txt

### Running the software

    source ~/.pyvenv/py34/bin/activate
    ./mimosis_unpacker_cli.py --host 192.168.0.103 timed_stats --interval 0.5
    # or to get a time-integrated image of the matrix:
    ./mimosis_unpacker_cli.py --host 192.168.0.103 matrix_image --filename test_0021.png

