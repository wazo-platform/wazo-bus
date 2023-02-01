# AsyncAPI Documentation Generator

This role of this docker is to parse and generate asyncapi documentation for
all events found in the `xivo_bus/resources` directory.

## Usage

1. build the image from root directory

`docker build -t wazo-asyncapi -f contribs/Dockerfile .`

1. run the image to parse and write asyncapi specification files to output

`docker run -v ${output_dir}:/app/output -i wazo-asyncapi -p ${stack_version}`

where:
  * output_dir: absolute path to where you want to extract the asyncapi documentation
  * stack_version: version to write in the specification files

The docker will then append and write each event's documentation to its microservice specification file.
