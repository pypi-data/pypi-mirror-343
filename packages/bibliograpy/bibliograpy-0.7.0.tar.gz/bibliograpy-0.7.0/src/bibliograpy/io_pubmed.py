"""Pubmed I/O module."""

import json

from typing import TextIO

import yaml

from bibliograpy.api_core import InputFormat, OutputFormat, Format, Formats
from bibliograpy.api_mesh import MeshPublicationType
from bibliograpy.api_pubmed import Tags

_MAX_TAG_LENGTH = 4
_DEFAULT_START_LINE = _MAX_TAG_LENGTH + 2
_TAG_LINE_SEPARATOR = '-'

class PubmedInputFormat(InputFormat):
    """Ris 2001 input format implementation."""

    def __init__(self, source: Format):
        super().__init__(source=source, standard=Formats.PUBMED)

    def from_yml(self, i: TextIO):
        """Reads from yml representation."""
        return [{Tags.parse(k): MeshPublicationType.parse(e[k]) if Tags.parse(k) is Tags.PT else e[k] for k in e}
                for e in yaml.safe_load(i)]

    def from_json(self, i: TextIO):
        """Reads from json representation."""
        return [{Tags.parse(k): MeshPublicationType.parse(e[k]) if Tags.parse(k) is Tags.PT else e[k] for k in e}
                for e in json.load(i)]

    def from_standard(self, i: TextIO) -> list[dict[Tags | str, str | list[str] | MeshPublicationType]]:
        """Reads from standard format."""

        results: list[dict[Tags, str | list[str] | MeshPublicationType]] = []

        while True:
            entry: dict[Tags | str, str | list[str] | MeshPublicationType] | None = _read_pubmed_entry(i)
            if entry is None:
                return results
            if len(entry) == 0:
                continue
            results.append(entry)
        return results

def _read_pubmed_entry(tio: TextIO) -> dict[Tags | str, str | list[str] | MeshPublicationType] | None:
    """Reads a single Pubmed entry from the input stream.
    Args:
        tio (TextIO): the input text stream

    Return:
        (dict[Tags | str, str | list[str] | MeshPublicationType] | None): a pubmed entry as a dictionary, an empty
        dictionary is returned if the first potential entry line is empty, None is returned if the end of input stream
        is reached
    """

    entry = None

    last_tag: Tags | str | None = None

    while line := tio.readline():

        # init the result dictionary inside the loop to return None if the end of the stream has been previously reached
        if entry is None:
            entry = {}

        # An empty line interrupts the entry reading.
        # Thus, if the first potential entry line is empty, en empty dictionary is returned
        if line.rstrip() == '':
            return entry

        try:
            tag: Tags = Tags.parse(line[:_MAX_TAG_LENGTH].rstrip())
            last_tag = tag

            # hack to support some exports which en hyphen offset can be found:
            # instead of:
            # AID - https://doi.org/10.1136/vr.d2344 [doi]
            # PMID- 21730035
            # such lines are:
            # AID  - https://doi.org/10.1136/vr.d2344 [doi]
            # PMID  - 21730035

            start_line_idx = _DEFAULT_START_LINE if line[_MAX_TAG_LENGTH] == _TAG_LINE_SEPARATOR \
                else _adjust_line_idx(tag.name)

            content = line[start_line_idx:].rstrip('\n\r')
            content = MeshPublicationType.parse(content) if tag is Tags.PT else content

            if tag.repeating and tag in entry:
                entry[tag].append(content)
            elif tag.repeating:
                entry[tag] = [content]
            else:
                entry[tag] = content

        except ValueError as e:

            # extension tags support (as strings)
            tag: str = line[:_MAX_TAG_LENGTH].rstrip()
            start_line_idx = _DEFAULT_START_LINE if line[4] == _TAG_LINE_SEPARATOR else _adjust_line_idx(tag)
            if line[start_line_idx - 2] == _TAG_LINE_SEPARATOR:
                entry[tag] = line[start_line_idx:].rstrip('\n\r')
                last_tag = tag
                continue

            if last_tag is None:
                raise e

            # long field support
            if isinstance(last_tag, Tags) and last_tag.repeating:
                entry[last_tag][-1] += line.rstrip('\n\r')
            else:
                entry[last_tag] += line.rstrip('\n\r')

    return entry


def _adjust_line_idx(tag_str: str) -> int:
    if len(tag_str) == 3:
        return _DEFAULT_START_LINE + 1
    if len(tag_str) == 4:
        return _DEFAULT_START_LINE + 2
    return _DEFAULT_START_LINE


class PubmedOutputFormat(OutputFormat):
    """Pubmed format implementation."""

    def __init__(self,
                 content: list[dict[Tags, str | list[str] | MeshPublicationType]],
                 target: Format):
        super().__init__(target=target, standard=Formats.PUBMED)
        self._content = content

    def _to_value(self, value: list | str) -> str | list[str]:
        if isinstance(value, list):
            result = []
            for v in value:
                result.append(self._to_value(v))
            return result

        return value.value if isinstance(value, MeshPublicationType) else value

    def to_yml(self, o: TextIO):
        """Writes to yml representation."""
        yaml.dump([{k.name: self._to_value(e[k]) for k in e}
                   for e in self._content],
                  o,
                  sort_keys=False)

    def to_json(self, o: TextIO):
        """Writes to json representation."""
        json.dump([{k.name: self._to_value(e[k]) for k in e}
                   for e in self._content],
                  fp=o,
                  sort_keys=False)

    @staticmethod
    def _to_std_tag(tag: Tags | str) -> str:
        s = tag if isinstance(tag, str) else tag.name
        l = len(s)

        if l == 3:
            return s + ' - '

        if l == 4:
            return s + '- '

        return s + '  - '


    def to_standard(self, o: TextIO):
        """Writes to standard format."""

        for bib_entry in self._content:

            for tag in bib_entry:

                if tag is Tags.PT:
                    for pt in bib_entry[tag]:
                        o.write(f'{Tags.PT.name}  - {pt.value}\n')
                elif tag.repeating:
                    for l in bib_entry[tag]:
                        o.write(f'{PubmedOutputFormat._to_std_tag(tag)}{l}\n')
                else:
                    o.write(f'{PubmedOutputFormat._to_std_tag(tag)}{bib_entry[tag]}\n')

    def to_py(self, o: TextIO):
        """Writes to python representation."""

        o.write('from bibliograpy.api_mesh import *\n')
        o.write('from bibliograpy.api_pubmed import *\n\n')
        o.write('\n')

        for bib_entry in self._content:
            key = bib_entry[Tags.PMID].upper()

            if not key[0].isalpha():
                key = 'PUBMED_' + key

            key.replace('.', '_')

            o.write(f'{key} = ')
            o.write('{\n')
            for e in bib_entry:
                if e is Tags.PT:
                    o.write(f"  Tags.{e.name}: [")
                    for i in bib_entry[e]:
                        o.write(f"MeshPublicationType.{i.name}, ")
                    o.write("],\n")
                elif e.repeating:
                    o.write(f"  Tags.{e.name}: {bib_entry[e]},\n")
                else:
                    o.write(f"  Tags.{e.name}: '{bib_entry[e]}',\n")
            o.write('}\n')
