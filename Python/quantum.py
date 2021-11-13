circuit = {
    "qubits": 3,
    "circuit": [
        {
        "gate": "h",
        "target": 0
        },
        {
        "gate": "cnot",
        "control": 0,
        "target": 1
        },
        {
        "gate": "cnot",
        "control": 0,
        "target": 2
        },
    ]
}
target = IonQ(workspace=workspace, target="ionq.simulator")
job = target.submit(circuit)
results = job.get_results()
results