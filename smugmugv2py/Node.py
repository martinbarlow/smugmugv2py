from json import dumps
from pprint import pprint
from Uri import Uri

class Node(object):
    def __init__(self, node):
        for key in node:
            setattr(self, key.lower(), node[key])
        self.uris = Uri(node["Uris"])

    @classmethod
    def get_node(cls, connection, node_uri):
        return cls(connection.get(node_uri)["Node"])

    def get_children(self, connection):
        ret=[]

        if self.haschildren:
            response = connection.get(self.uris.childnodes)
            if 'Node' in response:
                nodes=response["Node"]
                for node in nodes:
                    thisnode = Node(node)
                    ret.append(thisnode)

        return ret

    def __create_child_node(self, connection, type, name, url, privacy, description):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = {
            'Type': type,
            'Name': name,
            'UrlName': url,
            'Privacy': privacy,
        }

        if description:
            params['Description']=description

        return connection.post(self.__child_nodes, data=dumps(params), headers=headers)

    def create_child_folder(self, connection, name, url, privacy, description=None):
        response = self.__create_child_node(connection, 'Folder', name, url, privacy, description)

        if not "Node" in response["Response"]:
            pprint(response)

        return Node(response["Response"]["Node"])

    def create_child_album(self, connection, name, url, privacy, description=None):
        response = self.__create_child_node(connection, 'Album', name, url, privacy, description)

        if not "Node" in response["Response"]:
            pprint(response)

        return Node(response["Response"]["Node"])

    def delete_node(self, connection):
        return connection.delete(self.uri)

    def change_node(self, connection, changes):
        return connection.patch(self.uri, changes)["Response"]["Node"]
