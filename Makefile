GIT_REPO=https://github.com/nathankrueger/rpi2_blink_led

# Git stuff
co:
	git add $(FILES)

ci:
	git commit

rm:
	git rm $(FILES)

push:
	git push origin master

pull:
	git pull origin master

revert:
	git reset

repo:
	open $(GIT_REPO)

clean:
	rm *.pyc
