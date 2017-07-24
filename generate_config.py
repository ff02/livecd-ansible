#!/usr/bin/env python
import argparse
import os
import sys
import yaml
import argparse

from jinja2 import Environment, FileSystemLoader

# cmdargs = str(sys.argv)
# config_file_name = str(sys.argv[1])
# template_file_name = str(sys.argv[2])

template_folder='templates'
config_file_name='centos7-minimal.yml'
template_file_name='centos7-minimal.ks.j2'

parser = argparse.ArgumentParser(description='Creates kickstart for livec cd creation')

parser.add_argument('--config', nargs='?', help='Kickstart (default)')
parser.add_argument('--template', nargs='?', help='Template (default)')

args = parser.parse_args()
if args.config != None:
    config_file_name=args.config

if args.template != None:
    template_file_name=args.template


script_path, script_filename = os.path.split(os.path.abspath(__file__))
template_folder=os.path.join(script_path,template_folder)

env = Environment(loader=FileSystemLoader(template_folder))

print('Using config   : %s'    % config_file_name)
print('Using template : %s/%s' % (template_folder, template_file_name))

config_name=os.path.splitext(config_file_name)[0]

with open(config_file_name) as config_file_name_fh:
  dataMap = yaml.load(config_file_name_fh)
  template_dictionary = dataMap[0]['vars']

template_dictionary['work_dir'] = script_path
template_dictionary['config_name'] = config_name

template = env.get_template(template_file_name)
output_from_parsed_template = template.render(template_dictionary)

config_name_kickstart = config_name + '.ks'

with open(config_name_kickstart,"wb") as fh:
  fh.write(output_from_parsed_template)

print('Created        : %s' % config_name_kickstart)



