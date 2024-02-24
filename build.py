#!/usr/bin/env python

import os
import sys
import subprocess
import shutil
import traceback

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

def ostyped(linux_val, windorks_val):
  if os.name == 'nt':
    return windorks_val
  return linux_val

def main(args=sys.argv):
  os.makedirs('bin', exist_ok=True)

  ensure_intel_fortran_avail()

  main_bin = os.path.abspath(os.path.join('bin', 'main'))+ostyped('', '.exe')
  alib_dynamic_bin = os.path.abspath(os.path.join('bin', 'alib'))+ostyped('.so', '.dll')
  alib_static_bin = os.path.abspath(os.path.join('bin', 'alib'))+ostyped('.a', '.lib')
  alib_static_obj = os.path.abspath(os.path.join('bin', 'alib'))+ostyped('.o', '.o')

  warning_args = [
    '-warn', 'all',
    '-check', 'all',
    '-g', '-traceback',
  ]

  cmd('ifx', *warning_args, '-o', alib_dynamic_bin, '-shared', '-fpic', 'alib.f90')

  cmd('ifx', *warning_args, '-c', '-Fo'+alib_static_obj, '-fpie', '-fpic', 'alib.f90')
  cmd('ar', 'cr', alib_static_bin, alib_static_obj)

  cmd('ifx', *warning_args, '-o', main_bin, 'main.f90', '-Bstatic', alib_static_bin)

  cmd(main_bin, *args[1:])



if __name__ == '__main__':
  try:
    main()
  except:
    if not 'CalledProcessError' in traceback.format_exc():
      traceback.print_exc()
