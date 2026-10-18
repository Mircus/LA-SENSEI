import json
from pathlib import Path
from lasensei.lab_registry import RUNNERS as labs
from lasensei.chapter_demos import RUNNERS as chapters

ROOT=Path(__file__).resolve().parents[1]


def test_all_six_labs_run_and_return_evidence():
    assert len(labs)==6
    for func in labs.values():
        assert func()


def test_all_fourteen_chapter_workshops():
    assert list(chapters)==list(range(1,15))
    for func in chapters.values():
        assert func()


def test_exercise_crosswalk_integrity():
    entries=json.loads((ROOT/'exercises'/'index.json').read_text())
    assert len(entries)==69
    ids=[e['id'] for e in entries]
    assert len(set(ids))==69
    for e in entries:
        assert (ROOT/'exercises'/f'ch{e["chapter"]:02}.md').exists()
        if e['output_key']:
            assert e['output_key'] in chapters[e['chapter']]()
    assert sum(e['implementation']=='worked-computational' for e in entries)==32
    assert sum(e['implementation']=='partial-demonstration' for e in entries)==2
