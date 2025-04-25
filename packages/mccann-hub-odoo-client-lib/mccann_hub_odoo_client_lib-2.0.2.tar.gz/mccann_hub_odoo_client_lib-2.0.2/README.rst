
Odoo Client Library
======================


The Odoo Client Library is a Python3 library to communicate with an Odoo Server using its web
services in an user-friendly way. It was created for those that doesn't want to code XML-RPC calls
on the bare metal. It handles XML-RPC as well as JSON-RPC protocol and provides a bunch of syntaxic
sugar to make things a lot easier.

Guide
-----

First install the library: ::

    pip install mccann_hub-odoo_client_lib

Now copy-paste the following script describing a simple interaction with an Odoo server: ::

    import mccann_hub.odoolib as odoolib

    connection = odoolib.get_connection(hostname="localhost", database="my_db", \
        login="my_user", password="xxx")
    user_model = connection.get_model("res.users")
    ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(ids[0], ["name"])
    print user_info["name"]
    # will print "Administrator"

In the previous script, the get_connection() method creates a Connection object that represents a
communication channel with authentification to an Odoo server. By default, get_connection() uses
XML-RPC, but you can specify it to use JSON-RPC. You can also change the port. Example with a JSON-RPC
communication on port 6080: ::

    connection = odoolib.get_connection(hostname="localhost", protocol="jsonrpc", port=6080, ...)

The get_model() method on the Connection object creates a Model object. That object represents a
remote model on the Odoo server (for Odoo addon programmers, those are also called osv).
Model objects are dynamic proxies, which means you can remotely call methods in a natural way.
In the previous script we demonstrate the usage of the search() and read() methods. That scenario
is equivalent to the following interaction when you are coding an Odoo addon and this code is
executed on the server: ::

    user_osv = self.pool.get('res.users')
    ids = user_osv.search(cr, uid, [("login", "=", "admin")])
    user_info = user_osv.read(cr, uid, ids[0], ["name"])

Also note that coding using Model objects offer some syntaxic sugar compared to vanilla addon coding:

- You don't have to forward the "cr" and "uid" to all methods.
- The read() method automatically sort rows according the order of the ids you gave it to.
- The Model objects also provides the search_read() method that combines a search and a read, example: ::
    
    user_info = user_model.search_read([('login', '=', 'admin')], ["name"])[0]

Here are also some considerations about coding using the Odoo Client Library:

- Since you are using remote procedure calls, every call is executed inside its own transaction. So it can
  be dangerous, for example, to code multiple interdependant row creations. You should consider coding a method 
  inside an Odoo addon for such cases. That way it will be executed on the Odoo server and so it will be
  transactional.
- The browse() method can not be used. That method returns a dynamic proxy that lazy loads the rows' data from
  the database. That behavior is not implemented in the Odoo Client Library.

Testing
-------

There is a Docker compose file in the `test_containers` directory that will stand up a local instance of Odoo: ::

    docker compose -f ./test_containers/compose.yaml up 

Compatibility
-------------

- XML-RPC: OpenERP version 6.1 and superior

- JSON-RPC: Odoo version 8.0 (upcoming) and superior
