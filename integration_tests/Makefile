test-setup: egg-info bus

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

bus-test: egg-info
	docker build -t xivo-bus-test -f Dockerfile-bus ..

.PHONY: test-setup test egg-info bus
