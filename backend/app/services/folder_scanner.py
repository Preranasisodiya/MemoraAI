from pathlib import Path


# File types currently supported by MemoraAI
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def scan_folder(folder_path: str):
    """
    Recursively scan a user-selected folder.

    The selected folder is the scanning boundary.
    Only supported file types are returned for processing.
    Unsupported or inaccessible files are skipped safely.
    """

    root = Path(folder_path).resolve()

    # Validate selected path
    if not root.exists():
        raise ValueError("The selected folder does not exist.")

    if not root.is_dir():
        raise ValueError("The selected path is not a folder.")

    supported_files = []
    skipped_files = []
    errors = []

    # Recursively scan the selected folder
    for path in root.rglob("*"):

        # Never follow symbolic links
        if path.is_symlink():
            continue

        # Ignore directories
        if not path.is_file():
            continue

        try:
            extension = path.suffix.lower()

            if extension in SUPPORTED_EXTENSIONS:
                supported_files.append(path)
            else:
                skipped_files.append(path)

        except (PermissionError, OSError) as exc:
            errors.append({
                "path": str(path),
                "error": str(exc),
            })

    # Sort results for predictable output
    supported_files.sort(key=lambda p: str(p).lower())
    skipped_files.sort(key=lambda p: str(p).lower())

    return {
        "root_folder": str(root),
        "supported_files": supported_files,
        "skipped_files": skipped_files,
        "errors": errors,
        "statistics": {
            "supported": len(supported_files),
            "skipped": len(skipped_files),
            "errors": len(errors),
            "total_files_found": (
                len(supported_files)
                + len(skipped_files)
                + len(errors)
            ),
        },
    }