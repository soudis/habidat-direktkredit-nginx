#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import json,  os, filecmp, sys, shutil, subprocess, logging, traceback
from urllib.request import urlopen
from urllib.error import URLError

try: 

	log = logging.getLogger()
	log.addHandler(logging.StreamHandler(sys.stdout))
	log.setLevel(logging.INFO)

	file_loader = FileSystemLoader('templates')
	env = Environment(loader=file_loader)


	nginxDir = '/etc/nginx/conf.d/'
	nginxTmpDir = '/tmp/conf.d/'

	htmlDir = 'static/'

	if os.path.exists(nginxTmpDir):
		shutil.rmtree(nginxTmpDir)
	os.makedirs(nginxTmpDir)

	projects = {}
	# load projects
	with open("projects.json","r") as json_file:
		projects = json.load(json_file)

	projectConfigs = {}
	# load project configs (if exists)
	if os.path.isfile("projectConfigs.json"):
		with open('projectConfigs.json', 'r') as json_file:
		  projectConfigs = json.load(json_file)	

	#print(projects)	

	# build platforms dictionary
	platforms = {}
	projectConfigs = {}
	for projectId in projects:
		if 'platforms' in projects[projectId]:
			for platform in projects[projectId]['platforms']:
				if platform in platforms:
					platforms[platform]['projects'].append(projectId)
				else:
					platforms[platform] = { 'projects': [projectId] }		
		try:
			response = urlopen('http://%s:8080/projectconfig' % projects[projectId]['container'])
		except URLError as e:
			log.warning("Server not found: " + 'http://%s:8080/projectconfig' % projects[projectId]['container'])
		else:
			projectConfig = json.loads(response.read())
			projectConfigs[projectId] = projectConfig

	# write projectConfigs
	with open('projectConfigs.json', 'w') as outfile:
	    json.dump(projectConfigs, outfile)

	# generate nginx configuration and html templates
	for projectId in projects:
		log.info('Generate single project site %s' % projectId)
		template = env.get_template('nginx_single.conf')
		filename = 'dk_' + projects[projectId]['url'] + '.conf'
		template.stream(sslProvider=os.environ['SSL_PROVIDER'], url=projects[projectId]['url'], container=projects[projectId]['container']).dump(nginxTmpDir + filename)


	for platformId, platform in platforms.items():

		# if there are multiple projects per site => create project selection page
		log.info('Generate project platform %s' % platformId)
		template = env.get_template('nginx_platform.conf')
		filename = 'dk_' + platformId + '.conf'
		template.stream(platform=platform, projects=projects, sslProvider=os.environ['SSL_PROVIDER'], url=platformId, anyContainer=projects[next(iter(platform['projects']))]['container']).dump(nginxTmpDir + filename)
		template = env.get_template('project_chooser.html')
		index_file = open(htmlDir + platformId + '.html', "w")
		index_file.write(
		    template.render(platform=platform, projects=projects, projectConfigs=projectConfigs)
		)
		index_file.close()

	# compare new config 
	nginxChanged = False
	for file in os.listdir(nginxTmpDir):
		if not os.path.isfile(nginxDir + file) or not filecmp.cmp(nginxTmpDir + file, nginxDir + file):
			nginxChanged = True

	for file in os.listdir(nginxDir):
		if file.startswith('dk_') and not os.path.isfile(nginxTmpDir + file):
			nginxChanged = True

	# copy and restart nginx if changed
	if nginxChanged:
		for file in os.listdir(nginxDir):
			if file.startswith('dk_'):
				os.unlink(nginxDir + file)
		for file in os.listdir(nginxTmpDir):
			shutil.copy(nginxTmpDir + file, nginxDir)
		subprocess.call(['nginx', '-s', 'reload'], stderr=subprocess.PIPE)

except Exception as e:
	log.error('Unhandled exception')
	log.error(traceback.format_exc())