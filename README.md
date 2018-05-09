# breeze-ci

## `breeze require [package]`
- wraps `pipenv`
- runs `pipenv install [package]`

## `breeze test`
- locally runs tests as specified in `breeze.yml`

## `breeze deploy`
- runs `breeze test` and breaks if it fails
- adds all changes to git
- prompts for commit message
- pushes to repo
