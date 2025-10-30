"""Kelas Mahasiswa: menyimpan data identitas dan kehadiran."""

class Mahasiswa:
    """Representasi mahasiswa dengan nim, nama, dan hadir persen."""

    def __init__(self, nim, nama, hadir_persen=0):
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0
        self.hadir_persen = hadir_persen

    @property
    def hadir_persen(self):
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, value):
        try:
            v = float(value)
        except ValueError:
            raise ValueError("Nilai hadir harus berupa angka.")
        if not 0 <= v <= 100:
            raise ValueError("Hadir harus antara 0 dan 100.")
        self._hadir_persen = v

    def info(self):
        return f"{self.nim} - {self.nama} (Hadir: {self.hadir_persen}%)"
