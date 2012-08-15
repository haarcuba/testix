from testix import runner
import argparse
import sys
import os
import re

def letSubprocessesInheritEggNamespace():
	egg = os.path.realpath( sys.path[ 0 ] )
	os.environ[ 'PYTHONPATH' ] = '%s:%s' % ( egg, os.environ[ 'PYTHONPATH' ] )

def testFiles():
	result = []
	TEST_PATTERN = re.compile( '^test_.*\.py$' )
	for directory, unusedDirectoryNames, filenames in os.walk( '.', followlinks = True ):
		for filename in filenames:
			if TEST_PATTERN.search( filename ) is not None:
				relativeToTop = os.path.join( directory, filename )
				result.append( relativeToTop )
	return result

if __name__ == '__main__':
	letSubprocessesInheritEggNamespace()
	description = 	"testix - a Python unit test framework" \
					"this is free software, available under the GNU General Public License version 3.0"
	parser = argparse.ArgumentParser( description = description )
	parser.add_argument( 'tests', nargs = '*', metavar = 'TEST', help = 'each test should be a python file implementing a test suite' )
	parser.add_argument( '--find', '-f', action = 'store_true', default = False, help = 'find all test_*.py files and run them' )
	arguments = parser.parse_args()
	if len( arguments.tests ) == 0 and not arguments.find:
		parser.print_help()
		parser.exit( status = 1 )
	tests = []
	if arguments.find: 
		tests += testFiles()
	tests += arguments.tests
	runner.Runner( tests )
