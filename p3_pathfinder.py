from math import *
from heapq import heappush, heappop


def find_path(src_point, dst_point, mesh):
    path = []
    visited_boxes = []
    queue = []

    curr_dist_forward = {}
    prev_dist_forward = {}
    curr_dist_reverse = {}
    prev_dist_reverse = {}
    detail_points = {}

    connection_found = False
    dst_box = None
    src_box = None

    for node in mesh['boxes']:
        if node[0] < src_point[0] < node[1] and node[2] < src_point[1] < node[3]:
            # Set the source box to be the current node.
            # Node contains [x1, x2, y1, y2]
            src_box = node
            visited_boxes.append(node)

        if node[0] < dst_point[0] < node[1] and node[2] < dst_point[1] < node[3]:
            # Set the destination box to be the current node.
            dst_box = node

    # Bi-directional tracking setup
    # Keep track of our search from source
    curr_dist_forward[src_box] = 0
    prev_dist_forward[src_box] = None

    # Keep track of our search from destination
    curr_dist_reverse[dst_box] = 0
    prev_dist_reverse[dst_box] = None

    #push our source and destination onto the heap
    heappush(queue, (0, src_box, dst_box))
    heappush(queue, (0, dst_box, src_box))
    detail_points[src_box] = src_point
    detail_points[dst_box] = dst_point

    # While there exists something in the queue
    while queue:
        # Pop the lowest out of the queue
        distance, curr_box, curr_goal = heappop(queue)

        # Forward search
        if curr_goal == dst_box:
            # Calculate distance to adjust path length below
            final_dist = sqrt(pow((detail_points[curr_box][0] - dst_point[0]), 2) + pow((detail_points[curr_box][1] - dst_point[1]), 2))
            distance -= final_dist

            if curr_box == dst_box or src_box is None or dst_box is None or curr_box in curr_dist_reverse:
                visited_boxes.append(curr_box)
                connection_found = True
                last_box = curr_box
                break

        # Reverse search
        elif curr_goal == src_box:
            # Calculate distance to adjust path length below
            final_dist = sqrt(pow((detail_points[curr_box][0] - src_point[0]), 2) + pow((detail_points[curr_box][1] - src_point[1]), 2))
            distance -= final_dist

            if curr_box == src_box or dst_box is None or src_box is None or curr_box in curr_dist_forward:
                visited_boxes.append(curr_box)
                connection_found = True
                last_box = curr_box
                break

        # For each connected box to the current box
        for adj_box in mesh['adj'][curr_box]:
            # If that connecting box has not yet been visited
            if adj_box not in visited_boxes:
                x, y = detail_points[curr_box]

                #for bi-directional, check for what each side is looking for
                if curr_goal == dst_box:
                    #creating the x and y min max boundings
                    x, y = detail_points[curr_box]
                    x1, x2 = adj_box[0], adj_box[1]
                    x_next = min(x2 - 1, max(x1, x))
                    y1, y2 = adj_box[2], adj_box[3]
                    y_next = min(y2 - 1, max(y1, y))
                    detail_points[adj_box] = (x_next, y_next)

                    final_dist = sqrt(pow((x_next - dst_point[0]), 2) + pow((y_next - dst_point[1]), 2))
                    #calculating next move distance
                    adj_dist = sqrt(pow((x_next - x), 2) + pow((y_next - y), 2))
                    #djikstra's distance adding
                    path_len = distance + adj_dist

                if curr_goal == src_box:
                	#creating the x and y min max boundings
                    x, y = detail_points[curr_box]
                    x1, x2 = adj_box[0], adj_box[1]
                    x_next = min(x2 - 1, max(x1, x))
                    y1, y2 = adj_box[2], adj_box[3]
                    y_next = min(y2 - 1, max(y1, y))
                    detail_points[adj_box] = (x_next, y_next)

                    final_dist = sqrt(pow((x_next - src_point[0]), 2) + pow((y_next - src_point[1]), 2))
                    #calculating next move distance
                    adj_dist = sqrt(pow((x_next - x), 2) + pow((y_next - y), 2))
                    #djikstra's distance adding
                    path_len = distance + adj_dist


                # Adjust the path length based on the distance calculations above



                if curr_goal == dst_box:
                    if adj_box not in curr_dist_forward or path_len < curr_dist_forward[adj_box]:

                        curr_dist_forward[adj_box] = path_len
                        prev_dist_forward[adj_box] = curr_box

                        heappush(queue, (path_len + final_dist, adj_box, dst_box))
                        last_box = curr_box

                if curr_goal == src_box:
                    if adj_box not in curr_dist_reverse or path_len < curr_dist_reverse[adj_box]:

                        curr_dist_reverse[adj_box] = path_len
                        prev_dist_reverse[adj_box] = curr_box

                        heappush(queue, (path_len + final_dist, adj_box, src_box))
                        last_box = curr_box

        visited_boxes.append(curr_box)



    if connection_found:
        curr_forward_box = last_box
        while curr_forward_box and prev_dist_forward[curr_forward_box]:
            path.append((detail_points[curr_forward_box], detail_points[prev_dist_forward[curr_forward_box]]))
            curr_forward_box = prev_dist_forward[curr_forward_box]

        curr_reverse_box = last_box
        while curr_reverse_box and prev_dist_reverse[curr_reverse_box]:
            path.append((detail_points[curr_reverse_box], detail_points[prev_dist_reverse[curr_reverse_box]]))
            curr_reverse_box = prev_dist_reverse[curr_reverse_box]
      
    else:
        print "No path found."

    return path, visited_boxes

