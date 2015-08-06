'''
Created on Jul 21, 2012

@author: autumn
'''

class OutputFormatter():
    def __init__(self, data, title, width, cmd = ""):
        self.data = data
        self.title = title
        self.width = width
        self.cmd = cmd
        
    def __normalize_linestr__(self, orig_line, new_lines, width):
        persition = 0
        while persition < len(orig_line):
            new_lines.append(orig_line[persition:persition+width])
            persition += width
        
    def __format_line__(self, data_line):
        
        ret_lines = []
        
        line = []
        for i in range(len(data_line)):
            column = []
            orig_col = data_line[i]
            tmplist = orig_col.split('\n')
            for col in tmplist:
                self.__normalize_linestr__(col, column, self.width[i])
            
            line.append(column)
        
        numboflines = max([len(c) for c in line])
        
        for i in range(numboflines):
            this_line = ''
            for j in range(len(line)):
                col = line[j]
                #print "col : %r [%d : %d]" % (col, i, j)
                if i < len(col):
                    cell = col[i]
                    #print "[cell] %r" % cell
                    this_line += cell.ljust(self.width[j], ' ')
                else:
                    this_line += ' '.ljust(self.width[j], ' ')
    
            ret_lines.append(this_line)
            
        return ret_lines
            
    
    def print_dict(self):
        
        printlines = []
        printlines.append("*" * sum(self.width))
        if len(self.cmd) > 0:
            printlines.append("Command : %s" % self.cmd)
        printlines.append(''.join([t.ljust(w) for t, w in zip(self.title, self.width)]))
        printlines.append(''.join([' '.rjust(w, '-') for w in self.width]))
        
        for l in self.data:
            #print "%r" % l
            ret_lines = self.__format_line__(l)
            for line in ret_lines:
                printlines.append(line)
            del ret_lines
        
        printlines.append("*" * sum(self.width))
        printlines.append("\n")
        
        ######################################
        # Print out
        for line in printlines:
            print "%s" % (line)

        del printlines
        
    
###############################################
## For testing
##    

from swiftconsole.common.utils import exec_command

if __name__ == '__main__':
    data = []
    cmd = "salt 'ciswift001.webex.com' puppet.run"
    retcode, output, errors, interval = exec_command([cmd])
   
    tmplist = output.split(':', 1)
    node = tmplist[0]
    obj = eval(tmplist[1])
    msg = obj['stdout']
        
    line1 = [node, str(retcode), msg]
    data.append(line1)
    
    title = ['node', 'status', 'message']
    width = (30, 7, 60)
    
    formatter = OutputFormatter(data,title, width)
    formatter.print_dict()
    