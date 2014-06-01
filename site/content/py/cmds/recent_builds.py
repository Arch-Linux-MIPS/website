import json

from sh import alm_architect

class CmdRecentBuilds:
	def __init__(self, subcmd, qs):
		self._qs = qs
		self._subcmd = subcmd

	def run(self):
		json_str = alm_architect.stats("recent-builds", json=True).stdout.decode("utf-8")
		builds = json.loads(json_str)["builds"]

		html = "<ul>"

		for build in builds:
			html += "<li>{0}".format(build["pkg"].split("/")[-1])
			html += " <span class=\"ver\">{0}</span>".format(build["version"])
			html += " <span class=\"arch\">{0}</span>".format(build["arch"])
			html += "</li>"

		html += "</ul>"
		return html
