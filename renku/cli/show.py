# -*- coding: utf-8 -*-
#
# Copyright 2018 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Show information about objects in current repository.

Siblings
~~~~~~~~

In situations when multiple outputs have been generated by a single
``renku run`` command, the siblings can be discovered by running
``renku show siblings PATH`` command.

Assume that the following graph represents relations in the repository.

.. code-block:: text

          D---E---G
         /     \
    A---B---C   F

Then the following outputs would be shown.

.. code-block:: console

   $ renku show siblings C
   C
   D
   $ renku show siblings G
   F
   G
   $ renku show siblings A
   A


Output files
~~~~~~~~~~~~

You can list all output files generated in the repository by running
``renku show outputs`` commands. Alternatively, you can check if all
paths specified as arguments are output files.

.. code-block:: console

   $ renku run wc < source.txt > result.wc
   $ renku show outputs
   result.wc
   $ renku show outputs source.txt
   $ $?  # last command finished with an error code
   1

"""

import click

from ._client import pass_local_client
from ._git import with_git
from ._graph import Graph


@click.group()
def show():
    """Show information about objects in current repository.

    NOTE: The command produces machine readable output.
    """


@show.command()
@click.option('--revision', default='HEAD')
@click.argument(
    'paths', type=click.Path(exists=True, dir_okay=False), nargs=-1
)
@pass_local_client
@with_git(clean=False, commit=False)
def siblings(client, revision, paths):
    """Show siblings for given paths."""
    graph = Graph(client)
    paths = [graph.normalize_path(path) for path in paths]
    nodes = graph.build(paths=paths, revision=revision)
    siblings_ = set(nodes)
    for node in nodes:
        siblings_ |= graph.siblings(node)

    paths = {node.path for node in siblings_}
    for path in paths:
        click.echo(graph._format_path(path))


@show.command()
@click.option('--revision', default='HEAD')
@click.argument(
    'paths',
    type=click.Path(exists=True, dir_okay=False),
    nargs=-1,
)
@pass_local_client
@click.pass_context
@with_git(clean=False, commit=False)
def outputs(ctx, client, revision, paths):
    r"""Show output files in the repository.

    <PATHS>    Files to show. If no files are given all output files are shown.
    """
    graph = Graph(client)
    paths = [graph.normalize_path(path) for path in paths]
    filter = graph.build(paths=paths, revision=revision)
    output_paths = graph.output_paths

    click.echo('\n'.join(graph._format_path(path) for path in output_paths))
    ctx.exit(0 if not paths or len(output_paths) == len(filter) else 1)
