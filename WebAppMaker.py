from html_writer import *
import PySimpleGUI as sg
from os import system

def path(folder, file):
	return '%s/%s' % (folder, file)

def makeLayout(folder, name):
	system('mkdir %s' % (project:=path(folder, name)))
	open(path(project, 'app.py'), 'w')
	system('mkdir %s' % path(project, 'templates'))

def pythonEditor(project_folder):
	code='''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World'

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
'''.strip('\n')
	layout = [
					[sg.Multiline(code, key='multi', s=(50, 30))],
					[sg.B('Save'), sg.B('Open')]
					]
	win=sg.Window('', layout, finalize=True)
	while 1:
		event, values=win.read()
		if event==None:
			break
		elif event=='Save':
			with open(path(project_folder, 'app.py'), 'w') as f:
				f.write(values['multi'])
		elif event=='Open':
			win['multi'].update(open(path(project_folder, 'app.py'), 'r').read())
	win.close()

def HTMLEditor(templates):
	writer=html_writer()
	title=sg.popup_get_text('Title of the HTML document')
	writer.title(title)
	web_layout=[]
	values = [
		'Label',
		'Link',
		'Header',
	]
	layout = [
					[sg.Combo(
						values, enable_events=True, 
						readonly=True, key='widgets', size=(10, 1)
					)],
					[sg.B('Remove A Value'), sg.B('Reset Layout'), sg.B('Save')]
					]
	win=sg.Window('', layout)
	while 1:
		event, values=win.read()
		if event==None:
			break
		elif event=='widgets':
			widget=values['widgets']
			if widget=='Label':
				web_layout.append(label(sg.popup_get_text('Label\'s text')))
			elif widget=='Link':
				text=sg.popup_get_text('Link\'s text')
				href=sg.popup_get_text('Link\'s destination')
				web_layout.append(link(text, href))
			elif widget=='Header':
				text=sg.popup_get_text('Header\'s text')
				href=int(sg.popup_get_text('Level'))
		elif event=='Remove A Value':
			index=int(sg.popup_get_text('Index of the value to remove'))
			web_layout.pop(index)
		elif event=='Save':
			with open(path(templates, sg.popup_get_text('Template name')), 'w') as f:
				writer.body(web_layout)
				f.write(writer.html)
		elif event=='Reset Layout':
			web_layout=[]
	win.close()

def mainloop(FOLDER):
	win=sg.Window('', [
		[sg.B('Add Some HTML'), sg.B('Add Some Python Code')], 
		[sg.B('Run The Web App')]
	])
	while 1:
		event, values=win.read()
		if event==None:
			break
		elif event=='Add Some HTML':
			win.hide()
			HTMLEditor(path(FOLDER, 'templates'))
			win.UnHide()
		elif event=='Add Some Python Code':
			win.hide()
			pythonEditor(FOLDER)
			win.UnHide()
		elif event=='Run The Web App' 
				and sg.popup_yes_no(
					'This will freeze the app', 'are you sure you want to continue?')=='Yes:
			system('python %s' % path(FOLDER, 'app.py'))
	win.close()

if __name__=='__main__':
	w=sg.Window('', [[sg.B('Create New Project'), sg.B('Open An Existing Project')]])
	FOLDER='/storage/emulated/0/WebAppMaker/projects'
	while 1:
		e, v=w.read()
		if e==None:
			break
		elif e=='Create New Project':
			w.hide()
			name=sg.popup_get_text('Title of your project')
			makeLayout(FOLDER, name)
			mainloop(path(FOLDER, name))
			w.UnHide()
		elif e=='Open An Existing Project':
			w.hide()
			name=sg.popup_get_text('Title of your project')
			mainloop(path(FOLDER, name))
			w.UnHide()
	w.close()