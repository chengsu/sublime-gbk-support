#coding: utf8

import sublime, sublime_plugin
import os, re

def gbk2utf8(view):
    try:
        reg_all = sublime.Region(0, view.size())
        gbk = view.substr(reg_all).encode('gbk')
    except:
        try:
            gbk=open(view.file_name()+'.bkup','r',encoding='gbk').read()
        except:
            gbk=open(view.file_name(),'r',encoding='gbk').read()

        f=open(view.file_name(),'w',encoding='utf_8')
        f.write(gbk)
        f.close()

        f=open(view.file_name()+'.bkup','w',encoding='gbk')
        f.write(gbk)
        f.close()

        view.set_status('gbk','GBK')
        sublime.status_message('gbk encoding detected, open with utf8.')

def utf82gbk(view):
    if view.get_status('gbk'):
        reg_all = sublime.Region(0, view.size())
        gbk = view.substr(reg_all)

        f=open(view.file_name(),'w',encoding='gbk')
        f.write(gbk)
        f.close()

        try:
            os.remove(view.file_name()+'.bkup')
        except:
            pass

def onsave(view):
    if view.get_status('gbk'):
        reg_all = sublime.Region(0, view.size())
        gbk = view.substr(reg_all)

        f=open(view.file_name()+'.bkup','w',encoding='gbk')
        f.write(gbk)
        f.close()

class EventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        if view.file_name()[-5:]=='.bkup':
            view.close()
        else:
            gbk2utf8(view)

    def on_post_save(self, view):
        onsave(view)

    def on_close(self,view):
        utf82gbk(view)

class SaveWithGbkCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        view=self.view
        view.run_command('save')
        view.set_status('gbk','GBK')

        reg_all = sublime.Region(0, view.size())
        gbk = view.substr(reg_all)

        f=open(view.file_name()+'.bkup','w',encoding='gbk')
        f.write(gbk)
        f.close()

        sublime.status_message('saved with gbk.')

class SaveWithUtf8Command(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        view=self.view
        view.run_command('save')
        view.set_status('gbk','')

        sublime.status_message('saved with utf8.')

        try:
            os.remove(view.file_name()+'.bkup')
        except:
            pass


