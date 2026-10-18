# Wiki maintenance

Wiki page sources live in `docs/wiki/`. Content is in English to match the
project README. `_Sidebar.md` and `_Footer.md` provide GitHub Wiki navigation.
The top-level README remains available as the existing package documentation.

GitHub hosts the Wiki in a separate repository. Editing these source files does
not publish them. These instructions perform publication only when run manually.

1. Enable Wikis under the repository's Settings → General → Features, if needed.
2. Open the repository's Wiki tab and create its initial Home page if none exists.
3. Clone the Wiki alongside the project (from the project root):

```bash
git clone https://github.com/tanerim/ts_tokenizer.wiki.git ../ts_tokenizer.wiki
```

4. Copy the reviewed Markdown pages, including the sidebar and footer:

```bash
cp docs/wiki/*.md ../ts_tokenizer.wiki/
git -C ../ts_tokenizer.wiki status --short
git -C ../ts_tokenizer.wiki diff
```

5. Review existing pages before staging, then publish:

```bash
git -C ../ts_tokenizer.wiki add -- '*.md'
git -C ../ts_tokenizer.wiki commit -m "Document TS Tokenizer 0.3.0"
git -C ../ts_tokenizer.wiki push
```

No files are deleted by this workflow. Resolve differences with any existing
Wiki content before publishing. Wiki links deliberately use page names without
`.md`, as expected by GitHub Wiki; browse them on GitHub after publication.
Add the public Wiki link to the project README after it is live.

When API behavior changes, update the relevant page and the version labels in
Home and the sidebar. Keep the README's quick-start examples consistent.

GitHub references:

- [Managing Wiki pages](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages)
- [Custom sidebar and footer](https://docs.github.com/en/communities/documenting-your-project-with-wikis/creating-a-footer-or-sidebar-for-your-wiki)
