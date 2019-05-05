#!/usr/bin/env python3

import frontmatter
import os
import copy

blog_dir = "content/blog"
entries = []
for subdir, dirs, files in os.walk(blog_dir):
    for file in files:
        entries.append(os.path.join(subdir, file))

entries = sorted(entries)

issue_id = 8

modified_entries = {}

for entry in entries:
    with open(entry) as f:
        post = frontmatter.load(f)
        post_ = copy.deepcopy(post)
        post_['ghcommentid'] = issue_id
        issue_id += 1
        modified_entries[entry] = frontmatter.dumps(post_)

for entry in entries:
    print(entry)
    with open(entry, "w") as f:
        print(modified_entries[entry])
        f.write(modified_entries[entry])
