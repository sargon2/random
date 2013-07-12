Saving is stupid.

Type a word, ^s. Type a word, ^s.  Stupid.  So much duplication.

This is a proof-of-concept text editor that does not let the user save.  Of course, behind the scenes, it's still writing changes to disk -- but this process is completely abstracted away from the user.

Use cases that saving provides:

1. Make a change, revert to saved (solvable with undo checkpoints)
1. Your computer crashes, and after rebooting you don't have to redo any work (solved by automatic saving/event management)
1. Save multiple versions of a file, that are mostly similar but a little different (checkpoints)

