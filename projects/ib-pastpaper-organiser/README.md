# ib-pastpaper-organiser
Quick tool for me to extract questions from IB past papers.

## setup
Put the subject reports under `data/sr`.
```
$ sudo apt-get -y install ghostscript icc-profiles-free liblept5 libxml2 pngquant python3-pip tesseract-ocr zlib1g
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 main.py
```