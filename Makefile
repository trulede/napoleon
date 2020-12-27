
.PHONY: default build docker install push lint clean cleanall

default: build

build:
	python3 setup.py sdist bdist_wheel

install:
	pip install -e .

docker:
	docker build -f docker/Dockerfile --tag napoleon:latest .

push:
	docker push localhost:32000/napoleon:latest

lint:
	pylint napoleon

clean:
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./*.egg-info
	py3clean .

cleanall: clean
	docker ps --filter status=dead --filter status=exited -aq | xargs -r docker rm -v
	docker images -qf dangling=true | xargs -r docker rmi
	docker images -q | xargs -r docker rmi -f
