from app.services.folder_scanner import scan_folder


TEST_FOLDER = r"D:\MemoraAI_Knowledge"


result = scan_folder(TEST_FOLDER)

print("\n=== MemoraAI Folder Scanner Test ===")

print("\nRoot folder:")
print(result["root_folder"])

print("\nStatistics:")
for key, value in result["statistics"].items():
    print(f"  {key}: {value}")

print("\nSupported files:")
for file in result["supported_files"]:
    print(f"  ✓ {file}")

print("\nSkipped files:")
for file in result["skipped_files"]:
    print(f"  - {file}")

print("\nErrors:")
for error in result["errors"]:
    print(f"  ! {error['path']}")
    print(f"    {error['error']}")

print("\n=== Scan Complete ===")