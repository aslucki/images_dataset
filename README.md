# Datasets creation
## About
Scripts for preparing image classification datasets using publicly available, tagged images.
Project is based on the [Flickr API](https://www.flickr.com/services/api/).  

## Prerequisites
1. Project depends on the [Flickr API](https://www.flickr.com/services/api/)  
thus requires API credentials. Credentials should be stored as environmental variables,
named `API_KEY` and `API_SECRET`.

2. It's recommended to execute the code in [Docker](https://www.docker.com/).

## How to use
### Outline
1. Run `make build` in the root directory to prepare the environment.
2. Modify [config.yaml](config.yaml)
3. Run  `make create_dataset`
### 1. Prepare environment
Navigate to the project's root directory and run:
`make build`

If you're **NOT** going to use [Docker](https://www.docker.com/):
- Install python3
- Install pip3
- Run `pip3 install -r requrements.txt`

### 2. Configure dataset requirements
Modify the [config.yaml](config.yaml) file according to your needs.

#### Define image classes
Simply replace or add required classes and images count you'd like to donwload
for each of them.
It may be a good idea to try [Flickr browser](https://www.flickr.com/search/?tags=)
first to decide on the best query tag. Make sure that you're searching by `tags` and not
`text`.

```buildoutcfg
classes:
  - name: cat
    count: 20000
  - name: dog
    count: 10000
```

#### Configure train test split
After all the images are downloaded, the json file with relative paths to files
divided into train and test set is generated. 

```buildoutcfg
train_test_split:
  seed: 42

  # proportional - select n% of images from each class
  # absolute - select n images from each class
  type: 'absolute'
  test_size: 500
```

### 3. Execute scripts 
Navigate to the project's root directory and run:
`make create_dataset`

All the required steps will be performed automatically.
You may want to edit the [Makefile](Makefile) to change project's settings but it's 
not necessary as the code doesn't affect anything outside the project.

## Produced artifacts
1. Separate directories for each class containing small
images (240px on the longest side) with class instances.
2. `train_test_split.json` file containing relative paths to the images
divided into `training` and `testing` set.
3. `dataset.tgz` archive containing the above (1, 2).
4. `urls_data.json` urls to images on Flickr.
5. `summary.txt` report from the downloading process. At the same time it summarizes 
the contents of the dataset.

## Notes
- Obtained data isn't perfect.
  * There is no guarantee that all the images are unique.
  * Some images may be very similar to each other.
  * Some images may not represent an adequate class.
- Flickr API breaks sometimes,
there up to 5 retries in the case of Flickr API erros.
- Each step of the process has to finish in a single run.
There is no mechanism implemented that would allow to re-run steps from the middle.
  
