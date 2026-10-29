# Publishing checklist (for the owner)

Run from the private project, never by hand inside this folder:

```bash
.venv/bin/python tools/export_public.py     # rebuilds github/mastermind/ from the allowlist
cd github/mastermind && git add -A && git commit -m "Brain update" && git push
```

Once, after the first push, on github.com:
1. Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/docs`. The map is live at `https://srijxnj.github.io/mastermind/` within a minute.
2. Settings → General → Social preview → upload `docs/social-preview.png`.
3. About (gear icon on the repo page) → description: *An open-source second brain that turns Claude Code into your social media manager.* Website: the Pages URL. Topics: `claude-code` `instagram` `reels` `content-creation` `second-brain` `knowledge-graph` `local-first` `ai-agent` `creator-tools` `short-form-video`.
