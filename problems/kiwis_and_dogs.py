from dataclasses import dataclass

from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str, ...]
    dogs: tuple[str, ...]


# Problem
##############################################################################


class KiwisAndDogsProblem(Problem):
    NAME = "kiwis-and-dogs"

    def __init__(self):
        super().__init__()

        self.vtree = "A"   
        self.vbone = "E"

        # Node coordinates
        self.coordinates = {
            "A": (0, 0),
            "B": (1, 1),
            "C": (2, 0),
            "D": (3, 1),
            "E": (4, 2),
            "F": (3, 3),
            "G": (1, 3),
        }

        self.graph = {
            # A
            ("A", "B"): (3, "nobody(E)"),
            ("A", "C"): (4, ""),
            # B
            ("B", "A"): (3, "nobody(E)"),
            ("B", "C"): (1, ""),
            ("B", "G"): (5, ""),
            # C
            ("C", "B"): (1, ""),
            ("C", "D"): (2, "somebody(E),somebody(G)"),
            ("C", "A"): (4, ""),
            # D
            ("D", "C"): (2, "somebody(E),somebody(G)"),
            ("D", "E"): (8, "somebody(A)"),
            ("D", "F"): (3, "somebody(C)"),
            # E
            ("E", "D"): (8, "somebody(A)"),
            ("E", "F"): (5, ""),
            # F
            ("F", "D"): (3, "somebody(C)"),
            ("F", "E"): (5, ""),
            ("F", "G"): (7, ""),
            # G
            ("G", "F"): (7, ""),
            ("G", "B"): (5, ""),
        }
        self.num_kiwis = 2
        self.num_dogs = 1

    def get_coord(self, v):
        """Return the (x, y) coordinates of vertex v"""
        return self.coordinates.get(v, (0, 0))

    def get_start_states(self):
        return [State(kiwis=("D", "F"), dogs=("C",))]

    def is_goal_state(self, state):
        """Check if all kiwis are at vtree and all dogs are at vbone"""
        all_kiwis_at_tree = all(kiwi == self.vtree for kiwi in state.kiwis)
        all_dogs_at_bone = all(dog == self.vbone for dog in state.dogs)
        return all_kiwis_at_tree and all_dogs_at_bone

    def is_valid_state(self, _):
        return True

    def _check_conditions(self, state, conditions):
        """Check if the conditions for using an edge are satisfied"""
        if not conditions:
            return True
        
        condition_list = [c.strip() for c in conditions.split(",") if c.strip()]
        
        for condition in condition_list:
            if condition.startswith("somebody("):
                vertex = condition[9:-1]
                has_someone = (vertex in state.kiwis) or (vertex in state.dogs)
                if not has_someone:
                    return False
                    
            elif condition.startswith("nobody("):
                vertex = condition[7:-1]
                has_someone = (vertex in state.kiwis) or (vertex in state.dogs)
                if has_someone:
                    return False
        
        return True

    # KIWI ACTIONS - A
    @action(DDRange(0, "num_kiwis"), cost=3)
    def move_kiwi_A_to_B(self, state, kiwi_idx):
        """Move a kiwi from A to B (cost 3, nobody(E))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "A":
            return None
        
        if not self._check_conditions(state, "nobody(E)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "B"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=4)
    def move_kiwi_A_to_C(self, state, kiwi_idx):
        """Move a kiwi from A to C (cost 4)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "A":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "C"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - B
    @action(DDRange(0, "num_kiwis"), cost=3)
    def move_kiwi_B_to_A(self, state, kiwi_idx):
        """Move a kiwi from B to A (cost 3, nobody(E))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "B":
            return None
        
        if not self._check_conditions(state, "nobody(E)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "A"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=1)
    def move_kiwi_B_to_C(self, state, kiwi_idx):
        """Move a kiwi from B to C (cost 1)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "B":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "C"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=5)
    def move_kiwi_B_to_G(self, state, kiwi_idx):
        """Move a kiwi from B to G (cost 5)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "B":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "G"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - C
    @action(DDRange(0, "num_kiwis"), cost=1)
    def move_kiwi_C_to_B(self, state, kiwi_idx):
        """Move a kiwi from C to B (cost 1)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "C":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "B"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=2)
    def move_kiwi_C_to_D(self, state, kiwi_idx):
        """Move a kiwi from C to D (cost 2, somebody(E),somebody(G))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "C":
            return None
        
        if not self._check_conditions(state, "somebody(E),somebody(G)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "D"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=4)
    def move_kiwi_C_to_A(self, state, kiwi_idx):
        """Move a kiwi from C to A (cost 4)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "C":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "A"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - D
    @action(DDRange(0, "num_kiwis"), cost=2)
    def move_kiwi_D_to_C(self, state, kiwi_idx):
        """Move a kiwi from D to C (cost 2, somebody(E),somebody(G))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(E),somebody(G)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "C"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=8)
    def move_kiwi_D_to_E(self, state, kiwi_idx):
        """Move a kiwi from D to E (cost 8, somebody(A))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(A)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "E"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=3)
    def move_kiwi_D_to_F(self, state, kiwi_idx):
        """Move a kiwi from D to F (cost 3, somebody(C))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(C)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "F"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - E
    @action(DDRange(0, "num_kiwis"), cost=8)
    def move_kiwi_E_to_D(self, state, kiwi_idx):
        """Move a kiwi from E to D (cost 8, somebody(A))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "E":
            return None
        
        if not self._check_conditions(state, "somebody(A)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "D"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=5)
    def move_kiwi_E_to_F(self, state, kiwi_idx):
        """Move a kiwi from E to F (cost 5)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "E":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "F"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - F
    @action(DDRange(0, "num_kiwis"), cost=3)
    def move_kiwi_F_to_D(self, state, kiwi_idx):
        """Move a kiwi from F to D (cost 3, somebody(C))"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "F":
            return None
        
        if not self._check_conditions(state, "somebody(C)"):
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "D"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=5)
    def move_kiwi_F_to_E(self, state, kiwi_idx):
        """Move a kiwi from F to E (cost 5)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "F":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "E"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=7)
    def move_kiwi_F_to_G(self, state, kiwi_idx):
        """Move a kiwi from F to G (cost 7)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "F":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "G"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # KIWI ACTIONS - G
    @action(DDRange(0, "num_kiwis"), cost=7)
    def move_kiwi_G_to_F(self, state, kiwi_idx):
        """Move a kiwi from G to F (cost 7)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "G":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "F"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    @action(DDRange(0, "num_kiwis"), cost=5)
    def move_kiwi_G_to_B(self, state, kiwi_idx):
        """Move a kiwi from G to B (cost 5)"""
        current_pos = state.kiwis[kiwi_idx]
        if current_pos != "G":
            return None
        
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = "B"
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # DOG ACTIONS - A
    @action(DDRange(0, "num_dogs"), cost=3)
    def move_dog_A_to_B(self, state, dog_idx):
        """Move a dog from A to B (cost 3, nobody(E))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "A":
            return None
        
        if not self._check_conditions(state, "nobody(E)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "B"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=4)
    def move_dog_A_to_C(self, state, dog_idx):
        """Move a dog from A to C (cost 4)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "A":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "C"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - B
    @action(DDRange(0, "num_dogs"), cost=3)
    def move_dog_B_to_A(self, state, dog_idx):
        """Move a dog from B to A (cost 3, nobody(E))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "B":
            return None
        
        if not self._check_conditions(state, "nobody(E)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "A"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=1)
    def move_dog_B_to_C(self, state, dog_idx):
        """Move a dog from B to C (cost 1)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "B":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "C"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=5)
    def move_dog_B_to_G(self, state, dog_idx):
        """Move a dog from B to G (cost 5)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "B":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "G"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - C
    @action(DDRange(0, "num_dogs"), cost=1)
    def move_dog_C_to_B(self, state, dog_idx):
        """Move a dog from C to B (cost 1)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "C":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "B"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=2)
    def move_dog_C_to_D(self, state, dog_idx):
        """Move a dog from C to D (cost 2, somebody(E),somebody(G))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "C":
            return None
        
        if not self._check_conditions(state, "somebody(E),somebody(G)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "D"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=4)
    def move_dog_C_to_A(self, state, dog_idx):
        """Move a dog from C to A (cost 4)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "C":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "A"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - D
    @action(DDRange(0, "num_dogs"), cost=2)
    def move_dog_D_to_C(self, state, dog_idx):
        """Move a dog from D to C (cost 2, somebody(E),somebody(G))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(E),somebody(G)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "C"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=8)
    def move_dog_D_to_E(self, state, dog_idx):
        """Move a dog from D to E (cost 8, somebody(A))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(A)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "E"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=3)
    def move_dog_D_to_F(self, state, dog_idx):
        """Move a dog from D to F (cost 3, somebody(C))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "D":
            return None
        
        if not self._check_conditions(state, "somebody(C)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "F"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - E
    @action(DDRange(0, "num_dogs"), cost=8)
    def move_dog_E_to_D(self, state, dog_idx):
        """Move a dog from E to D (cost 8, somebody(A))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "E":
            return None
        
        if not self._check_conditions(state, "somebody(A)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "D"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=5)
    def move_dog_E_to_F(self, state, dog_idx):
        """Move a dog from E to F (cost 5)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "E":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "F"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - F
    @action(DDRange(0, "num_dogs"), cost=3)
    def move_dog_F_to_D(self, state, dog_idx):
        """Move a dog from F to D (cost 3, somebody(C))"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "F":
            return None
        
        if not self._check_conditions(state, "somebody(C)"):
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "D"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=5)
    def move_dog_F_to_E(self, state, dog_idx):
        """Move a dog from F to E (cost 5)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "F":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "E"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=7)
    def move_dog_F_to_G(self, state, dog_idx):
        """Move a dog from F to G (cost 7)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "F":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "G"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    # DOG ACTIONS - G
    @action(DDRange(0, "num_dogs"), cost=7)
    def move_dog_G_to_F(self, state, dog_idx):
        """Move a dog from G to F (cost 7)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "G":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "F"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

    @action(DDRange(0, "num_dogs"), cost=5)
    def move_dog_G_to_B(self, state, dog_idx):
        """Move a dog from G to B (cost 5)"""
        current_pos = state.dogs[dog_idx]
        if current_pos != "G":
            return None
        
        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = "B"
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))