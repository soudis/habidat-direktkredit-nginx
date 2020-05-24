#!/usr/bin/env python3

import json, sys, os, logging

try: 

	log = logging.getLogger()
	log.addHandler(logging.StreamHandler(sys.stdout))
	log.setLevel(logging.INFO)

	if len(sys.argv) < 4:
		log.info('Usage: add_project.py <project identifier> <container name> <url> [<platform url>] [<platform url>] ...')
		exit(1)

	projectId = sys.argv[1]
	containerName = sys.argv[2]
	projectURL = sys.argv[3]
	projectPlatforms = []

	if len(sys.argv) > 4:
		projectPlatforms = sys.argv[4:]

	projects = {}
	if os.path.isfile("projects.json"):
		with open("projects.json","r") as json_file:
			projects = json.load(json_file)

	if sys.argv[1] in projects:
		log.error('Project ' + sys.argv[1] + ' already exists')
		exit(1)

	projects[projectId] = {"container": containerName, "url": projectURL, "platforms": projectPlatforms}

	with open('projects.json', 'w') as outfile:
		json.dump(projects, outfile)

	log.info('Project ' + projectId + ' added')

except Exception as e:
	log.error('Unhandled exception')
	log.error(traceback.format_exc())