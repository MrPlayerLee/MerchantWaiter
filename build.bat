@echo off

pyinstaller --onefile --noconsole --icon=Icon/Icon.ico --add-data "Icon/Icon.ico;Icon" --add-data "sfx/Merchant_Come.wav;sfx" --add-data "sfx/Merchant_Here.wav;sfx" NewMerchantWaiter.py


pause