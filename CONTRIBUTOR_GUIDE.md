# Contributor Guide

**Version:** v1

The Digital Infrastructure Observatory is built as an open ecosystem, not a closed lab project. The dataset is more useful and more accurate when people outside the project team can check it, extend it, and build on it. This guide explains the ways to take part.

You do not need to be a developer to contribute. Several of the most valuable contributions are corrections from people who know a particular cable, company, or jurisdiction well.

## Ways to contribute

### 1. Report a missing or incorrect record

The most direct way to improve the platform. Useful reports include a cable or policy event that is missing entirely, an incorrect owner, supplier, landing point, length, or status, an out-of-date operational status, and a record that appears twice under different names.

Cable ownership and supplier information is reported inconsistently across public sources, so corrections from people with direct knowledge of a system are especially valuable.

**How:** open a GitHub issue, or use the feedback form linked from the project website. Identify the record, say what is wrong, give the correct value if you know it, and cite a source if you have one.

### 2. Submit a new source

The discovery pipeline searches public sources, but coverage is uneven, particularly outside the United States and Europe. Regional trade press, national regulators, and non-English sources are all underrepresented relative to their importance.

Suggesting a source that the pipeline should be watching improves coverage for every future record, not just one.

**How:** open an issue with the source and a short note on what it covers.

### 3. Suggest an improvement to the data

Beyond individual records, suggestions about the structure of the dataset are welcome: a variable worth capturing that is not currently recorded, a category that does not fit the data well, or a coding rule that produces misleading results in particular cases.

Because these changes affect every record, they are reviewed by the Principal Investigators before being adopted. See the Governance Framework for that process.

### 4. Contribute code or documentation

The dashboard is a React application and the repository is public. Contributions might include bug fixes, accessibility and usability improvements, new visualizations, performance work, or clearer documentation.

**How:** fork the repository, make your change on a branch, run the linter, and open a pull request describing what it changes and why. Smaller, focused pull requests are easier to review.

### 5. Build new indicators or applications

The dataset is intended to be built upon. Possibilities include new indicators computed from the existing variables, analysis of a particular region, corridor, or company, visualizations for a specific audience, and integration of this data with other infrastructure or economic datasets.

If you are working on something along these lines, the project team is glad to hear about it, and beta access provides a downloadable copy of the dataset.

### 6. Extend the framework to other sectors

The pipeline design, AI extraction followed by validation, human review, a structured database, and a public dashboard, is not specific to submarine cables. The project's own next phases apply it to AI data centers and 5G networks, and the same approach could be applied to other critical infrastructure sectors such as energy, healthcare, transport, or logistics.

Researchers interested in adapting the framework to another sector are encouraged to get in touch. The methodology, prompts, and pipeline structure are documented so that they can be reused.

## Getting started

1. Explore the [live dashboard](https://research-platform-sand.vercel.app/).
2. Read the [Data Dictionary](DATA_DICTIONARY.md) to understand what each variable means.
3. Read the [Workflow Documentation](WORKFLOW_DOCUMENTATION.md) to see how records are produced and checked.
4. Open an issue, or request beta access from the website if you would like the underlying dataset.

## What happens to your contribution

Reports are triaged by a research assistant, verified against sources, and either accepted, declined with an explanation, or held pending better evidence. Accepted data corrections are applied to the database with the change and its rationale recorded in the record's notes. You will be told the outcome either way.

The full process is described in the [Governance Framework](GOVERNANCE_FRAMEWORK.md).

## Code of conduct

Contributors are expected to engage respectfully and in good faith. This is a research platform on a politically sensitive subject; discussion of the data should stay grounded in evidence and sources.

## License

The project is released under the MIT License. Contributions are accepted under the same license.
