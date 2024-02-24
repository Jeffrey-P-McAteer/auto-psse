#!/usr/bin/env python

import os
import sys
import subprocess
import shutil

def cmd(*args, **kwargs):
  if not 'check' in kwargs:
    kwargs['check'] = True
  cmd = [x for x in args if not x is None]
  print(f'> {" ".join(cmd)}')
  subprocess.run(cmd, **kwargs)


def ensure_intel_fortran_avail():
  #install_sh_url = 'https://registrationcenter-download.intel.com/akdlm/IRC_NAS/163da6e4-56eb-4948-aba3-debcec61c064/l_BaseKit_p_2024.0.1.46_offline.sh'
  # /j/downloads/l_BaseKit_p_2024.0.1.46_offline.sh -f $PWD/intel -r no -a --silent --cli --eula accept --action install --install-dir $PWD/intel --download-cache /tmp --download-dir /tmp
  # ./intel/l_BaseKit_p_2024.0.1.46_offline/install.sh --cli --silent --eula accept --action install --install-dir $PWD/intel --download-cache /tmp --download-dir /tmp

  # TODO auto-install logic


  os.environ['PATH'] = os.path.abspath(os.path.join('intel2', '2024.0', 'bin'))+os.pathsep+os.environ['PATH']
  if not shutil.which('ifx'):
    raise Exception('Please download the intel HPC kit and ensure ifx is on your PATH')


def main(args=sys.argv):
  os.makedirs('bin', exist_ok=True)

  ensure_intel_fortran_avail()

  main_bin = os.path.abspath(os.path.join('bin', 'main'))
  alib_bin = os.path.abspath(os.path.join('bin', 'alib'))
  warning_args = [
    '-warn', 'all',
    '-check', 'all',
    '-g', '-traceback',
  ]

  cmd('ifx', *warning_args, '-o', alib_bin, '-shared', 'alib.f90')

  cmd('ifx', *warning_args, '-o', main_bin, 'main.f90', '-Bstatic', alib_bin)

  cmd(main_bin, '')



if __name__ == '__main__':
  main()
