from pathlib import Path
import glob


def get_folder_object_info(folder_name, get_object_count=True, get_total_bytes=True):
    total_bytes = 0
    objects = 0

    if get_object_count and get_total_bytes:
        folder_contents = Path(folder_name).rglob("*")
        for f in folder_contents:
            objects += 1
            if f.is_file():
                total_bytes = total_bytes + f.stat().st_size
        result = {"object_count": objects, "total_bytes": total_bytes}
        return result

    if get_object_count and not get_total_bytes:
        folder_contents = Path(folder_name).rglob("*")
        for f in folder_contents:
            objects += 1
        result = {"object_count": objects}
        return result

    if not get_object_count and get_total_bytes:
        folder_contents = Path(folder_name).rglob("*")
        for f in folder_contents:
            if f.is_file():
                total_bytes = total_bytes + f.stat().st_size
        result = {"total_bytes": total_bytes}
        return result





