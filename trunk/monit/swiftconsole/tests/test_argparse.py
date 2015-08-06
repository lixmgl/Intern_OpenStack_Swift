'''
Created on Jul 19, 2012

@author: autumn
'''

import sys
import argparse
import swiftconsole.ui.commands as commands

cmd_parser = argparse.ArgumentParser(description='Swift console')
cmd_parser.add_argument('command', choices = ['show-ring', 'push-config'])

if len(sys.argv) < 2:
    cmd_parser.print_help()
    sys.exit(1)

command = sys.argv[1]
args = sys.argv[2:]

sub_prog = "%s %s" % (sys.argv[0], command)

def run_command(command, *args, **awg):
    cmd = command.replace('-','_')
    try:
        func = commands.__dict__[cmd]
        #if args != None:
        retcode = func(*args, **awg)
        #else:
        #   retcode = func()
        return (retcode, '')
    except Exception as e:
        return (-1, e)

if command == 'show-ring':
    parser = argparse.ArgumentParser(description="Show ring config", prog=sub_prog)
    parser.add_argument('-n', '--name', choices = ['object', 'container', 'account'], required=True)
    ret = parser.parse_args(args)    

    run_command(command, ret.name)
    
elif command == 'push-config':
    parser = argparse.ArgumentParser(description="Show ring config", prog=sub_prog)
    parser.add_argument('-t', '--nodetype', choices = ['storage', 'proxy'], required=True)
    ret = parser.parse_args(args)
    #print "%r" % ret
    run_command(command, ret.nodetype)
    
elif command in ['-h', '--help']:
    cmd_parser.print_help()
    
else:
    print "Not supported command."
    

########################################################
## For testing    
def foo(hello, *args, **kw):
    print hello

    for each in args:
        print each
        
    for each in kw:
        print "%r" % each

if __name__ == '__main__':
    foo("LOVE", ["lol", "lololol"])





"""
base_parser_show_ring = argparse.ArgumentParser(description='Show ring configuration', add_help=False)
base_parser_show_ring.add_argument("show-ring", type=str)

base_parser_push_cfg = argparse.ArgumentParser(description='Push configuration to swift servers')
base_parser_push_cfg.add_argument("push-config", type=str)

parser_ring = argparse.ArgumentParser(parents=[base_parser_show_ring])
parser_ring.add_argument("-n", "--ringname", choices = ['object', 'container', 'account'])
parser_ring

base_parser_show_ring.print_help()


print "============================================================"

parser_ring.print_help()
"""