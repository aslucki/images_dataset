IMAGE_NAME=imagenet_download
PORT=8000
OUTPUT_DIR=outputs
CONFIG_FILE=config.yaml
URLS_DATA_FILE=urls_data.json
SPLIT_INFO_FILE=train_test_split.json
DOWNLOAD_REPORT_FILE=summary.txt

VPATH=$(OUTPUT_DIR)
INC=$(CONFIG_FILE)
export PYTHONPATH=datasets

build:
	docker build -t $(IMAGE_NAME) .

dev:
	docker run --rm -ti -p $(PORT):$(PORT) \
		-v $(PWD)/:/project \
		-w '/project' \
		--env-file .env \
		$(IMAGE_NAME)

test:
	python3 -m pytest -v datasets

create_dataset: dataset.tgz
	@echo "Dataset created\033[0m" 

urls_data.json: $(CONFIG_FILE)
	@mkdir -p $(OUTPUT_DIR)
	@python3 datasets/fetch_urls.py \
		--config $(CONFIG_FILE) \
		--output_dir $(OUTPUT_DIR) \
		--output_file_name $(URLS_DATA_FILE)

summary.txt: urls_data.json
	@python3 datasets/download_dataset.py \
		--input_file_name $(URLS_DATA_FILE) \
		--output_dir $(OUTPUT_DIR) \
		--output_file_name $(DOWNLOAD_REPORT_FILE)

train_test_split.json: $(CONFIG_FILE) summary.txt
	@python3 datasets/split_dataset.py \
		--config $(CONFIG_FILE) \
		--output_dir $(OUTPUT_DIR) \
		--output_file_name $(SPLIT_INFO_FILE)	

dataset.tgz: train_test_split.json
	rm -f dataset.tgz~
	@cd $(OUTPUT_DIR); \
	tar czf dataset.tgz \
		--exclude=$(URLS_DATA_FILE) \
		--exclude=$(DOWNLOAD_REPORT_FILE) \
		 *