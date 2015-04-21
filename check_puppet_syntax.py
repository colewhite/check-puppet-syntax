#!/usr/bin/python

from multiprocessing import Pool
import subprocess
import os
import argparse

try:
    from shellcolor import ShellColor
    color = ShellColor()
    shellcolor = True
except ImportError:
    shellcolor = False


def get_files(folder, extension):
    filelist = []
    for dp, dn, fn in os.walk(os.path.expanduser(folder)):
        for f in fn:
            if f.endswith(extension):
                filelist.append(os.path.join(dp, f))
    return filelist


def parse_pp(filepath):
    errors = []
    process = subprocess.Popen(
        ['puppet parser validate --color=false {}'.format(filepath)], shell=True, stderr=subprocess.PIPE)
    errors.append(filepath + ':\n')
    errors.append(process.stderr.read())
    return errors


def parse_erb(filepath):
    errors = []
    process = subprocess.Popen(
        ['cat {} | erb -P -x -T - | ruby -c > /dev/null'.format(filepath)], shell=True, stderr=subprocess.PIPE)
    errors.append(filepath + ':\n')
    errors.append(process.stderr.read())
    return errors

def parse_yaml(filepath):
    errors = []
    process = subprocess.Popen(
        ['ruby -e \"require \'yaml\'; YAML.parse(File.open(\'{}\'))\";'.format(filepath)], shell=True, stderr=subprocess.PIPE)
    errors.append(filepath + ':\n')
    errors.append(process.stderr.read())
    return errors

def directory_check(rootdir, suffix):
    errors = []
    pool = Pool()
    files = get_files(rootdir, suffix)
    if len(files) > 0:
        if 'pp' in suffix:
            items = pool.map(parse_pp, files)
        elif 'erb' in suffix:
            items = pool.map(parse_erb, files)
        elif 'yaml' in suffix:
            items = pool.map(parse_yaml, files)
        for error in items:
            if error[1] != '':
                errors.append(error[0] + error[1])
        pool.close()
        pool.join()
    else:
        return ['No {} files to check.'.format(suffix)]
    return errors


def colorize(message):
    if shellcolor:
        if 'Warning:' in message:
            return color.colorize(message, 'RESET')
        elif 'Error:' in message:
            return color.colorize(message, 'RED')
        elif 'syntax error' in message:
            return color.colorize(message, 'RED')
        else:
            return color.colorize(message, 'RESET')
    else:
        return message


def error_counter(message):
    if 'Warning:' in message:
        return 0
    elif 'Error:' in message:
        if 'spec' in message:
            return 0
        else:
            return 1
    elif 'syntax error' in message:
        if 'spec' in message:
            return 0
        else:
            return 1
    elif 'Syntax error' in message:
        if 'spec' in message:
            return 0
        else:
            return 1
    else:
        return 0


class FileCheck(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        counter = 0
        if values.endswith('.pp'):
            for item in parse_pp(values):
                print colorize(item)
                counter += error_counter(item)
        elif values.endswith('.erb'):
            for item in parse_erb(values):
                print colorize(item)
                counter += error_counter(item)
        elif values.endswith('.yaml'):
            for item in parse_yaml(values):
                print colorize(item)
                counter += error_counter(item)
        else:
            print 'File is not .pp, .erb, or .yaml.'
            exit(1)
        if counter == 0:
            exit(0)
        else:
            exit(1)


class DirectoryCheck(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        counter = 0
        print 'Puppet File Messages:'
        for item in directory_check(values, '.pp'):
            print colorize(item)
            counter += error_counter(item)

        print 'Template File Messages:'
        for item in directory_check(values, '.erb'):
            print colorize(item)
            counter += error_counter(item)

        print 'YAML File Messages:'
        for item in directory_check(values, '.yaml'):
            print colorize(item)
            counter += error_counter(item)

        if counter == 0:
            exit(0)
        else:
            exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puppet .pp, .erb, and .yaml syntax checker.')
    parser.add_argument('-f', '--file', help='File to be checked.', action=FileCheck)
    parser.add_argument('-d', '--directory', help='Directory to be checked. (Recursive)', action=DirectoryCheck)
    args = parser.parse_args()
