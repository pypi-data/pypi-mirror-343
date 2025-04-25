class MonkeyBananaProblem:
    def __init__(self):
        
        self.initial_state = ("door", "floor", "window", False)
        self.goal_state = ("center", "on_block", "center", True)

    def is_goal(self, state):
        """Check if the goal state is reached."""
        return state == self.goal_state

    def get_successors(self, state):
        """Generate possible next states from the current state."""
        monkey, vertical, block, has_banana = state
        successors = []
        
        
        if vertical == "floor":
            for new_pos in ["door", "window", "center"]:
                if new_pos != monkey:
                    successors.append(((new_pos, vertical, block, has_banana), f"Monkey walks to {new_pos}"))
        
        
        if vertical == "floor" and monkey == block:
            for new_pos in ["door", "window", "center"]:
                if new_pos != block:
                    successors.append(((new_pos, vertical, new_pos, has_banana), f"Monkey pushes block to {new_pos}"))
        
        
        if vertical == "floor" and monkey == block:
            successors.append(((monkey, "on_block", block, has_banana), "Monkey climbs on the block"))
        
       
        if vertical == "on_block" and block == "center":
            successors.append(((monkey, vertical, block, True), "Monkey grabs the banana"))
        
        return successors

    def solve(self):
        """Perform DFS to find the sequence of moves leading to the goal."""
        stack = [(self.initial_state, [])] 
        visited = set()
        
        while stack:
            current_state, path = stack.pop()
            
            if self.is_goal(current_state):
                return path  
            
            if current_state not in visited:
                visited.add(current_state)
                
                for next_state, action in self.get_successors(current_state):
                    stack.append((next_state, path + [action]))
        
        return None 


problem = MonkeyBananaProblem()
solution = problem.solve()

if solution:
    print("Solution found:")
    for step in solution:
        print(f"- {step}")
else:
    print("No solution found.")
