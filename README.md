# Kedro Basics
In this project, we have tried to present a poi extraction pipeline using kedro. This pipeline demonstrates a process which can extract poi using a java based open source library named gazetteer from pbf file and then transform them according to the requirements. In this project, focus was on extracting poi's for Bangladesh based on geoboundary and translate them from English to Bangla or Bangla to English when the algorithm fits the required criterions.

## Requirements
- Java
- Python

## Setup
Run the following command to get your setup ready for python environment.
```
source init.sh && cd $TOOL_PROJECT_DIR
```

## Run Kedro
To run kedro, you must go to the kedro project directory aka `$TOOL_PROJECT_DIR` (`_101`) and run the following commands
```
kedro run # will run the full pipeline
kedro run -p <pipeline_name> # will run a specific pipeline
```

### HELPER (HOW TO REMOVE MISTAKENLY PUSHED BIG FILES)
https://stackoverflow.com/questions/72123622/how-to-delete-all-files-1-mb-from-the-history-but-keep-them-in-the-repository
https://github.com/newren/git-filter-repo/blob/main/INSTALL.md

After refactoring, please add the remote again using

`git remote add origin <url>`