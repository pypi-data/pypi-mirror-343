# **sleepyconvert**
*A quick way to convert file formats.*

<br />

## **Welcome to sleepyconvert!**
Do you find yourself bookmarking various online converters or having several tools to convert common file types? I did, and it didn't spark joy.

**`sleepyconvert`** is a tool that handles this in a minimal syntax.

Quickly convert file formats to and from:
- **data**
  - `csv`
  - `parquet`
  - `json`
  - `pkl`
  - `xlsx`
- **img**
  - `png`
  - `jpg`/`jpeg`
- **doc**
  - `html`
  - `pdf`
  - `md`

For some data files, you can optionally compress (*gzip*) the output.

> ℹ️ Note that this tool presumes format by file extension. If you leave out extensions, or give csv data a `.json` extension for funsies, then you're being silly.

> ℹ️ Due to how document file formats vary, not all functionality can be preserved from one type to another, and formatting 1-1-ness may vary.

<br />

## **Get Started 🚀**

```sh
pip install sleepyconvert
pip install --upgrade sleepyconvert

python -m sleepyconvert --help
python -m sleepyconvert data data.csv data.parquet --compress
python -m sleepyconvert img photo.png photo.jpg
python -m sleepyconvert doc photo.html photo.pdf
```

<br />

## **Usage ⚙**

Set a function in your shell environment to run a script like:
```sh
alias convert='python -m sleepyconvert'
```

Presuming you've named said macro `convert`, print the help message:
```sh
convert --help
convert data data.csv data.parquet
convert img photo.png photo.jpg
convert doc photo.html photo.pdf
```

<br />

## **Technologies 🧰**

  - [Pandas](https://pandas.pydata.org/docs/)
  - [Typer](https://typer.tiangolo.com/)
  - [PyArrow](https://arrow.apache.org/docs/python/index.html)
  - [openpyxl](https://pypi.org/project/openpyxl/)
  - [weasyprint](https://pypi.org/project/weasyprint/)
  - [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
  - [Markdown](PyPIhttps://pypi.org/project/Markdown/)
  - [html2text](https://pypi.org/project/html2text/)

<br />

## **Contribute 🤝**

If you have thoughts on how to make the tool more pragmatic, submit a PR 😊.

To add support for more data/file types:
1. append extension name to `supported_<mode>_formats` in `sleepyconvert_toolchain.params.py`
2. add detection logic branch to the `main` function in `sleepyconvert_toolchain/commands.py`
3. update this readme

<br />

## **License, Stats, Author 📜**

<img align="right" alt="example image tag" src="https://i.imgur.com/ZHnNGeO.png" width="200" />

<!-- badge cluster -->
![PyPI - License](https://img.shields.io/pypi/l/sleepyconvert?style=plastic)
![PyPI - Version](https://img.shields.io/pypi/v/sleepyconvert)
![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/convert)
<!-- / -->

See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*. \
👉 [GitHub](https://github.com/anthonybench/convert) \
👉 [PyPI](https://pypi.org/project/sleepyconvert/)