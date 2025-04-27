import time
import logging
from ..utils.config import settings
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import Aer
logger = logging.getLogger(__name__)

class QuantumSimulator:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuantumSimulator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self._initialize_backend()
            self.__class__._initialized = True

    def _initialize_backend(self):
        if settings.USE_SIMULATOR:
            logger.info("Setting up local simulator backend...")
            self.backend = Aer.get_backend('qasm_simulator')
        else:
            logger.info("Setting up IBM Quantum backend...")
            try:
                QiskitRuntimeService.save_account(
                    channel='ibm_quantum',
                    token=settings.IBM_TOKEN,
                    overwrite=True
                )
                service = QiskitRuntimeService()
                available_backends = service.backends()
                logger.info("Available IBM Quantum Backends:")
                for backend in available_backends:
                    logger.info(f"- {backend.name}")

                self.backend = service.backend('ibm_sherbrooke')
                logger.info(f"Using IBM backend: {self.backend.name}")
            except Exception as e:
                logger.error(f"Error initializing IBM backend: {e}")
                self.backend = None  
            logger.info("IBM backend setup complete.")
    def execute_job(self, qc):
        start_time = time.time()
        result = None
        if settings.USE_SIMULATOR:
            result = self._execute_simulator(qc)
        else:
            result = self._execute_ibm(qc)
        
        end_time = time.time()

        elapsed_time = (end_time - start_time)
        logger.info(f"Circuit Execution took {elapsed_time:.2f} seconds.")
        return result    

    def _execute_simulator(self, qc):
        transpiled_qc = transpile(qc.reverse_bits(), self.backend)
        result = self.backend.run(transpiled_qc, shots=2048).result()
        counts = result.get_counts()
        return counts

    def _execute_ibm(self, qc):
        pm = generate_preset_pass_manager(backend=self.backend)
        isa_circuit = pm.run(qc.reverse_bits())

        sampler = Sampler(mode=self.backend)
        sampler.options.default_shots = 10000
        logger.info("Running the circuit on the IBM backend...")
        job = sampler.run([isa_circuit])
        logger.info(f"Job ID: {job.job_id()}")
        pub_result = job.result()[0]
        logger.info(pub_result.data)
        counts = pub_result.data.c.get_counts()
        return counts
