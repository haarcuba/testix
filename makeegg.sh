#!/bin/bash

if [[ -z "$PYTHON" ]]; then
	PYTHON=python
fi

_createVersion()
{
	 gitHash=`git log | head -1 | awk '{ print $2; }'`
	 echo "VERSION = '$gitHash'" > version.py 
}

_compileAllPythons() 
{
	for name in $(find testix -name '*py') ; do
		echo compiling $name
		$PYTHON -c "import compiler ; compiler.compileFile( '$name' )" || exit -1
	done
}

_zipAllPYC()
{
	zip -r testix.egg version.py __main__.py $(find testix -name '*pyc' | grep -v startertests)
}

_resetVersion()
{
	echo "VERSION = 'development'" > version.py
}

_main()
{
	rm -f testix.egg && \
	_createVersion && \
	_compileAllPythons &&\
	_zipAllPYC &&\
	_resetVersion
}

_error()
{
	echo ERROR: something failed
}

_main || _error
