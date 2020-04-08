# Sphinx documentation

**Note**: Sphinx documentation is not required for the class project but is typical to find in software projects so instructions on how to create these can be found below. 

<!-- toc -->

- [Accessing docs](#accessing-docs)
- [Sphinx setup guide](#sphinx-setup-guide)
- [Updating docs](#updating-docs)
  * [Changes to current files](#changes-to-current-files)
  * [Addition of files](#addition-of-files)

<!-- tocstop -->

## Accessing docs 

Open up `build/html/index.html` to access documentation. 


## Sphinx setup guide 
This documentation was created by doing the following from this directory: 

1. Install the necessary packages
    ```bash
    conda install sphinx
    conda install sphinx_rtd_theme
    ```
1. Run `sphinx-quickstart`

2. Edit `conf.py`

    Add the following at the top of the script: 
    
    ```python
    import os
    import sys
    import sphinx_rtd_theme
    sys.path.insert(0, os.path.abspath('../..'))
    sys.path.insert(0, os.path.abspath('../'))
    sys.path.insert(0, os.path.abspath('../src'))
    ```
    
    Change `html_theme` (found around line 85) and add `html_theme_path` as follows:
    
    ```python
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    ```

3. Run `sphinx-apidoc` to autogenerate pages with `autodoc` as follows from the command line:

    ```bash
    sphinx-apidoc -f -o source/ ../ 
    ```

4. Add to `source/index.rst`:

    ```markdowns
    Contents
    --------
    .. toctree::
       :maxdepth: 2
    
       src
       app
    ```

5. Make html files by running from the command line: 

    ```bash
    make html 
    ```

## Updating docs

### Changes to current files 
Any time that the current Python files or sphinx `.rst` files are changed, the `html` should be recreated by running from this directory:

```bash
make html
```

### Addition of files 

If new files are added, the autodoc files should be recreated by running 


```bash
    sphinx-apidoc -f -o source/ ../ 

```

as in step 3 in the setup guide above. 

If new directories are added, the above command should be run for the new directory and the directory needs to be added to `source/index.rst` as in step 4 in the guide below.