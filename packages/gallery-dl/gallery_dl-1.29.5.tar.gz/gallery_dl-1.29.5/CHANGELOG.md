## 1.29.5 - 2025-04-26
### Extractors
#### Additions
- [bluesky] add `video` extractor ([#4438](https://github.com/mikf/gallery-dl/issues/4438))
- [instagram] add `followers` extractor ([#7374](https://github.com/mikf/gallery-dl/issues/7374))
- [itaku] add `stars` extractor ([#7411](https://github.com/mikf/gallery-dl/issues/7411))
- [pictoa] add support ([#6683](https://github.com/mikf/gallery-dl/issues/6683) [#7409](https://github.com/mikf/gallery-dl/issues/7409))
- [twitter] add `followers` extractor ([#6331](https://github.com/mikf/gallery-dl/issues/6331))
#### Fixes
- [architizer] fix `project` extractor ([#7421](https://github.com/mikf/gallery-dl/issues/7421))
- [bluesky:likes] fix infinite loop ([#7194](https://github.com/mikf/gallery-dl/issues/7194) [#7287](https://github.com/mikf/gallery-dl/issues/7287))
- [deviantart] fix `401 Unauthorized` errors for for multi-image posts ([#6653](https://github.com/mikf/gallery-dl/issues/6653))
- [everia] fix `title` extraction ([#7379](https://github.com/mikf/gallery-dl/issues/7379))
- [fanbox] fix `comments` extraction
- [fapello] stop pagination on empty results ([#7385](https://github.com/mikf/gallery-dl/issues/7385))
- [kemonoparty] fix `archives` option ([#7416](https://github.com/mikf/gallery-dl/issues/7416) [#7419](https://github.com/mikf/gallery-dl/issues/7419))
- [pixiv] fix `user_details` requests not being cached ([#7414](https://github.com/mikf/gallery-dl/issues/7414))
- [pixiv:novel] handle exceptions during `embeds` extraction ([#7422](https://github.com/mikf/gallery-dl/issues/7422))
- [subscribestar] fix username & password login
- [wikifeet] support site redesign ([#7286](https://github.com/mikf/gallery-dl/issues/7286) [#7396](https://github.com/mikf/gallery-dl/issues/7396))
#### Improvements
- [bluesky:likes] use `repo.listRecords` endpoint ([#7194](https://github.com/mikf/gallery-dl/issues/7194) [#7287](https://github.com/mikf/gallery-dl/issues/7287))
- [gelbooru] don't hardcode image server domains ([#7392](https://github.com/mikf/gallery-dl/issues/7392))
- [instagram] support `/share/` URLs ([#7241](https://github.com/mikf/gallery-dl/issues/7241))
- [kemonoparty] use `/posts-legacy` endpoint ([#6780](https://github.com/mikf/gallery-dl/issues/6780) [#6931](https://github.com/mikf/gallery-dl/issues/6931) [#7404](https://github.com/mikf/gallery-dl/issues/7404))
- [naver] support videos ([#4682](https://github.com/mikf/gallery-dl/issues/4682) [#7395](https://github.com/mikf/gallery-dl/issues/7395))
- [scrolller] support album posts ([#7339](https://github.com/mikf/gallery-dl/issues/7339))
- [subscribestar] add warning for missing login cookie
- [twitter] update API endpoint query hashes ([#7382](https://github.com/mikf/gallery-dl/issues/7382) [#7386](https://github.com/mikf/gallery-dl/issues/7386))
- [weasyl] use `gallery-dl` User-Agent header ([#7412](https://github.com/mikf/gallery-dl/issues/7412))
#### Metadata
- [deviantart:stash] extract more metadata ([#7397](https://github.com/mikf/gallery-dl/issues/7397))
- [moebooru:pool] replace underscores in pool names ([#4646](https://github.com/mikf/gallery-dl/issues/4646))
- [naver] fix recent `date` bug ([#4682](https://github.com/mikf/gallery-dl/issues/4682))
### Post Processors
- [ugoira] restore `keep-files` functionality ([#7304](https://github.com/mikf/gallery-dl/issues/7304))
- [ugoira] support `"keep-files": true` + custom extension ([#7304](https://github.com/mikf/gallery-dl/issues/7304))
- [ugoira] use `_ugoira_frame_index` to detect `.zip` files
### Miscellaneous
- [util] auto-update Chrome version
- use internal version of `re.compile()` for extractor patterns
