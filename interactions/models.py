from django.contrib.auth.models import User
from django.db import models
from neomodel import StructuredNode, StringProperty
from neomodel import StructuredRel, Relationship
from neomodel import EITHER
from neomodel import db
from neomodel.match import Traversal
from itertools import combinations

def translate(value):
    dictionary = {
        'id': 'id',
        'gravidade': 'severity',
        'evidencia': 'evidence',
        'acao': 'action',
        'explicacao': 'explanation',
    }

    return dictionary[value]

class Interactions(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username

class Interaction(StructuredRel):
    severity = StringProperty()
    evidence = StringProperty()
    action = StringProperty()
    explanation = StringProperty()

    @classmethod
    def get_instance(cls, pk):
        rel = None

        q = ("MATCH ()-[r]->() WHERE ID(r)={pk} RETURN r")

        for row in db.cypher_query(q, {'pk': pk})[0]:
            rel = row[0]

        if not rel:
            return

        i = cls.inflate(rel)
        i._start_node_class = Drug
        i._end_node_class = Drug

        return i

class Interaction(StructuredRel):
    severity = StringProperty()
    evidence = StringProperty()
    action = StringProperty()
    explanation = StringProperty()

    @classmethod
    def get_instance(cls, pk):
        rel = None

        q = ("MATCH ()-[r]->() WHERE ID(r)={pk} RETURN r")

        for row in db.cypher_query(q, {'pk': pk})[0]:
            rel = row[0]

        if not rel:
            return

        i = cls.inflate(rel)
        i._start_node_class = Drug
        i._end_node_class = Drug

        return i

class Drug(StructuredNode):
    __label__ = "DRUG"

    name = StringProperty()
    action = StringProperty(db_property="drugAction")

    mild_interaction = Relationship(
        'Drug', 'MILD_INTERACTION', model=Interaction)

    moderate_interaction = Relationship(
        'Drug', 'MODERATE_INTERACTION', model=Interaction)

    nothing_expected = Relationship(
        'Drug', 'NOTHING_EXPECTED', model=Interaction)

    severe_interaction = Relationship(
        'Drug', 'SEVERE_INTERACTION', model=Interaction)

    unknown_severity_interaction = Relationship(
        'Drug', 'UNKNOWN_SEVERITY_INTERACTION', model=Interaction)

    def get_interaction(self, node):
        rel = None

        q = ("MATCH (them), (us) "
             "WHERE id(them)={them} and id(us)={self} "
             "MATCH" + "(us)-[r]-(them)" + " RETURN r")

        for row in self.cypher(q, {'them': node.id})[0]:
            rel = row[0]

        if not rel:
            return

        i = Interaction.inflate(rel)
        i._start_node_class = self.__class__
        i._end_node_class = node.__class__

        return i

    def _get_nodes_list(nodes_id):
        nodes = list()
        for node_id in nodes_id:
            node = Drug()
            node.id = node_id
            node.refresh()
            nodes.append(node)
        return nodes

    def get_related_nodes(self):
        """ Retorna todos os nós conectados a este nó. """

        definition = dict(node_class=Drug, direction=EITHER,
                          relation_type=None, model=Interaction)

        return Traversal(self, Drug.__label__, definition).all()

    def get_interactions(self):
        """ Retorna todas as relação deste nó """

        return list(map(lambda node: self.get_interaction(
            node), self.get_related_nodes()))

    @classmethod
    def get_mutiple_interactions(cls, nodes_id):
        interactions = list()

        nodes = cls._get_nodes_list(nodes_id)

        for start_node, end_node in combinations(nodes, r=2):
            i = start_node.get_interaction(end_node)
            if i:
                interactions.append(i)

        return interactions


class MetaData(object):
    def __init__(self):
        self.severity = ['Grave', 'Nada esperado', 'Leve',
                        'Moderada', 'Gravidade desconhecida']
        self.evidence = ['Teórica', 'Extensa', 'Caso', 'Estudo']
        self.action = ['Ajustar', 'Monitorar', 'Informar', 'Nenhuma', 'Evitar']
