# clipboard-many-files
@readwithai - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-assisted reading](https://www.reddit.com/r/machineAidedReading/)

A command-line tool to copy several files to the clipboard as though you copied them from a file browser.

At present, this tool only supports Linux (both X11 and wayland). This tools requires [xclip](https://github.com/astrand/xclip) if you are using X11 or [wl-clipboard](https://github.com/bugaevc/wl-clipboard) if you are using Wayland.

## Motivation
You can copy and paste multiple images from file browsers such as Dolphin in KDE to many apps such as editors or browsers. It is useful to be able to do this form the command-line and so scripts

I could not find any command-line tools to this, despite it being fairly straight-forward when you understand the protocol used. I decided to implement this in a standard way and share it in an easy-to-use form.

## Alternatives and prior work
Most file browsers support copy and pasting multiple files.

It is fairly straightforward to do this manually by setting the [text/uri-list](https://unix.stackexchange.com/questions/53503/copying-files-from-command-line-to-clipboard) target in the clipboard to a new-line separated list of entries [file URL scheme](https://datatracker.ietf.org/doc/rfc8089/). Any user familiar with bash could create a shell script on their path to do so. This tool however removes the need to maintain such as script, and can easily be installed on any system.

## Attribution
I made use of [this approach of converting paths to URLs](https://dnmtechs.com/converting-a-filename-to-a-file-url-in-python-3/).

When reviewing clipbaord libraries, I found some of the code of [pyperclip](https://github.com/asweigart/pyperclip) informative for implementing wayland functionality.

## Caveats
I wrote and tested this library on Linux and this is the only operating system supported at the moment. Patches are welcome for other systems and will be quickly merged.

I use a couple of command-line tools to access the clipboard. I could find no python library which supported setting targets and reading the code for `xclip` communicating with X11 directly is probably more effort that this involved. [Klembord](https://github.com/OzymandiasTheGreat/klembord) seems to have this option - but has been archived and when I tested this functionality on X11 it did not work.

## Support
If you found this tool useful you could give me $1 on my ko-fi. This will incentivize me to respond to issues on this project and [create similar tools](https://readwithai.substack.com/p/my-productivity-tools).

You can also support this project by [looking at similar tools that I have created](https://readwithai.substack.com/p/my-productivity-tools) or reviewing my work related to [reading and research](https://readwithai.substack.com).


## About me
