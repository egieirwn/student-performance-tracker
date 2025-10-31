"""Aplikasi CLI Student Performance Tracker."""

import os
from tracker import (
    RekapKelas,
    build_markdown_report,
    build_html_report,
    save_text,
)

DATA_DIR = "data"
OUT_DIR = "out"
ATTENDANCE_CSV = os.path.join(DATA_DIR, "kehadiran.csv")
GRADES_CSV = os.path.join(DATA_DIR, "grades.csv")
OUT_REPORT = os.path.join(OUT_DIR, "report.md")
OUT_HTML = os.path.join(OUT_DIR, "report.html")


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)


def print_menu():
    print("\n=== Student Performance Tracker ===")
    print("1) Muat data dari CSV")
    print("2) Tambah mahasiswa")
    print("3) Ubah presensi")
    print("4) Ubah nilai")
    print("5) Lihat rekap")
    print("6) Simpan laporan Markdown")
    print("7) Simpan data ke CSV")
    print("8) Tampilkan mahasiswa dengan nilai < 70")
    print("9) Simpan laporan HTML berwarna")
    print("10) Reset semua data (hapus isi CSV & memori)")
    print("11) Keluar")


def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val


def reset_data():
    """Mengosongkan isi file kehadiran.csv dan grades.csv."""
    confirm = input("Apakah kamu yakin ingin menghapus semua data? (y/n): ").lower()
    if confirm != "y":
        print("❌ Dibatalkan.")
        return False  # return False supaya tahu reset dibatalkan

    os.makedirs(DATA_DIR, exist_ok=True)

    # Kosongkan dan tulis ulang header
    with open(ATTENDANCE_CSV, "w", encoding="utf-8") as f:
        f.write("nim,nama,hadir_persen\n")
    with open(GRADES_CSV, "w", encoding="utf-8") as f:
        f.write("nim,quiz,tugas,uts,uas\n")

    print("✅ Semua data berhasil direset (file kehadiran.csv dan grades.csv dikosongkan).")
    return True  # return True untuk tandai reset sukses


def main():
    ensure_dirs()
    rk = RekapKelas()

    while True:
        print_menu()
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            print("Memuat data dari CSV...")
            if os.path.exists(ATTENDANCE_CSV):
                rk.load_attendance_csv(ATTENDANCE_CSV)
                print(" - kehadiran.csv dimuat.")
            else:
                print(" - kehadiran.csv tidak ditemukan.")
            if os.path.exists(GRADES_CSV):
                rk.load_grades_csv(GRADES_CSV)
                print(" - grades.csv dimuat.")
            else:
                print(" - grades.csv tidak ditemukan.")

        elif pilihan == "2":
            nim = input_non_empty("NIM: ")
            nama = input_non_empty("Nama: ")
            hadir = input("Hadir (%): ").strip() or "0"
            try:
                rk.tambah_mahasiswa(nim, nama, hadir)
                print("✅ Mahasiswa berhasil ditambahkan.")
            except Exception as e:
                print("❌ Gagal:", e)

        elif pilihan == "3":
            nim = input_non_empty("NIM: ")
            hadir = input_non_empty("Persentase hadir baru: ")
            try:
                rk.set_hadir(nim, hadir)
                print("✅ Presensi berhasil diperbarui.")
            except Exception as e:
                print("❌ Gagal:", e)

        elif pilihan == "4":
            nim = input_non_empty("NIM: ")
            print("Kosongkan jika tidak ingin mengubah kolom tertentu.")
            quiz = input("Quiz: ").strip() or None
            tugas = input("Tugas: ").strip() or None
            uts = input("UTS: ").strip() or None
            uas = input("UAS: ").strip() or None
            try:
                rk.set_penilaian(nim, quiz=quiz, tugas=tugas, uts=uts, uas=uas)
                print("✅ Nilai berhasil diperbarui.")
            except Exception as e:
                print("❌ Gagal:", e)

        elif pilihan == "5":
            records = rk.rekap()
            if not records:
                print("⚠️ Belum ada data.")
            else:
                print("| NIM   |     Nama     |   Hadir (%)   | Nilai Akhir | Predikat |")
                print("|-------|--------------|---------------|-------------|----------|")
                for r in records:
                    print(f"| {r['nim']} | {r['nama']} | {r['hadir']:.1f} | {r['nilai_akhir']:.2f} | {r['predikat']} |")

        elif pilihan == "6":
            records = rk.rekap()
            content = build_markdown_report(records)
            save_text(OUT_REPORT, content)
            print(f"✅ Laporan Markdown disimpan ke {OUT_REPORT}")

        elif pilihan == "7":
            rk.save_attendance_csv(ATTENDANCE_CSV)
            rk.save_grades_csv(GRADES_CSV)
            print("✅ Data berhasil disimpan ke data/kehadiran.csv dan data/grades.csv")

        elif pilihan == "8":
            records = rk.filter_below(70)
            if not records:
                print("🎉 Tidak ada mahasiswa dengan nilai < 70.")
            else:
                print("\nMahasiswa dengan nilai < 70:")
                print("| NIM   |     Nama     |   Hadir (%)   | Nilai Akhir | Predikat |")
                print("|-------|--------------|---------------|-------------|----------|")
                for r in records:
                    print(f"| {r['nim']} | {r['nama']} | {r['hadir']:.1f} | {r['nilai_akhir']:.2f} | {r['predikat']} |")

        elif pilihan == "9":
            records = rk.rekap()
            html = build_html_report(records)
            save_text(OUT_HTML, html)
            print(f"✅ Laporan HTML disimpan ke {OUT_HTML}")

        elif pilihan == "10":
            if reset_data():
                rk = RekapKelas()  # kosongkan data di memori juga
                print("🧹 Data di memori juga telah dihapus.")

        elif pilihan == "11":
            print("👋 Keluar dari aplikasi. Sampai jumpa!")
            break

        else:
            print("❌ Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
