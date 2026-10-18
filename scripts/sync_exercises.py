"""Regenerate manuscript-faithful worksheets from a local LaTeX source tree.

Usage: python scripts/sync_exercises.py /path/to/unzipped/chapters
"""
import argparse, re, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Regenerate exercise worksheets from the book chapters')
parser.add_argument('source_dir', type=Path, help='folder with ch01.tex...ch14.tex')
arguments=parser.parse_args()
SRC=arguments.source_dir
sys.path.insert(0,str(ROOT/'src'))
from lasensei.chapter_demos import RUNNERS as chapter_runners


def latex_md(txt):
    txt = txt.replace('\\,', ' ').replace('\\emph{','*').replace('\\textbf{','**')
    # restore formatting created by the above substitutions, if any
    txt = re.sub(r'\\mat\{([^{}]*)\}', lambda m: r'\begin{pmatrix}' + m.group(1) + r'\end{pmatrix}', txt)
    for k,v in {'\\F':r'\mathbb{F}', '\\R':r'\mathbb{R}', '\\C':r'\mathbb{C}', '\\Z':r'\mathbb{Z}', '\\GL':r'\operatorname{GL}', '\\diag':r'\operatorname{diag}', '\\tr':r'\operatorname{tr}', '\\Hom':r'\operatorname{Hom}', '\\rank':r'\operatorname{rank}'}.items():
        txt=txt.replace(k,v)
    txt=txt.replace('\\"u', 'ü').replace('\\"o','ö').replace('\\"a','ä')
    txt=txt.replace('---','—').replace('--','–')
    return ' '.join(txt.split())

all_ex=[]
for ch in range(1,15):
    tex=(SRC/f'ch{ch:02}.tex').read_text()
    title=latex_md(re.search(r'\\chapter\{([^}]*)\}',tex).group(1))
    part=tex.split('\\exercises',1)[1]
    hits=re.findall(r'\\item\s+\\level\{([^}]*)\}\s+(.*?)(?=\n\\item|\n\\end\{enumerate\})', part, re.S)
    demonstrations=chapter_runners[ch]()
    lines=[f'# Chapter {ch}: {title}', '',
           'Source: *Linear Algebra: One Language, Many Dialects*, draft manuscript (October 2026).',
           'Exercise numbering follows the source chapter exactly. Proof-based problems are intentionally not replaced by numerical examples.', '',
           f'Run the workshop: `la-sensei chapter {ch}`', '',
           '## Exercises', '']
    for i,(level,prompt) in enumerate(hits,1):
        exercise_id=f'E{ch:02}.{i:02}'
        output_keys=[key for key in demonstrations if key==exercise_id or key==exercise_id+'_PARTIAL']
        support='worked-computational' if exercise_id in output_keys else 'partial-demonstration' if output_keys else 'reader-proof-or-exploration'
        # exclude proofs from evidence of solution; flag this as a computational demo only
        label={'worked-computational':'Runnable worked instance',
               'partial-demonstration':'Partial computational evidence',
               'reader-proof-or-exploration':'Reader proof / discussion / exploration'}[support]
        prompt=latex_md(prompt)
        lines += [f'### {exercise_id} — {level}', '', prompt, '',f'**Companion status:** {label}.', '']
        if output_keys:
            lines += [f'Check result: `la-sensei chapter {ch}` → `{output_keys[0]}`.', '']
        else:
            lines += ['**Suggested method:** Give the abstract argument first; if computing examples, state which additional assumptions you used.', '']
        all_ex.append(dict(id=exercise_id,chapter=ch,chapter_title=title,
                           kind=level,source_text=prompt,implementation=support,
                           command=f'la-sensei chapter {ch}' if output_keys else None,
                           output_key=output_keys[0] if output_keys else None))
    lines += ['## Further comparison', '',
              'Which statements in these exercises depend on the scalar field, on characteristic, or on positivity? Identify the exact hypothesis before generalizing.', '',
              '[Book-wide exercise map](../EXERCISE_MAP.md) · [Return to README](../README.md)', '']
    (ROOT/'exercises'/f'ch{ch:02}.md').write_text('\n'.join(lines))

(ROOT/'exercises'/'index.json').write_text(json.dumps(all_ex,indent=2,ensure_ascii=False)+'\n')
worked=[e for e in all_ex if e['implementation']=='worked-computational']
partial=[e for e in all_ex if e['implementation']=='partial-demonstration']
reader=[e for e in all_ex if e['implementation']=='reader-proof-or-exploration']
outline=['# Exercise crosswalk', '',
         f'The supplied draft contains **{len(all_ex)} numbered chapter exercises** ({len(worked)} runnable worked instances, {len(partial)} partial demonstrations, and {len(reader)} theoretical/reader investigations).', '',
         'Six additional extended laboratories are implemented in `labs/` and as notebooks in `notebooks/`.', '',
         '**Important:** a program that confirms examples is not a substitute for a proof; several runnable entries provide answers to the computational part only.', '',
         '| Book ID | Type | Companion mode | Location |', '|---|---|---|---|']
for ex in all_ex:
    kind=ex['implementation'].replace('reader-proof-or-exploration','theoretical / reader').replace('worked-computational','worked instance').replace('partial-demonstration','partial evidence')
    outline.append(f"| {ex['id']} | {ex['kind']} | {kind} | [worksheet](exercises/ch{ex['chapter']:02}.md) · `la-sensei chapter {ex['chapter']}` |" if ex['command'] else f"| {ex['id']} | {ex['kind']} | {kind} | [worksheet](exercises/ch{ex['chapter']:02}.md) |")
outline += ['', 'Generated against the **October 2026 LaTeX draft**. If the exercise order or text changes, regenerate and review this mapping; do not silently reuse exercise IDs.', '']
(ROOT/'EXERCISE_MAP.md').write_text('\n'.join(outline))
print('Exercises:',len(all_ex),'runnable:',len(worked),'partial:',len(partial),'theory:',len(reader))
