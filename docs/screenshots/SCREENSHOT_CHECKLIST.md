# Manual screenshot checklist

Use screenshots only after rechecking the current PR head and status.

## PR #216 checks

- URL: <https://github.com/Tencent/YOLO-Master/pull/216/checks>
- Required state: all required checks for the current head must be completed and passing.
- Include: PR number, current short commit SHA, checks summary, and visible successful required checks.
- Crop: GitHub page body only.
- Remove: browser chrome, bookmarks, account avatar/menu, email, notifications, tokens, and unrelated tabs.
- Filename: `pr216-ci-passed.png`.
- README placement: at most one optional image under upstream contribution status.
- Current audit note: `dd490a8` had 9 passed, 3 pending, and 5 skipped checks on 2026-08-03; do not use an older green run as a substitute.

## PR #216 overview

- URL: <https://github.com/Tencent/YOLO-Master/pull/216>
- Include: title, PR number, Draft/Open state, base/head branches, and current head commit.
- Crop/remove: same privacy requirements as above.
- Filename: `pr216-overview.png`.

## Local validator

- Run the public validators from a clean checkout.
- Include only the PASS summary, repository name, and validated revision.
- Exclude terminal username, prompt path, environment variables, and machine details.
- Filename: `validator-pass.png`.

