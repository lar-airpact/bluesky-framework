# bluesky-framework

![](https://travis-ci.com/lar-airpact/airpact5-senior-design.svg?branch=staging)
[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3613)

## Description
This repository contains all artifacts, scripts, configuration files, etc. in order to run the WSU LAR group's version of BlueSky Framework. Although the primary bulk of the processing is done by the BlueSky Framework itself, the WSU LAR group wrote scripts in order to post-process the data, which this respository includes.

## In Progress
1. Adding ability to consistently create the Docker Image
1. Adding ability to continously deploy Singularity Image to Aeolus.
1. Adding ability to easily change WSU LAR group files that are present inside the images.

## Goals Accomplished
1. Moved portion of WSU AIRPACT-5 Software into version control. While this has all of the usual benefits of version control (e.g. backing up software, traceability, giving developers ability to move faster, work concurrently, and scale), it has the added benefit that one can work on the code anywhere rather than having to develop code inside Aeolus.
1. Successfully generated Docker Image and Singularity Image.
1. Successfully applied CI to the repository.
