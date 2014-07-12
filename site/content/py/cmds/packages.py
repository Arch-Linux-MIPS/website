import json
import sh

class CmdPackages:
	def __init__(self, subcmd, qs):
		self._qs = qs
		self._subcmd = subcmd

	def run(self):
		if len(self._subcmd) == 3:
			return self.run_info(self._subcmd[0], self._subcmd[1], self._subcmd[2])

		if "q" in self._qs:
			return self.run_query(self._qs["q"])

		if len(self._subcmd) == 0:
			return self.run_overview()

		raise Exception("Unknown action")

	def run_info(self, repo, arch, pkg_name):
		return "Package Info: {0}/{1} {2}".format(repo, pkg_name, arch)

	def repo_sort(self, pkg_id):
		repo = pkg_id.split("/")[0]
		if repo == "core":
			return 0
		if repo == "extra":
			return 1
		if repo == "community":
			return 2
		return 3

	def run_overview(self):
		js = json.loads(str(sh.alm_architect(["dump", "--json", "/"])))
		html = "<table id=\"packages\">"

		html += "<tr class=\"header\">"
		html += "<td class=\"repo\">Repository</td>"
		html += "<td class=\"name\">Package Name</td>"
		html += "<td class=\"version-built\">Built</td>"
		html += "<td class=\"version\">Latest</td>"
		html += "</tr>"

		pkgs = js["pkgs"]
		pkgs.sort(key=lambda p: (self.repo_sort(p["id"]), p["name"]))

		for pkg in pkgs:
			ver_curr = pkg["version"] if "version" in pkg else ""
			ver_built = pkg["version-built"] if "version-built" in pkg else ""

			html += "<tr class=\"{0}\">".format(" ".join(pkg["status"]))
			html += "<td class=\"repo\">{0}</td>".format(pkg["id"].split("/")[0])
			html += "<td class=\"name\">{0}</td>".format(pkg["name"])
			html += "<td class=\"version-built\">{0}</td>".format(ver_built)
			html += "<td class=\"version\">{0}</td>".format(ver_curr)
			html += "</tr>"

		html += "</table>"
		return html

	def run_query(self, query):
		return "Package Search: {0}".format(query)
