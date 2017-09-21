''' Converts a simplified configuration file to a full configuration file
''' 

import sys, os
import json
import xmltodict
import re

from docutils import nodes, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, states
from collections import OrderedDict
from docutils.core import publish_parts
from optparse import OptionParser
from ODSA_Config import read_conf_file

mod_options = None
ex_options = None
ex_module = {} # map exercise names to modules
sect_options = None
default_ex_options = {
    "ka": {
      "required": True,
      "points": 1,
      "threshold": 5
    }, 
    "ss": {
      "required": False,
      "points": 0,
      "threshold": 1
    }, 
    "pe": {
      "required": True,
      "points": 1,
      "threshold": 0.9
    },
    "dgm": {
      "required": False,
      "points": 0,
      "threshold": 1
    }
}

EXERCISE_FIELDS = ['points', 'required', 'long_name', 'threshold', 'exer_options']
MODULE_FIELDS = ['dispModComp', 'mod_options', 'codeinclude']

avembed_element = '''\
<avembed
    type="%(type)s"
    exer_name="%(exer_name)s"
    long_name="%(long_name)s"
    points="%(points)s"
    required="True"
    threshold="%(threshold)s">
</avembed>
'''

extertool_element = '''\
<extertool
    resource_name=%(resource_name)s
    resource_type="%(resource_type)s"
    learning_tool="%(learning_tool)s"
    points="%(points)s">
</extertool>
'''

inlineav_element = '''\
<inlineav
    type="%(type)s"
    exer_name="%(exer_name)s"
    long_name="%(long_name)s"
    points="%(points)s"
    output="%(output)s"
    required="True"
    threshold="%(threshold)s">
</inlineav>
'''

odsalink_element = '''<odsalink>%(odsalink)s</odsalink>'''
odsascript_element = '''<odsascript>%(odsascript)s</odsascript>'''


class avembed(Directive):
  required_arguments = 2
  optional_arguments = 1
  final_argument_whitespace = True
  option_spec = {
                  'long_name': directives.unchanged
                }
  has_content = True


  def run(self):
    """ Restructured text extension for inserting embedded AVs with show/hide button """
    av_path = self.arguments[0]
    self.options['type'] = self.arguments[1]
    self.options['exer_name'] = os.path.basename(av_path).partition('.')[0]

    self.options['required'] = default_ex_options[self.options['type']]['required']
    self.options['points'] = default_ex_options[self.options['type']]['points']
    self.options['threshold'] = default_ex_options[self.options['type']]['threshold']

    if self.options['exer_name'] in ex_options:
      for key, value in ex_options[self.options['exer_name']].iteritems():
        self.options[key] = value
      #del ex_options[self.options['exer_name']]

    if 'long_name' not in self.options:
      self.options['long_name'] = self.options['exer_name']

    res = avembed_element % (self.options)

    return [nodes.raw('', res, format='xml')]


class avmetadata(Directive):
  '''
  '''
  required_arguments = 0
  optional_arguments = 8
  final_argument_whitespace = True
  has_content = True
  option_spec = {'author':directives.unchanged,
                 'topic': directives.unchanged,
                 'requires': directives.unchanged,
                 'satisfies': directives.unchanged,
                 'prerequisites': directives.unchanged
                 }

  def run(self):
      """ Restructured text extension for collecting  AVs metadata nothing is written in the output html file """
      return [nodes.raw('', '<avmetadata>null</avmetadata>', format='xml')]


odsalink_element = '''<odsalink>%(odsalink)s</odsalink>'''
odsascript_element = '''<odsascript>%(odsascript)s</odsascript>'''


class extrtoolembed(Directive):
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  has_content = True
  option_spec = {
                 'resource_name': directives.unchanged,
                 'resource_type': directives.unchanged,
                 'learning_tool': directives.unchanged,
                 'points': directives.unchanged
                 }

  def run(self):

    resource_name = self.arguments[0]
    if 'resource_name' not in self.options or self.options['resource_name'] == '':
      self.options['resource_name'] = resource_name
    if 'resource_type' not in self.options or self.options['resource_type'] == '':
      self.options['resource_type'] = 'external_assignment'
    if 'learning_tool' not in self.options or self.options['learning_tool'] == '':
      self.options['learning_tool'] = 'code-workout'
    if 'points' not in self.options or self.options['points'] == '':
      self.options['points'] = 2.0

    res = extertool_element % (self.options)
    return [nodes.raw('', res, format='xml')]


class inlineav(Directive):
  required_arguments = 2
  optional_arguments = 6
  final_argument_whitespace = True
  option_spec = {
                  'long_name': directives.unchanged,
                  'output': directives.unchanged,
                  'align': directives.unchanged,
                  'points': directives.unchanged,
                  'required': directives.unchanged,
                  'threshold': directives.unchanged
                }
  has_content = True


  def run(self):
    """ Restructured text extension for including inline JSAV content on module pages """
    self.options['exer_name'] = self.arguments[0]
    self.options['type'] = self.arguments[1]

    self.options['required'] = default_ex_options[self.options['type']]['required']
    self.options['points'] = default_ex_options[self.options['type']]['points']
    self.options['threshold'] = default_ex_options[self.options['type']]['threshold']

    if self.options['exer_name'] in ex_options:
        for key, value in ex_options[self.options['exer_name']].iteritems():
            self.options[key] = value
        #del ex_options[self.options['exer_name']]

    if 'long_name' not in self.options:
      self.options['long_name'] = self.options['exer_name']

    self.options['align'] = None
    self.options['output'] = None

    res = inlineav_element % (self.options)
    return [nodes.raw('', res, format='xml')]


class odsalink(Directive):
  '''
  '''
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  option_spec = {}

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    self.options['odsalink'] = self.arguments[0]
    res = odsalink_element % (self.options)
    return [nodes.raw('', res, format='xml')]


class odsascript(Directive):
  '''
  '''
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  option_spec = {}

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    self.options['odsascript'] = self.arguments[0]
    res = odsascript_element % (self.options)
    return [nodes.raw('', res, format='xml')]


class index(Directive):
  '''
  '''
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  option_spec = {}

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    return [nodes.raw('', '<index>null</index>', format='xml')]


class codeinclude(Directive):
  '''
  '''
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  option_spec = {}

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    return [nodes.raw('', '<codeinclude>null</codeinclude>', format='xml')]


class todo(Directive):
  '''
  '''
  required_arguments = 0
  optional_arguments = 3
  final_argument_whitespace = True
  has_content = True
  option_spec = {
                'type': directives.unchanged,
                'tag': directives.unchanged
                }

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    return [nodes.raw('', '<todo>null</todo>', format='xml')]


class glossary(Directive):
  '''
  '''
  required_arguments = 0
  optional_arguments = 3
  final_argument_whitespace = True
  has_content = True
  option_spec = {
                'sorted': directives.unchanged
                }

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    return [nodes.raw('', '<glossary>null</glossary>', format='xml')]


class only(Directive):
  '''
  '''
  required_arguments = 1
  optional_arguments = 0
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  has_content = True

  def run(self):
    # """ Restructured text extension for including CSS and other libraries """
    return [nodes.raw('', '<only>null</only>', format='xml')]


class odsafig(Directive):
  '''
  '''
  required_arguments = 0
  optional_arguments = 9
  final_argument_whitespace = True
  has_content = True
  option_spec = {
                'figwidth_value': directives.unchanged,
                'figclass': directives.unchanged,
                'align': directives.unchanged,
                'capalign': directives.unchanged,
                'figwidth': directives.unchanged,
                'alt': directives.unchanged,
                'scale': directives.unchanged,
                'width': directives.unchanged,
                'height': directives.unchanged
                }

  has_content = True

  def run(self):
    return [nodes.raw('', '<odsafig>null</odsafig>', format='xml')]

def print_err(err_msg):
  '''
  '''
  sys.stderr.write('%s\n' % err_msg)

def extract_mod_config(mod_json):
  '''
  '''
  # validate mod_json
  mod_config = {}
  mod_config['long_name'] = ""
  mod_config['sections'] = OrderedDict()
  one_sec_only = False
  one_sec_name = None

  for k, v in mod_json['document'].iteritems():
    if k == '@title':
      mod_config['long_name'] = v.replace('\\','')

    # 'subtitle' is used when the rst file contains only one section
    if k == 'subtitle':
      one_sec_only = True
      one_sec_name = v['#text']
      mod_config['sections'][one_sec_name] = OrderedDict()

    # The rst file contains only one section and all exercises are defined
    # directly under this section
    if k == 'raw' and one_sec_only == True:
      mod_config['sections'][one_sec_name] = extract_exs_config(v)

    # The rst file contains only one section which has in one or more subsections
    if k == 'section' and one_sec_only == True:
      # mod_config['sections'][one_sec_name] = extract_exs_config(v)
      if isinstance(v, list):
        for sub_sec_v in v:
          if 'raw' in sub_sec_v.keys():
            mod_config['sections'][one_sec_name].update(extract_exs_config(sub_sec_v['raw']))

          # Sometimes exercises are defined under a topic directive
          if 'topic' in sub_sec_v.keys() and isinstance(sub_sec_v['topic'], list):
            for topic in sub_sec_v['topic']:
              if 'raw' in topic.keys():
                mod_config['sections'][one_sec_name].update(extract_exs_config(topic['raw']))
          elif 'topic' in sub_sec_v.keys() and isinstance(sub_sec_v['topic'], dict):
              if 'raw' in sub_sec_v['topic'].keys():
                mod_config['sections'][one_sec_name].update(extract_exs_config(sub_sec_v['topic']['raw']))

      elif isinstance(v, dict):
        if 'raw' in v.keys():
          mod_config['sections'][one_sec_name].update(extract_exs_config(v['raw']))

    if k == 'section' and one_sec_only == False:
      mod_config['sections'] = extract_sec_config(v)


  return mod_config


def extract_sec_config(sec_json):
  '''
  '''
  sections_config = OrderedDict()
  for x in sec_json:
    sec_title = None
    for k, v in x.iteritems():
      if k == 'title':
        sec_title = v
        sections_config[sec_title] = OrderedDict()

      if k == 'raw':
        sections_config[sec_title].update(extract_exs_config(v))

      if k == 'section':
        if isinstance(v, list):
          for sub_sec_v in v:
            if 'raw' in sub_sec_v.keys():
              sections_config[sec_title].update(extract_exs_config(sub_sec_v['raw']))
        elif isinstance(v, dict):
          if 'raw' in v.keys():
            sections_config[sec_title].update(extract_exs_config(v['raw']))
    if sec_title in sect_options:
      for k, v in sect_options[sec_title].iteritems():
        sections_config[sec_title][k] = v
      del sect_options[sec_title]
    if 'extertool' in sections_config[sec_title].keys():
      sections_config[sec_title] = sections_config[sec_title]['extertool']

  return sections_config


def extract_exs_config(exs_json):
  '''
  '''
  exs_config = OrderedDict()
  if isinstance(exs_json, list):
    for x in exs_json:
      if isinstance(x, dict) and 'avembed' in x.keys():
        ex_obj = x['avembed']
        exer_name = ex_obj['@exer_name']
        exs_config[exer_name] = OrderedDict()
        exs_config[exer_name]['long_name'] = ex_obj['@long_name']
        exs_config[exer_name]['required'] = default_ex_options[ex_obj['@type']]['required']
        exs_config[exer_name]['points'] = float(ex_obj['@points'])
        threshold = float(ex_obj['@threshold'])
        exs_config[exer_name]['threshold'] = threshold if ex_obj['@type'] == 'pe' else int(threshold)

        if exer_name in ex_options:
          for key, value in ex_options[exer_name].iteritems():
              exs_config[exer_name][key] = value
          del ex_options[exer_name]

      if isinstance(x, dict) and 'extertool' in x.keys():
        ex_obj = x['extertool']
        exs_config['extertool'] = OrderedDict()
        exs_config['extertool']['learning_tool'] = ex_obj['@learning_tool']
        exs_config['extertool']['resource_type'] = ex_obj['@resource_type']
        exs_config['extertool']['resource_name'] = ex_obj['@resource_name']
        exs_config['extertool']['points'] = float(ex_obj['@points'])

      if isinstance(x, dict) and 'inlineav' in x.keys() and x['inlineav']['@type'] == "ss":
        ex_obj = x['inlineav']
        exer_name = ex_obj['@exer_name']
        exs_config[exer_name] = OrderedDict()
        exs_config[exer_name]['long_name'] = ex_obj['@long_name']
        exs_config[exer_name]['required'] = default_ex_options[ex_obj['@type']]['required']
        exs_config[exer_name]['points'] = float(ex_obj['@points'])
        exs_config[exer_name]['threshold'] = float(ex_obj['@threshold'])
        if exer_name in ex_options:
          for key, value in ex_options[exer_name].iteritems():
              exs_config[exer_name][key] = value
          del ex_options[exer_name]

      if isinstance(x, dict) and 'inlineav' in x.keys() and x['inlineav']['@type'] == "dgm":
        ex_obj = x['inlineav']
        exer_name = ex_obj['@exer_name']
        exs_config[exer_name] = OrderedDict()
  elif isinstance(exs_json, dict):
    if 'avembed' in exs_json.keys():
      ex_obj = exs_json['avembed']
      exer_name = ex_obj['@exer_name']
      exs_config[exer_name] = OrderedDict()
      exs_config[exer_name]['long_name'] = ex_obj['@long_name']
      exs_config[exer_name]['required'] = default_ex_options[ex_obj['@type']]['required']
      exs_config[exer_name]['points'] = float(ex_obj['@points'])
      threshold = float(ex_obj['@threshold'])
      exs_config[exer_name]['threshold'] = threshold if ex_obj['@type'] == 'pe' else int(threshold)
      if exer_name in ex_options:
          for key, value in ex_options[exer_name].iteritems():
              exs_config[exer_name][key] = value
          del ex_options[exer_name]

    if 'extertool' in exs_json.keys():
      ex_obj = exs_json['extertool']
      exs_config['extertool'] = OrderedDict()
      exs_config['extertool']['learning_tool'] = ex_obj['@learning_tool']
      exs_config['extertool']['resource_type'] = ex_obj['@resource_type']
      exs_config['extertool']['resource_name'] = ex_obj['@resource_name']
      exs_config['extertool']['points'] = float(ex_obj['@points'])

    if 'inlineav' in exs_json.keys() and exs_json['inlineav']['@type'] == "ss":
      ex_obj = exs_json['inlineav']
      exer_name = ex_obj['@exer_name']
      exs_config[exer_name] = OrderedDict()
      exs_config[exer_name]['long_name'] = ex_obj['@long_name']
      exs_config[exer_name]['required'] = default_ex_options[ex_obj['@type']]['required']
      exs_config[exer_name]['points'] = float(ex_obj['@points'])
      exs_config[exer_name]['threshold'] = float(ex_obj['@threshold'])
      if exer_name in ex_options:
          for key, value in ex_options[exer_name].iteritems():
              exs_config[exer_name][key] = value
          del ex_options[exer_name]

    if 'inlineav' in exs_json.keys() and exs_json['inlineav']['@type'] == "dgm":
      ex_obj = exs_json['inlineav']
      exer_name = ex_obj['@exer_name']
      exs_config[exer_name] = OrderedDict()


  return exs_config


def register():
  '''
  '''
  directives.register_directive('avembed',avembed)
  directives.register_directive('avmetadata',avmetadata)
  directives.register_directive('extrtoolembed',extrtoolembed)
  directives.register_directive('inlineav',inlineav)
  directives.register_directive('odsalink',odsalink)
  directives.register_directive('odsascript',odsascript)
  directives.register_directive('index',index)
  directives.register_directive('codeinclude',codeinclude)
  directives.register_directive('todo',todo)
  directives.register_directive('only',only)
  directives.register_directive('glossary',glossary)
  directives.register_directive('odsafig',odsafig)


def remove_markup(source):
  '''
  remove unnecessary markups in the rst files
  '''
  source = source.replace(' --- ','')
  source = source.replace('|---|','')
  source = re.sub(r"\:(?!output)[a-zA-Z]+\:", '',source, flags=re.MULTILINE)
  source = re.sub(r"\[.+\]\_", '',source, flags=re.MULTILINE)

  return source

def get_chapter_module_files(conf_data):
  ''' get a dictionary where the keys are the chapter names and the values are 
      the paths to the rst files of the modules in the chapter
  '''
  files = OrderedDict()
  for chapter, modules in conf_data['chapters'].iteritems():
    files[chapter] = []
    for module in modules.keys():
      files[chapter].append(os.path.join(os.path.abspath('RST/{0}/'.format(conf_data['lang'])), module + ".rst"))
  return files

def get_options(conf_data):
  ''' 
  gets a tuple where: 
    the first item is a dictionary where the keys are the 
      short names of exercises (or sections) and the values are the options that 
      were specified for each exercise
    the second item is a dictionary where the keys are the names of sections and
     the values are options for each section
    the third item is a dictionary where the keys are the names of modules
      and the values are options for each module
  '''
  exercises = {}
  sections = {}
  mod_opts = {}
  for chapter in conf_data['chapters'].values():
    for module, children in chapter.iteritems():
      mod_opts[module] = {}
      if 'sections' in children:
        for section_name, exercise_objs in children['sections'].iteritems():
          sections[section_name] = {}
          for key, value in exercise_objs.iteritems():
              if type(value) is OrderedDict and any(k in EXERCISE_FIELDS for k in value):
                if 'long_name' in value:
                  del value['long_name']
                exercises[key] = value
                ex_module[key] = module
              elif key != 'long_name':
                sections[section_name][key] = value
          if len(sections[section_name]) == 0:
            del sections[section_name]
        del children['sections']

      if 'long_name' in children:
        del children['long_name']
      for key, value in children.iteritems():
        if key in MODULE_FIELDS:  
          mod_options[module][key] = value
        elif any(k in EXERCISE_FIELDS for k in value):
          exercises[key] = value
          ex_module[key] = module 
        else:
          sections[key] = value
      if len(mod_opts[module]) == 0:
        del mod_opts[module]
  
  return (exercises, sections, mod_opts)

def generate_full_config(config_file_path):
  ''' Generates a full configuration from a simplified configuration
  '''
  global ex_options, default_ex_options, sect_options, mod_options
  register()

  conf_data = read_conf_file(config_file_path)
  for ex_type in ["ka", "ss", "pe"]:
    field = "glob_{0}_options".format(ex_type)
    if field not in conf_data:
      print_err("WARNING: Missing {0}, using default values instead.".format(field))
      conf_data[field] = default_ex_options[ex_type]

  ex_options, sect_options, mod_options = get_options(conf_data)
  default_ex_options = {
      "ka": conf_data["glob_ka_options"], 
      "ss": conf_data["glob_ss_options"], 
      "pe": conf_data["glob_pe_options"],
      "dgm": {
        "required": False,
        "points": 0,
        "threshold": 1
      }
  }

  full_config = OrderedDict()
  full_config = conf_data.copy()
  full_config['chapters'] = OrderedDict()
  del full_config['glob_ka_options']
  del full_config['glob_ss_options']
  del full_config['glob_pe_options']

  mod_files = get_chapter_module_files(conf_data)
  for chapter, files in mod_files.iteritems():
    full_config['chapters'][chapter] = OrderedDict()
    for x in files:
      rst_dir_name = x.split(os.sep)[-2]
      rst_fname = os.path.basename(x).partition('.')[0]
      if rst_dir_name == conf_data['lang']:
        mod_path = rst_fname
      else:
        mod_path = rst_dir_name + '/' + rst_fname

      if not os.path.isfile(x):
        print_err("ERROR: '{0}' is not a valid module path" % mod_path)
        sys.exit(1)

      with open(x, 'r') as rstfile:
        source = rstfile.read()

      source = remove_markup(source)

      rst_parts = publish_parts(source,
                  settings_overrides={'output_encoding': 'utf8',
                  'initial_header_level': 2},
                  writer_name="xml")

      mod_json = xmltodict.parse(rst_parts['whole'])
      mod_config = extract_mod_config(mod_json)

      full_config['chapters'][chapter][mod_path] = mod_config

  for exer in ex_options:
    print_err('WARNING: the exercise "{0}" does not exist in module "{1}"'.format(exer, ex_module[exer]))
  return full_config
