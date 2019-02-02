IMAGE_NAME=imagenet_download
PORT=8000
VPATH = outputs/
INC=config.yaml

build:
	docker build -t $(IMAGE_NAME) .

dev:
	docker run --rm -ti -p $(PORT):$(PORT) \
		-v $(PWD)/:/project \
		-w '/project' $(IMAGE_NAME)

test:
	export PYTHONPATH=imagenet
	python3 -m pytest imagenet


wordnet_mapping.json:
	python3 imagenet/create_wordnet_mapping.py --config $(config)

fetched_urls.json: config.yaml wordnet_mapping.json
	python3 imagenet/fetch_urls.py --config $(config)

test.txt: dep1.txt dep2.txt
	cat dep1.txt dep2.txt > test.txt

dep2.txt: dep1.txt
	cat dep1.txt dep1.txt > dep2.txt

dep1.txt:
	cat dep1.txt
