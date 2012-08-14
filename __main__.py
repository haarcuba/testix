from testix import runner
import argparse

if __name__ == '__main__':
	description = 	"testix - a Python unit test framework" \
					"this is free software, available under the GNU General Public License version 3.0"
	parser = argparse.ArgumentParser( description = description )
	parser.add_argument( 'tests', nargs = '+', metavar = 'TEST', help = 'each test should be a python file implementing a test suite' )
	arguments = parser.parse_args()
	runner.Runner( arguments.tests )
