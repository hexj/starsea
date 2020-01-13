#!/usr/bin/env bash
git filter-branch -f --prune-empty --index-filter 'git rm -rf --cached --ignore-unmatch '$1'' --tag-name-filter cat -- --all
# git filter-branch --index-filter 'git rm -r -q --cached --ignore-unmatch '$1'' --prune-empty --tag-name-filter cat -- --all

rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now
git gc  --auto --aggressive --prune=now
