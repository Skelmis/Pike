Pike
---

Because writing basic files for reporting things is more complicated than it needs to be. Also, I don't enjoy word.

I find this perfect for writing up disclosures as it keeps all my notes, findings, etc together in a clean and concise manner. 

In terms of features, this is developed to meet my bug bounty needs and that's about it. If you'd like a feature, or found a bug (I'm aware of a couple), please open an issue.

### Usage

Refer to the [example report](https://github.com/Skelmis/Pike/tree/master/example_report) directory for examples. Essentially you define a [main file](https://github.com/Skelmis/Pike/blob/master/example_report/main.py) which grabs config data and ingests all markdown files within the directory before putting them into a report.

#### Structure

Modify your layout file. An example can be seen [here](https://github.com/Skelmis/Pike/blob/master/example_report/configuration/layout.md).

#### But the output looks bad!

Congrats, that's the word default template styling. 

If you want to change:
- Create a new Word document.
- Modify the styles to what you want.
- Within your [config file](https://github.com/Skelmis/Pike/blob/master/example_report/configuration/config.json), point `docx_template` at your new document.

### Building documentation

For more information, please read the full documentation:

1. Ensure you install both the standard and `doc` dependencies installed
2. `cd docs`
3. `make html`
4. And then open the file `docs/_build/html/index.html`