test-setup: egg-info bus-test

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

bus-test: egg-info
	docker build -t xivo-bus-test -f docker/Dockerfile-bus ..

.PHONY: test-setup test egg-info bus
