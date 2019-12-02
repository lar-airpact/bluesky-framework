# bluesky-framework

![](https://travis-ci.com/lar-airpact/bluesky-framework.svg?branch=staging)
[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3613)

## Description
This repository contains all artifacts, scripts, configuration files, etc. in order to run the WSU LAR group's version of BlueSky Framework. Although the primary bulk of the processing is done by the BlueSky Framework itself, the WSU LAR group wrote scripts in order to post-process the data, which this respository includes.

## An Important Note on the Image Creation
Unfortunately, due to the fact that this particular framework is deprecated, we didn't have access to the source code. Thus, the creation of this image ended up being quite "hacky", forcing us to commit the image while being run as a container. Thus, there was no build from a Dockerfile. This is obviously poor practice and should be avoided at all costs. In these circumstances, it was necessary in order to deliver a functional product.

Thus, the "Dockerfile" merely serves as an example of what the image building *should* look like. The actual steps to replicate the existing image in Docker Hub don't exist. One would need to dig through the image layers and piece it together, which is outside the scope of this project.
