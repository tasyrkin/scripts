'''
The script automatically remaps jre executables pointing from /usr/bin/<binary_name> -> /System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/<binary_name>
to their jdk counterparts: /System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home/bin/<binary_name>
'''
import subprocess

usr_bin = '/usr/bin/'
old_dir = '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/'
new_dir = '/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home/bin/'

command = 'ls -laF {} | grep {}'.format(usr_bin, old_dir)

proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#reading all lines from the subprocess, therefore blocking until the subprocess is finished
split_lines = map(lambda line: line.split(), proc.stdout.readlines())

split_lines_flat = [lpart for sublist in split_lines for lpart in sublist]

names = map(lambda lpart: lpart.replace('@', ''), filter(lambda lpart: lpart.endswith('@'), split_lines_flat))

retval = proc.wait()

if len(names) > 0:
  print 'found commands to process:'
  print str(map(lambda name: '{}{}'.format(usr_bin, name), names))
else:
  print 'nothing to process, exiting'
  exit()

not_found = []

for name in names:
  p = subprocess.Popen('ls -laF {}{}'.format(new_dir, name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  retval = p.wait()
  if retval != 0:
    not_found.append(name)

if len(not_found) > 0:
  print 'unable to find following commands in JDK:'
  print str(not_found)
  exit()

not_unlinked = []
not_linked = []

for name in names:
  p = subprocess.Popen('rm -f {}{}'.format(usr_bin, name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  retval = p.wait()
  if retval != 0:
    not_unlinked.append(name)
  else:
    p_link = subprocess.Popen('ln -s {}{} {}{}'.format(new_dir, name, usr_bin, name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval_link = p_link.wait()
    if retval_link != 0:
      not_linked.append(name)

if len(not_unlinked) > 0:
  print 'unable to unlink following commands:'
  print map(lambda name: '{}{}'.format(usr_bin, name), sorted(not_unlinked))

if len(not_linked) > 0:
  print 'unable to link following commands:'
  print map(lambda name: '{}{}'.format(usr_bin, name), sorted(not_linked))

if len(not_unlinked) == 0 and len(not_linked) == 0:
  print 'sucessfully migrated java commands:'
  print map(lambda name: '{}{}'.format(new_dir, name), names)
