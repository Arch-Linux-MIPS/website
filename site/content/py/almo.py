import traceback

from urllib.parse import parse_qs
from urllib.parse import urlparse

from cmds.packages import CmdPackages
from cmds.recent_builds import CmdRecentBuilds

_cmds = {
	"packages": CmdPackages,
	"recent-builds": CmdRecentBuilds,
}

class AlmoPy:
	def __init__(self, env, start_response):
		self._env = env
		self._start_response = start_response

	def run(self):
		if self._env["PATH_INFO"] == "/py/ssi":
			path = None
			q = self._env["QUERY_STRING"]
		elif self._env["REQUEST_URI"].startswith("/py"):
			path = self._env["REQUEST_URI"][3:]
			q = self._env["QUERY_STRING"]
		else:
			url = urlparse(self._env["REQUEST_URI"])
			path = url.path
			q = url.query

		try:
			q = parse_qs(q)
		except:
			q = {}

		if path is None:
			path = q.get("p", [""])[0]

		dirs = [ d for d in path.split("/") if len(d) > 0 ]
		cmd = dirs[0] if len(dirs) > 0 else None
		subcmd = dirs[1:] if len(dirs) > 1 else []

		cmd_class = _cmds.get(cmd)
		if cmd_class is None:
			self._start_response("404 File Not Found", [("Content-Type","text/html")])
			return [ "404 File Not Found: {0}".format(path).encode("utf-8") ]

		html = cmd_class(subcmd, q).run()
		self._start_response("200 OK", [("Content-Type","text/html")])
		return [ html.encode("utf-8") ]

def application(env, start_response):
	try:
		return AlmoPy(env, start_response).run()
	except Exception as ex:
		self._start_response("500 Internal Server Error", [("Content-Type","text/html")])
		return [ "FATAL\n{0}\n{1}".format(str(ex), traceback.format_exc()).encode("utf-8") ]
