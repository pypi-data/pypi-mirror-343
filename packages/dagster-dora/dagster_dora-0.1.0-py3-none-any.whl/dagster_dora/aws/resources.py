"""Módulo de Ativos Dora Dagster.

Este módulo contém classes e funções para configurar e gerenciar recursos AWS 
dentro de pipelines Dagster.
"""
from json import load, loads
from typing import Any, Dict, Iterator, Tuple
import dagster as dg
from pydantic import Field, ConfigDict, computed_field

class Stack(dg.ConfigurableResource):
    """Recursos Dora para pipelines.

    Atributos:
        output_file (str): Caminho para o arquivo de saída que contém a configuração do stack.
        model_config (ConfigDict): Configuração do modelo que permite tipos arbitrários e campos extras.
    """
    output_file:str = Field(description="Stack output file", default="output.json")
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

class AwsResources(Stack):
    """Recursos do Stack AWS.

    Esta classe herda de Stack e fornece um iterador para acessar os recursos 
    definidos no arquivo de saída do stack.
    """

    @computed_field
    def resources(self) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Iterador de recursos.

        Lê o arquivo de saída especificado e gera tuplas contendo o nome do job 
        e os recursos associados a ele.

        Retorna:
            Iterator[Tuple[str, Dict[str, Any]]]: Um iterador de tuplas onde o 
            primeiro elemento é o nome do job e o segundo é um dicionário com 
            os recursos.
        """
        with open(self.output, mode='r', encoding='utf-8') as _f:
            outputs = load(_f)
            for stack in outputs:
                for job, resources in outputs[stack].items():
                    yield (job , loads(resources))
