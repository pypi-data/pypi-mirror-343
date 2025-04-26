import subprocess
import sys
import signal
import atexit
import shutil
import os
import platform
import requests
import stat
from pathlib import Path
import time

_cloudflared_process = None
_jlab_process = None

# Define a directory to store the downloaded binary
DOWNLOAD_DIR = Path.home() / ".jovyanai" / "bin"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
CLOUDFLARED_PATH = DOWNLOAD_DIR / "cloudflared"


def _get_cloudflared_download_url():
    """Determines the cloudflared download URL for the current OS/Arch."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine == "aarch64":
            arch = "arm64"
        else:
            return None, f"Unsupported Linux architecture: {machine}"
        filename = f"cloudflared-linux-{arch}"
    elif system == "darwin": # macOS
        if machine == "x86_64":
            arch = "amd64"
        elif machine == "arm64": # Apple Silicon
             arch = "arm64"
        else:
            return None, f"Unsupported macOS architecture: {machine}"
        filename = f"cloudflared-darwin-{arch}.tgz" # Needs extraction later
    elif system == "windows":
        if machine in ["x86_64", "amd64"]:
             arch = "amd64"
        else:
             return None, f"Unsupported Windows architecture: {machine}"
        filename = f"cloudflared-windows-{arch}.exe"
    else:
        return None, f"Unsupported operating system: {system}"

    url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/{filename}"
    return url, filename


def _download_and_extract(url, filename, dest_path):
    """Downloads and extracts/saves the cloudflared binary."""
    print(f"Downloading cloudflared from {url}...", file=sys.stderr)
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        temp_download_path = dest_path.parent / (filename + ".tmp")

        with open(temp_download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Download complete.", file=sys.stderr)

        if filename.endswith(".tgz"):
             print(f"Extracting {temp_download_path}...", file=sys.stderr)
             import tarfile
             with tarfile.open(temp_download_path, "r:gz") as tar:
                 # Find the binary within the archive (common names)
                 binary_member = None
                 for member in tar.getmembers():
                     if member.name == 'cloudflared' or member.name.endswith('/cloudflared'):
                         binary_member = member
                         break
                 if not binary_member:
                     raise RuntimeError("Could not find 'cloudflared' binary in the downloaded archive.")
                 binary_member.name = dest_path.name # Extract directly with the final name
                 tar.extract(binary_member, path=dest_path.parent)
             print("Extraction complete.", file=sys.stderr)
             temp_download_path.unlink() # Clean up archive
        else:
            # For non-archives (Linux .deb/.rpm, Windows .exe), just rename
            temp_download_path.rename(dest_path)

        # Make executable
        current_stat = os.stat(dest_path)
        os.chmod(dest_path, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"cloudflared saved to {dest_path} and made executable.", file=sys.stderr)
        return dest_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading cloudflared: {e}", file=sys.stderr)
        if temp_download_path.exists():
             temp_download_path.unlink()
        return None
    except Exception as e:
        print(f"Error processing downloaded file: {e}", file=sys.stderr)
        if temp_download_path.exists():
             temp_download_path.unlink()
        if dest_path.exists(): # Clean up partially extracted file
            dest_path.unlink()
        return None


def ensure_cloudflared():
    """Checks for cloudflared, downloads if needed, returns executable path."""
    # 1. Check PATH
    cloudflared_path = shutil.which("cloudflared")
    if cloudflared_path:
        print(f"Found cloudflared in PATH: {cloudflared_path}", file=sys.stderr)
        return cloudflared_path

    # 2. Check local download directory
    if CLOUDFLARED_PATH.exists() and os.access(CLOUDFLARED_PATH, os.X_OK):
        print(f"Found downloaded cloudflared: {CLOUDFLARED_PATH}", file=sys.stderr)
        return str(CLOUDFLARED_PATH)

    # 3. Download
    print(f"cloudflared not found, attempting download to {DOWNLOAD_DIR}...", file=sys.stderr)
    url, filename = _get_cloudflared_download_url()
    if not url:
        print(f"Error: {filename}", file=sys.stderr) # filename contains the error message here
        return None

    executable_path = _download_and_extract(url, filename, CLOUDFLARED_PATH)
    return executable_path


def _cleanup_processes(signum=None, frame=None):
    """Gracefully terminate child processes."""
    global _cloudflared_process, _jlab_process

    processes_to_stop = []
    if _jlab_process and _jlab_process.poll() is None:
        processes_to_stop.append(("JupyterLab", _jlab_process))
    if _cloudflared_process and _cloudflared_process.poll() is None:
        processes_to_stop.append(("cloudflared", _cloudflared_process))

    if not processes_to_stop:
        return

    print("\nStopping child processes...", file=sys.stderr)

    for name, proc in processes_to_stop:
        if proc.poll() is None: # Check again if it terminated in the meantime
            print(f"Stopping {name} (PID {proc.pid})...", file=sys.stderr, end="")
            try:
                # On non-Windows, send SIGTERM first for graceful shutdown
                if os.name != 'nt':
                    proc.terminate()
                    proc.wait(timeout=5) # Give it time to shut down
                else:
                    # Windows doesn't really have SIGTERM, kill is more direct
                    proc.kill()
                    proc.wait(timeout=5)
                print(" stopped.", file=sys.stderr)
            except subprocess.TimeoutExpired:
                print(" timeout, killing...", file=sys.stderr, end="")
                proc.kill()
                proc.wait(timeout=2) # Short wait after kill
                print(" killed.", file=sys.stderr)
            except Exception as e:
                print(f" error: {e}", file=sys.stderr)

    _cloudflared_process = None
    _jlab_process = None
    # Add a small delay to allow terminal output to flush
    time.sleep(0.1)


def start_jlab():
    """Starts JupyterLab and a cloudflared tunnel."""
    global _cloudflared_process, _jlab_process

    # Ensure cloudflared is available
    cloudflared_executable = ensure_cloudflared()
    if not cloudflared_executable:
        print("Could not find or install cloudflared. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Register cleanup handlers *after* we know we can proceed
    atexit.register(_cleanup_processes)
    signal.signal(signal.SIGTERM, _cleanup_processes)
    signal.signal(signal.SIGINT, _cleanup_processes) # Handle Ctrl+C

    jlab_port = "8888"
    tunnel_url = f"http://localhost:{jlab_port}"

    # Start cloudflared tunnel
    print(f"Starting cloudflared tunnel for {tunnel_url}...", file=sys.stderr)
    try:
        # Pipe stderr to avoid cluttering, but maybe capture/log it?
        # For now, let it print the URL.
        _cloudflared_process = subprocess.Popen(
            [str(cloudflared_executable), "tunnel", "--url", tunnel_url,
             "--protocol", "http2", "--no-autoupdate"],
            stdout=sys.stdout, # Show tunnel URL
            stderr=sys.stderr, # Capture other logs maybe? Or also sys.stderr
        )
        print("cloudflared tunnel process started.", file=sys.stderr)
        # Brief pause to allow tunnel to potentially establish/print URL
        time.sleep(2)
    except Exception as e:
        print(f"Error starting cloudflared: {e}", file=sys.stderr)
        _cleanup_processes() # Attempt cleanup before exiting
        sys.exit(1)

    time.sleep(5)

    # Start JupyterLab
    print(f"Starting JupyterLab on port {jlab_port}...", file=sys.stderr)
    jlab_command = ["jupyter", "lab",
        "--ip=0.0.0.0",
        f"--port={jlab_port}",
        "--no-browser",
        "--ServerApp.token=''",
        "--ServerApp.allow_origin='*'"
        # Add other ServerApp flags if needed
    ]
    print(f"Running command: {' '.join(jlab_command)}", file=sys.stderr)
    try:
        # Use Popen to manage the process directly for cleanup
        _jlab_process = subprocess.Popen(jlab_command)
        # Wait for JupyterLab process to finish
        _jlab_process.wait()
        print("JupyterLab process exited.", file=sys.stderr)

    except KeyboardInterrupt:
        print("\nJupyterLab interrupted by user.", file=sys.stderr)
        # Cleanup will be handled by the signal handler and atexit
    except Exception as e:
        print(f"Error running JupyterLab: {e}", file=sys.stderr)
    finally:
        # Explicitly call cleanup when JLab finishes or fails.
        # atexit handles normal exit, signal handlers handle interruption.
        # This ensures cloudflared stops if JLab crashes.
        _cleanup_processes()
        sys.exit(0) # Ensure clean exit code after cleanup


if __name__ == "__main__":
    start_jlab() 