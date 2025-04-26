import unittest
from flask import Flask
from quantum_finance.backend.api import api, init_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_app(self.app)
        self.client = self.app.test_client()

    def test_root_endpoint(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Welcome to the Quantum Computing API"})

    def test_create_circuit(self):
        response = self.client.post("/api/circuit", json={"num_qubits": 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn("circuit_id", response.get_json())

    def test_add_gate(self):
        circuit_response = self.client.post("/api/circuit", json={"num_qubits": 2})
        circuit_id = circuit_response.get_json()["circuit_id"]
        gate_response = self.client.post(f"/api/circuit/{circuit_id}/gate", json={"gate": "H", "qubit": 0})
        self.assertEqual(gate_response.status_code, 200)
        self.assertEqual(gate_response.get_json(), {"message": "Gate added successfully"})

    def test_measure_circuit(self):
        circuit_response = self.client.post("/api/circuit", json={"num_qubits": 1})
        circuit_id = circuit_response.get_json()["circuit_id"]
        self.client.post(f"/api/circuit/{circuit_id}/gate", json={"gate": "H", "qubit": 0})
        measure_response = self.client.get(f"/api/circuit/{circuit_id}/measure")
        self.assertEqual(measure_response.status_code, 200)
        self.assertIn("result", measure_response.get_json())

    def test_invalid_circuit_id(self):
        response = self.client.get("/api/circuit/invalid_id/measure")
        self.assertEqual(response.status_code, 404)

    def test_invalid_gate(self):
        circuit_response = self.client.post("/api/circuit", json={"num_qubits": 1})
        circuit_id = circuit_response.get_json()["circuit_id"]
        gate_response = self.client.post(f"/api/circuit/{circuit_id}/gate", json={"gate": "InvalidGate", "qubit": 0})
        self.assertEqual(gate_response.status_code, 400)

if __name__ == '__main__':
    unittest.main()