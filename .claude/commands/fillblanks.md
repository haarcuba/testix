this command's format is /fillblanks FILE1 [FILE2] ...

- look at each file for comments that start with `# blank:`
- then do what the comment says, "filling in the blanks"
- the `blank` ends with `endblank`

if files are not specified, use `git grep blank:` to find them
