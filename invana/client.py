#  Copyright 2020 Invana
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http:www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from .gremlin import GremlinClient
from .operations import VertexOperations, EdgeOperations, SchemaAllOperations, GraphStatsOperations


class InvanaClient:

    def __init__(self, gremlin_url, traversal_source="g", username=None, password=None,
                 loop=None, read_timeout=3600, write_timeout=3600):
        self.gremlin_client = GremlinClient(
            gremlin_url,
            traversal_source=traversal_source, loop=loop,
            read_timeout=read_timeout, write_timeout=write_timeout,
            username=username, password=password
        )
        self.vertex = VertexOperations(gremlin_client=self.gremlin_client)
        self.edge = EdgeOperations(gremlin_client=self.gremlin_client)
        self.stats = GraphStatsOperations(gremlin_client=self.gremlin_client)
        self.schema = SchemaAllOperations(gremlin_client=self.gremlin_client)

    def get_event_loop(self):
        return self.gremlin_client.loop

    async def execute_query(self, gremlin_query, serialize=True):
        return await self.gremlin_client.execute_query(gremlin_query, serialize=serialize)

    def execute_query_as_sync(self, gremlin_query, serialize=True):
        return self.gremlin_client.execute_query_as_sync(gremlin_query, serialize=serialize)
