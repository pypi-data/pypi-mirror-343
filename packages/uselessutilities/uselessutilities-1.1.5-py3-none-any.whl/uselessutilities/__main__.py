# uselessutilities/__main__.py

import sys
from .cli import main

if __name__ == "__main__":
    # Pass along any command-line arguments to your main()
    sys.exit(main(sys.argv[1:]))