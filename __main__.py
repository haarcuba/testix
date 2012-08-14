from testix import runner
import argparse
import sys
import os

def letSubprocessesInheritEggNamespace():
	egg = os.path.realpath( sys.path[ 0 ] )
	os.environ[ 'PYTHONPATH' ] = '%s:%s' % ( egg, os.environ[ 'PYTHONPATH' ] )

if __name__ == '__main__':
	letSubprocessesInheritEggNamespace()
	description = 	"testix - a Python unit test framework" \
					"this is free software, available under the GNU General Public License version 3.0"
	parser = argparse.ArgumentParser( description = description )
	parser.add_argument( 'tests', nargs = '+', metavar = 'TEST', help = 'each test should be a python file implementing a test suite' )
	arguments = parser.parse_args()
	runner.Runner( arguments.tests )
