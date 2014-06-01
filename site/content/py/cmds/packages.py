
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
			return self.run_query(None)

		raise Exception("Unknown action")

	def run_info(self, repo, arch, pkg_name):
		return "Package Info: {0}/{1} {2}".format(repo, pkg_name, arch)

	def run_query(self, query):
		return "Package Search: {0}".format(query)
