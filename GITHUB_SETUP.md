# GitHub setup — private working repository

The manuscript is not yet ready for publication. Start with a **private** repository and decide on a public license later.

## If GitHub CLI (`gh`) is installed and authenticated

```bash
# From the unzipped LA-SENSEI directory:
git init
git add .
git commit -m "Initial LA-SENSEI structural companion"
git branch -M main
gh repo create LA-SENSEI --private --source=. --remote=origin --push
```

If you have already created an empty private `LA-SENSEI` repository on GitHub, skip `gh repo create` and run:

```bash
git init
git add .
git commit -m "Initial LA-SENSEI structural companion"
git branch -M main
git remote add origin https://github.com/YOUR-USER/LA-SENSEI.git
git push -u origin main
```

Replace `YOUR-USER` with your GitHub username or organization. Do not run both alternatives. A remote repository must already exist for the second alternative.

## Validate before sharing

```bash
python -m pip install -e '.[test]'
python -m pytest -q
la-sensei lab similarity
```

## Publication status

All rights reserved: see `NOTICE.md`. This is **not yet** a publicly licensed book companion. Review code, exercises, attribution, and licensing before changing repository visibility.
