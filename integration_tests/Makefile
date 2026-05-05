test-setup: bus-test bus-documentation

test:
	pytest -x

bus-documentation:
	docker build -t local/bus-documentation-test -f ../contribs/Dockerfile ..

bus-test:
	docker build -t local/bus-test -f docker/Dockerfile-bus ..

.PHONY: test-setup test bus-test bus-documentation
