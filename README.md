# Manage Web calls

A little tool for defining web APIs by

* maintaining a JSON file with default parameters
* a way to pass extra parameters on the command line
* overriding defaults

## Example

The following is a simple JSON file that specifies that the target web API expects JSON-based data, provides an API key, and then lists calls to make for a given named action.

	{
		"api":"json",
		"key":"12345678901234567890",

		"actions":{
			"list":{
				"url":"https://api.digitalocean.com/v2/droplets",
				"method":"GET"
			},
			"create":{
				"url":"https://api.digitalocean.com/v2/droplets",
				"method":"POST",
				"requires":["region", "size", "image", "name"],
				"requestdata":{
					"region":"lon1",
					"size":"512mb",
					"image":"22222654"
				}
			}
			"destroy":{
				"url":"https://api.digitalocean.com/v2/droplets/$id",
				"method":"DELETE",
				"requestdata":{
				}
			}
		}
	}

If the file this data was saved in was called `example.json` and resided in the local directory, the command to run the list operation would simply be

	webcall example.json list

Notably, the "create" action specifies that it needs the requesteddata section to list a "name" parameter. This is not supplied in the default arguments, so will need to be supplied on the command line:

	webcall example.json create name=newDropletName

This would append the data to the `requestdata` set.

The `destroy` example shows the example of having placeholders in the URL - to pass the relevant information to the URL, use an assignment preceded by a "%":

	webcall example.json destroy %id=123456

The `id` information here will not be passed to the request data, instead it will be used to replace the relevant token for the request.

## Still to come

Still to implement:

* output control (headers, json body) with filter patterns (grep or json pattern - with the latter, all results are combined to a single line, with tab separators)
* writing new structures to the `requestdata` section (`webcall example.json list superkey.subkey=newvalue` will complain about an inexistent `superkey`, for example)
* support for header definitions in the JSON and on the command line
* example implementation for a different sort of API

## License

(C) 2017 Tai Kedzierski
Provided to you under the terms of the GPLv3.0
