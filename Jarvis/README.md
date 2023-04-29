https://github.com/nltk/nltk_data

sphinx_kws -ifile fileids.txt -kws kws.txt -di . -do .

安装 Whisper

iwr -useb https://gitee.com/glsnames/scoop-installer/raw/master/bin/install.ps1 | iex
scoop config SCOOP_REPO 'https://gitee.com/glsnames/scoop-installer'
scoop update
scope install ffmpeg
pip install setuptools-rust tqdm ffmpeg