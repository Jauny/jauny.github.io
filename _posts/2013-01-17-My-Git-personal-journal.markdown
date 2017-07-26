---
id: 5
title: My Git personal journal
date: 2013-01-17
layout: post
---

__how git works__
https://codewords.recurse.com/issues/two/git-from-the-inside-out

# remove a file
```ruby
$ git rm /file/path
```
Deletes the file and removes it from the git tracking at the same time.

# add all the removed files
```ruby
$ git add -u
```
Add all deleted files at once instead of doing git rm /file/name for each file

# amend
```ruby
$ git commit --amend
```
Insert a forgotten change to the last commit, so you don't have to make a new commit for a quick addition.

# branch
_rename a branch_

```ruby
$ git branch -m oldname newname
```
_push to origin._ __(will create the remote branch if it doesn't already exist)__

```ruby
$ git push origin branchname
```

# Remote actions
## get info on all locals and remote branches
```ruby
git remote show origin
```
## rebase
```ruby
$ git rebase origin/master
```
Like pull but puts local commits on the side for the update, then merge the local commits, making merges conflicts about the addition of the local changes, versus the addition of origin's changes on top of local.

```ruby
$ git rebase -i
```
Allows to merge multiple commits in one, so you make cleaner pushes to origin and keep a clean local logs.

```ruby
$ git rebase -i <commit>
$ pick -> e commit
// do modifications
$ git add .
$ git commit --amend
$ git rebase --continue
```
Allows to make modification to a previous commit

## Push to staging
_after having rebased origin/branchname of course_

```
git push -f staging head:master
```
*staging is the name of the app on heroku
*head is the branch you're on
*master is the branch you wanna push onto

## get logs from staging

```
heroku logs --tail --remote staging
```
*--tail means live stream of logs
*--remore is where the app is
*staging is the name of the app
  