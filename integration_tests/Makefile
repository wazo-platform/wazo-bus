test-setup: egg-info bus-test bus-documentation

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

bus-documentation:
	docker build -t local/bus-documentation-test -f ../contribs/Dockerfile ..

bus-test: egg-info
	docker build -t local/bus-test -f docker/Dockerfile-bus ..

.PHONY: test-setup test egg-info bus-test bus-documentation
