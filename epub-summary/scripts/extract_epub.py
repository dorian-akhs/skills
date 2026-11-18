#!/usr/bin/env python3
"""Extract ordered EPUB text and a coverage ledger, without third-party packages."""
import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

VERSION = 1
TEXT_TYPES = {'application/xhtml+xml', 'text/html'}
BLOCKS = {'p', 'li', 'blockquote', 'pre', 'tr', 'dt', 'dd', 'figcaption'}
HEADINGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
SKIP = {'head', 'script', 'style'}


def tag(element):
    return element.tag.rsplit('}', 1)[-1] if isinstance(element.tag, str) else ''


def clean(value):
    return re.sub(r'\s+', ' ', value).strip().replace(chr(0x2014), ' - ')


def resolve(base, href):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return href
    name = posixpath.normpath(posixpath.join(posixpath.dirname(base), unquote(parsed.path))) if parsed.path else base
    if name.startswith('../') or name.startswith('/'):
        raise ValueError('Resource outside EPUB container')
    return name + ('#' + unquote(parsed.fragment) if parsed.fragment else '')


def inline(element, resource):
    if tag(element) in SKIP:
        return ''
    if tag(element) == 'img':
        return '[Image : ' + (element.get('alt') or 'sans texte alternatif') + ']'
    result = element.text or ''
    for child in element:
        value = inline(child, resource)
        if tag(child) == 'a' and child.get('href'):
            value = '[' + value + '](' + resolve(resource, child.get('href')) + ')'
        result += value + (child.tail or '')
    return result


def blocks(element, resource, anchor=''):
    current = element.get('id') or anchor
    kind = tag(element)
    if kind in SKIP:
        return
    # Containers with nested blocks are traversed, not flattened, to retain headings.
    nested = any(tag(child) in BLOCKS | HEADINGS for child in element.iter() if child is not element)
    if kind in HEADINGS or (kind in BLOCKS and not nested):
        value = clean(inline(element, resource))
        if value:
            yield kind, current, value
        return
    if clean(element.text or ''):
        yield 'text', current, clean(element.text)
    for child in element:
        if tag(child) not in BLOCKS | HEADINGS and not any(tag(item) in BLOCKS | HEADINGS for item in child.iter()):
            value = clean(inline(child, resource))
            if value:
                yield 'text', child.get('id') or current, value
        else:
            yield from blocks(child, resource, current)
        if clean(child.tail or ''):
            yield 'text', current, clean(child.tail)


def write_json(directory, name, value):
    (directory / name).write_text(json.dumps(value, ensure_ascii=False, indent=2).replace(chr(0x2014), ' - ') + '\n', encoding='utf-8')


def extract(source, output, target_chars):
    warnings = []
    with ZipFile(source) as archive:
        if sum(info.file_size for info in archive.infolist()) > 512 * 1024 * 1024:
            raise ValueError('EPUB exceeds 512 MiB uncompressed limit; inspect manually')
        def xml(name):
            data = archive.read(name)
            if b'<!ENTITY' in data.upper():
                raise ValueError('XML entity declarations unsupported')
            return ET.fromstring(data)
        container = xml('META-INF/container.xml')
        rootfiles = [element.get('full-path') for element in container.iter() if tag(element) == 'rootfile']
        if not rootfiles:
            raise ValueError('No OPF package found')
        if len(rootfiles) > 1:
            warnings.append('Multiple renditions: only the first OPF package was processed')
        package_path = rootfiles[0]
        package = xml(package_path)
        metadata_element = next(element for element in package if tag(element) == 'metadata')
        metadata = {}
        for field in ('title', 'creator', 'language', 'identifier', 'publisher', 'date', 'source'):
            metadata[field] = [clean(''.join(element.itertext())) for element in metadata_element if tag(element) == field]
        manifest_element = next(element for element in package if tag(element) == 'manifest')
        items = {element.get('id'): dict(element.attrib) for element in manifest_element if tag(element) == 'item'}
        spine = next(element for element in package if tag(element) == 'spine')
        encrypted = []
        if 'META-INF/encryption.xml' in archive.namelist():
            encrypted = [element.get('URI') for element in xml('META-INF/encryption.xml').iter() if tag(element) == 'CipherReference']
            warnings.append('Encryption manifest present: inspect encrypted resources; font obfuscation is not necessarily DRM')
        toc = []
        for item in items.values():
            if 'nav' not in item.get('properties', '').split() and item.get('media-type') != 'application/x-dtbncx+xml':
                continue
            resource = resolve(package_path, item['href']).split('#')[0]
            try:
                tree = xml(resource)
                if item.get('media-type') == 'application/x-dtbncx+xml':
                    for point in tree.iter():
                        if tag(point) == 'navPoint':
                            label = next((clean(''.join(element.itertext())) for element in point if tag(element) == 'navLabel'), '')
                            content = next((element.get('src') for element in point if tag(element) == 'content'), None)
                            if content:
                                toc.append({'label': label, 'target': resolve(resource, content)})
                else:
                    for nav in tree.iter():
                        if tag(nav) == 'nav':
                            nav_type = nav.get('{http://www.idpf.org/2007/ops}type', '')
                            for link in nav.iter():
                                if tag(link) == 'a' and link.get('href'):
                                    toc.append({'label': clean(''.join(link.itertext())), 'target': resolve(resource, link.get('href')), 'nav_type': nav_type})
            except (KeyError, ET.ParseError, ValueError) as error:
                warnings.append(f'TOC extraction failed: {resource}: {error}')
        if not toc:
            warnings.append('No usable EPUB navigation found; chapter mapping needs manual verification')
        resources, sections, coverage = [], [], []
        block_count = 0
        for index, reference in enumerate(spine, 1):
            if tag(reference) != 'itemref':
                continue
            entry = {'id': f'spine-{index:04d}', 'idref': reference.get('idref'), 'linear': reference.get('linear', 'yes'), 'status': 'error'}
            resources.append(entry)
            item = items.get(reference.get('idref'))
            if item is None:
                entry['error'] = 'Missing manifest item'
                continue
            resource = resolve(package_path, item['href']).split('#')[0]
            entry['resource'] = resource
            if item.get('media-type') not in TEXT_TYPES:
                entry['error'] = 'Non-text spine resource: inspect separately'
                continue
            try:
                tree = xml(resource)
                body = next((element for element in tree.iter() if tag(element) == 'body'), tree)
                entry['warnings'] = []
                for kind in ('img', 'svg', 'math', 'table'):
                    count = sum(tag(element) == kind for element in body.iter())
                    if count:
                        entry['warnings'].append(f'{kind}: {count}; visual or structured content needs verification')
                parsed = list(blocks(body, resource))
                if not parsed:
                    raise ValueError('No readable text')
                current = None
                for kind, anchor, value in parsed:
                    if current is None or kind in HEADINGS:
                        current = {'id': f'section-{len(sections)+1:04d}', 'spine': entry['id'], 'resource': resource, 'title': value if kind in HEADINGS else resource, 'heading_level': int(kind[1]) if kind in HEADINGS else None, 'blocks': []}
                        sections.append(current)
                    block_count += 1
                    current['blocks'].append({'id': f'b{block_count:06d}', 'kind': kind, 'anchor': anchor, 'text': value})
                entry['status'] = 'extracted'
            except (KeyError, ET.ParseError, ValueError) as error:
                entry['error'] = str(error)
        for section in sections:
            batches, batch, size = [], [], 0
            for block in section['blocks']:
                if batch and size + len(block['text']) > target_chars:
                    batches.append(batch)
                    batch, size = [], 0
                batch.append(block)
                size += len(block['text'])
            if batch:
                batches.append(batch)
            section['words'] = sum(len(block['text'].split()) for block in section['blocks'])
            section['characters'] = sum(len(block['text']) for block in section['blocks'])
            section['chunks'] = []
            for index, batch in enumerate(batches, 1):
                chunk_id = f"{section['id']}-{index:03d}"
                relative = f'chunks/{chunk_id}.md'
                lines = [f"# {section['title']}", f"Source: {section['spine']} / {section['resource']}", '']
                for block in batch:
                    lines.extend([f"[{block['id']}] {section['resource']}" + ('#' + block['anchor'] if block['anchor'] else ''), ('#' * int(block['kind'][1]) + ' ' if block['kind'] in HEADINGS else '') + block['text'], ''])
                (output / relative).write_text('\n'.join(lines), encoding='utf-8')
                section['chunks'].append(relative)
                coverage.append({'id': chunk_id, 'section': section['id'], 'spine': section['spine'], 'file': relative, 'first_block': batch[0]['id'], 'last_block': batch[-1]['id'], 'status': 'pending', 'chapter': None, 'analysis': None, 'reason': None})
            section['block_ids'] = [block['id'] for block in section.pop('blocks')]
        in_spine = {reference.get('idref') for reference in spine}
        outside = [{'idref': key, 'resource': resolve(package_path, item['href']), 'decision': 'pending'} for key, item in items.items() if key not in in_spine and item.get('media-type') in TEXT_TYPES]
        result = {'extraction_version': VERSION, 'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'metadata': metadata, 'package': package_path, 'normalizations': ['Whitespace collapsed; U+2014 replaced by ASCII hyphen. Verify quotations in original XHTML.'], 'warnings': warnings, 'encrypted_resources': encrypted, 'resources': resources, 'text_outside_spine': outside, 'sections': sections, 'total_words': sum(section['words'] for section in sections), 'total_characters': sum(section['characters'] for section in sections), 'chunk_target_characters': target_chars, 'ebook_convert_available': shutil.which('ebook-convert') is not None}
        write_json(output, 'manifest.json', result)
        write_json(output, 'toc.json', toc)
        write_json(output, 'coverage.json', coverage)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--chunk-chars', type=int, default=18000)
    args = parser.parse_args()
    source = args.source.expanduser().resolve(strict=True)
    if source.suffix.lower() != '.epub':
        parser.error('Version 1 supports EPUB only')
    if args.chunk_chars < 1000:
        parser.error('--chunk-chars must be at least 1000')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    cache = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))
    output = (args.output or cache / 'epub-summary' / digest / 'v1').expanduser().absolute()
    if output.exists():
        manifest = output / 'manifest.json'
        if manifest.is_file():
            previous = json.loads(manifest.read_text(encoding='utf-8'))
            if previous.get('sha256') == digest and previous.get('extraction_version') == VERSION and previous.get('chunk_target_characters') == args.chunk_chars:
                print(f'Existing cache, not overwritten: {output}')
                return
        parser.error('Output exists and is not a matching cache. Choose a new --output')
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.extract-', dir=output.parent))
    try:
        (staging / 'chunks').mkdir(mode=0o700)
        (staging / 'analyses').mkdir(mode=0o700)
        result = extract(source, staging, args.chunk_chars)
        staging.rename(output)
    except Exception:
        # Only remove this process's freshly created staging directory on failure.
        shutil.rmtree(staging)
        raise
    errors = sum(entry['status'] == 'error' for entry in result['resources'])
    print(f'{output}\n{len(result["sections"])} sections, {result["total_words"]} words, {errors} resource errors')


if __name__ == '__main__':
    main()
