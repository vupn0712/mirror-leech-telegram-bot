from ....helper.ext_utils.status_utils import (
    MirrorStatus,
    get_readable_file_size,
    get_readable_time,
)


class GoogleDriveStatus:
    def __init__(self, listener, obj, gid, status):
        self.listener = listener
        self._obj = obj
        self._size = self.listener.size
        self._gid = gid
        self._status = status
        self.tool = "gDriveApi"

    def processed_bytes(self):
        return get_readable_file_size(self._obj.processed_bytes)

    def size(self):
        return get_readable_file_size(self._size)

    def status(self):
        if self._status == "up":
            return MirrorStatus.STATUS_UPLOAD
        elif self._status == "dl":
            return MirrorStatus.STATUS_DOWNLOAD
        else:
            return MirrorStatus.STATUS_CLONE

    def name(self):
        return self.listener.name

    def gid(self) -> str:
        return self._gid

    def progress_raw(self):
        if self._obj.total_files_to_upload > 0:
            return self._obj.uploaded_files_count / self._obj.total_files_to_upload * 100
        try:
            return self._obj.processed_bytes / self._size * 100
        except:
            return 0

    def progress(self):
        pct = round(self.progress_raw(), 2)
        if self._obj.total_files_to_upload > 0:
            return f"{pct}% ({self._obj.uploaded_files_count}/{self._obj.total_files_to_upload} files)"
        return f"{pct}%"

    def speed(self):
        return f"{get_readable_file_size(self._obj.speed)}/s"

    def eta(self):
        try:
            if self._obj.total_files_to_upload > 0:
                remaining = self._obj.total_files_to_upload - self._obj.uploaded_files_count
                if self._obj.uploaded_files_count > 0:
                    from time import time
                    elapsed = time() - self._obj._upload_start_time
                    per_file = elapsed / self._obj.uploaded_files_count
                    return get_readable_time(remaining * per_file)
                return "-"
            seconds = (self._size - self._obj.processed_bytes) / self._obj.speed
            return get_readable_time(seconds)
        except:
            return "-"

    def task(self):
        return self._obj
