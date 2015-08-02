# mpdb
This project is an extension of the built in python debugger (pdb).
It's purpose is to provide the user with an easy to digest presentation of the relevant variables and their values
when they run pdb.  It's a work in progress.
Please contact me if you have any questions or comments.


Below is an image of the output produced when mpdb is run on the included sample file.

![image01]
[image01]: ./mpdb/documentation/example01.jpg

How to install/implement mpdb:
(I will wrap this into a pip package soon!)

To Install:


    easy_install prettytable

To Use:


- In all 3 files set:
PRODUCTION = True

    - Add the following to the code you are debugging:
        from .mpdb.mpdb import *
        from .mpdb.zpdb import *

    - Insert one of the following instructions into your code where you wish
      to create a debugging breakpoint:

        Mpdb.run(locals()) <-- runs mpdb and quit resumes code execution
            OR
        set_trace(locals()) <-- runs mpdb and quit lauches pdb

