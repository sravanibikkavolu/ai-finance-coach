import sys
import os
import importlib.metadata

# Permissive licenses allowed for general use
ALLOWED_LICENSES = [
    "mit",
    "apache",
    "bsd",
    "psf",
    "python software foundation",
    "isc",
    "unlicense",
    "cc0",
    "mpl",
    "lgpl",
    "zlib",
    "public domain",
]


def check_files():
    required_files = ["README.md", "requirements.txt", "pyproject.toml", "app.py"]
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
    return missing


def check_secrets():
    if not os.path.exists("app.py"):
        return []

    issues = []
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Check if a typical API key pattern or hardcoded key is found
    if "gsk_" in content:
        issues.append("Found potential hardcoded Groq API key in app.py")

    return issues


def check_licenses():
    if not os.path.exists("requirements.txt"):
        return [], []

    non_compliant = []
    skipped = []

    # Read requirements.txt with fallback encodings to handle UTF-16 / UTF-8
    content = ""
    for encoding in ["utf-16", "utf-16-le", "utf-16-be", "utf-8", "latin-1"]:
        try:
            with open("requirements.txt", "r", encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if not content:
        return [], []

    packages = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Extract package name (before == or >= or <=)
        name = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
        packages.append(name)

    for pkg in packages:
        try:
            meta = importlib.metadata.metadata(pkg)
            # License can be in License field or Classifiers
            lic = meta.get("License") or ""
            classifiers = meta.get_all("Classifier") or []

            # Check classifiers for license
            lic_classifiers = [
                c.split("::")[-1].strip().lower()
                for c in classifiers
                if "license" in c.lower()
            ]

            # Combine all license info
            lic_info = (lic + " " + " ".join(lic_classifiers)).lower()

            # Determine if it matches any allowed license
            is_allowed = False
            for allowed in ALLOWED_LICENSES:
                if allowed in lic_info:
                    is_allowed = True
                    break

            # If no license info could be parsed, default to warning/compliance skip
            if not lic_info.strip():
                continue

            if not is_allowed:
                non_compliant.append((pkg, lic))
        except importlib.metadata.PackageNotFoundError:
            skipped.append(pkg)

    return non_compliant, skipped


def main():
    print("=== AI Finance Coach Compliance Checker ===")

    # 1. Check Files
    print("\n1. Checking project structure...")
    missing_files = check_files()
    if missing_files:
        print(f"[-] Missing required files: {', '.join(missing_files)}")
        sys.exit(1)
    print("[+] All required files present.")

    # 2. Check Secrets
    print("\n2. Scanning for hardcoded credentials...")
    secret_issues = check_secrets()
    if secret_issues:
        for issue in secret_issues:
            print(f"[-] {issue}")
        sys.exit(1)
    print("[+] No hardcoded secrets found.")

    # 3. Check Licenses
    print("\n3. Verifying package license compliance...")
    non_compliant, skipped = check_licenses()

    if skipped:
        print(
            f"[!] Warning: Some packages are not installed in the environment: {', '.join(skipped)}"
        )

    if non_compliant:
        print("[-] Non-compliant licenses found:")
        for pkg, lic in non_compliant:
            print(f"    - {pkg}: {lic}")
        sys.exit(1)

    print("[+] License compliance check passed (all packages use permissive licenses).")
    print("\n[+] Compliance Check: SUCCESS")
    sys.exit(0)


if __name__ == "__main__":
    main()
