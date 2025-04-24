![Logo](./docs/climax_logo_100x100.png)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

# [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) (a Command Line IMAge eXplorer)

## Installing [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/)

We recommend that you install [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) as a tool using [uv](https://github.com/astral-sh/uv):

    $ uv tool install climax-rfglab

Doing this will result in the placement of the [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) executable in a bin directory in the PATH, which allows the tool to be run without uv. If the directory with the [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) executable is not in the PATH, a warning will be displayed and the following command can be issued to add it to the PATH:

    $ uv tool update-shell

[CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) can also be installed as a regular [Python](https://www.python.org/downloads/) package using [uv](https://github.com/astral-sh/uv):  

    $ uv pip install climax-rfglab

or [pip](https://pip.pypa.io/en):

    $ python3 -m pip install climax-rfglab

### A note on the Python interpreter

[CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) requires that you have [Python 3.10 or above](https://www.python.org/downloads/) installed.

## Using [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/)
How you run [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) depends on how you chose to install it.

If you installed [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) as a tool using [uv](https://github.com/astral-sh/uv), then you can invoke [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) with:

    $ climax <filename>

If you installed [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) as a [Python](https://www.python.org/downloads/) package, you can run it as:

    $ python3 -m climax.py <filename>

You can also run [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) without installing it, taking advantage of [uvx](https://github.com/astral-sh/uv):

    $ uvx --from climax-rfglab climax <filename>

There are a few ways to open an image with [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/):

- You can specifiy the path to the image that you want to open (e.g. *tests/cells_movie.tif*) :

        $ climax tests/cells_movie.tif

- Or you can indicate a folder (*slices* in this example) that contains an image sequence:

        $ climax ./slices

- If there are image channels split into different files, you can specify a group of substrings to distinguish which files in the folder belong to which channel. For example, to open the files in the *slices* folder containing the substrings '488' and '561' as two different channels:

        $ climax ./slices -s 488 561

- You can use a list of paths to concatenate sideways (i.e. display side-by-side, but all the images must have the same dimensions!!):

        $ climax cells_movie_1.tif cells_movie_2.tif

- You can specify the color map used to display the image. The color map defaults to *'gray'*. Check [here](https://matplotlib.org/stable/tutorials/colors/colormaps.html) for a list of color maps.

        $ climax cells_movie.tif -c viridis

[JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/) provides access to the standard [matplotlib](https://matplotlib.org/) toolbar, and also includes a second toolbar with additional functionality:

|icon|function|
|----------------------------------------|------------------------|
|![refresh_icon](./docs/refresh_icon.png)|rotate 90&deg; clockwise
|![refresh_icon](./docs/arrows_h_icon.png)|flip horizontally|
|![refresh_icon](./docs/arrows_v_icon.png)|flip vertically|
|![refresh_icon](./docs/shield_icon.png)|invert color map|
|![refresh_icon](./docs/area_chart_icon.png)|hide/show axes|
|![refresh_icon](./docs/fast_forward_icon.png)|continuous/discrete update|

## [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/) today

As we develop and improve [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/), there may be small changes to the user interface. This is how [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/) looks as of today:

![JuNkIE today](./docs/junkie_today.gif)

## Citing [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/)

If you use [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/), please cite this repository. We are working on the paper!

## Adding functionality onto [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/)

If you would like to extend [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/), please check out [JuNkIE-picasso](https://bitbucket.org/raymond_hawkins_utor/junkie_picasso/src/master/), a [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/) fork that allows you to define arbitrary image processing pipelines and integrate them into [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/).

## Sponsors

We are grateful for the generous support from the following agencies and institutions, which contribute to the
development and maintenance of [JuNkIE](https://bitbucket.org/rfg_lab/junkie/src/master/):

![Sponsors](./docs/sponsors.png)