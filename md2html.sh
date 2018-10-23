for file in "$@"; do
	pandoc -f markdown_github "${file}" -t asciidoc -o "${file%.md}.tmp.adoc" ||exit $?
	touch -r "${file}" "${file%.md}.tmp.adoc" ||exit $?
	TZ=UTC asciidoc -o "${file%.md}.html" -a footer-style=none -a toc2 -a source-highlighter=highlight "${file%.md}.tmp.adoc" ||exit $?
	rm "${file%.md}.tmp.adoc"
done
