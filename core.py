import os
import platform
import shlex
import subprocess
from enum import Enum
from pathlib import Path

if os.name == "nt":
    gs_cmd = "gswin{}c".format(platform.architecture()[0][:2])
elif os.name == "posix":
    gs_cmd = "gs"


class VectorFormat(str, Enum):
    SVG = ".svg"
    PDF = ".pdf"
    EPS = ".eps"
    EMF = ".emf"


def eps2pdf(src: Path, dst: Path):
    assert src.suffix == VectorFormat.EPS
    assert dst.suffix == VectorFormat.PDF
    cmd = "{} -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dEPSCrop -q -sOutputFile={} {}".format(gs_cmd, dst, src)
    cmd = shlex.split(cmd, posix=os.name == "posix")
    subprocess.run(cmd, capture_output=False)


def emf2svg(src: Path, dst: Path):
    assert src.suffix == VectorFormat.EMF
    assert dst.suffix == VectorFormat.SVG
    cmd = "inkscape --export-filename={} {}".format(dst, src)
    cmd = shlex.split(cmd, posix=os.name == "posix")
    subprocess.run(cmd, capture_output=False)


def pdf2svg(src: Path, dst: Path):
    assert src.suffix == VectorFormat.PDF
    assert dst.suffix == VectorFormat.SVG
    cmd = "pdf2svg {} {}".format(src, dst)
    cmd = shlex.split(cmd, posix=os.name == "posix")
    subprocess.run(cmd, capture_output=False)


def svg2any(src: Path, dst: Path):
    assert src.suffix == VectorFormat.SVG
    cmd = "inkscape --export-filename={} {}".format(dst, src)
    cmd = shlex.split(cmd, posix=os.name == "posix")
    subprocess.run(cmd, capture_output=False)


def pdf2any(src: Path, dst: Path):
    svg_tmp = src.with_suffix(VectorFormat.SVG)
    pdf2svg(src, svg_tmp)
    svg2any(svg_tmp, dst)


def eps2any(src: Path, dst: Path):
    pdf_tmp = src.with_suffix(VectorFormat.PDF)
    eps2pdf(src, pdf_tmp)
    pdf2any(pdf_tmp, dst)


def emf2any(src: Path, dst: Path):
    svg_tmp = src.with_suffix(VectorFormat.SVG)
    emf2svg(src, svg_tmp)
    svg2any(svg_tmp, dst)


def any2any(src: Path, dst: Path):
    match src.suffix:
        case VectorFormat.SVG:
            svg2any(src, dst)
        case VectorFormat.PDF:
            pdf2any(src, dst)
        case VectorFormat.EPS:
            eps2any(src, dst)
        case VectorFormat.EMF:
            emf2any(src, dst)
        case _:
            print("unsupported vector format !")


if __name__ == "__main__":
    eps2any("demo.eps", "output.emf")
