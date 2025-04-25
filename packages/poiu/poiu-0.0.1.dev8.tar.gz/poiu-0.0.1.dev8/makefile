# .PHONY informa ao make que o target não é um arquivo
.PHONY: bump-pre-release-number bump-pre-release-label bump-patch bump-minor bump-major 

.PHONY: bump-show-pre-release-number bump-show-pre-release-label bump-show-patch bump-show-minor bump-show-major bump-show-bump 

bump-pre-release-number:
	bump-my-version bump pre_n 

bump-pre-release-label:
	bump-my-version bump pre_l

bump-patch:
	bump-my-version bump patch

bump-minor:
	bump-my-version bump minor

bump-major:
	bump-my-version bump major

bump-show-pre-release-number:
	bump-my-version show --increment pre_n new_version 

bump-show-pre-release-label:
	bump-my-version show --increment pre_l new_version 

bump-show-patch:
	bump-my-version show --increment patch new_version

bump-show-minor:
	bump-my-version show --increment minor new_version 

bump-show-major:
	bump-my-version show --increment major new_version 

bump-show-bump:
	bump-my-version show-bump
