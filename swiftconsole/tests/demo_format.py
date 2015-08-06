'''
Created on Jul 20, 2012

@author: autumn
'''

class OutputFormatter():
    def __init__(self, data, title, width):
        self.data = data
        self.title = title
        self.width = width
        
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
        printlines.append(''.join([t.ljust(w) for t, w in zip(self.title, self.width)]))
        printlines.append(''.join([' '.rjust(w, '=') for w in self.width]))
        
        for l in self.data:
            #print "%r" % l
            ret_lines = self.__format_line__(l)
            for line in ret_lines:
                printlines.append(line)
            del ret_lines
        
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
    #print "retcode : %d \noutput: \n%r" % (retcode, output)
    
    tmplist = output.split(':', 1)
    node = tmplist[0]
    obj = eval(tmplist[1])
    msg = obj['stdout']
    
    #print "node : %s " % node
    #print "obj : %r" % obj
    #for k, v in obj.iteritems():
    #    print "%s : %s" % (k, str(v))
        
    line1 = [node, str(retcode), msg]
    data.append(line1)
    
    """
    line1 = ['ciswift001.webex.com', 'storagenode', 'running']
    data.append(line1)
    
    line2 = ['ciswift002.webex.com', 'storagenode', 'running']
    data.append(line2)
    
    line3 = ['ciswift003.webex.com', 'proxy', 'stopped']
    data.append(line3)
    """
    
    title = ['node', 'status', 'message']
    width = (30, 7, 60)
    
    formatter = OutputFormatter(data,title, width)
    formatter.print_dict()
    
    
        
        
    






