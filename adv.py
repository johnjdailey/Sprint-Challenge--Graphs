#adv.py



from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval


# Load world

world = World()


# You may uncomment the smaller graphs for development and testing purposes.

# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary

room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map

world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


#CODE BEGINS HERE

#Prior to traversing the entire map, we need to understand which rooms are connected to each other.
#To do this, we shall start in our starting room, and check which rooms are connected to it
#those connected rooms are then recursively evaluated until the entire grid is populated

#this works because all rooms are connected in one larger graph

def room_recursive(starting_room,room_graph,room_paths=None,visited=None):
    """
    This function shows the path of how rooms are connected together.
    starting_room = The node in the graph we are evaluating neighbors of
    room_graph = The overall map of the adventure maze we are exploring
    room_paths = The linked paths that a room can lead to, default value of None.
        Populated on a per room basis during the recursive search
    visited = The list of rooms that have been searched
    """
    
    # If no room has been visited yet, initialize an empty list

    if visited is None:
        visited = []

    # If a room's directions is not defined yet, create a dictionary

    if room_paths is None:
        room_paths = {}

    # Grab the current room's ID

    room_id = starting_room.id

    # If that room ID is not in the pathing dictionary

    if room_id not in room_paths.keys():

        # Add that room ID to the visited list

        visited.append(room_id)

        # In the room_paths dictionary, add this room as a key

        room_paths[room_id] = {}

        # Grab the directions for that starting room

        directions = starting_room.get_exits()

        # For each direction the room has...

        for dir in directions:

            # Update the room_paths dictionary so at the key of the room ID
            # Each direction the room has from the get_exits function
            # Attach that direction, and the ID of the connected room

            room_paths[room_id].update({dir:starting_room.get_room_in_direction(dir).id})

        # Shuffle the directions a room has to have a non-deterministic crawl

        directions = starting_room.get_exits()
        random.shuffle(directions)

        # For each direction our starting_room has connected to it,
        # Walk the path to that new room

        for direction in directions:
            new_room = starting_room.get_room_in_direction(direction)

            # Recursively apply the same logic above to the next room!

            room_recursive(new_room,room_graph,room_paths,visited)

        if len(room_paths) == len(room_graph):
            return room_paths,visited


def bfs(starting_room, destination_room,room_paths):
    """
    Using Breadth First Search
    This will return the shortest path between a starting room and a destination room
    starting_room = Room ID of starting room
    destination_room = Room ID of destination room.
    room_paths = The linked paths that a room can lead to, default value of None.
        (generated from recursive_room_population function)
    """

    # Create a list of visited rooms:
    # Keeping track of previously visited rooms will expedite the bfs

    visited = set()

    # Setting up a queue of rooms to explore
    # A queue is used since it is first in first out
    # which naturally orientates to breadth first search since newly discovered nodes are processed
    # All other nodes in the queue are analyzed
    # A queue will necessarily show the shortest path for a given route because of this attribute

    room_queue = Queue()

    # Direction queue will queue up the directions to travel

    dir_queue = Queue()

    # The queue is initialized with the starting room

    room_queue.enqueue([starting_room])

    # The direction queue is initialized as a blank list, since no movement has occurred yet

    dir_queue.enqueue([])
    
    # While there are rooms in the queue to evaluate...

    while room_queue.size() > 0:

        # Take the next value in the queue

        vertex_path = room_queue.dequeue()

        # Take the next direction to travel in that queue

        dir_path = dir_queue.dequeue()

        # The last room in the room_path taken from the queue
        # is the newest explored room

        vertex = vertex_path[-1]

        # If that room has not been visited before

        if vertex not in visited:
            visited.add(vertex)

            # If the new room is the desired destination

            if vertex == destination_room:
                return dir_path

            # Then, for each direction that a room has mapped to it in the room_path dictionary

            for direction in room_paths[vertex]:

                # Copy the room_path and travel_path queues

                path_copy = vertex_path.copy()
                dirpath_copy = dir_path.copy()
                
                # Add the newest room and directions to the copied room_path route

                path_copy.append(room_paths[vertex][direction])
                dirpath_copy.append(direction)
                room_queue.enqueue(path_copy)
                dir_queue.enqueue(dirpath_copy)


# Initialize the answer list of traversal path

traversal_path = []

# Set the player in the world's starting room

player = Player(world.starting_room)

# Visit all rooms with the recursion function

room_dict,visited = room_recursive(world.starting_room,room_graph)

# For each room in the visited list

for i in range(len(visited)-1):

    # Set path as the shortest pathway between two rooms

    path = bfs(visited[i],visited[i+1],room_dict)

    # Add the path of the navigation between those two rooms to the traversal path list

    traversal_path.extend(path)


# TRAVERSAL TEST - DO NOT MODIFY

visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# TESTS PASSED: 996 moves, 500 rooms visited


#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
