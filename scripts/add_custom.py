#!/usr/bin/env python3

import json
import logging
import os
import sys

try: 

	log = logging.getLogger()
	log.addHandler(logging.StreamHandler(sys.stdout))
	log.setLevel(logging.INFO)

	if len(sys.argv) < 4:
		log.info('Usage: custom.py <identifier> <container name> <url>')
		exit(1)

	id = sys.argv[1]
	containerName = sys.argv[2]
	projectURL = sys.argv[3]

	custom = {}
	if os.path.isfile("custom.json"):
		with open("custom.json","r") as json_file:
			custom = json.load(json_file)

	if sys.argv[1] in custom:
		log.error('Custom config ' + sys.argv[1] + ' already exists')
		exit(1)

	custom[id] = {"container": containerName, "url": projectURL}

	with open('custom.json', 'w') as outfile:
		json.dump(custom, outfile)

	log.info('Custom config ' + id + ' added')

except Exception as e:
	log.error('Unhandled exception')
	log.error(traceback.format_exc())