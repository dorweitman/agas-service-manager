class RunScore:
    def __init__(self, army_id, duration_in_minutes: float):
        self.army_id = army_id
        self.duration = duration_in_minutes

    def __lt__(self, other: "RunScore"):
        return self.duration < other.duration


def map_person_to_matches(scores, neighbors_count: int = 4):
    scores.sort()
    radius = int(neighbors_count / 2)
    number_of_scores = len(scores)
    user_to_neighbors_map = {}

    # Find neighbors for the first #radius Ids
    for i in range(radius):
        army_id = scores[i].army_id
        neighbors = []
        for x in range(i):
            neighbors += {scores[x]}

        neighbors_from_right = neighbors_count - i
        for j in range(i + 1, i + 1 + neighbors_from_right):
            neighbors += {scores[j]}

        user_to_neighbors_map[army_id] = neighbors

    # Get neighbors of all the Ids that have radius neighbors
    # that are bigger than them and radius neighbors that are smaller
    # than them.
    for i in range(radius, number_of_scores - radius):
        army_id = scores[i].army_id
        neighbors = []
        for j in range(i-radius, i):
            neighbors += {scores[j]}
        for j in range(i+1, i+1+radius):
            neighbors += {scores[j]}
        user_to_neighbors_map[army_id] = neighbors

    # Find neighbors for the last #radius Ids
    for i in range(number_of_scores-radius, number_of_scores):
        army_id = scores[i].army_id
        neighbors = []
        neighbors_from_right = number_of_scores - (i+1)
        neighbors_from_left = neighbors_count - neighbors_from_right

        for j in range(i - neighbors_from_left, i):
            neighbors += {scores[j]}

        for x in range(i+1, i + neighbors_from_right+1):
            neighbors += {scores[x]}

        user_to_neighbors_map[army_id] = neighbors

    return user_to_neighbors_map
