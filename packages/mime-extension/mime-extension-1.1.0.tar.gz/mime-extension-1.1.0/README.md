# mime-extension
 - **@readwithai**️ - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/)  [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined
)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

Find the file extensions associated with mime-type on a Linux systems.

Note that the reverse query - going from extension to mime-type can be achieved using the  [xdg-mime](https://www.freedesktop.org/wiki/Software/xdg-utils/) command-line tool. You can go from the contents of a file to a mime-type using [the file command](https://www.darwinsys.com/file/) with `file -b --mime-type $FILE`.

# Motivation
There appears to be no standard script to perform this function but a solution and script is provided on [stack exchange by Kamil Maciorowski](https://superuser.com/questions/1347359/how-can-i-get-the-extensions-of-a-file-based-on-its-content). I needed this functionality, and where possible I prefer my solutions to work on any computer and be easily installed so I am packaging this as a script.

Additionally, the solution in stack overflow is based upon `/etc/mime.types` but I think most desktop environmenets now use the XML files `/usr/share/mime` combined with `~/.local/share/mime` for this information.

# Installation
You can install `mime-extension` using [pipx](https://github.com/pypa/pipx):
```
pipx install mime-extension
```

# Usage
```
mime-extension text/html
```

Note that there are often multiple file extensions.

# Support this tool
If you like this tool you could give me money ($1 maybe) on my [ko-fi](https://ko-fi.com/readwithai).

You could also look at some of the [other command-line tools](https://readwithai.substack.com/p/my-productivity-tools) I have created.

# About me
I am @readwithai I make tools for reading, research and agency often using Obsidian.

I also produce a [stream of tools](https://readwithai.substack.com/p/my-productivity-tools) related to the work I do on this.

You can follow me on [X](https://x.com/readwithai) or my blog [blog](https://readwithai.substack.com/).
