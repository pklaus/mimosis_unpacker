
To set up this software:

1. Make sure, python3 is installed
2. Set up Python venv (virtual environment)
3. Install additional packages (into venv)

For example:

    python3 -m venv /local/pklaus/pyvenv/py34
    source /local/pklaus/pyvenv/py34/bin/activate
    pip install -r requirements.txt

To run this software:

    source /local/pklaus/pyvenv/py34/bin/activate
    ./mimosis_unpacker_cli.py --host 192.168.0.103 --buffer-size 4096

