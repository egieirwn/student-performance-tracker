"""Entry point agar bisa dijalankan langsung dengan `python -m tracker`."""
from tracker import RekapKelas, build_markdown_report, save_text
import os

def main():
    print("=== Menjalankan student_performance_tracker ===")

    rk = RekapKelas()

    # Tambahkan beberapa contoh mahasiswa
    rk.tambah_mahasiswa("230101001", "Egie", 92)
    rk.set_penilaian("230101001", quiz=90, tugas=85, uts=88, uas=92)

    rk.tambah_mahasiswa("230101002", "Fiko", 80)
    rk.set_penilaian("230101002", quiz=70, tugas=75, uts=68, uas=72)

    rk.tambah_mahasiswa("230101003", "Pradipta", 60)
    rk.set_penilaian("230101003", quiz=98, tugas=89, uts=90, uas=98)

    # Buat laporan otomatis
    records = rk.rekap()
    os.makedirs("out", exist_ok=True)
    content = build_markdown_report(records)
    save_text("out/report.md", content)

    print("📄 Laporan berhasil dibuat di: out/report.md")
    print("Mahasiswa yang tercantum:", len(records), "orang.")

if __name__ == "__main__":
    main()
