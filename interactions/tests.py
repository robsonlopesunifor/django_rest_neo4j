from django.test import TestCase

# Create your tests here.
from .models import Drug, Interaction


class DrugTest(TestCase):
    def test_get_all_drugs(self):
        """ Testa se esta pegando as drogas """
        d = Drug.nodes.all()
        self.assertEqual(len(d), 1893)

    def test_get_one_drug(self):
        """ Testa se está pegando uma droga """
        d = Drug.nodes.get(name="Femprocumona")
        self.assertEqual(d.name, "Femprocumona")

    def test_unknown_severity_interaction(self):
        """ Testa unknown_severity_interaction """
        d = Drug.nodes.get(name="Femprocumona")
        d2 = Drug.nodes.get(name="Peginterferon alfa")
        rel = d.unknown_severity_interaction.relationship(d2)
        self.assertEqual(rel.severity, "Gravidade desconhecida")

    def test_mild_interaction(self):
        """ Testa mild_interaction """
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Valproato")
        rel = d.mild_interaction.relationship(d2)
        self.assertEqual(rel.severity, "Leve")

    def test_moderate_interaction(self):
        """ Testa moderate_interaction """
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Rifampicina")
        rel = d.moderate_interaction.relationship(d2)
        self.assertEqual(rel.severity, "Moderada")

    def test_nothing_expected(self):
        """ Testa nothing_expected """
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Propranolol")
        rel = d.nothing_expected.relationship(d2)
        self.assertEqual(rel.severity, "Nada esperado")

    def test_severe_interaction(self):
        """ Testa severe_interaction """
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Fosfenitoina")
        rel = d.severe_interaction.relationship(d2)
        self.assertEqual(rel.severity, "Grave")

    def test_get_interaction(self):
        """ Testa severe_interaction """
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Fosfenitoina")
        rel = d.get_interaction(d2)
        self.assertEqual(rel.severity, "Grave")

    def test_get_interaction_vertice_nodes(self):
        """ Testa se get_interaction() retorna end_node e start_node"""
        d = Drug.nodes.get(name="Lorazepam")
        d2 = Drug.nodes.get(name="Fosfenitoina")
        rel = d.get_interaction(d2)
        self.assertEqual(rel.start_node().name, "Lorazepam")
        self.assertEqual(rel.end_node().name, "Fosfenitoina")

    def test_get_interactions(self):
        """ Testa get_interactions() """
        d = Drug.nodes.get(name="Lorazepam")
        rels = d.get_interactions()
        self.assertEqual(len(rels), 137)

    def test_get_multiple_interactions(self):
        """ Testa get_mutiple_interactions() """
        drug_list = [17, 443, 681]
        rels = Drug.get_mutiple_interactions(drug_list)
        self.assertEqual(len(rels), 2)

    def test_get_instance_interaction(self):
        i = Interaction.get_instance(pk=12)
        self.assertEqual(i.evidence, "Teórica")
