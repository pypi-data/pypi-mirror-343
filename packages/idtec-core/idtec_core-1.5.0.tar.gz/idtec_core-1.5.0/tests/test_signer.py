
from idtec_core import signer
import os

def test_sign_file():
    sample_file = "sample.txt"
    key_file = "ideal-lattice_private.pem"

    with open(sample_file, "w") as f:
        f.write("This is a test document.")

    signer.sign_file(sample_file, key_file)

    assert os.path.exists(sample_file + ".idtec-signature")
