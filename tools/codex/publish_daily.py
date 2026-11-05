"""Render and publish Codex-authored reports. Standard library; no model/API clients."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlsplit

SHANGHAI = timezone(timedelta(hours=8))
TOPICS = {
    'deposition-surrogates': '过程模块AI替代',
    'surface-exchange': '沉降与陆气交换',
    'deposition-constraints': '观测约束与反演',
    'geospatial-surface': '遥感与地表表征',
    'source-sink-coupling': '过程耦合与数值方法',
}
TRAILERS = ('\n\nCo-Authored-By: lilmortyj <781113402@qq.com>'
            '\nCo-Authored-By: xixi <3495302215@qq.com>'
            '\nCo-Authored-By: wy <345619498@qq.com>')


def read_json(path, default=None):
    return json.loads(Path(path).read_text(encoding='utf-8-sig')) if Path(path).exists() else default


def canonical(value):
    value = str(value).strip().lower().rstrip('/')
    value = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value)
    value = re.sub(r'^doi:', '', value)
    if re.fullmatch(r'10\.\d{4,9}/\S+', value):
        return 'doi:' + value
    value = re.sub(r'^https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/', '', value)
    value = re.sub(r'^arxiv:', '', value).removesuffix('.pdf')
    value = re.sub(r'v\d+$', '', value)
    if re.fullmatch(r'\d{4}\.\d{4,5}|[a-z-]+/\d{7}', value):
        return 'arxiv:' + value
    raise ValueError('Use a DOI or arXiv identifier: ' + value)


def https_url(value):
    parsed = urlsplit(str(value))
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Expected a public HTTPS source URL')
    if parsed.hostname in {'localhost', '127.0.0.1', '::1'}:
        raise ValueError('Local source URLs are not allowed')
    return str(value)


def ledger(repo):
    return read_json(repo / 'archive/codex/recommendations.json', {'version': 1, 'papers': {}, 'runs': {}})


def historic_ids(repo):
    result = set(ledger(repo)['papers'])
    # Existing arXiv pages predate the Codex ledger; ignore version when deduplicating.
    for path in (repo / 'docs').glob('*/*/*.md'):
        match = re.match(r'^(\d{4}\.\d{4,5})(?:v\d+)?-', path.name)
        if match:
            result.add(canonical(match[1]))
    for path in (repo / 'docs').glob('*/*/papers.meta.json'):
        for paper in (read_json(path, {}) or {}).get('papers', []):
            for field in ('doi', 'url', 'pdf'):
                try:
                    result.add(canonical(paper.get(field, '')))
                except ValueError:
                    pass
    return result


def validate(payload, repo):
    run_date = date.fromisoformat(payload['date'])
    if run_date > datetime.now(SHANGHAI).date():
        raise ValueError('Report date is in the future')
    if payload.get('generator') != 'codex-subscription':
        raise ValueError('generator must be codex-subscription')
    papers = payload['papers']
    if not isinstance(papers, list) or len(papers) > 5:
        raise ValueError('Use zero to five papers; do not fill a quota')
    for field in ('brief', 'search_notes'):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError('Missing report field: ' + field)
    if not isinstance(payload.get('search_sources'), list) or not payload['search_sources']:
        raise ValueError('Record checked primary-source search pages, including on empty days')
    for url in payload['search_sources']:
        https_url(url)
    existing = ledger(repo)
    if payload['date'] in existing['runs']:
        raise ValueError('This date was already published; do not replace a finished report')
    known = historic_ids(repo)
    seen = set()
    required = ('id', 'title', 'title_zh', 'authors', 'published', 'url', 'source',
                'section', 'topics', 'evidence_level', 'summary', 'method', 'result',
                'relevance', 'limitations', 'novelty')
    for paper in papers:
        if any(not paper.get(key) for key in required):
            raise ValueError('Paper has missing required fields: ' + str(paper.get('id')))
        paper['id'] = canonical(paper['id'])
        aliases = {canonical(v) for v in paper.get('aliases', [])} | {paper['id']}
        if aliases & (seen | known):
            raise ValueError('Already recommended (or duplicate within report): ' + paper['id'])
        seen.update(aliases)
        if not isinstance(paper['authors'], list) or not all(isinstance(v, str) for v in paper['authors']):
            raise ValueError('authors must be a list of names')
        if not isinstance(paper['topics'], list) or not 1 <= len(paper['topics']) <= 3 or set(paper['topics']) - TOPICS.keys():
            raise ValueError('Use one to three known topic tags')
        published = date.fromisoformat(paper['published'])
        if published > run_date:
            raise ValueError('Cannot recommend a future publication')
        if paper['novelty'] not in ('recent', 'method-backfill'):
            raise ValueError('novelty must be recent or method-backfill')
        if (run_date - published).days > 30 and paper['novelty'] != 'method-backfill':
            raise ValueError('Older papers must be explicitly labelled method-backfill')
        if paper['section'] not in ('deep', 'quick') or paper['evidence_level'] not in ('full_text', 'abstract'):
            raise ValueError('Invalid section or evidence_level')
        if paper['section'] == 'deep' and paper['evidence_level'] != 'full_text':
            raise ValueError('Full text must be read before calling a paper deep reading')
        for field in ('critical_assessment', 'differences'):
            if field in paper and (not isinstance(paper[field], str) or not paper[field].strip()):
                raise ValueError(field + ' must be nonempty text when provided')
        https_url(paper['url'])
        if paper.get('pdf_url'):
            https_url(paper['pdf_url'])
        if not 0 <= float(paper.get('score', 8)) <= 10:
            raise ValueError('score must be between 0 and 10')
    return payload


def slug(paper):
    digest = hashlib.sha256(paper['id'].encode()).hexdigest()[:12]
    title = re.sub(r'[^a-z0-9]+', '-', paper['title'].lower()).strip('-')[:75].rstrip('-')
    return 'codex-' + digest + '-' + (title or 'paper')


def json_text(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def safe_text(value):
    # Research text is rendered as text, never executable HTML supplied by a source.
    return html.escape(str(value), quote=False)


def paper_page(paper):
    fields = {
        'title': paper['title'], 'title_zh': paper['title_zh'],
        'authors': ', '.join(paper['authors']), 'date': paper['published'],
        'tags': ['paper:' + ('精读区' if paper['section'] == 'deep' else '速读区')]
                + ['query:' + t for t in paper['topics']],
        'score': float(paper.get('score', 8)), 'evidence': paper['relevance'],
        'tldr': paper['summary'], 'source': paper['source'],
        'selection_source': 'codex-subscription', 'summary_format': 'problem-oriented', 'method': paper['method'],
        'result': paper['result'], 'conclusion': paper['limitations'],
    }
    if paper.get('pdf_url'):
        fields['pdf'] = paper['pdf_url']
    if paper.get('motivation'):
        fields['motivation'] = paper['motivation']
    for field in ('critical_assessment', 'differences'):
        if paper.get(field):
            fields[field] = paper[field]
    # JSON strings/arrays/numbers are valid YAML and work with the existing front-end.
    lines = ['---'] + [f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in fields.items()] + ['---', '']
    level = '已阅读全文' if paper['evidence_level'] == 'full_text' else '仅核对摘要'
    novelty = '近期文献' if paper['novelty'] == 'recent' else '非近期文献（按研究价值选入）'
    lines += [f'[原文]({paper["url"]}) · {novelty} · {level}', '',
              '## 本文研究了什么？', safe_text(paper['summary']), '',
              safe_text(paper['method']), '', safe_text(paper['result']), '',
              '## 有哪些局限或隐含问题？', safe_text(paper['limitations']), '']
    if paper.get('critical_assessment'):
        lines += ['**隐含问题分析（阅读者推断）**', '', safe_text(paper['critical_assessment']), '']
    lines += ['## 对我的研究有什么用，哪里不同？', safe_text(paper['relevance']), '']
    if paper.get('differences'):
        lines += ['**差异与迁移前提**', '', safe_text(paper['differences']), '']
    return '\n'.join(lines)


def section_lines(papers, section, daypath):
    items = [p for p in papers if p['section'] == section]
    return [f'{i}. [{safe_text(p["title_zh"])}](/{daypath}/{slug(p)}) — {safe_text(p["relevance"])}'
            for i, p in enumerate(items, 1)] or ['- 本次无合适推荐。']


def sidebar_block(payload, daypath):
    compact = payload['date'].replace('-', '')
    lines = [f'  * {payload["date"]} <!--dpr-date:{compact}-->',
             f'    * [当日日报](/{daypath}/README)']
    for section, label in [('deep', '精读区'), ('quick', '速读区')]:
        items = [p for p in payload['papers'] if p['section'] == section]
        if not items:
            continue
        lines.append('    * ' + label)
        for paper in items:
            meta = {'title': paper['title'], 'link': paper['url'],
                    'score': str(paper.get('score', 8)),
                    'tags': [{'kind': 'query', 'label': t} for t in paper['topics']],
                    'evidence': paper['relevance']}
            attr = html.escape(json.dumps(meta, ensure_ascii=False), quote=True)
            title = html.escape(paper['title'])
            lines.append(f'      * <a class="dpr-sidebar-item-link dpr-sidebar-item-structured" href="#/{daypath}/{slug(paper)}" data-sidebar-item="{attr}">{title}</a>')
    return '\n'.join(lines) + '\n'


def output_files(payload, repo):
    payload = validate(payload, repo)
    compact = payload['date'].replace('-', '')
    daypath = compact[:6] + '/' + compact[6:]
    papers = payload['papers']
    timestamp = datetime.now(SHANGHAI).isoformat(timespec='seconds')
    lines = [f'# 日报 · {payload["date"]}', '', f'- 生成时间：{timestamp}',
             f'- 当次推荐总数：{len(papers)}',
             f'- 精读区：{sum(p["section"] == "deep" for p in papers)}',
             f'- 速读区：{sum(p["section"] == "quick" for p in papers)}', '',
             '## 今日简报', safe_text(payload['brief']), '',
             '## 精读区', *section_lines(papers, 'deep', daypath), '',
             '## 速读区', *section_lines(papers, 'quick', daypath), '',
             '## 检索记录', safe_text(payload['search_notes']), '',
             *[f'- [检索来源 {i}]({u})' for i, u in enumerate(payload['search_sources'], 1)], '']
    report = '\n'.join(lines)
    outputs = {f'docs/{daypath}/README.md': report,
               f'archive/{compact}/recommend/codex_papers_{compact}.json': json_text(payload)}
    for paper in papers:
        outputs[f'docs/{daypath}/{slug(paper)}.md'] = paper_page(paper)
    metadata = []
    for paper in papers:
        metadata.append({'paper_id': daypath + '/' + slug(paper), 'section': paper['section'],
                         'title_en': paper['title'], 'title_zh': paper['title_zh'],
                         'authors': ', '.join(paper['authors']), 'date': paper['published'],
                         'url': paper['url'], 'doi': paper['id'] if paper['id'].startswith('doi:') else '',
                         'pdf': paper.get('pdf_url', ''), 'score': str(paper.get('score', 8)),
                         'evidence': paper['relevance'], 'tldr': paper['summary'],
                         'tags': ', '.join('query:' + t for t in paper['topics']),
                         'source': paper['source'], 'selection_source': 'codex-subscription',
                         'evidence_level': paper['evidence_level'], 'abstract_en': ''})
        for field in ('critical_assessment', 'differences'):
            if paper.get(field):
                metadata[-1][field] = paper[field]
    outputs[f'docs/{daypath}/papers.meta.json'] = json_text(
        {'label': payload['date'], 'date': payload['date'], 'generated_at': timestamp,
         'count': len(papers), 'papers': metadata, 'errors': []})
    old_sidebar = (repo / 'docs/_sidebar.md').read_text(encoding='utf-8') if (repo / 'docs/_sidebar.md').exists() else '* [首页](/)\n* Daily Papers\n'
    marker = '* Daily Papers\n'
    if marker not in old_sidebar:
        raise ValueError('Daily Papers sidebar marker missing; preserve custom sidebar instead of replacing it')
    outputs['docs/_sidebar.md'] = old_sidebar.replace(marker, marker + sidebar_block(payload, daypath), 1)
    previous = sorted((repo / 'docs').glob('*/*/README.md'), reverse=True)
    history = [f'- [{p.parent.parent.name[:4]}-{p.parent.parent.name[4:]}-{p.parent.name}](/{p.relative_to(repo / "docs").with_suffix("").as_posix()})'
               for p in previous if re.fullmatch(r'\d{6}', p.parent.parent.name) and re.fullmatch(r'\d{2}', p.parent.name)]
    outputs['docs/README.md'] = report + '\n---\n\n## 历史日报\n\n' + '\n'.join(history[:60]) + '\n'
    state = ledger(repo)
    for paper in papers:
        for identity in {paper['id']} | {canonical(v) for v in paper.get('aliases', [])}:
            state['papers'][identity] = {'title': paper['title'], 'recommended_on': payload['date'], 'url': paper['url']}
    state['runs'][payload['date']] = {'count': len(papers), 'generated_at': timestamp,
                                    'path': daypath + '/README', 'generator': 'codex-subscription'}
    outputs['archive/codex/recommendations.json'] = json_text(state)
    return outputs


def render(payload, repo):
    outputs = output_files(payload, repo)
    for name in outputs:
        target = repo / name
        if target.is_symlink() or not target.resolve().is_relative_to(repo.resolve()):
            raise ValueError('Output path leaves repository: ' + name)
        if name not in ('docs/README.md', 'docs/_sidebar.md', 'archive/codex/recommendations.json') and target.exists():
            raise ValueError('Refusing to overwrite an existing dated artifact: ' + name)
    for name, content in outputs.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + '.codex-tmp')
        tmp.write_text(content, encoding='utf-8', newline='\n')
        tmp.replace(target)
    return sorted(outputs)


def git(repo, *args):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    result = subprocess.run(['git', '-c', 'safe.directory=' + str(repo), '-C', str(repo), *args],
                            env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
    if result.returncode:
        raise RuntimeError('Git ' + args[0] + ' failed: ' + result.stderr.strip())
    return result.stdout.strip()


def publish(payload, repo):
    # Never stage user edits or force-push. Inputs are prepared outside the tracked checkout.
    if git(repo, 'branch', '--show-current') != 'main':
        raise ValueError('Publish only from main')
    if git(repo, 'diff', '--name-only') or git(repo, 'diff', '--cached', '--name-only'):
        raise ValueError('Tracked changes exist; do not mix them with a daily report')
    git(repo, 'fetch', 'origin', 'main')
    if git(repo, 'rev-list', '--count', 'origin/main..HEAD') != '0':
        raise ValueError('Unpublished commits exist; inspect them before publishing a report')
    git(repo, 'merge', '--ff-only', 'origin/main')
    names = render(payload, repo)
    git(repo, 'add', '--', *names)
    if set(git(repo, 'diff', '--cached', '--name-only').splitlines()) != set(names):
        raise ValueError('Unexpected staged files; stop')
    git(repo, 'commit', '-m', '[daily] ' + payload['date'] + ' literature report' + TRAILERS)
    commit = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'push', 'origin', 'HEAD:main')
    remote = git(repo, 'ls-remote', 'origin', 'refs/heads/main').split()[0]
    if remote != commit:
        raise RuntimeError('Push finished but remote head verification differed')
    return {'commit': commit, 'files': names, 'remote_verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['history', 'check', 'render', 'publish'])
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.action == 'history':
        state = ledger(repo)
        recent = sorted(state['papers'].items(), key=lambda v: v[1]['recommended_on'], reverse=True)[:60]
        print(json_text({'runs': list(state['runs'])[-14:], 'recommended_count': len(historic_ids(repo)), 'recent': dict(recent)}))
        return
    if not args.input:
        parser.error('--input is required')
    payload = read_json(args.input)
    if args.action == 'check':
        files = output_files(payload, repo)
        result = {'valid': True, 'papers': len(payload['papers']), 'files': sorted(files)}
    elif args.action == 'render':
        result = {'files': render(payload, repo)}
    else:
        result = publish(payload, repo)
    print(json_text(result))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
