### Background

This repository has a collection of code that I've written to convert latex (.tex) to MS Word (.docx).
Many people need latex to do their jobs efficiently; I am one of those people.
Unfortunately, not all organizations have latex support, and many have requirements for producing documents in MS Word (.docx) format.
Pandoc can be used to convert .tex to .docx; however, there are some issues with the associated workflow.
While pandoc filters are currently being developed to address some of these issues, all of them have not been addressed yet, so I created this workflow to work around these issues while still using pandoc as the underlying conversion mechanism.


### What this code does

The python + pandoc workflow takes as an input
a .tex file
and produces as an output
a .docx document.


### How it works

To convert your .tex file with references, etc. to .docx (Word) format, you need pandoc.
A single pandoc command will convert your .tex document to a somewhat IDA styled .docx, but at this time, the title page, and formatting for figures, tables, equation numbering, and associated cross-references are not supported with the single command line conversion.
The conversion command is found in the pandoc directory.
Pandoc does not support all of the tex features that can be used to directly produce a nicely rendered pdf, so your .tex document may require some prepping before running pandoc, and some features may be incompatible with .docx format.
If you don't do this prep work, then pandoc will typically tell you what it can't handle.
If something isn't compatible with the conversion to .docx, then you may or may not get an error message from pandoc; that is, pandoc may just ignore the incompatible feature as is done with equation numbering.
For this reason, the python code in tex2docx.py does much of this prep work to address incompatibilities, but it requires that the input .tex file follow some standardized rules described below.
The file tex2docx.py automatically preps your .tex document and then runs pandoc to produce your .docx converted file.

It capture equations with numbering (with some existing caveats), references and citations in Chicago style, figures and tables (with some existing caveats), etc.


### How to use this workflow

- The file Example.tex provides an example that can be used as a quick start guide.
- See the How to use LaTeX section below for instructions on using latex.
- Make sure you take note of the caveats and issues listed below while writing your document.
- After completing your document, run tex2docx.py, making sure to pass the name of the .tex file as an input.
- The file Example.docx illustrates the output associated with running tex2docx on Example.tex




### How to use latex
- For the front end GUI, I recommend TexStudio.
- For Windows, I recommend MikTex to manage the backend of your latex distribution.
- For Linux, I recommend TexLive.
You can find links to download these here: https://www.latex-project.org/get/


### Caveats and Known Issues
- Equations: equation numbering *in the conversion to .docx* is currently only supported for single line equations using the *equation* environment LaTeX.
In the future, I will add support for *align* environments for multiline equation numbering support.
This does *not* affect equation numbering in the pdf rendered from the .tex file.
That is, if you don't care about the conversion to .docx, then write your equations however you want, but if you don't care about the conversion to .docx, then why are you visiting this repository?

-  Equation labeling: there is an existing issue where commented out labels are counted toward equation numbering for the .docx conversion.
This does not affect the .tex or .pdf versions, obviously.
When converting to .docx, ensure that you do not have any commented out labels, e.g. *%\label{}*.
To number equations correctly, make sure the label starts with *eq:*.  That is, the label for an equation should be something like *\label{eq: Pythagorean Theorem}*.
  - Update: label flags can now be specified.  The default for equations is ["eq:", "eqn:"], and the default for figures is ["fig:" ]

- Filters: this code makes use of pandoc filters.  In particular, you need pandoc-xnos.


### Pandoc

- Pandoc: https://pandoc.org/

- Pandoc-xnos filter: https://github.com/tomduck/pandoc-xnos
