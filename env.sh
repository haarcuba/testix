export TOP=$(pwd)
export PYTHONPATH=$TOP

_indicateWorkArea() {
	prompt='(testix) \W$ '
	color='\[\e[34;1m\]'
	resetColor='\[\e[0m\]'
	export PS1="$color$prompt$resetColor"
}
_indicateWorkArea
