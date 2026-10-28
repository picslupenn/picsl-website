Visit **[picsl.upenn.edu](http://picsl.upenn.edu)** 🚀

# PICSL website

Static website for the Penn Image Computing and Science Laboratory, replacing the old
WordPress site at https://picsl.upenn.edu. Built with Jekyll on the
[Lab Website Template](https://github.com/greenelab/lab-website-template)
([documentation](https://greene-lab.gitbook.io/lab-website-template-docs)).
The `protowebsite` repository in the same organization is an earlier draft of the site
that is no longer used; make changes here instead.

The easiest way to update the site is to ask [Claude Code](https://claude.com/claude-code)
to do it, then open a pull request. The tutorial below walks through that. If you have
write access to the repository, you can also
[ask Claude in a GitHub issue](#updating-the-website-from-a-github-issue) without
installing anything.

## Updating the website with Claude Code

### One-time setup

Lab members don't need write access to the repository. You work on your own copy (a
*fork*) and propose changes with a pull request, which a lab admin reviews and merges.

1. Install [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), and make
   sure you have `git`, the GitHub CLI (`gh`) and Ruby with Bundler. On a Mac,
   `brew install git gh ruby` covers all of these. Log in to GitHub with `gh auth login`.
2. Fork and clone the repository, then start Claude Code in it:

   ```sh
   gh repo fork picslupenn/picsl-website --clone
   cd picsl-website
   claude
   ```

   `gh repo fork --clone` creates your fork on GitHub, clones it, and sets the lab's
   repository up as the `upstream` remote.
3. Ask Claude to get the site running locally:

   > Install what's needed and show me how to preview the site locally.

   Claude runs `bundle install`, then starts `bundle exec jekyll serve`. Open
   http://localhost:4000 to see the site. It rebuilds when files change, so you can leave
   it running while you work.

### Making a change

Each change follows the same loop: start a branch, describe what you want in plain
language, check the result, refine, and open a pull request.

**1. Start from a fresh branch.** Your fork doesn't update itself, so bring it up to date
with the lab's repository first:

> Sync my fork with the lab's repository and create a branch called update-my-profile.

**2. Describe the change.** Be specific and point Claude to sources. Claude can read web
pages, download images, look up papers in PubMed and ORCID, and edit the site files.
Some requests that have worked well:

- *Team:*
  > Add Jane Doe as a PhD student, using her profile at https://example.edu/jane.
  > Use her photo, cropped so the circle is centered on her face.

  > Move John Smith to alumni.

  > Update my photo and positions from my Penn faculty page: https://www.med.upenn.edu/apps/faculty/index.php/...

- *Research highlights:*
  > Write a post for the Research page about our new paper, doi:10.xxxx/yyyy.
  > Use a figure from the paper if its license allows it.

  > Find my most impressive last-author papers from 2025 and write a featured post for each.

- *Fixes:*
  > The thumbnails on the Software page are cropped strangely. Can you fix that?

  > Check all the links on my member page and fix any that are broken.

- *New pages:*
  > Add a Jobs page to the menu with a posting for a postdoc position. Here is the ad: ...

You can paste screenshots into Claude Code to show what looks wrong.

**3. Check the result.** Look at the page at http://localhost:4000, or ask Claude to take
screenshots and review them. Tell Claude what to change ("the photo is too zoomed in",
"move this section to the bottom", "that's not my Google Scholar ID") and repeat until
you're happy.

Check facts yourself, especially names, roles, IDs and anything summarizing a paper.
Claude writes research posts from the abstract and should say when it's unsure, but you
know the work best.

**4. Open a pull request.** When you're done:

> Commit these changes and open a pull request to the lab's repository.

Claude commits to your branch, pushes it to your fork, and opens a pull request (PR)
against `picslupenn/picsl-website` describing the change. Then:

- A lab admin approves the automated checks. GitHub requires this for first-time
  contributors.
- A bot then comments on the PR with a **preview link** showing the whole site with your
  changes. Check it, especially on a phone.
- The admin reviews the PR. If they ask for changes, describe them to Claude on the same
  branch and push again; the PR and its preview update automatically.
- Once the PR is merged, the live site updates automatically within a few minutes.

For your next change, start again at step 1 so your new branch starts from the latest
version of the site.

### Tips

- **Images:** photos should be square and centered on the face, since the site shows them
  in a circle. Ask Claude to remove photo metadata (EXIF), which can include GPS location.
- **Figures from papers:** only reuse figures whose license allows it (for example
  CC BY), and credit them. Ask Claude to check the license. When reuse isn't allowed,
  Claude can draw a simple diagram instead, or you can supply one of your own figures.
- **Publications:** the Publications page is generated automatically from the ORCID
  records in `_data/orcid.yaml`. To fix or add papers, update your ORCID record; the site
  checks for updates weekly and opens a citation-update PR. PRs and pushes refresh
  citations only when citation inputs, generator code, or citation workflows change.
  To pull in ORCID changes immediately, run `update-citations` manually on `main` in
  GitHub Actions, then run `build-site` on `main` after it finishes.
- **Name variants in publications:** If your name in papers is different from your name on
  the site, or if you have name variants, you can use `aliases` to help the site find your
  papers (see Jim Gee's page for anexample). The search on the Publications page is
  case-insensitive but IS sensitive to punctuation.
- **Big changes:** for something large, such as a redesign or many new pages, ask Claude
  to propose a plan first.

## Updating the website from a GitHub issue

People with write access to this repository (lab admins) can ask Claude for a change
directly on GitHub, without cloning anything:

1. [Open an issue](https://github.com/picslupenn/picsl-website/issues/new) that describes
   the change and mentions `@claude` in the title or body. The same kinds of requests as
   above work, for example:

   > @claude Add Jane Doe as a PhD student, using her profile at https://example.edu/jane.

   Drag images into the issue to attach them, such as a photo for a member page.
2. A Claude workflow runs in GitHub Actions and replies on the issue with its progress.
   It follows the same rules as Claude Code locally (`CLAUDE.md`). It makes the change on
   a `claude/issue-…` branch, builds the site, and checks the links.
3. Claude's reply links to the branch and to a page for opening a pull request. Open the
   PR, check its preview link, and review it like any other PR.

To refine the change, comment on the issue or the PR and mention `@claude` again. If
Claude says it's blocked, for example because the workflow doesn't allow a command it
needs, the permissions are set in `claude_args` in `.github/workflows/claude.yml`.

Mentions of `@claude` from people without write access are ignored, so lab members
working in a fork should use Claude Code as described above.

## For admins: reviewing pull requests

1. On a PR from a new contributor, click **Approve and run** so the checks and preview
   build can run.
2. Open the preview link that the bot posts in the PR comments and look over the changes.
   The **Files changed** tab shows exactly what was edited.
3. Ask for changes in a review comment, or merge with **Squash and merge**. The live site
   updates within a few minutes.

Admins can also make changes directly with Claude Code in a clone of the lab's
repository. To add or remove admins, change people's roles in the
[picslupenn organization](https://github.com/orgs/picslupenn/people), or give them the
Maintain or Admin role on this repository. Everyone else contributes through forks and
needs no access.

## Where things live

| What | Where |
|---|---|
| Team members | `_members/<name>.md` (`role`: `principal-investigator`, `faculty`, `research-associate`, `staff`, `postdoc`, `phd`, `alumni`; add `group: alum` for alumni) |
| Photos of team members | `images/members/` |
| Research and software cards | `_data/projects.yaml` (tag `research` or `software`) |
| Research posts | `research/<slug>.md`, with images in `images/research/` |
| Software pages | `software/<slug>.md` |
| Publications | faculty ORCID IDs in `_data/orcid.yaml`, or individual DOIs in `_data/sources.yaml`. The `update-citations` workflow generates `_data/citations.yaml`; don't edit that file. |
| Navigation menu | the `nav:` block at the top of each top-level page (`about/`, `research/`, `team/`, etc.) |
| Site title, links, footer | `_config.yaml` |
| Colors and fonts | `_styles/-theme.scss` |

Pages migrated from the old site keep their old URLs through `redirect_from` front
matter, so old links and bookmarks still work.

## Running locally without Claude Code

```sh
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Deployment

Merges to `main` are built and deployed to GitHub Pages by the workflows in
`.github/workflows/`. Pull requests get a preview build automatically.

Moving the site to picsl.upenn.edu is prepared in pull request
[#1](https://github.com/picslupenn/picsl-website/pull/1). That PR lists the DNS changes
Penn IT needs to make, and should be merged only after DNS has changed.

## Migration from WordPress

`tools/migrate_wp.py` did the one-time import from the WordPress site. It scraped the
pages listed in the WordPress sitemaps, using Wayback Machine copies for pages that
failed on the live site, and downloaded media into `images/wp/`. It is kept for
reference. Don't re-run it: it would overwrite pages that have been edited since.
