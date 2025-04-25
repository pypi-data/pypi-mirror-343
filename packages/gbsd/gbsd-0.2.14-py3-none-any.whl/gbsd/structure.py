from ase import Atoms
import numpy as np

def generate_random_closest_approach(
    element_counts: dict[str, int],
    number_density: float,
    closest_approach: float = 0.0,
    max_steps_per_particle: int = 10_000
) -> Atoms:
    total_atoms = sum(element_counts.values())    

    # Get cell
    volume = total_atoms / number_density
    cell_length = volume**(1/3)
    cell: np.ndarray = cell_length * np.eye(3)
    inverse_cell = np.linalg.inv(cell)

    # Generate positions
    positions = np.zeros((total_atoms, 3))
    
    for particle in range(1, total_atoms):
        for attempt in range(max_steps_per_particle):
            proposed_position = np.random.rand(3) @ cell

            # Get distances with MIC
            displacements = proposed_position[None, :] - positions[:particle]
            displacement_shifts = np.round(displacements @ inverse_cell) @ cell
            image_displacements = displacements - displacement_shifts

            distances = np.linalg.norm(image_displacements, axis=-1)

            if np.min(distances) > closest_approach:
                positions[particle] = proposed_position
                break
            elif attempt == max_steps_per_particle - 1:
                raise RuntimeError(f"Unable to place atoms within max_steps_per_particle... Got to {particle+1}.")

    symbols = np.concatenate(list([element] * count for element, count in element_counts.items()))

    return Atoms(symbols, positions, cell=cell, pbc=True)