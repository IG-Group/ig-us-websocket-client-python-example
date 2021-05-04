# IG US WebSocket Client Python Example

## Introduction

This project is an example to demonstrate calling the  [IG US](https://www.ig.com/us/welcome-page) WebSocket API using the [Python](https://www.python.org/) programming language.

It has been developed using Python 3.7.

It is not production quality code.

The example negotiates and establishes a FIXP session and then requests a SecurityList and a stream of Quote messages.

It stops and disconnects after a configured number of Quote messages are received.

To run the example an [IG US](https://www.ig.com/us/welcome-page) Demo environment Username and Password are required. Open an account [here](https://www.ig.com/us/application-form).

[Introduction to the IG US WebSocket API](https://github.com/IG-Group/ig-orchestrations/blob/master/ig-us-rfed/document/document-websocket/markdown/websocketAPI.md)

[IG US WebSocket PreTrade API](https://github.com/IG-Group/ig-orchestrations/blob/master/ig-us-rfed/document/document-websocket/markdown/websocketPreTradeAPI.md)

## How to run the example

See below for how to activate the environment if you are using conda.

```
python WebSocketClient.py --userName=a_username --password=a_password --quoteLimit=10
```

By default the example will connect to the Demo environment.


## Consider Installing Anaconda

Anaconda is a commonly used Python environment.

You may choose to download the  [Indidual Edition](https://www.anaconda.com/products/individual).

Refer to the documents on the above site.

### Create (Activate) the provided conda environment

```
conda env create -f environment.yml
```

### How to export a conda environment if you extend it

```
conda env export > environment.yml
```
