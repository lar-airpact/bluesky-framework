FROM pnwairfire/bluesky-framework

# Set working directory
ENV BS_DIR /bluesky/dist/bluesky/
WORKDIR ${BS_DIR}

# Add blue sky required files to Docker Container
COPY bluesky_3.5.1 ./

# Install any dependencies
RUN apt-get install csh

# Add the hack job
COPY hack.sh ./

# Run the hack
CMD ["/bin/bash", "hack.sh"]