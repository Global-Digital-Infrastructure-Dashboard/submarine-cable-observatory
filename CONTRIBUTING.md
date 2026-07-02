# Contributing

Thank you for your interest in contributing to the Digital Infrastructure Observatory. This is an open research platform, and contributions of many kinds are welcome, from code and documentation to corrections in the underlying dataset.

## Ways to contribute

- **Report a data issue or correction.** If you spot an inaccurate or outdated record (for example a wrong cable owner, landing point, or status), please open an issue. Data accuracy is central to this project, so these reports are especially valuable.
- **Suggest a feature or improvement.** Ideas for new views, metrics, or datasets are welcome.
- **Improve documentation.** Fixes and additions to the README, this guide, or other docs help everyone.
- **Contribute code.** Bug fixes and features are welcome via pull request.

## Reporting issues

Open an issue and include:

- A clear description of the problem or suggestion.
- **For data corrections:** the specific record, what is wrong, and a source or reference for the correct value if you have one.
- **For bugs:** steps to reproduce, what you expected, and what actually happened.

## Development setup

See the [README](README.md#getting-started) for how to run the dashboard locally. In short: clone the repo, run `npm install`, configure your environment variables, and run `npm run dev`.

## Pull requests

1. Fork the repository and create a branch for your change.
2. Keep changes focused. Smaller, self-contained pull requests are easier to review.
3. Run the linter (`npm run lint`) before submitting.
4. Open a pull request with a clear description of what it changes and why, and link any related issue.

## A note on data changes

Records that appear on the live dashboard pass through a human review step. Proposed data changes may be checked against sources before they are merged, so that the public dataset stays reliable.

## Questions

If you are unsure where to start or have a question, open an issue or reach out to the team (contact details are in the [README](README.md#contact--beta-access)).
