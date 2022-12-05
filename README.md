## Install

### Via pip

`python -m pip install -U srun-cli-bit`

### Via binary

Download binary file from GitHub  [release page](https://github.com/c-my/srun-cli-bit/releases/latest) .
(If you are using Linux, you may need  to run `chmod +x [binary_file]` first.)

### Via source
1. Clone this repo
2. Install dependencies using `pip install -r requirements.txt`
3. Run `python src/main.py login`

## Usage

`srun-bit config`: set account ID and Password

`srun-bit login`: sign in the network account

`srun-bit logout`: disconnect the network 

`srun-bit info`: show account information

## Note
### Latest Binary Version Compile Option
* Windows10(python3.9.15): `python -m nuitka src/main.py --onefile --standalone --mingw64`
* Ubuntu(python3.9.15): `python -m nuitka --onefile --standalone src/main.py`

**_Windows binary version NOT works on Windows7_**

## Thanks to

[https://github.com/vouv/srun](https://github.com/vouv/srun)

[Nuitka](https://nuitka.net/)

