# invis-scan

Find Unicode control and format characters in UTF-8 text, including bidirectional overrides and zero-width formatting characters. It reports code points and locations without printing the file contents.

Requires Python 3.8+ and uses only the standard library.

    python invis_scan.py src/main.py README.md

Tabs and line breaks are allowed. Findings are not automatically malicious: some format characters are legitimate in emoji and natural-language text, so inspect their reported locations in context. The scanner does not detect visually similar letters or every homoglyph. Columns count Unicode code points, not bytes.

Exit status: 0 when no findings or read errors occur, 1 when findings are present, 2 when a file cannot be read as UTF-8.

## License

MIT. See [LICENSE](LICENSE).
