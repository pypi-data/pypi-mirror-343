import pennylane as qml
import numpy as np
import pytest


# This test class is meant to verify compatibility of PennyLane subroutines with the plugin.
# A listing of the subroutines can be found at the following links:
# https://docs.pennylane.ai/en/stable/introduction/operations.html
# https://docs.pennylane.ai/en/stable/code/qml.html#classes

class TestPennylaneSubroutine:
    """Test the PennyLane subroutine functions with 'snowflurry.qubit'.
    The decompose transforms implemented in the plugin should return the same
    state as the PennyLane 'default.qubit'.
    """

    @pytest.fixture(autouse=True)
    def dev_pennylane(self):
        self.dev_pennylane = qml.device("default.qubit", wires=5)

    @pytest.fixture(autouse=True)
    def dev_snowflurry(self):
        self.dev_snowflurry = qml.device("snowflurry.qubit", wires=5)

    
    @pytest.mark.xfail
    def test_AQFT(self):
        """Test the AQFT subroutine."""
        def circuit_AQFT():
            qml.AQFT(order=1, wires=[0, 1, 2, 3, 4])
            return qml.state()

        snowflurry_qnode = qml.QNode(circuit_AQFT, self.dev_snowflurry)
        pennylane_qnode = qml.QNode(circuit_AQFT, self.dev_pennylane)
        result_snowflurry = snowflurry_qnode()
        result_pennylane = pennylane_qnode()
        assert result_pennylane.all() == result_snowflurry.all()

    @pytest.mark.xfail
    def test_BasisState(self):
        """Test the BasisState subroutine.

        FIXME : Qubits that do not have any gates applied are just not represented in the state vector.
        Therefore, as long as all qubits are acted upon after initialization, the state vector will
        should be completely defined.
        """
        print("Testing BasisState subroutine")

        def circuit_BasisState_all_ones():
            qml.BasisState(np.array([1, 1, 1, 1, 1]), wires=[0, 1, 2, 3, 4])
            return qml.state()

        pennylane_qnode = qml.QNode(circuit_BasisState_all_ones, self.dev_pennylane)
        snowflurry_qnode = qml.QNode(circuit_BasisState_all_ones, self.dev_snowflurry)
        result_pennylane = pennylane_qnode()
        result_snowflurry = snowflurry_qnode()
        assert result_pennylane.all() == result_snowflurry.all()

        def circuit_BasisState_all_zeros():
            qml.BasisState(np.array([0, 0, 0, 0, 0]), wires=[0, 1, 2, 3, 4])
            return qml.state()

        pennylane_qnode = qml.QNode(circuit_BasisState_all_zeros, self.dev_pennylane)
        snowflurry_qnode = qml.QNode(circuit_BasisState_all_zeros, self.dev_snowflurry)
        result_pennylane = pennylane_qnode()
        result_snowflurry = snowflurry_qnode()
        assert result_pennylane.all() == result_snowflurry.all()
