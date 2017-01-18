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
		}
	}

If the file this data was saved in was called `example.json` and resided in the local directory, the command to run the list operation would simply be

	webcall example.json list

Notably, the "create" action specifies that it needs the requesteddata section to list a "name" parameter. This is not supplied in the default arguments, so will need to be supplied on the command line:

	webcall example.json create name=newDropletName

This would append the data to the `requestdata` set.

## Still to come

Still to implement:

* writing new structures to the `requesteddata` section (`webcall example.json superkey.subkey=newvalue` will complain about an inexistent `superkey`)
* support for header definitions in the JSON and on the command line

## License

(C) Tai Kedzierski
Provided to you under the terms of the GPLv3.0
