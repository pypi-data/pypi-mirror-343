


""" Test tool to run a program with various Pythons. """

from SajadDE.PythonVersions import getSupportedPythonVersions
from SajadDE.utils.Execution import check_output
from SajadDE.utils.InstalledPythons import findPythons


def findAllPythons():
    for python_version in getSupportedPythonVersions():
        for python in findPythons(python_version):
            yield python, python_version


def executeWithInstalledPython(python, args):
    return check_output([python.getPythonExe()] + args)



