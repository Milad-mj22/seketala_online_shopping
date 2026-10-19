import os
import sys

# پوشه‌هایی که به طور پیش‌فرض نادیده گرفته می‌شوند
SKIP_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'env',
    'node_modules', '.idea', '.vscode', 'build', 'dist',
    '.mypy_cache', '.pytest_cache', '.tox', 'site-packages'
}


def ask_yes_no(question, default=False):
    """پرسش بله/خیر از کاربر"""
    suffix = " [y/N]: " if not default else " [Y/n]: "
    while True:
        answer = input(question + suffix).strip().lower()
        if answer == "":
            return default
        if answer in ("y", "yes", "بله", "ب", "آ", "اری"):
            return True
        if answer in ("n", "no", "خیر", "خ", "ن", "نه"):
            return False
        print("⚠️ لطفاً y یا n وارد کنید.")


def collect_python_files(root_dir, output_file):
    root_dir = os.path.abspath(root_dir)
    output_file = os.path.abspath(output_file)

    py_files = []
    skipped_dirs = []

    print("\n" + "=" * 60)
    print("🔍 پیمایش پوشه‌ها...")
    print("=" * 60)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        rel = os.path.relpath(dirpath, root_dir)
        rel_display = "." if rel == "." else rel

        # بررسی پوشه‌های پیش‌فرض نادیده گرفته شده
        new_dirnames = []
        for d in dirnames:
            if d in SKIP_DIRS:
                skipped_dirs.append(os.path.join(rel_display, d))
                continue
            new_dirnames.append(d)
        dirnames[:] = new_dirnames

        # پرسش درباره‌ی خود پوشه (به جز ریشه)
        if dirpath != root_dir:
            if not ask_yes_no(f"📁 پوشه «{rel_display}» پردازش شود؟", default=True):
                skipped_dirs.append(rel_display)
                dirnames[:] = []  # زیرپوشه‌ها را پیمایش نکن
                continue

        # جمع‌آوری فایل‌های .py در این پوشه
        for fname in filenames:
            if fname.lower().endswith('.py'):
                py_files.append(os.path.join(dirpath, fname))

    py_files.sort()

    if not py_files:
        print(f"\n⚠️ هیچ فایل .py برای تجمیع پیدا نشد.")
        return

    total_bytes = 0

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write("📦 تجمیع فایل‌های پایتون\n")
        out.write(f"📁 دایرکتوری ریشه: {root_dir}\n")
        out.write(f"📄 تعداد فایل‌ها: {len(py_files)}\n")
        out.write("=" * 80 + "\n\n")

        for path in py_files:
            rel_path = os.path.relpath(path, root_dir)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(path, 'r', encoding='latin-1') as f:
                        content = f.read()
                except Exception as e:
                    out.write("\n" + "=" * 80 + "\n")
                    out.write(f"📄 فایل: {path}\n")
                    out.write(f"❌ خطا در خواندن فایل: {e}\n")
                    out.write("=" * 80 + "\n\n")
                    continue

            total_bytes += len(content.encode('utf-8'))

            out.write("\n" + "=" * 80 + "\n")
            out.write(f"📄 فایل: {path}\n")
            out.write(f"📁 مسیر نسبی: {rel_path}\n")
            out.write(f"📏 اندازه: {len(content)} کاراکتر\n")
            out.write("=" * 80 + "\n")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            out.write("\n")

    print("\n" + "=" * 60)
    print(f"✅ {len(py_files)} فایل تجمیع شد.")
    print(f"📏 حجم کل: {total_bytes / 1024:.1f} KB")
    print(f"💾 فایل خروجی: {output_file}")

    if skipped_dirs:
        print(f"\n⏭️ پوشه‌های نادیده گرفته شده ({len(skipped_dirs)}):")
        for d in skipped_dirs:
            print(f"   - {d}")


def main():
    if len(sys.argv) >= 2:
        root_dir = sys.argv[1]
    else:
        root_dir = input("📁 مسیر دایرکتوری ریشه را وارد کنید: ").strip().strip('"').strip("'")

    if not os.path.isdir(root_dir):
        print(f"❌ دایرکتوری وجود ندارد: {root_dir}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        default_out = os.path.join(os.path.dirname(os.path.abspath(root_dir)), "all_python_files.txt")
        output_file = input(f"💾 مسیر فایل خروجی (پیش‌فرض: {default_out}): ").strip().strip('"').strip("'")
        if not output_file:
            output_file = default_out

    collect_python_files(root_dir, output_file)


if __name__ == "__main__":
    main()