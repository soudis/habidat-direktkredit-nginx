#!/usr/bin/env python3

import json, sys, os, logging

try: 

	log = logging.getLogger()
	log.addHandler(logging.StreamHandler(sys.stdout))
	log.setLevel(logging.INFO)

	if len(sys.argv) < 2:
		log.info('Usage: delete_project.py <project identifier>')
		exit(1)

	projectId = sys.argv[1]

	projects = {}
	if os.path.isfile("projects.json"):
		with open("projects.json","r") as json_file:
			projects = json.load(json_file)

	if not sys.argv[1] in projects:
		log.error('Project ' + sys.argv[1] + ' does not exist')
		exit(1)

	del projects[projectId]

	with open('projects.json', 'w') as outfile:
		json.dump(projects, outfile)

	log.info('Project ' + projectId + ' deleted')

except Exception as e:
	log.error('Unhandled exception')
	log.error(traceback.format_exc())