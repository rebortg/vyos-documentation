import re
import json
from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective

from testcoverage import get_working_commands

def setup(app):

    app.add_config_value(
        'vyos_phabricator_url',
        'https://phabricator.vyos.net/',
        'html'
    )

    app.add_config_value(
        'vyos_working_commands',
        get_working_commands(),
        'html'
    )
    app.add_config_value(
        'vyos_coverage',
        {
            'cfgcmd': [0,len(app.config.vyos_working_commands['cfgcmd'])],
            'opcmd': [0,len(app.config.vyos_working_commands['opcmd'])]
        },
        'html'
    )

    app.add_role('vytask', vytask_role)
    app.add_role('cfgcmd', cmd_role)
    app.add_role('opcmd', cmd_role)

    app.add_node(
        inlinecmd,
        html=(inlinecmd.visit_span, inlinecmd.depart_span),
        latex=(inlinecmd.visit_tex, inlinecmd.depart_tex),
        text=(inlinecmd.visit_span, inlinecmd.depart_span)
    )

    app.add_node(
        CmdDiv,
        html=(CmdDiv.visit_div, CmdDiv.depart_div),
        latex=(CmdDiv.visit_tex, CmdDiv.depart_tex),
        text=(CmdDiv.visit_div, CmdDiv.depart_div)
    )
    app.add_node(
        CmdBody,
        html=(CmdBody.visit_div, CmdBody.depart_div),
        latex=(CmdBody.visit_tex, CmdBody.depart_tex),
        text=(CmdBody.visit_div, CmdBody.depart_div)
    )
    app.add_node(
        CmdHeader,
        html=(CmdHeader.visit_div, CmdHeader.depart_div),
        latex=(CmdHeader.tex, CmdHeader.tex),
        text=(CmdHeader.visit_div, CmdHeader.depart_div)
    )
    app.add_node(CfgcmdList)
    app.add_node(CfgcmdListCoverage)
    app.add_directive('cfgcmdlist', CfgcmdlistDirective)

    app.add_node(OpcmdList)
    app.add_node(OpcmdListCoverage)
    app.add_directive('opcmdlist', OpcmdlistDirective)

    app.add_directive('cfgcmd', CfgCmdDirective)
    app.add_directive('opcmd', OpCmdDirective)
    app.connect('doctree-resolved', process_cmd_nodes)



class CfgcmdList(nodes.General, nodes.Element):
    pass

class OpcmdList(nodes.General, nodes.Element):
    pass

class CfgcmdListCoverage(nodes.General, nodes.Element):
    pass

class OpcmdListCoverage(nodes.General, nodes.Element):
    pass

class CmdHeader(nodes.General, nodes.Element):

    @staticmethod
    def visit_div(self, node):
        self.body.append(self.starttag(node, 'div'))

    @staticmethod
    def depart_div(self, node=None):
        # self.body.append('</div>\n')
        self.body.append('<a class="cmdlink" href="#%s" ' %
                        node.children[0]['refid'] +
                        'title="%s"></a></div>' % (
                        'Permalink to this Command'))

    @staticmethod
    def tex(self, node=None):
        pass


class CmdDiv(nodes.General, nodes.Element):

    @staticmethod
    def visit_div(self, node):
        self.body.append(self.starttag(node, 'div'))

    @staticmethod
    def depart_div(self, node=None):
        self.body.append('</div>\n')

    @staticmethod
    def tex(self, node=None):
        pass

    @staticmethod
    def visit_tex(self, node=None):
        self.body.append('\n\n\\begin{changemargin}{0cm}{0cm}\n')

    @staticmethod
    def depart_tex(self, node=None):
        self.body.append('\n\\end{changemargin}\n\n')

class CmdBody(nodes.General, nodes.Element):

    @staticmethod
    def visit_div(self, node):
        self.body.append(self.starttag(node, 'div'))

    @staticmethod
    def depart_div(self, node=None):
        self.body.append('</div>\n')

    @staticmethod
    def visit_tex(self, node=None):
        self.body.append('\n\n\\begin{changemargin}{0.5cm}{0.5cm}\n')


    @staticmethod
    def depart_tex(self, node=None):
        self.body.append('\n\\end{changemargin}\n\n')


    @staticmethod
    def tex(self, node=None):
        pass


class inlinecmd(nodes.inline):

    @staticmethod
    def visit_span(self, node):
        self.body.append(self.starttag(node, 'span'))

    @staticmethod
    def depart_span(self, node=None):
        self.body.append('</span>\n')

    @staticmethod
    def visit_tex(self, node=None):
        self.body.append(r'\sphinxbfcode{\sphinxupquote{')
        #self.literal_whitespace += 1

    @staticmethod
    def depart_tex(self, node=None):
        self.body.append(r'}}')
        #self.literal_whitespace -= 1


class CfgcmdlistDirective(Directive):
    has_content = False
    required_arguments = 0
    option_spec = {
        'show-coverage': directives.flag
    }

    def run(self):
        cfglist = CfgcmdList()
        cfglist['coverage'] = False
        if 'show-coverage' in self.options:
            cfglist['coverage'] = True
        return [cfglist]


class OpcmdlistDirective(Directive):
    has_content = False
    required_arguments = 0
    option_spec = {
        'show-coverage': directives.flag
    }

    def run(self):
        oplist = OpcmdList()
        oplist['coverage'] = False
        if 'show-coverage' in self.options:
            oplist['coverage'] = True
            
        return [oplist]



class CmdDirective(SphinxDirective):

    has_content = True
    custom_class = ''

    def run(self):


        

        title_list = []
        content_list = []
        title_text = ''
        content_text = ''
        has_body = False

        cfgmode = self.custom_class + "cmd"

        if '' in self.content:
            index = self.content.index('')
            title_list = self.content[0:index]
            content_list = self.content[index + 1:]
            title_text = ' '.join(title_list)
            content_text = '\n'.join(content_list)
            has_body = True
        else:
            title_text = ' '.join(self.content)
        
        if self.env.docname == 'cli':
            print(self.env.docname)
            print(self.env.metadata)
            print(dir(self.content))
            print(title_text)

        anchor_id = nodes.make_id(self.custom_class + "cmd-" + title_text)
        target = nodes.target(ids=[anchor_id])

        panel_name = 'cmd-{}'.format(self.custom_class)
        panel_element = CmdDiv()
        panel_element['classes'] += ['cmd', panel_name]

        heading_element = CmdHeader(title_text)
        title_nodes, messages = self.state.inline_text(title_text,
                                                       self.lineno)

        title = inlinecmd(title_text, '', *title_nodes)
        target['classes'] += []
        title['classes'] += [cfgmode]
        heading_element.append(target)
        heading_element.append(title)

        heading_element['classes'] += [self.custom_class + 'cmd-heading']

        panel_element.append(heading_element)

        append_list = {
            'docname': self.env.docname,
            'cmdnode': title.deepcopy(),
            'cmd': title_text,
            'target': target,
        }

        if cfgmode == 'opcmd':
            if not hasattr(self.env, "vyos_opcmd"):
                self.env.vyos_opcmd = []
            self.env.vyos_opcmd.append(append_list)

        if cfgmode == 'cfgcmd':
            if not hasattr(self.env, "vyos_cfgcmd"):
                self.env.vyos_cfgcmd = []
            self.env.vyos_cfgcmd.append(append_list)

        if has_body:
            body_element = CmdBody(content_text)
            self.state.nested_parse(
                content_list,
                self.content_offset,
                body_element
            )

            body_element['classes'] += [self.custom_class + 'cmd-body']
            panel_element.append(body_element)
        return [panel_element]


class OpCmdDirective(CmdDirective):
    custom_class = 'op'


class CfgCmdDirective(CmdDirective):
    custom_class = 'cfg'


def strip_cmd(cmd):
    #cmd = re.sub('set','',cmd)
    cmd = re.sub('\s\|\s','',cmd)
    cmd = re.sub('<\S*>','',cmd)
    cmd = re.sub('\[\S\]','',cmd)
    cmd = re.sub('\s+','',cmd)
    return cmd

def build_row(app, fromdocname, rowdata):
    row = nodes.row()
    for cell in rowdata:
        entry = nodes.entry()
        row += entry
        if isinstance(cell, list):
            for item in cell:
                if isinstance(item, dict):
                    entry += process_cmd_node(app, item, fromdocname, '')
                else:
                    entry += nodes.paragraph(text=item)
        elif isinstance(cell, bool):
            if cell:
                entry += nodes.paragraph(text="")
                entry['classes'] = ['coverage-ok']
            else:
                entry += nodes.paragraph(text="")
                entry['classes'] = ['coverage-fail']
        else:
            entry += nodes.paragraph(text=cell)
    return row



def process_coverage(app, fromdocname, doccmd, xmlcmd, cli_type):
    coverage_list = {}
    int_docs = 0
    int_xml = 0
    for cmd in doccmd:
        coverage_item = {
            'doccmd': None,
            'xmlcmd': None,
            'doccmd_item': None,
            'xmlcmd_item': None,
            'indocs': False,
            'inxml': False,
            'xmlfilename': None
        }
        coverage_item['doccmd'] = cmd['cmd']
        coverage_item['doccmd_item'] = cmd
        coverage_item['indocs'] = True
        int_docs += 1
        coverage_list[strip_cmd(cmd['cmd'])] = dict(coverage_item)
    
    for cmd in xmlcmd:
        
        strip = strip_cmd(cmd['cmd'])
        if strip not in coverage_list.keys():
            coverage_item = {
                'doccmd': None,
                'xmlcmd': None,
                'doccmd_item': None,
                'xmlcmd_item': None,
                'indocs': False,
                'inxml': False,
                'xmlfilename': None
            }
            coverage_item['xmlcmd'] = cmd['cmd']
            coverage_item['xmlcmd_item'] = cmd
            coverage_item['inxml'] = True
            coverage_item['xmlfilename'] = cmd['filename']
            int_xml += 1
            coverage_list[strip] = dict(coverage_item)
        else:
            #print("===BEGIN===")
            #print(cmd)
            #print(coverage_list[strip])
            #print(strip)
            #print("===END====")
            coverage_list[strip]['xmlcmd'] = cmd['cmd']
            coverage_list[strip]['xmlcmd_item'] = cmd
            coverage_list[strip]['inxml'] = True
            coverage_list[strip]['xmlfilename'] = cmd['filename']
            int_xml += 1


    

    table = nodes.table()
    tgroup = nodes.tgroup(cols=3)
    table += tgroup

    header = (f'{int_docs}/{len(coverage_list)} in Docs', f'{int_xml}/{len(coverage_list)} in XML', 'Command')
    colwidths = (1, 1, 8)
    table = nodes.table()
    tgroup = nodes.tgroup(cols=len(header))
    table += tgroup
    for colwidth in colwidths:
        tgroup += nodes.colspec(colwidth=colwidth)
    thead = nodes.thead()
    tgroup += thead
    thead += build_row(app, fromdocname, header)
    tbody = nodes.tbody()
    tgroup += tbody
    for entry in sorted(coverage_list):
        body_text_list = []
        if coverage_list[entry]['indocs']:
            body_text_list.append(coverage_list[entry]['doccmd_item'])
        else:
            body_text_list.append('Not documented yet')

        if coverage_list[entry]['inxml']:
            body_text_list.append("------------------")
            body_text_list.append(str(coverage_list[entry]['xmlfilename']) + ":")
            body_text_list.append(coverage_list[entry]['xmlcmd'])
        else:
            body_text_list.append('Nothing found in XML Definitions')

            
        tbody += build_row(app, fromdocname, 
            (
                coverage_list[entry]['indocs'],
                coverage_list[entry]['inxml'],
                body_text_list
            )
        )

    return table

def process_cmd_node(app, cmd, fromdocname, cli_type):
    para = nodes.paragraph()
    newnode = nodes.reference('', '')
    innernode = cmd['cmdnode']
    newnode['refdocname'] = cmd['docname']
    newnode['refuri'] = app.builder.get_relative_uri(
        fromdocname, cmd['docname'])
    newnode['refuri'] += '#' + cmd['target']['refid']
    newnode['classes'] += ['cmdlink']
    newnode.append(innernode)
    para += newnode
    return para


def process_cmd_nodes(app, doctree, fromdocname):
    try:
        env = app.builder.env
        
        for node in doctree.traverse(CfgcmdList):
            content = []
            if node.attributes['coverage']:
                node.replace_self(
                    process_coverage(
                        app,
                        fromdocname,
                        env.vyos_cfgcmd,
                        app.config.vyos_working_commands['cfgcmd'],
                        'cfgcmd'
                        )
                    )
            else:
                for cmd in sorted(env.vyos_cfgcmd, key=lambda i: i['cmd']):
                    content.append(process_cmd_node(app, cmd, fromdocname, 'cfgcmd'))                
                node.replace_self(content)
            
        for node in doctree.traverse(OpcmdList):
            content = []
            if node.attributes['coverage']:
                node.replace_self(
                    process_coverage(
                        app,
                        fromdocname,
                        env.vyos_opcmd,
                        app.config.vyos_working_commands['opcmd'],
                        'opcmd'
                        )
                    )
            else:
                for cmd in sorted(env.vyos_opcmd, key=lambda i: i['cmd']):
                    content.append(process_cmd_node(app, cmd, fromdocname, 'opcmd'))
                node.replace_self(content)

    except Exception as inst:
        print(inst)


def vytask_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    app = inliner.document.settings.env.app
    base = app.config.vyos_phabricator_url
    ref = base + str(text)
    set_classes(options)
    node = nodes.reference(
        rawtext, utils.unescape(str(text)), refuri=ref, **options)
    return [node], []


def cmd_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.literal(text, text)
    return [node], []