# pagemarkdown
Let your markdown pages spawn markdown pages!

## Installation
Download `pmd.py`.

## Description
Pagemarkdown introduces the `.pmd` file format, which extends markdown to allow for multiple files to be created from a single .pmd file. All standard markdown formatting applies, but there is a new special character introduced: `§`, allowing you to divide one pagemarkdown file into multiple pages. For example, if we have the following file `test.pmd`:

```markdown
  §test/testing
  # Testing
  §test/testing2
  # Testing 2
  ```
  §test/testing3
  # Testing 3
  ```
```

This would produce two files in the new local directory `test`, `testing.html` containing `# Testing` and `testing2.html` containing `# Testing 2`. PMD respects code blocks and will not create `testing3.html`. Notice that in these cases there is no extension for these file paths - this is because you can specify whether the output will be `.md` or `.html` in the command line.

There is also a mode which allows you to specify the page title:

```markdown
  §
  TITLE: Special Testing
  ADDRESS: test/special
  §
```

This creates a file called `test/special.html` with the title `Special Testing`.

`pmd.py` also supports an advanced directory mode, where you supply a whole directory. In this case it will recursively search for all `.pmd` files in that directory and spawn new files, respecting the existing directory structure. If you supply a different root directory, the existing directory structure will still be maintained.

## Usage
usage: py pmd.py [-h] \[--markdown\] [--directory] \[--output OUTPUT\] target

Pagemarkdown to HTML converter.

positional arguments:
  target                Target file or directory to convert from.

optional arguments:
  -h, --help            show this help message and exit
  --markdown, -m        Compile to markdown files instead of html files.
  --directory, -d       Target is a directory.
  --output OUTPUT, -o OUTPUT
                        Output directory (default is current working directory).
