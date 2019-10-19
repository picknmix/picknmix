=======
Maintainer
=======

Below are couple of scripts meant for the usage of the maintainer of this project.

bump-version-and-push-tag-to-github.sh
--------------------------------------
Source file: `./bump-version-and-push-tag-to-github.sh`_

Bump the version of the current release to the next available on based on the ``.bumpversion.cfg`` file.
Perform some checks and inform the user.

Usage:

      $ ./bump-version-and-push-tag-to-github.sh [new release version]

      for e.g.:
         $ ./bump-version-and-push-tag-to-github.sh 0.1.2

It's optional to specify a release version as a cli arg.
In the absence of the release version supplied via CLI args, it will use the information in the .bumpversion.cfg file

For brevity, the verbose output from bumpversion can be found at ``.bumpversion-verbose-output.txt``.


delete-tag.sh
-------------
Source file: `./delete-tag.sh`_

Delete a specified git tag from the local and remote repository. It does not however remove any commits made by bumpversion.

Usage:

    $ ./delete-tag.sh [tag name]

       for e.g.:
          $ ./delete-tag.sh v0.1.2


Suggestions on how to remove git commits can be found in ``.git-commits-removal-suggestions.txt``.
