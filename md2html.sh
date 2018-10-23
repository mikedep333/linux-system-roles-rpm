# Copyright 2018 Red Hat, Inc.
# Author: Václav Doležal <vdolezal@redhat.com>
# THIS FILE IS PROVIDED AS IS, WITH ABSOLUTELY NO WARRANTY EXPRESSED
# OR IMPLIED.  ANY USE IS AT YOUR OWN RISK.
#
# Permission is hereby granted to use or copy this program
# for any purpose, provided the above notices are retained on all copies.
# Permission to modify the code and to distribute modified code is granted,
# provided the above notices are retained, and a notice that the code was
# modified is included with the above copyright notice.
for file in "$@"; do
	pandoc -f markdown_github "${file}" -t asciidoc -o "${file%.md}.tmp.adoc" ||exit $?
	touch -r "${file}" "${file%.md}.tmp.adoc" ||exit $?
	TZ=UTC asciidoc -o "${file%.md}.html" -a footer-style=none -a toc2 -a source-highlighter=highlight "${file%.md}.tmp.adoc" ||exit $?
	rm "${file%.md}.tmp.adoc"
done
