export TOP=$(pwd)
export PYTHONPATH=$TOP

_indicateWorkArea() {
	prompt='(testix) \W$ '
	color='\[\e[34;1m\]'
	resetColor='\[\e[0m\]'
	export PS1="$color$prompt$resetColor"
}
_indicateWorkArea

_setupVIM() {
	export VIMINIT=$(find vim/plugin/ -name '*.vim' | awk '{print "source " $0 "|" } END { print "source vim/vimrc" }')
	alias vim='vim --noplugin'
}
_setupVIM
