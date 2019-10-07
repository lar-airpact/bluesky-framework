FROM pnwairfire/bluesky-framework

# Set working directory
ENV BS_DIR /bluesky/dist/bluesky/
WORKDIR ${BS_DIR}

# Add blue sky required files to Docker Container
COPY bluesky_3.5.1 ./

# Hack
COPY /usr/lib/python2.7/dist-packages/mapscript.pyc /bluesky/dist/bluesky/base/lib/MapScript-5.6.3-py2.7-linux-x86_64.egg/

# Run bash.
CMD ["/bin/bash"]