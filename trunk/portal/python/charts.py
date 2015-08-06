# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import xml_memory
import xml_cpu

urls = (
        '/', 'Charts'
)

render_charts = web.template.render('templates', cache=False)

class Charts:
    def GET(self):
        '''
        Renders the charts template.
        '''
        memory_xml = xml_memory.get_memory()
        cpu_xml = xml_cpu.get_cpu()
        return render_charts.charts(memory_xml, cpu_xml)

app_charts = web.application(urls, locals())