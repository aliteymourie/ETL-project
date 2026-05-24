import subprocess
import sys
import importlib

# لیست تمام کتابخانه‌های مورد نیاز پروژه همراه با نام پکیج آن‌ها در pip
REQUIRED_LIBRARIES = {
    "yaml": "pyyaml",
    "pyodbc": "pyodbc",
    "sqlalchemy": "sqlalchemy",
    "pandas": "pandas",
    "psycopg2": "psycopg2-binary",  # نسخه باینری برای راحتی نصب در لینوکس و ویندوز
    "jdatetime": "jdatetime",        # برای مدیریت تاریخ شمسی در بخش تقویم جلالی
    "pydantic": "pydantic"          # برای اعتبارسنجی دیتا دیتا شیت‌ها
}

def check_and_install_libraries():
    print("--- بررسی و نصب خودکار کتابخانه‌های پروژه ETL ---")
    
    missing_libraries = []
    
    # ۱. بررسی اینکه کدام کتابخانه‌ها نصب نیستند
    for module_name, pip_name in REQUIRED_LIBRARIES.items():
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} از قبل نصب شده است.")
        except ImportError:
            print(f"❌ {module_name} یافت نشد. نیاز به نصب دارد.")
            missing_libraries.append(pip_name)
            
    # ۲. نصب کتابخانه‌های مفقود شده در صورت وجود
    if missing_libraries:
        print(f"\nدر حال نصب {len(missing_libraries)} کتابخانه مفقود شده...")
        try:
            # اجرای دستور pip install به صورت مستقیم از درون پایتون
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_libraries])
            print("\n🎉 تمام کتابخانه‌ها با موفقیت نصب و به‌روزرسانی شدند!")
        except subprocess.CalledProcessError as e:
            print(f"\n🚨 خطایی در حین نصب کتابخانه‌ها رخ داد: {e}")
            sys.exit(1)
    else:
        print("\n🚀 عالیه! تمام پیش‌نیازهای پایتونی از قبل آماده هستند.")

if __name__ == "__main__":
    check_and_install_libraries()