# rcp103
CNAM UE RCP103


SaaS LateX: [https://www.overleaf.com/](https://www.overleaf.com/)
==> se créer un compte fictif avec [https://10minemail.com](https://10minemail.com)

Extenion LateX pour VSCode:

- [https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

- [https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile)
A LaTeX file is typically built by calling the command Build LaTeX project from the Command Palette or from the TeX badge. 
This command is bind to ctrl+alt+b.

https://winshell.org/
https://miktex.org/ https://www.luatex.org/ 

## Pre-req

### Install MiKTeX on WSL2-Ubuntu2404

Check Perl is installed : 

```bash
perl -v
```

```console
This is perl 5, version 38, subversion 2 (v5.38.2) built for x86_64-linux-gnu-thread-multi
```

```bash
ls -al /etc/os-release
cat /usr/lib/os-release | grep -i "PRETTY_NAME"
```

```console
/etc/os-release -> ../usr/lib/os-release
PRETTY_NAME="Ubuntu 24.04.4 LTS"
```

Read [docs](https://miktex.org/download)

```bash
curl -fsSL https://miktex.org/download/key | sudo gpg --dearmor -o /usr/share/keyrings/miktex.gpg
echo "deb [signed-by=/usr/share/keyrings/miktex.gpg] https://miktex.org/download/ubuntu noble universe" | sudo tee /etc/apt/sources.list.d/miktex.list
sudo apt-get update
sudo apt-get install miktex --yes
```

```bash
miktexsetup --help
miktexsetup --version
```

```console
MiKTeX Setup Utility 5.5.0+add6066

© 2026 Christian Schenk

This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

```bash
miktexsetup finish
```


```bash
miktexsetup finish
ls -al ~/bin/lualatex
ls -al ~/bin/*tex*
ls -al /usr/bin/miktex*

cat ~/.profile | grep -i PATH
ls -al $HOME/bin
miktex --help
```
### Upgrade MiKTeX

```bash
sudo apt-get update
sudo apt-get upgrade miktex --yes
```
[https://github.com/MiKTeX/miktex/issues/724#issuecomment-785949728](https://github.com/MiKTeX/miktex/issues/724#issuecomment-785949728)

```bash
sudo mpm --admin --update
mpm --update

miktex packages update-package-database
miktex packages update
```

### Install TexLive on Windows

- [https://www.tug.org/texlive/quickinstall.html](https://www.tug.org/texlive/quickinstall.html)
```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

powershell.exe -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://mirror.ctan.org/systems/texlive/tlnet/install-tl-windows.exe' -OutFile '.\install-tl-windows.exe'"

Start-Process "install-tl-windows.exe"
```

```console
Installing to: C:/texlive/2026
```

[https://www.tug.org/texlive/windows.html](https://www.tug.org/texlive/windows.html)
```bash
SET "PATH=%PATH%;C:\texlive\2026\bin\windows"
```

# Générer le rapport

Read the [docs](https://docs.miktex.org/manual/miktex-pdftex.html)

```bash
# pdflatex --job-name=tp1 ./rapport/rapport_suites.tex --output-directory=/tmp

miktex packages install miktex-pdftex --help
miktex packages install miktex-pdftex
miktex packages install plain
miktex packages install cm
miktex packages install fontname
miktex packages install knuth-lib
miktex packages install montex
miktex packages install miktex-metafont
miktex packages install metafont
miktex packages install kdgreek
miktex packages install modes
miktex packages install tex-ini-files

miktex packages install latexmk
ls -al ~/bin/latexmk
ls -al /usr/libexec/miktex/runperl

miktex-pdftex --help
miktex-pdftex  --version
miktex-pdftex --job-name=tp1 ./rapport/rapport_suites.tex --output-directory=./rapport --output-format=pdf

```

# How-To use MikTeX Console

```bash
mpm
```