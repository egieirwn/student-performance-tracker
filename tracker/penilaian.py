"""Kelas Penilaian: menyimpan nilai mahasiswa."""

class Penilaian:
    """Menyimpan nilai dan menghitung nilai akhir berbobot."""

    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _valid(self, val):
        try:
            v = float(val)
        except ValueError:
            raise ValueError("Nilai harus berupa angka.")
        if not 0 <= v <= 100:
            raise ValueError("Nilai harus di antara 0 dan 100.")
        return v

    @property
    def quiz(self): return self._quiz
    @quiz.setter
    def quiz(self, v): self._quiz = self._valid(v)

    @property
    def tugas(self): return self._tugas
    @tugas.setter
    def tugas(self, v): self._tugas = self._valid(v)

    @property
    def uts(self): return self._uts
    @uts.setter
    def uts(self, v): self._uts = self._valid(v)

    @property
    def uas(self): return self._uas
    @uas.setter
    def uas(self, v): self._uas = self._valid(v)

    def nilai_akhir(self):
        """Hitung nilai akhir berbobot."""
        return (
            self.quiz * 0.15 +
            self.tugas * 0.25 +
            self.uts * 0.25 +
            self.uas * 0.35
        )
