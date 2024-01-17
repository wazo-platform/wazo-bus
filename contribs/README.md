# AsyncAPI Documentation Generator

This role of this docker is to parse and generate asyncapi documentation for
all events found in the `wazo_bus/resources` directory.

## Usage

1. build the image from root directory

`docker build -t wazo-asyncapi -f contribs/Dockerfile .`

1. run the image to parse and write asyncapi specification files to output

`docker run -v ${output_dir}:/app/output -i wazo-asyncapi -p ${stack_version}`

where:
  * output_dir: absolute path to where you want to extract the asyncapi documentation
  * stack_version: version to write in the specification files

The docker will then append and write each event's documentation to its microservice specification file.


## Validation

To validate the generated specification files, [asyncapi-cli](https://github.com/asyncapi/cli) should be used:

1. `docker run -v ${spec_file}:/{service_name}.yml -i asyncapi/cli:latest validate /{service_name}.yml`

where:
  * spec_file: absolute path to the specification file you wish to validate
  * service_name: service name to use by the validator
