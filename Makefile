IMAGE_NAME=imagenet_download
PORT=8000
OUTPUT_DIR=outputs
CONFIG_FILE=config.yaml

VPATH=$(OUTPUT_DIR)
INC=$(CONFIG_FILE)

build:
	docker build -t $(IMAGE_NAME) .

dev:
	docker run --rm -ti -p $(PORT):$(PORT) \
		-v $(PWD)/:/project \
		-w '/project' \
		--env-file .env \
		$(IMAGE_NAME)

test:
	export PYTHONPATH=datasets
	pytest -v datasets

urls_data.json: $(CONFIG_FILE)
	python3 datasets/fetch_urls.py \
		--config $(CONFIG_FILE) \
		--output_dir $(OUTPUT_DIR)