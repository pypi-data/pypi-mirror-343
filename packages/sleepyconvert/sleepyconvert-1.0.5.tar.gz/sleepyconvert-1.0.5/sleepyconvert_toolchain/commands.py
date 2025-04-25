from sys import exit
from rich import print
import typer
from sleepyconvert_toolchain.params import *
from sleepyconvert_toolchain.utils import *

app = typer.Typer(help="Convert common filetypes and data formats quickly.")


@app.command()
def data(input_path:str, output_path:str, compress:bool=False):
  '''Convert data file from one format to another, optionally compressing output'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_data_formats)
  if not (input_format and output_format):
    exit(1)
    
  # additional guards
  if compress and output_format == 'xlsx':
    errorMessage('Cannot compress xlsx files. Please remove the --compress flag.')
    exit(1)

  # read
  try:
    df = readData(input_format, input_path)
  except Exception as e:
    errorMessage(f'Error reading data:\n{e}')
    exit(1)

  # write
  try:
    writeData(df, output_format, output_path, compress)
  except Exception as e:
    errorMessage(f'Error writing data:\n{e}')
    exit(1)

  # log
  output_path_display = f'{output_path}.gz' if compress else output_path
  successMessage(input_path, output_path_display, compress)
  exit(0)


@app.command()
def img(input_path:str, output_path:str):
  '''Convert image file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_img_formats)
  if not (input_format and output_format):
    exit(1)

  # write
    try:
      match (input_format, output_format):
        case ('png', 'jpg'|'jpeg'):
          convertPNGtoJPG(input_path, output_path)
        case ('jpg'|'jpeg', 'png'):
          convertJPGtoPNG(input_path, output_path)
    except Exception as e:
      errorMessage(f'Error converting {input_format} to {output_format}:\n{e}')
      exit(1)

  # log
  successMessage(input_path, output_path, compress=False)
  exit(0)


@app.command()
def doc(input_path:str, output_path:str):
  '''Convert document file from one format to another'''
  input_format, output_format = verifyPaths(input_path, output_path, supported_doc_formats)
  if not (input_format and output_format):
    exit(1)

  # write
  try:
    match (input_format, output_format):
      case ('html', 'pdf'):
        convertHTMLtoPDF(input_path, output_path)
      case ('pdf', 'html'):
        convertPDFtoHTML(input_path, output_path)
      case ('md', 'pdf'):
        convertMDtoPDF(input_path, output_path)
      case ('pdf', 'md'):
        convertPDFtoMD(input_path, output_path)
      case ('html', 'md'):
        convertHTMLtoMD(input_path, output_path)
      case ('md', 'html'):
        convertMDtoHTML(input_path, output_path)
  except Exception as e:
    errorMessage(f'Error converting {input_path} to {output_path}:\n{e}')
    exit(1)

  # log
  successMessage(input_path, output_path, compress=False)
  exit(0)
