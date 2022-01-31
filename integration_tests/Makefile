test-setup: egg-info bus

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

bus: egg-info
	docker build -t xivo-bus -f Dockerfile-bus ..

.PHONY: test-setup test egg-info bus
