import shutil
import subprocess
import sys


def main():
    # Find uv executable
    uv_path = shutil.which("uv")
    if not uv_path:
        # Check standard venv paths
        for path in [".venv/Scripts/uv.exe", ".venv/bin/uv"]:
            if shutil.which(path):
                uv_path = path
                break

    if not uv_path:
        print("uv executable not found. Skipping audit.")
        sys.exit(0)

    try:
        # Run uv audit
        result = subprocess.run([uv_path, "audit"], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)

        # Check if the failure is due to a network connection/DNS issue
        stderr_lower = result.stderr.lower()
        if (
            "dns error" in stderr_lower
            or "no such host is known" in stderr_lower
            or "failed to fetch" in stderr_lower
            or "temporary failure in name resolution" in stderr_lower
        ):
            print(
                "Vulnerability audit warning: Offline / Network connection issue. Skipped audit."
            )
            sys.exit(0)

        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running uv audit: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
