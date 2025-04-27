# Introduction

*mkdocs plugin to get nav sorted without yml directives*

Use numeric prefixes for your documentation files/directories names
to drive navigation items sort order.

## Example

You can easily change navigation items layout changing files layout.
Just add a numeric prefixes to files and/or directories of your choice.

We'll start with default layout:
```
docs
| - section_a
    | - file1.md
    | - file2.md
| - section_b
    | - file3.md
    | - file4.md
| - about.md
| - index.md
| - quickstart.md
```

And now we turn it into a structured one:
```
docs
| - 01_index.md
| - 10_quickstart.md
| - 20_section_a
    | - 10_file2.md
    | - 20_file1.md
| - 30_section_b
    | - file3.md
    | - file4.md
| - 40_about.md
```

!!! tip
    See also ``Demo sorted`` and ``Demo unsorted`` to the left.

## Requirements

1.  Python 3.10+
2.  `mkdocs` package

## Installation

``` shell
pip install mkdocs-navsorted-plugin
```

## Configuration

1. Add ``navsorted`` plugin into ``mkdocs.yml``:

    ```yaml title="mkdocs.yml"
    plugins:
      - navsorted
    ```

2. Start adding numeric prefixes to your documentation files and directories.


## Get involved into mkdocs-navsorted

!!! success "Submit issues"
    If you spotted something weird in application behavior or want to propose a feature you can do 
    that at <https://github.com/idlesign/mkdocs-navsorted-plugin/issues>

!!! tip "Write code"
    If you are eager to participate in application development, 
    fork it at <https://github.com/idlesign/mkdocs-navsorted-plugin>, write 
    your code, whether it should be a bugfix or a feature implementation,
    and make a pull request right from the forked project page.

!!! info "Spread the word"
    If you have some tips and tricks or any other words in mind that 
    you think might be of interest for the others --- publish it.
