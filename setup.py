import sys
import utils
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
  packages = ['lxml', 'lxml._elementpath', 'gzip'], excludes = [],
  include_files = ['resources'],
)

executables = [
    Executable('bams.py', base = 'Win32GUI', targetName = 'bams.exe',
               icon = 'bams.ico', compress = True),
    Executable('bams-cmd.py', base = 'Console', targetName = 'bams-cmd.exe',
               compress = True),
]

setup(name='BAMS',
      version = utils.__version__,
      description = 'BAMS is used for managing bank accounts',
      options = dict(build_exe = buildOptions),
      executables = executables)
