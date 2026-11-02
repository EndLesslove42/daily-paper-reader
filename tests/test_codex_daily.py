"""Publication boundaries and archive compatibility for the no-API daily path."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'tools/codex/publish_daily.py'
spec = importlib.util.spec_from_file_location('codex_daily', TOOL)
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)


class DailyPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        (self.repo/'docs').mkdir()
        self.sidebar = '* [首页](/)\n* Daily Papers\n  * 2026-10-01 <!--dpr-date:20261001-->\n    * old paper\n'
        (self.repo/'docs/_sidebar.md').write_text(self.sidebar, encoding='utf-8')
        self.payload = {
            'date': '2026-11-02', 'generator': 'codex-subscription',
            'brief': '新的沉降方法。', 'search_notes': '查过近期原始论文。',
            'search_sources': ['https://gmd.copernicus.org/'],
            'papers': [{'id': 'doi:10.5194/example-2026', 'title': 'Surface exchange',
                        'title_zh': '地表交换', 'authors': ['A. Author'], 'published': '2026-10-29',
                        'url': 'https://gmd.copernicus.org/articles/example/', 'source': 'GMD',
                        'section': 'quick', 'topics': ['surface-exchange'],
                        'evidence_level': 'abstract', 'summary': '研究沉降。', 'method': '阻力模型。',
                        'result': '方法可检验。', 'relevance': '可比较Vd。',
                        'limitations': '仅摘要，不做全文评价。', 'novelty': 'recent'}],
        }

    def test_compatible_pages_and_preserved_history(self):
        names = daily.render(copy.deepcopy(self.payload), self.repo)
        sidebar = (self.repo/'docs/_sidebar.md').read_text(encoding='utf-8')
        self.assertIn('old paper', sidebar)
        self.assertIn('<!--dpr-date:20261102-->', sidebar)
        self.assertIn('dpr-sidebar-item-structured', sidebar)
        self.assertIn('#/202611/02/codex-', sidebar)
        meta = json.loads((self.repo/'docs/202611/02/papers.meta.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['count'], 1)
        page = (self.repo/next(n for n in names if '/codex-' in n and n.endswith('.md'))).read_text(encoding='utf-8')
        self.assertTrue(page.startswith('---\ntitle: '))
        self.assertIn('selection_source: "codex-subscription"', page)
        self.assertIn('仅核对摘要', page)
        self.assertNotIn('api_key', page)

    def test_same_day_is_idempotent_and_other_dates_cannot_repeat_a_paper(self):
        daily.render(copy.deepcopy(self.payload), self.repo)
        with self.assertRaisesRegex(ValueError, 'already published'):
            daily.output_files(copy.deepcopy(self.payload), self.repo)
        other = copy.deepcopy(self.payload)
        other['date'] = '2026-11-01'
        with self.assertRaisesRegex(ValueError, 'Already recommended'):
            daily.output_files(other, self.repo)

    def test_legacy_arxiv_version_and_publisher_alias_are_deduplicated(self):
        day = self.repo/'docs/202610/01'
        day.mkdir(parents=True)
        (day/'2610.12345v1-old-paper.md').write_text('old', encoding='utf-8')
        self.payload['papers'][0]['aliases'] = ['https://arxiv.org/abs/2610.12345v3']
        with self.assertRaisesRegex(ValueError, 'Already recommended'):
            daily.output_files(self.payload, self.repo)

    def test_empty_day_keeps_navigation_and_records_actual_search(self):
        self.payload['papers'] = []
        daily.render(self.payload, self.repo)
        self.assertIn('本次无合适推荐', (self.repo/'docs/README.md').read_text(encoding='utf-8'))
        self.assertIn('当日日报', (self.repo/'docs/_sidebar.md').read_text(encoding='utf-8'))
        self.assertIn('2026-11-02', daily.ledger(self.repo)['runs'])

    def test_bad_metadata_fails_before_writing_anything(self):
        bad = copy.deepcopy(self.payload['papers'][0])
        bad['id'] = 'doi:10.5194/second'
        bad['published'] = '2027-01-01'
        self.payload['papers'].append(bad)
        with self.assertRaises(ValueError):
            daily.render(self.payload, self.repo)
        self.assertFalse((self.repo/'docs/202611').exists())
        self.assertEqual((self.repo/'docs/_sidebar.md').read_text(encoding='utf-8'), self.sidebar)

    def test_abstract_cannot_be_marked_deep_and_old_paper_needs_backfill_label(self):
        self.payload['papers'][0]['section'] = 'deep'
        with self.assertRaisesRegex(ValueError, 'Full text'):
            daily.validate(self.payload, self.repo)
        self.payload['papers'][0]['section'] = 'quick'
        self.payload['papers'][0]['published'] = '2025-01-01'
        with self.assertRaisesRegex(ValueError, 'Older papers'):
            daily.validate(self.payload, self.repo)

    def test_unsafe_urls_are_rejected(self):
        for url in ['javascript:alert(1)', 'http://example.org', 'https://user:pass@example.org', 'https://localhost/x']:
            self.payload['papers'][0]['url'] = url
            with self.assertRaises(ValueError):
                daily.validate(self.payload, self.repo)

    def init_git_remote(self):
        origin = self.repo.parent / (self.repo.name + '-origin.git')
        self.addCleanup(lambda: __import__('shutil').rmtree(origin, ignore_errors=True))
        daily.git(self.repo, 'init', '--bare', str(origin))
        daily.git(self.repo, 'init', '-b', 'main')
        daily.git(self.repo, 'config', 'user.name', 'Test Author')
        daily.git(self.repo, 'config', 'user.email', 'test@example.org')
        daily.git(self.repo, 'add', '--', 'docs/_sidebar.md')
        daily.git(self.repo, 'commit', '-m', 'Initial sidebar')
        daily.git(self.repo, 'remote', 'add', 'origin', str(origin))
        daily.git(self.repo, 'push', '-u', 'origin', 'main')

    def test_publish_pushes_only_report_files_and_verifies_remote(self):
        self.init_git_remote()
        (self.repo/'unrelated.txt').write_text('user draft', encoding='utf-8')
        result = daily.publish(copy.deepcopy(self.payload), self.repo)
        self.assertTrue(result['remote_verified'])
        self.assertNotIn('unrelated.txt', daily.git(self.repo, 'show', '--pretty=', '--name-only', 'HEAD'))
        self.assertIn('Co-Authored-By:', daily.git(self.repo, 'log', '-1', '--format=%B'))
        self.assertIn('?? unrelated.txt', daily.git(self.repo, 'status', '--short'))

    def test_publish_stops_on_user_tracked_changes(self):
        self.init_git_remote()
        (self.repo/'docs/_sidebar.md').write_text(self.sidebar + 'user edit\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Tracked changes'):
            daily.publish(copy.deepcopy(self.payload), self.repo)
        self.assertFalse((self.repo/'archive').exists())


if __name__ == '__main__':
    unittest.main()
