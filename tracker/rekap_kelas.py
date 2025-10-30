"""Kelas RekapKelas: menyimpan seluruh data mahasiswa dan nilai."""

from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """Mengelola data mahasiswa, nilai, dan rekap laporan."""

    def __init__(self):
        self._data = {}

    def tambah_mahasiswa(self, nim, nama, hadir_persen=0):
        if nim in self._data:
            raise ValueError("Mahasiswa sudah ada.")
        m = Mahasiswa(nim, nama, hadir_persen)
        p = Penilaian()
        self._data[nim] = {"mhs": m, "nilai": p}

    def set_hadir(self, nim, hadir_persen):
        if nim not in self._data:
            raise KeyError("NIM tidak ditemukan.")
        self._data[nim]["mhs"].hadir_persen = hadir_persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        if nim not in self._data:
            raise KeyError("NIM tidak ditemukan.")
        p = self._data[nim]["nilai"]
        if quiz is not None: p.quiz = quiz
        if tugas is not None: p.tugas = tugas
        if uts is not None: p.uts = uts
        if uas is not None: p.uas = uas

    def predikat(self, nilai):
        n = float(nilai)
        if n >= 85: return "A"
        elif n >= 70: return "B"
        elif n >= 60: return "C"
        elif n >= 40: return "D"
        return "E"

    def rekap(self):
        records = []
        for nim, d in sorted(self._data.items()):
            m, p = d["mhs"], d["nilai"]
            nilai_akhir = round(p.nilai_akhir(), 2)
            records.append({
                "nim": nim,
                "nama": m.nama,
                "hadir": m.hadir_persen,
                "nilai_akhir": nilai_akhir,
                "predikat": self.predikat(nilai_akhir)
            })
        return records

    def filter_below(self, threshold=70):
        """Tampilkan hanya mahasiswa dengan nilai akhir di bawah threshold."""
        return [r for r in self.rekap() if r["nilai_akhir"] < threshold]

    def load_attendance_csv(self, path):
        import csv
        with open(path, newline='', encoding="utf-8") as f:
            for row in csv.DictReader(f):
                nim = row.get("nim")
                nama = row.get("nama")
                hadir = row.get("hadir_persen", 0)
                if nim not in self._data:
                    self.tambah_mahasiswa(nim, nama, hadir)
                else:
                    self.set_hadir(nim, hadir)

    def load_grades_csv(self, path):
        import csv
        with open(path, newline='', encoding="utf-8") as f:
            for row in csv.DictReader(f):
                nim = row.get("nim")
                if nim not in self._data:
                    self.tambah_mahasiswa(nim, "(no name)", 0)
                self.set_penilaian(
                    nim,
                    quiz=row.get("quiz", 0),
                    tugas=row.get("tugas", 0),
                    uts=row.get("uts", 0),
                    uas=row.get("uas", 0)
                )

    def save_attendance_csv(self, path):
        import csv
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nim", "nama", "hadir_persen"])
            for nim, d in sorted(self._data.items()):
                m = d["mhs"]
                writer.writerow([nim, m.nama, m.hadir_persen])

    def save_grades_csv(self, path):
        import csv
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nim", "quiz", "tugas", "uts", "uas"])
            for nim, d in sorted(self._data.items()):
                n = d["nilai"]
                writer.writerow([nim, n.quiz, n.tugas, n.uts, n.uas])
